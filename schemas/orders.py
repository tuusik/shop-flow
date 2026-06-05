from datetime import date
from schemas.base import BaseSchema
from uuid import UUID
from typing import List


class SOrderItemBase(BaseSchema):
    product_id: UUID
    quantity: int


class SOrderItem(SOrderItemBase):
    id: UUID
    order_id: UUID


class SOrderBase(BaseSchema):
    user_id: UUID
    created_at: date


class SOrderCreate(SOrderBase):
    items: List[SOrderItemBase]


class SOrder(SOrderBase):
    id: UUID
    items: List[SOrderItem] | None = None
