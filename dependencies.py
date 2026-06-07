from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal
from services.orders import OrderService
from services.products import ProductService
from services.users import UserService


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)


async def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    return ProductService(session)


async def get_order_service(session: AsyncSession = Depends(get_session)) -> OrderService:
    return OrderService(session)
