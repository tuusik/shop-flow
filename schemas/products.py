from pydantic import BaseModel
from datetime import date

class SProduct(BaseModel):
    id: int
    title: str
    description: str
    price: float
    stock: int
    created_at: date

