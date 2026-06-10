import allure

from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from data.urls import URLS


@allure.epic("Main functionality")
@allure.feature("Main page")
class TestMainPageFunctionality:
    """Tests for the core functionality of the main page."""

    @allure.title('Navigate by clicking "Constructor"')
    @allure.description('''
        Verify navigation by clicking "Constructor":
        1. Open the main page
        2. Navigate to the Order Feed
        3. Return to the main page by clicking "Constructor"
        4. Verify the user is no longer on the order feed page
        ''')
    def test_go_to_constructor_from_header(self, driver):
        main = MainPage(driver)
        main.open()

        # Go to the order feed so we are definitely not on /
        main.click_order_feed()
        main.wait_for_url_contains(URLS.url_feed)
        assert main.is_url_contains(URLS.url_feed)

        # Return by clicking "Constructor"
        main.click_constructor()
        main.wait_for_url_contains("/")
        assert not main.is_url_contains(URLS.url_feed)

    @allure.title('Navigate by clicking "Order Feed"')
    @allure.description('''
        Verify navigation by clicking "Order Feed":
        1. Open the main page
        2. Click on "Order Feed"
        3. Verify that the order feed page loaded
        ''')
    def test_go_to_order_feed_from_header(self, driver):
        main = MainPage(driver)
        main.open()

        main.click_order_feed()

        feed = OrderFeedPage(driver)
        assert feed.is_order_feed_page_loaded()

    @allure.title('Clicking an ingredient shows a popup with details')
    @allure.description('''
        Verify that clicking an ingredient opens a details popup:
        1. Open the main page
        2. Click on an ingredient
        3. Verify that the details modal opened
        ''')
    def test_ingredient_modal_opens_on_click(self, driver):
        main = MainPage(driver)
        main.open()

        main.click_ingredient()
        assert main.is_ingredient_modal_visible()

    @allure.title('Adding an ingredient to the order increases its counter')
    @allure.description('''
        Verify that the ingredient counter increases after dragging:
        1. Open the main page
        2. Record the current ingredient counter value
        3. Drag the ingredient into the constructor area
        4. Verify that the counter value increased
        ''')
    def test_ingredient_counter_increases_after_drag(self, driver):
        main = MainPage(driver)
        main.open()

        before = main.get_ingredient_counter()
        main.drag_ingredient_to_constructor()
        after = main.get_ingredient_counter()

        assert after > before
