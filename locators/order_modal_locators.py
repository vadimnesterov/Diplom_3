from selenium.webdriver.common.by import By


class OrderModalLocators:
    """Локаторы модального окна заказа."""

    # Корень модалки
    MODAL_ROOT = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]"
    )

    # Заголовок "идентификатор заказа" или "номер заказа"
    ORDER_MODAL_TITLE = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]"
        "//h2[contains(text(),'идентификатор заказа') or contains(text(),'номер заказа')]"
    )

    # Номер заказа (большие цифры)
    ORDER_NUMBER = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]//p[contains(@class,'digits')]"
    )

    # Кнопка закрытия модалки
    ORDER_MODAL_CLOSE = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]"
        "//button[contains(@class,'Modal_modal__close')]"
    )
