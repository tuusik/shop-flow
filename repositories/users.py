from typing import Any, List
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from models.order import Order
from models.user import User
from repositories.base import BaseRepository
from schemas.users import SUserBase


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_users_list(self) -> List[User]:
        return self.get_list()

    def get_by_email(self, email: str) -> User | None:
        return self.session.scalars(select(User).where(User.email == email)).first()

    def create(self, user: SUserBase) -> User:
        new_user = User(**user.model_dump())
        new_user.id = uuid4()
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def update(self, id: UUID, data: dict[str, Any]) -> User | None:
        user = self.get(id)
        if not user:
            return None
        for field, value in data.items():
            setattr(user, field, value)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_orders(self, id: UUID) -> List[Order] | None:
        user = self.get(id)
        if not user:
            return None
        return list(self.session.scalars(
            select(Order).where(Order.user_id == id).options(selectinload(Order.items))
        ))
