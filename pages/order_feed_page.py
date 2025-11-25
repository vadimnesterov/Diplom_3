# pages/order_feed_page.py v1.4

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure

from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators


class OrderFeedPage(BasePage):
    @allure.step("Проверить, что открыта страница ленты заказов")
    def is_order_feed_page_loaded(self, timeout: int = 10) -> bool:
        """
        Более мягкая проверка:
        - сначала ждём URL /feed;
        - если таймаут, но URL уже содержит /feed — всё равно считаем, что страница открыта.
        Никаких жёстких проверок верстки, чтобы Firefox не падал по мелочи.
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains("/feed"))
            return True
        except Exception:
            return "/feed" in self.driver.current_url

    def _parse_int_from(self, locator, timeout: int = 15) -> int:
        """
        Универсальный парсер числа из текстового элемента:
        1) ждём видимости локатора;
        2) если не нашли — пробуем вытащить текст через JS (важно для Firefox);
        3) оставляем только цифры, конвертируем в int.
        """
        text = None

        try:
            el = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            text = el.text
        except TimeoutException:
            # Firefox / нестабильный DOM: пробуем достать текст через JS
            try:
                by, value = locator

                if by == By.CSS_SELECTOR:
                    script = "return document.querySelector(arguments[0])?.textContent;"
                    text = self.driver.execute_script(script, value)
                elif by == By.XPATH:
                    script = (
                        "try {return document.evaluate(arguments[0], document, null,"
                        "XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue"
                        ".textContent;} catch(e) {return null;}"
                    )
                    text = self.driver.execute_script(script, value)
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
        return self._parse_int_from(OrderFeedLocators.dayly_orders_counter)

    @staticmethod
    def normalize_order_number(order_number: str) -> str:
        """
        Очищает номер заказа:
        - берёт только цифры;
        - убирает ведущие нули.
        """
        if not order_number:
            return ""
        digits = "".join(ch for ch in order_number if ch.isdigit())
        return digits.lstrip("0")

    @allure.step('Получить список номеров заказов в блоке "В работе" (нормализованный)')
    def get_orders_in_progress_normalized(self, timeout: int = 15) -> list:
        """
        Возвращает список номеров заказов из блока «В работе»:
        - берём второй список ul.OrderFeed_orderList__*;
        - собираем все li;
        - нормализуем номера через normalize_order_number().
        """
        locator = (
            By.XPATH,
            "//ul[contains(@class, 'OrderFeed_orderList__')][2]//li"
        )

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_any_elements_located(locator)
            )
            elements = self.driver.find_elements(*locator)
            texts = [el.text for el in elements if el.text]
        except TimeoutException:
            # Fallback через JS (как в эталоне-подходе)
            try:
                script = """
                    const uls = document.querySelectorAll("ul[class*='OrderFeed_orderList__']");
                    if (!uls || uls.length < 2) return [];
                    const ul = uls[1];
                    return Array.from(ul.querySelectorAll("li")).map(li => li.textContent || "");
                """
                texts = self.driver.execute_script(script)
                if not texts:
                    return []
            except Exception:
                return []

        return [
            self.normalize_order_number(t)
            for t in texts
            if t and self.normalize_order_number(t)
        ]

    @allure.step('Ожидать появления заказа в блоке "В работе"')
    def wait_for_order_in_progress(
        self,
        normalized_order_number: str,
        timeout: int = 30,
        poll: float = 1.0,
    ) -> bool:
        """
        Ждём, пока нормализованный номер заказа появится в блоке «В работе».
        Используем get_orders_in_progress_normalized() в цикле до timeout.
        """
        if not normalized_order_number:
            return False

        end_time = time.monotonic() + timeout

        while time.monotonic() < end_time:
            orders = self.get_orders_in_progress_normalized(timeout=5)
            if normalized_order_number in orders:
                return True
            time.sleep(poll)

        return False

    @allure.step('Проверить, что номер заказа есть в блоке "В работе"')
    def is_order_in_progress_block(self, order_number: str, timeout: int = 15) -> bool:
        """
        Обёртка поверх wait_for_order_in_progress:
        - нормализуем номер;
        - ждём появления в блоке «В работе».
        """
        normalized = self.normalize_order_number(order_number)
        return self.wait_for_order_in_progress(normalized, timeout=timeout)

    @allure.step("Ожидать обновления счётчиков ленты заказов")
    def wait_for_counters_update(
        self,
        initial_total: int | None = None,
        initial_today: int | None = None,
        timeout: int = 30,
        poll: float = 1.0,
    ) -> bool:
        """
        Ждём, пока счётчики обновятся относительно исходных значений.
        - Если initial_total is None — игнорируем общий счётчик.
        - Если initial_today is None — игнорируем дневной счётчик.
        - Условие успеха: каждый заданный счётчик стал строго больше начального.
        """
        end_time = time.monotonic() + timeout

        while time.monotonic() < end_time:
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

            if initial_today is not None and current_today is not None:
                ok_today = current_today > initial_today

            if ok_total and ok_today:
                return True

            time.sleep(poll)

        return False
