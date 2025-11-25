import pytest
import allure

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


@allure.suite("Smoke: эталонная логика ленты заказов")
@pytest.mark.xfail(reason="Эталонная логика для предварительной проверки", strict=False)
class TestOrderFeedEtalonSmoke:
    def _login_and_get_pages(self, driver, api_user):
        """Вспомогательный метод: логин + подготовка MainPage и OrderFeedPage."""
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        login_page.submit_login()

        main_page = MainPage(driver)
        feed_page = OrderFeedPage(driver)
        return main_page, feed_page

    @allure.title('Эталон: после создания заказа увеличивается "Выполнено за всё время"')
    @allure.description(
        "1. Логин\n"
        "2. Переход в ленту заказов\n"
        "3. Сохранение счётчика \"Выполнено за всё время\"\n"
        "4. Переход на конструктор\n"
        "5. Создание заказа через UI\n"
        "6. Снова переход в ленту заказов\n"
        "7. Ожидание и проверка увеличения счётчика"
    )
    def test_etalon_total_counter(self, driver, api_user):
        main_page, feed_page = self._login_and_get_pages(driver, api_user)

        # 1) Переход в ленту заказов
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась."

        # 2) Сохраняем исходный total
        initial_total = feed_page.get_total_orders_count()

        # 3) Возвращаемся на конструктор
        main_page.click_constructor()

        # 4) Создаём заказ через UI
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Не удалось получить номер заказа."
        assert order_number != "9999", "Получен временный номер заказа 9999."

        # 5) Снова идём в /feed
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась после оформления заказа."

        # 6) Ждём обновления счётчика (эталонная логика)
        assert feed_page.wait_for_counters_update(
            initial_total=initial_total,
            initial_today=None,
            timeout=20,
        ), 'Счётчик "Выполнено за всё время" не обновился после создания заказа.'

        # 7) Контрольное сравнение
        new_total = feed_page.get_total_orders_count()
        assert new_total > initial_total, (
            f'Счётчик "Выполнено за всё время" не увеличился. '
            f"Было: {initial_total}, стало: {new_total}"
        )

    @allure.title('Эталон: после создания заказа увеличивается "Выполнено за сегодня"')
    @allure.description(
        "1. Логин\n"
        "2. Переход в ленту заказов\n"
        "3. Сохранение счётчика \"Выполнено за сегодня\"\n"
        "4. Переход на конструктор\n"
        "5. Создание заказа через UI\n"
        "6. Снова переход в ленту заказов\n"
        "7. Ожидание и проверка увеличения дневного счётчика"
    )
    def test_etalon_today_counter(self, driver, api_user):
        main_page, feed_page = self._login_and_get_pages(driver, api_user)

        # 1) Переход в ленту заказов
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась."

        # 2) Сохраняем исходный today
        initial_today = feed_page.get_today_orders_count()

        # 3) Возвращаемся на конструктор
        main_page.click_constructor()

        # 4) Создаём заказ через UI
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Не удалось получить номер заказа."
        assert order_number != "9999", "Получен временный номер заказа 9999."

        # 5) Снова идём в /feed
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась после оформления заказа."

        # 6) Ждём обновления дневного счётчика
        assert feed_page.wait_for_counters_update(
            initial_total=None,
            initial_today=initial_today,
            timeout=20,
        ), 'Счётчик "Выполнено за сегодня" не обновился после создания заказа.'

        # 7) Контрольное сравнение
        new_today = feed_page.get_today_orders_count()
        assert new_today > initial_today, (
            f'Счётчик "Выполнено за сегодня" не увеличился. '
            f"Было: {initial_today}, стало: {new_today}"
        )

    @allure.title('Эталон: номер заказа появляется в блоке "В работе"')
    @allure.description(
        "1. Логин\n"
        "2. Переход в ленту заказов\n"
        "3. Переход на конструктор\n"
        "4. Создание заказа через UI\n"
        "5. Снова переход в ленту заказов\n"
        "6. Ожидание появления номера в блоке «В работе»"
    )
    def test_etalon_order_in_progress(self, driver, api_user):
        main_page, feed_page = self._login_and_get_pages(driver, api_user)

        # 1) Сначала просто убеждаемся, что /feed открывается
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась."

        # 2) Возвращаемся на конструктор
        main_page.click_constructor()

        # 3) Создаём заказ через UI
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Не удалось получить номер заказа."
        assert order_number != "9999", "Получен временный номер заказа 9999."

        # 4) Нормализуем номер (как в эталоне)
        normalized_number = feed_page.normalize_order_number(order_number)

        # 5) Снова идём в /feed
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась после оформления заказа."

        # 6) Ждём, пока заказ появится в блоке «В работе»
        assert feed_page.wait_for_order_in_progress(
            normalized_number,
            timeout=30,
        ), f"Заказ {normalized_number} не появился в блоке 'В работе'."

        # Дополнительная проверка: номер есть в текущем списке
        in_progress_now = feed_page.get_orders_in_progress_normalized()
        assert normalized_number in in_progress_now, (
            f"Номер заказа {normalized_number} отсутствует в блоке 'В работе'. "
            f"Текущий список: {in_progress_now}"
        )
