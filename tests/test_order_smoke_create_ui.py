import pytest
import allure

from pages.login_page import LoginPage
from pages.main_page import MainPage


@allure.suite("Debug / Smoke: создание заказа через UI")
@pytest.mark.xfail(reason="Временный отладочный тест, может быть нестабилен", strict=False)
class TestCreateOrderUISmoke:

    @allure.title("Создание заказа через UI с главной страницы (конструктор)")
    @allure.description(
        "1. Авторизация пользователя\n"
        "2. Переход на конструктор (если нужно)\n"
        "3. Создание заказа через UI\n"
        "4. Проверка, что номер заказа получен и он не 9999"
    )
    def test_create_order_ui_from_constructor(self, driver, api_user):
        # Авторизация
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        login_page.submit_login()

        main_page = MainPage(driver)

        # На всякий случай переключаемся на конструктор,
        # чтобы гарантированно НЕ быть на /feed
        main_page.click_constructor()

        # Создание заказа через UI
        order_number = main_page.create_order_ui()

        # Проверяем, что номер заказа получен
        assert order_number is not None, "Не удалось получить номер заказа."
        assert order_number != "9999", "Получен временный номер заказа 9999."
