from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from models.user import User
from models.product import Product
from repositories.orders import OrderRepository
from schemas.orders import SOrder, SOrderCreate


class OrderService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = OrderRepository(session)

    def get_orders_list(self) -> List[SOrder]:
        return [SOrder.model_validate(o) for o in self.repo.get_orders_list()]

    def get_order(self, id: UUID) -> SOrder | None:
        order = self.repo.get(id)
        if not order:
            return None
        return SOrder.model_validate(order)

    def create_order(self, data: SOrderCreate) -> SOrder:
        user = self.session.get(User, data.user_id)
        if not user:
            raise ValueError(f"User {data.user_id} not found")

        for item in data.items:
            product = self.session.get(Product, item.product_id)
            if not product:
                raise ValueError(f"Product {item.product_id} not found")
            if product.stock < item.quantity:
                raise ValueError(
                    f"Not enough stock for product {item.product_id}: "
                    f"requested {item.quantity}, available {product.stock}"
                )

        for item in data.items:
            product = self.session.get(Product, item.product_id)
            product.stock -= item.quantity

        return SOrder.model_validate(self.repo.create(data))

    def delete_order(self, id: UUID) -> bool:
        order = self.repo.get(id)
        if not order:
            return False

        for item in order.items:
            product = self.session.get(Product, item.product_id)
            if product:
                product.stock += item.quantity

        return self.repo.delete(id)
