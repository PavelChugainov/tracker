from src.database.db_helper import logger
from src.database.models.user import User
from src.api_v1.users.schemas import UserCreate


from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    try:
        stmt = select(User).where(User.id == user_id)
        res = await session.execute(stmt)
        user = res.scalar_one_or_none()
        return user
    except Exception as e:
        logger.info(f"Error due get user by id in crud {e}")
        return None


async def get_user(session: AsyncSession, user_username: str | None) -> User | None:
    stmt = select(User).where(User.username == user_username)
    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user
    # return await session.get(User, user_username)


async def get_users(session: AsyncSession) -> list[User] | None:
    stmt = select(User).order_by(User.id)
    res = await session.execute(stmt)
    return list(res.scalars().all())


async def create_user(user_data: UserCreate, session: AsyncSession) -> User | None:
    # Convert Pydantic model to ORM model
    try:
        new_user = User(
            name=user_data.name,
            username=user_data.username,
            email=user_data.email,
        )
        session.add(new_user)
        logger.info("user added")
        await session.commit()
        await session.refresh(new_user)

        return await get_user_by_id(new_user.id, session=session)
    except Exception as e:
        logger.info(f"Error due user creation {e}")
        await session.rollback()
        return None
