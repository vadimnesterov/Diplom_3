"""
Тестовый пользователь для UI-тестов
"""

# ДАННЫЕ ДЛЯ СТАБИЛЬНЫХ UI-ТЕСТОВ (как было у тебя)
TEST_USER_EMAIL = "ui_tester@example.com"
TEST_USER_PASSWORD = "123456"
TEST_USER_NAME = "UITester"


# --- API-константы для автогенерации пользователей ---
class UserAPIData:
    """URL и методы для работы с пользователем через API."""

    # Создание пользователя
    USER_CREATE_URL = (
        "https://stellarburgers.nomoreparties.site/api/auth/register",
        "post",
    )

    # Авторизация пользователя
    USER_LOGIN_URL = (
        "https://stellarburgers.nomoreparties.site/api/auth/login",
        "post",
    )
