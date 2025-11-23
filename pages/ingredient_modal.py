from locators.modal_locators import ModalLocators
from .base_page import BasePage


class IngredientModal(BasePage):
    """Модальное окно ингредиента."""

    def is_open(self) -> bool:
        """Проверить, что модальное окно ингредиента открыто."""
        return self.is_visible(ModalLocators.INGREDIENT_MODAL)

    def get_title(self) -> str:
        """Получить название ингредиента."""
        return self.get_text(ModalLocators.INGREDIENT_MODAL_TITLE)

    def close_by_cross(self):
        """Закрыть модальное окно по крестику."""
        self.click(ModalLocators.INGREDIENT_MODAL_CLOSE)
