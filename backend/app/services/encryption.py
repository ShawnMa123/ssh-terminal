"""
Encryption service for sensitive data
"""
from cryptography.fernet import Fernet
from ..config import settings


class EncryptionService:
    """Handles encryption and decryption of sensitive data"""

    def __init__(self):
        self.cipher = Fernet(settings.encryption_key.encode())

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext string

        Args:
            plaintext: Plain text to encrypt

        Returns:
            Base64 encoded encrypted string
        """
        if not plaintext:
            return ""

        encrypted_bytes = self.cipher.encrypt(plaintext.encode())
        return encrypted_bytes.decode()

    def decrypt(self, encrypted: str) -> str:
        """
        Decrypt encrypted string

        Args:
            encrypted: Base64 encoded encrypted string

        Returns:
            Decrypted plaintext
        """
        if not encrypted:
            return ""

        decrypted_bytes = self.cipher.decrypt(encrypted.encode())
        return decrypted_bytes.decode()


# Global encryption service instance
encryption_service = EncryptionService()
