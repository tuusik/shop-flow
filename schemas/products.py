from datetime import date
from schemas.base import BaseSchema
from uuid import UUID

class SProductBase(BaseSchema):
    title: str
    description: str
    price: float
    stock: int
    created_at: date

class SProduct(SProductBase):
    id: UUID

class SProductPatch(SProductBase):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    created_at: date | None = None