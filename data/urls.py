# data/urls.py v1.2

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
    """Ручки для работы с API (через базовый MAIN_URL)"""
    CREATE_USER = f"{MainUrl.MAIN_URL}api/auth/register"
    LOGIN = f"{MainUrl.MAIN_URL}api/auth/login"
    DELETE_USER = f"{MainUrl.MAIN_URL}api/auth/user"
    CREATE_ORDER = f"{MainUrl.MAIN_URL}api/orders"
    GET_ORDERS = f"{MainUrl.MAIN_URL}api/orders"
    GET_USER_ORDERS = f"{MainUrl.MAIN_URL}api/orders"
    GET_ALL_ORDERS = f"{MainUrl.MAIN_URL}api/orders/all"
