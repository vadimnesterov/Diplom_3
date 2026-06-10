from selenium.webdriver.common.by import By


class OrderFeedLocators:
    # -------------------- COUNTERS --------------------

    # "Completed all time" counter
    total_orders_counter = (
        By.XPATH,
        "//p[text()='Выполнено за все время:']/following-sibling::p",
    )

    # "Completed today" counter
    daily_orders_counter = (
        By.XPATH,
        "//p[text()='Выполнено за сегодня:']/following-sibling::p",
    )

    # -------------------- ORDERS IN PROGRESS --------------------

    # All order items inside the "In Progress" block
    # Second <ul> — the "In Progress" list
    orders_in_progress_items = (
        By.XPATH,
        "//ul[contains(@class, 'OrderFeed_orderList__')][2]//li",
    )
