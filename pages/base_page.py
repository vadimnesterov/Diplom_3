from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Базовый класс для всех страниц UI-тестов."""

    def __init__(self, driver):
        self.driver = driver

    def open(self, url: str):
        """Открыть указанный URL."""
        self.driver.get(url)

    def wait_visible(self, locator, timeout: int = 10):
        """Ожидать, пока элемент станет видимым."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout: int = 10):
        """Ожидать, пока элемент станет кликабельным."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def find(self, locator, timeout: int = 10):
        """Найти элемент по локатору (с ожиданием видимости)."""
        return self.wait_visible(locator, timeout)

    def click(self, locator, timeout: int = 10):
        """Клик по элементу (с ожиданием кликабельности)."""
        element = self.wait_clickable(locator, timeout)
        element.click()
        return element

    def type_text(self, locator, text: str, timeout: int = 10):
        """Ввести текст в поле ввода (очистить и напечатать)."""
        element = self.wait_visible(locator, timeout)
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator, timeout: int = 10) -> str:
        """Получить текст элемента."""
        element = self.wait_visible(locator, timeout)
        return element.text

    def is_visible(self, locator, timeout: int = 5) -> bool:
        """Проверить, что элемент появился на странице и видим."""
        try:
            self.wait_visible(locator, timeout)
            return True
        except TimeoutException:
            return False
