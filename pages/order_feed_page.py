from data.urls import FEED_PAGE
from locators.order_feed_locators import OrderFeedLocators
from .base_page import BasePage


class OrderFeedPage(BasePage):
    """Страница 'Лента заказов'."""

    def open_feed(self):
        """Открыть страницу ленты заказов."""
        self.open(FEED_PAGE)

    def is_feed_open(self) -> bool:
        """Проверить, что открыта лента заказов."""
        return self.is_visible(OrderFeedLocators.FEED_HEADER)

    def get_orders_list(self):
        """Получить список элементов заказов (WebElements)."""
        # find_elements через driver
        return self.driver.find_elements(*OrderFeedLocators.ORDERS_LIST)

    def get_total_orders_all_time(self) -> str:
        """Получить текст 'Выполнено за все время'."""
        return self.get_text(OrderFeedLocators.TOTAL_ORDERS_ALL_TIME)

    def get_total_orders_today(self) -> str:
        """Получить текст 'Выполнено за сегодня'."""
        return self.get_text(OrderFeedLocators.TOTAL_ORDERS_TODAY)
