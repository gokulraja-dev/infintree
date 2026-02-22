from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from .model import Department
from app.modules.users.model import User, UserRole

# Method to create a new department
async def create_department(db: AsyncSession, name: str, description: str = None):
    department = Department(name=name, description=description)
    db.add(department)
    await db.commit()
    await db.flush()
    await db.refresh(department)
    return department

# Method to get all departments
async def get_departments(db: AsyncSession):
    stmt = select(Department)
    result = await db.execute(stmt)
    return result.scalars().all()

# Method to get a department by ID
async def get_department(db: AsyncSession, department_id: str):
    stmt = select(Department).where(Department.id == department_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Method to get a department by department name
async def get_department_by_name(db: AsyncSession, name: str):
    stmt = select(Department).where(Department.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Method to update a department
async def update_department(db: AsyncSession, department_id: str, **kwargs):
    stmt = (
        update(Department)
        .where(Department.id == department_id)
        .values(**kwargs)
    )

    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

# Method to delete a department
async def delete_department(db: AsyncSession, department_id: str):
    stmt = delete(Department).where(Department.id == department_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

# Method to create a new department user using kwargs
async def create_department_user(db: AsyncSession, **kwargs):
    department_user = User(**kwargs)
    db.add(department_user)
    await db.commit()
    await db.flush()
    await db.refresh(department_user)
    return department_user

# Method to assing a user to a department in user role table
async def assign_user_to_department(db: AsyncSession, user_id: str, department_id: str, role_id: str):
    user_role = UserRole(user_id=user_id, role_id=role_id, department_id=department_id)
    db.add(user_role)
    await db.commit()
    await db.flush()
    await db.refresh(user_role)
    return user_role

# Method to get the user by user id
async def get_user_by_id(db: AsyncSession, user_id: str):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Method to get the user by email
async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Method to get all users in a department
async def get_users_in_department(db: AsyncSession, department_id: str):
    stmt = select(User).join(UserRole, UserRole.user_id == User.id).where(UserRole.department_id == department_id)
    result = await db.execute(stmt)
    return result.scalars().all()

# Method to delete a user from a department
async def delete_user_from_department(db: AsyncSession, user_id: str, department_id: str):
    stmt = delete(UserRole).where(UserRole.user_id == user_id, UserRole.department_id == department_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

# Method to delete a user
async def delete_user(db: AsyncSession, user_id: str):
    stmt = delete(User).where(User.id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

# Method to get the department user by user id and department id
async def get_department_user(db: AsyncSession, user_id: str, department_id: str):
    stmt = select(UserRole).where(UserRole.user_id == user_id, UserRole.department_id == department_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()