from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from src.models.user import User
from src.database.db_helper import get_session
from src.database.crud import get_camp_by_id, create_camp
from src.schemas.camp import CampOut, CampCreate


router = APIRouter(prefix="/camps", tags=["camps"])


@router.post("/", response_model=CampOut, status_code=status.HTTP_200_OK)
async def create_camp_endpoint(
    camp_data: CampCreate, session: AsyncSession = Depends(get_session)
):
    """Create new camp"""
    try:
        camp = await create_camp(camp_data, session)
        return camp
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error due camp creation: {str(e)}",
        )
