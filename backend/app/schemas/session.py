"""
Session Pydantic schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    """Schema for creating a session"""
    # Option 1: Connect using saved server
    server_id: Optional[int] = Field(None, gt=0)
    credential_id: Optional[int] = Field(None, gt=0)

    # Option 2: Quick connect with direct parameters
    host: Optional[str] = None
    port: Optional[int] = Field(None, ge=1, le=65535)
    username: Optional[str] = None
    password: Optional[str] = None
    private_key: Optional[str] = None

    # Terminal settings
    terminal_cols: int = Field(default=80, ge=20, le=500)
    terminal_rows: int = Field(default=24, ge=10, le=200)


class SessionResponse(BaseModel):
    """Schema for session response"""
    id: int
    session_id: str
    server_id: Optional[int] = None
    credential_id: Optional[int] = None
    status: str
    log_file_path: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    terminal_cols: int
    terminal_rows: int

    class Config:
        from_attributes = True


class SessionUpdate(BaseModel):
    """Schema for updating session"""
    terminal_cols: Optional[int] = Field(None, ge=20, le=500)
    terminal_rows: Optional[int] = Field(None, ge=10, le=200)
    status: Optional[str] = Field(None, pattern="^(active|closed|error)$")
