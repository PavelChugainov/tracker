from pydantic import BaseModel, EmailStr, ConfigDict

from typing import List


class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: str
    is_verified: bool


class UserReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass
