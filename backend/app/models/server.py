"""
SSH Server model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class SSHServer(Base):
    """SSH Server configuration model"""

    __tablename__ = "ssh_servers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    host = Column(String(255), nullable=False)
    port = Column(Integer, default=22, nullable=False)
    username = Column(String(100), nullable=True)
    auth_type = Column(String(20), nullable=True)  # 'password' or 'key'
    credential_id = Column(Integer, ForeignKey("credentials.id"), nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(String(255), nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    credential = relationship("Credential", back_populates="servers")
    sessions = relationship("SSHSession", back_populates="server", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SSHServer(id={self.id}, name='{self.name}', host='{self.host}:{self.port}')>"
