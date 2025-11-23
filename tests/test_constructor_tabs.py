from pages.constructor_page import ConstructorPage
from locators.constructor_page_locators import ConstructorPageLocators


class TestConstructorTabs:
    """Тесты вкладок конструктора бургеров."""

    def test_buns_tab_active_by_default(self, driver):
        """
        Вкладка 'Булки' активна по умолчанию при открытии конструктора.
        """
        page = ConstructorPage(driver)
        page.open_constructor()

        buns_tab = driver.find_element(*ConstructorPageLocators.TAB_BUNS)
        classes = buns_tab.get_attribute("class")

        assert "tab_tab_type_current" in classes

    def test_switch_to_sauces_tab(self, driver):
        """
        Переключение на вкладку 'Соусы'.
        """
        page = ConstructorPage(driver)
        page.open_constructor()
        page.select_sauces_tab()

        sauces_tab = driver.find_element(*ConstructorPageLocators.TAB_SAUCES)
        classes = sauces_tab.get_attribute("class")

        assert "tab_tab_type_current" in classes

    def test_switch_to_fillings_tab(self, driver):
        """
        Переключение на вкладку 'Начинки'.
        """
        page = ConstructorPage(driver)
        page.open_constructor()
        page.select_fillings_tab()

        fillings_tab = driver.find_element(*ConstructorPageLocators.TAB_FILLINGS)
        classes = fillings_tab.get_attribute("class")

        assert "tab_tab_type_current" in classes
