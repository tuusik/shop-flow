from pydantic import EmailStr
from datetime import date
from schemas.base import BaseSchema
from uuid import UUID

class SUserBase(BaseSchema):
    email: EmailStr
    created_at: date

class SUser(SUserBase):
    id: UUID

class SUserPatch(SUserBase):
    email: EmailStr | None = None
    created_at: date | None = None