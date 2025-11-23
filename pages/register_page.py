from .base_page import BasePage
from locators.register_page_locators import RegisterPageLocators


class RegisterPage(BasePage):
    """Страница регистрации."""

    def open_register(self):
        self.open("https://stellarburgers.education-services.ru/register")

    def set_name(self, name: str):
        self.type(RegisterPageLocators.NAME_FIELD, name)

    def set_email(self, email: str):
        self.type(RegisterPageLocators.EMAIL_FIELD, email)

    def set_password(self, password: str):
        self.type(RegisterPageLocators.PASSWORD_FIELD, password)

    def submit_register(self):
        self.click(RegisterPageLocators.REGISTER_BUTTON)
