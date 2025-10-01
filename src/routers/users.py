from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from fastapi.security import OAuth2PasswordBearer


from src.models.user import User
from src.database.db_helper import get_session
from src.database.crud import create_user, get_user_by_id, get_users
from src.schemas.user import UserCreate, UserOut, UserBase

router = APIRouter(prefix="/users", tags=["users"])

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/users", response_model=list[UserOut], status_code=status.HTTP_200_OK)
async def get_users_endpoint(session: AsyncSession = Depends(get_session)):

    try:
        users = await get_users(session)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error due getting user's list{e}",
        )
    return None


@router.get("/items")
async def read_items(token: Annotated[str, Depends(oauth_scheme)]):
    return {"token": token}


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
):
    """Create new user with one or several addresses"""
    try:
        res = await create_user(user_data, session)
        user = res.__dict__

        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error due user creation: {str(e)}",
        )


@router.get("/", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    """Get user by id"""
    try:
        user = await get_user_by_id(user_id, session)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error due getting user by id: {e}",
        )
