from selenium.webdriver.common.by import By


class OrderFeedLocators:
    """Локаторы элементов на странице 'Лента заказов'."""

    # Заголовок / текст "Лента заказов"
    FEED_HEADER = (By.XPATH, "//h1[text()='Лента заказов']")

    # Список карточек заказов
    ORDERS_LIST = (
        By.XPATH,
        "//ul[contains(@class,'OrderFeed_list') or contains(@class,'OrderHistory_list')]/li",
    )

    # Блок "Выполнено за все время"
    TOTAL_ORDERS_ALL_TIME = (
        By.XPATH,
        "//p[text()='Выполнено за все время:']/following-sibling::p",
    )

    # Блок "Выполнено за сегодня"
    TOTAL_ORDERS_TODAY = (
        By.XPATH,
        "//p[text()='Выполнено за сегодня:']/following-sibling::p",
    )
