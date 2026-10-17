import pytest
import allure
import requests
from config import BASE_URL

@allure.feature("User API")
@allure.story("User Login")
class TestUserLogin:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_success(self, base_url, random_login, random_password):
        with allure.step("Подготовка: формирование данных для регистрации"):
            reg_payload = {
                "login": random_login,
                "password": random_password,
                "firstName": "Ivan"
            }
        
        with allure.step("Действие: регистрация пользователя"):
            requests.post(f"{base_url}/register", json=reg_payload)

        with allure.step("Подготовка: формирование данных для авторизации"):
            login_payload = {
                "login": random_login,
                "password": random_password
            }

        with allure.step("Действие: отправка запроса на авторизацию"):
            response = requests.post(f"{base_url}/login", json=login_payload)
        
        with allure.step("Проверка: статус ответа должен быть 200"):
            assert response.status_code == 200
        
        with allure.step("Проверка: в ответе присутствует поле 'accessToken'"):
            data = response.json()
            assert "accessToken" in data
        
        with allure.step("Проверка: флаг success в ответе равен True"):
            assert data["success"] is True

    @allure.title("Вход с неверным логином и паролем")
    def test_login_invalid_credentials(self, base_url, random_login, random_password):
        with allure.step("Подготовка: формирование payload с неверными данными"):
            login_payload = {
                "login": "wrong_login_" + random_login,
                "password": "wrong_password_123"
            }

        with allure.step("Действие: отправка запроса с неверными учетными данными"):
            response = requests.post(f"{base_url}/login", json=login_payload)
        
        with allure.step("Проверка: статус ответа должен быть 401"):
            assert response.status_code == 401
        
        with allure.step("Проверка: в ответе присутствует сообщение об ошибке"):
            data = response.json()
            assert "message" in data or "error" in data
    