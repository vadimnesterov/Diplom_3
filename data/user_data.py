from data.urls import Endpoints


class UserAPIData:
    """Endpoint tuples (URL, HTTP method) for user API calls."""

    # Create a new user
    USER_CREATE_URL = (
        Endpoints.CREATE_USER,
        "post",
    )

    # Authenticate user
    USER_LOGIN_URL = (
        Endpoints.LOGIN,
        "post",
    )

    # Delete user account
    USER_DELETE_URL = (
        Endpoints.DELETE_USER,
        "delete",
    )
