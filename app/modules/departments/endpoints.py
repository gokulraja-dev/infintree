from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.debs import get_db
from app.core.permission_dependancy import require_permission
from app.modules.users.model import User
from .schemas import CreateDepartmentRequest, UpdateDepartmentRequest
from .usecases import create_department_usecase, get_all_departments_usecase, get_department_usecase, update_department_usecase, delete_department_usecase

# Router initialization
router = APIRouter()

# Dependencies
db = Annotated[AsyncSession, Depends(get_db)]

# Endpoint to create a new department
@router.post("")
async def create_department_endpoint(db: db, request: CreateDepartmentRequest, current_user: User = Depends(require_permission("departments.create"))):
    resp = await create_department_usecase(db, request)
    return resp

# Endpoint to get all departments or single department by ID
@router.get("")
async def get_all_departments_endpoint(db: db, department_id: str = None, current_user: User = Depends(require_permission("departments.read"))):

    if department_id:
        resp = await get_department_usecase(db, department_id)
        return resp
    
    resp = await get_all_departments_usecase(db)
    return resp

# Endpoint to update a department by ID
@router.put("")
async def update_department_endpoint(db: db, department_id: str, request: UpdateDepartmentRequest, current_user: User = Depends(require_permission("departments.update"))):
    resp = await update_department_usecase(db, department_id, request)
    return resp

# Endpoint to delete a department by ID
@router.delete("")
async def delete_department_endpoint(db: db, department_id: str, current_user: User = Depends(require_permission("departments.delete"))):
    resp = await delete_department_usecase(db, department_id)
    return resp