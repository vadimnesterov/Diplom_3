# pages/constructor_page.py v1.3

from pages.base_page import BasePage
from data.urls import MainUrl
from locators.constructor_page_locators import ConstructorPageLocators


class ConstructorPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # ----------------------------------------------------
    # Открытие конструктора
    # ----------------------------------------------------
    def open_constructor(self):
        """
        Открывает страницу с конструктором бургера:
        переходим через базовый URL и ждём появления заголовка.
        """
        self.open(MainUrl.MAIN_URL)
        self.wait_for_visible(ConstructorPageLocators.PAGE_HEADER)

    # ----------------------------------------------------
    # Вкладки: Булки / Соусы / Начинки
    # ----------------------------------------------------
    def _wait_tab_active(self, locator):
        """
        Ожидает, что у вкладки появится класс "tab_tab_type_current".
        Используем ожидание видимости.
        """
        self.wait_for_condition(
            lambda d: "tab_tab_type_current"
            in self.wait_for_visible(locator).get_attribute("class")
        )

    def select_buns_tab(self):
        tab = self.wait_for_clickable(ConstructorPageLocators.TAB_BUNS)
        self.scroll_into_view(ConstructorPageLocators.TAB_BUNS)
        self.click(ConstructorPageLocators.TAB_BUNS)
        self._wait_tab_active(ConstructorPageLocators.TAB_BUNS)

    def select_sauces_tab(self):
        tab = self.wait_for_clickable(ConstructorPageLocators.TAB_SAUCES)
        self.scroll_into_view(ConstructorPageLocators.TAB_SAUCES)
        self.click(ConstructorPageLocators.TAB_SAUCES)
        self._wait_tab_active(ConstructorPageLocators.TAB_SAUCES)

    def select_fillings_tab(self):
        tab = self.wait_for_clickable(ConstructorPageLocators.TAB_FILLINGS)
        self.scroll_into_view(ConstructorPageLocators.TAB_FILLINGS)
        self.click(ConstructorPageLocators.TAB_FILLINGS)
        self._wait_tab_active(ConstructorPageLocators.TAB_FILLINGS)

    # ----------------------------------------------------
    # Сборка простого бургера (минимальный сценарий)
    # ----------------------------------------------------
    def build_burger_with_one_bun(self):
        """
        Минимальная сборка бургера для сценариев оформления заказа.

        Логика:
        - переключаемся на вкладку "Булки" (если возможно);
        - берём первый доступный ингредиент в списке;
        - перетаскиваем его в область конструктора через drag&drop из BasePage.
        """
        try:
            self.select_buns_tab()
        except Exception:
            pass

        # первый ингредиент
        ingredient = self.wait_for_visible(
            ConstructorPageLocators.FIRST_INGREDIENT
        )

        # область конструктора
        constructor_drop_area = self.wait_for_visible(
            ConstructorPageLocators.CONSTRUCTOR_DROP_AREA
        )

        self.drag_and_drop(ingredient, constructor_drop_area)

    # ----------------------------------------------------
    # Кнопка "Оформить заказ"
    # ----------------------------------------------------
    def click_order_button(self):
        """
        Ждём кликабельность кнопки "Оформить заказ" и кликаем по ней.
        """
        self.scroll_into_view(ConstructorPageLocators.ORDER_BUTTON)
        self.click(ConstructorPageLocators.ORDER_BUTTON)
