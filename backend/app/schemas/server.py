"""
Server Pydantic schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ServerBase(BaseModel):
    """Base server schema"""
    name: str = Field(..., min_length=1, max_length=100)
    host: str = Field(..., min_length=1, max_length=255)
    port: int = Field(default=22, ge=1, le=65535)
    username: Optional[str] = Field(None, max_length=100)
    auth_type: Optional[str] = Field(None, pattern="^(password|key)$")
    credential_id: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[str] = None


class ServerCreate(ServerBase):
    """Schema for creating a server"""
    pass


class ServerUpdate(BaseModel):
    """Schema for updating a server"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    host: Optional[str] = Field(None, min_length=1, max_length=255)
    port: Optional[int] = Field(None, ge=1, le=65535)
    username: Optional[str] = Field(None, max_length=100)
    auth_type: Optional[str] = Field(None, pattern="^(password|key)$")
    credential_id: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[str] = None


class ServerResponse(ServerBase):
    """Schema for server response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
