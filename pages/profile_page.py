from data.urls import PROFILE_PAGE
from locators.profile_page_locators import ProfilePageLocators
from .base_page import BasePage


class ProfilePage(BasePage):
    """Страница личного кабинета."""

    def open_profile(self):
        """Открыть страницу профиля по прямой ссылке."""
        self.open(PROFILE_PAGE)

    def is_profile_open(self) -> bool:
        """Проверить, что страница профиля открыта."""
        return self.is_visible(ProfilePageLocators.PROFILE_HEADER)

    def click_logout(self):
        """Нажать кнопку 'Выход'."""
        self.click(ProfilePageLocators.LOGOUT_BUTTON)
