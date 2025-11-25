# tests/test_main_page_functionality.py

import pytest

from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from data.urls import URLS


class TestMainPageFunctionality:
    """Проверки основной функциональности главной страницы."""

    def test_go_to_constructor_from_header(self, driver):
        """Переход по клику на «Конструктор»."""
        main = MainPage(driver)
        main.open()  # открываем главную

        # Уходим в ленту заказов, чтобы точно не быть на /
        main.click_order_feed()
        assert URLS.url_feed in driver.current_url

        # Возвращаемся кликом по «Конструктор»
        main.click_constructor()
        assert URLS.url_feed not in driver.current_url

    def test_go_to_order_feed_from_header(self, driver):
        """Переход по клику на «Лента заказов»."""
        main = MainPage(driver)
        main.open()

        main.click_order_feed()

        feed = OrderFeedPage(driver)
        assert feed.is_order_feed_page_loaded()

    def test_ingredient_modal_opens_on_click(self, driver):
        """Если кликнуть на ингредиент, появляется модальное окно с деталями."""
        main = MainPage(driver)
        main.open()

        main.click_ingredient()
        assert main.is_ingredient_modal_visible()

    def test_ingredient_modal_closes_on_cross(self, driver):
        """Модальное окно закрывается по крестику/оверлею."""
        main = MainPage(driver)
        main.open()

        main.click_ingredient()
        assert main.is_ingredient_modal_visible()

        main.close_ingredient_modal()
        assert main.is_ingredient_modal_closed()

    def test_ingredient_counter_increases_after_drag(self, driver):
        """При добавлении ингредиента в заказ счётчик этого ингредиента увеличивается."""
        main = MainPage(driver)
        main.open()

        before = main.get_ingredient_counter()
        main.drag_ingredient_to_constructor()
        after = main.get_ingredient_counter()

        assert after > before
