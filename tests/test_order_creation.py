from pages.login_page import LoginPage
from pages.constructor_page import ConstructorPage
from pages.order_modal import OrderModal


class TestOrderCreation:
    """Тесты оформления заказа."""

    def test_create_order_authorized_user(self, driver, api_user):
        """
        Авторизованный пользователь может оформить заказ:
        открывается модальное окно с номером заказа.
        """
        # Логинимся
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(api_user["email"])
        login_page.set_password(api_user["password"])
        login_page.submit_login()

        # Переходим в конструктор (на всякий случай)
        constructor_page = ConstructorPage(driver)
        constructor_page.open_constructor()

        # Оформляем заказ
        constructor_page.click_order_button()

        order_modal = OrderModal(driver)
        assert order_modal.is_open()
        order_number = order_modal.get_order_number()
        assert order_number is not None
        assert order_number != ""

        order_modal.close()

    def test_create_order_unauthorized_user_redirects_to_login(self, driver):
        """
        Неавторизованный пользователь:
        при попытке оформить заказ происходит переход на страницу логина.
        """
        constructor_page = ConstructorPage(driver)
        constructor_page.open_constructor()

        constructor_page.click_order_button()

        assert "/login" in driver.current_url
