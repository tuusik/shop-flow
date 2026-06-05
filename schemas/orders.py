from datetime import date
from schemas.base import BaseSchema
from uuid import UUID

class SOrder(BaseSchema):
    id: UUID
    user_id: int
    created_at: date

class SOrderItem(BaseSchema):
    id: UUID
    order_id: int
    product_id: int
    quantity: int