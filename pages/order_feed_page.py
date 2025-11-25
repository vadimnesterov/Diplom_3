from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators


class OrderFeedPage(BasePage):
    """Страница ленты заказов (/feed)."""

    def __init__(self, driver, timeout: int = 10):
        super().__init__(driver, timeout)

    # === базовая smoke-проверка ===

    def is_order_feed_page_loaded(self, timeout: int = 15) -> bool:
        """
        Smoke-проверка: страница ленты заказов открылась.
        Логика:
        1) ждём URL с '/feed';
        2) ждём заголовок и хотя бы один счётчик.
        """
        # 1. Ждём загрузку документа
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            pass

        url_ok = "/feed" in self.driver.current_url

        # 2. Ждём заголовок и счётчик
        try:
            self.wait_for_visible(OrderFeedLocators.title_orders_list, timeout=timeout)
            self.wait_for_visible(OrderFeedLocators.total_orders_counter, timeout=timeout)
            return True
        except TimeoutException:
            return url_ok

    # === вспомогательное ===

    def _parse_int_from_element(self, locator, timeout: int = 15) -> int:
        """Взять целое число из текста элемента счётчика."""
        el = self.wait_for_visible(locator, timeout=timeout)
        text = el.text.strip().replace(" ", "")
        return int(text) if text.isdigit() else 0

    def get_total_orders_count(self) -> int:
        """Значение счётчика «Выполнено за всё время»."""
        return self._parse_int_from_element(OrderFeedLocators.total_orders_counter)

    def get_today_orders_count(self) -> int:
        """Значение счётчика «Выполнено за сегодня»."""
        return self._parse_int_from_element(OrderFeedLocators.dayly_orders_counter)

    # === ожидание изменения счётчиков ===

    def wait_for_counters_update(
        self,
        initial_total: int | None,
        initial_today: int | None,
        timeout: int = 20,
    ) -> bool:
        """
        Подождать, пока хотя бы один из счётчиков изменится.
        Без time.sleep — используем WebDriverWait с кастомным условием.
        """
        def counters_changed(driver):
            try:
                total = self.get_total_orders_count()
                today = self.get_today_orders_count()
            except TimeoutException:
                return False

            total_changed = initial_total is not None and total > initial_total
            today_changed = initial_today is not None and today > initial_today
            return total_changed or today_changed

        try:
            WebDriverWait(self.driver, timeout).until(counters_changed)
            return True
        except TimeoutException:
            return False

    # === блок «В работе» ===

    def _normalize_order_number(self, text: str) -> str:
        """Оставить только цифры из номера заказа."""
        return "".join(ch for ch in text if ch.isdigit())

    def get_orders_in_progress_normalized(self) -> list[str]:
        """
        Получить список номеров заказов в разделе «В работе»
        (все номера нормализованы — только цифры).
        """
        elements = self.finds(OrderFeedLocators.number_order_in_job)
        result: list[str] = []
        for el in elements:
            raw = el.text.strip()
            if not raw:
                continue
            normalized = self._normalize_order_number(raw)
            if normalized:
                result.append(normalized)
        return result

    def wait_for_order_in_progress(self, normalized_order_number: str, timeout: int = 30) -> bool:
        """
        Подождать появления нужного номера заказа в разделе «В работе».
        """
        def order_present(driver):
            return normalized_order_number in self.get_orders_in_progress_normalized()

        try:
            WebDriverWait(self.driver, timeout).until(order_present)
            return True
        except TimeoutException:
            return False

    # Публичный метод нормализации, как в эталоне
    def normalize_order_number(self, order_number: str) -> str:
        return self._normalize_order_number(order_number)
