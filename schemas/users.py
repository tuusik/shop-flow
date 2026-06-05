from pydantic import EmailStr
from datetime import date
from schemas.base import BaseSchema

class SUser(BaseSchema):
    id: int
    email: EmailStr
    created_at: date