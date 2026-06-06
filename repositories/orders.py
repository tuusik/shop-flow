from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List
from models.order import Order, OrderItem
from schemas.orders import SOrderCreate
from repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: Session):
        super().__init__(session, Order)

    def get_orders_list(self) -> List[Order]:
        return self.get_list()

    def create(self, order: SOrderCreate) -> Order:
        new_order = Order(user_id=order.user_id, created_at=order.created_at)
        new_order.id = uuid4()
        for item in order.items:
            order_item = OrderItem(product_id=item.product_id, quantity=item.quantity)
            order_item.id = uuid4()
            new_order.items.append(order_item)
        self.session.add(new_order)
        self.session.commit()
        self.session.refresh(new_order)
        return new_order

    def get_products_in_order(self, id: UUID) -> List[OrderItem] | None:
        order = self.get(id)
        if not order:
            return None
        return list(self.session.scalars(select(OrderItem).where(OrderItem.order_id == id)))
