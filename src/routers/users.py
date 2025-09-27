from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from src.models.user import User
from database.db_helper import get_session
from database.crud import create_user, get_user
from src.schemas.user import UserCreate, UserOut


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
):
    """Create new user with one or several addresses"""
    try:
        user = await create_user(user_data, session)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error due user creation: {str(e)}",
        )
