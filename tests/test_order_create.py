import pytest
import allure
import requests
from config import BASE_URL

@allure.feature("Order API")
@allure.story("Order Creation")
class TestOrderCreate:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized_with_ingredients(self, base_url, random_login, random_password):
        with allure.step("Подготовка: создание тестового пользователя"):
            reg_payload = {
                "login": random_login,
                "password": random_password,
                "firstName": "Ivan"
            }
            requests.post(f"{base_url}/register", json=reg_payload)

        with allure.step("Подготовка: получение токена авторизации"):
            login_payload = {
                "login": random_login,
                "password": random_password
            }
            login_resp = requests.post(f"{base_url}/login", json=login_payload)
            token = login_resp.json()["accessToken"]

        with allure.step("Подготовка: формирование списка ингредиентов"):
            ingredients = ["677c16a44100000000000001", "677c16a44100000000000002"]

        with allure.step("Действие: отправка запроса на создание заказа"):
            payload = {"ingredients": ingredients}
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(f"{base_url}/orders", json=payload, headers=headers)
        
        with allure.step("Проверка: статус ответа должен быть 200"):
            assert response.status_code == 200
        
        with allure.step("Проверка: в ответе присутствует поле 'order'"):
            data = response.json()
            assert "order" in data
        
        with allure.step("Проверка: список ингредиентов совпадает"):
            assert data["order"]["ingredients"] == ingredients

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self, base_url):
        with allure.step("Подготовка: payload с ингредиентами"):
            payload = {"ingredients": ["677c16a44100000000000001"]}

        with allure.step("Действие: отправка запроса без токена"):
            response = requests.post(f"{base_url}/orders", json=payload)
        
        with allure.step("Проверка: статус ответа должен быть 401"):
            assert response.status_code == 401
    @allure.title("Создание заказа с пустым списком ингредиентов")
    def test_create_order_with_empty_ingredients(self, base_url, random_login, random_password):
        with allure.step("Подготовка: создание тестового пользователя"):
            reg_payload = {
                "login": random_login,
                "password": random_password,
                "firstName": "Ivan"
            }
            requests.post(f"{base_url}/register", json=reg_payload)

        with allure.step("Подготовка: получение токена авторизации"):
            login_payload = {
                "login": random_login,
                "password": random_password
            }
            login_resp = requests.post(f"{base_url}/login", json=login_payload)
            token = login_resp.json()["accessToken"]

        with allure.step("Подготовка: пустой список ингредиентов"):
            payload = {"ingredients": []}

        with allure.step("Действие: отправка запроса с пустым списком"):
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(f"{base_url}/orders", json=payload, headers=headers)
        
        with allure.step("Проверка: статус ответа должен быть 200"):
            assert response.status_code == 200
        
        with allure.step("Проверка: в ответе присутствует поле 'order'"):
            data = response.json()
            assert "order" in data
        
        with allure.step("Проверка: список ингредиентов в заказе пустой"):
            assert data["order"]["ingredients"] == []

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredients(self, base_url, random_login, random_password):
        with allure.step("Подготовка: создание тестового пользователя"):
            reg_payload = {
                "login": random_login,
                "password": random_password,
                "firstName": "Ivan"
            }
            requests.post(f"{base_url}/register", json=reg_payload)

        with allure.step("Подготовка: получение токена авторизации"):
            login_payload = {
                "login": random_login,
                "password": random_password
            }
            login_resp = requests.post(f"{base_url}/login", json=login_payload)
            token = login_resp.json()["accessToken"]

        with allure.step("Подготовка: неверный хеш ингредиентов"):
            payload = {"ingredients": ["invalid_hash_123"]}

        with allure.step("Действие: отправка запроса с неверным хешем"):
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(f"{base_url}/orders", json=payload, headers=headers)
        
        with allure.step("Проверка: статус ответа должен быть 400"):
            assert response.status_code == 400