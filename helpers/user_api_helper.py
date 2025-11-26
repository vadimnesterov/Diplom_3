# helpers/user_api_helper.py v1.1

import requests

from data.user_data import UserAPIData
from .common_api_helper import CommonApiHelper


class UserAPIHelper(CommonApiHelper):
    """Методы для работы с пользователем через API."""

    def create_user_request(self, data: dict) -> requests.Response:
        url, method = UserAPIData.USER_CREATE_URL
        return requests.request(
            url=url,
            method=method,
            json=data,
        )

    def login_user_request(self, data: dict) -> requests.Response:
        url, method = UserAPIData.USER_LOGIN_URL
        return requests.request(
            url=url,
            method=method,
            json=data,
        )

    def delete_user_request(self, token: str) -> requests.Response:
        url, method = UserAPIData.USER_DELETE_URL
        headers = {"Authorization": token}
        return requests.request(
            url=url,
            method=method,
            headers=headers,
        )

    def build_user_payload(self) -> dict:
        name = self.make_random_string(23)
        password = self.make_random_string(23)
        email = (
            f"{self.make_random_string(15)}@"
            f"{self.make_random_string(15)}notexists.com"
        )

        return {
            "name": name,
            "password": password,
            "email": email,
        }

    def create_test_user(self) -> dict:
        user_data = self.build_user_payload()
        response = self.create_user_request(user_data)

        assert response.status_code == 200, (
            f"Ошибка при создании пользователя. "
            f"Код ответа: {response.status_code}, тело: {response.text}"
        )

        return user_data

    def delete_user(self, token: str):
        response = self.delete_user_request(token)
        assert response.status_code in (200, 202), (
            f"Ошибка при удалении пользователя. "
            f"Код ответа: {response.status_code}, тело: {response.text}"
        )
