import pytest
import allure
import requests
from config import API_CONFIG
from helpers import get_fake_user_data

@allure.feature("Order API")
@allure.story("Order Creation")
class TestOrderCreate:

    @allure.title("Создание заказа с авторизацией и реальными ингредиентами")
    def test_create_order_authorized_with_ingredients(self, fake_user_data):
        url_register = f"{API_CONFIG.BASE_URL}{API_CONFIG.REGISTER}"
        url_login = f"{API_CONFIG.BASE_URL}{API_CONFIG.LOGIN}"
        url_orders = f"{API_CONFIG.BASE_URL}{API_CONFIG.CREATE_ORDER}"
        url_ingredients = f"{API_CONFIG.BASE_URL}/api/ingredients"

        with allure.step("Подготовка: создание тестового пользователя"):
            requests.post(url_register, json=fake_user_data)

        with allure.step("Подготовка: получение токена авторизации"):
            login_payload = {
                "email": fake_user_data["email"],
                "password": fake_user_data["password"]
            }
            login_resp = requests.post(url_login, json=login_payload)
            token = login_resp.json()["accessToken"]

        with allure.step("Подготовка: получение реальных ID ингредиентов из API"):
            ingredients_resp = requests.get(url_ingredients)
            ingredients_data = ingredients_resp.json()["data"]
            if len(ingredients_data) < 2:
                pytest.skip("Недостаточно ингредиентов в базе для теста")
            ingredients = [
                ingredients_data[0]["_id"],
                ingredients_data[1]["_id"]
            ]

        with allure.step("Действие: отправка запроса на создание заказа"):
            payload = {"ingredients": ingredients}
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(url_orders, json=payload, headers=headers)

        assert response.status_code == 200 and "order" in response.json()

    @allure.title("Попытка создания заказа без авторизации (должна быть ошибка 401)")
    def test_create_order_unauthorized(self, fake_user_data):
        url_orders = f"{API_CONFIG.BASE_URL}{API_CONFIG.CREATE_ORDER}"
        url_ingredients = f"{API_CONFIG.BASE_URL}/api/ingredients"

        with allure.step("Подготовка: получение валидных ID ингредиентов"):
            ingredients_resp = requests.get(url_ingredients)
            ingredients_data = ingredients_resp.json()["data"]
            if not ingredients_data:
                pytest.skip("Нет ингредиентов в базе")
            ingredients = [ingredients_data[0]["_id"]]

        with allure.step("Действие: отправка запроса без токена"):
            payload = {"ingredients": ingredients}
            response = requests.post(url_orders, json=payload)

        assert response.status_code == 401

    @allure.title("Создание заказа с пустым списком ингредиентов (должна быть ошибка 400)")
    def test_create_order_with_empty_ingredients(self, fake_user_data):
        url_register = f"{API_CONFIG.BASE_URL}{API_CONFIG.REGISTER}"
        url_login = f"{API_CONFIG.BASE_URL}{API_CONFIG.LOGIN}"
        url_orders = f"{API_CONFIG.BASE_URL}{API_CONFIG.CREATE_ORDER}"

        with allure.step("Подготовка: создание тестового пользователя"):
            requests.post(url_register, json=fake_user_data)

        with allure.step("Подготовка: получение токена авторизации"):
            login_payload = {
                "email": fake_user_data["email"],
                "password": fake_user_data["password"]
            }
            login_resp = requests.post(url_login, json=login_payload)
            token = login_resp.json()["accessToken"]

        with allure.step("Подготовка: пустой список ингредиентов"):
            payload = {"ingredients": []}

        with allure.step("Действие: отправка запроса с пустым списком"):
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(url_orders, json=payload, headers=headers)

        assert response.status_code == 400 and response.json().get("success") is False

    @allure.title("Создание заказа с неверным хешем ингредиентов (должна быть ошибка 500)")
    def test_create_order_invalid_ingredients(self, fake_user_data):
        url_register = f"{API_CONFIG.BASE_URL}{API_CONFIG.REGISTER}"
        url_login = f"{API_CONFIG.BASE_URL}{API_CONFIG.LOGIN}"
        url_orders = f"{API_CONFIG.BASE_URL}{API_CONFIG.CREATE_ORDER}"

        with allure.step("Подготовка: создание тестового пользователя"):
            requests.post(url_register, json=fake_user_data)

        with allure.step("Подготовка: получение токена авторизации"):
            login_payload = {
                "email": fake_user_data["email"],
                "password": fake_user_data["password"]
            }
            login_resp = requests.post(url_login, json=login_payload)
            token = login_resp.json()["accessToken"]

        with allure.step("Подготовка: неверный хеш ингредиентов"):
            payload = {"ingredients": ["invalid_hash_123"]}

        with allure.step("Действие: отправка запроса с неверным хешем"):
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(url_orders, json=payload, headers=headers)

        assert response.status_code == 500