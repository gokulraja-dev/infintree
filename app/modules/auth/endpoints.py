from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.debs import get_db
from typing import Annotated
from .usecases import authenticate_user, update_user_password, get_roles
from .schemas import SetPasswordRequest, RoleScope
from app.core.permission_dependancy import require_permission
from app.modules.users.model import User

# Roter Initialization
router = APIRouter()

# Dependencies
db = Annotated[AsyncSession, Depends(get_db)]

# Endpoint to handle user login
@router.post("/login")
async def login(db: db, form: OAuth2PasswordRequestForm = Depends()):
    resp = await authenticate_user(db, form.username, form.password)
    return resp

# Endpoint to change user's default password
@router.post("/set-password")
async def set_password_endpoint(db: db, request: SetPasswordRequest):
    resp = await update_user_password(db, request)
    return resp

# Endpoint to get roles
@router.get("/roles")
async def get_roles_endpoint(db: db, scope: RoleScope, current_user: User = Depends(require_permission("user.read"))):
    resp = await get_roles(db, scope.value.lower())
    return resp