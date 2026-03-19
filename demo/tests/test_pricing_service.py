from unittest.mock import MagicMock
from src.api.services.pricing_service import calculate_item_price, calculate_order_total


def test_no_discount_under_10():
    product = MagicMock(price=1000)
    assert calculate_item_price(product, 5) == 5000


def test_5_percent_discount_at_10():
    product = MagicMock(price=1000)
    assert calculate_item_price(product, 10) == 9500


def test_10_percent_discount_at_50():
    product = MagicMock(price=1000)
    assert calculate_item_price(product, 50) == 45000


def test_15_percent_discount_at_100():
    product = MagicMock(price=1000)
    assert calculate_item_price(product, 100) == 85000


def test_calculate_order_total():
    p1 = MagicMock(price=1000)
    p2 = MagicMock(price=500)
    total = calculate_order_total([(p1, 5), (p2, 10)])
    assert total == 5000 + 4750
