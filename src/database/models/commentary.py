from src.database.models.base import Base


from sqlalchemy import DATE, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from datetime import datetime


class Commentary(Base):
    __tablename__ = "commentary"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    date: Mapped[datetime] = mapped_column(DATE)

    author: Mapped["User"] = relationship(back_populates="commentary")  # type: ignore
    review_id: Mapped[str] = mapped_column(ForeignKey("review.id"))  # type: ignore

    def __repr__(self) -> str:
        return f"Commentary(id={self.id!r}, text={self.text!r}, date={self.date!r})"
