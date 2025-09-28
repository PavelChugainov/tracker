from src.models.base import Base


from sqlalchemy import Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


from typing import List


class Camp(Base):
    __tablename__ = "camp"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Связь "один к одному" с Address
    address: Mapped["Address"] = relationship(back_populates="camp")  # type: ignore

    reviews: Mapped[List["Review"]] = relationship(  # type: ignore
        back_populates="camp", cascade="all, delete-orphan"
    )

    rating: Mapped[float] = mapped_column(Float)
    price: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"Camp(id={self.id!r}, rating={self.rating!r}, price={self.price!r})"
