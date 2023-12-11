from django.db.models import CharField
from cryptography.fernet import Fernet
from django.conf import settings

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import base64


class SecureCharField(CharField):
    """Encrypted Field"""

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 512
        super().__init__(*args, **kwargs)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=bytes(settings.SECURE_SALT, "utf-8"),
        iterations=100000,
        backend=default_backend()
    )

    # Encode the FERNET encryption key
    key = base64.urlsafe_b64encode(kdf.derive(
        bytes(settings.ENCRYPTION_KEY, "utf-8")
    ))

    # Create a "fernet" object using the key stored in the .env file
    f = Fernet(key)

    def from_db_value(self, value: str, expression, connection) -> str:
        """
        Decrypts the value retrieved from the database.
        """
        value = str(self.f.decrypt(bytes(value, 'cp1252')), encoding='utf-8')
        return value

    def get_prep_value(self, value: str) -> str:
        """
        Encrypts the value before storing it in the database.
        """
        value = str(self.f.encrypt(bytes(value, 'utf-8')), 'cp1252')
        return value
