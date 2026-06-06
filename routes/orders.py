from uuid import UUID
from fastapi import HTTPException, APIRouter, status
from typing import List
from database import session_factory
from schemas.orders import SOrder, SOrderCreate
from services.orders import OrderService

order_router = APIRouter(prefix="/orders")


@order_router.get("", status_code=status.HTTP_200_OK)
def get_orders() -> List[SOrder]:
    with session_factory() as session:
        return OrderService(session).get_orders_list()


@order_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_order(id: UUID) -> SOrder:
    with session_factory() as session:
        order = OrderService(session).get_order(id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return order


@order_router.post("", status_code=status.HTTP_201_CREATED)
def create_order(order: SOrderCreate):
    with session_factory() as session:
        try:
            return OrderService(session).create_order(order)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@order_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id: UUID):
    with session_factory() as session:
        if not OrderService(session).delete_order(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
