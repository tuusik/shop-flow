import datetime
from sqlalchemy import create_engine
from sqlalchemy import Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    created_at: Mapped[datetime.date] = mapped_column(Date)

engine = create_engine('postgresql+psycopg2://postgres:postgres\
@localhost:5436/shopflow', echo=True)

