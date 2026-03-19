from sqlalchemy import select

from src.api.models.customer import Customer
from src.api.repositories.base import AbstractRepository


class CustomerRepository(AbstractRepository[Customer]):
    model = Customer

    async def search_by_email(self, email: str) -> Customer | None:
        query = select(Customer).where(Customer.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_segment(self, segment: str) -> list[Customer]:
        query = select(Customer).where(Customer.segment == segment)
        result = await self.session.execute(query)
        return list(result.scalars().all())
