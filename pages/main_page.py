# pages/main_page.py v1.4

import allure

from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators
from data.urls import MainUrl


class MainPage(BasePage):
    # Нужен для тестов: driver.get(f"{MainPage.BASE_URL}feed")
    BASE_URL = MainUrl.MAIN_URL

    def __init__(self, driver):
        super().__init__(driver)
        self.url = MainUrl.MAIN_URL

    @allure.step("Открыть главную страницу")
    def open(self):
        self.driver.get(self.url)
        self.wait_for_page_load()

    @allure.step('Кликнуть на кнопку "Конструктор"')
    def click_constructor(self):
        self.click_button(MainPageLocators.constructor_button)

    @allure.step('Кликнуть на кнопку "Лента заказов"')
    def click_order_feed(self):
        self.click_button(MainPageLocators.order_feed_button)

    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self):
        self.click_button(MainPageLocators.fluorescent_bun)

    @allure.step("Закрыть модальное окно ингредиента")
    def close_ingredient_modal(self):
        try:
            self.click_button(MainPageLocators.close_ingredient_modal)
        except Exception:
            self.close_modal_by_overlay()

    @allure.step("Закрыть модальное окно кликом на оверлей")
    def close_modal_by_overlay(self):
        try:
            if self.is_element_visible(MainPageLocators.modal_overlay, timeout=2):
                self.click_button(MainPageLocators.modal_overlay)
        except Exception:
            self.force_close_modals()

    @allure.step("Проверить видимость модального окна")
    def is_ingredient_modal_visible(self):
        return self.is_element_visible(MainPageLocators.ingredient_modal)

    @allure.step("Проверить, что модальное окно закрыто")
    def is_ingredient_modal_closed(self):
        return self.is_element_not_visible(MainPageLocators.ingredient_modal)

    @allure.step("Перетащить ингредиент в конструктор")
    def drag_ingredient_to_constructor(self):
        # На всякий случай закрываем все модалки перед DnD
        self.close_all_modals()

        self.wait_element_visible(MainPageLocators.fluorescent_bun)
        self.wait_element_visible(MainPageLocators.constructor_drop_area)

        self.drag_and_drop(
            MainPageLocators.fluorescent_bun,
            MainPageLocators.constructor_drop_area,
        )

    @allure.step("Получить значение счётчика ингредиента")
    def get_ingredient_counter(self):
        try:
            counter_element = self.find_element(MainPageLocators.ingredient_counter)
            if counter_element.is_displayed():
                counter_text = counter_element.text
                return int(counter_text) if counter_text else 0
            return 0
        except Exception:
            return 0

    @allure.step("Закрыть все открытые модальные окна")
    def close_all_modals(self):
        try:
            if self.is_element_visible(MainPageLocators.close_ingredient_modal, timeout=1):
                self.click_button(MainPageLocators.close_ingredient_modal)

            self.close_modal_by_overlay()
            self.force_close_modals()
        except Exception:
            self.force_close_modals()

    @allure.step("Нажать кнопку оформления заказа")
    def click_order_button(self):
        self.click_button(MainPageLocators.order_button)

    @allure.step("Получить номер заказа из модального окна (сырое значение)")
    def get_order_number_from_modal(self):
        try:
            order_number_element = self.wait_element_visible(
                MainPageLocators.order_modal,
                timeout=10,
            )
            return order_number_element.text
        except Exception:
            return None

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        try:
            self.click_button(MainPageLocators.close_order_modal)
        except Exception:
            self.close_modal_by_overlay()

    @allure.step("Проверить, что кнопка оформления заказа доступна")
    def is_order_button_visible(self):
        return self.is_element_visible(MainPageLocators.order_button)

    @allure.step("Получить финальный номер заказа из модального окна")
    def get_final_order_number(self, timeout: int = 15):
        try:
            # Ждём, пока исчезнет временный номер "9999" через BasePage
            self.wait_for_invisibility(
                MainPageLocators.order_number_loading,
                timeout=timeout,
            )

            # Затем ждём появление финального номера
            order_number_element = self.wait_element_visible(
                MainPageLocators.order_number_final,
                timeout=5,
            )
            return order_number_element.text
        except Exception:
            return None

    @allure.step("Создать заказ через UI и получить финальный номер")
    def create_order_ui(self):
        """
        Standalone-метод:
        1) Открывает главную страницу
        2) Перетаскивает ингредиент в конструктор
        3) Жмёт 'Оформить заказ'
        4) Возвращает финальный номер заказа (без гарантии формата)
        """
        # Всегда гарантируем, что мы на главной
        self.open()

        self.drag_ingredient_to_constructor()
        self.click_order_button()

        order_number = self.get_final_order_number()
        self.close_order_modal()

        return order_number
