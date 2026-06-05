from datetime import date
from schemas.base import BaseSchema

class SProduct(BaseSchema):
    id: int
    title: str
    description: str
    price: float
    stock: int
    created_at: date

