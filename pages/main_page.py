import allure

from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators
from data.urls import MainUrl


class MainPage(BasePage):
    # Used in tests: driver.get(f"{MainPage.BASE_URL}feed")
    BASE_URL = MainUrl.MAIN_URL

    def __init__(self, driver):
        super().__init__(driver)
        self.url = MainUrl.MAIN_URL

    @allure.step("Open the main page")
    def open(self):
        self.driver.get(self.url)
        self.wait_for_page_load()

    @allure.step('Click the "Constructor" button')
    def click_constructor(self):
        self.click_button(MainPageLocators.constructor_button)

    @allure.step('Click the "Order Feed" button')
    def click_order_feed(self):
        self.click_button(MainPageLocators.order_feed_button)

    @allure.step("Click on an ingredient")
    def click_ingredient(self):
        self.click_button(MainPageLocators.fluorescent_bun)

    @allure.step("Close the ingredient modal")
    def close_ingredient_modal(self):
        try:
            self.click_button(MainPageLocators.close_ingredient_modal)
        except Exception:
            self.close_modal_by_overlay()

    @allure.step("Close the modal by clicking the overlay")
    def close_modal_by_overlay(self):
        try:
            if self.is_element_visible(MainPageLocators.modal_overlay, timeout=2):
                self.click_button(MainPageLocators.modal_overlay)
        except Exception:
            self.force_close_modals()

    @allure.step("Check ingredient modal visibility")
    def is_ingredient_modal_visible(self):
        return self.is_element_visible(MainPageLocators.ingredient_modal)

    @allure.step("Check that the ingredient modal is closed")
    def is_ingredient_modal_closed(self):
        return self.is_element_not_visible(MainPageLocators.ingredient_modal)

    @allure.step("Drag ingredient into the constructor")
    def drag_ingredient_to_constructor(self):
        # Close all modals before DnD just in case
        self.close_all_modals()

        self.wait_element_visible(MainPageLocators.fluorescent_bun)
        self.wait_element_visible(MainPageLocators.constructor_drop_area)

        self.drag_and_drop(
            MainPageLocators.fluorescent_bun,
            MainPageLocators.constructor_drop_area,
        )

    @allure.step("Get ingredient counter value")
    def get_ingredient_counter(self):
        try:
            counter_element = self.find_element(MainPageLocators.ingredient_counter)
            if counter_element.is_displayed():
                counter_text = counter_element.text
                return int(counter_text) if counter_text else 0
            return 0
        except Exception:
            return 0

    @allure.step("Close all open modals")
    def close_all_modals(self):
        try:
            if self.is_element_visible(MainPageLocators.close_ingredient_modal, timeout=1):
                self.click_button(MainPageLocators.close_ingredient_modal)

            self.close_modal_by_overlay()
            self.force_close_modals()
        except Exception:
            self.force_close_modals()

    @allure.step("Click the place order button")
    def click_order_button(self):
        self.click_button(MainPageLocators.order_button)

    @allure.step("Get order number from modal (raw value)")
    def get_order_number_from_modal(self):
        try:
            order_number_element = self.wait_element_visible(
                MainPageLocators.order_modal,
                timeout=10,
            )
            return order_number_element.text
        except Exception:
            return None

    @allure.step("Close the order modal")
    def close_order_modal(self):
        try:
            self.click_button(MainPageLocators.close_order_modal)
        except Exception:
            self.close_modal_by_overlay()

    @allure.step("Check that the place order button is visible")
    def is_order_button_visible(self):
        return self.is_element_visible(MainPageLocators.order_button)

    @allure.step("Get the final order number from the modal")
    def get_final_order_number(self, timeout: int = 15):
        try:
            # Wait until the temporary placeholder "9999" disappears via BasePage
            self.wait_for_invisibility(
                MainPageLocators.order_number_loading,
                timeout=timeout,
            )

            # Then wait for the final order number to appear
            order_number_element = self.wait_element_visible(
                MainPageLocators.order_number_final,
                timeout=5,
            )
            return order_number_element.text
        except Exception:
            return None

    @allure.step("Create an order via UI and return the final order number")
    def create_order_ui(self):
        """
        Standalone method:
        1) Opens the main page
        2) Drags an ingredient into the constructor
        3) Clicks 'Place Order'
        4) Returns the final order number (format not guaranteed)
        """
        # Always ensure we are on the main page
        self.open()

        self.drag_ingredient_to_constructor()
        self.click_order_button()

        order_number = self.get_final_order_number()
        self.close_order_modal()

        return order_number
