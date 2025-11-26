# tests/test_order_creation.py v1.1

import allure

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


class TestOrderFeed:
    @allure.title('После создания заказа счётчик "Выполнено за всё время" увеличивается')
    @allure.description(
        "1. Авторизация пользователя\n"
        "2. Переход в ленту заказов\n"
        "3. Сохранение значения счётчика \"Выполнено за всё время\"\n"
        "4. Возврат в конструктор и создание заказа через UI\n"
        "5. Повторный переход в ленту заказов\n"
        "6. Проверка, что счётчик увеличился"
    )
    def test_new_order_increases_total_counter(self, driver, api_user):
        # Авторизация
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        login_page.submit_login()

        main_page = MainPage(driver)
        feed_page = OrderFeedPage(driver)

        # Переход в ленту заказов
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась."

        # Сохранение исходного значения счётчика
        initial_total = feed_page.get_total_orders_count()

        # Возврат на главную (конструктор) и создание заказа через UI
        main_page.click_constructor()
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Не удалось получить номер заказа."
        assert order_number != "9999", "Получен временный номер заказа 9999 вместо финального."

        # Снова переходим в ленту заказов через шапку
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась после оформления заказа."

        # Ожидание обновления счётчика
        assert feed_page.wait_for_counters_update(
            initial_total=initial_total,
            initial_today=None,
            timeout=20,
        ), 'Счётчик "Выполнено за всё время" не обновился после создания заказа.'

        # Контрольное сравнение
        new_total = feed_page.get_total_orders_count()
        assert new_total > initial_total, (
            f'Счётчик "Выполнено за всё время" не увеличился. '
            f"Было: {initial_total}, стало: {new_total}"
        )

    @allure.title('После создания заказа счётчик "Выполнено за сегодня" увеличивается')
    @allure.description(
        "1. Авторизация пользователя\n"
        "2. Переход в ленту заказов\n"
        "3. Сохранение значения счётчика \"Выполнено за сегодня\"\n"
        "4. Возврат в конструктор и создание заказа через UI\n"
        "5. Повторный переход в ленту заказов\n"
        "6. Проверка, что дневной счётчик увеличился"
    )
    def test_new_order_increases_today_counter(self, driver, api_user):
        # Авторизация
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        login_page.submit_login()

        main_page = MainPage(driver)
        feed_page = OrderFeedPage(driver)

        # Переход в ленту заказов
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась."

        # Сохранение исходного значения дневного счётчика
        initial_today = feed_page.get_today_orders_count()

        # Возврат на главную (конструктор) и создание заказа через UI
        main_page.click_constructor()
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Не удалось получить номер заказа."
        assert order_number != "9999", "Получен временный(ЗАГЛУШКА) номер заказа 9999 вместо финального."

        # Снова переходим в ленту заказов через шапку
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась после оформления заказа."

        # Ожидание обновления дневного счётчика
        assert feed_page.wait_for_counters_update(
            initial_total=None,
            initial_today=initial_today,
            timeout=20,
        ), 'Счётчик "Выполнено за сегодня" не обновился после создания заказа.'

        # Контрольное сравнение
        new_today = feed_page.get_today_orders_count()
        assert new_today > initial_today, (
            f'Счётчик "Выполнено за сегодня" не увеличился. '
            f"Было: {initial_today}, стало: {new_today}"
        )

    @allure.title('После оформления заказа его номер появляется в разделе "В работе"')
    @allure.description(
        "1. Авторизация пользователя\n"
        "2. Создание заказа через UI с главной страницы (конструктор)\n"
        "3. Переход в ленту заказов через шапку\n"
        "4. Проверка, что номер заказа присутствует в блоке \"В работе\""
    )
    def test_order_number_appears_in_in_progress_block(self, driver, api_user):
        # Авторизация
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        login_page.submit_login()

        main_page = MainPage(driver)
        feed_page = OrderFeedPage(driver)

        # На всякий случай активируем конструктор
        main_page.click_constructor()

        # Создание заказа через UI
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Не удалось получить номер заказа."
        assert order_number != "9999", "Получен временный номер заказа 9999 вместо финального."

        normalized_number = feed_page.normalize_order_number(order_number)

        # Переход в ленту заказов через шапку
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась."

        # Ожидание появления номера в блоке «В работе»
        assert feed_page.wait_for_order_in_progress(
            normalized_number,
            timeout=30,
        ), f"Заказ {normalized_number} не появился в блоке 'В работе'."

        # Дополнительная проверка
        in_progress_now = feed_page.get_orders_in_progress_normalized()
        assert normalized_number in in_progress_now, (
            f"Номер заказа {normalized_number} отсутствует в блоке 'В работе'. "
            f"Текущий список: {in_progress_now}"
        )
