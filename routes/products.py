from uuid import UUID, uuid4
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import status
from typing import List
from models import Product
from database import session_factory
from schemas.products import SProduct, SProductBase, SProductPatch

product_router = APIRouter(prefix="/products")

@product_router.get("", status_code=status.HTTP_200_OK)
def get_products() -> List[SProduct]:
    with session_factory() as session:
        obj = session.query(Product).all()
        return obj

@product_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_product(id: UUID) -> SProduct:
    with session_factory() as session:
        obj = session.get(Product, id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with current id is not found")
        return obj

@product_router.post("", status_code=status.HTTP_201_CREATED)
def create_product(product: SProductBase):
    with session_factory() as session:
        new_product = Product(**product.model_dump())
        new_product.id = uuid4()
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        return new_product

@product_router.put("/{id}", status_code=status.HTTP_200_OK)
def update_product(id: UUID, product: SProductBase):
    with session_factory() as session:
        obj = session.get(Product, id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with current id is not found")
        for field, value in product.model_dump().items():
            setattr(obj, field, value)
        session.commit()
        return obj

@product_router.patch("/{id}", status_code=status.HTTP_200_OK)
def patch_product(id: UUID, product: SProductPatch):
    with session_factory() as session:
        obj = session.get(Product, id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with current id is not found")
        for field, value in product.model_dump(exclude_none=True).items():
            setattr(obj, field, value)
        session.commit()
        return obj

@product_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: UUID):
    with session_factory() as session:
        obj = session.get(Product, id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with current id is not found")
        session.delete(obj)
        session.commit()
