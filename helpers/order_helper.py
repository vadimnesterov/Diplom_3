# helpers/order_helper.py
# version: v1.1


def normalize_order_number(order_number: str) -> str:
    """
    Нормализует номер заказа:
    - оставляет только цифры;
    - убирает ведущие нули.

    Используется для:
    - UI (лента заказов)
    - API
    - сравнений между системами
    """
    if not order_number:
        return ""

    digits = "".join(ch for ch in order_number if ch.isdigit())
    return digits.lstrip("0")
