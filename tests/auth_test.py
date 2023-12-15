import os
import requests
import json
import pytest
import allure

from dotenv import load_dotenv
from conftest import auth_token_fixture, asset_create_fixture
load_dotenv()

BASE_URL = os.getenv('BASE_URL')
USERNAME = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
PROJECT_PATH = '\\'.join(os.path.abspath(__file__).split('\\')[0:-2])


@allure.suite('Auth methods')
class TestAuthMethods:

    @allure.title('Auth test with correct data')
    def test_auth_correct_data(self):

        payload = {
            'username': USERNAME,
            'password': PASSWORD
        }

        json_payload = json.dumps(payload)

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(url=f'{BASE_URL}/api-token-auth/', data=json_payload, headers=headers)

        if response.status_code == 200:
            print('\nАутентификация прошла успешно с правильными данными.')
            print(f'\nПолучен токен: {response.json()["token"]}')
            assert response.status_code == 200
        else:
            print('\nПроизошла ошибка:', response.status_code)
            assert False

    @allure.title('Auth test with incorrect data')
    def test_auth_incorrect_data(self):

        payload = {
            'username': '1234',
            'password': '1234'
        }

        json_payload = json.dumps(payload)

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(url=f'{BASE_URL}/api-token-auth/', data=json_payload, headers=headers)

        if response.status_code == 400:
            print('\nАутентификация с неправильнымы данными не прошла')
            msg = response.json()['non_field_errors'][0]
            assert msg == 'wrong_username_or_password', f'\nТест провалился: {msg}'
        else:
            if response.status_code == 200:
                print('\nПрошла Аутентификация с неправильнымы данными')
                assert False
            print('\nПроизошла ошибка:', response.status_code)
            assert False


