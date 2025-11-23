from selenium.webdriver.common.by import By

from data.urls import MAIN_PAGE, PROFILE_PAGE
from pages.login_page import LoginPage
from pages.constructor_page import ConstructorPage
from pages.profile_page import ProfilePage


class TestHeaderNavigation:
    """Тесты навигации по хедеру."""

    def test_account_button_opens_login_for_unauthorized_user(self, driver):
        """
        Неавторизованный пользователь:
        по клику на 'Личный Кабинет' открывается страница логина.
        """
        page = ConstructorPage(driver)
        page.open_constructor()

        account_button = driver.find_element(By.XPATH, "//p[text()='Личный Кабинет']")
        account_button.click()

        assert "/login" in driver.current_url

    def test_account_button_opens_profile_for_authorized_user(self, driver, api_user):
        """
        Авторизованный пользователь:
        по клику на 'Личный Кабинет' открывается страница профиля.
        """
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        login_page.submit_login()

        # После логина оказываемся на конструкторе
        account_button = driver.find_element(By.XPATH, "//p[text()='Личный Кабинет']")
        account_button.click()

        profile_page = ProfilePage(driver)
        assert profile_page.is_profile_open()
        assert PROFILE_PAGE in driver.current_url

    def test_constructor_button_returns_to_main_page(self, driver, api_user):
        """
        Переход из личного кабинета обратно в конструктор по кнопке 'Конструктор'.
        """
        # Логинимся
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        login_page.submit_login()

        # Идём в профиль
        account_button = driver.find_element(By.XPATH, "//p[text()='Личный Кабинет']")
        account_button.click()

        # Возврат в конструктор
        constructor_button = driver.find_element(By.XPATH, "//p[text()='Конструктор']")
        constructor_button.click()

        assert driver.current_url.startswith(MAIN_PAGE)
