"""
SSH Servers CRUD API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..models.server import SSHServer
from ..schemas.server import ServerCreate, ServerUpdate, ServerResponse


router = APIRouter(prefix="/api/servers", tags=["servers"])


@router.get("/", response_model=List[ServerResponse])
async def list_servers(db: AsyncSession = Depends(get_db)):
    """Get list of all SSH servers"""
    result = await db.execute(select(SSHServer))
    servers = result.scalars().all()
    return servers


@router.get("/{server_id}", response_model=ServerResponse)
async def get_server(server_id: int, db: AsyncSession = Depends(get_db)):
    """Get specific SSH server by ID"""
    result = await db.execute(select(SSHServer).where(SSHServer.id == server_id))
    server = result.scalar_one_or_none()

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    return server


@router.post("/", response_model=ServerResponse, status_code=201)
async def create_server(
    server_data: ServerCreate, db: AsyncSession = Depends(get_db)
):
    """Create new SSH server"""
    # Check if server with same name exists
    result = await db.execute(
        select(SSHServer).where(SSHServer.name == server_data.name)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400, detail=f"Server with name '{server_data.name}' already exists"
        )

    # Create server
    server = SSHServer(**server_data.model_dump())
    db.add(server)
    await db.commit()
    await db.refresh(server)

    return server


@router.put("/{server_id}", response_model=ServerResponse)
async def update_server(
    server_id: int, server_data: ServerUpdate, db: AsyncSession = Depends(get_db)
):
    """Update SSH server"""
    result = await db.execute(select(SSHServer).where(SSHServer.id == server_id))
    server = result.scalar_one_or_none()

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    # Update fields
    update_data = server_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(server, field, value)

    await db.commit()
    await db.refresh(server)

    return server


@router.delete("/{server_id}", status_code=204)
async def delete_server(server_id: int, db: AsyncSession = Depends(get_db)):
    """Delete SSH server"""
    result = await db.execute(select(SSHServer).where(SSHServer.id == server_id))
    server = result.scalar_one_or_none()

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    await db.delete(server)
    await db.commit()

    return None
