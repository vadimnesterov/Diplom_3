from .base_page import BasePage
from locators.login_page_locators import LoginPageLocators
from locators.constructor_page_locators import ConstructorPageLocators


class LoginPage(BasePage):
    """Страница логина."""

    def open_login(self):
        self.open("https://stellarburgers.education-services.ru/login")

    def set_email(self, email: str):
        self.type(LoginPageLocators.EMAIL_FIELD, email)

    def set_password(self, password: str):
        self.type(LoginPageLocators.PASSWORD_FIELD, password)

    def submit_login(self):
        """Нажать кнопку 'Войти' и дождаться загрузки конструктора."""
        self.click(LoginPageLocators.LOGIN_BUTTON)

        # SAFE: ждём появление кнопки 'Оформить заказ' после редиректа
        try:
            from pages.constructor_page import ConstructorPage
            ConstructorPage(self.driver).is_visible(ConstructorPageLocators.ORDER_BUTTON)
        except:
            pass

    def go_to_register(self):
        """Переход на страницу регистрации."""
        self.click(LoginPageLocators.REGISTER_LINK)
