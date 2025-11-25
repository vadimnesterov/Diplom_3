import pytest
import allure

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


@allure.suite("Debug / Smoke: заказ в блоке «В работе»")
@pytest.mark.xfail(reason="Временный отладочный тест, может быть нестабильен", strict=False)
class TestOrderInProgressSmoke:

    @allure.title("Номер созданного заказа появляется в блоке «В работе» (упрощённый сценарий)")
    @allure.description(
        "1. Авторизация пользователя\n"
        "2. Создание заказа через UI с главной страницы\n"
        "3. Переход в ленту заказов через шапку\n"
        "4. Ожидание появления номера заказа в блоке «В работе»"
    )
    def test_order_number_appears_in_in_progress_block_simplified(self, driver, api_user):
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

        # Создаем заказ через UI
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Не удалось получить номер заказа."
        assert order_number != "9999", "Получен временный номер заказа 9999."

        # Нормализуем номер (как в эталоне)
        normalized_order_number = feed_page.normalize_order_number(order_number)

        # Переходим в ленту заказов через шапку
        main_page.click_order_feed()
        assert feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась."

        # Ждём, пока заказ появится в разделе «В работе»
        assert feed_page.wait_for_order_in_progress(
            normalized_order_number
        ), f"Заказ {order_number} не появился в разделе 'В работе'."

        # Дополнительная проверка: номер есть в текущем списке
        orders_in_progress_normalized = feed_page.get_orders_in_progress_normalized()
        assert normalized_order_number in orders_in_progress_normalized, (
            f"Заказ {order_number} (нормализованный: {normalized_order_number}) "
            f"не найден в разделе 'В работе'. "
            f"Текущие заказы: {orders_in_progress_normalized}"
        )
