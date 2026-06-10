import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators
from helpers.order_helper import normalize_order_number


class OrderFeedPage(BasePage):

    @allure.step("Check that the order feed page is open")
    def is_order_feed_page_loaded(self, timeout: int = 10) -> bool:
        try:
            self.wait_for_url_contains("/feed", timeout=timeout)
            return True
        except TimeoutException:
            return False

    def _parse_int_from(self, locator, timeout: int = 15) -> int:
        """
        Return the integer value from the element identified by locator.
        Returns 0 if the element text contains no digits.
        Raises TimeoutException if the element is not visible within timeout.
        """
        element = self.wait_for_visible(locator, timeout=timeout)
        text = element.text.strip()
        digits = "".join(ch for ch in text if ch.isdigit())
        return int(digits) if digits else 0

    @allure.step('Get the "Completed all time" counter value')
    def get_total_orders_count(self) -> int:
        return self._parse_int_from(OrderFeedLocators.total_orders_counter)

    @allure.step('Get the "Completed today" counter value')
    def get_today_orders_count(self) -> int:
        return self._parse_int_from(OrderFeedLocators.daily_orders_counter)

    def _collect_in_progress_normalized(self, timeout: int = 15) -> list:
        """
        Internal helper (no Allure step): wait for at least one order to appear
        in the In Progress block, then return all order numbers as normalized strings.
        Returns an empty list if no orders are present within timeout.
        Called by the polling loop in wait_for_order_in_progress to avoid Allure
        step spam on every poll tick.
        """
        try:
            self.wait_for_visible(
                OrderFeedLocators.orders_in_progress_items,
                timeout=timeout,
            )
        except TimeoutException:
            return []

        elements = self.find_elements(OrderFeedLocators.orders_in_progress_items)

        result = []
        for el in elements:
            try:
                text = el.text
            except StaleElementReferenceException:
                continue
            if text and (n := normalize_order_number(text)):
                result.append(n)
        return result

    @allure.step('Get the list of order numbers in the "In Progress" block (normalised)')
    def get_orders_in_progress_normalized(self, timeout: int = 15) -> list:
        """
        Return all order numbers currently in the In Progress block as normalized strings.
        Decorated with @allure.step for direct single-read use from tests or page methods.
        """
        return self._collect_in_progress_normalized(timeout)

    @allure.step('Wait for the order to appear in the "In Progress" block')
    def wait_for_order_in_progress(
        self,
        normalized_order_number: str,
        timeout: int = 30,
    ) -> bool:
        if not normalized_order_number:
            return False

        def condition(_):
            orders = self._collect_in_progress_normalized(timeout=5)
            return normalized_order_number in orders

        try:
            self.wait_for_condition(condition, timeout=timeout)
            return True
        except TimeoutException:
            return False

    @allure.step('Check that the order number is present in the "In Progress" block')
    def is_order_in_progress_block(self, order_number: str, timeout: int = 15) -> bool:
        normalized = normalize_order_number(order_number)
        return self.wait_for_order_in_progress(normalized, timeout=timeout)

    @allure.step("Wait for the order feed counters to update")
    def wait_for_counters_update(
        self,
        initial_total: int | None = None,
        initial_today: int | None = None,
        timeout: int = 30,
    ) -> bool:

        def condition(_):
            try:
                current_total = (
                    self.get_total_orders_count() if initial_total is not None else None
                )
                current_today = (
                    self.get_today_orders_count() if initial_today is not None else None
                )
            except TimeoutException:
                # Counter element temporarily absent (e.g. page still loading after
                # navigation). Treat as "not ready yet" so the outer wait retries
                # instead of propagating the exception and aborting the poll early.
                return False

            ok_total = True
            ok_today = True

            if initial_total is not None and current_total is not None:
                ok_total = current_total > initial_total

            if initial_today is not None and current_today is not None:
                ok_today = current_today > initial_today

            return ok_total and ok_today

        try:
            self.wait_for_condition(condition, timeout=timeout)
            return True
        except Exception:
            return False
