"""
Application configuration management
"""
import os
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = "Web SSH Client"
    app_version: str = "0.1.0"
    debug: bool = Field(default=False, env="DEBUG")

    # Server
    backend_host: str = Field(default="0.0.0.0", env="BACKEND_HOST")
    backend_port: int = Field(default=8000, env="BACKEND_PORT")

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/ssh_client.db",
        env="DATABASE_URL"
    )

    # Security
    encryption_key: str = Field(..., env="ENCRYPTION_KEY")

    # CORS
    allowed_origins: Union[List[str], str] = Field(
        default=["http://localhost:5173", "http://localhost:80"],
        env="ALLOWED_ORIGINS"
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse comma-separated string into list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # Logging
    log_dir: str = Field(default="./logs", env="LOG_DIR")

    # Session
    max_sessions: int = Field(default=100, env="MAX_SESSIONS")
    session_timeout: int = Field(default=3600, env="SESSION_TIMEOUT")  # seconds

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


# Ensure required directories exist
os.makedirs(settings.log_dir, exist_ok=True)
os.makedirs("./data", exist_ok=True)
