from pydantic import EmailStr

from schemas.base import BaseSchema


class SUserLogin(BaseSchema):
    email: EmailStr
    password: str


class SToken(BaseSchema):
    access_token: str
    token_type: str = "bearer"
