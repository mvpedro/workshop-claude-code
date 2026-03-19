from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database import get_session
from src.api.exceptions.business import NotFound
from src.api.repositories.product_repository import ProductRepository
from src.api.schemas.pagination import PaginatedResponse
from src.api.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=PaginatedResponse[ProductResponse])
async def list_products(
    page: int = 1,
    page_size: int = 20,
    category: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    repo = ProductRepository(session)
    filters = {}
    if category:
        filters["category"] = category
    total = await repo.count(**filters)
    items = await repo.list(offset=(page - 1) * page_size, limit=page_size, **filters)
    return PaginatedResponse(
        items=items, total=total, page=page, page_size=page_size,
        pages=(total + page_size - 1) // page_size if total > 0 else 0,
    )


@router.get("/low-stock", response_model=list[ProductResponse])
async def low_stock_products(session: AsyncSession = Depends(get_session)):
    repo = ProductRepository(session)
    return await repo.get_low_stock()


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, session: AsyncSession = Depends(get_session)):
    repo = ProductRepository(session)
    product = await repo.get_by_id(product_id)
    if product is None:
        raise NotFound("Produto", product_id)
    return product


@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(data: ProductCreate, session: AsyncSession = Depends(get_session)):
    repo = ProductRepository(session)
    product = await repo.create(**data.model_dump())
    await session.commit()
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str, data: ProductUpdate, session: AsyncSession = Depends(get_session)
):
    repo = ProductRepository(session)
    product = await repo.update(product_id, **data.model_dump(exclude_unset=True))
    if product is None:
        raise NotFound("Produto", product_id)
    await session.commit()
    return product


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: str, session: AsyncSession = Depends(get_session)):
    repo = ProductRepository(session)
    deleted = await repo.delete(product_id)
    if not deleted:
        raise NotFound("Produto", product_id)
    await session.commit()


@router.get("/category/{category}/summary")
async def category_summary(category: str, session: AsyncSession = Depends(get_session)):
    """Retorna resumo de uma categoria: total de produtos, estoque total, preço médio."""
    repo = ProductRepository(session)
    products = await repo.filter_by_category(category)
    if not products:
        return {"category": category, "total_products": 0, "total_stock": 0, "avg_price": 0}
    return {
        "category": category,
        "total_products": len(products),
        "total_stock": sum(p.stock for p in products),
        "avg_price": sum(p.price for p in products) / len(products),
    }
