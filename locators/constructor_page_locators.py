from selenium.webdriver.common.by import By

class ConstructorPageLocators:
    PAGE_HEADER = (By.XPATH, "//h1[contains(text(),'Соберите бургер')]")
    # --- TABS ---
    TAB_BUNS = (By.XPATH, "//span[text()='Булки']/parent::div[@class='tab_tab__1SPyG pt-4 pr-10 pb-4 pl-10 noselect' or contains(@class,'tab_tab__')]")
    TAB_SAUCES = (By.XPATH, "//span[text()='Соусы']/parent::div[contains(@class,'tab_tab__')]")
    TAB_FILLINGS = (By.XPATH, "//span[text()='Начинки']/parent::div[contains(@class,'tab_tab__')]")

    # Order button
    ORDER_BUTTON = (By.XPATH, "//button[contains(@class,'button_button') and .='Оформить заказ']")
