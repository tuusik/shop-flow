import pytest
from pydantic import ValidationError
from schemas.users import SUser
from schemas.products import SProduct


class TestUserSchema:
    def test_valid_user(self, user):
        assert user

    def test_bad_email(self):
        with pytest.raises(ValidationError):
            SUser(id=1, email="johndoe#gmail.com", created_at="2018-11-21")

    def test_bad_date(self):
        with pytest.raises(ValidationError):
            SUser(id=1, email="johndoe@gmail.com", created_at="21.11.2018")

    def test_missing_email(self):
        with pytest.raises(ValidationError):
            SUser(id=1, created_at="2018-11-21")

    def test_missing_id(self):
        with pytest.raises(ValidationError):
            SUser(email="test@test.com", created_at="2018-11-21")


class TestProductSchema:
    def test_valid_product(self):
        product = SProduct(
            id=1,
            title="Test",
            description="Desc",
            price=9.99,
            stock=5,
            created_at="2024-01-01",
        )
        assert product.title == "Test"
        assert product.price == 9.99

    def test_invalid_price_type(self):
        with pytest.raises(ValidationError):
            SProduct(
                id=1,
                title="Test",
                description="Desc",
                price="not-a-number",
                stock=5,
                created_at="2024-01-01",
            )

    def test_invalid_stock_type(self):
        with pytest.raises(ValidationError):
            SProduct(
                id=1,
                title="Test",
                description="Desc",
                price=10.0,
                stock="not-a-number",
                created_at="2024-01-01",
            )

    def test_missing_title(self):
        with pytest.raises(ValidationError):
            SProduct(
                id=1,
                description="Desc",
                price=10.0,
                stock=5,
                created_at="2024-01-01",
            )

    def test_bad_date(self):
        with pytest.raises(ValidationError):
            SProduct(
                id=1,
                title="Test",
                description="Desc",
                price=10.0,
                stock=5,
                created_at="not-a-date",
            )

    def test_from_attributes(self):
        product = SProduct.model_validate({
            "id": 1,
            "title": "Test",
            "description": "Desc",
            "price": 9.99,
            "stock": 5,
            "created_at": "2024-01-01",
        })
        assert product.title == "Test"
