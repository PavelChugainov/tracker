from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Address
from sqlalchemy.orm import selectinload

from database.db_helper import logger
from database.schemas import AddressCreate, UserCreate


async def get_user(user_id: int, session: AsyncSession) -> User | None:
    stmt = select(User).options(selectinload(User.addresses)).where(User.id == user_id)
    res = await session.execute(stmt)
    user = res.scalars().first()
    return user


async def create_user(user_data: UserCreate, session: AsyncSession) -> User | None:
    # Convert Pydantic model to ORM model
    try:
        new_user = User(
            name=user_data.name,
            last_name=user_data.last_name,
        )
        # Handle address: assume user_data.address is List[AddressModel]
        for addr_data in user_data.addresses:
            address = Address(email_address=addr_data.email_address)
            new_user.addresses.append(address)
        logger.info("trying to add user")
        session.add(new_user)
        logger.info("user added")
        await session.commit()
        await session.refresh(new_user)

        return await get_user(new_user.id, session=session)
    except Exception as e:
        logger.info(f"error in crud {e}")
        await session.rollback()
        return None
