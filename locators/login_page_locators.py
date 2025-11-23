from selenium.webdriver.common.by import By


class LoginPageLocators:
    """Локаторы страницы логина."""

    EMAIL_FIELD = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_FIELD = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")


    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Войти']")

    REGISTER_LINK = (By.XPATH, "//a[normalize-space()='Зарегистрироваться']")

    MODAL_OVERLAY = (By.CSS_SELECTOR, "div.Modal_modal_overlay__x2ZCr")

