from typing import Optional

from src.models.base import Base


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from typing import List


class User(Base):
    """
    id: int
    name: str
    last_name: str
    username: str
    phone_number: str
    """

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    phone_number: Mapped[str | None] = mapped_column(String(20), unique=True)

    # Обратная связь для комментариев
    commentary: Mapped[List["Commentary"]] = relationship(  # type: ignore
        back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, last_name={self.last_name!r})"
