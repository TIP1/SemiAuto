import os
import requests
import json
import pytest

from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('BASE_URL')
USERNAME = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')


@pytest.fixture(name="auth_token", scope="class")
def auth_token_fixture():
    class BasicAuth:
        def __init__(self):
            self.token = ''

        def auth_method(self):
            payload = {
                'username': USERNAME,
                'password': PASSWORD
            }

            json_payload = json.dumps(payload)

            headers = {
                'Content-Type': 'application/json',
            }

            response = requests.post(url=f'{BASE_URL}/api-token-auth/', data=json_payload, headers=headers)

            self.token = response.json()['token']
            return self.token

    return BasicAuth()


@pytest.fixture(name="asset_create", scope="class")
def asset_create_fixture(auth_token):
    payload = {
        "content_type": "base",
        "external_id": "Уникальная_строка_1",
        "values": {
            "title": "Limansky",
            "description": "test"
        }
    }

    json_payload = json.dumps(payload)

    headers = {
        'Authorization': f'Token {auth_token.auth_method()}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url=f'{BASE_URL}/api/v1/content_import/assets/create', data=json_payload,
                                     headers=headers)

    return response.json()