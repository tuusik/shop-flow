from models.product import Product
from models.order import OrderItem
from uuid import UUID, uuid4
from schemas.products import SProductBase
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import List

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, id: UUID) -> Product | None:
        return self.session.get(Product, id)

    def get_products_list(self) -> List[Product]:
        return list(self.session.scalars(select(Product)))

    def create(self, product: SProductBase):
        new_product = Product(**product.model_dump())
        new_product.id = uuid4()
        self.session.add(new_product)
        self.session.commit()
        self.session.refresh(new_product)
        return new_product

    def update(self, id: UUID, data: dict) -> Product | None:
        product = self.get(id)
        if not product:
            return None
        for field, value in data.items():
            setattr(product, field, value)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, id: UUID) -> bool:
        product = self.get(id)
        if not product:
            return False
        self.session.delete(product)
        self.session.commit()
        return True

    def get_popular_products(self, limit: int) -> List[Product]:
        return list(self.session.scalars(
            select(Product)
            .join(Product.items)
            .group_by(Product.id)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
        ))