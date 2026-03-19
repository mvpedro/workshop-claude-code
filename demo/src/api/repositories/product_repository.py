from sqlalchemy import select

from src.api.models.product import Product
from src.api.repositories.base import AbstractRepository


class ProductRepository(AbstractRepository[Product]):
    model = Product

    async def filter_by_category(self, category: str) -> list[Product]:
        query = select(Product).where(Product.category == category)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_low_stock(self, threshold: int = 5) -> list[Product]:
        query = select(Product).where(Product.stock <= threshold)
        result = await self.session.execute(query)
        return list(result.scalars().all())
