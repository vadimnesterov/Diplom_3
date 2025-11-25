# pages/base_page.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure


class BasePage:
    """Базовый класс для всех PageObject."""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    # ===== базовые утилиты ожиданий =====

    def _get_wait(self, timeout: int | None = None) -> WebDriverWait:
        """Вернуть WebDriverWait с нужным таймаутом."""
        return WebDriverWait(self.driver, timeout or self.timeout)

    @allure.step("Ждать кликабельности элемента")
    def wait_element_clickable(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Ждать видимости элемента")
    def wait_element_visible(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    # ===== поиск элементов =====

    @allure.step("Найти элемент без ожидания")
    def find_element(self, locator):
        return self.driver.find_element(*locator)

    @allure.step("Найти несколько элементов без ожидания")
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step("Найти элемент с ожиданием")
    def find_element_with_wait(self, locator, timeout: int = 10):
        return self.wait_element_visible(locator, timeout)

    # ===== клики и ввод =====

    @allure.step("Кликнуть по кнопке")
    def click_button(self, locator, timeout: int = 10):
        """
        Стандартный клик:
        1) ждём кликабельности
        2) кликаем
        3) если не получилось — дожидаемся видимости и жмём JS-кликом
        """
        try:
            element = self.wait_element_clickable(locator, timeout)
            element.click()
        except Exception:
            element = self.wait_element_visible(locator, timeout)
            self.driver.execute_script("arguments[0].click();", element)

    def click(self, locator, timeout: int | None = None):
        """Совместимость со старым интерфейсом: click()."""
        return self.click_button(locator, timeout or self.timeout)

    @allure.step("Ввести текст в поле")
    def type(self, locator, text: str, timeout: int | None = None):
        """
        Ввести текст в поле:
        1) дождаться видимости
        2) очистить
        3) ввести текст
        """
        element = self.wait_element_visible(locator, timeout or self.timeout)
        element.clear()
        element.send_keys(text)
        return element

    # ===== проверки видимости =====

    @allure.step("Проверить видимость элемента")
    def is_element_visible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Проверить, что элемент невидим")
    def is_element_not_visible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ===== модальные окна =====

    @allure.step("Принудительно закрыть все модальные окна")
    def force_close_modals(self):
        try:
            self.driver.execute_script(
                """
                // Нажать ESC
                var escEvent = new KeyboardEvent('keydown', {
                    key: 'Escape',
                    code: 'Escape',
                    keyCode: 27,
                    which: 27
                });
                document.dispatchEvent(escEvent);

                // Клик по всем overlay/modal
                var overlays = document.querySelectorAll('[class*="overlay"], [class*="modal"]');
                overlays.forEach(function(overlay) {
                    if (overlay.style.display !== 'none') {
                        overlay.click();
                    }
                });
                """
            )
        except Exception:
            pass

    # ===== drag & drop =====

    @allure.step("Перетащить элемент (JS drag&drop)")
    def drag_and_drop(self, source_locator, target_locator):
        source = self.find_element_with_wait(source_locator)
        target = self.find_element_with_wait(target_locator)

        self.driver.execute_script(
            """
            function createEvent(typeOfEvent) {
                var event = document.createEvent("CustomEvent");
                event.initCustomEvent(typeOfEvent, true, true, null);
                event.dataTransfer = {
                    data: {},
                    setData: function (key, value) {
                        this.data[key] = value;
                    },
                    getData: function (key) {
                        return this.data[key];
                    }
                };
                return event;
            }

            function dispatchEvent(element, event, transferData) {
                if (transferData !== undefined) {
                    event.dataTransfer = transferData;
                }
                if (element.dispatchEvent) {
                    element.dispatchEvent(event);
                } else if (element.fireEvent) {
                    element.fireEvent("on" + event.type, event);
                }
            }

            var source = arguments[0];
            var target = arguments[1];

            var dragStartEvent = createEvent('dragstart');
            dispatchEvent(source, dragStartEvent);

            var dragEnterEvent = createEvent('dragenter');
            dispatchEvent(target, dragEnterEvent, dragStartEvent.dataTransfer);

            var dragOverEvent = createEvent('dragover');
            dispatchEvent(target, dragOverEvent, dragStartEvent.dataTransfer);

            var dropEvent = createEvent('drop');
            dispatchEvent(target, dropEvent, dragStartEvent.dataTransfer);

            var dragEndEvent = createEvent('dragend');
            dispatchEvent(source, dragEndEvent, dragStartEvent.dataTransfer);
            """,
            source,
            target,
        )

    # ===== загрузка страницы / JS =====

    @allure.step("Открыть URL")
    def open(self, url: str):
        self.driver.get(url)

    @allure.step("Ждать загрузки страницы")
    def wait_for_page_load(self, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    @allure.step("Выполнить JavaScript")
    def execute_script(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    # ===== универсальные ожидания (обёртки под старые вызовы) =====

    def wait_for_visible(self, locator, timeout: int | None = None):
        """Совместимость: старое имя метода, используется в страницах (OrderFeedPage и др.)."""
        return self.wait_element_visible(locator, timeout or self.timeout)

    def wait_for_clickable(self, locator, timeout: int | None = None):
        """Совместимость: старое имя метода."""
        return self.wait_element_clickable(locator, timeout or self.timeout)

    def wait_for_text(self, locator, text: str, timeout: int | None = None) -> bool:
        wait = self._get_wait(timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_url_contains(self, substring: str, timeout: int | None = None) -> bool:
        wait = self._get_wait(timeout)
        return wait.until(EC.url_contains(substring))

    def wait_for_condition(self, condition_fn, timeout: int | None = None):
        """Универсальное ожидание произвольного предиката."""
        wait = self._get_wait(timeout)
        return wait.until(condition_fn)

    # ===== утилиты =====

    def scroll_into_view(self, locator, timeout: int | None = None):
        element = self.wait_for_visible(locator, timeout)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element,
        )
        return element

    def get_text(self, locator, timeout: int | None = None) -> str:
        element = self.wait_for_visible(locator, timeout)
        return element.text
