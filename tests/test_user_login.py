import pytest
import allure
import requests
from config import API_CONFIG
from helpers import get_fake_user_data

@allure.feature("User API")
@allure.story("User Login")
class TestUserLogin:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_success(self, fake_user_data):
        url_register = f"{API_CONFIG.BASE_URL}{API_CONFIG.REGISTER}"
        url_login = f"{API_CONFIG.BASE_URL}{API_CONFIG.LOGIN}"

        with allure.step("Подготовка: регистрация пользователя"):
            requests.post(url_register, json=fake_user_data)

        with allure.step("Подготовка: формирование данных для авторизации"):
            login_payload = {
                "email": fake_user_data["email"],
                "password": fake_user_data["password"]
            }

        with allure.step("Действие: отправка запроса на авторизацию"):
            response = requests.post(url_login, json=login_payload)
        
        with allure.step("Проверка: статус ответа должен быть 200"):
            assert response.status_code == 200
        
        with allure.step("Проверка: в ответе присутствует поле 'accessToken'"):
            data = response.json()
            assert "accessToken" in data
        
        with allure.step("Проверка: флаг success в ответе равен True"):
            assert data["success"] is True

    @allure.title("Вход с неверным логином и паролем")
    def test_login_invalid_credentials(self, fake_user_data):
        url_login = f"{API_CONFIG.BASE_URL}{API_CONFIG.LOGIN}"

        with allure.step("Подготовка: формирование payload с неверными данными"):
            login_payload = {
                "email": "wrong_email_" + fake_user_data["email"],
                "password": "wrong_password_123"
            }

        with allure.step("Действие: отправка запроса с неверными учетными данными"):
            response = requests.post(url_login, json=login_payload)
        
        with allure.step("Проверка: статус ответа должен быть 401"):
            assert response.status_code == 401
        
        with allure.step("Проверка: в ответе присутствует сообщение об ошибке"):
            data = response.json()
            assert "message" in data or "error" in data