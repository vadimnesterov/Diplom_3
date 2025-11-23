from selenium.webdriver.common.by import By


class LoginPageLocators:
    """Локаторы элементов на странице логина."""

    # Поля ввода
    EMAIL_FIELD = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_FIELD = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")

    # Кнопка входа — стабильный CSS локатор
    LOGIN_BUTTON = (
        By.CSS_SELECTOR,
        "button.button_button__33qZ0.button_button_type_primary__1O7Bx.button_button_size_medium__3zxIa"
    )

    # Fallback по тексту
    LOGIN_BUTTON_TEXT = (By.XPATH, "//button[normalize-space()='Войти']")

    # Ссылка "Зарегистрироваться"
    REGISTER_LINK = (By.LINK_TEXT, "Зарегистрироваться")

    # Ссылка "Восстановить пароль"
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Восстановить пароль")

    # Сообщение об ошибке
    ERROR_MESSAGE = (
        By.XPATH,
        "//p[contains(@class,'input__error') or contains(@class,'error')]",
    )
