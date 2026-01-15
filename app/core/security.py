from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
import re

pwd_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16
)

def hash_password(password: str) -> str:
    return pwd_hasher.hash(password)

def verify_password(password: str, stored: str) -> bool:
    try:
        return pwd_hasher.verify(stored, password)
    except VerifyMismatchError:
        return False

# Decode jwt header without verification
def decode_jwt_header(token: str) -> dict:
    try:
        headers = jwt.get_unverified_header(token)
        return headers
    except jwt.PyJWTError:
        return {}

# Validate password complexity
def validate_password_complexity(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True