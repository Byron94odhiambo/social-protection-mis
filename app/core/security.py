# app/core/security.py
from cryptography.fernet import Fernet
import os
from base64 import b64encode, b64decode
from dotenv import load_dotenv

load_dotenv()

def get_encryption_key():
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        # Generate a new key if none exists
        key = Fernet.generate_key()
        # Save to .env file
        with open(".env", "a") as env_file:
            env_file.write(f"\nENCRYPTION_KEY={key.decode()}")
    else:
        # Convert string key back to bytes if loaded from .env
        try:
            key = key.encode()
        except AttributeError:
            pass
    return key

ENCRYPTION_KEY = get_encryption_key()
fernet = Fernet(ENCRYPTION_KEY)

def encrypt_phone(phone: str) -> str:
    return b64encode(fernet.encrypt(phone.encode())).decode()

def decrypt_phone(encrypted_phone: str) -> str:
    return fernet.decrypt(b64decode(encrypted_phone)).decode()