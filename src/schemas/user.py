from typing import Optional

from pydantic import BaseModel


from typing import List


class UserCreate(BaseModel):
    name: str
    last_name: Optional[str] = None
    username: str
    phone_number: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: str
    last_name: Optional[str] = None
    username: str
    phone_number: Optional[str] = None
