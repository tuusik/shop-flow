from models.user import User
from uuid import UUID, uuid4
from schemas.users import SUserBase
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from typing import List
from models.order import Order

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, id: UUID) -> User | None:
        return self.session.get(User, id)

    def get_by_email(self, email: str) -> User | None:
        return self.session.scalars(select(User).where(User.email == email)).first()

    def get_users_list(self) -> List[User]:
        return list(self.session.scalars(select(User)))

    def create(self, user: SUserBase) -> User:
        new_user = User(**user.model_dump())
        new_user.id = uuid4()
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def update(self, id: UUID, data: dict) -> User | None:
        user = self.get(id)
        if not user:
            return None
        for field, value in data.items():
            setattr(user, field, value)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, id: UUID) -> bool:
        user = self.get(id)
        if not user:
            return False
        self.session.delete(user)
        self.session.commit()
        return True

    def get_user_orders(self, id: UUID) -> List[Order] | None:
        user = self.get(id)
        if not user:
            return None
        return list(self.session.scalars(select(Order).where(Order.user_id == id).options(selectinload(Order.items))))
