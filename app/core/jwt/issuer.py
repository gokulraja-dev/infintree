from datetime import datetime, timedelta, timezone
from authlib.jose import jwt
import os
from app.core.jwt.key_store import get_active_key

JWT_EXP_MIN = int(os.getenv("JWT_EXP_MIN", 60))


def create_access_token(user, role_name, permissions, user_role, aud="infintree"):
    # Constants
    SCOPE_TYPE = None
    SCOPE_ID = None

    kid, key = get_active_key()
    now = datetime.now(timezone.utc)

    # Scope detection
    if user_role.department_id:
        SCOPE_TYPE = "department"
        SCOPE_ID = str(user_role.department_id)

    elif user_role.group_id:
        SCOPE_TYPE = "group"
        SCOPE_ID = str(user_role.group_id)

    else:
        SCOPE_TYPE = "system"
        SCOPE_ID = None

    payload = {
        "sub": str(user.id),
        "email": user.email,
        "roles": [role_name],
        "permissions": permissions,
        "scope": {
            "type": SCOPE_TYPE,
            "id": SCOPE_ID
        },
        "aud": aud,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXP_MIN)).timestamp()),
    }

    return jwt.encode({"alg": "RS256", "kid": kid}, payload, key).decode()
