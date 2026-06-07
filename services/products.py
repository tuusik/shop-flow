from math import ceil
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.products import ProductRepository
from schemas.base import SPaginated
from schemas.products import SProduct, SProductBase, SProductPatch


class ProductService:
    def __init__(self, session: AsyncSession):
        self.repo = ProductRepository(session)

    async def get_products_list(self) -> List[SProduct]:
        return [SProduct.model_validate(p) for p in await self.repo.get_products_list()]

    async def get_products_paginated(
        self, page: int, size: int,
        search: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> SPaginated[SProduct]:
        items, total = await self.repo.get_products_paginated(page, size, search, min_price, max_price)
        return SPaginated[SProduct](
            items=[SProduct.model_validate(p) for p in items],
            total=total,
            page=page,
            size=size,
            pages=ceil(total / size) if total else 0,
        )

    async def get_product(self, id: UUID) -> SProduct | None:
        product = await self.repo.get(id)
        if not product:
            return None
        return SProduct.model_validate(product)

    async def create_product(self, data: SProductBase) -> SProduct:
        if data.stock < 0:
            raise ValueError("Stock cannot be negative")
        return SProduct.model_validate(await self.repo.create(data))

    async def update_product(self, id: UUID, data: SProductBase) -> SProduct | None:
        if data.stock < 0:
            raise ValueError("Stock cannot be negative")
        product = await self.repo.update(id, data.model_dump())
        if not product:
            return None
        return SProduct.model_validate(product)

    async def patch_product(self, id: UUID, data: SProductPatch) -> SProduct | None:
        if data.stock is not None and data.stock < 0:
            raise ValueError("Stock cannot be negative")
        product = await self.repo.update(id, data.model_dump(exclude_none=True))
        if not product:
            return None
        return SProduct.model_validate(product)

    async def delete_product(self, id: UUID) -> bool:
        return await self.repo.delete(id)

    async def get_popular_products(self, limit: int) -> List[SProduct]:
        return [SProduct.model_validate(p) for p in await self.repo.get_popular_products(limit)]
