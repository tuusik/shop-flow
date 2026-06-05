from pydantic import BaseModel
from datetime import date

class SOrder(BaseModel):
    id: int
    user_id: int
    created_at: date

class SOrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int