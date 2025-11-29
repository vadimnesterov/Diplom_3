# data/user_data.py v1.2

from data.urls import Endpoints


class UserAPIData:
    """URL и методы для работы с пользователем через API."""

    # Создание пользователя
    USER_CREATE_URL = (
        Endpoints.CREATE_USER,
        "post",
    )

    # Авторизация пользователя
    USER_LOGIN_URL = (
        Endpoints.LOGIN,
        "post",
    )

    # Удаление пользователя
    USER_DELETE_URL = (
        Endpoints.DELETE_USER,
        "delete",
    )
