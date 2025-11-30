# locators/order_feed_locators.py
# version: v1.1

from selenium.webdriver.common.by import By


class OrderFeedLocators:
    # -------------------- COUNTERS --------------------

    # "Выполнено за всё время"
    total_orders_counter = (
        By.XPATH,
        "//p[text()='Выполнено за все время:']/following-sibling::p",
    )

    # "Выполнено за сегодня"
    daily_orders_counter = (
        By.XPATH,
        "//p[text()='Выполнено за сегодня:']/following-sibling::p",
    )

    # -------------------- ORDERS IN PROGRESS --------------------

    # Все элементы заказов в блоке "В работе"
    # Второй список ul с заказами
    orders_in_progress_items = (
        By.XPATH,
        "//ul[contains(@class, 'OrderFeed_orderList__')][2]//li",
    )
