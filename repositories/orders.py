from models.order import Order, OrderItem
from uuid import UUID, uuid4
from schemas.orders import SOrderCreate
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, id: UUID) -> Order | None:
        return self.session.get(Order, id)

    def get_orders_list(self) -> List[Order]:
        return list(self.session.scalars(select(Order)))

    def create(self, order: SOrderCreate):
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

    def delete(self, id: UUID) -> bool:
        order = self.get(id)
        if not order:
            return False
        self.session.delete(order)
        self.session.commit()
        return True
