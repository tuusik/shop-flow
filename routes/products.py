from uuid import UUID
from fastapi import HTTPException, APIRouter, status
from typing import List
from database import session_factory
from schemas.products import SProduct, SProductBase, SProductPatch
from services.products import ProductService

product_router = APIRouter(prefix="/products")


@product_router.get("", status_code=status.HTTP_200_OK)
def get_products() -> List[SProduct]:
    with session_factory() as session:
        return ProductService(session).get_products_list()


@product_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_product(id: UUID) -> SProduct:
    with session_factory() as session:
        product = ProductService(session).get_product(id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product


@product_router.post("", status_code=status.HTTP_201_CREATED)
def create_product(product: SProductBase):
    with session_factory() as session:
        return ProductService(session).create_product(product)


@product_router.put("/{id}", status_code=status.HTTP_200_OK)
def update_product(id: UUID, product: SProductBase) -> SProduct:
    with session_factory() as session:
        updated = ProductService(session).update_product(id, product)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return updated


@product_router.patch("/{id}", status_code=status.HTTP_200_OK)
def patch_product(id: UUID, product: SProductPatch) -> SProduct:
    with session_factory() as session:
        updated = ProductService(session).patch_product(id, product)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return updated


@product_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: UUID):
    with session_factory() as session:
        if not ProductService(session).delete_product(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
