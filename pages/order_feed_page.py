# pages/order_feed_page.py

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators


class OrderFeedPage(BasePage):
    """Страница ленты заказов (/feed)."""

    def __init__(self, driver, timeout: int = 10):
        super().__init__(driver, timeout)

    # ==========================================================
    #  1. ПРОВЕРКА ЗАГРУЗКИ СТРАНИЦЫ (/feed)
    # ==========================================================

    def is_order_feed_page_loaded(self, timeout: int = 15) -> bool:
        """
        Страница считается загруженной, если:
        - URL содержит '/feed'
        - виден заголовок 'Лента заказов'
        - виден хотя бы один счётчик
        """
        # 1) дождаться document.readyState
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            pass

        url_ok = "/feed" in self.driver.current_url

        # 2) ждём главный UI: заголовок + счётчик
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(OrderFeedLocators.title_orders_list)
            )
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(OrderFeedLocators.total_orders_counter)
            )
            return True
        except TimeoutException:
            return url_ok

    # ==========================================================
    #  2. ЧТЕНИЕ СЧЁТЧИКОВ
    # ==========================================================

    def _parse_int_from(self, locator, timeout: int = 15) -> int:
        """Достаёт число из текста элемента."""
        el = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        txt = el.text.strip().replace(" ", "")
        return int(txt) if txt.isdigit() else 0

    def get_total_orders_count(self) -> int:
        return self._parse_int_from(OrderFeedLocators.total_orders_counter)

    def get_today_orders_count(self) -> int:
        return self._parse_int_from(OrderFeedLocators.dayly_orders_counter)

    # ==========================================================
    #  3. ОЖИДАНИЕ УВЕЛИЧЕНИЯ СЧЁТЧИКОВ
    # ==========================================================

    def wait_for_counters_update(self, initial_total, initial_today, timeout: int = 25) -> bool:
        """
        Ждём пока хотя бы один счётчик увеличится.
        """
        def changed(_):
            try:
                total = self.get_total_orders_count()
                today = self.get_today_orders_count()
            except TimeoutException:
                return False

            return (
                (initial_total is not None and total > initial_total) or
                (initial_today is not None and today > initial_today)
            )

        try:
            WebDriverWait(self.driver, timeout).until(changed)
            return True
        except TimeoutException:
            return False

    # ==========================================================
    #  4. РАБОТА С БЛОКОМ "В РАБОТЕ"
    # ==========================================================

    def _normalize(self, text: str) -> str:
        return "".join(ch for ch in text if ch.isdigit())

    def get_orders_in_progress_normalized(self) -> list[str]:
        """Список номеров в блоке 'В работе' (нормализованный)."""
        items = self.driver.find_elements(*OrderFeedLocators.number_order_in_job)
        result = []
        for el in items:
            raw = el.text.strip()
            if not raw:
                continue
            norm = self._normalize(raw)
            if norm:
                result.append(norm)
        return result

    def wait_for_order_in_progress(self, normalized_order_number: str, timeout: int = 30) -> bool:
        """
        Ждём появления номера заказа в блоке 'В работе'.
        """
        def present(_):
            return normalized_order_number in self.get_orders_in_progress_normalized()

        try:
            WebDriverWait(self.driver, timeout).until(present)
            return True
        except TimeoutException:
            return False

    # Публичная нормализация номера заказа (для тестов)
    def normalize_order_number(self, order_number: str) -> str:
        return self._normalize(order_number)
