"""
Credential Pydantic schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CredentialBase(BaseModel):
    """Base credential schema"""
    name: str = Field(..., min_length=1, max_length=100)
    credential_type: str = Field(..., pattern="^(password|private_key)$")


class CredentialCreate(CredentialBase):
    """Schema for creating a credential"""
    password: Optional[str] = None
    private_key: Optional[str] = None
    passphrase: Optional[str] = None


class CredentialUpdate(BaseModel):
    """Schema for updating a credential"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = None
    private_key: Optional[str] = None
    passphrase: Optional[str] = None


class CredentialResponse(CredentialBase):
    """Schema for credential response (no sensitive data)"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
