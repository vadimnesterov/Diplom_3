# pages/constructor_page.py v1.4

import allure

from pages.base_page import BasePage
from data.urls import MainUrl
from locators.constructor_page_locators import ConstructorPageLocators


class ConstructorPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # ----------------------------------------------------
    # Открытие конструктора
    # ----------------------------------------------------
    @allure.step("Открыть страницу конструктора")
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
        ВСПОМОГАТЕЛЬНЫЙ метод — allure.step здесь НЕ нужен.
        """
        self.wait_for_condition(
            lambda d: "tab_tab_type_current"
            in self.find_element(locator).get_attribute("class")
        )

    @allure.step("Переключиться на вкладку 'Булки'")
    def select_buns_tab(self):
        self.wait_for_clickable(ConstructorPageLocators.TAB_BUNS)
        self.scroll_into_view(ConstructorPageLocators.TAB_BUNS)
        self.click(ConstructorPageLocators.TAB_BUNS)
        self._wait_tab_active(ConstructorPageLocators.TAB_BUNS)

    @allure.step("Переключиться на вкладку 'Соусы'")
    def select_sauces_tab(self):
        self.wait_for_clickable(ConstructorPageLocators.TAB_SAUCES)
        self.scroll_into_view(ConstructorPageLocators.TAB_SAUCES)
        self.click(ConstructorPageLocators.TAB_SAUCES)
        self._wait_tab_active(ConstructorPageLocators.TAB_SAUCES)

    @allure.step("Переключиться на вкладку 'Начинки'")
    def select_fillings_tab(self):
        self.wait_for_clickable(ConstructorPageLocators.TAB_FILLINGS)
        self.scroll_into_view(ConstructorPageLocators.TAB_FILLINGS)
        self.click(ConstructorPageLocators.TAB_FILLINGS)
        self._wait_tab_active(ConstructorPageLocators.TAB_FILLINGS)

    # ----------------------------------------------------
    # Сборка простого бургера (минимальный сценарий)
    # ----------------------------------------------------
    @allure.step("Собрать бургер с одной булкой")
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

        ingredient = self.wait_for_visible(
            ConstructorPageLocators.FIRST_INGREDIENT
        )

        constructor_drop_area = self.wait_for_visible(
            ConstructorPageLocators.CONSTRUCTOR_DROP_AREA
        )

        self.drag_and_drop(ingredient, constructor_drop_area)

    # ----------------------------------------------------
    # Кнопка "Оформить заказ"
    # ----------------------------------------------------
    @allure.step("Нажать кнопку 'Оформить заказ' в конструкторе")
    def click_order_button(self):
        """
        Ждём кликабельность кнопки "Оформить заказ" и кликаем по ней.
        """
        self.scroll_into_view(ConstructorPageLocators.ORDER_BUTTON)
        self.click(ConstructorPageLocators.ORDER_BUTTON)
