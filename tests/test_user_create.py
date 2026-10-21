import pytest
import allure
import requests
from config import API_CONFIG
from helpers import get_fake_user_data

@allure.feature("User API")
@allure.story("User Registration")
class TestUserCreate:

    @allure.title("Успешное создание нового пользователя")
    def test_create_new_user(self, fake_user_data):
        url = f"{API_CONFIG.BASE_URL}{API_CONFIG.REGISTER}"
        payload = {
            "email": fake_user_data["email"],
            "password": fake_user_data["password"],
            "name": fake_user_data["name"]
        }

        with allure.step("Действие: отправка POST запроса на регистрацию"):
            response = requests.post(url, json=payload)

        with allure.step("Проверка: статус ответа должен быть 200"):
            assert response.status_code == 200
        
        with allure.step("Проверка: в ответе присутствует поле 'success' и оно равно True"):
            data = response.json()
            assert data.get("success") is True

    @allure.title("Попытка создать пользователя с существующим email")
    def test_create_existing_user(self, fake_user_data):
        url = f"{API_CONFIG.BASE_URL}{API_CONFIG.REGISTER}"
        payload = {
            "email": fake_user_data["email"],
            "password": fake_user_data["password"],
            "name": fake_user_data["name"]
        }

        with allure.step("Подготовка: создание пользователя для первого запроса"):
            requests.post(url, json=payload)

        with allure.step("Действие: повторная отправка запроса с теми же данными"):
            response = requests.post(url, json=payload)

        with allure.step("Проверка: статус ответа должен быть 403 (Forbidden)"):
            assert response.status_code == 403

    @allure.title("Создание пользователя без обязательного поля (email)")
    def test_create_without_email(self, fake_user_data):
        url = f"{API_CONFIG.BASE_URL}{API_CONFIG.REGISTER}"
        payload = {
            "password": fake_user_data["password"],
            "name": fake_user_data["name"]
        }

        with allure.step("Действие: отправка запроса без поля email"):
            response = requests.post(url, json=payload)

        with allure.step("Проверка: статус ответа должен быть 403 (согласно документации для отсутствующих полей)"):
            assert response.status_code == 403