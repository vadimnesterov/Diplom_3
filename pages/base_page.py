# pages/base_page.py
# version: v1.7

import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    # ================= URL =================

    @allure.step("Открыть URL")
    def open(self, url: str):
        self.driver.get(url)

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.driver.current_url

    @allure.step("Проверить, что URL содержит подстроку")
    def is_url_contains(self, substring: str) -> bool:
        return substring in self.driver.current_url

    # ================= WAIT CORE =================

    def _get_wait(self, timeout: int | None = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.timeout)

    @allure.step("Ожидание загрузки страницы")
    def wait_for_page_load(self, timeout: int | None = None):
        self._get_wait(timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    @allure.step("Ожидание отображения элемента")
    def wait_for_visible(self, locator, timeout: int | None = None):
        return self._get_wait(timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Ожидание кликабельности элемента")
    def wait_for_clickable(self, locator, timeout: int | None = None):
        return self._get_wait(timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Ожидание появления текста")
    def wait_for_text(self, locator, text: str, timeout: int | None = None):
        return self._get_wait(timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    @allure.step("Ожидание части URL")
    def wait_for_url_contains(self, substring: str, timeout: int | None = None):
        return self._get_wait(timeout).until(
            EC.url_contains(substring)
        )

    @allure.step("Ожидание произвольного условия")
    def wait_for_condition(self, condition, timeout: int | None = None):
        return self._get_wait(timeout).until(condition)

    @allure.step("Ожидание исчезновения элемента")
    def wait_for_invisibility(self, locator, timeout: int | None = None) -> bool:
        try:
            result = self._get_wait(timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return bool(result)
        except TimeoutException:
            return False

    # ================= CHECKERS =================

    @allure.step("Проверка, что элемент видим")
    def is_element_visible(self, locator, timeout: int | None = None) -> bool:
        try:
            self.wait_for_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    @allure.step("Проверка, что элемент НЕ видим")
    def is_element_not_visible(self, locator, timeout: int | None = None) -> bool:
        return self.wait_for_invisibility(locator, timeout)

    # ================= ELEMENT ACCESS =================

    @allure.step("Поиск элемента")
    def find_element(self, locator, timeout: int | None = None):
        return self.wait_for_visible(locator, timeout)

    @allure.step("Ожидание элемента (алиас совместимости)")
    def wait_element_visible(self, locator, timeout: int | None = None):
        return self.wait_for_visible(locator, timeout)

    # ================= ACTIONS =================

    @allure.step("Клик по элементу (с JS fallback)")
    def click(self, locator, timeout: int | None = None):
        try:
            element = self.wait_for_clickable(locator, timeout)
            element.click()
        except Exception:
            element = self.wait_for_visible(locator, timeout)
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Клик по кнопке")
    def click_button(self, locator, timeout: int | None = None):
        self.click(locator, timeout)

    @allure.step("Ввод текста")
    def fill(self, locator, value: str, timeout: int | None = None):
        element = self.wait_for_visible(locator, timeout)
        element.clear()
        element.send_keys(value)
        return element

    @allure.step("Ввод текста (backward compatibility для старых PageObject)")
    def type(self, locator, value: str, timeout: int | None = None):
        return self.fill(locator, value, timeout)

    @allure.step("Получение текста элемента")
    def get_text(self, locator, timeout: int | None = None) -> str:
        element = self.wait_for_visible(locator, timeout)
        return element.text

    # ================= JS =================

    @allure.step("Выполнение JavaScript")
    def execute_script(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    # ================= MODALS =================

    @allure.step("Принудительное закрытие всех модальных окон")
    def force_close_modals(self):
        try:
            self.driver.execute_script(
                """
                var escEvent = new KeyboardEvent('keydown', {
                    key: 'Escape',
                    code: 'Escape',
                    keyCode: 27,
                    which: 27
                });
                document.dispatchEvent(escEvent);

                var overlays = document.querySelectorAll(
                    '[class*="overlay"], [class*="modal"]'
                );
                overlays.forEach(function(el) {
                    if (el.style.display !== 'none') {
                        el.click();
                    }
                });
                """
            )
        except Exception:
            pass

    # ================= DRAG & DROP (SAFE JS) =================

    @allure.step("Drag and Drop элемента (через JS, стабильно для Firefox)")
    def drag_and_drop(self, source_locator, target_locator):
        source = self.wait_for_visible(source_locator)
        target = self.wait_for_visible(target_locator)

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
                element.dispatchEvent(event);
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
