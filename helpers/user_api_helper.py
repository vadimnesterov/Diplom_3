import logging

import requests
from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout

from data.user_data import UserAPIData
from .common_api_helper import CommonApiHelper

logger = logging.getLogger(__name__)

# Network-level exceptions that indicate the backend is unreachable.
# Used in safe_delete_user() (teardown) and imported by conftest for setup.
# HTTP-level errors (4xx / 5xx) are intentionally excluded — those are
# application logic failures and must propagate as test failures.
NETWORK_EXCEPTIONS = (ConnectTimeout, ConnectionError, ReadTimeout)


class UserAPIHelper(CommonApiHelper):
    """API client for user management: registration, login, and deletion."""

    def create_user_request(self, data: dict) -> requests.Response:
        url, method = UserAPIData.USER_CREATE_URL
        return requests.request(
            url=url,
            method=method,
            json=data,
        )

    def login_user_request(self, data: dict) -> requests.Response:
        url, method = UserAPIData.USER_LOGIN_URL
        return requests.request(
            url=url,
            method=method,
            json=data,
        )

    def delete_user_request(self, token: str) -> requests.Response:
        url, method = UserAPIData.USER_DELETE_URL
        headers = {"Authorization": token}
        return requests.request(
            url=url,
            method=method,
            headers=headers,
        )

    def build_user_payload(self) -> dict:
        name = self.make_random_string(23)
        password = self.make_random_string(23)
        email = (
            f"{self.make_random_string(15)}@"
            f"{self.make_random_string(15)}notexists.com"
        )

        return {
            "name": name,
            "password": password,
            "email": email,
        }

    def create_test_user(self) -> dict:
        user_data = self.build_user_payload()
        response = self.create_user_request(user_data)

        assert response.status_code == 200, (
            f"User creation failed. Status: {response.status_code}, body: {response.text}"
        )

        return user_data

    def delete_user(self, token: str):
        response = self.delete_user_request(token)
        assert response.status_code in (200, 202), (
            f"User deletion failed. Status: {response.status_code}, body: {response.text}"
        )

    def safe_delete_user(self, token: str):
        """Delete the test user, suppressing network-level failures with a warning.

        HTTP-level errors (e.g. 401 wrong token) are not caught and will
        propagate — those indicate a logic bug, not an infrastructure failure.
        """
        try:
            self.delete_user(token)
        except NETWORK_EXCEPTIONS as exc:
            logger.warning(
                "Backend unavailable during teardown — test user may not have been deleted: %s",
                exc,
            )
