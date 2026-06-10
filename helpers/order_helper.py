def normalize_order_number(order_number: str) -> str:
    """
    Normalize an order number string:
    - keeps digits only;
    - strips leading zeros.

    Used for: UI (order feed), API responses, cross-system comparisons.
    """
    if not order_number:
        return ""

    digits = "".join(ch for ch in order_number if ch.isdigit())
    return digits.lstrip("0")
