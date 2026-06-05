from uuid import UUID, uuid4
from fastapi import HTTPException, APIRouter, status
from typing import List
from models import Order, OrderItem
from database import session_factory
from schemas.orders import SOrder, SOrderCreate, SOrderItem

order_router = APIRouter(prefix="/orders")


@order_router.get("", status_code=status.HTTP_200_OK)
def get_orders() -> List[SOrder]:
    with session_factory() as session:
        orders = session.query(Order).all()
        return orders


@order_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_order(id: UUID) -> SOrder:
    with session_factory() as session:
        obj = session.get(Order, id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return obj


@order_router.post("", status_code=status.HTTP_201_CREATED)
def create_order(order: SOrderCreate):
    with session_factory() as session:
        new_order = Order(user_id=order.user_id, created_at=order.created_at)
        new_order.id = uuid4()
        for item in order.items:
            order_item = OrderItem(product_id=item.product_id, quantity=item.quantity)
            order_item.id = uuid4()
            new_order.items.append(order_item)
        session.add(new_order)
        session.commit()
        session.refresh(new_order)
        return new_order


@order_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id: UUID):
    with session_factory() as session:
        obj = session.get(Order, id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        session.delete(obj)
        session.commit()
