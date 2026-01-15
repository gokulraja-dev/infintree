import json, os, base64
from fastapi import HTTPException, status
from authlib.jose import jwt, JsonWebKey
from app.core.jwt.key_store import get_jwks
from app.core.security import decode_jwt_header

LEEWAY = int(os.getenv("JWT_LEEWAY", 60))


def verify_token(token: str, aud: str):
    try:
        header = decode_jwt_header(token)
        kid = header.get("kid")
        if not kid:
            raise HTTPException(401, "Missing kid")

        jwks = get_jwks()
        jwk_dict = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if not jwk_dict:
            raise HTTPException(401, "Unknown signing key")

        key = JsonWebKey.import_key(jwk_dict)

        claims = jwt.decode(
            token,
            key,
            claims_options={
                "exp": {"essential": True},
                "aud": {"essential": True, "value": aud},
            },
            claims_params={"leeway": LEEWAY}
        )

        claims.validate()
        return dict(claims)

    except HTTPException:
        raise
    except Exception as e:
        print("JWT VERIFY ERROR:", e)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
