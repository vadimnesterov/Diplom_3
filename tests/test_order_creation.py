import allure

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from helpers.order_helper import normalize_order_number


class TestOrderFeed:
    @allure.title('After placing an order the "Completed all time" counter increases')
    @allure.description(
        "1. Log in as a user\n"
        "2. Navigate to the order feed\n"
        "3. Save the current \"Completed all time\" counter value\n"
        "4. Return to the constructor and create an order via UI\n"
        "5. Navigate back to the order feed\n"
        "6. Verify that the counter increased"
    )
    def test_new_order_increases_total_counter(self, driver, api_user):
        # Log in
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        assert login_page.submit_login(), "Login failed"

        main_page = MainPage(driver)
        feed_page = OrderFeedPage(driver)

        # Navigate to the order feed
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Order feed page did not load."

        # Save the initial counter value
        initial_total = feed_page.get_total_orders_count()

        # Return to the main page (constructor) and create an order via UI
        main_page.click_constructor()
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Failed to get the order number."
        assert order_number != "9999", "Received temporary placeholder order number 9999 instead of the final number."

        # Navigate back to the order feed via the header
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Order feed page did not load after placing the order."

        # Wait for the counter to update
        assert feed_page.wait_for_counters_update(
            initial_total=initial_total,
            initial_today=None,
            timeout=30,
        ), '"Completed all time" counter did not update after placing the order.'

        # Final comparison
        new_total = feed_page.get_total_orders_count()
        assert new_total > initial_total, (
            f'"Completed all time" counter did not increase. '
            f"Before: {initial_total}, after: {new_total}"
        )

    @allure.title('After placing an order the "Completed today" counter increases')
    @allure.description(
        "1. Log in as a user\n"
        "2. Navigate to the order feed\n"
        "3. Save the current \"Completed today\" counter value\n"
        "4. Return to the constructor and create an order via UI\n"
        "5. Navigate back to the order feed\n"
        "6. Verify that the daily counter increased"
    )
    def test_new_order_increases_today_counter(self, driver, api_user):
        # Log in
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        assert login_page.submit_login(), "Login failed"

        main_page = MainPage(driver)
        feed_page = OrderFeedPage(driver)

        # Navigate to the order feed
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Order feed page did not load."

        # Save the initial daily counter value
        initial_today = feed_page.get_today_orders_count()

        # Return to the main page (constructor) and create an order via UI
        main_page.click_constructor()
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Failed to get the order number."
        assert order_number != "9999", "Received temporary placeholder order number 9999 instead of the final number."

        # Navigate back to the order feed via the header
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Order feed page did not load after placing the order."

        # Wait for the daily counter to update
        assert feed_page.wait_for_counters_update(
            initial_total=None,
            initial_today=initial_today,
            timeout=30,
        ), '"Completed today" counter did not update after placing the order.'

        # Final comparison
        new_today = feed_page.get_today_orders_count()
        assert new_today > initial_today, (
            f'"Completed today" counter did not increase. '
            f"Before: {initial_today}, after: {new_today}"
        )

    @allure.title('After placing an order its number appears in the "In Progress" section')
    @allure.description(
        "1. Log in as a user\n"
        "2. Create an order via UI from the main page (constructor)\n"
        "3. Navigate to the order feed via the header\n"
        "4. Verify that the order number is present in the \"In Progress\" block"
    )
    def test_order_number_appears_in_in_progress_block(self, driver, api_user):
        # Log in
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        assert login_page.submit_login(), "Login failed"

        main_page = MainPage(driver)
        feed_page = OrderFeedPage(driver)

        # Activate the constructor just in case
        main_page.click_constructor()

        # Create an order via UI
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Failed to get the order number."
        assert order_number != "9999", "Received temporary placeholder order number 9999 instead of the final number."

        normalized_number = normalize_order_number(order_number)

        # Navigate to the order feed via the header
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Order feed page did not load."

        # Verify the order number appears in the "In Progress" block within the timeout.
        # A second read is intentionally omitted — the order may leave "In Progress"
        # quickly once processed, creating a TOCTOU race. The wait is the verification.
        assert feed_page.wait_for_order_in_progress(
            normalized_number,
            timeout=30,
        ), f"Order {normalized_number} did not appear in the 'In Progress' block."
