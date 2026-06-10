import allure

from pages.main_page import MainPage


class TestIngredientModal:

    @allure.title("Closing the ingredient modal by the cross button")
    @allure.description(
        "1. Open the main page\n"
        "2. Click on an ingredient\n"
        "3. Verify that the modal opened\n"
        "4. Close the modal by clicking the cross\n"
        "5. Verify that the modal is closed"
    )
    def test_ingredient_modal_closes_by_cross(self, driver):
        main_page = MainPage(driver)

        main_page.open()
        main_page.click_ingredient()

        assert main_page.is_ingredient_modal_visible(), "Ingredient modal did not open"

        main_page.close_ingredient_modal()

        assert main_page.is_ingredient_modal_closed(), "Ingredient modal did not close after clicking the cross"
