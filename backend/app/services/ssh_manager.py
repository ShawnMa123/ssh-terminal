"""
SSH Connection Manager - manages multiple SSH connections
"""
import asyncio
import logging
from typing import Dict, Optional
from datetime import datetime
import os
from .ssh_connection import SSHConnection
from ..config import settings


logger = logging.getLogger(__name__)


class SSHConnectionManager:
    """Manages multiple SSH connections with session tracking"""

    def __init__(self):
        self.connections: Dict[str, SSHConnection] = {}
        self._lock = asyncio.Lock()

    async def create_connection(
        self,
        session_id: str,
        host: str,
        port: int,
        username: str,
        password: Optional[str] = None,
        private_key: Optional[str] = None,
        server_name: Optional[str] = None,
    ) -> tuple[bool, Optional[str]]:
        """
        Create and establish new SSH connection

        Args:
            session_id: Unique session identifier
            host: SSH server host
            port: SSH server port
            username: SSH username
            password: SSH password (if using password auth)
            private_key: Private key content (if using key auth)
            server_name: Friendly server name for logging

        Returns:
            Tuple of (success, error_message)
        """
        async with self._lock:
            # Check if session already exists
            if session_id in self.connections:
                return False, "Session already exists"

            # Check max sessions limit
            if len(self.connections) >= settings.max_sessions:
                return False, f"Max sessions limit ({settings.max_sessions}) reached"

            # Create connection
            connection = SSHConnection(
                host=host,
                port=port,
                username=username,
                password=password,
                private_key=private_key,
                server_name=server_name,
            )

            connection.session_id = session_id

            # Setup log file
            log_file = self._get_log_file_path(server_name or host)
            connection.set_log_file(log_file)

            # Setup disconnect callback
            def on_disconnect():
                asyncio.create_task(self.remove_connection(session_id))

            connection.on_disconnect = on_disconnect

            # Attempt connection
            success = await connection.connect()

            if success:
                self.connections[session_id] = connection
                logger.info(
                    f"SSH session {session_id} created: {username}@{host}:{port}"
                )
                return True, None
            else:
                return False, "Failed to establish SSH connection"

    async def remove_connection(self, session_id: str) -> bool:
        """
        Remove and disconnect SSH connection

        Args:
            session_id: Session identifier

        Returns:
            True if removed successfully
        """
        async with self._lock:
            connection = self.connections.get(session_id)
            if not connection:
                return False

            await connection.disconnect()
            del self.connections[session_id]

            logger.info(f"SSH session {session_id} removed")
            return True

    def get_connection(self, session_id: str) -> Optional[SSHConnection]:
        """
        Get SSH connection by session ID

        Args:
            session_id: Session identifier

        Returns:
            SSHConnection instance or None
        """
        return self.connections.get(session_id)

    async def send_data(self, session_id: str, data: str) -> bool:
        """
        Send data to SSH connection

        Args:
            session_id: Session identifier
            data: Data to send

        Returns:
            True if sent successfully
        """
        connection = self.get_connection(session_id)
        if not connection:
            return False

        return await connection.send(data)

    async def resize_terminal(
        self, session_id: str, width: int, height: int
    ) -> bool:
        """
        Resize terminal for SSH connection

        Args:
            session_id: Session identifier
            width: Terminal width
            height: Terminal height

        Returns:
            True if resized successfully
        """
        connection = self.get_connection(session_id)
        if not connection:
            return False

        return await connection.resize(width, height)

    async def disconnect_all(self):
        """Disconnect all active SSH connections"""
        async with self._lock:
            session_ids = list(self.connections.keys())

            for session_id in session_ids:
                connection = self.connections.get(session_id)
                if connection:
                    await connection.disconnect()

            self.connections.clear()
            logger.info("All SSH sessions disconnected")

    def get_active_sessions(self) -> list[str]:
        """
        Get list of active session IDs

        Returns:
            List of session IDs
        """
        return list(self.connections.keys())

    def get_session_count(self) -> int:
        """
        Get count of active sessions

        Returns:
            Number of active sessions
        """
        return len(self.connections)

    def _get_log_file_path(self, server_name: str) -> str:
        """
        Generate log file path for server

        Args:
            server_name: Server name

        Returns:
            Absolute path to log file
        """
        # Create server-specific log directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        server_dir = os.path.join(settings.log_dir, server_name)
        os.makedirs(server_dir, exist_ok=True)

        # Log file name: {server_name}_{timestamp}.log
        log_file = os.path.join(server_dir, f"{server_name}_{timestamp}.log")
        return log_file


# Global SSH connection manager instance
ssh_manager = SSHConnectionManager()
