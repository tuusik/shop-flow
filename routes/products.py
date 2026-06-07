from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from dependencies import get_product_service
from schemas.base import SPaginated
from schemas.products import SProduct, SProductBase, SProductPatch
from services.products import ProductService

product_router = APIRouter(prefix="/products")


@product_router.get("", status_code=status.HTTP_200_OK)
async def get_products(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
) -> SPaginated[SProduct]:
    return await service.get_products_paginated(page, size)


@product_router.get("/popular", status_code=status.HTTP_200_OK)
async def get_popular_products(
    limit: int = Query(5, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
) -> List[SProduct]:
    return await service.get_popular_products(limit)


@product_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_product(id: UUID, service: ProductService = Depends(get_product_service)) -> SProduct:
    product = await service.get_product(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@product_router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(product: SProductBase, service: ProductService = Depends(get_product_service)) -> SProduct:
    try:
        return await service.create_product(product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@product_router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_product(
    id: UUID, product: SProductBase, service: ProductService = Depends(get_product_service)
) -> SProduct:
    try:
        updated = await service.update_product(id, product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated


@product_router.patch("/{id}", status_code=status.HTTP_200_OK)
async def patch_product(
    id: UUID, product: SProductPatch, service: ProductService = Depends(get_product_service)
) -> SProduct:
    try:
        updated = await service.patch_product(id, product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated


@product_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: UUID, service: ProductService = Depends(get_product_service)) -> None:
    if not await service.delete_product(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
