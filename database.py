import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base  # noqa: F401

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
engine = create_engine(DATABASE_URL, echo=DEBUG)

SessionLocal = sessionmaker(engine, expire_on_commit=False)
