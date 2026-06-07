from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.orders import OrderRepository
from repositories.products import ProductRepository
from repositories.users import UserRepository
from schemas.orders import SOrder, SOrderCreate, SOrderItem


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = OrderRepository(session)
        self.user_repo = UserRepository(session)
        self.product_repo = ProductRepository(session)

    async def get_orders_list(self) -> List[SOrder]:
        return [SOrder.model_validate(o) for o in await self.repo.get_orders_list()]

    async def get_order(self, id: UUID) -> SOrder | None:
        order = await self.repo.get(id)
        if not order:
            return None
        return SOrder.model_validate(order)

    async def create_order(self, data: SOrderCreate) -> SOrder:
        user = await self.user_repo.get(data.user_id)
        if not user:
            raise ValueError(f"User {data.user_id} not found")

        for item in data.items:
            product = await self.product_repo.get(item.product_id)
            if not product:
                raise ValueError(f"Product {item.product_id} not found")
            if product.stock < item.quantity:
                raise ValueError(
                    f"Not enough stock for product {item.product_id}: "
                    f"requested {item.quantity}, available {product.stock}"
                )

        for item in data.items:
            product = await self.product_repo.get(item.product_id)
            assert product is not None
            product.stock -= item.quantity

        return SOrder.model_validate(await self.repo.create(data))

    async def delete_order(self, id: UUID) -> bool:
        order = await self.repo.get(id)
        if not order:
            return False

        for item in order.items:
            product = await self.product_repo.get(item.product_id)
            if product:
                product.stock += item.quantity

        return await self.repo.delete(id)

    async def get_products_in_order(self, id: UUID) -> List[SOrderItem] | None:
        items = await self.repo.get_products_in_order(id)
        if not items:
            return None
        return [SOrderItem.model_validate(i) for i in items]
