from typing import List
from database import engine
from fastapi import APIRouter
from database import User, session_fabric
from schemas.users import SUser
from fastapi import status, HTTPException

user_router = APIRouter(prefix="/users")

@user_router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: SUser):
    user = User(**user.model_dump())
    with session_fabric() as session:
        if not session.query(User).where(User.id == user.id).scalar():
            session.add(user)
            session.commit()
        else:
            raise HTTPException(status_code=400, detail="User with same id already exists!")

@user_router.get("", status_code=status.HTTP_200_OK)
def get_users_list() -> List[SUser]:
    with session_fabric() as session:
        result = session.query(User).all()
        return result

@user_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_user(id: int) -> SUser:
    with session_fabric() as session:
        result = session.query(User).where(User.id == id).scalar()
        return result

@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    with session_fabric() as session:
        obj = session.query(User).get(id)
        if obj:
            session.delete(obj)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нету пользователя с таким id")