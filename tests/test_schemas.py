import pytest
from pydantic import ValidationError
from schemas.users import SUser, SUserBase, SUserPatch
from schemas.products import SProduct, SProductBase, SProductPatch
from uuid import UUID


class TestUserSchema:
    def test_valid_user(self, user):
        assert user

    def test_bad_email(self):
        with pytest.raises(ValidationError):
            SUser(id=UUID("12345678-1234-5678-1234-567812345678"), email="johndoe#gmail.com", created_at="2018-11-21")

    def test_bad_date(self):
        with pytest.raises(ValidationError):
            SUser(id=UUID("12345678-1234-5678-1234-567812345678"), email="johndoe@gmail.com", created_at="21.11.2018")

    def test_missing_email(self):
        with pytest.raises(ValidationError):
            SUser(id=UUID("12345678-1234-5678-1234-567812345678"), created_at="2018-11-21")

    def test_base_without_id(self):
        user = SUserBase(email="test@test.com", created_at="2018-11-21")
        assert user.email == "test@test.com"

    def test_patch_optional_fields(self):
        patch = SUserPatch(email="new@test.com")
        assert patch.email == "new@test.com"
        assert patch.created_at is None


class TestProductSchema:
    def test_valid_product(self):
        product = SProduct(
            id=UUID("12345678-1234-5678-1234-567812345678"),
            title="Test",
            description="Desc",
            price=9.99,
            stock=5,
            created_at="2024-01-01",
        )
        assert product.title == "Test"
        assert product.price == 9.99

    def test_base_without_id(self):
        product = SProductBase(title="Test", description="Desc", price=9.99, stock=5, created_at="2024-01-01")
        assert product.title == "Test"

    def test_patch_optional_fields(self):
        patch = SProductPatch(title="New Title")
        assert patch.title == "New Title"
        assert patch.description is None
        assert patch.price is None

    def test_invalid_price_type(self):
        with pytest.raises(ValidationError):
            SProduct(
                id=UUID("12345678-1234-5678-1234-567812345678"),
                title="Test",
                description="Desc",
                price="not-a-number",
                stock=5,
                created_at="2024-01-01",
            )

    def test_invalid_stock_type(self):
        with pytest.raises(ValidationError):
            SProduct(
                id=UUID("12345678-1234-5678-1234-567812345678"),
                title="Test",
                description="Desc",
                price=10.0,
                stock="not-a-number",
                created_at="2024-01-01",
            )

    def test_missing_title(self):
        with pytest.raises(ValidationError):
            SProduct(
                id=UUID("12345678-1234-5678-1234-567812345678"),
                description="Desc",
                price=10.0,
                stock=5,
                created_at="2024-01-01",
            )

    def test_bad_date(self):
        with pytest.raises(ValidationError):
            SProduct(
                id=UUID("12345678-1234-5678-1234-567812345678"),
                title="Test",
                description="Desc",
                price=10.0,
                stock=5,
                created_at="not-a-date",
            )

    def test_from_attributes(self):
        product = SProduct.model_validate({
            "id": "12345678-1234-5678-1234-567812345678",
            "title": "Test",
            "description": "Desc",
            "price": 9.99,
            "stock": 5,
            "created_at": "2024-01-01",
        })
        assert product.title == "Test"
