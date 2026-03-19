from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.api.models.order import Order
from src.api.repositories.base import AbstractRepository


class OrderRepository(AbstractRepository[Order]):
    model = Order

    async def get_by_id_with_items(self, order_id: str) -> Order | None:
        query = select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_customer(self, customer_id: str) -> list[Order]:
        query = select(Order).where(Order.customer_id == customer_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_status(self, status: str) -> list[Order]:
        query = select(Order).where(Order.status == status)
        result = await self.session.execute(query)
        return list(result.scalars().all())
