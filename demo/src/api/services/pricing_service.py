from src.api.models.product import Product


def calculate_item_price(product: Product, quantity: int) -> float:
    """Calculate price for a line item, applying bulk discounts."""
    base = product.price * quantity
    if quantity >= 100:
        return base * 0.85  # 15% discount
    if quantity >= 50:
        return base * 0.90  # 10% discount
    if quantity >= 10:
        return base * 0.95  # 5% discount
    return base


def calculate_order_total(items: list[tuple[Product, int]]) -> float:
    """Calculate total for all items in an order."""
    return sum(calculate_item_price(product, qty) for product, qty in items)
