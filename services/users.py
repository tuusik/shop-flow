from repositories.users import UserRepository
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from schemas.users import SUser, SUserPatch, SUserBase
from schemas.orders import SOrder

class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)

    def get_users_list(self) -> List[SUser]:
        return [SUser.model_validate(user) for user in self.repo.get_users_list()]

    def get_user(self, id: UUID) -> SUser | None:
        user = self.repo.get(id)
        if not user:
            return None
        return SUser.model_validate(user)

    def delete_user(self, id: UUID) -> bool:
        return self.repo.delete(id)

    def create_user(self, user: SUserBase) -> SUser:
        if self.repo.get_by_email(user.email):
            raise ValueError("User with current email already exists")
        return SUser.model_validate(self.repo.create(user))

    def update_user(self, id: UUID, data: SUserBase) -> SUser | None:
        user = self.repo.update(id, data.model_dump())
        if not user:
            return None
        return SUser.model_validate(user)

    def patch_user(self, id: UUID, data: SUserPatch) -> SUser | None:
        user = self.repo.update(id, data.model_dump(exclude_none=True))
        if not user:
            return None
        return SUser.model_validate(user)

    def get_user_orders(self, id: UUID) -> List[SOrder] | None:
        orders = self.repo.get_user_orders(id)
        if orders is None:
            return None
        return [SOrder.model_validate(o) for o in orders]

