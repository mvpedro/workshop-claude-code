import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.events import bus
from src.api.events.types import StockLow
from src.api.exceptions.business import InsufficientStock
from src.api.models.product import Product
from src.api.services.inventory_service import reserve_stock, release_stock


async def test_reserve_stock_success(session: AsyncSession):
    product = Product(name="Test Product", price=100.0, stock=10, category="test", sku="TEST-001")
    session.add(product)
    await session.flush()

    await reserve_stock(session, product, 3)
    assert product.stock == 7


async def test_reserve_stock_insufficient(session: AsyncSession):
    product = Product(name="Low Stock", price=100.0, stock=2, category="test", sku="TEST-002")
    session.add(product)
    await session.flush()

    with pytest.raises(InsufficientStock):
        await reserve_stock(session, product, 5)


async def test_reserve_stock_emits_low_stock_event(session: AsyncSession):
    product = Product(name="Almost Low", price=100.0, stock=7, category="test", sku="TEST-003")
    session.add(product)
    await session.flush()

    received_events = []
    bus.subscribe(StockLow, lambda e: received_events.append(e))

    # Reserve 3 units: stock goes from 7 to 4, which is <= threshold of 5
    await reserve_stock(session, product, 3)

    assert product.stock == 4
    assert len(received_events) == 1
    assert isinstance(received_events[0], StockLow)
    assert received_events[0].current_stock == 4


async def test_release_stock(session: AsyncSession):
    product = Product(name="Release Test", price=100.0, stock=5, category="test", sku="TEST-004")
    session.add(product)
    await session.flush()

    await release_stock(session, product, 3)
    assert product.stock == 8
