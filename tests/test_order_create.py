import pytest
import allure
import requests
from config import API_CONFIG
from helpers import get_fake_user_data

@allure.feature("Order API")
@allure.story("Order Creation")
class TestOrderCreate:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized_with_ingredients(self, fake_user_data):
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

        with allure.step("Подготовка: формирование списка ингредиентов"):
            ingredients = ["677c16a44100000000000001", "677c16a44100000000000002"]

        with allure.step("Действие: отправка запроса на создание заказа"):
            payload = {"ingredients": ingredients}
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(url_orders, json=payload, headers=headers)
        
        with allure.step("Проверка: статус ответа должен быть 200"):
            assert response.status_code == 200
        
        with allure.step("Проверка: в ответе присутствует поле 'order'"):
            data = response.json()
            assert "order" in data
        
        with allure.step("Проверка: список ингредиентов совпадает"):
            assert data["order"]["ingredients"] == ingredients

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self, fake_user_data):
        url_orders = f"{API_CONFIG.BASE_URL}{API_CONFIG.CREATE_ORDER}"

        with allure.step("Подготовка: payload с ингредиентами"):
            payload = {"ingredients": ["677c16a44100000000000001"]}

        with allure.step("Действие: отправка запроса без токена"):
            response = requests.post(url_orders, json=payload)
        
        with allure.step("Проверка: статус ответа должен быть 401"):
            assert response.status_code == 401

    @allure.title("Создание заказа с пустым списком ингредиентов")
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
        
        with allure.step("Проверка: статус ответа должен быть 400 согласно документации"):
            assert response.status_code == 400
        
        with allure.step("Проверка: в ответе присутствует сообщение об ошибке"):
            data = response.json()
            assert data.get("success") is False
            assert "message" in data or "error" in data

    @allure.title("Создание заказа с неверным хешем ингредиентов")
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
        
        with allure.step("Проверка: статус ответа должен быть 500 согласно документации для невалидного хеша"):
            assert response.status_code == 500