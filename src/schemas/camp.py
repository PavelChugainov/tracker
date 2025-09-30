from typing import Optional

from pydantic import BaseModel, ConfigDict


from typing import List
from src.schemas.address import AddressCreate


class Camp(BaseModel):
    """A base model that allows protocols to be used for fields."""

    model_config = ConfigDict(arbitrary_types_allowed=True)


class CampCreate(Camp):
    name: str
    address: AddressCreate
    rating: Optional[float] = None
    price: Optional[float] = None


class CampOut(Camp):
    id: int
    name: str
    address: AddressCreate
    rating: Optional[float] = None
    price: Optional[float] = None
