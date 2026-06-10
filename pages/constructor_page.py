import allure

from pages.base_page import BasePage
from data.urls import MainUrl
from locators.constructor_page_locators import ConstructorPageLocators


class ConstructorPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # ----------------------------------------------------
    # Opening the constructor
    # ----------------------------------------------------
    @allure.step("Open the constructor page")
    def open_constructor(self):
        """
        Opens the burger constructor page:
        navigates to the base URL and waits for the page header to appear.
        """
        self.open(MainUrl.MAIN_URL)
        self.wait_for_visible(ConstructorPageLocators.PAGE_HEADER)

    # ----------------------------------------------------
    # Tabs: Buns / Sauces / Fillings
    # ----------------------------------------------------
    def _wait_tab_active(self, locator):
        """
        Waits for the tab to receive the "tab_tab_type_current" class.
        Internal helper; @allure.step is intentionally omitted to avoid step spam from the already-decorated callers.
        """
        self.wait_for_condition(
            lambda d: "tab_tab_type_current"
            in self.find_element(locator).get_attribute("class")
        )

    @allure.step("Switch to the 'Buns' tab")
    def select_buns_tab(self):
        self.wait_for_clickable(ConstructorPageLocators.TAB_BUNS)
        self.scroll_into_view(ConstructorPageLocators.TAB_BUNS)
        self.click(ConstructorPageLocators.TAB_BUNS)
        self._wait_tab_active(ConstructorPageLocators.TAB_BUNS)

    @allure.step("Switch to the 'Sauces' tab")
    def select_sauces_tab(self):
        self.wait_for_clickable(ConstructorPageLocators.TAB_SAUCES)
        self.scroll_into_view(ConstructorPageLocators.TAB_SAUCES)
        self.click(ConstructorPageLocators.TAB_SAUCES)
        self._wait_tab_active(ConstructorPageLocators.TAB_SAUCES)

    @allure.step("Switch to the 'Fillings' tab")
    def select_fillings_tab(self):
        self.wait_for_clickable(ConstructorPageLocators.TAB_FILLINGS)
        self.scroll_into_view(ConstructorPageLocators.TAB_FILLINGS)
        self.click(ConstructorPageLocators.TAB_FILLINGS)
        self._wait_tab_active(ConstructorPageLocators.TAB_FILLINGS)

    # ----------------------------------------------------
    # Building a simple burger (minimal scenario)
    # ----------------------------------------------------
    @allure.step("Build a burger with one bun")
    def build_burger_with_one_bun(self):
        """
        Minimal burger assembly for order placement scenarios.

        Logic:
        - switch to the "Buns" tab (if possible);
        - take the first available ingredient in the list;
        - drag it into the constructor area via drag&drop from BasePage.
        """
        try:
            self.select_buns_tab()
        except Exception:
            pass

        self.drag_and_drop(
            ConstructorPageLocators.FIRST_INGREDIENT,
            ConstructorPageLocators.CONSTRUCTOR_DROP_AREA,
        )

    # ----------------------------------------------------
    # "Place Order" button
    # ----------------------------------------------------
    @allure.step("Click the 'Place Order' button in the constructor")
    def click_order_button(self):
        """
        Waits for the 'Place Order' button to be clickable and clicks it.
        """
        self.scroll_into_view(ConstructorPageLocators.ORDER_BUTTON)
        self.click(ConstructorPageLocators.ORDER_BUTTON)
