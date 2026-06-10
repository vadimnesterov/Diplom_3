from selenium.webdriver.common.by import By


class ConstructorPageLocators:
    PAGE_HEADER = (By.XPATH, "//h1[contains(text(),'Соберите бургер')]")

    # --- TABS ---
    TAB_BUNS = (
        By.XPATH,
        "//span[text()='Булки']/parent::div[@class='tab_tab__1SPyG pt-4 pr-10 pb-4 pl-10 noselect' "
        "or contains(@class,'tab_tab__')]"
    )
    TAB_SAUCES = (
        By.XPATH,
        "//span[text()='Соусы']/parent::div[contains(@class,'tab_tab__')]"
    )
    TAB_FILLINGS = (
        By.XPATH,
        "//span[text()='Начинки']/parent::div[contains(@class,'tab_tab__')]"
    )

    # --- INGREDIENTS ---
    # First item in the ingredient section list
    FIRST_INGREDIENT = (
        By.XPATH,
        "//section[contains(@class,'BurgerIngredients')]"
        "//*[self::li or self::a or self::div][1]"
    )

    # --- CONSTRUCTOR AREA ---
    # Drop zone that accepts dragged ingredients
    CONSTRUCTOR_DROP_AREA = (
        By.XPATH,
        "//main//section[contains(@class,'BurgerConstructor')]"
        "//*[contains(@class,'BurgerConstructor_basket') "
        "or contains(@class,'burger-element_pos_top') "
        "or name()='ul']"
    )

    # --- ORDER BUTTON ---
    ORDER_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'button_button') and .='Оформить заказ']"
    )
