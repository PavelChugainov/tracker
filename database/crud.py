from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, UserCreate, AddressCreate, Address


async def get_user(user_id: int, session: AsyncSession) -> User | None:
    res = await session.execute(select(User).where(User.id == user_id))
    user = res.scalars().first()
    return user

async def create_user(
        user_data: UserCreate,
        session: AsyncSession
        ) -> User:
    # Convert Pydantic model to ORM model
    new_user = User(
        name=user_data.name,
        last_name=user_data.last_name,
    )
    # Handle address: assume user_data.address is List[AddressModel]
    for addr_data in user_data.addresses:
        address = Address(email_address=addr_data.email_address)
        new_user.addresses.append(address)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user
