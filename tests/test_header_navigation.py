from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from pages.constructor_page import ConstructorPage
from data.urls import MAIN_PAGE, PROFILE_PAGE


class TestHeaderNavigation:
    """Тесты навигации по хедеру."""

    # ----------------------------
    # 1. Неавторизованный пользователь
    # ----------------------------

    def test_account_button_opens_login_for_unauthorized_user(self, driver):
        """
        Неавторизованный пользователь:
        по клику на 'Личный Кабинет' должна открываться страница логина.
        """
        base = BasePage(driver)
        constructor_page = ConstructorPage(driver)

        constructor_page.open_constructor()

        # Клик через BasePage (обходит overlay)
        base.click((By.XPATH, "//p[text()='Личный Кабинет']"))

        assert "/login" in driver.current_url

    # ----------------------------
    # 2. Авторизованный пользователь
    # ----------------------------

    def test_account_button_opens_profile_for_authorized_user(self, driver, api_user):
        """
        Авторизованный пользователь:
        по клику на 'Личный Кабинет' открывается страница профиля.
        """

        login_page = LoginPage(driver)
        base = BasePage(driver)

        # Авторизация
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        login_page.submit_login()

        # Клик в хедере
        base.click((By.XPATH, "//p[text()='Личный Кабинет']"))

        profile_page = ProfilePage(driver)
        assert profile_page.is_profile_open()
        assert PROFILE_PAGE in driver.current_url

    # ----------------------------
    # 3. Возврат в конструктор
    # ----------------------------

    def test_constructor_button_returns_to_main_page(self, driver, api_user):
        """
        Авторизованный пользователь:
        переход из личного кабинета обратно в конструктор по кнопке 'Конструктор'.
        """
        login_page = LoginPage(driver)
        base = BasePage(driver)

        # Авторизация
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        login_page.submit_login()

        # Переход в профиль
        base.click((By.XPATH, "//p[text()='Личный Кабинет']"))

        # Возврат в конструктор
        base.click((By.XPATH, "//p[text()='Конструктор']"))

        assert driver.current_url.startswith(MAIN_PAGE)
