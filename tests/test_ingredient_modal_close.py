import pytest
import allure

from pages.main_page import MainPage


class TestIngredientModal:

    @allure.title("Закрытие модального окна ингредиента по крестику")
    @allure.description(
        "1. Открыть главную страницу\n"
        "2. Кликнуть по ингредиенту\n"
        "3. Убедиться, что модальное окно открылось\n"
        "4. Закрыть модальное окно по крестику\n"
        "5. Убедиться, что модальное окно закрыто"
    )
    def test_ingredient_modal_closes_by_cross(self, driver):
        main_page = MainPage(driver)

        # Открываем главную страницу
        main_page.open()

        # Кликаем по ингредиенту
        main_page.click_ingredient()

        # Проверяем, что модальное окно открылась
        assert main_page.is_ingredient_modal_visible(), "Модальное окно ингредиента не открылась"

        # Закрываем модальное окно по крестику
        main_page.close_ingredient_modal()

        # Проверяем, что модальное окно закрылось
        assert main_page.is_ingredient_modal_closed(), "Модальное окно ингредиента не закрылась по крестику"
