from src.database.models.base import Base


from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    coordinate: Mapped[str] = mapped_column(String(50))
    camp_id: Mapped[int] = mapped_column(ForeignKey("camp.id"))
    distance: Mapped[float] = mapped_column(Float)

    camp: Mapped["Camp"] = relationship(back_populates="address")  # type: ignore

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, coordinate={self.coordinate!r}, distance={self.distance!r})"
