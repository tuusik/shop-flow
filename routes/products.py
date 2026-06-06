from uuid import UUID
from fastapi import HTTPException, APIRouter, status
from typing import List
from repositories.products import ProductRepository
from database import session_factory
from schemas.products import SProduct, SProductBase, SProductPatch

product_router = APIRouter(prefix="/products")


@product_router.get("", status_code=status.HTTP_200_OK)
def get_products() -> List[SProduct]:
    with session_factory() as session:
        repo = ProductRepository(session)
        return [SProduct.model_validate(p) for p in repo.get_products_list()]


@product_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_product(id: UUID) -> SProduct:
    with session_factory() as session:
        repo = ProductRepository(session)
        product = repo.get(id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return SProduct.model_validate(product)


@product_router.post("", status_code=status.HTTP_201_CREATED)
def create_product(product: SProductBase):
    with session_factory() as session:
        repo = ProductRepository(session)
        new_product = repo.create(product)
        return SProduct.model_validate(new_product)


@product_router.put("/{id}", status_code=status.HTTP_200_OK)
def update_product(id: UUID, product: SProductBase) -> SProduct:
    with session_factory() as session:
        repo = ProductRepository(session)
        updated = repo.update(id, product.model_dump())
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return SProduct.model_validate(updated)


@product_router.patch("/{id}", status_code=status.HTTP_200_OK)
def patch_product(id: UUID, product: SProductPatch) -> SProduct:
    with session_factory() as session:
        repo = ProductRepository(session)
        updated = repo.update(id, product.model_dump(exclude_none=True))
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return SProduct.model_validate(updated)


@product_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: UUID):
    with session_factory() as session:
        repo = ProductRepository(session)
        if not repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
