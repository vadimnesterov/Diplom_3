from data.urls import REGISTER_PAGE
from locators.register_page_locators import RegisterPageLocators
from .base_page import BasePage


class RegisterPage(BasePage):
    """Страница регистрации."""

    def open_register(self):
        """Открыть страницу регистрации."""
        self.open(REGISTER_PAGE)

    def set_name(self, name: str):
        """Заполнить поле имени."""
        self.type_text(RegisterPageLocators.NAME_FIELD, name)

    def set_email(self, email: str):
        """Заполнить поле email."""
        self.type_text(RegisterPageLocators.EMAIL_FIELD, email)

    def set_password(self, password: str):
        """Заполнить поле пароля."""
        self.type_text(RegisterPageLocators.PASSWORD_FIELD, password)

    def submit_register(self):
        """Нажать кнопку 'Зарегистрироваться'."""
        self.click(RegisterPageLocators.REGISTER_BUTTON)

    def go_to_login(self):
        """Перейти по ссылке 'Войти'."""
        self.click(RegisterPageLocators.LOGIN_LINK)

    def get_error_message(self) -> str:
        """Получить текст ошибки регистрации."""
        return self.get_text(RegisterPageLocators.ERROR_MESSAGE)
