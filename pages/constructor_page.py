from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data.urls import MAIN_PAGE
from locators.constructor_page_locators import ConstructorPageLocators


class ConstructorPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ----------------------------------------------------
    # Ждём исчезновения оверлея
    # ----------------------------------------------------
    def _wait_overlay_disappear(self):
        try:
            self.wait.until_not(
                EC.presence_of_element_located(ConstructorPageLocators.MODAL_OVERLAY)
            )
        except:
            pass

    # ----------------------------------------------------
    # Открытие конструктора
    # ----------------------------------------------------
    def open_constructor(self):
        self.driver.get(MAIN_PAGE)
        self.wait.until(
            EC.visibility_of_element_located(ConstructorPageLocators.PAGE_HEADER)
        )
        self._wait_overlay_disappear()

    # ----------------------------------------------------
    # Хелпер: wait until tab has class tab_tab_type_current
    # ----------------------------------------------------
    def _wait_tab_active(self, locator):
        self.wait.until(
            lambda d: "tab_tab_type_current" in d.find_element(*locator).get_attribute("class")
        )

    # ----------------------------------------------------
    # Булки
    # ----------------------------------------------------
    def select_buns_tab(self):
        self._wait_overlay_disappear()
        tab = self.wait.until(EC.element_to_be_clickable(ConstructorPageLocators.TAB_BUNS))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", tab)
        self.driver.execute_script("arguments[0].click();", tab)
        self._wait_tab_active(ConstructorPageLocators.TAB_BUNS)

    # ----------------------------------------------------
    # Соусы
    # ----------------------------------------------------
    def select_sauces_tab(self):
        self._wait_overlay_disappear()
        tab = self.wait.until(EC.element_to_be_clickable(ConstructorPageLocators.TAB_SAUCES))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", tab)
        self.driver.execute_script("arguments[0].click();", tab)
        self._wait_tab_active(ConstructorPageLocators.TAB_SAUCES)

    # ----------------------------------------------------
    # Начинки
    # ----------------------------------------------------
    def select_fillings_tab(self):
        self._wait_overlay_disappear()
        tab = self.wait.until(EC.element_to_be_clickable(ConstructorPageLocators.TAB_FILLINGS))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", tab)
        self.driver.execute_script("arguments[0].click();", tab)
        self._wait_tab_active(ConstructorPageLocators.TAB_FILLINGS)

    # ----------------------------------------------------
    # Кнопка "Оформить заказ"
    # ----------------------------------------------------
    def click_order_button(self):
        self._wait_overlay_disappear()
        button = self.wait.until(EC.element_to_be_clickable(ConstructorPageLocators.ORDER_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)

    # ----------------------------------------------------
    # Проверка видимости любого элемента
    # ----------------------------------------------------
    def is_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
