from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models.customer import Customer
from src.api.models.order import Order
from src.api.models.order_item import OrderItem


async def get_top_products(session: AsyncSession, limit: int = 10) -> list[dict]:
    query = (
        select(
            OrderItem.product_id,
            func.sum(OrderItem.quantity).label("total_sold"),
            func.sum(OrderItem.unit_price * OrderItem.quantity).label("total_revenue"),
        )
        .group_by(OrderItem.product_id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(limit)
    )
    result = await session.execute(query)
    return [
        {"product_id": row.product_id, "total_sold": row.total_sold, "total_revenue": row.total_revenue}
        for row in result.all()
    ]


async def get_revenue_by_period(session: AsyncSession, group_by: str = "month") -> list[dict]:
    query = (
        select(
            func.strftime("%Y-%m", Order.created_at).label("period"),
            func.sum(Order.total).label("revenue"),
            func.count(Order.id).label("order_count"),
        )
        .where(Order.status != "cancelled")
        .group_by("period")
        .order_by("period")
    )
    result = await session.execute(query)
    return [
        {"period": row.period, "revenue": row.revenue, "order_count": row.order_count}
        for row in result.all()
    ]


async def get_customer_lifetime_value(session: AsyncSession, customer_id: str) -> dict:
    query = (
        select(
            func.count(Order.id).label("order_count"),
            func.sum(Order.total).label("total_spent"),
            func.min(Order.created_at).label("first_order"),
            func.max(Order.created_at).label("last_order"),
        )
        .where(Order.customer_id == customer_id, Order.status != "cancelled")
    )
    result = await session.execute(query)
    row = result.one()
    return {
        "customer_id": customer_id,
        "order_count": row.order_count or 0,
        "total_spent": row.total_spent or 0.0,
        "first_order": str(row.first_order) if row.first_order else None,
        "last_order": str(row.last_order) if row.last_order else None,
    }
