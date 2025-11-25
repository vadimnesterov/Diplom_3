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
    # Открытие конструктора (главной страницы)
    # ----------------------------------------------------
    def open_constructor(self):
        """
        Открывает главную страницу с конструктором бургера.
        Открываем MAIN_PAGE и ждём заголовок.
        """
        self.driver.get(MAIN_PAGE)
        self.wait.until(
            EC.visibility_of_element_located(ConstructorPageLocators.PAGE_HEADER)
        )

    # ----------------------------------------------------
    # Вкладки: Булки / Соусы / Начинки
    # (переключаем вкладку и проверяем класс активной)
    # ----------------------------------------------------
    def _wait_tab_active(self, locator):
        """
        Ожидает, что у вкладки появится класс "tab_tab_type_current",

        """
        self.wait.until(
            lambda d: "tab_tab_type_current"
            in d.find_element(*locator).get_attribute("class")
        )

    def select_buns_tab(self):
        tab = self.wait.until(
            EC.element_to_be_clickable(ConstructorPageLocators.TAB_BUNS)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", tab)
        self.driver.execute_script("arguments[0].click();", tab)
        self._wait_tab_active(ConstructorPageLocators.TAB_BUNS)

    def select_sauces_tab(self):
        tab = self.wait.until(
            EC.element_to_be_clickable(ConstructorPageLocators.TAB_SAUCES)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", tab)
        self.driver.execute_script("arguments[0].click();", tab)
        self._wait_tab_active(ConstructorPageLocators.TAB_SAUCES)

    def select_fillings_tab(self):
        tab = self.wait.until(
            EC.element_to_be_clickable(ConstructorPageLocators.TAB_FILLINGS)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", tab)
        self.driver.execute_script("arguments[0].click();", tab)
        self._wait_tab_active(ConstructorPageLocators.TAB_FILLINGS)

    # ----------------------------------------------------
    # Сборка простого бургера (как в Diplom_3: dnd + конструктор)
    # ----------------------------------------------------
    def build_burger_with_one_bun(self):
        """
        Минимальная сборка бургера для сценариев оформления заказа.

        Логика:
        - переходим на вкладку "Булки";
        - берём первый доступный ингредиент из списка;
        - перетаскиваем его в область конструктора через JS drag&drop.
        """
        # На всякий случай переключаемся на "Булки"
        try:
            self.select_buns_tab()
        except Exception:
            # Если вкладка не переключилась — продолжаем, список обычно и так виден
            pass

        # Ищем первый ингредиент в блоке ингредиентов
        ingredient = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//section[contains(@class,'BurgerIngredients')]"
                    "//*[self::li or self::a or self::div][1]",
                )
            )
        )

        # Ищем область конструктора, куда кидаем ингредиент
        constructor_drop_area = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//main//section[contains(@class,'BurgerConstructor')]"
                    "//*[contains(@class,'BurgerConstructor_basket') "
                    "or contains(@class,'burger-element_pos_top') "
                    "or name()='ul']",
                )
            )
        )

        self._drag_and_drop(ingredient, constructor_drop_area)

    def _drag_and_drop(self, source_element, target_element):
        """
        JS drag&drop — логика такая же, как в BasePage Diplom_3.
        """
        self.driver.execute_script(
            """
            function createEvent(typeOfEvent) {
                var event = document.createEvent('CustomEvent');
                event.initCustomEvent(typeOfEvent, true, true, null);
                event.dataTransfer = {
                    data: {},
                    setData: function (key, value) {
                        this.data[key] = value;
                    },
                    getData: function (key) {
                        return this.data[key];
                    }
                };
                return event;
            }

            function dispatchEvent(element, event, transferData) {
                if (transferData !== undefined) {
                    event.dataTransfer = transferData;
                }
                if (element.dispatchEvent) {
                    element.dispatchEvent(event);
                } else if (element.fireEvent) {
                    element.fireEvent('on' + event.type, event);
                }
            }

            var source = arguments[0];
            var target = arguments[1];

            var dragStartEvent = createEvent('dragstart');
            dispatchEvent(source, dragStartEvent);

            var dragEnterEvent = createEvent('dragenter');
            dispatchEvent(target, dragEnterEvent, dragStartEvent.dataTransfer);

            var dragOverEvent = createEvent('dragover');
            dispatchEvent(target, dragOverEvent, dragStartEvent.dataTransfer);

            var dropEvent = createEvent('drop');
            dispatchEvent(target, dropEvent, dragStartEvent.dataTransfer);

            var dragEndEvent = createEvent('dragend');
            dispatchEvent(source, dragEndEvent, dragStartEvent.dataTransfer);
            """,
            source_element,
            target_element,
        )

    # ----------------------------------------------------
    # Кнопка "Оформить заказ"
    # ----------------------------------------------------
    def click_order_button(self):
        """
        Ждём кликабельность кнопки и кликаем по ней.
        Никаких оверлеев, только ожидание кнопки и клик.
        """
        button = self.wait.until(
            EC.element_to_be_clickable(ConstructorPageLocators.ORDER_BUTTON)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        self.driver.execute_script("arguments[0].click();", button)
