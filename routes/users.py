from typing import List
from fastapi import APIRouter
from models import User
from database import session_factory
from schemas.users import SUser, SUserPatch, SUserBase
from fastapi import status, HTTPException
from uuid import UUID, uuid4

user_router = APIRouter(prefix="/users")

@user_router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: SUserBase):
    with session_factory() as session:
        new_user = User(**user.model_dump())
        new_user.id = uuid4()
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

@user_router.get("", status_code=status.HTTP_200_OK)
def get_users_list() -> List[SUser]:
    with session_factory() as session:
        obj = session.query(User).all()
        return obj

@user_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_user(id: UUID) -> SUser:
    with session_factory() as session:
        obj = session.get(User, id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with current id is not found")
        return obj

@user_router.put("/{id}", status_code=status.HTTP_200_OK)
def update_user(id: UUID, user: SUserBase):
    with session_factory() as session:
        obj = session.get(User, id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with current id is not found")
        for field, value in user.model_dump().items():
            setattr(obj, field, value)
        session.commit()
        return obj

@user_router.patch("/{id}", status_code=status.HTTP_200_OK)
def patch_user(id: UUID, user: SUserPatch):
    with session_factory() as session:
        obj = session.get(User, id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with current id is not found")
        for field, value in user.model_dump(exclude_none=True).items():
            setattr(obj, field, value)
        session.commit()
        return obj

@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: UUID):
    with session_factory() as session:
        obj = session.get(User, id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with current id is not found")
        session.delete(obj)
        session.commit()
