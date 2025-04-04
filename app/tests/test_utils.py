import pytest
from app.utils import encrypt_password, decrypt_password
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", Fernet.generate_key().decode())
fernet = Fernet(SECRET_KEY.encode())


# Unit-tests for encryption/decryption of passwords


def test_encrypt_password():
    password = "secretpassword"

    encrypted_password = encrypt_password(password)

    assert encrypted_password != password
    assert isinstance(encrypted_password, str)

    decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
    assert decrypted_password == password


def test_decrypt_password():
    password = "secret_password"

    encrypted_password = encrypt_password(password)

    decrypted_password = decrypt_password(encrypted_password)

    assert decrypted_password == password
