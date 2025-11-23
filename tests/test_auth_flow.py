from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.constructor_page import ConstructorPage
from locators.constructor_page_locators import ConstructorPageLocators


class TestAuthFlow:
    """Тесты авторизации и регистрации пользователя."""

    def test_login_existing_user_success(self, driver, api_user):
        """
        Позитивный сценарий:
        существующий пользователь может войти в систему через форму логина.
        """
        login_page = LoginPage(driver)
        login_page.open_login()

        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        login_page.submit_login()

        # После успешного логина ожидаем, что открылся конструктор
        constructor_page = ConstructorPage(driver)
        assert constructor_page.is_visible(ConstructorPageLocators.ORDER_BUTTON)

    def test_register_with_short_password_shows_error(self, driver):
        """
        Негативный сценарий:
        при регистрации с коротким паролем отображается сообщение об ошибке.
        """
        register_page = RegisterPage(driver)
        register_page.open_register()

        # Данные не завязаны на существующего пользователя
        register_page.set_name("TestUser")
        register_page.set_email("shortpass@example.com")
        register_page.set_password("123")  # заведомо короткий пароль
        register_page.submit_register()

        error_text = register_page.get_error_message()
        assert "Некорректный пароль" in error_text

    def test_login_page_has_link_to_register(self, driver):
        """
        Проверяем, что со страницы логина можно перейти на страницу регистрации.
        """
        login_page = LoginPage(driver)
        login_page.open_login()

        login_page.go_to_register()

        # Проверяем, что в URL есть /register
        assert "/register" in driver.current_url
