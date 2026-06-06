from typing import List
from fastapi import APIRouter
from repositories.users import UserRepository
from database import session_factory
from schemas.users import SUser, SUserPatch, SUserBase
from fastapi import status, HTTPException
from uuid import UUID

user_router = APIRouter(prefix="/users")


@user_router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: SUserBase):
    with session_factory() as session:
        repo = UserRepository(session)
        new_user = repo.create(user)
        return SUser.model_validate(new_user)


@user_router.get("", status_code=status.HTTP_200_OK)
def get_users_list() -> List[SUser]:
    with session_factory() as session:
        repo = UserRepository(session)
        return [SUser.model_validate(u) for u in repo.get_users_list()]


@user_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_user(id: UUID) -> SUser:
    with session_factory() as session:
        repo = UserRepository(session)
        user = repo.get(id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return SUser.model_validate(user)


@user_router.put("/{id}", status_code=status.HTTP_200_OK)
def update_user(id: UUID, user: SUserBase) -> SUser:
    with session_factory() as session:
        repo = UserRepository(session)
        updated = repo.update(id, user.model_dump())
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return SUser.model_validate(updated)


@user_router.patch("/{id}", status_code=status.HTTP_200_OK)
def patch_user(id: UUID, user: SUserPatch) -> SUser:
    with session_factory() as session:
        repo = UserRepository(session)
        updated = repo.update(id, user.model_dump(exclude_none=True))
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return SUser.model_validate(updated)


@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: UUID):
    with session_factory() as session:
        repo = UserRepository(session)
        if not repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
