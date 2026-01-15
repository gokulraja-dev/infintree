from datetime import datetime, timedelta, timezone
from authlib.jose import jwt
import os
from app.core.jwt.key_store import get_active_key

JWT_EXP_MIN = int(os.getenv("JWT_EXP_MIN", 60))


def create_access_token(user, aud: str = "infintree"):
    kid, key = get_active_key()
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user.id),
        "email": user.email,
        "aud": aud,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXP_MIN)).timestamp()),
    }

    return jwt.encode({"alg": "RS256", "kid": kid}, payload, key).decode()
