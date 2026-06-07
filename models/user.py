from __future__ import annotations

import datetime
from uuid import UUID

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    created_at: Mapped[datetime.date] = mapped_column(Date)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user", cascade="all, delete-orphan")  # type: ignore[name-defined]
