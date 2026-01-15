from fastapi import Depends, HTTPException
from sqlalchemy import select
from app.core.auth import get_current_user
from app.db.debs import get_db
from app.modules.users.model import UserRole
from app.modules.permissions.model import Permission, RolePermission


def require_permission(permission_code: str):
    async def dependency(user=Depends(get_current_user), db=Depends(get_db)):
        # ROOT ADMIN bypass
        if user.user_type == "ROOT_ADMIN":
            return user

        result = await db.scalar(
            select(UserRole)
            .join(RolePermission, RolePermission.role_id == UserRole.role_id)
            .join(Permission, Permission.id == RolePermission.permission_id)
            .where(
                UserRole.user_id == user.id,
                Permission.code == permission_code
            )
        )

        if not result:
            raise HTTPException(403, "Permission denied")

        return user

    return dependency
