# data/urls.py

class MainUrl:
    MAIN_URL = "https://stellarburgers.education-services.ru/"


class URLS:
    """URLs сервиса"""
    url_feed = "feed"                            # Лента заказов
    url_login = "login"                          # Авторизация
    url_recovery = "forgot-password"             # Восстановление пароля
    url_register = "register"                    # Регистрация пользователя
    url_profile_area = "account/profile"         # Личный кабинет
    url_history_order = "account/order-history"  # История заказов
    url_reset_password = "reset-password"        # Сброс пароля


class Endpoints:
    """Ручки для работы с API"""
    CREATE_USER = "api/auth/register"
    LOGIN = "api/auth/login"
    DELETE_USER = "api/auth/user"
    CREATE_ORDER = "api/orders"
    GET_ORDERS = "api/orders"
    GET_USER_ORDERS = "api/orders"
    GET_ALL_ORDERS = "api/orders/all"


# --- совместимость с прежними константами ---

MAIN_PAGE = MainUrl.MAIN_URL
LOGIN_PAGE = MAIN_PAGE + URLS.url_login
REGISTER_PAGE = MAIN_PAGE + URLS.url_register
PROFILE_PAGE = MAIN_PAGE + URLS.url_profile_area
FEED_PAGE = MAIN_PAGE + URLS.url_feed
