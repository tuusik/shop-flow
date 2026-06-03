import pytest
from schemas.users import SUser

@pytest.fixture
def user():
    return SUser(id=1, email="johndoe@gmail.com", created_at="2018-11-21")
