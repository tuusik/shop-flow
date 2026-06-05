from datetime import date
from schemas.base import BaseSchema

class SOrder(BaseSchema):
    id: int
    user_id: int
    created_at: date

class SOrderItem(BaseSchema):
    id: int
    order_id: int
    product_id: int
    quantity: int