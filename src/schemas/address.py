from typing import Optional

from pydantic import BaseModel


from typing import List


class Address(BaseModel):
    pass


class AddressCreate(Address):
    coordinate: str
    distance: Address


class AddressOut(Address):
    id: int
    coordinate: str
    distance: Address
