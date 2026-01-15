from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.modules.users.model import User

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