import requests

from data.user_data import UserAPIData
from .common_api_helper import CommonApiHelper


class UserAPIHelper(CommonApiHelper):
    """Методы для работы с пользователем через API."""

    def create_user_request(self, data: dict) -> requests.Response:
        """
        Отправляет запрос на создание пользователя.
        Использует URL и метод из UserAPIData.USER_CREATE_URL.
        """
        url, method = UserAPIData.USER_CREATE_URL
        return requests.request(
            url=url,
            method=method,
            json=data,
        )

    def build_user_payload(self, keys: list[str] | None = None) -> dict:
        """
        Формирует словарь с данными пользователя: name / password / email.
        Если передан список keys — возвращает только указанные поля.
        """
        name = self.make_random_string(23)
        password = self.make_random_string(23)
        email = (
            f"{self.make_random_string(15)}@"
            f"{self.make_random_string(15)}notexists.com"
        )

        full_data = {
            "name": name,
            "password": password,
            "email": email,
        }

        if keys is None:
            return full_data

        return {key: full_data[key] for key in keys if key in full_data}

    def create_test_user(self, keys: list[str] | None = None) -> dict:
        """
        Создаёт тестового пользователя через API и возвращает его данные.
        Если ответ не 200, поднимает исключение с описанием ошибки.
        """
        user_data = self.build_user_payload(keys=keys)
        response = self.create_user_request(user_data)

        assert response.status_code == 200, (
            f"Ошибка при создании пользователя. "
            f"Код ответа: {response.status_code}, тело: {response.text}"
        )

        return user_data
