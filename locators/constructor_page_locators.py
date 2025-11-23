from selenium.webdriver.common.by import By


class ConstructorPageLocators:
    """Локаторы элементов на странице конструктора бургеров."""

    # Вкладки конструктора
    TAB_BUNS = (By.XPATH, "//span[text()='Булки']/..")
    TAB_SAUCES = (By.XPATH, "//span[text()='Соусы']/..")
    TAB_FILLINGS = (By.XPATH, "//span[text()='Начинки']/..")

    # Одна карточка ингредиента (любая)
    INGREDIENT_ITEM = (
        By.XPATH,
        "//section[contains(@class,'BurgerIngredients_ingredients')]"
        "//div[contains(@class,'BurgerIngredient_ingredient__')]",
    )

    # Модальное окно ингредиента
    INGREDIENT_MODAL = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]"
        "//h2[contains(@class,'Modal_modal_title')]",
    )

    # Кнопка закрытия модального окна ингредиента (крестик)
    INGREDIENT_MODAL_CLOSE = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]"
        "//button[contains(@class,'Modal_modal__close')]",
    )

    # Кнопка "Оформить заказ"
    ORDER_BUTTON = (
        By.XPATH,
        "//button[.//p[text()='Оформить заказ']]",
    )
