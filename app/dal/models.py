from typing import List
from datetime import datetime

from . import Base

from sqlalchemy import Integer, Float, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    parent_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    parent: Mapped["Category"] = relationship(back_populates='children')
    children: Mapped[List["Category"]] = relationship(back_populates='parent')


class Building(Base):
    __tablename__ = 'buildings'

    id: Mapped[int] = mapped_column(primary_key=True)
    territory: Mapped[str] = mapped_column(String(100))
    area: Mapped[int] = mapped_column(String(100))
    sell_type: Mapped[str] = mapped_column(String(20))
    room_number: Mapped[int] = mapped_column(Integer)
    land_area: Mapped[float] = mapped_column(Float)
    building_area: Mapped[float] = mapped_column(Float)
    price: Mapped[int] = mapped_column(BigInteger)
    floor: Mapped[int] = mapped_column(Integer)
    floor_number: Mapped[int] = mapped_column(Integer)
    building_repair: Mapped[str] = mapped_column(Text)
    type_of_ad: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    source: Mapped[str] = mapped_column(String(20))

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
