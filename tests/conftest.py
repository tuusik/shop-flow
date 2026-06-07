import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_shopflow.db"

from uuid import UUID

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from database import SessionLocal, engine
from dependencies import get_session
from main import app
from models import Base
from schemas.users import SUser


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    if os.path.exists("./test_shopflow.db"):
        os.remove("./test_shopflow.db")


@pytest_asyncio.fixture(autouse=True)
async def clean_db():
    yield
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest_asyncio.fixture
async def override_session():
    async def _get_test_session():
        async with SessionLocal() as session:
            yield session
    app.dependency_overrides[get_session] = _get_test_session
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(override_session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture
def user():
    return SUser(id=UUID("12345678-1234-5678-1234-567812345678"), email="johndoe@gmail.com", created_at="2018-11-21")


@pytest.fixture
def user_data():
    return {"email": "johndoe@gmail.com", "password": "secret123", "created_at": "2018-11-21"}


@pytest_asyncio.fixture
async def created_user(client, user_data):
    response = await client.post("/auth/register", json=user_data)
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


@pytest_asyncio.fixture
async def created_product(client, product_data):
    response = await client.post("/products", json=product_data)
    assert response.status_code == 201
    return response.json()


@pytest_asyncio.fixture
async def created_user_and_product(client, user_data, product_data):
    user = (await client.post("/users", json=user_data)).json()
    product = (await client.post("/products", json=product_data)).json()
    return {"user": user, "product": product}


@pytest_asyncio.fixture
async def order_data(created_user_and_product):
    return {
        "user_id": created_user_and_product["user"]["id"],
        "created_at": "2024-02-01",
        "items": [{"product_id": created_user_and_product["product"]["id"], "quantity": 2}],
    }


@pytest_asyncio.fixture
async def created_order(client, order_data):
    response = await client.post("/orders", json=order_data)
    assert response.status_code == 201
    return response.json()
