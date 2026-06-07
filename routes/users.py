from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from dependencies import get_user_service
from schemas.base import SPaginated
from schemas.orders import SOrder
from schemas.users import SUser, SUserBase, SUserPatch
from services.users import UserService

user_router = APIRouter(prefix="/users")


@user_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user: SUserBase, service: UserService = Depends(get_user_service)) -> SUser:
    try:
        return await service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_router.get("", status_code=status.HTTP_200_OK)
async def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    service: UserService = Depends(get_user_service),
) -> SPaginated[SUser]:
    return await service.get_users_paginated(page, size)


@user_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(id: UUID, service: UserService = Depends(get_user_service)) -> SUser:
    user = await service.get_user(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@user_router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user(id: UUID, user: SUserBase, service: UserService = Depends(get_user_service)) -> SUser:
    try:
        updated = await service.update_user(id, user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated


@user_router.patch("/{id}", status_code=status.HTTP_200_OK)
async def patch_user(id: UUID, user: SUserPatch, service: UserService = Depends(get_user_service)) -> SUser:
    try:
        updated = await service.patch_user(id, user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated


@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: UUID, service: UserService = Depends(get_user_service)) -> None:
    if not await service.delete_user(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@user_router.get("/{id}/orders", status_code=status.HTTP_200_OK)
async def get_user_orders(id: UUID, service: UserService = Depends(get_user_service)) -> List[SOrder]:
    orders = await service.get_user_orders(id)
    if orders is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return orders
