import os
os.environ["DATABASE_URL"] = "sqlite:///./test_shopflow.db"

import pytest
from fastapi.testclient import TestClient
from main import app
from models import Base
from database import engine
from schemas.users import SUser
from uuid import UUID


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
    return SUser(id=UUID("12345678-1234-5678-1234-567812345678"), email="johndoe@gmail.com", created_at="2018-11-21")


@pytest.fixture
def user_data():
    return {"email": "johndoe@gmail.com", "created_at": "2018-11-21"}


@pytest.fixture
def created_user(client, user_data):
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def product_data():
    return {
        "title": "Test Product",
        "description": "A product for testing",
        "price": 19.99,
        "stock": 10,
        "created_at": "2024-01-15",
    }


@pytest.fixture
def created_product(client, product_data):
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
    return response.json()
