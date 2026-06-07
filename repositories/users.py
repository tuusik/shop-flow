from typing import Any, List
from uuid import UUID, uuid4

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.order import Order
from models.user import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_users_list(self) -> List[User]:
        return await self.get_list()

    async def get_users_paginated(
        self, page: int, size: int,
        search: str | None = None,
    ) -> tuple[List[User], int]:
        filters: list[Any] = []
        if search:
            filters.append(or_(User.email.ilike(f"%{search}%")))
        return await self.get_list_paginated(page, size, *filters)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.scalars(select(User).where(User.email == email))
        return result.first()

    async def create(self, data: dict[str, Any]) -> User:
        new_user = User(**data)
        new_user.id = uuid4()
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def update(self, id: UUID, data: dict[str, Any]) -> User | None:
        user = await self.get(id)
        if not user:
            return None
        for field, value in data.items():
            setattr(user, field, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_orders(self, id: UUID) -> List[Order] | None:
        user = await self.get(id)
        if not user:
            return None
        result = await self.session.scalars(
            select(Order).where(Order.user_id == id).options(selectinload(Order.items))
        )
        return list(result)
