from typing import Generic, List, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def get(self, id: UUID) -> T | None:
        return self.session.get(self.model, id)

    def get_list(self) -> List[T]:
        return list(self.session.scalars(select(self.model)))

    def delete(self, id: UUID) -> bool:
        obj = self.get(id)
        if not obj:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True
