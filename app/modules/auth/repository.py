from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.modules.users.model import User, UserRole
from app.modules.permissions.model import Role, Permission, RolePermission

# Method to get user by email
async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return await db.scalar(stmt)

# Method to update user profile
async def update_user(db: AsyncSession, user_id: str, **kwargs):

    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(**kwargs)
    )

    result = await db.execute(stmt)
    await db.commit()

# Method to get user with role
async def get_user_with_role(db: AsyncSession, email: str):
    stmt = (
        select(User, UserRole)
        .join(UserRole, UserRole.user_id == User.id)
        .where(User.email == email)
    )

    result = await db.execute(stmt)
    row = result.first()

    if not row:
        return None

    user, user_role = row
    return user, user_role

# Method to fetch role name and permissions
async def get_role_and_permissions(db: AsyncSession, role_id):
    stmt = (
        select(Role.name, Permission.code)
        .join(RolePermission, RolePermission.role_id == Role.id)
        .join(Permission, Permission.id == RolePermission.permission_id)
        .where(Role.id == role_id)
    )

    result = await db.execute(stmt)
    rows = result.all()

    if not rows:
        return None

    role_name = rows[0][0]
    permissions = [row[1] for row in rows]

    return role_name, permissions

# Method to get the roles based on the given scope type
async def get_roles_by_scope_type(db: AsyncSession, scope_type: str):
    stmt = select(Role).where(Role.scope_type == scope_type)
    result = await db.execute(stmt)
    return result.scalars().all()

# Method to get the role by role id
async def get_role_by_id(db: AsyncSession, role_id: str):
    stmt = select(Role).where(Role.id == role_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()