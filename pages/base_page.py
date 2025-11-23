import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException
)


class BasePage:
    OVERLAY = (By.CLASS_NAME, "Modal_modal_overlay__x2ZCr")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        """SAFE: открыть URL."""
        self.driver.get(url)

    # ---------------- WAITERS ----------------

    def wait_for_overlay_to_disappear(self, timeout: int = 10):
        """Ждём, пока модальный оверлей исчезнет."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.OVERLAY)
            )
        except (TimeoutException, NoSuchElementException):
            pass

    def wait_element_to_be_clickable(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def is_visible(self, locator, timeout: int = 10) -> bool:
        """Возвращает True, если элемент видим."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ---------------- ACTIONS ----------------

    @allure.step("Ввод текста")
    def type(self, locator, text: str, clear: bool = True, timeout: int = 10):
        """Ожидание поля и ввод текста."""
        self.wait_for_overlay_to_disappear(timeout)

        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

        if clear:
            element.clear()

        element.send_keys(text)
        return element

    @allure.step("Клик по элементу")
    def click(self, locator, timeout: int = 10):
        """Клик: ожидание оверлея → обычный клик → JS-клик."""
        self.wait_for_overlay_to_disappear(timeout)

        element = self.wait_element_to_be_clickable(locator, timeout)

        try:
            element.click()
            return
        except ElementClickInterceptedException:
            self.wait_for_overlay_to_disappear(timeout)
            element = self.wait_element_to_be_clickable(locator, timeout)

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
            self.driver.execute_script("arguments[0].click();", element)
            return
