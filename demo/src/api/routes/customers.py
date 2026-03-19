from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database import get_session
from src.api.exceptions.business import DuplicateEmail, NotFound
from src.api.repositories.customer_repository import CustomerRepository
from src.api.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from src.api.schemas.pagination import PaginatedResponse

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=PaginatedResponse[CustomerResponse])
async def list_customers(
    page: int = 1,
    page_size: int = 20,
    segment: str | None = None,
    is_active: bool | None = None,
    session: AsyncSession = Depends(get_session),
):
    repo = CustomerRepository(session)
    filters = {}
    if segment:
        filters["segment"] = segment
    if is_active is not None:
        filters["is_active"] = is_active
    total = await repo.count(**filters)
    items = await repo.list(offset=(page - 1) * page_size, limit=page_size, **filters)
    return PaginatedResponse(
        items=items, total=total, page=page, page_size=page_size,
        pages=(total + page_size - 1) // page_size if total > 0 else 0,
    )


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str, session: AsyncSession = Depends(get_session)):
    repo = CustomerRepository(session)
    customer = await repo.get_by_id(customer_id)
    if customer is None:
        raise NotFound("Cliente", customer_id)
    return customer


@router.post("", response_model=CustomerResponse, status_code=201)
async def create_customer(data: CustomerCreate, session: AsyncSession = Depends(get_session)):
    repo = CustomerRepository(session)
    existing = await repo.search_by_email(data.email)
    if existing:
        raise DuplicateEmail(data.email)
    customer = await repo.create(**data.model_dump())
    await session.commit()
    return customer


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str, data: CustomerUpdate, session: AsyncSession = Depends(get_session)
):
    repo = CustomerRepository(session)
    customer = await repo.update(customer_id, **data.model_dump(exclude_unset=True))
    if customer is None:
        raise NotFound("Cliente", customer_id)
    await session.commit()
    return customer


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(customer_id: str, session: AsyncSession = Depends(get_session)):
    repo = CustomerRepository(session)
    deleted = await repo.delete(customer_id)
    if not deleted:
        raise NotFound("Cliente", customer_id)
    await session.commit()
