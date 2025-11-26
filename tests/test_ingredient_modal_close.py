import allure

from pages.main_page import MainPage


class TestIngredientModal:

    @allure.title("Модальное окно ингредиента закрывается по крестику")
    @allure.description(
        "1. Открыть главную страницу\n"
        "2. Кликнуть по ингредиенту\n"
        "3. Убедиться, что модалка открылась\n"
        "4. Закрыть модалку по крестику\n"
        "5. Убедиться, что модалка закрыта"
    )
    def test_ingredient_modal_closes_by_cross(self, driver):
        main_page = MainPage(driver)

        # Открываем главную страницу
        main_page.open()

        # Кликаем по ингредиенту
        main_page.click_ingredient()

        # Проверяем, что модалка открылась
        assert main_page.is_ingredient_modal_visible(), "Модалка ингредиента не открылась"

        # Закрываем модалку по крестику
        main_page.close_ingredient_modal()

        # Проверяем, что модалка закрылась
        assert main_page.is_ingredient_modal_closed(), "Модалка ингредиента не закрылась по крестику"
