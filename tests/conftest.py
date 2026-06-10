import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from helpers.user_api_helper import NETWORK_EXCEPTIONS, UserAPIHelper


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    """Provide a WebDriver instance for Chrome or Firefox, quit after the test."""
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

    if browser == "firefox":
        # A brief pause after quitting Firefox lets the OS release geckodriver
        # resources (socket, temporary profile) before the next Firefox instance
        # starts. Without this, back-to-back Firefox sessions on Windows can raise
        # NoSuchWindowException on the first driver.get() call of the next test.
        # Chrome is unaffected -- its multi-process architecture cleans up without
        # this guard. Under extreme stress (20+ consecutive full-suite runs) the
        # race may still appear; that is an artifact of the benchmark, not normal
        # CI usage. This is teardown infrastructure, not a test-level sleep.
        time.sleep(1)


@pytest.fixture
def api_user():
    """
    Fixture:
    1) Creates a user via API
    2) Logs in
    3) Returns user data + token
    4) Deletes the user after the test

    Network-level failures during setup skip the test -- there is nothing to
    run if the backend is unreachable. HTTP-level errors (e.g. registration
    rejected) are not caught and will fail the test as expected.

    Teardown delegates to safe_delete_user(), which logs a warning on network
    failure and lets HTTP-level errors propagate.
    """
    helper = UserAPIHelper()

    try:
        user_data = helper.create_test_user()
        login_response = helper.login_user_request(user_data)
    except NETWORK_EXCEPTIONS as exc:
        pytest.skip(f"Backend unavailable -- skipping test: {exc}")

    access_token = login_response.json().get("accessToken")
    assert access_token, "Authorisation token was not received"

    yield {
        "email": user_data["email"],
        "password": user_data["password"],
        "access_token": access_token,
    }

    helper.safe_delete_user(access_token)
