import random
import string




class CommonApiHelper:
    """Базовый помощник для API."""

    def make_random_string(self, length: int = 10) -> str:
        """Возвращает случайную строку из строчных латинских букв."""
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(length))
