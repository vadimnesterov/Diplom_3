# data/user_data.py v1.1

class UserAPIData:
    """URL и методы для работы с пользователем через API."""

    BASE_API_URL = "https://stellarburgers.education-services.ru/api"

    # ✅ Создание пользователя
    USER_CREATE_URL = (
        f"{BASE_API_URL}/auth/register",
        "post",
    )

    # ✅ Авторизация пользователя
    USER_LOGIN_URL = (
        f"{BASE_API_URL}/auth/login",
        "post",
    )

    # ✅ Удаление пользователя
    USER_DELETE_URL = (
        f"{BASE_API_URL}/auth/user",
        "delete",
    )
