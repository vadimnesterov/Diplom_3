from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPageLocators:
    EMAIL_FIELD = (By.XPATH, "//input[@name='name']")
    PASSWORD_FIELD = (By.XPATH, "//input[@type='password']")

    # Кнопка "Войти" — стабильный CSS локатор
    LOGIN_BUTTON = (
        By.CSS_SELECTOR,
        "button.button_button__33qZ0.button_button_type_primary__1O7Bx.button_button_size_medium__3zxIa"
    )

    # Дублирующий локатор по тексту — fallback
    LOGIN_BUTTON_TEXT = (By.XPATH, "//button[normalize-space()='Войти']")

    # Кнопка перехода на страницу логина с главной
    ENTER_ACCOUNT_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']")

    # Кнопка перехода "Войти" на странице регистрации
    ENTER_FROM_REGISTER = (By.XPATH, "//a[text()='Войти']")


class LoginPage(BasePage):

    def open_login(self):
        self.click(LoginPageLocators.ENTER_ACCOUNT_BUTTON)

    def set_email(self, email):
        self.type(LoginPageLocators.EMAIL_FIELD, email)

    def set_password(self, password):
        self.type(LoginPageLocators.PASSWORD_FIELD, password)

    def submit_login(self):
        # 1 попытка — клик по стабильному CSS
        try:
            self.click(LoginPageLocators.LOGIN_BUTTON)
        except Exception:
            # fallback
            self.click(LoginPageLocators.LOGIN_BUTTON_TEXT)
