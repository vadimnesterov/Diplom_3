# pages/order_feed_page.py
# version: v1.7

import allure

from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators
from helpers.order_helper import normalize_order_number


class OrderFeedPage(BasePage):

    @allure.step("Проверить, что открыта страница ленты заказов")
    def is_order_feed_page_loaded(self, timeout: int = 10) -> bool:
        try:
            self.wait_for_url_contains("/feed", timeout=timeout)
            return True
        except Exception:
            current_url = self.execute_script("return window.location.href")
            return "/feed" in current_url

    def _parse_int_from(self, locator, timeout: int = 15) -> int:
        try:
            element = self.wait_for_visible(locator, timeout=timeout)
            text = element.text
        except Exception:
            try:
                script = """
                    try {
                        return document.evaluate(
                            arguments[0],
                            document,
                            null,
                            XPathResult.FIRST_ORDERED_NODE_TYPE,
                            null
                        ).singleNodeValue?.textContent;
                    } catch(e) {
                        return null;
                    }
                """
                text = self.execute_script(script, locator[1])
            except Exception:
                text = None

        if not text:
            return 0

        digits = "".join(ch for ch in text if ch.isdigit())
        return int(digits) if digits else 0

    @allure.step('Получить значение счётчика "Выполнено за всё время"')
    def get_total_orders_count(self) -> int:
        return self._parse_int_from(OrderFeedLocators.total_orders_counter)

    @allure.step('Получить значение счётчика "Выполнено за сегодня"')
    def get_today_orders_count(self) -> int:
        return self._parse_int_from(OrderFeedLocators.daily_orders_counter)

    @allure.step('Получить список номеров заказов в блоке "В работе" (нормализованный)')
    def get_orders_in_progress_normalized(self, timeout: int = 15) -> list:
        try:
            self.wait_for_visible(
                OrderFeedLocators.orders_in_progress_items,
                timeout=timeout,
            )

            script = """
                const result = [];
                const snapshot = document.evaluate(
                    arguments[0],
                    document,
                    null,
                    XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
                    null
                );
                for (let i = 0; i < snapshot.snapshotLength; i++) {
                    result.push(snapshot.snapshotItem(i).textContent || "");
                }
                return result;
            """
            texts = self.execute_script(
                script,
                OrderFeedLocators.orders_in_progress_items[1],
            ) or []

        except Exception:
            try:
                script = """
                    const uls = document.querySelectorAll("ul[class*='OrderFeed_orderList__']");
                    if (!uls || uls.length < 2) return [];
                    const ul = uls[1];
                    return Array.from(ul.querySelectorAll("li")).map(li => li.textContent || "");
                """
                texts = self.execute_script(script) or []
            except Exception:
                texts = []

        return [
            normalize_order_number(t)
            for t in texts
            if t and normalize_order_number(t)
        ]

    @allure.step('Ожидать появления заказа в блоке "В работе"')
    def wait_for_order_in_progress(
        self,
        normalized_order_number: str,
        timeout: int = 30,
    ) -> bool:
        if not normalized_order_number:
            return False

        def condition(_):
            orders = self.get_orders_in_progress_normalized(timeout=5)
            return normalized_order_number in orders

        try:
            self.wait_for_condition(condition, timeout=timeout)
            return True
        except Exception:
            return False

    @allure.step('Проверить, что номер заказа есть в блоке "В работе"')
    def is_order_in_progress_block(self, order_number: str, timeout: int = 15) -> bool:
        normalized = normalize_order_number(order_number)
        return self.wait_for_order_in_progress(normalized, timeout=timeout)

    @allure.step("Ожидать обновления счётчиков ленты заказов")
    def wait_for_counters_update(
        self,
        initial_total: int | None = None,
        initial_today: int | None = None,
        timeout: int = 30,
    ) -> bool:

        last_total = None
        last_today = None

        def condition(_):
            nonlocal last_total, last_today

            current_total = (
                self.get_total_orders_count() if initial_total is not None else None
            )
            current_today = (
                self.get_today_orders_count() if initial_today is not None else None
            )

            ok_total = True
            ok_today = True

            if initial_total is not None and current_total is not None:
                ok_total = current_total > initial_total
                last_total = current_total

            if initial_today is not None and current_today is not None:
                ok_today = current_today > initial_today
                last_today = current_today

            return ok_total and ok_today

        try:
            self.wait_for_condition(condition, timeout=timeout)
            return True
        except Exception:
            return False
