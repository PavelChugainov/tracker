from src.database.db_helper import logger
from src.database.models.user import User
from src.api_v1.users.schemas import UserCreate, UserReadSchema

from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.utils import hash_password


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


async def create_user(session: AsyncSession, user_in: UserCreate) -> UserReadSchema:
    # check if user with the same username or email is already exist
    stmt = select(User).where(
        (User.email == user_in.email) | (User.username == user_in.username)
    )
    result: Result = await session.execute(stmt)
    user = result.scalars().first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email is already exist",
        )
    # hash password
    hashed_password = hash_password(user_in.password)
    db_user = User(
        name=user_in.name,
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return UserReadSchema.model_validate(db_user)
