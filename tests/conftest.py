# conftest.py
# version: v1.2

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from helpers.user_api_helper import UserAPIHelper



# Фикстура WebDriver с параметризацией по браузерам (Chrome, Firefox)


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    yield driver

    driver.quit()



# Фикстура для создания тестового пользователя через API


@pytest.fixture
def api_user():
    """
    Фикстура:
    1) Создаёт пользователя через API
    2) Логинится
    3) Возвращает данные + токен
    4) После теста удаляет пользователя
    """
    helper = UserAPIHelper()

    user_data = helper.create_test_user()
    login_response = helper.login_user_request(user_data)

    access_token = login_response.json().get("accessToken")
    assert access_token, "Токен авторизации не получен"

    yield {
        "email": user_data["email"],
        "password": user_data["password"],
        "access_token": access_token,
    }

    helper.delete_user(access_token)
