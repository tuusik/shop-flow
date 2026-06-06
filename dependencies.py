from fastapi import Depends
from sqlalchemy.orm import Session
from database import session_factory
from services.users import UserService
from services.products import ProductService
from services.orders import OrderService


def get_session():
    with session_factory() as session:
        yield session


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(session)


def get_product_service(session: Session = Depends(get_session)) -> ProductService:
    return ProductService(session)


def get_order_service(session: Session = Depends(get_session)) -> OrderService:
    return OrderService(session)
