# pages/base_page.py  v1.2

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure


class BasePage:
    """Базовый Page Object. Содержит универсальные методы ожиданий, кликов и JS-утилит."""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    # ===== БАЗОВЫЕ ОЖИДАНИЯ =====

    def _get_wait(self, timeout: int | None = None) -> WebDriverWait:
        """Получить WebDriverWait с заданным или дефолтным таймаутом."""
        return WebDriverWait(self.driver, timeout or self.timeout)

    @allure.step("Ожидание кликабельности элемента")
    def wait_element_clickable(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Ожидание видимости элемента")
    def wait_element_visible(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    # ===== ПОИСК ЭЛЕМЕНТОВ =====

    @allure.step("Поиск элемента без ожидания")
    def find_element(self, locator):
        return self.driver.find_element(*locator)

    @allure.step("Поиск списка элементов без ожидания")
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step("Поиск элемента с ожиданием видимости")
    def find_element_with_wait(self, locator, timeout: int = 10):
        return self.wait_element_visible(locator, timeout)

    # ===== КЛИКИ И ВВОД =====

    @allure.step("Клик по элементу")
    def click_button(self, locator, timeout: int = 10):
        """
        Универсальный клик:
        1) ожидание кликабельности
        2) обычный клик
        3) при ошибке — ожидание видимости + JS-клик
        """
        try:
            element = self.wait_element_clickable(locator, timeout)
            element.click()
        except Exception:
            element = self.wait_element_visible(locator, timeout)
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Клик по элементу (совместимый метод)")
    def click(self, locator, timeout: int | None = None):
        """Обёртка совместимости для старых вызовов click()."""
        return self.click_button(locator, timeout or self.timeout)

    @allure.step("Ввод текста в поле")
    def type(self, locator, text: str, timeout: int | None = None):
        element = self.wait_element_visible(locator, timeout or self.timeout)
        element.clear()
        element.send_keys(text)
        return element

    # ===== ПРОВЕРКИ ВИДИМОСТИ =====

    @allure.step("Проверка видимости элемента")
    def is_element_visible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Проверка невидимости элемента")
    def is_element_not_visible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ===== МОДАЛЬНЫЕ ОКНА =====

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

    # ===== DRAG & DROP =====

    @allure.step("Перетаскивание элемента (через JS drag&drop)")
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

    # ===== ЗАГРУЗКА СТРАНИЦ И JS =====

    @allure.step("Открытие URL")
    def open(self, url: str):
        self.driver.get(url)

    # URL

    @allure.step("Получить текущий URL страницы")
    def get_current_url(self) -> str:
        return self.driver.current_url

    @allure.step("Проверить, что текущий URL содержит: {substring}")
    def is_url_contains(self, substring: str) -> bool:
        return substring in self.driver.current_url

    @allure.step("Ожидание полной загрузки страницы")
    def wait_for_page_load(self, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    @allure.step("Выполнение JavaScript-кода")
    def execute_script(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    # ===== УНИВЕРСАЛЬНЫЕ ОБЁРТКИ =====

    def wait_for_visible(self, locator, timeout: int | None = None):
        return self.wait_element_visible(locator, timeout or self.timeout)

    def wait_for_clickable(self, locator, timeout: int | None = None):
        return self.wait_element_clickable(locator, timeout or self.timeout)

    def wait_for_text(self, locator, text: str, timeout: int | None = None) -> bool:
        wait = self._get_wait(timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_url_contains(self, substring: str, timeout: int | None = None) -> bool:
        wait = self._get_wait(timeout)
        return wait.until(EC.url_contains(substring))

    def wait_for_condition(self, condition_fn, timeout: int | None = None):
        wait = self._get_wait(timeout)
        return wait.until(condition_fn)

    # ===== ВСПОМОГАТЕЛЬНЫЕ УТИЛИТЫ =====

    @allure.step("Прокрутить страницу до элемента")
    def scroll_into_view(self, locator, timeout: int | None = None):
        element = self.wait_for_visible(locator, timeout)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element,
        )
        return element

    @allure.step("Получить текст элемента")
    def get_text(self, locator, timeout: int | None = None) -> str:
        element = self.wait_for_visible(locator, timeout)
        return element.text
