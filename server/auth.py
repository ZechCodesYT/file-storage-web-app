from hashlib import sha256
import os


def hash_password(password: str) -> str:
    salt = os.getenv("PASSWORD_SALT", "SALT")
    salted = f"{salt}{password}"
    hashed = salted.encode()
    for _ in range(100):
        hashed = sha256(hashed).hexdigest().encode()

    return hashed.decode()


def check_password_matches(password: str, hashed_password: str) -> bool:
    hashed = hash_password(password)
    return hashed == hashed_password
