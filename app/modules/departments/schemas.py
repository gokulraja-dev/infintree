from pydantic import BaseModel
from typing import Optional

# Schema for create department request
class CreateDepartmentRequest(BaseModel):
    name: str
    description: Optional[str]

# Schema for update department request
class UpdateDepartmentRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]