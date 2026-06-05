import os
os.environ["DATABASE_URL"] = "sqlite:///./test_shopflow.db"

import pytest
from fastapi.testclient import TestClient
from main import app
from models import Base
from database import engine
from schemas.users import SUser


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
    if os.path.exists("./test_shopflow.db"):
        os.remove("./test_shopflow.db")


@pytest.fixture(autouse=True)
def clean_db():
    yield
    for table in reversed(Base.metadata.sorted_tables):
        with engine.connect() as conn:
            conn.execute(table.delete())
            conn.commit()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def user():
    return SUser(id=1, email="johndoe@gmail.com", created_at="2018-11-21")


@pytest.fixture
def user_data():
    return {"id": 1, "email": "johndoe@gmail.com", "created_at": "2018-11-21"}


@pytest.fixture
def created_user(client, user_data):
    client.post("/users", json=user_data)
    return user_data


@pytest.fixture
def product_data():
    return {
        "id": 1,
        "title": "Test Product",
        "description": "A product for testing",
        "price": 19.99,
        "stock": 10,
        "created_at": "2024-01-15",
    }


@pytest.fixture
def created_product(client, product_data):
    client.post("/products", json=product_data)
    return product_data
