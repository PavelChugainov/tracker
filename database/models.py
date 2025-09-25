from typing import List, Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, Float, Integer, DATE
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20))

    # Обратная связь для комментариев
    comments: Mapped[List["Commentary"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, last_name={self.last_name!r})"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    coordinate: Mapped[str] = mapped_column(String(50))
    camp_id: Mapped[int] = mapped_column(ForeignKey("camp.id"))
    distance: Mapped[float] = mapped_column(Float)

    camp: Mapped["Camp"] = relationship(back_populates="address")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, coordinate={self.coordinate!r}, distance={self.distance!r})"


class Camp(Base):
    __tablename__ = "camp"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Связь "один к одному" с Address
    address: Mapped["Address"] = relationship(back_populates="camp")

    reviews: Mapped[List["Review"]] = relationship(
        back_populates="camp", cascade="all, delete-orphan"
    )

    rating: Mapped[float] = mapped_column(Float)
    price: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"Camp(id={self.id!r}, rating={self.rating!r}, price={self.price!r})"


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[int] = mapped_column(Integer)

    camp_id: Mapped[int] = mapped_column(ForeignKey("camp.id"))
    camp: Mapped["Camp"] = relationship(back_populates="reviews")

    def __repr__(self) -> str:
        return f"Review(id={self.id!r}, rating={self.rating!r})"


class Commentary(Base):
    __tablename__ = "commentary"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    date: Mapped[datetime] = mapped_column(DATE)

    author: Mapped["User"] = relationship(back_populates="comments")

    def __repr__(self) -> str:
        return f"Commentary(id={self.id!r}, text={self.text!r}, date={self.date!r})"
