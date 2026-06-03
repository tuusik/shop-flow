import pytest
from pydantic import ValidationError
from schemas.users import SUser

def test_user_schema(user):
    assert user

def test_user_schema_with_bad_email():
    with pytest.raises(ValidationError):
        SUser(id=1, email="johndoe#gmail.com", created_at="2018-11-21")

def test_user_schema_with_bad_date():
    with pytest.raises(ValidationError):
        SUser(id=1, email="johndoe@gmail.com", created_at="21.11.2018")