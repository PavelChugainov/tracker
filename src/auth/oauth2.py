from fastapi.security import OAuth2PasswordBearer
from src.api_v1.users.schemas import User
from fastapi import Depends
from typing import Annotated

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    return User(
        id=0,
        name="fake_name",
        username="fake_username",
        email="gchugaino@gmail.com",
        password="somepass",
    )


async def get_current_user(token: Annotated[str, Depends(oauth_scheme)]):
    user = fake_decode_token(token)
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password
