from typing import Generic, List, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get(self, id: UUID) -> T | None:
        return await self.session.get(self.model, id)

    async def get_list(self) -> List[T]:
        result = await self.session.scalars(select(self.model))
        return list(result)

    async def delete(self, id: UUID) -> bool:
        obj = await self.get(id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
