# pages/login_page.py v1.2

from data.urls import MainUrl, URLS
from .base_page import BasePage
from locators.login_page_locators import LoginPageLocators
from locators.constructor_page_locators import ConstructorPageLocators
from data.urls import URLS


class LoginPage(BasePage):
    """Страница логина."""

    def open_login(self):
        self.open(MainUrl.MAIN_URL + URLS.url_login)

    def set_email(self, email: str):
        self.type(LoginPageLocators.EMAIL_FIELD, email)

    def set_password(self, password: str):
        self.type(LoginPageLocators.PASSWORD_FIELD, password)

    def submit_login(self) -> bool:
        """
        Нажать кнопку 'Войти' и дождаться успешной авторизации.
        Возвращает True, если логин прошёл успешно.
        """
        self.click(LoginPageLocators.LOGIN_BUTTON)

        # ЯВНО ждём появления кнопки "Оформить заказ"
        return self.is_element_visible(
            ConstructorPageLocators.ORDER_BUTTON,
            timeout=10
        )

    def go_to_register(self):
        """Переход на страницу регистрации."""
        self.click(LoginPageLocators.REGISTER_LINK)
