# tests/test_main_page_functionality.py v1.1

import allure

from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from data.urls import URLS


@allure.epic("Основная функциональность")
@allure.feature("Главная страница")
class TestMainPageFunctionality:
    """Проверки основной функциональности главной страницы."""

    @allure.title('Переход по клику на «Конструктор»')
    @allure.description('''
        Проверка перехода по клику на «Конструктор»:
        1. Открыть главную страницу
        2. Перейти в «Ленту заказов»
        3. Вернуться на главную по клику на «Конструктор»
        4. Проверить, что пользователь не находится в ленте заказов
        ''')
    def test_go_to_constructor_from_header(self, driver):
        """Переход по клику на «Конструктор»."""
        main = MainPage(driver)
        main.open()  # открываем главную

        # Уходим в ленту заказов, чтобы точно не быть на /
        main.click_order_feed()
        main.wait_for_url_contains(URLS.url_feed)
        assert main.is_url_contains(URLS.url_feed)

        # Возвращаемся кликом по «Конструктор»
        main.click_constructor()
        main.wait_for_url_contains("/")  # ждём возврат на главную
        assert not main.is_url_contains(URLS.url_feed)

    @allure.title('Переход по клику на раздел «Лента заказов»')
    @allure.description('''
        Проверка перехода по клику на раздел «Лента заказов»:
        1. Открыть главную страницу
        2. Кликнуть по разделу «Лента заказов»
        3. Проверить, что страница ленты заказов загрузилась
        ''')
    def test_go_to_order_feed_from_header(self, driver):
        """Переход по клику на «Лента заказов»."""
        main = MainPage(driver)
        main.open()

        main.click_order_feed()

        feed = OrderFeedPage(driver)
        assert feed.is_order_feed_page_loaded()

    @allure.title('Если кликнуть на ингредиент, появится всплывающее окно с деталями')
    @allure.description('''
        Проверка открытия всплывающего окна с деталями ингредиента:
        1. Открыть главную страницу
        2. Кликнуть на ингредиент
        3. Проверить, что модальное окно с деталями открылось
        ''')
    def test_ingredient_modal_opens_on_click(self, driver):
        """Если кликнуть на ингредиент, появляется модальное окно с деталями."""
        main = MainPage(driver)
        main.open()

        main.click_ingredient()
        assert main.is_ingredient_modal_visible()

    @allure.title('При добавлении ингредиента в заказ счётчик этого ингредиента увеличивается')
    @allure.description('''
        Проверка увеличения счётчика ингредиента:
        1. Открыть главную страницу
        2. Запомнить текущее значение счётчика ингредиента
        3. Перетащить ингредиент в область конструктора
        4. Проверить, что значение счётчика увеличилось
        ''')
    def test_ingredient_counter_increases_after_drag(self, driver):
        """При добавлении ингредиента в заказ счётчик этого ингредиента увеличивается."""
        main = MainPage(driver)
        main.open()

        before = main.get_ingredient_counter()
        main.drag_ingredient_to_constructor()
        after = main.get_ingredient_counter()

        assert after > before
