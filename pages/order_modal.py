from locators.modal_locators import ModalLocators
from .base_page import BasePage


class OrderModal(BasePage):
    """Модальное окно заказа."""

    def is_open(self) -> bool:
        """Проверить, что модальное окно заказа открыто."""
        return self.is_visible(ModalLocators.ORDER_MODAL)

    def get_order_number(self) -> str:
        """Получить номер заказа из модального окна."""
        return self.get_text(ModalLocators.ORDER_NUMBER)

    def close(self):
        """Закрыть модальное окно заказа."""
        self.click(ModalLocators.ORDER_MODAL_CLOSE)
