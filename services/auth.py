import os
from datetime import datetime, timedelta
from uuid import UUID

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.users import UserRepository
from schemas.auth import SToken, SUserLogin
from schemas.users import SUser

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"])


def create_access_token(user_id: UUID) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def login(self, data: SUserLogin) -> SToken:
        user = await self.repo.get_by_email(data.email)
        if not user or not pwd_context.verify(data.password, user.hashed_password):
            raise ValueError("Invalid email or password")
        token = create_access_token(user.id)
        return SToken(access_token=token)

    async def get_current_user(self, user_id: UUID) -> SUser:
        user = await self.repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        return SUser.model_validate(user)
