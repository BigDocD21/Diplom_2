import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def get_fake_user_data():
    email = f"{generate_random_string(8)}@test.com"
    password = generate_random_string(10)
    name = generate_random_string(8)
    return {
        "email": email,
        "password": password,
        "name": name
    }