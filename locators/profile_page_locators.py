from selenium.webdriver.common.by import By


class ProfilePageLocators:
    # Активная вкладка «Профиль» в аккаунте
    PROFILE_HEADER = (By.XPATH, "//a[contains(@class,'Account_link_active') and text()='Профиль']")

    NAME_INPUT = (By.XPATH, "//label[text()='Имя']/following-sibling::input")
    EMAIL_INPUT = (By.XPATH, "//label[text()='Логин']/following-sibling::input")

    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
