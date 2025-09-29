from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.address import Address
from sqlalchemy.orm import selectinload

from src.database.db_helper import logger
from src.schemas.user import UserCreate
from src.models.user import User


async def get_user(user_id: int, session: AsyncSession) -> User | None:
    stmt = select(User).options(selectinload(User.commentary)).where(User.id == user_id)
    res = await session.execute(stmt)
    user = res.scalars().first()
    return user


async def create_user(user_data: UserCreate, session: AsyncSession) -> User | None:
    # Convert Pydantic model to ORM model
    try:
        new_user = User(
            name=user_data.name,
            last_name=user_data.last_name,
            username=user_data.username,
            phone_number=user_data.phone_number,
        )
        session.add(new_user)
        logger.info("user added")
        await session.commit()
        await session.refresh(new_user)

        return await get_user(new_user.id, session=session)
    except Exception as e:
        logger.info(f"error in crud {e}")
        await session.rollback()
        return None
