from data.user_data import TEST_USER_EMAIL, TEST_USER_PASSWORD
from pages.login_page import LoginPage
from pages.constructor_page import ConstructorPage
from pages.order_modal import OrderModal
from locators.constructor_page_locators import ConstructorPageLocators


class TestOrderCreation:
    """Тесты оформления заказа."""

    def test_create_order_authorized_user(self, driver):
        """
        Авторизованный пользователь может оформить заказ:
        открывается модальная страница с номером заказа.
        """
        # Логинимся
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.set_email(TEST_USER_EMAIL)
        login_page.set_password(TEST_USER_PASSWORD)
        login_page.submit_login()

        # Переходим в конструктор (на всякий случай)
        constructor_page = ConstructorPage(driver)
        constructor_page.open_constructor()

        # Нажимаем 'Оформить заказ'
        constructor_page.click_order_button()

        # Проверяем модальную страницу заказа
        order_modal = OrderModal(driver)
        assert order_modal.is_open()

        order_number = order_modal.get_order_number()
        assert order_number is not None
        assert len(order_number.strip()) > 0

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
