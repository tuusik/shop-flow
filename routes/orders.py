from uuid import UUID
from fastapi import HTTPException, APIRouter, status
from typing import List
from repositories.orders import OrderRepository
from database import session_factory
from schemas.orders import SOrder, SOrderCreate

order_router = APIRouter(prefix="/orders")


@order_router.get("", status_code=status.HTTP_200_OK)
def get_orders() -> List[SOrder]:
    with session_factory() as session:
        repo = OrderRepository(session)
        return [SOrder.model_validate(o) for o in repo.get_orders_list()]


@order_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_order(id: UUID) -> SOrder:
    with session_factory() as session:
        repo = OrderRepository(session)
        order = repo.get(id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return SOrder.model_validate(order)


@order_router.post("", status_code=status.HTTP_201_CREATED)
def create_order(order: SOrderCreate):
    with session_factory() as session:
        repo = OrderRepository(session)
        new_order = repo.create(order)
        return SOrder.model_validate(new_order)


@order_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id: UUID):
    with session_factory() as session:
        repo = OrderRepository(session)
        if not repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
