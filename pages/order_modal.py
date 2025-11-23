from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage
from locators.modal_locators import ModalLocators


class OrderModal(BasePage):
    """Модальное окно заказа."""

    def is_open(self) -> bool:
        """SAFE: модалка считается открытой, когда появился номер заказа."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(ModalLocators.ORDER_NUMBER)
            )
            return True
        except:
            return False

    def get_order_number(self) -> str:
        """SAFE: получить номер заказа (как у конкурентов)."""
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(ModalLocators.ORDER_NUMBER)
        )
        return element.text

    def close(self):
        """Кнопка закрытия модалки."""
        close_btn = self.driver.find_element(*ModalLocators.ORDER_MODAL_CLOSE)
        close_btn.click()
