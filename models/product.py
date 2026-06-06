from __future__ import annotations

import datetime
from uuid import UUID

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Product(Base):
    __tablename__ = "products"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    stock: Mapped[int]
    created_at: Mapped[datetime.date] = mapped_column(Date)

    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="product")  # type: ignore[name-defined]
