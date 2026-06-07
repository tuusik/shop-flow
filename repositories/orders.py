from typing import List
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.order import Order, OrderItem
from repositories.base import BaseRepository
from schemas.orders import SOrderCreate


class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Order)

    async def get_orders_list(self) -> List[Order]:
        return await self.get_list()

    async def create(self, order: SOrderCreate) -> Order:
        new_order = Order(user_id=order.user_id, created_at=order.created_at)
        new_order.id = uuid4()
        for item in order.items:
            order_item = OrderItem(product_id=item.product_id, quantity=item.quantity)
            order_item.id = uuid4()
            new_order.items.append(order_item)
        self.session.add(new_order)
        await self.session.commit()
        return new_order

    async def get_products_in_order(self, id: UUID) -> List[OrderItem] | None:
        order = await self.get(id)
        if not order:
            return None
        result = await self.session.scalars(select(OrderItem).where(OrderItem.order_id == id))
        return list(result)
