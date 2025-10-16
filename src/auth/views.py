from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from src.api_v1.users.schemas import UserLoginSchema
from src.auth import utils as auth_utils
from src.api_v1.users import crud
from src.database.db_helper import get_session
from src.database.models import User

http_bearer = HTTPBearer()

router = APIRouter(prefix="/jwt", tags=["JWT"])


class InvalidTokenError(BaseException):
    pass


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


async def validate_auth_user(
    session: AsyncSession = Depends(get_session),
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (
        user := await crud.get_user(
            session=session,
            user_username=username,
        )
    ):
        raise unauthed_exc

    stmt = select(User.password_hash).where(User.username == username)
    result: Result = await session.execute(stmt)
    hashed_password = result.scalar_one_or_none()

    if not hashed_password:
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=hashed_password,
    ):
        raise unauthed_exc

    return user


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> UserLoginSchema:
    token = credentials.credentials
    try:

        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


async def get_current_auth_user(
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(get_current_token_payload),
):
    username: str | None = payload.get("sub")
    if user := await crud.get_user(
        session=session,
        user_username=username,
    ):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid(user not found)",
    )


def get_current_verified_auth_user(
    user: UserLoginSchema = Depends(get_current_auth_user),
):
    if user.is_verified:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user isn't verified",
    )


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(user: UserLoginSchema = Depends(validate_auth_user)):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.get("/users/me/")
def get_user_check_self_info(
    user: UserLoginSchema = Depends(get_current_verified_auth_user),
):
    return {
        "username": user.username,
        "email": user.email,
    }
