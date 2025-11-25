from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.order_modal_locators import OrderModalLocators


class OrderModal:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def is_open(self) -> bool:
        """Открыта ли модалка с заказом."""
        try:
            self.wait.until(
                EC.visibility_of_element_located(OrderModalLocators.MODAL_ROOT)
            )
            return True
        except Exception:
            return False

    def wait_until_closed(self, timeout: int = 15) -> bool:
        """Ожидать закрытия модального окна."""
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.visibility_of_element_located(OrderModalLocators.MODAL_ROOT)
            )
            return True
        except Exception:
            return False

    def get_order_number(self) -> str:
        """
        Получить номер заказа из модалки.
        Возвращает только цифры (без пробелов и #).
        """
        element = self.wait.until(
            EC.visibility_of_element_located(OrderModalLocators.ORDER_NUMBER)
        )
        text = element.text.strip()
        digits = "".join(ch for ch in text if ch.isdigit())
        return digits
