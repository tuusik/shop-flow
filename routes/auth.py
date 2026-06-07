from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_auth_service, get_current_user, get_user_service
from schemas.auth import SToken, SUserLogin
from schemas.users import SUser, SUserRegister
from services.auth import AuthService
from services.users import UserService

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: SUserRegister, service: UserService = Depends(get_user_service)) -> SUser:
    try:
        return await service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@auth_router.post("/login")
async def login(data: SUserLogin, service: AuthService = Depends(get_auth_service)) -> SToken:
    try:
        return await service.login(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@auth_router.get("/me")
async def me(user: SUser = Depends(get_current_user)) -> SUser:
    return user
