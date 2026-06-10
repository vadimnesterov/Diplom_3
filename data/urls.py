class MainUrl:
    MAIN_URL = "https://stellarburgers.education-services.ru/"


class URLS:
    """Relative URL paths for Stellar Burgers pages."""
    url_feed = "feed"                            # Order feed page
    url_login = "login"                          # Login page
    url_recovery = "forgot-password"             # Password recovery page
    url_register = "register"                    # User registration page
    url_profile_area = "account/profile"         # User profile page
    url_history_order = "account/order-history"  # Order history page
    url_reset_password = "reset-password"        # Password reset page


class Endpoints:
    """Full API endpoint URLs (base URL + path)."""
    CREATE_USER = f"{MainUrl.MAIN_URL}api/auth/register"
    LOGIN = f"{MainUrl.MAIN_URL}api/auth/login"
    DELETE_USER = f"{MainUrl.MAIN_URL}api/auth/user"
    CREATE_ORDER = f"{MainUrl.MAIN_URL}api/orders"
    GET_ORDERS = f"{MainUrl.MAIN_URL}api/orders"
    GET_USER_ORDERS = f"{MainUrl.MAIN_URL}api/orders"
    GET_ALL_ORDERS = f"{MainUrl.MAIN_URL}api/orders/all"
