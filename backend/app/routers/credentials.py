"""
Credentials CRUD API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..models.credential import Credential
from ..schemas.credential import CredentialCreate, CredentialResponse
from ..services.encryption import encryption_service


router = APIRouter(prefix="/api/credentials", tags=["credentials"])


@router.get("/", response_model=List[CredentialResponse])
async def list_credentials(db: AsyncSession = Depends(get_db)):
    """Get list of all credentials"""
    result = await db.execute(select(Credential))
    credentials = result.scalars().all()
    return credentials


@router.get("/{credential_id}", response_model=CredentialResponse)
async def get_credential(credential_id: int, db: AsyncSession = Depends(get_db)):
    """Get specific credential by ID"""
    result = await db.execute(
        select(Credential).where(Credential.id == credential_id)
    )
    credential = result.scalar_one_or_none()

    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")

    return credential


@router.post("/", response_model=CredentialResponse, status_code=201)
async def create_credential(
    credential_data: CredentialCreate, db: AsyncSession = Depends(get_db)
):
    """Create new credential with encrypted password/private key"""
    # Encrypt sensitive data
    encrypted_password = None
    encrypted_private_key = None

    if credential_data.password:
        encrypted_password = encryption_service.encrypt(credential_data.password)

    if credential_data.private_key:
        encrypted_private_key = encryption_service.encrypt(credential_data.private_key)

    # Create credential
    credential = Credential(
        name=credential_data.name,
        username=credential_data.username,
        encrypted_password=encrypted_password,
        encrypted_private_key=encrypted_private_key,
        description=credential_data.description,
    )

    db.add(credential)
    await db.commit()
    await db.refresh(credential)

    return credential


@router.delete("/{credential_id}", status_code=204)
async def delete_credential(credential_id: int, db: AsyncSession = Depends(get_db)):
    """Delete credential"""
    result = await db.execute(
        select(Credential).where(Credential.id == credential_id)
    )
    credential = result.scalar_one_or_none()

    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")

    await db.delete(credential)
    await db.commit()

    return None
