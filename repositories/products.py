from typing import Any, List
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.order import OrderItem
from models.product import Product
from repositories.base import BaseRepository
from schemas.products import SProductBase


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: Session):
        super().__init__(session, Product)

    def get_products_list(self) -> List[Product]:
        return self.get_list()

    def create(self, product: SProductBase) -> Product:
        new_product = Product(**product.model_dump())
        new_product.id = uuid4()
        self.session.add(new_product)
        self.session.commit()
        self.session.refresh(new_product)
        return new_product

    def update(self, id: UUID, data: dict[str, Any]) -> Product | None:
        product = self.get(id)
        if not product:
            return None
        for field, value in data.items():
            setattr(product, field, value)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_popular_products(self, limit: int) -> List[Product]:
        return list(self.session.scalars(
            select(Product)
            .join(Product.items)
            .group_by(Product.id)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
        ))
