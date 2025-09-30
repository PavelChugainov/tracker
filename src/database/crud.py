from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.address import Address
from sqlalchemy.orm import selectinload

from src.database.db_helper import logger
from src.schemas.user import UserCreate
from src.schemas.camp import CampCreate
from src.models.user import User
from src.models.camp import Camp


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    try:
        stmt = select(User).where(User.id == user_id)
        res = await session.execute(stmt)
        user = res.scalar_one_or_none()
        return user
    except Exception as e:
        logger.info(f"Error due get user by id in crud {e}")
        return None


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

        return await get_user_by_id(new_user.id, session=session)
    except Exception as e:
        logger.info(f"Error due user creation {e}")
        await session.rollback()
        return None


async def get_camp_by_id(camp_id: int, session: AsyncSession) -> Camp | None:
    stmt = (
        select(Camp)
        .options(selectinload(Camp.address))
        .options(selectinload(Camp.reviews))
        .where(Camp.id == camp_id)
    )
    res = await session.execute(stmt)
    camp = res.scalar_one_or_none()
    return camp


async def create_camp(camp_data: CampCreate, session: AsyncSession) -> Camp | None:
    try:
        new_camp = Camp(
            name=camp_data.name,
            address=camp_data.address,
            price=camp_data.price,
        )
        session.add(new_camp)
        logger.info("new camp added")
        await session.commit()
        await session.refresh(new_camp)

        return await get_camp_by_id(new_camp.id, session=session)
    except Exception as e:
        logger.info(f"Error due camp creation {e}")
        await session.rollback()
        return None
