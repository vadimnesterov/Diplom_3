# pages/main_page.py

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import allure

from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators
from data.urls import MainUrl


class MainPage(BasePage):
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
            order_number_element = self.wait_element_visible(MainPageLocators.order_modal, timeout=10)
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
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(MainPageLocators.order_number_loading)
            )
            order_number_element = self.wait_element_visible(
                MainPageLocators.order_number_final,
                timeout=5,
            )
            return order_number_element.text
        except Exception:
            return None

    @allure.step("Создать заказ через UI")
    def create_order_ui(self):
        """
        Эталонная, максимально стабильная реализация:
        1) перетаскиваем ингредиент
        2) ждём появления счётчика ингредиента (доказательство, что добавился)
        3) ждём кликабельности кнопки 'Оформить заказ'
        4) кликаем
        5) ждём исчезновения 9999 (временного номера)
        6) ждём появления финального реального номера
        7) закрываем модалку
        8) возвращаем номер
        """

        # 1. Перетаскиваем ингредиент
        self.drag_ingredient_to_constructor()

        # 2. Проверяем что ингредиент действительно добавился
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(MainPageLocators.ingredient_counter)
        )

        # 3. Кнопка "Оформить заказ" должна быть кликабельна
        order_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.order_button)
        )

        # 4. Кликаем
        order_btn.click()

        # 5. Ждём исчезновения временного номера 9999 (если он появляется)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(MainPageLocators.order_number_loading)
            )
        except Exception:
            pass  # иногда 9999 не успевает появиться — это нормально

        # 6. Ждём появления финального номера заказа
        final_number_el = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(MainPageLocators.order_number_final)
        )
        order_number = final_number_el.text.strip()

        # 7. Закрываем модалку заказа
        try:
            close_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(MainPageLocators.close_order_modal)
            )
            close_btn.click()
        except Exception:
            self.close_modal_by_overlay()

        # 8. Возвращаем номер
        return order_number

