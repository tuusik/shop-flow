from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from services.orders import OrderService
from services.products import ProductService
from services.users import UserService


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(session)


def get_product_service(session: Session = Depends(get_session)) -> ProductService:
    return ProductService(session)


def get_order_service(session: Session = Depends(get_session)) -> OrderService:
    return OrderService(session)
