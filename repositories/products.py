from typing import Any, List
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.order import OrderItem
from models.product import Product
from repositories.base import BaseRepository
from schemas.products import SProductBase


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Product)

    async def get_products_list(self) -> List[Product]:
        return await self.get_list()

    async def create(self, product: SProductBase) -> Product:
        new_product = Product(**product.model_dump())
        new_product.id = uuid4()
        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product

    async def update(self, id: UUID, data: dict[str, Any]) -> Product | None:
        product = await self.get(id)
        if not product:
            return None
        for field, value in data.items():
            setattr(product, field, value)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_popular_products(self, limit: int) -> List[Product]:
        result = await self.session.scalars(
            select(Product)
            .join(Product.items)
            .group_by(Product.id)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
        )
        return list(result)
