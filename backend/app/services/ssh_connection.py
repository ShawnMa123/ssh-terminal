"""
SSH Connection handler using Paramiko
"""
import asyncio
import logging
from typing import Optional, Callable
from datetime import datetime
import paramiko
from paramiko.channel import Channel


logger = logging.getLogger(__name__)


class SSHConnection:
    """Manages a single SSH connection with PTY support"""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: Optional[str] = None,
        private_key: Optional[str] = None,
        server_name: Optional[str] = None,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.private_key = private_key
        self.server_name = server_name or host

        self.client: Optional[paramiko.SSHClient] = None
        self.channel: Optional[Channel] = None
        self.connected = False
        self.session_id: Optional[str] = None

        # Callbacks
        self.on_data: Optional[Callable[[bytes], None]] = None
        self.on_disconnect: Optional[Callable[[], None]] = None

        # Logging
        self.log_buffer = []
        self.log_file_path: Optional[str] = None

    async def connect(self) -> bool:
        """
        Establish SSH connection

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Create SSH client
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Prepare authentication
            auth_kwargs = {
                "hostname": self.host,
                "port": self.port,
                "username": self.username,
            }

            if self.password:
                auth_kwargs["password"] = self.password
            elif self.private_key:
                # Load private key
                from io import StringIO
                key_file = StringIO(self.private_key)
                auth_kwargs["pkey"] = paramiko.RSAKey.from_private_key(key_file)

            # Connect in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None, lambda: self.client.connect(**auth_kwargs, timeout=10)
            )

            # Open PTY channel
            self.channel = self.client.invoke_shell(
                term="xterm-256color", width=80, height=24
            )
            self.channel.setblocking(0)

            self.connected = True
            logger.info(f"SSH connected to {self.host}:{self.port}")

            # Start reading output
            asyncio.create_task(self._read_loop())

            return True

        except Exception as e:
            logger.error(f"SSH connection failed: {e}")
            await self.disconnect()
            return False

    async def send(self, data: str) -> bool:
        """
        Send data to SSH channel

        Args:
            data: String data to send

        Returns:
            True if sent successfully
        """
        if not self.connected or not self.channel:
            return False

        try:
            self.channel.send(data)
            self._log_data(f">> {data}", is_input=True)
            return True
        except Exception as e:
            logger.error(f"Failed to send data: {e}")
            return False

    async def resize(self, width: int, height: int) -> bool:
        """
        Resize PTY terminal

        Args:
            width: Terminal width in characters
            height: Terminal height in characters

        Returns:
            True if resized successfully
        """
        if not self.connected or not self.channel:
            return False

        try:
            self.channel.resize_pty(width=width, height=height)
            logger.debug(f"Terminal resized to {width}x{height}")
            return True
        except Exception as e:
            logger.error(f"Failed to resize terminal: {e}")
            return False

    async def disconnect(self):
        """Close SSH connection and cleanup"""
        self.connected = False

        if self.channel:
            try:
                self.channel.close()
            except:
                pass
            self.channel = None

        if self.client:
            try:
                self.client.close()
            except:
                pass
            self.client = None

        # Save logs
        await self._save_logs()

        # Trigger disconnect callback
        if self.on_disconnect:
            try:
                self.on_disconnect()
            except:
                pass

        logger.info(f"SSH disconnected from {self.host}:{self.port}")

    async def _read_loop(self):
        """Background task to read SSH output"""
        while self.connected and self.channel:
            try:
                # Check if data available
                if self.channel.recv_ready():
                    data = self.channel.recv(4096)
                    if data:
                        # Log data
                        self._log_data(data.decode("utf-8", errors="replace"), is_input=False)

                        # Send to callback
                        if self.on_data:
                            try:
                                import inspect
                                result = self.on_data(data)
                                # If callback is async, schedule it as a task
                                if inspect.iscoroutine(result):
                                    asyncio.create_task(result)
                            except Exception as e:
                                logger.error(f"Error in data callback: {e}")

                # Check if channel closed
                if self.channel.exit_status_ready():
                    logger.info("SSH channel closed by server")
                    await self.disconnect()
                    break

                # Small delay to prevent CPU spinning
                await asyncio.sleep(0.01)

            except Exception as e:
                logger.error(f"Error in read loop: {e}")
                await self.disconnect()
                break

    def _log_data(self, data: str, is_input: bool):
        """
        Log SSH session data

        Args:
            data: Data to log
            is_input: True if data is user input, False if server output
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        direction = "INPUT" if is_input else "OUTPUT"
        log_entry = f"[{timestamp}] {direction}: {data}"

        self.log_buffer.append(log_entry)

        # Flush buffer if too large (>100 entries)
        if len(self.log_buffer) > 100:
            asyncio.create_task(self._save_logs())

    async def _save_logs(self):
        """Save buffered logs to file"""
        if not self.log_buffer or not self.log_file_path:
            return

        try:
            import aiofiles

            async with aiofiles.open(self.log_file_path, "a", encoding="utf-8") as f:
                await f.write("\n".join(self.log_buffer) + "\n")

            self.log_buffer.clear()
            logger.debug(f"Logs saved to {self.log_file_path}")

        except Exception as e:
            logger.error(f"Failed to save logs: {e}")

    def set_log_file(self, file_path: str):
        """
        Set log file path

        Args:
            file_path: Absolute path to log file
        """
        self.log_file_path = file_path
