from src.database.models.base import Base


from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[int] = mapped_column(Integer)

    camp_id: Mapped[int] = mapped_column(ForeignKey("camp.id"))
    camp: Mapped["Camp"] = relationship(back_populates="reviews")  # type: ignore

    def __repr__(self) -> str:
        return f"Review(id={self.id!r}, rating={self.rating!r})"
