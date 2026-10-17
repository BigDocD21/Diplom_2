import pytest
import allure
import requests
from config import BASE_URL

@allure.feature("User API")
@allure.story("User Registration")
class TestUserCreate:

    @allure.title("Успешное создание нового пользователя")
    def test_create_new_user(self, base_url, random_login, random_password):
        with allure.step("Подготовка: формирование payload с уникальными данными"):
            payload = {
                "login": random_login,
                "password": random_password,
                "firstName": "Ivan"
            }

        with allure.step("Действие: отправка POST запроса на регистрацию"):
            response = requests.post(f"{base_url}/register", json=payload)

        with allure.step("Проверка: статус ответа должен быть 201"):
            assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        
        with allure.step("Проверка: в ответе присутствует поле 'id'"):
            data = response.json()
            assert "id" in data
        
        with allure.step("Проверка: флаг success в ответе равен True"):
            assert data["success"] is True

    @allure.title("Попытка создать пользователя с существующим логином")
    def test_create_existing_user(self, base_url, random_login, random_password):
        with allure.step("Подготовка: создание пользователя для первого запроса"):
            first_payload = {
                "login": random_login,
                "password": random_password,
                "firstName": "Ivan"
            }
            requests.post(f"{base_url}/register", json=first_payload)

        with allure.step("Подготовка: формирование payload для повторного запроса"):
            second_payload = {
                "login": random_login,
                "password": random_password,
                "firstName": "Ivan"
            }

        with allure.step("Действие: повторная отправка запроса с теми же данными"):
            response = requests.post(f"{base_url}/register", json=second_payload)

        with allure.step("Проверка: статус ответа должен быть 403 (Forbidden)"):
            assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"

    @allure.title("Создание пользователя без обязательного поля (login)")
    def test_create_without_login(self, base_url, random_password):
        with allure.step("Подготовка: формирование payload без поля login"):
            payload = {
                "password": random_password,
                "firstName": "Ivan"
            }

        with allure.step("Действие: отправка запроса без поля login"):
            response = requests.post(f"{base_url}/register", json=payload)

        with allure.step("Проверка: статус ответа должен быть 400 (Bad Request)"):
            assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"