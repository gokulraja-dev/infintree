from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

# Schema for create department request
class CreateDepartmentRequest(BaseModel):
    name: str
    description: Optional[str]

# Schema for update department request
class UpdateDepartmentRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]

# Enum for department user role
class DepartmentUserRole(str, Enum):
    DEPARTMENT_MANAGER = "DEPARTMENT_MANAGER"
    DEPARTMENT_VIEWER = "DEPARTMENT_VIEWER"

# Schema for create department user request
class CreateDepartmentUserRequest(BaseModel):
    department_id: str
    role_id: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    user_type: DepartmentUserRole
