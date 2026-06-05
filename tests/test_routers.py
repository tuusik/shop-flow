import pytest


class TestUsers:
    def test_create_user(self, client, user_data):
        response = client.post("/users", json=user_data)
        assert response.status_code == 201

    def test_create_duplicate_user(self, client, user_data, created_user):
        response = client.post("/users", json=user_data)
        assert response.status_code == 400

    def test_get_users_list(self, client, created_user):
        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert any(u["email"] == created_user["email"] for u in users)

    def test_get_user_by_id(self, client, created_user):
        response = client.get(f"/users/{created_user['id']}")
        assert response.status_code == 200
        assert response.json()["email"] == created_user["email"]

    def test_delete_user(self, client, created_user):
        response = client.delete(f"/users/{created_user['id']}")
        assert response.status_code == 204

    def test_delete_nonexistent_user(self, client):
        response = client.delete("/users/9999")
        assert response.status_code == 404

    def test_get_user_returns_correct_fields(self, client, created_user):
        response = client.get(f"/users/{created_user['id']}")
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert "created_at" in data


class TestProducts:
    def test_create_product(self, client, product_data):
        response = client.post("/products", json=product_data)
        assert response.status_code == 201

    def test_create_duplicate_product(self, client, product_data, created_product):
        response = client.post("/products", json=product_data)
        assert response.status_code == 400

    def test_get_products_list(self, client, created_product):
        response = client.get("/products")
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert any(p["title"] == created_product["title"] for p in products)

    def test_get_product_by_id(self, client, created_product):
        response = client.get(f"/products/{created_product['id']}")
        assert response.status_code == 200
        assert response.json()["title"] == created_product["title"]

    def test_delete_nonexistent_product(self, client):
        response = client.delete("/products/9999")
        assert response.status_code == 404

    def test_get_product_returns_correct_fields(self, client, created_product):
        response = client.get(f"/products/{created_product['id']}")
        data = response.json()
        assert "id" in data
        assert "title" in data
        assert "description" in data
        assert "price" in data
        assert "stock" in data
        assert "created_at" in data
