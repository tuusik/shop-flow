import pytest


@pytest.mark.asyncio
class TestUsers:
    async def test_create_user(self, client, user_data):
        response = await client.post("/users", json=user_data)
        assert response.status_code == 201
        assert "id" in response.json()

    async def test_create_duplicate_user(self, client, user_data, created_user):
        response = await client.post("/users", json=user_data)
        assert response.status_code == 400

    async def test_get_users_list(self, client, created_user):
        response = await client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert any(u["id"] == created_user["id"] for u in users)

    async def test_get_user_by_id(self, client, created_user):
        response = await client.get(f"/users/{created_user['id']}")
        assert response.status_code == 200
        assert response.json()["email"] == created_user["email"]

    async def test_delete_user(self, client, created_user):
        response = await client.delete(f"/users/{created_user['id']}")
        assert response.status_code == 204

    async def test_delete_nonexistent_user(self, client):
        response = await client.delete("/users/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    async def test_get_user_returns_correct_fields(self, client, created_user):
        response = await client.get(f"/users/{created_user['id']}")
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert "created_at" in data


@pytest.mark.asyncio
class TestProducts:
    async def test_create_product(self, client, product_data):
        response = await client.post("/products", json=product_data)
        assert response.status_code == 201
        assert "id" in response.json()

    async def test_create_duplicate_product(self, client, product_data, created_product):
        response = await client.post("/products", json=product_data)
        assert response.status_code == 201

    async def test_create_product_negative_stock(self, client, product_data):
        data = {**product_data, "stock": -1}
        response = await client.post("/products", json=data)
        assert response.status_code == 400

    async def test_get_products_list(self, client, created_product):
        response = await client.get("/products")
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert any(p["id"] == created_product["id"] for p in products)

    async def test_get_product_by_id(self, client, created_product):
        response = await client.get(f"/products/{created_product['id']}")
        assert response.status_code == 200
        assert response.json()["title"] == created_product["title"]

    async def test_get_nonexistent_product(self, client):
        response = await client.get("/products/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    async def test_update_product(self, client, created_product):
        data = {
            "title": "Updated",
            "description": "Updated desc",
            "price": 99.99,
            "stock": 5,
            "created_at": "2024-01-15",
        }
        response = await client.put(f"/products/{created_product['id']}", json=data)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated"

    async def test_update_nonexistent_product(self, client):
        data = {
            "title": "X",
            "description": "X",
            "price": 1.0,
            "stock": 1,
            "created_at": "2024-01-01",
        }
        response = await client.put("/products/00000000-0000-0000-0000-000000000000", json=data)
        assert response.status_code == 404

    async def test_patch_product(self, client, created_product):
        response = await client.patch(f"/products/{created_product['id']}", json={"price": 9.99})
        assert response.status_code == 200
        assert response.json()["price"] == 9.99
        assert response.json()["title"] == created_product["title"]

    async def test_delete_product(self, client, created_product):
        response = await client.delete(f"/products/{created_product['id']}")
        assert response.status_code == 204

    async def test_delete_nonexistent_product(self, client):
        response = await client.delete("/products/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    async def test_get_product_returns_correct_fields(self, client, created_product):
        response = await client.get(f"/products/{created_product['id']}")
        data = response.json()
        assert "id" in data
        assert "title" in data
        assert "description" in data
        assert "price" in data
        assert "stock" in data
        assert "created_at" in data


@pytest.mark.asyncio
class TestOrders:
    async def test_create_order(self, client, order_data):
        response = await client.post("/orders", json=order_data)
        assert response.status_code == 201
        assert "id" in response.json()

    async def test_create_order_nonexistent_user(self, client, order_data):
        data = {**order_data, "user_id": "00000000-0000-0000-0000-000000000000"}
        response = await client.post("/orders", json=data)
        assert response.status_code == 400

    async def test_create_order_insufficient_stock(self, client, created_user_and_product):
        data = {
            "user_id": created_user_and_product["user"]["id"],
            "created_at": "2024-02-01",
            "items": [{"product_id": created_user_and_product["product"]["id"], "quantity": 999}],
        }
        response = await client.post("/orders", json=data)
        assert response.status_code == 400

    async def test_get_orders_list(self, client, created_order):
        response = await client.get("/orders")
        assert response.status_code == 200
        orders = response.json()
        assert isinstance(orders, list)
        assert any(o["id"] == created_order["id"] for o in orders)

    async def test_get_order_by_id(self, client, created_order):
        response = await client.get(f"/orders/{created_order['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created_order["id"]

    async def test_get_nonexistent_order(self, client):
        response = await client.get("/orders/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    async def test_delete_order(self, client, created_order):
        response = await client.delete(f"/orders/{created_order['id']}")
        assert response.status_code == 204

    async def test_delete_nonexistent_order(self, client):
        response = await client.delete("/orders/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    async def test_order_stock_restored_on_delete(self, client, created_user_and_product, order_data):
        response = await client.post("/orders", json=order_data)
        order = response.json()
        await client.delete(f"/orders/{order['id']}")
        product_response = await client.get(f"/products/{created_user_and_product['product']['id']}")
        assert product_response.json()["stock"] == created_user_and_product["product"]["stock"]
