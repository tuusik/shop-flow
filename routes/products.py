
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import status
from typing import List
from models import Product
from database import session_factory
from schemas.products import SProduct

product_router = APIRouter(prefix="/products")

@product_router.get("", status_code=status.HTTP_200_OK)
def get_products() -> List[SProduct]:
    with session_factory() as session:
        result = session.query(Product).all()
        return result

@product_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_product(id: int) -> SProduct:
    with session_factory() as session:
        result = session.query(Product).where(Product.id == id).scalar()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with current id is not found")
        return result

@product_router.post("", status_code=status.HTTP_201_CREATED)
def create_product(product: SProduct):
    with session_factory() as session:
        obj = Product(**product.model_dump())
        if not session.query(Product).where(Product.id == obj.id).scalar():
            session.add(obj)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product with same id already exists")

@product_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):
    with session_factory() as session:
        obj = session.query(Product).where(Product.id == id).scalar()
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with current id is not found")
        session.delete(obj)
        session.commit()
