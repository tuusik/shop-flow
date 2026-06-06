from datetime import date
from uuid import UUID

from schemas.base import BaseSchema


class SProductBase(BaseSchema):
    title: str
    description: str
    price: float
    stock: int
    created_at: date

class SProduct(SProductBase):
    id: UUID

class SProductPatch(SProductBase):
    title: str | None = None  # type: ignore[assignment]
    description: str | None = None  # type: ignore[assignment]
    price: float | None = None  # type: ignore[assignment]
    stock: int | None = None  # type: ignore[assignment]
    created_at: date | None = None  # type: ignore[assignment]
