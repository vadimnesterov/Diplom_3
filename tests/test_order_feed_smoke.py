# tests/test_order_feed_smoke.py

import pytest

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


class TestOrderFeedSmoke:

    def test_order_feed_page_opens(self, driver, api_user):
        """Минимальная проверка: страница ленты заказов открывается."""

        # 1. Логиним пользователя
        login = LoginPage(driver)
        login.open_login()
        login.set_email(api_user["email"])
        login.set_password(api_user["password"])
        login.submit_login()

        # 2. Переходим в ленту заказов
        main = MainPage(driver)
        main.click_order_feed()

        # 3. Проверяем видимость ключевого элемента OrderFeed
        feed = OrderFeedPage(driver)
        assert feed.is_order_feed_page_loaded(), "Страница ленты заказов НЕ загрузилась!"
