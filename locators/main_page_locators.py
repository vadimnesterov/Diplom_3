from selenium.webdriver.common.by import By


class MainPageLocators:
    # Header navigation buttons
    constructor_button = (By.XPATH, "//p[text()='Конструктор']")                                    # Constructor nav button
    order_feed_button = (By.XPATH, "//p[text()='Лента Заказов']")                                   # Order Feed nav button
    personal_account_button = (By.XPATH, "//p[text()='Личный Кабинет']")                            # Personal account nav button

    # Ingredient detail modal window
    ingredient_modal = (By.XPATH, "//h2[text()= 'Детали ингредиента']")                             # "Ingredient details" modal
    close_ingredient_modal = (By.XPATH, "//button[contains(@class,'close')]")                       # Close button on the ingredient modal

    modal_overlay = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay__x2ZCr')]")            # Modal overlay backdrop
    fluorescent_bun = (By.XPATH, "//img[@alt = 'Флюоресцентная булка R2-D3']")                      # Fluorescent Bun R2-D3 ingredient image
    constructor_drop_area = (By.XPATH, "//div[contains(@class, 'constructor-element_pos_top')]")    # Constructor drop area for drag-and-drop

    # Ingredient counter badge
    ingredient_counter = (
        By.XPATH,
        "//img[@alt='Флюоресцентная булка R2-D3']/../.."
        "//p[contains(@class, 'counter_counter__num__3nue1')]"
    )

    # Order placement locators
    order_button = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")                      # "Place order" button
    login_to_order_button = (By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]")            # "Login to account" button (shown when not authenticated)

    order_modal = (By.XPATH, ".//h2[contains(@class, 'Modal_modal__title_shadow__3ikwq')]")        # Order number element inside the confirmation modal
    order_number_loading = (By.XPATH, "//h2[text()='9999']")                                       # Temporary loading placeholder "9999"
    order_number_final = (
        By.XPATH,
        "//h2[contains(@class, 'Modal_modal__title_shadow__3ikwq') and not(text()='9999')]"
    )                                                                                               # Final confirmed order number (not the loading placeholder)
    close_order_modal = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__')]//button[contains(@class, 'close')]"
    )
