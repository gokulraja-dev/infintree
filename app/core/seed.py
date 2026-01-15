from sqlalchemy import select
from app.modules.users.model import User, UserRole
from app.modules.permissions.model import Role
from app.core.iam_loader import load_iam_policies
from app.core.security import hash_password
import os

ROOT_EMAIL = os.getenv("ROOT_ADMIN_EMAIL", "root@infintree.io")
ROOT_PASSWORD = os.getenv("ROOT_ADMIN_PASSWORD", "ChangeMeNow!")


async def seed_system(db):

    # 1 Load IAM policies
    await load_iam_policies(db)

    # 2 Create Root Admin user
    root = await db.scalar(select(User).where(User.email == ROOT_EMAIL))
    if not root:
        root = User(
            email=ROOT_EMAIL,
            first_name="Root",
            last_name="Admin",
            password_hash=hash_password(ROOT_PASSWORD),
            default_password=True,
            user_type="ROOT_ADMIN"
        )
        db.add(root)
        await db.commit()

    # 3 Assign ROOT_ADMIN role
    root_role = await db.scalar(select(Role).where(Role.name == "ROOT_ADMIN"))
    if not await db.scalar(select(UserRole).where(
        UserRole.user_id == root.id,
        UserRole.role_id == root_role.id
    )):
        db.add(UserRole(user_id=root.id, role_id=root_role.id))
        await db.commit()
