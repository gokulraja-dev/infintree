from pydantic import BaseModel, EmailStr

# Schema for Update user's default password request
class SetPasswordRequest(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str
    confirm_password: str