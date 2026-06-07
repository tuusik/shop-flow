from datetime import date
from uuid import UUID

from pydantic import EmailStr

from schemas.base import BaseSchema


class SUserBase(BaseSchema):
    email: EmailStr
    created_at: date


class SUserRegister(BaseSchema):
    email: EmailStr
    password: str
    created_at: date = date.today()


class SUser(SUserBase):
    id: UUID


class SUserPatch(SUserBase):
    email: EmailStr | None = None  # type: ignore[assignment]
    created_at: date | None = None  # type: ignore[assignment]
