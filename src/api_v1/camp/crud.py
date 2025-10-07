from src.database.db_helper import logger
from src.database.models.camp import Camp
from src.api_v1.camp.schemas import CampCreate


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


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