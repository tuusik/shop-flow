from pydantic import BaseModel, EmailStr
from datetime import date

class SUser(BaseModel):
    id: int
    email: EmailStr
    created_at: date