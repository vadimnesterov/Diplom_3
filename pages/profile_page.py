from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from locators.profile_page_locators import ProfilePageLocators


class ProfilePage(BasePage):
    """Страница профиля авторизованного пользователя."""

    def is_profile_open(self) -> bool:
        """Проверить, что открыта страница профиля."""

        # 1. Ждём, что мы на URL профиля
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/account/profile")
            )
        except TimeoutException:
            return False

        # 2. Кнопка «Выход» есть только на странице профиля
        return self.is_visible(ProfilePageLocators.LOGOUT_BUTTON)
