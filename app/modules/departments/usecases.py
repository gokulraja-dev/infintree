from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .schemas import CreateDepartmentRequest, UpdateDepartmentRequest, CreateDepartmentUserRequest
from .repository import create_department, get_departments, get_department, get_department_by_name, update_department, delete_department, create_department_user, assign_user_to_department, get_user_by_email, get_users_in_department, get_user_by_id, delete_user_from_department, get_department_user
from app.modules.auth.repository import get_role_by_id
from app.core.security import hash_password

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

# Method to create a department user
async def create_department_user_usecase(db: AsyncSession, payload: CreateDepartmentUserRequest):
   # Step: 1 - Check if the given department exists
    department = await get_department(db, payload.department_id)

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    # Step: 2 - Check if the given role exists
    role = await get_role_by_id(db, payload.role_id)

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    # Step: 3 - Create the department user
    
    # Check if the given email already exists
    existing_user = await get_user_by_email(db, payload.email)

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    # Preparing the user data
    user_data = {
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "email": payload.email,
        "password_hash": hash_password(payload.password),
        "user_type": payload.user_type,
        "default_password": True,
    }

    # Creating the user
    user_create_resp = await create_department_user(db, **user_data)

    if not user_create_resp:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create department user")

    # Step: 4 - Assign the user to the department
    user_assign_resp = await assign_user_to_department(db, user_create_resp.id, payload.department_id, payload.role_id)

    if not user_assign_resp:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to assign user to department")

    # Step: 5 - Return the created department user
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "Department user created successfully"})

# Method to get all the users in departments
async def get_all_users_in_departments_usecase(db: AsyncSession, department_id: str):
    # Constants
    USERS = []

    # Step: 1 - Check if the given department exists
    department = await get_department(db, department_id)

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    # Step: 2 - Get all the users in the department
    department_users = await get_users_in_department(db, department_id)

    for user in department_users:
        USERS.append({
            "user_id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "user_type": user.user_type,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        })


    # Step: 3 - Return the users in the department
    return JSONResponse(status_code=status.HTTP_200_OK, content={"users": jsonable_encoder(USERS)})

# Method to remove user from department
async def remove_user_from_department_usecase(db: AsyncSession, department_id: str, user_id: str):
    # Step: 1 - Check if the given department exists
    department = await get_department(db, department_id)

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    # Step: 2 - Check if the given user exists
    user = await get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Step : 3 - Check if the given user is in the department
    department_user = await get_department_user(db, user_id, department_id)

    if not department_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in the department")

    # Step: 4 - Remove the user from the department
    if not await delete_user_from_department(db, user_id, department_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to remove user from department")

    # Step: 5 - Return the removed user from the department
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "User removed from department successfully"})