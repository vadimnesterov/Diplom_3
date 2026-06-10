import allure

from data.urls import MainUrl, URLS
from .base_page import BasePage
from locators.login_page_locators import LoginPageLocators
from locators.constructor_page_locators import ConstructorPageLocators


class LoginPage(BasePage):
    """Login page."""

    @allure.step("Open the login page")
    def open_login(self):
        self.open(MainUrl.MAIN_URL + URLS.url_login)

    @allure.step("Enter email")
    def set_email(self, email: str):
        self.fill(LoginPageLocators.EMAIL_FIELD, email)

    @allure.step("Enter password")
    def set_password(self, password: str):
        self.fill(LoginPageLocators.PASSWORD_FIELD, password)

    @allure.step("Click the 'Login' button and wait for successful authorisation")
    def submit_login(self) -> bool:
        """Returns True if login succeeded."""
        self.click(LoginPageLocators.LOGIN_BUTTON)

        return self.is_element_visible(
            ConstructorPageLocators.ORDER_BUTTON,
            timeout=10
        )

    @allure.step("Navigate to the registration page")
    def go_to_register(self):
        self.click(LoginPageLocators.REGISTER_LINK)
