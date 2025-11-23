from selenium.webdriver.common.by import By


class LoginPageLocators:
    """Локаторы элементов на странице логина."""

    # Поля ввода
    EMAIL_FIELD = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_FIELD = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")

    # Кнопка входа
    LOGIN_BUTTON = (By.XPATH, "//button[.//p[text()='Войти']]")

    # Ссылка "Зарегистрироваться"
    REGISTER_LINK = (By.LINK_TEXT, "Зарегистрироваться")

    # Ссылка "Восстановить пароль"
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Восстановить пароль")

    # Сообщение об ошибке (если пароль неверный)
    ERROR_MESSAGE = (
        By.XPATH,
        "//p[contains(@class,'input__error') or contains(@class,'error')]",
    )
