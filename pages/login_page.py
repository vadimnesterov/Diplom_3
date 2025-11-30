# pages/login_page.py
# version: v1.5

import allure

from data.urls import MainUrl, URLS
from .base_page import BasePage
from locators.login_page_locators import LoginPageLocators
from locators.constructor_page_locators import ConstructorPageLocators


class LoginPage(BasePage):
    """Страница логина."""

    @allure.step("Открыть страницу логина")
    def open_login(self):
        self.open(MainUrl.MAIN_URL + URLS.url_login)

    @allure.step("Ввести email")
    def set_email(self, email: str):
        self.fill(LoginPageLocators.EMAIL_FIELD, email)

    @allure.step("Ввести пароль")
    def set_password(self, password: str):
        self.fill(LoginPageLocators.PASSWORD_FIELD, password)

    @allure.step("Нажать кнопку 'Войти' и дождаться успешной авторизации")
    def submit_login(self) -> bool:
        """
        Нажать кнопку 'Войти' и дождаться успешной авторизации.
        Возвращает True, если логин прошёл успешно.
        """
        self.click(LoginPageLocators.LOGIN_BUTTON)

        return self.is_element_visible(
            ConstructorPageLocators.ORDER_BUTTON,
            timeout=10
        )

    @allure.step("Перейти на страницу регистрации")
    def go_to_register(self):
        """Переход на страницу регистрации."""
        self.click(LoginPageLocators.REGISTER_LINK)
