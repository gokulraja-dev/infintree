from pydantic import BaseModel, EmailStr
from enum import Enum

# Schema for Update user's default password request
class SetPasswordRequest(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str
    confirm_password: str

# Enumuration for available roles scopes
class RoleScope(str, Enum):
    SYSTEM = "system"
    DEPARTMENT = "department"
    GROUP = "group"