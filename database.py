import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from models import Base  # noqa: F401

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
engine = create_async_engine(DATABASE_URL, echo=DEBUG)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
