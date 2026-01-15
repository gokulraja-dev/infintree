from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import get_user_by_email, update_user
from app.core.security import verify_password, hash_password
from app.core.jwt.issuer import create_access_token
from app.core.security import validate_password_complexity
from .schemas import SetPasswordRequest

# Method to authenticate user and generate token
async def authenticate_user(db: AsyncSession, email: str, password: str):
    if not email or not password:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email and password are required")

    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials or user not found")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    if user.default_password is True:
        raise HTTPException(status_code=status.HTTP_428_PRECONDITION_REQUIRED, detail="Password change required")

    return {
        "access_token": create_access_token(user, aud="infintree"),
        "token_type": "bearer"
    }

# Method to change user's default password
async def update_user_password(db: AsyncSession, request: SetPasswordRequest):
    user = await get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    if user.default_password is False:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Password change not allowed for this user")
    
    if not verify_password(request.old_password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Old password is incorrect")

    if request.old_password == request.new_password:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "New password must be different from old password")

    if request.new_password != request.confirm_password:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "New password and confirmation do not match")

    if not validate_password_complexity(request.new_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "New password does not meet complexity requirements")
    
    hashed_password = hash_password(request.new_password)

    await update_user(db, user.id, password_hash=hashed_password, default_password=False)

    return {"msg": "Password updated successfully"}