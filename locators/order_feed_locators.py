from selenium.webdriver.common.by import By


class OrderFeedLocators:
    # Заголовок страницы "Лента заказов"
    title_orders_list = (
        By.XPATH,
        "//h1[contains(text(), 'Лента заказов')]"
    )

    # Счётчик "Выполнено за всё время"
    total_orders_counter = (
        By.XPATH,
        "//p[contains(text(), 'Выполнено за все') or contains(text(), 'Выполнено за всё')]/following-sibling::p"
    )

    # Счётчик "Выполнено за сегодня"
    daily_orders_counter = (
        By.XPATH,
        "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p"
    )

    # Элементы заказов в блоке "В работе"
    number_order_in_job = (
        By.XPATH,
        "//ul[contains(@class,'OrderFeed_orderList') and contains(@class,'inWork')]//li"
        " | //ul[contains(@class,'OrderFeed_ordersList') and contains(@class,'inWork')]//li"
        " | //ul[contains(@class,'OrderFeed_list') and contains(@class,'inWork')]//li"
    )
