"""
SSH Sessions API
"""
from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..models.server import SSHServer
from ..models.credential import Credential
from ..models.session import SSHSession
from ..schemas.session import SessionCreate, SessionResponse
from ..services.ssh_manager import ssh_manager
from ..services.encryption import encryption_service


router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.get("/", response_model=List[SessionResponse])
async def list_sessions(
    active_only: bool = False, db: AsyncSession = Depends(get_db)
):
    """Get list of SSH sessions"""
    query = select(SSHSession)

    if active_only:
        query = query.where(SSHSession.status == "active")

    result = await db.execute(query)
    sessions = result.scalars().all()
    return sessions


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    """Get specific session by ID"""
    result = await db.execute(
        select(SSHSession).where(SSHSession.session_id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.post("/", response_model=SessionResponse, status_code=201)
async def create_session(
    session_data: SessionCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create new SSH session and establish connection

    Requires either server_id or direct connection parameters
    """
    # Generate unique session ID
    session_id = str(uuid.uuid4())

    # Get connection parameters
    if session_data.server_id:
        # Load from saved server
        result = await db.execute(
            select(SSHServer).where(SSHServer.id == session_data.server_id)
        )
        server = result.scalar_one_or_none()

        if not server:
            raise HTTPException(status_code=404, detail="Server not found")

        host = server.host
        port = server.port
        server_name = server.name

        # Get credentials
        if session_data.credential_id:
            result = await db.execute(
                select(Credential).where(Credential.id == session_data.credential_id)
            )
            credential = result.scalar_one_or_none()

            if not credential:
                raise HTTPException(status_code=404, detail="Credential not found")

            username = credential.username
            password = (
                encryption_service.decrypt(credential.encrypted_password)
                if credential.encrypted_password
                else None
            )
            private_key = (
                encryption_service.decrypt(credential.encrypted_private_key)
                if credential.encrypted_private_key
                else None
            )
        else:
            raise HTTPException(
                status_code=400, detail="credential_id required when using server_id"
            )

    else:
        # Direct connection parameters
        if not all([session_data.host, session_data.username]):
            raise HTTPException(
                status_code=400,
                detail="host and username required for direct connection",
            )

        host = session_data.host
        port = session_data.port or 22
        username = session_data.username
        password = session_data.password
        private_key = session_data.private_key
        server_name = host

    # Establish SSH connection
    success, error = await ssh_manager.create_connection(
        session_id=session_id,
        host=host,
        port=port,
        username=username,
        password=password,
        private_key=private_key,
        server_name=server_name,
    )

    if not success:
        raise HTTPException(status_code=500, detail=error or "Failed to connect")

    # Create session record
    session = SSHSession(
        session_id=session_id,
        server_id=session_data.server_id,
        credential_id=session_data.credential_id,
        status="active",
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)

    return session


@router.delete("/{session_id}", status_code=204)
async def close_session(session_id: str, db: AsyncSession = Depends(get_db)):
    """Close SSH session and disconnect"""
    # Get session record
    result = await db.execute(
        select(SSHSession).where(SSHSession.session_id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Disconnect SSH
    await ssh_manager.remove_connection(session_id)

    # Update session status
    session.status = "closed"
    await db.commit()

    return None


@router.get("/active/count")
async def get_active_session_count():
    """Get count of active SSH sessions"""
    count = ssh_manager.get_session_count()
    return {"active_sessions": count}
