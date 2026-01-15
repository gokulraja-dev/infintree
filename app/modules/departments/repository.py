from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from .model import Department

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