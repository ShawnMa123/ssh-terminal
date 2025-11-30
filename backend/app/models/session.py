"""
SSH Session model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class SSHSession(Base):
    """SSH Session model for tracking active and historical sessions"""

    __tablename__ = "ssh_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(64), unique=True, nullable=False, index=True)
    server_id = Column(Integer, ForeignKey("ssh_servers.id"), nullable=False)
    status = Column(String(20), nullable=False, default="active")  # active, closed, error
    log_file_path = Column(String(512), nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    terminal_cols = Column(Integer, default=80, nullable=False)
    terminal_rows = Column(Integer, default=24, nullable=False)

    # Relationships
    server = relationship("SSHServer", back_populates="sessions")

    def __repr__(self):
        return f"<SSHSession(id={self.id}, session_id='{self.session_id}', status='{self.status}')>"
