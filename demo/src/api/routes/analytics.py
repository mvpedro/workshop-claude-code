from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database import get_session
from src.api.services import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/top-products")
async def top_products(limit: int = 10, session: AsyncSession = Depends(get_session)):
    return await analytics_service.get_top_products(session, limit)


@router.get("/revenue")
async def revenue_by_period(group_by: str = "month", session: AsyncSession = Depends(get_session)):
    return await analytics_service.get_revenue_by_period(session, group_by)


@router.get("/customer-ltv/{customer_id}")
async def customer_ltv(customer_id: str, session: AsyncSession = Depends(get_session)):
    return await analytics_service.get_customer_lifetime_value(session, customer_id)
