import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date
from models.base import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    stock: Mapped[int]
    created_at: Mapped[datetime.date] = mapped_column(Date)

    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="product")
