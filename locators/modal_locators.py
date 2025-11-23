from selenium.webdriver.common.by import By


class ModalLocators:
    """Локаторы для модальных окон (ингредиент и заказ)."""

    # Ингредиент
    INGREDIENT_MODAL = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]"
        "//h2[contains(@class,'Modal_modal_title')]",
    )
    INGREDIENT_MODAL_TITLE = INGREDIENT_MODAL
    INGREDIENT_MODAL_CLOSE = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]"
        "//button[contains(@class,'Modal_modal__close')]",
    )

    # Заказ
    ORDER_MODAL = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]"
        "//h2[contains(text(),'идентификатор заказа') or contains(text(),'номер заказа')]",
    )
    ORDER_NUMBER = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]//p[contains(@class,'digits')]",
    )
    ORDER_MODAL_CLOSE = INGREDIENT_MODAL_CLOSE
