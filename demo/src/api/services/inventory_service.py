from sqlalchemy.ext.asyncio import AsyncSession

from src.api.events import bus
from src.api.events.types import StockLow
from src.api.exceptions.business import InsufficientStock
from src.api.models.product import Product


async def reserve_stock(session: AsyncSession, product: Product, quantity: int) -> None:
    if product.stock < quantity:
        raise InsufficientStock(product.id, quantity, product.stock)
    product.stock -= quantity
    await session.flush()
    if product.stock <= 5:
        bus.publish(StockLow(product_id=product.id, current_stock=product.stock))


async def release_stock(session: AsyncSession, product: Product, quantity: int) -> None:
    product.stock += quantity
    await session.flush()
