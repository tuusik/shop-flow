from uuid import UUID
from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from schemas.products import SProduct, SProductBase, SProductPatch
from services.products import ProductService
from dependencies import get_product_service

product_router = APIRouter(prefix="/products")


@product_router.get("", status_code=status.HTTP_200_OK)
def get_products(service: ProductService = Depends(get_product_service)) -> List[SProduct]:
    return service.get_products_list()


@product_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_product(id: UUID, service: ProductService = Depends(get_product_service)) -> SProduct:
    product = service.get_product(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@product_router.post("", status_code=status.HTTP_201_CREATED)
def create_product(product: SProductBase, service: ProductService = Depends(get_product_service)):
    try:
        return service.create_product(product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@product_router.put("/{id}", status_code=status.HTTP_200_OK)
def update_product(id: UUID, product: SProductBase, service: ProductService = Depends(get_product_service)) -> SProduct:
    try:
        updated = service.update_product(id, product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated


@product_router.patch("/{id}", status_code=status.HTTP_200_OK)
def patch_product(id: UUID, product: SProductPatch, service: ProductService = Depends(get_product_service)) -> SProduct:
    try:
        updated = service.patch_product(id, product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated


@product_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: UUID, service: ProductService = Depends(get_product_service)):
    if not service.delete_product(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
