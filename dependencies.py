from typing import AsyncGenerator
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal
from schemas.users import SUser
from services.auth import ALGORITHM, SECRET_KEY, AuthService
from services.orders import OrderService
from services.products import ProductService
from services.users import UserService

security = HTTPBearer()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)


async def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    return ProductService(session)


async def get_order_service(session: AsyncSession = Depends(get_session)) -> OrderService:
    return OrderService(session)


async def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> SUser:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    auth_service = AuthService(session)
    try:
        return await auth_service.get_current_user(UUID(user_id))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
