from selenium.webdriver.common.by import By


class LoginPageLocators:
    """Locators for the Login page."""

    EMAIL_FIELD = (By.XPATH, "//label[text()='Email']/following-sibling::input")         # Email input field
    PASSWORD_FIELD = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")     # Password input field
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Войти']")                     # "Log in" submit button
    REGISTER_LINK = (By.XPATH, "//a[normalize-space()='Зарегистрироваться']")            # "Register" navigation link
    MODAL_OVERLAY = (By.CSS_SELECTOR, "div.Modal_modal_overlay__x2ZCr")                  # Modal overlay backdrop
