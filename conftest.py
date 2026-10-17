import pytest
import random
import string
from helpers import get_fake_credentials
from config import BASE_URL

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def random_login():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

@pytest.fixture
def random_password():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

@pytest.fixture
def fake_user_data():
    return get_fake_credentials()