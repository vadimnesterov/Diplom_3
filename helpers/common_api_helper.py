import random
import string


class CommonApiHelper:
    """Base API helper."""

    def make_random_string(self, length: int = 10) -> str:
        """Return a random lowercase ASCII string of the given length."""
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(length))
