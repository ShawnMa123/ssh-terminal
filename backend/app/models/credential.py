"""
Credential model for encrypted storage
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Credential(Base):
    """Credential model for storing encrypted passwords and keys"""

    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    credential_type = Column(String(20), nullable=False)  # 'password' or 'private_key'
    encrypted_password = Column(Text, nullable=True)
    encrypted_private_key = Column(Text, nullable=True)
    passphrase_encrypted = Column(Text, nullable=True)  # For private key passphrase
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    servers = relationship("SSHServer", back_populates="credential")

    def __repr__(self):
        return f"<Credential(id={self.id}, name='{self.name}', type='{self.credential_type}')>"
