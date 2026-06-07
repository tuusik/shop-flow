from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_order_service
from schemas.orders import SOrder, SOrderCreate, SOrderItem
from services.orders import OrderService

order_router = APIRouter(prefix="/orders")


@order_router.get("", status_code=status.HTTP_200_OK)
async def get_orders(service: OrderService = Depends(get_order_service)) -> List[SOrder]:
    return await service.get_orders_list()


@order_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_order(id: UUID, service: OrderService = Depends(get_order_service)) -> SOrder:
    order = await service.get_order(id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@order_router.post("", status_code=status.HTTP_201_CREATED)
async def create_order(order: SOrderCreate, service: OrderService = Depends(get_order_service)) -> SOrder:
    try:
        return await service.create_order(order)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@order_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: UUID, service: OrderService = Depends(get_order_service)) -> None:
    if not await service.delete_order(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")


@order_router.get("/{id}/products", status_code=status.HTTP_200_OK)
async def get_products_in_order(id: UUID, service: OrderService = Depends(get_order_service)) -> List[SOrderItem]:
    items = await service.get_products_in_order(id)
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return items
