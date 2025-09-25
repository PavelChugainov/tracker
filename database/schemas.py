from typing import Optional

from pydantic import BaseModel


from typing import List


class AddressCreate(BaseModel):
    email_address: str


class UserCreate(BaseModel):
    name: str
    last_name: Optional[str] = None
    addresses: List["AddressCreate"]


class AddressOut(BaseModel):
    id: int
    email_address: str


class UserOut(BaseModel):
    id: int
    name: str
    last_name: Optional[str] = None
    addresses: List["AddressOut"]
