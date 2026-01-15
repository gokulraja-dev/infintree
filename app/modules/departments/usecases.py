from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .schemas import CreateDepartmentRequest, UpdateDepartmentRequest
from .repository import create_department, get_departments, get_department, get_department_by_name, update_department, delete_department

# Method to create a new department
async def create_department_usecase(db: AsyncSession, request: CreateDepartmentRequest):
    # Step: 1 - Check if the department already exists
    existing_department = await get_department_by_name(db, request.name)
    if existing_department:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department already exists")
    
    # Step: 2 - Create the department
    department = await create_department(db, request.name, request.description)
    if not department:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create department")
    
    # Step: 3 - Return the created department
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Department created successfully"})

# Method to get all departments
async def get_all_departments_usecase(db: AsyncSession):
    departments = await get_departments(db)

    if not departments:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"departments": []})
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"departments": jsonable_encoder(departments)})

# Method to get a department by ID
async def get_department_usecase(db: AsyncSession, department_id: str):
    
    department = await get_department(db, department_id)

    if not department:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"department": {}})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"department": jsonable_encoder(department)})


# Method to update a department
async def update_department_usecase(db: AsyncSession, department_id: str, request: UpdateDepartmentRequest):

    # Step: 1 - Check if the department exists
    department = await get_department(db, department_id)

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    
    # Step: 2 - Check if the department name already exists
    existing_department = await get_department_by_name(db, request.name)
    if existing_department and str(existing_department.id) != str(department_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department name already exists")
    
    # Step: 3 - Update the department
    updated_department = await update_department(db, department_id, name=request.name, description=request.description)

    if not updated_department:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to update department")
    
    # Step: 4 - Return the updated department
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Department updated successfully"})


# Method to delete a department
async def delete_department_usecase(db: AsyncSession, department_id: str):
    # Step: 1 - Check if the department exists
    department = await get_department(db, department_id)

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    
    # Step: 2 - Delete the department
    if not await delete_department(db, department_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to delete department")
    
    # Step: 3 - Return the deleted department
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Department deleted successfully"})