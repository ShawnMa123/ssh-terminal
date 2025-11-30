"""
Session Pydantic schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    """Schema for creating a session"""
    server_id: int = Field(..., gt=0)
    terminal_cols: int = Field(default=80, ge=20, le=500)
    terminal_rows: int = Field(default=24, ge=10, le=200)


class SessionResponse(BaseModel):
    """Schema for session response"""
    id: int
    session_id: str
    server_id: int
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
