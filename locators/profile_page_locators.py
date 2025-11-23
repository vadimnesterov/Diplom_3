from selenium.webdriver.common.by import By


class ProfilePageLocators:
    """Локаторы элементов на странице профиля."""

    # Заголовок "Профиль"
    PROFILE_HEADER = (By.XPATH, "//a[@href='/account/profile' and contains(@class,'tab_tab_type_current')]")

    # Кнопка "Выход"
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
