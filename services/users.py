from math import ceil
from typing import List
from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.users import UserRepository
from schemas.base import SPaginated
from schemas.orders import SOrder
from schemas.users import SUser, SUserBase, SUserPatch, SUserRegister

pwd_context = CryptContext(schemes=["bcrypt"])


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def get_users_list(self) -> List[SUser]:
        return [SUser.model_validate(user) for user in await self.repo.get_users_list()]

    async def get_users_paginated(self, page: int, size: int, search: str | None = None) -> SPaginated[SUser]:
        items, total = await self.repo.get_users_paginated(page, size, search)
        return SPaginated[SUser](
            items=[SUser.model_validate(u) for u in items],
            total=total,
            page=page,
            size=size,
            pages=ceil(total / size) if total else 0,
        )

    async def get_user(self, id: UUID) -> SUser | None:
        user = await self.repo.get(id)
        if not user:
            return None
        return SUser.model_validate(user)

    async def delete_user(self, id: UUID) -> bool:
        return await self.repo.delete(id)

    async def create_user(self, user: SUserBase) -> SUser:
        if await self.repo.get_by_email(user.email):
            raise ValueError("User with current email already exists")
        user_data = user.model_dump()
        user_data["hashed_password"] = ""
        return SUser.model_validate(await self.repo.create(user_data))

    async def register(self, data: SUserRegister) -> SUser:
        if await self.repo.get_by_email(data.email):
            raise ValueError("User with this email already exists")
        user_data = data.model_dump(exclude={"password"})
        user_data["hashed_password"] = pwd_context.hash(data.password)
        return SUser.model_validate(await self.repo.create(user_data))

    async def update_user(self, id: UUID, data: SUserBase) -> SUser | None:
        existing = await self.repo.get_by_email(data.email)
        if existing and existing.id != id:
            raise ValueError("User with current email already exists")
        user = await self.repo.update(id, data.model_dump())
        if not user:
            return None
        return SUser.model_validate(user)

    async def patch_user(self, id: UUID, data: SUserPatch) -> SUser | None:
        if data.email is not None:
            existing = await self.repo.get_by_email(data.email)
            if existing and existing.id != id:
                raise ValueError("User with current email already exists")
        user = await self.repo.update(id, data.model_dump(exclude_none=True))
        if not user:
            return None
        return SUser.model_validate(user)

    async def get_user_orders(self, id: UUID) -> List[SOrder] | None:
        orders = await self.repo.get_user_orders(id)
        if orders is None:
            return None
        return [SOrder.model_validate(o) for o in orders]
