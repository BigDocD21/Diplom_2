import pytest
from helpers import get_fake_user_data

@pytest.fixture
def fake_user_data():
    return get_fake_user_data()