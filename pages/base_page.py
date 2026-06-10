import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class BasePage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    # ================= URL =================

    @allure.step("Open URL: {url}")
    def open(self, url: str):
        self.driver.get(url)

    @allure.step("Get current URL")
    def get_current_url(self) -> str:
        return self.driver.current_url

    @allure.step("Check URL contains substring: {substring}")
    def is_url_contains(self, substring: str) -> bool:
        return substring in self.driver.current_url

    # ================= WAIT CORE =================

    def _get_wait(self, timeout: int | None = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.timeout)

    @allure.step("Wait for page to fully load")
    def wait_for_page_load(self, timeout: int | None = None):
        self._get_wait(timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    @allure.step("Wait for element to be visible: {locator}")
    def wait_for_visible(self, locator, timeout: int | None = None):
        return self._get_wait(timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Wait for element to be clickable: {locator}")
    def wait_for_clickable(self, locator, timeout: int | None = None):
        return self._get_wait(timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Wait for text in element: '{text}'")
    def wait_for_text(self, locator, text: str, timeout: int | None = None):
        return self._get_wait(timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    @allure.step("Wait for URL to contain: '{substring}'")
    def wait_for_url_contains(self, substring: str, timeout: int | None = None):
        return self._get_wait(timeout).until(
            EC.url_contains(substring)
        )

    @allure.step("Wait for custom condition")
    def wait_for_condition(self, condition, timeout: int | None = None):
        return self._get_wait(timeout).until(condition)

    @allure.step("Wait for element to disappear: {locator}")
    def wait_for_invisibility(self, locator, timeout: int | None = None) -> bool:
        try:
            result = self._get_wait(timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return bool(result)
        except TimeoutException:
            return False

    # ================= CHECKERS =================

    @allure.step("Check element is visible: {locator}")
    def is_element_visible(self, locator, timeout: int | None = None) -> bool:
        try:
            self.wait_for_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    @allure.step("Check element is NOT visible: {locator}")
    def is_element_not_visible(self, locator, timeout: int | None = None) -> bool:
        return self.wait_for_invisibility(locator, timeout)

    # ================= ELEMENT ACCESS =================

    @allure.step("Find element: {locator}")
    def find_element(self, locator, timeout: int | None = None):
        return self.wait_for_visible(locator, timeout)

    @allure.step("Find all elements matching locator")
    def find_elements(self, locator) -> list:
        """Return all elements matching the given locator (does not wait)."""
        return self.driver.find_elements(*locator)

    def wait_element_visible(self, locator, timeout: int | None = None):
        """Compatibility alias for wait_for_visible. No @allure.step — delegates to the already-decorated method."""
        return self.wait_for_visible(locator, timeout)

    # ================= ACTIONS =================

    @allure.step("Click element: {locator}")
    def click(self, locator, timeout: int | None = None):
        try:
            element = self.wait_for_clickable(locator, timeout)
            element.click()
        except ElementClickInterceptedException:
            element = self.wait_for_visible(locator, timeout)
            self.execute_script("arguments[0].click();", element)

    @allure.step("Click button: {locator}")
    def click_button(self, locator, timeout: int | None = None):
        self.click(locator, timeout)

    @allure.step("Type '{value}' into element: {locator}")
    def fill(self, locator, value: str, timeout: int | None = None):
        element = self.wait_for_visible(locator, timeout)
        element.clear()
        element.send_keys(value)
        return element

    @allure.step("Get text of element: {locator}")
    def get_text(self, locator, timeout: int | None = None) -> str:
        element = self.wait_for_visible(locator, timeout)
        return element.text

    # ================= SCROLL =================

    @allure.step("Scroll element into view: {locator}")
    def scroll_into_view(self, locator, timeout: int | None = None):
        element = self.wait_for_visible(locator, timeout)
        self.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element,
        )
        return element

    # ================= JS =================

    @allure.step("Execute JavaScript")
    def execute_script(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    # ================= MODALS =================

    @allure.step("Force close all modal overlays")
    def force_close_modals(self):
        try:
            self.execute_script(
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

    @allure.step("Drag and drop element (JS simulation, Firefox-compatible)")
    def drag_and_drop(self, source_locator, target_locator):
        source = self.wait_for_visible(source_locator)
        target = self.wait_for_visible(target_locator)

        self.execute_script(
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
