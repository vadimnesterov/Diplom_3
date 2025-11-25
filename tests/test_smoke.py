# tests/test_smoke.py

import pytest
import allure

from pages.login_page import LoginPage
from pages.main_page import MainPage
from locators.main_page_locators import MainPageLocators


@allure.suite("Smoke")
class TestSmoke:

    def test_login_smoke(self, driver, api_user):
        """Минимальная проверка: юзер логинится и видит главную/хедер."""

        # Логин через UI
        login = LoginPage(driver)
        login.open_login()
        login.set_email(api_user["email"])
        login.set_password(api_user["password"])
        login.submit_login()

        main = MainPage(driver)

        # Проверяем, что мы вообще на домене Stellar Burgers
        assert "stellarburgers" in driver.current_url.lower()

        # Проверяем наличие кнопки "Лента заказов" в шапке
        assert main.is_element_visible(MainPageLocators.order_feed_button)
