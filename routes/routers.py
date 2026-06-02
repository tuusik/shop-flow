from typing import List
from sqlalchemy.orm import Session
from database import engine
from fastapi import APIRouter
from database import User
from schemas.users import SUser
from fastapi import status, HTTPException

router = APIRouter(prefix="/users")

@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: SUser):
    user = User(**user.model_dump())
    with Session(engine) as session:
        session.add(user)
        session.commit()

@router.get("", status_code=status.HTTP_200_OK)
def get_users_list() -> List[SUser]:
    with Session(engine) as session:
        result = session.query(User).all()
        return result

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_user(id: int) -> SUser:
    with Session(engine) as session:
        result = session.query(User).where(User.id == id).scalar()
        return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    with Session(engine) as session:
        obj = session.query(User).get(id)
        if obj:
            session.delete(obj)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нету пользователя с таким id")