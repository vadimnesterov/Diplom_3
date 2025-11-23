from selenium.webdriver.common.by import By


class RegisterPageLocators:
    """Локаторы элементов на странице регистрации."""

    # Поля ввода
    NAME_FIELD = (By.XPATH, "//label[text()='Имя']/following-sibling::input")
    EMAIL_FIELD = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_FIELD = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")

    # Кнопка "Зарегистрироваться"
    REGISTER_BUTTON = (By.XPATH, "//button[.//p[text()='Зарегистрироваться']]")

    # Ссылка "Войти"
    LOGIN_LINK = (By.LINK_TEXT, "Войти")

    # Сообщение об ошибке (например, короткий пароль)
    ERROR_MESSAGE = (
        By.XPATH,
        "//p[contains(@class,'input__error') or contains(@class,'error')]",
    )
