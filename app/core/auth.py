from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from authlib.jose import jwt
from app.db.debs import get_db
from app.modules.users.model import User
from sqlalchemy import select
from  .jwt.verifier import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = verify_token(token, "infintree")
        user_id = payload["sub"]
    except Exception:
        raise HTTPException(401, "Invalid token")

    user = await db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(401)
    return user
