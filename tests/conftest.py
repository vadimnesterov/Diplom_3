import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from data.urls import MAIN_PAGE
from helpers.user_api_helper import UserAPIHelper


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    """Запуск тестов в Chrome и Firefox."""
    browser = request.param

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        web_driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        options.set_preference("layout.css.devPixelsPerPx", "1.0")
        web_driver = webdriver.Firefox(options=options)
        web_driver.set_window_size(1920, 1080)
    else:
        raise ValueError(f"Неизвестный браузер: {browser}")

    web_driver.implicitly_wait(5)
    web_driver.get(MAIN_PAGE)

    yield web_driver

    web_driver.quit()


@pytest.fixture
def api_user():
    """
    Создаёт тестового пользователя через API.
    Возвращает словарь с полями name, password, email.
    """
    helper = UserAPIHelper()
    return helper.create_test_user()
