from selenium.webdriver.common.by import By


class RegisterPageLocators:
    NAME_FIELD = (By.XPATH, "//label[text()='Имя']/following-sibling::input")
    EMAIL_FIELD = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_FIELD = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")

    REGISTER_BUTTON = (By.XPATH, "//button[normalize-space()='Зарегистрироваться']")

    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class, 'input__error') or contains(@class, 'error')]")
