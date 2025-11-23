from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Базовый класс для всех страниц UI-тестов."""

    # Общий селектор для любых модальных оверлеев
    OVERLAY = (
        By.CSS_SELECTOR,
        ".Modal_modal__P3_V5, .Modal_modal_overlay__x2ZCr",
    )

    def __init__(self, driver):
        self.driver = driver

    # ---------- Базовые действия ----------

    def open(self, url: str) -> None:
        """Открыть указанный URL."""
        self.driver.get(url)

    # ---------- Ожидания ----------

    def wait_overlay_disappear(self, timeout: int = 10) -> None:
        """Ожидать, пока исчезнет модальное перекрытие (overlay)."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.OVERLAY)
            )
        except TimeoutException:
            # Если overlay нет или он не исчез — продолжаем сценарий
            pass

    def wait_visible(self, locator, timeout: int = 10):
        """Ожидать, пока элемент станет видимым."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout: int = 10):
        """Ожидать, пока элемент станет кликабельным (с учётом overlay)."""
        self.wait_overlay_disappear()
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    # ---------- Работа с элементами ----------

    def find(self, locator, timeout: int = 10):
        """Найти элемент по локатору (с ожиданием видимости)."""
        return self.wait_visible(locator, timeout)

    def click(self, locator, timeout: int = 10):
        """
        Клик по элементу с ожиданием кликабельности.
        Если обычный клик перехватывается другим элементом,
        выполняется JS-клик.
        """
        self.wait_overlay_disappear()
        element = self.wait_clickable(locator, timeout)

        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

        self.wait_overlay_disappear()
        return element

    # На случай, если где-то используется старое имя
    def click_when_clickable(self, locator, timeout: int = 10):
        """Обёртка над click() для совместимости с существующим кодом."""
        return self.click(locator, timeout)

    def type_text(self, locator, text: str, timeout: int = 10):
        """Ввести текст в поле: дождаться, очистить и напечатать."""
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
