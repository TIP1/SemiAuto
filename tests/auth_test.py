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


@allure.suite('Base methods')
class TestBasicMethods:

    @allure.title('Auth test')
    def test_auth(self):

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
            print('Запрос успешно выполнен')
            print(response.json()['token'])
            assert response.status_code == 200
        else:
            print('Произошла ошибка:', response.status_code)
            assert False

    @allure.title('Upload test')
    def test_upload(self, auth_token, asset_create):

        query_params = {
            'upload_id': 1,
            'check_duplicates': True,
            'with_meta': False,
            'override_by_meta': False
        }

        file_names = os.listdir(f'{PROJECT_PATH}\\files')

        for file_name in file_names:

            file_path = f'{PROJECT_PATH}\\files\\{file_name}'
            file_size = os.stat(file_path).st_size  # значение в байтах

            headers = {
                'Authorization': f'Token {auth_token.auth_method()}',
            }

            test_files = {
                "file": open(file_path, 'rb')
            }

            if file_size / (1024 * 1024) > 5: # значение в мб
                headers['HTTP_CONTENT_RANGE'] = f'0-{file_size}/{file_size}'

            response = requests.post(url=f'{BASE_URL}/api/v1/content_import/assets/upload/{asset_create["pk"]}',
                                 params=query_params, headers=headers, files=test_files)

            if response.status_code == 200:
                print(f'Запрос успешно выполнен. Файл {file_name} загружен.')
                assert response.status_code == 200
            else:
                print(f'Произошла ошибка при загрузке файла {file_name}:', response.status_code)
                assert False

        query_params_search = {
            'ordering': 'file',
            'cursor': '1', #offset
            'page_size': 10 #limit
        }

        # response_search = requests.get(url=f'{BASE_URL}/api/v1/search/assets/',
        #                        params=query_params_search, headers=headers)

        response_search = requests.get(url=f'{BASE_URL}/api/v1/mutual_integration/find_assets/search/',
                               params=query_params_search, headers=headers)

        if response_search.status_code == 200:
            print(response.json())
            assert response.status_code == 200
        else:
            print('Произошла ошибка:', response_search.status_code)
            assert False


