from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database import get_session
from src.api.exceptions.business import NotFound
from src.api.repositories.order_repository import OrderRepository
from src.api.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from src.api.schemas.pagination import PaginatedResponse
from src.api.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=PaginatedResponse[OrderResponse])
async def list_orders(
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    customer_id: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    repo = OrderRepository(session)
    filters = {}
    if status:
        filters["status"] = status
    if customer_id:
        filters["customer_id"] = customer_id
    total = await repo.count(**filters)
    items = await repo.list(offset=(page - 1) * page_size, limit=page_size, **filters)
    return PaginatedResponse(
        items=items, total=total, page=page, page_size=page_size,
        pages=(total + page_size - 1) // page_size if total > 0 else 0,
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, session: AsyncSession = Depends(get_session)):
    repo = OrderRepository(session)
    order = await repo.get_by_id_with_items(order_id)
    if order is None:
        raise NotFound("Pedido", order_id)
    return order


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(data: OrderCreate, session: AsyncSession = Depends(get_session)):
    order = await order_service.create_order(session, data)
    await session.commit()
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str, data: OrderStatusUpdate, session: AsyncSession = Depends(get_session)
):
    order = await order_service.transition_status(session, order_id, data.status)
    await session.commit()
    return order
