from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_user_service
from schemas.users import SUser, SUserRegister
from services.users import UserService

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: SUserRegister, service: UserService = Depends(get_user_service)) -> SUser:
    try:
        return await service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
