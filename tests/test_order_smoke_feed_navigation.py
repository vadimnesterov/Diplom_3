import pytest
import allure

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


@allure.suite("Debug / Smoke: навигация в ленту заказов")
@pytest.mark.xfail(reason="Временный отладочный тест, может быть нестабилен", strict=False)
class TestOrderFeedNavigationSmoke:

    @allure.title("Переход в ленту заказов из шапки после авторизации")
    @allure.description(
        "1. Авторизация пользователя\n"
        "2. Клик по разделу «Лента заказов»\n"
        "3. Проверка, что страница ленты заказов загрузилась"
    )
    def test_order_feed_page_is_loaded_after_login(self, driver, api_user):
        # Авторизация
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        login_page.submit_login()

        main_page = MainPage(driver)

        # Переход в ленту заказов
        main_page.click_order_feed()

        feed_page = OrderFeedPage(driver)

        # Проверяем, что лента заказов реально загрузилась
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась."
