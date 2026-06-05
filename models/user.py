import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date
from models.base import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    created_at: Mapped[datetime.date] = mapped_column(Date)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user", cascade="all, delete-orphan")
