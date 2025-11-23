from data.urls import LOGIN_PAGE
from locators.login_page_locators import LoginPageLocators
from .base_page import BasePage


class LoginPage(BasePage):
    """Страница логина."""

    def open_login(self):
        """Открыть страницу логина."""
        self.open(LOGIN_PAGE)

    def set_email(self, email: str):
        """Заполнить поле email."""
        self.type_text(LoginPageLocators.EMAIL_FIELD, email)

    def set_password(self, password: str):
        """Заполнить поле пароля."""
        self.type_text(LoginPageLocators.PASSWORD_FIELD, password)

    def submit_login(self):
        """Нажать кнопку 'Войти'."""
        self.click(LoginPageLocators.LOGIN_BUTTON)

    def go_to_register(self):
        """Перейти по ссылке 'Зарегистрироваться'."""
        self.click(LoginPageLocators.REGISTER_LINK)

    def go_to_forgot_password(self):
        """Перейти по ссылке 'Восстановить пароль'."""
        self.click(LoginPageLocators.FORGOT_PASSWORD_LINK)

    def get_error_message(self) -> str:
        """Получить текст ошибки авторизации."""
        return self.get_text(LoginPageLocators.ERROR_MESSAGE)
