from data.urls import MAIN_PAGE
from locators.constructor_page_locators import ConstructorPageLocators
from .base_page import BasePage


class ConstructorPage(BasePage):
    """Страница конструктора бургеров."""

    def open_constructor(self):
        """Открыть страницу конструктора."""
        self.open(MAIN_PAGE)

    def select_buns_tab(self):
        """Переключиться на вкладку 'Булки'."""
        self.click(ConstructorPageLocators.TAB_BUNS)

    def select_sauces_tab(self):
        """Переключиться на вкладку 'Соусы'."""
        self.click(ConstructorPageLocators.TAB_SAUCES)

    def select_fillings_tab(self):
        """Переключиться на вкладку 'Начинки'."""
        self.click(ConstructorPageLocators.TAB_FILLINGS)

    def click_ingredient(self):
        """Кликнуть по первому ингредиенту для открытия модалки."""
        self.click(ConstructorPageLocators.INGREDIENT_ITEM)

    def click_order_button(self):
        """Нажать кнопку 'Оформить заказ'."""
        self.click(ConstructorPageLocators.ORDER_BUTTON)
