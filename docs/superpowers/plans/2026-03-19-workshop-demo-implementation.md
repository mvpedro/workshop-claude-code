# Workshop Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build two functional demo projects for the "Claude Code na Prática" workshop — a FastAPI+DBT application with automated docs pipeline, and a validation agent with subagents.

**Architecture:** The demo app (`demo/`) uses FastAPI with SQLAlchemy+SQLite, layered architecture (routes→services→repositories), an event bus, middleware chain, and a DBT project with DuckDB. The validation agent (`validation-agent/`) uses CLAUDE.md to orchestrate parallel subagents that check proposals against categorized project documentation.

**Tech Stack:** Python 3.11+, FastAPI, SQLAlchemy (async, SQLite), Pydantic, Alembic, pytest+httpx, DBT Core+DuckDB, MkDocs Material, GitHub Actions

**Spec:** `docs/superpowers/specs/2026-03-19-workshop-demo-implementation-design.md`

---

## Dependency Graph

```
Task 1 (scaffolding)
  ├→ Task 2 (models)
  │    ├→ Task 4 (schemas)
  │    ├→ Task 5 (repositories)
  │    │    └→ Task 6 (services) → Task 8 (routes + main) → Task 9 (test infra) → Task 11 (route tests)
  │    └→ Task 10 (alembic)
  ├→ Task 3 (exceptions + events) → Task 6 (services)
  │                                → Task 7 (middleware) → Task 8 (routes + main)
  └→ (nothing else starts from Task 1 alone — Task 9 needs Task 8)

Task 12 (service + event tests) — after Tasks 3, 5, 6, 9

Task 13 (DBT) — fully independent, can run in parallel with Tasks 2-12
Task 14 (CLAUDE.md + prompts) — independent
Task 15 (MkDocs + scripts) — independent
Task 16 (GitHub Actions) — after Task 14

Task 17-21 (validation agent) — fully independent, can run in parallel with all demo tasks
```

**Parallelization opportunities:**
- Tasks 2, 3 can start after Task 1
- Task 7 can start after Task 3
- Tasks 4, 5 can start after Task 2
- Task 9 (test infra) depends on Task 8 (main.py) because conftest imports `app`
- Task 13 (DBT) can run in parallel with everything in demo/
- Tasks 17-21 (validation agent) can run in parallel with everything

---

## Phase 1: Demo — Foundation

### Task 1: Project Scaffolding

**Files:**
- Create: `demo/pyproject.toml`
- Create: `demo/requirements.txt`
- Create: `demo/src/__init__.py`
- Create: `demo/src/api/__init__.py`
- Create: `demo/src/api/config.py`
- Create: `demo/src/api/database.py`
- Create: `demo/src/api/models/__init__.py`
- Create: `demo/src/api/schemas/__init__.py`
- Create: `demo/src/api/repositories/__init__.py`
- Create: `demo/src/api/services/__init__.py`
- Create: `demo/src/api/events/__init__.py`
- Create: `demo/src/api/middleware/__init__.py`
- Create: `demo/src/api/routes/__init__.py`
- Create: `demo/src/api/exceptions/__init__.py`
- Create: `demo/src/api/tasks/__init__.py`

- [ ] **Step 1: Create pyproject.toml**

```toml
[project]
name = "workshop-demo"
version = "0.1.0"
description = "Workshop Demo — Sistema de Gestão de Clientes, Produtos e Pedidos"
requires-python = ">=3.11"

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

- [ ] **Step 2: Create requirements.txt**

```
fastapi>=0.110,<1.0
uvicorn[standard]>=0.27
sqlalchemy[asyncio]>=2.0,<3.0
aiosqlite>=0.20
pydantic>=2.0,<3.0
pydantic-settings>=2.0,<3.0
alembic>=1.13,<2.0
httpx>=0.27
pytest>=8.0
pytest-asyncio>=0.23
```

- [ ] **Step 3: Create config.py**

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Workshop Demo API"
    database_url: str = "sqlite+aiosqlite:///./demo.db"
    api_key: str = "demo-api-key-2024"
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60
    debug: bool = False

    model_config = {"env_prefix": "DEMO_"}


settings = Settings()
```

- [ ] **Step 4: Create database.py**

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.api.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
```

- [ ] **Step 5: Create all __init__.py files**

Create empty `__init__.py` in each package directory: `src/`, `src/api/`, `src/api/models/`, `src/api/schemas/`, `src/api/repositories/`, `src/api/services/`, `src/api/events/`, `src/api/middleware/`, `src/api/routes/`, `src/api/exceptions/`, `src/api/tasks/`.

- [ ] **Step 6: Install dependencies and verify**

```bash
cd demo && pip install -r requirements.txt
python -c "from src.api.config import settings; print(settings.app_name)"
```

Expected: `Workshop Demo API`

- [ ] **Step 7: Commit**

```bash
git add demo/pyproject.toml demo/requirements.txt demo/src/
git commit -m "feat(demo): project scaffolding with config and database"
```

---

### Task 2: SQLAlchemy Models

**Files:**
- Create: `demo/src/api/models/base.py`
- Create: `demo/src/api/models/customer.py`
- Create: `demo/src/api/models/product.py`
- Create: `demo/src/api/models/order.py`
- Create: `demo/src/api/models/order_item.py`
- Modify: `demo/src/api/models/__init__.py`

**Depends on:** Task 1

- [ ] **Step 1: Create base model**

```python
# demo/src/api/models/base.py
import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
```

- [ ] **Step 2: Create customer model**

```python
# demo/src/api/models/customer.py
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.models.base import BaseModel


class Customer(BaseModel):
    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(50))
    segment: Mapped[str] = mapped_column(String(50), default="bronze")  # bronze, silver, gold
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    orders: Mapped[list["Order"]] = relationship(back_populates="customer")
```

- [ ] **Step 3: Create product model**

```python
# demo/src/api/models/product.py
from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.api.models.base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)  # in cents
    stock: Mapped[int] = mapped_column(Integer, default=0)
    category: Mapped[str] = mapped_column(String(100), index=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True)
```

- [ ] **Step 4: Create order model with state machine**

```python
# demo/src/api/models/order.py
from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.models.base import BaseModel

VALID_TRANSITIONS: dict[str, list[str]] = {
    "pending": ["processing", "cancelled"],
    "processing": ["shipped", "cancelled"],
    "shipped": ["delivered"],
    "delivered": [],
    "cancelled": [],
}


class Order(BaseModel):
    __tablename__ = "orders"

    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    total: Mapped[float] = mapped_column(Float, default=0.0)
    notes: Mapped[str | None] = mapped_column(Text)

    customer: Mapped["Customer"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

    def can_transition_to(self, new_status: str) -> bool:
        return new_status in VALID_TRANSITIONS.get(self.status, [])
```

- [ ] **Step 5: Create order_item model**

```python
# demo/src/api/models/order_item.py
from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.models.base import BaseModel


class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Float)  # price at time of purchase, in cents

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()
```

- [ ] **Step 6: Update models __init__.py with all imports**

```python
# demo/src/api/models/__init__.py
from src.api.models.base import Base, BaseModel
from src.api.models.customer import Customer
from src.api.models.order import Order, VALID_TRANSITIONS
from src.api.models.order_item import OrderItem
from src.api.models.product import Product

__all__ = ["Base", "BaseModel", "Customer", "Order", "OrderItem", "Product", "VALID_TRANSITIONS"]
```

- [ ] **Step 7: Verify models load**

```bash
cd demo && python -c "from src.api.models import Base, Customer, Product, Order, OrderItem; print('Models OK:', [t.name for t in Base.metadata.sorted_tables])"
```

Expected: tables listed including customers, products, orders, order_items

- [ ] **Step 8: Commit**

```bash
git add demo/src/api/models/
git commit -m "feat(demo): SQLAlchemy models with relationships and order state machine"
```

---

### Task 3: Exceptions + Event System

**Files:**
- Create: `demo/src/api/exceptions/base.py`
- Create: `demo/src/api/exceptions/business.py`
- Create: `demo/src/api/exceptions/infrastructure.py`
- Create: `demo/src/api/events/bus.py`
- Create: `demo/src/api/events/types.py`
- Create: `demo/src/api/events/handlers.py`

**Depends on:** Task 1 (can run in parallel with Task 2)

- [ ] **Step 1: Create exception hierarchy**

```python
# demo/src/api/exceptions/base.py
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
```

```python
# demo/src/api/exceptions/business.py
from src.api.exceptions.base import AppException


class InsufficientStock(AppException):
    def __init__(self, product_id: str, requested: int, available: int):
        super().__init__(
            f"Estoque insuficiente para produto {product_id}: "
            f"solicitado {requested}, disponível {available}",
            status_code=409,
        )


class InvalidStatusTransition(AppException):
    def __init__(self, order_id: str, current: str, target: str):
        super().__init__(
            f"Transição inválida para pedido {order_id}: {current} → {target}",
            status_code=422,
        )


class DuplicateEmail(AppException):
    def __init__(self, email: str):
        super().__init__(f"Email já cadastrado: {email}", status_code=409)


class NotFound(AppException):
    def __init__(self, entity: str, entity_id: str):
        super().__init__(f"{entity} não encontrado: {entity_id}", status_code=404)
```

```python
# demo/src/api/exceptions/infrastructure.py
from src.api.exceptions.base import AppException


class DatabaseError(AppException):
    def __init__(self, detail: str = "Erro interno no banco de dados"):
        super().__init__(detail, status_code=500)


class ExternalServiceError(AppException):
    def __init__(self, service: str, detail: str = ""):
        super().__init__(
            f"Erro no serviço externo '{service}': {detail}", status_code=502
        )
```

- [ ] **Step 2: Create event system**

```python
# demo/src/api/events/types.py
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class OrderCreated:
    order_id: str
    customer_id: str
    total: float
    item_count: int
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class OrderStatusChanged:
    order_id: str
    old_status: str
    new_status: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class StockLow:
    product_id: str
    current_stock: int
    threshold: int = 5
    timestamp: datetime = field(default_factory=datetime.now)
```

```python
# demo/src/api/events/bus.py
import logging
from collections import defaultdict
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

EventHandler = Callable[[Any], None]

_subscribers: dict[type, list[EventHandler]] = defaultdict(list)


def subscribe(event_type: type, handler: EventHandler) -> None:
    _subscribers[event_type].append(handler)


def publish(event: object) -> None:
    event_type = type(event)
    handlers = _subscribers.get(event_type, [])
    logger.info("Publicando evento %s para %d handlers", event_type.__name__, len(handlers))
    for handler in handlers:
        try:
            handler(event)
        except Exception:
            logger.exception("Erro no handler %s para evento %s", handler.__name__, event_type.__name__)


def clear() -> None:
    """Clear all subscribers. Used in tests."""
    _subscribers.clear()
```

```python
# demo/src/api/events/handlers.py
from src.api.events import bus
from src.api.events.types import OrderCreated, OrderStatusChanged, StockLow


def setup_event_handlers() -> None:
    """Register all event handlers. Called during app startup."""
    # These will be connected to actual services in main.py
    # For now, register logging handlers as defaults
    bus.subscribe(OrderCreated, _log_order_created)
    bus.subscribe(OrderStatusChanged, _log_status_changed)
    bus.subscribe(StockLow, _log_stock_low)


def _log_order_created(event: OrderCreated) -> None:
    import logging
    logging.getLogger(__name__).info(
        "Pedido criado: %s (cliente: %s, total: R$%.2f)",
        event.order_id, event.customer_id, event.total / 100,
    )


def _log_status_changed(event: OrderStatusChanged) -> None:
    import logging
    logging.getLogger(__name__).info(
        "Status do pedido %s alterado: %s → %s",
        event.order_id, event.old_status, event.new_status,
    )


def _log_stock_low(event: StockLow) -> None:
    import logging
    logging.getLogger(__name__).warning(
        "Estoque baixo: produto %s com %d unidades (limite: %d)",
        event.product_id, event.current_stock, event.threshold,
    )
```

- [ ] **Step 3: Verify imports**

```bash
cd demo && python -c "from src.api.exceptions.business import InsufficientStock, NotFound; from src.api.events.bus import publish, subscribe; from src.api.events.types import OrderCreated; print('OK')"
```

- [ ] **Step 4: Commit**

```bash
git add demo/src/api/exceptions/ demo/src/api/events/
git commit -m "feat(demo): exception hierarchy and in-process event bus"
```

---

### Task 4: Pydantic Schemas

**Files:**
- Create: `demo/src/api/schemas/pagination.py`
- Create: `demo/src/api/schemas/customer.py`
- Create: `demo/src/api/schemas/product.py`
- Create: `demo/src/api/schemas/order.py`

**Depends on:** Task 2 (needs to know model fields)

- [ ] **Step 1: Create pagination schema**

```python
# demo/src/api/schemas/pagination.py
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int
```

- [ ] **Step 2: Create customer schemas**

```python
# demo/src/api/schemas/customer.py
from datetime import datetime

from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None
    segment: str = "bronze"


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    segment: str | None = None
    is_active: bool | None = None


class CustomerResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str | None
    segment: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

- [ ] **Step 3: Create product schemas**

```python
# demo/src/api/schemas/product.py
from datetime import datetime

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float  # in cents
    stock: int = 0
    category: str
    sku: str


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    category: str | None = None


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str | None
    price: float
    stock: int
    category: str
    sku: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

- [ ] **Step 4: Create order schemas**

```python
# demo/src/api/schemas/order.py
from datetime import datetime

from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int


class OrderCreate(BaseModel):
    customer_id: str
    items: list[OrderItemCreate]
    notes: str | None = None


class OrderItemResponse(BaseModel):
    id: str
    product_id: str
    quantity: int
    unit_price: float

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: str
    customer_id: str
    status: str
    total: float
    notes: str | None
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    status: str
```

- [ ] **Step 5: Verify schemas**

```bash
cd demo && python -c "from src.api.schemas.customer import CustomerCreate, CustomerResponse; from src.api.schemas.order import OrderCreate; from src.api.schemas.pagination import PaginatedResponse; print('Schemas OK')"
```

- [ ] **Step 6: Commit**

```bash
git add demo/src/api/schemas/
git commit -m "feat(demo): Pydantic request/response schemas with pagination"
```

---

### Task 5: Repository Layer

**Files:**
- Create: `demo/src/api/repositories/base.py`
- Create: `demo/src/api/repositories/customer_repository.py`
- Create: `demo/src/api/repositories/product_repository.py`
- Create: `demo/src/api/repositories/order_repository.py`

**Depends on:** Task 2

- [ ] **Step 1: Create abstract repository**

```python
# demo/src/api/repositories/base.py
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class AbstractRepository(ABC, Generic[T]):
    model: type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: str) -> T | None:
        return await self.session.get(self.model, entity_id)

    async def list(self, offset: int = 0, limit: int = 20, **filters: Any) -> list[T]:
        query = select(self.model)
        for key, value in filters.items():
            if value is not None and hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count(self, **filters: Any) -> int:
        query = select(func.count()).select_from(self.model)
        for key, value in filters.items():
            if value is not None and hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def create(self, **kwargs: Any) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def update(self, entity_id: str, **kwargs: Any) -> T | None:
        instance = await self.get_by_id(entity_id)
        if instance is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(instance, key, value)
        await self.session.flush()
        return instance

    async def delete(self, entity_id: str) -> bool:
        instance = await self.get_by_id(entity_id)
        if instance is None:
            return False
        await self.session.delete(instance)
        await self.session.flush()
        return True
```

- [ ] **Step 2: Create concrete repositories**

Create `customer_repository.py` with `search_by_email(email)` and `get_by_segment(segment)`.
Create `product_repository.py` with `filter_by_category(category)` and `get_low_stock(threshold=5)`.
Create `order_repository.py` with `get_by_customer(customer_id)` and `get_by_status(status)`.

Each concrete repository sets `model = <ModelClass>` and adds the specialized query methods using `select()` with appropriate `where()` clauses.

- [ ] **Step 3: Verify repositories**

```bash
cd demo && python -c "from src.api.repositories.customer_repository import CustomerRepository; from src.api.repositories.order_repository import OrderRepository; print('Repos OK')"
```

- [ ] **Step 4: Commit**

```bash
git add demo/src/api/repositories/
git commit -m "feat(demo): repository layer with abstract base and concrete implementations"
```

---

## Phase 2: Demo — Business Logic + API

### Task 6: Services

**Files:**
- Create: `demo/src/api/services/pricing_service.py`
- Create: `demo/src/api/services/inventory_service.py`
- Create: `demo/src/api/services/notification_service.py`
- Create: `demo/src/api/services/analytics_service.py`
- Create: `demo/src/api/services/order_service.py`

**Depends on:** Tasks 3, 5

- [ ] **Step 1: Create pricing service**

```python
# demo/src/api/services/pricing_service.py
from src.api.models.product import Product


def calculate_item_price(product: Product, quantity: int) -> float:
    """Calculate price for a line item, applying bulk discounts."""
    base = product.price * quantity
    if quantity >= 100:
        return base * 0.85  # 15% discount
    if quantity >= 50:
        return base * 0.90  # 10% discount
    if quantity >= 10:
        return base * 0.95  # 5% discount
    return base


def calculate_order_total(items: list[tuple[Product, int]]) -> float:
    """Calculate total for all items in an order."""
    return sum(calculate_item_price(product, qty) for product, qty in items)
```

- [ ] **Step 2: Create inventory service**

```python
# demo/src/api/services/inventory_service.py
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
```

- [ ] **Step 3: Create notification service**

```python
# demo/src/api/services/notification_service.py
import logging

from src.api.events.types import OrderCreated, OrderStatusChanged

logger = logging.getLogger(__name__)


def handle_order_created(event: OrderCreated) -> None:
    logger.info(
        "[NOTIFICAÇÃO] Confirmação de pedido enviada para cliente %s "
        "(pedido: %s, total: R$%.2f)",
        event.customer_id, event.order_id, event.total / 100,
    )


def handle_status_changed(event: OrderStatusChanged) -> None:
    logger.info(
        "[NOTIFICAÇÃO] Atualização de status enviada para pedido %s: %s → %s",
        event.order_id, event.old_status, event.new_status,
    )
```

- [ ] **Step 4: Create analytics service**

```python
# demo/src/api/services/analytics_service.py
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
```

- [ ] **Step 5: Create order service (orchestrator)**

```python
# demo/src/api/services/order_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from src.api.events import bus
from src.api.events.types import OrderCreated, OrderStatusChanged
from src.api.exceptions.business import InvalidStatusTransition, NotFound
from src.api.models.order import Order
from src.api.models.order_item import OrderItem
from src.api.models.product import Product
from src.api.schemas.order import OrderCreate
from src.api.services import inventory_service, pricing_service


async def create_order(session: AsyncSession, data: OrderCreate) -> Order:
    items_with_products: list[tuple[Product, int]] = []
    for item in data.items:
        product = await session.get(Product, item.product_id)
        if product is None:
            raise NotFound("Produto", item.product_id)
        items_with_products.append((product, item.quantity))

    # Reserve stock for all items
    for product, qty in items_with_products:
        await inventory_service.reserve_stock(session, product, qty)

    # Calculate total
    total = pricing_service.calculate_order_total(items_with_products)

    # Create order
    order = Order(customer_id=data.customer_id, total=total, notes=data.notes)
    session.add(order)
    await session.flush()

    # Create order items
    for product, qty in items_with_products:
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=qty,
            unit_price=product.price,
        )
        session.add(order_item)
    await session.flush()

    # Emit event
    bus.publish(OrderCreated(
        order_id=order.id,
        customer_id=data.customer_id,
        total=total,
        item_count=len(data.items),
    ))

    return order


async def transition_status(session: AsyncSession, order_id: str, new_status: str) -> Order:
    query = select(Order).where(Order.id == order_id).options(selectinload(Order.items))
    result = await session.execute(query)
    order = result.scalar_one_or_none()
    if order is None:
        raise NotFound("Pedido", order_id)
    if not order.can_transition_to(new_status):
        raise InvalidStatusTransition(order_id, order.status, new_status)

    old_status = order.status
    order.status = new_status
    await session.flush()

    # Release stock if cancelled
    if new_status == "cancelled":
        for item in order.items:
            product = await session.get(Product, item.product_id)
            if product:
                await inventory_service.release_stock(session, product, item.quantity)

    bus.publish(OrderStatusChanged(
        order_id=order.id, old_status=old_status, new_status=new_status
    ))

    return order
```

- [ ] **Step 6: Verify services import**

```bash
cd demo && python -c "from src.api.services import order_service, pricing_service, inventory_service, analytics_service, notification_service; print('Services OK')"
```

- [ ] **Step 7: Commit**

```bash
git add demo/src/api/services/
git commit -m "feat(demo): business services with pricing, inventory, analytics, and order orchestration"
```

---

### Task 7: Middleware

**Files:**
- Create: `demo/src/api/middleware/auth.py`
- Create: `demo/src/api/middleware/logging.py`
- Create: `demo/src/api/middleware/error_handler.py`
- Create: `demo/src/api/middleware/rate_limiter.py`

**Depends on:** Task 3 (exceptions — error_handler.py imports AppException)

- [ ] **Step 1: Create all middleware modules**

**auth.py** — checks `X-API-Key` header against `settings.api_key`. Returns 401 if missing/invalid. Skips `/docs` and `/openapi.json` paths.

**logging.py** — logs method, path, status_code, and duration_ms for each request using `time.perf_counter()`.

**error_handler.py** — catches `AppException` subclasses and returns JSON `{"detail": exception.message}` with the exception's `status_code`. Catches generic `Exception` and returns 500.

**rate_limiter.py** — in-memory dict keyed by client IP. Tracks request count within a sliding window. Returns 429 if limit exceeded. Uses `settings.rate_limit_requests` and `settings.rate_limit_window_seconds`.

All middleware use the Starlette `BaseHTTPMiddleware` pattern.

- [ ] **Step 2: Verify middleware imports**

```bash
cd demo && python -c "from src.api.middleware.auth import AuthMiddleware; from src.api.middleware.error_handler import ErrorHandlerMiddleware; print('Middleware OK')"
```

- [ ] **Step 3: Commit**

```bash
git add demo/src/api/middleware/
git commit -m "feat(demo): middleware chain — auth, logging, error handling, rate limiting"
```

---

### Task 8: Routes + Main App Assembly

**Files:**
- Create: `demo/src/api/routes/customers.py`
- Create: `demo/src/api/routes/products.py`
- Create: `demo/src/api/routes/orders.py`
- Create: `demo/src/api/routes/analytics.py`
- Create: `demo/src/api/tasks/background.py`
- Create: `demo/src/api/tasks/order_processing.py`
- Create: `demo/src/api/main.py`

**Depends on:** Tasks 4, 5, 6, 7

- [ ] **Step 1: Create customer routes**

```python
# demo/src/api/routes/customers.py
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
        pages=(total + page_size - 1) // page_size,
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
```

- [ ] **Step 2: Create product routes**

Similar to customer routes but with additional endpoints:
- `GET /products` with `category` filter and pagination
- `GET /products/low-stock` using `repo.get_low_stock()`
- Standard CRUD: GET by id, POST, PUT, DELETE

- [ ] **Step 3: Create order routes**

- `GET /orders` with `status` and `customer_id` filters, pagination
- `GET /orders/{id}` with items loaded (selectinload)
- `POST /orders` — delegates to `order_service.create_order()`, wraps in BackgroundTasks for post-processing
- `PATCH /orders/{id}/status` — delegates to `order_service.transition_status()`

- [ ] **Step 4: Create analytics routes**

```python
# demo/src/api/routes/analytics.py
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
```

- [ ] **Step 5: Create background tasks**

```python
# demo/src/api/tasks/background.py
import logging

logger = logging.getLogger(__name__)


def process_new_order(order_id: str) -> None:
    """Post-order processing: confirm, notify, update analytics."""
    logger.info("[BACKGROUND] Processando novo pedido: %s", order_id)
    logger.info("[BACKGROUND] Confirmação enviada para pedido: %s", order_id)
    logger.info("[BACKGROUND] Analytics atualizados para pedido: %s", order_id)
```

```python
# demo/src/api/tasks/order_processing.py
import logging

logger = logging.getLogger(__name__)


def process_status_change(order_id: str, old_status: str, new_status: str) -> None:
    logger.info(
        "[BACKGROUND] Processando mudança de status: pedido %s (%s → %s)",
        order_id, old_status, new_status,
    )
```

- [ ] **Step 6: Create main.py**

```python
# demo/src/api/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.config import settings
from src.api.database import engine
from src.api.events import bus
from src.api.events.handlers import setup_event_handlers
from src.api.events.types import OrderCreated, OrderStatusChanged
from src.api.middleware.auth import AuthMiddleware
from src.api.middleware.error_handler import ErrorHandlerMiddleware
from src.api.middleware.logging import LoggingMiddleware
from src.api.middleware.rate_limiter import RateLimiterMiddleware
from src.api.models import Base
from src.api.routes import analytics, customers, orders, products
from src.api.services import notification_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    setup_event_handlers()
    # Connect notification service to events
    bus.subscribe(OrderCreated, notification_service.handle_order_created)
    bus.subscribe(OrderStatusChanged, notification_service.handle_status_changed)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    description="API REST para gestão de clientes, produtos e pedidos",
    version="0.1.0",
    lifespan=lifespan,
)

# Middleware (order matters: outermost first)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimiterMiddleware)
app.add_middleware(AuthMiddleware)

# Routes
app.include_router(customers.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
```

- [ ] **Step 7: Verify app starts**

```bash
cd demo && python -c "from src.api.main import app; print('App routes:', [r.path for r in app.routes])"
```

- [ ] **Step 8: Commit**

```bash
git add demo/src/api/routes/ demo/src/api/tasks/ demo/src/api/main.py
git commit -m "feat(demo): API routes, background tasks, and main app assembly"
```

---

## Phase 3: Demo — Tests

### Task 9: Test Infrastructure

**Files:**
- Create: `demo/tests/__init__.py`
- Create: `demo/tests/conftest.py`

**Depends on:** Task 8 (conftest imports `app` from main.py)

- [ ] **Step 1: Create conftest with test DB and client**

```python
# demo/tests/conftest.py
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.api.database import get_session
from src.api.events import bus
from src.api.models import Base
from src.api.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite://"  # in-memory

engine = create_async_engine(TEST_DATABASE_URL)
TestSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    bus.clear()


@pytest.fixture
async def session():
    async with TestSession() as session:
        yield session


@pytest.fixture
async def client():
    async def override_session():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def api_headers():
    return {"X-API-Key": "demo-api-key-2024"}
```

- [ ] **Step 2: Verify pytest discovers conftest**

```bash
cd demo && python -m pytest --collect-only 2>&1 | head -5
```

Expected: no errors, possibly "no tests ran"

- [ ] **Step 3: Commit**

```bash
git add demo/tests/
git commit -m "feat(demo): test infrastructure with in-memory SQLite and async client"
```

---

### Task 10: Alembic Setup

**Files:**
- Create: `demo/alembic.ini`
- Create: `demo/migrations/env.py`
- Create: `demo/migrations/versions/001_initial_schema.py`
- Create: `demo/migrations/versions/002_add_order_items.py`

**Depends on:** Task 2

- [ ] **Step 1: Create alembic.ini**

```ini
[alembic]
script_location = migrations
sqlalchemy.url = sqlite+aiosqlite:///./demo.db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
```

- [ ] **Step 2: Create migrations/env.py**

Standard async Alembic env.py that imports `Base.metadata` from `src.api.models` and configures the async engine.

- [ ] **Step 3: Create migration 001 — initial schema**

Manual migration file that creates `customers` and `products` tables matching the SQLAlchemy models.

- [ ] **Step 4: Create migration 002 — add order tables**

Manual migration file that creates `orders` and `order_items` tables with foreign keys.

- [ ] **Step 5: Commit**

```bash
git add demo/alembic.ini demo/migrations/
git commit -m "feat(demo): Alembic migrations for initial schema and order items"
```

---

### Task 11: Route Tests

**Files:**
- Create: `demo/tests/test_customers.py`
- Create: `demo/tests/test_products.py`
- Create: `demo/tests/test_orders.py`

**Depends on:** Tasks 8, 9

- [ ] **Step 1: Write customer tests**

Test CRUD operations:
- `test_create_customer` — POST, assert 201, check response fields
- `test_list_customers` — create 3, GET list, assert pagination
- `test_get_customer` — create, GET by id, assert fields
- `test_update_customer` — create, PUT, assert updated fields
- `test_delete_customer` — create, DELETE, assert 204, GET returns 404
- `test_filter_by_segment` — create bronze + gold, filter segment=gold, assert count
- `test_duplicate_email` — create, create same email, assert 409

All requests must include `api_headers` fixture.

- [ ] **Step 2: Run customer tests**

```bash
cd demo && python -m pytest tests/test_customers.py -v
```

Expected: all pass

- [ ] **Step 3: Write product tests**

Similar to customers but with:
- `test_filter_by_category`
- `test_low_stock_endpoint` — create product with stock=3, hit low-stock endpoint

- [ ] **Step 4: Run product tests**

```bash
cd demo && python -m pytest tests/test_products.py -v
```

- [ ] **Step 5: Write order tests**

- `test_create_order` — create customer + product, POST order, assert 201, assert stock reduced
- `test_create_order_insufficient_stock` — product with stock=1, order qty=5, assert 409
- `test_status_transition_valid` — create order, PATCH to processing, assert 200
- `test_status_transition_invalid` — create order, PATCH to delivered (skipping processing/shipped), assert 422
- `test_cancel_order_releases_stock` — create order, cancel, assert stock restored
- `test_list_orders_by_customer` — create 2 orders for customer A and 1 for B, filter by A, assert count

- [ ] **Step 6: Run order tests**

```bash
cd demo && python -m pytest tests/test_orders.py -v
```

- [ ] **Step 7: Commit**

```bash
git add demo/tests/test_customers.py demo/tests/test_products.py demo/tests/test_orders.py
git commit -m "test(demo): route tests for customers, products, and orders"
```

---

### Task 12: Service + Event Tests

**Files:**
- Create: `demo/tests/test_pricing_service.py`
- Create: `demo/tests/test_inventory_service.py`
- Create: `demo/tests/test_event_bus.py`

**Depends on:** Tasks 3, 6, 9

- [ ] **Step 1: Write pricing service tests**

```python
# demo/tests/test_pricing_service.py
from unittest.mock import MagicMock

from src.api.services.pricing_service import calculate_item_price, calculate_order_total


def test_no_discount_under_10():
    product = MagicMock(price=1000)  # R$10.00 in cents
    assert calculate_item_price(product, 5) == 5000


def test_5_percent_discount_at_10():
    product = MagicMock(price=1000)
    assert calculate_item_price(product, 10) == 9500


def test_10_percent_discount_at_50():
    product = MagicMock(price=1000)
    assert calculate_item_price(product, 50) == 45000


def test_15_percent_discount_at_100():
    product = MagicMock(price=1000)
    assert calculate_item_price(product, 100) == 85000


def test_calculate_order_total():
    p1 = MagicMock(price=1000)
    p2 = MagicMock(price=500)
    total = calculate_order_total([(p1, 5), (p2, 10)])
    assert total == 5000 + 4750  # no discount + 5% discount
```

- [ ] **Step 2: Run pricing tests**

```bash
cd demo && python -m pytest tests/test_pricing_service.py -v
```

- [ ] **Step 3: Write inventory service tests**

Test `reserve_stock` and `release_stock`:
- `test_reserve_stock_success` — product with stock=10, reserve 3, assert stock=7
- `test_reserve_stock_insufficient` — product with stock=2, reserve 5, assert raises `InsufficientStock`
- `test_reserve_stock_emits_low_stock_event` — reserve until stock <= 5, assert `StockLow` event published
- `test_release_stock` — product with stock=5, release 3, assert stock=8

These tests need a real async session (use the `session` fixture from conftest).

- [ ] **Step 4: Run inventory tests**

```bash
cd demo && python -m pytest tests/test_inventory_service.py -v
```

- [ ] **Step 5: Write event bus tests**

```python
# demo/tests/test_event_bus.py
from src.api.events.bus import clear, publish, subscribe
from src.api.events.types import OrderCreated


def test_publish_calls_subscribers():
    received = []
    subscribe(OrderCreated, lambda e: received.append(e))
    event = OrderCreated(order_id="1", customer_id="c1", total=1000, item_count=2)
    publish(event)
    assert len(received) == 1
    assert received[0].order_id == "1"
    clear()


def test_publish_no_subscribers():
    clear()
    event = OrderCreated(order_id="1", customer_id="c1", total=1000, item_count=2)
    publish(event)  # should not raise


def test_handler_error_does_not_break_others():
    received = []

    def bad_handler(e):
        raise ValueError("boom")

    subscribe(OrderCreated, bad_handler)
    subscribe(OrderCreated, lambda e: received.append(e))
    event = OrderCreated(order_id="1", customer_id="c1", total=1000, item_count=2)
    publish(event)
    assert len(received) == 1
    clear()
```

- [ ] **Step 6: Run event bus tests**

```bash
cd demo && python -m pytest tests/test_event_bus.py -v
```

- [ ] **Step 7: Run full test suite**

```bash
cd demo && python -m pytest -v
```

Expected: all tests pass

- [ ] **Step 8: Commit**

```bash
git add demo/tests/test_pricing_service.py demo/tests/test_inventory_service.py demo/tests/test_event_bus.py
git commit -m "test(demo): service and event bus unit tests"
```

---

## Phase 4: Demo — DBT

### Task 13: DBT Project

**Files:**
- Create: `demo/dbt/dbt_project.yml`
- Create: `demo/dbt/profiles.yml`
- Create: `demo/dbt/packages.yml`
- Create: `demo/dbt/seeds/raw_customers.csv`
- Create: `demo/dbt/seeds/raw_products.csv`
- Create: `demo/dbt/seeds/raw_orders.csv`
- Create: `demo/dbt/seeds/raw_order_items.csv`
- Create: `demo/dbt/models/sources.yml`
- Create: `demo/dbt/models/staging/stg_customers.sql`
- Create: `demo/dbt/models/staging/stg_products.sql`
- Create: `demo/dbt/models/staging/stg_orders.sql`
- Create: `demo/dbt/models/intermediate/int_customer_orders.sql`
- Create: `demo/dbt/models/intermediate/int_product_performance.sql`
- Create: `demo/dbt/models/marts/dim_customers.sql`
- Create: `demo/dbt/models/marts/fct_orders.sql`
- Create: `demo/dbt/macros/cents_to_reais.sql`

**Depends on:** None (fully independent, can run in parallel with all FastAPI tasks)

- [ ] **Step 1: Create dbt_project.yml**

```yaml
name: 'workshop_demo'
version: '1.0.0'
config-version: 2
profile: 'workshop_demo'

model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
macro-paths: ["macros"]

seeds:
  workshop_demo:
    +schema: raw
```

- [ ] **Step 2: Create profiles.yml**

```yaml
workshop_demo:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: 'workshop_demo.duckdb'
      threads: 4
```

- [ ] **Step 3: Create packages.yml**

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: ">=1.1.0"
```

- [ ] **Step 4: Create seed CSVs**

**raw_customers.csv** — 20 rows with columns: `id,nome,email,telefone,segmento,ativo,data_cadastro`. Use realistic Brazilian names and emails. Mix of segments: ~10 bronze, ~6 silver, ~4 gold. Some inactive.

**raw_products.csv** — 15 rows with columns: `id,nome,descricao,preco_centavos,estoque,categoria,sku`. Spread across categories: Laticínios, Equipamentos, Insumos, Serviços. Prices from 500 to 500000 (centavos). Some low stock (<5).

**raw_orders.csv** — 50 rows with columns: `id,cliente_id,status_code,valor_total_centavos,data_pedido,notas`. Status codes: 1=pending, 2=processing, 3=shipped, 4=delivered, 5=cancelled. Dates spread across 2025-07 to 2026-02. Some customers with many orders, some with one.

**raw_order_items.csv** — ~100 rows with columns: `id,pedido_id,produto_id,quantidade,preco_unitario_centavos`. Each order has 1-4 items. References valid order IDs and product IDs from the other seeds. This enables the `int_product_performance` model to correctly join orders to products.

- [ ] **Step 5: Create sources.yml**

```yaml
version: 2
sources:
  - name: raw
    schema: raw
    tables:
      - name: raw_customers
      - name: raw_products
      - name: raw_orders
      - name: raw_order_items
```

No descriptions — intentionally undocumented so Claude generates them.

- [ ] **Step 6: Create staging models**

```sql
-- models/staging/stg_customers.sql
with source as (
    select * from {{ source('raw', 'raw_customers') }}
)
select
    id as customer_id,
    nome as customer_name,
    lower(trim(email)) as email,
    telefone as phone,
    case
        when lower(segmento) = 'ouro' then 'gold'
        when lower(segmento) = 'prata' then 'silver'
        else 'bronze'
    end as segment,
    ativo = 1 as is_active,
    cast(data_cadastro as date) as signup_date
from source
```

```sql
-- models/staging/stg_products.sql
with source as (
    select * from {{ source('raw', 'raw_products') }}
)
select
    id as product_id,
    nome as product_name,
    descricao as description,
    preco_centavos as price_cents,
    {{ cents_to_reais('preco_centavos') }} as price_reais,
    estoque as stock,
    lower(trim(categoria)) as category,
    upper(sku) as sku
from source
```

```sql
-- models/staging/stg_orders.sql
with source as (
    select * from {{ source('raw', 'raw_orders') }}
)
select
    id as order_id,
    cliente_id as customer_id,
    case status_code
        when 1 then 'pending'
        when 2 then 'processing'
        when 3 then 'shipped'
        when 4 then 'delivered'
        when 5 then 'cancelled'
    end as status,
    valor_total_centavos as total_cents,
    {{ cents_to_reais('valor_total_centavos') }} as total_reais,
    cast(data_pedido as date) as order_date,
    notas as notes
from source
```

- [ ] **Step 7: Create intermediate models**

```sql
-- models/intermediate/int_customer_orders.sql
with customers as (
    select * from {{ ref('stg_customers') }}
),
orders as (
    select * from {{ ref('stg_orders') }}
    where status != 'cancelled'
)
select
    c.customer_id,
    c.customer_name,
    c.email,
    c.segment,
    c.is_active,
    c.signup_date,
    count(o.order_id) as order_count,
    coalesce(sum(o.total_cents), 0) as total_spent_cents,
    {{ cents_to_reais('coalesce(sum(o.total_cents), 0)') }} as total_spent_reais,
    min(o.order_date) as first_order_date,
    max(o.order_date) as last_order_date
from customers c
left join orders o on c.customer_id = o.customer_id
group by c.customer_id, c.customer_name, c.email, c.segment, c.is_active, c.signup_date
```

```sql
-- models/intermediate/int_product_performance.sql
with products as (
    select * from {{ ref('stg_products') }}
),
order_items as (
    select
        oi.produto_id as product_id,
        oi.quantidade as quantity,
        oi.preco_unitario_centavos as unit_price_cents,
        o.order_id,
        o.status
    from {{ source('raw', 'raw_order_items') }} oi
    inner join {{ ref('stg_orders') }} o on oi.pedido_id = o.order_id
    where o.status != 'cancelled'
)
select
    p.product_id,
    p.product_name,
    p.category,
    p.price_cents,
    p.stock,
    count(distinct oi.order_id) as times_ordered,
    coalesce(sum(oi.quantity), 0) as total_units_sold,
    coalesce(sum(oi.quantity * oi.unit_price_cents), 0) as total_revenue_cents,
    {{ cents_to_reais('coalesce(sum(oi.quantity * oi.unit_price_cents), 0)') }} as total_revenue_reais
from products p
left join order_items oi on p.product_id = oi.product_id
group by p.product_id, p.product_name, p.category, p.price_cents, p.stock
```

- [ ] **Step 8: Create marts models**

```sql
-- models/marts/dim_customers.sql
with customer_orders as (
    select * from {{ ref('int_customer_orders') }}
)
select
    customer_id,
    customer_name,
    email,
    segment,
    is_active,
    signup_date,
    order_count,
    total_spent_cents,
    total_spent_reais,
    first_order_date,
    last_order_date,
    case
        when total_spent_cents >= 100000 then 'gold'
        when total_spent_cents >= 50000 then 'silver'
        else 'bronze'
    end as calculated_segment
from customer_orders
```

```sql
-- models/marts/fct_orders.sql
with orders as (
    select * from {{ ref('stg_orders') }}
),
customers as (
    select * from {{ ref('int_customer_orders') }}
),
order_items as (
    select
        oi.pedido_id as order_id,
        oi.produto_id as product_id,
        oi.quantidade as quantity,
        oi.preco_unitario_centavos as unit_price_cents
    from {{ source('raw', 'raw_order_items') }} oi
),
product_perf as (
    select * from {{ ref('int_product_performance') }}
)
select
    o.order_id,
    o.customer_id,
    c.customer_name,
    c.segment as customer_segment,
    o.status,
    o.total_cents,
    o.total_reais,
    o.order_date,
    o.notes,
    c.order_count as customer_total_orders,
    c.total_spent_reais as customer_ltv_reais,
    count(oi.product_id) as item_count
from orders o
left join customers c on o.customer_id = c.customer_id
left join order_items oi on o.order_id = oi.order_id
group by
    o.order_id, o.customer_id, c.customer_name, c.segment,
    o.status, o.total_cents, o.total_reais, o.order_date, o.notes,
    c.order_count, c.total_spent_reais
```

Note: `fct_orders` references both `int_customer_orders` and `int_product_performance` (via the `product_perf` CTE, used to ensure the model appears in the DAG lineage). It also joins `raw_order_items` directly for the `item_count` column.

- [ ] **Step 9: Create macro**

```sql
-- macros/cents_to_reais.sql
{% macro cents_to_reais(column_name) %}
    round(cast({{ column_name }} as float) / 100, 2)
{% endmacro %}
```

- [ ] **Step 10: Install dbt packages and verify build**

```bash
cd demo/dbt && pip install dbt-core dbt-duckdb && dbt deps && dbt seed && dbt build
```

Expected: seeds loaded, all models built successfully, no test failures (no tests defined yet)

- [ ] **Step 11: Commit**

```bash
git add demo/dbt/
git commit -m "feat(demo): DBT project with DuckDB, seeds, staging/intermediate/marts models"
```

---

## Phase 5: Demo — Docs Pipeline

### Task 14: CLAUDE.md + Prompt Templates

**Files:**
- Create: `demo/CLAUDE.md`
- Create: `demo/prompts/full-scan.md`
- Create: `demo/prompts/incremental.md`
- Create: `demo/prompts/dbt-docs.md`

**Depends on:** None (independent)

- [ ] **Step 1: Create CLAUDE.md**

Write in Portuguese. Content from the workshop-spec.md CLAUDE.md section — project description, stack, conventions, documentation rules. Must be concise enough to show on screen in 30 seconds during the demo.

- [ ] **Step 2: Create prompt templates**

Use the content from the workshop-spec.md "Prompt templates" section, adjusted for the enhanced architecture. The full-scan template must mention: repositories, events, middleware, exceptions, background tasks — in addition to routes, models, services, and DBT.

The incremental template must reference `${CHANGED_FILES}` environment variable.

- [ ] **Step 3: Commit**

```bash
git add demo/CLAUDE.md demo/prompts/
git commit -m "feat(demo): CLAUDE.md project instructions and prompt templates"
```

---

### Task 15: MkDocs + Scripts

**Files:**
- Create: `demo/mkdocs.yml`
- Create: `demo/scripts/run-docs-generation.sh`
- Create: `demo/scripts/setup-mkdocs.sh`
- Create: `demo/docs/.gitkeep`

**Depends on:** None (independent)

- [ ] **Step 1: Create mkdocs.yml**

```yaml
site_name: "Workshop Demo — Documentação"
site_description: "Documentação gerada automaticamente via Claude Code"
theme:
  name: material
  language: pt-BR
  palette:
    - scheme: default
      primary: indigo
      toggle:
        icon: material/brightness-7
        name: Modo escuro
    - scheme: slate
      primary: indigo
      toggle:
        icon: material/brightness-4
        name: Modo claro

plugins:
  - search

markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - admonition
  - pymdownx.details
  - attr_list

nav:
  - Início: README.md
```

The nav section is minimal because the docs will be generated by Claude and may vary. MkDocs auto-discovers pages in the docs/ folder.

- [ ] **Step 2: Create scripts**

**setup-mkdocs.sh:**
```bash
#!/bin/bash
pip install mkdocs-material pymdown-extensions
echo "MkDocs instalado. Rode 'mkdocs serve' para visualizar."
```

**run-docs-generation.sh:**
```bash
#!/bin/bash
set -e
echo "Gerando documentação via Claude Code..."
claude -p "$(cat prompts/full-scan.md)" --allowedTools Edit,Write,Read,Glob,Grep,Bash
echo "Documentação gerada em docs/"
```

- [ ] **Step 3: Create docs/.gitkeep**

Empty file to keep the docs/ directory in git.

- [ ] **Step 4: Commit**

```bash
git add demo/mkdocs.yml demo/scripts/ demo/docs/.gitkeep
git commit -m "feat(demo): MkDocs configuration and helper scripts"
```

---

### Task 16: GitHub Actions Workflows

**Files:**
- Create: `.github/workflows/docs-full-scan.yml`
- Create: `.github/workflows/docs-incremental.yml`

**Depends on:** Task 14 (needs prompt files to exist)

- [ ] **Step 1: Create docs-full-scan.yml**

Use the content from the workshop-spec.md GitHub Actions section. Key points:
- `workflow_dispatch` trigger
- `working-directory: demo` on relevant steps
- `claude -p "$(cat prompts/full-scan.md)" --allowedTools Edit,Write,Read,Glob,Grep,Bash`
- `peter-evans/create-pull-request@v6` for PR creation

- [ ] **Step 2: Create docs-incremental.yml**

Use the content from the workshop-spec.md. Key points:
- `pull_request` trigger on `demo/src/**` and `demo/dbt/**`
- `fetch-depth: 0` for full history
- `git diff --name-only origin/main...HEAD -- demo/` for changed files
- `working-directory: demo`
- Commits docs back to PR branch

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/
git commit -m "feat: GitHub Actions workflows for docs generation pipeline"
```

---

## Phase 6: Validation Agent

### Task 17: Validation Agent — CLAUDE.md

**Files:**
- Create: `validation-agent/CLAUDE.md`

**Depends on:** None (fully independent)

- [ ] **Step 1: Create orchestrator CLAUDE.md**

Write in Portuguese. Must include:
- Dual mode support (code review + proposal validation)
- Agent tool dispatch instructions for 3 parallel subagents
- Compliance subagent → `docs/compliance/`
- Product + Style subagent → `docs/produto/` + `docs/estilo/`
- Technical subagent → `docs/tecnico/`
- Response format (compatible / attention / conflict with citations)
- Rules: cite specific documents, don't invent restrictions, be direct

Use the content from the design spec Section 5 "CLAUDE.md — Orchestrator" and the workshop-spec.md validation agent section.

- [ ] **Step 2: Commit**

```bash
git add validation-agent/CLAUDE.md
git commit -m "feat(validation-agent): orchestrator CLAUDE.md with dual mode and subagent dispatch"
```

---

### Task 18: Validation Agent — Compliance + Product Docs

**Files:**
- Create: `validation-agent/docs/compliance/requisitos-lgpd.md`
- Create: `validation-agent/docs/compliance/politica-dados.md`
- Create: `validation-agent/docs/compliance/restricoes-integracao.md`
- Create: `validation-agent/docs/produto/decisoes-produto.md`
- Create: `validation-agent/docs/produto/roadmap.md`
- Create: `validation-agent/docs/produto/regras-negocio.md`

**Depends on:** None

- [ ] **Step 1: Create compliance docs**

All in Portuguese. Must be credible, specific with dates and reasoning, interconnected.

**requisitos-lgpd.md** — LGPD requirements: consent for data collection, data minimization principle (collect only what's needed), retention limits (delete after purpose fulfilled), right to deletion, anonymization requirements for analytics. Include specific rule: "Dados pessoais (CPF, nome, email) NÃO devem ser armazenados em tabelas analíticas ou de reporting."

**politica-dados.md** — Data classification (public, internal, confidential, restricted). PII handling rules. Anonymization requirements. Include specific rule: "CPF é dado classificado como RESTRITO e só pode ser armazenado em tabelas transacionais com criptografia."

**restricoes-integracao.md** — List of approved external APIs and integration patterns. Include specific rule: "Toda integração com gateway de pagamento deve implementar circuit breaker e retry com backoff exponencial." List approved integrations: Pagar.me (approved, async only), AWS SES (email), Twilio (SMS).

- [ ] **Step 2: Create product docs**

**decisoes-produto.md** — Key product decisions with dates: scope definition, MVP features, what's explicitly out of scope. Include: "Rewrite de frontend está fora do escopo até Q3 2026" and "Novas integrações de pagamento só serão consideradas após estabilização do fluxo atual (previsão: Q2 2026)."

**roadmap.md** — Quarterly roadmap with priorities. Q1 2026: stabilize core, Q2 2026: analytics dashboard, Q3 2026: evaluate new integrations.

**regras-negocio.md** — Business rules for pricing, discounts, order limits. Discount tiers, minimum order values, customer segment rules.

- [ ] **Step 3: Commit**

```bash
git add validation-agent/docs/compliance/ validation-agent/docs/produto/
git commit -m "feat(validation-agent): compliance and product documentation"
```

---

### Task 19: Validation Agent — Technical + Style Docs

**Files:**
- Create: `validation-agent/docs/tecnico/decisoes-arquitetura.md`
- Create: `validation-agent/docs/tecnico/stack-definida.md`
- Create: `validation-agent/docs/tecnico/principios-tecnicos.md`
- Create: `validation-agent/docs/tecnico/padroes-testes.md`
- Create: `validation-agent/docs/estilo/guia-estilo-codigo.md`
- Create: `validation-agent/docs/estilo/convencoes-documentacao.md`
- Create: `validation-agent/docs/estilo/padroes-formatacao.md`

**Depends on:** None

- [ ] **Step 1: Create technical docs**

**decisoes-arquitetura.md** — ADR-style decisions: "Adotamos repository pattern para isolar a camada de persistência (decidido em 2025-09, motivação: facilitar troca de banco no futuro)." "Event bus in-process para comunicação entre serviços (decidido em 2025-10, motivação: desacoplamento sem complexidade de message broker)."

**stack-definida.md** — Approved stack with versions. Python 3.11+, FastAPI, SQLAlchemy 2.x, React (frontend), PostgreSQL (production). Explicitly NOT allowed: Flask, Django, Vue.js, Angular, MongoDB.

**principios-tecnicos.md** — Core principles:
1. "Chamadas a serviços externos DEVEM ser assíncronas (httpx.AsyncClient, nunca requests síncrono). Motivação: timeout de 30s no gateway de pagamento causou cascading failures em produção (incidente 2025-08)."
2. "Functional core, imperative shell — lógica de negócio pura, side effects na borda."
3. "Imutabilidade por padrão — preferir dataclasses frozen, evitar mutação de estado."
4. "Error handling via Result types quando possível, exceções apenas para condições excepcionais."
5. "Queries analíticas podem usar SQL raw (sem ORM) para performance."

**padroes-testes.md** — Test standards:
1. "Pirâmide de testes: muitos unitários, alguns de integração, poucos E2E."
2. "NUNCA mockar o banco de dados. Testes de integração devem usar banco real (SQLite in-memory)."
3. "Testes de integração obrigatórios para toda fronteira externa."
4. "Cobertura mínima: 80% para serviços, 70% para rotas."

- [ ] **Step 2: Create style docs**

**guia-estilo-codigo.md** — Naming: snake_case for functions/variables, PascalCase for classes. File organization: one class per file for models, grouped by feature for services.

**convencoes-documentacao.md** — Docstrings in Portuguese, Google style. READMEs required for each module. Changelog updated with each PR.

**padroes-formatacao.md** — Line length 100 chars, imports sorted with isort, type annotations required for all public functions.

- [ ] **Step 3: Commit**

```bash
git add validation-agent/docs/tecnico/ validation-agent/docs/estilo/
git commit -m "feat(validation-agent): technical principles and style documentation"
```

---

### Task 20: Validation Agent — Scenario Prompts

**Files:**
- Create: `validation-agent/scenarios/scenario-1/step-1-implement.md`
- Create: `validation-agent/scenarios/scenario-1/step-2-validate.md`
- Create: `validation-agent/scenarios/scenario-1/step-3-brainstorm.md`
- Create: `validation-agent/scenarios/scenario-1/expected-findings.md`
- Create: `validation-agent/scenarios/scenario-2/step-1-implement.md`
- Create: `validation-agent/scenarios/scenario-2/step-2-validate.md`
- Create: `validation-agent/scenarios/scenario-2/step-3-brainstorm.md`
- Create: `validation-agent/scenarios/scenario-2/expected-findings.md`
- Create: `validation-agent/scenarios/scenario-3/step-1-implement.md`
- Create: `validation-agent/scenarios/scenario-3/step-2-validate.md`
- Create: `validation-agent/scenarios/scenario-3/step-3-brainstorm.md`
- Create: `validation-agent/scenarios/scenario-3/expected-findings.md`

**Depends on:** Tasks 18, 19 (needs to know what's in the docs to craft conflicting prompts)

- [ ] **Step 1: Create scenario 1 prompts (payment gateway — primary demo)**

Use the exact prompt content from the design spec Section 5 "Scenario prompt content specification" for step-1, step-2, and step-3.

**expected-findings.md** should list:
- `principios-tecnicos.md`: chamada HTTP síncrona com requests viola princípio de async obrigatório para serviços externos
- `requisitos-lgpd.md`: armazenar CPF em tabela de analytics viola princípio de minimização de dados
- `politica-dados.md`: CPF é dado RESTRITO, não pode ir para tabela analítica
- `restricoes-integracao.md`: integração com Pagar.me deve usar circuit breaker (não mencionado na implementação)

- [ ] **Step 2: Create scenario 2 prompts (React→Vue migration — backup)**

**step-1-implement.md**: Ask Claude to create a migration plan file and update package.json to replace React with Vue. Also ask to refactor test files to use mocks instead of real DB.

**step-2-validate.md**: Standard validation prompt (same as scenario 1 step-2).

**step-3-brainstorm.md**: "O time quer migrar de React pra Vue e usar mocks nos testes de integração pra acelerar a suite..."

**expected-findings.md**: `stack-definida.md` (React approved, Vue not), `padroes-testes.md` (no mocking DB), `decisoes-produto.md` (rewrite out of scope until Q3 2026)

- [ ] **Step 3: Create scenario 3 prompts (raw SQL analytics — backup)**

**step-1-implement.md**: Ask Claude to create an analytics endpoint that queries production DB directly with raw SQL, returning customer PII (nome, email, CPF) grouped by region.

**step-2-validate.md**: Standard validation prompt.

**step-3-brainstorm.md**: "Quero adicionar um endpoint de relatório de vendas por região com dados do cliente..."

**expected-findings.md**: `requisitos-lgpd.md` (PII in analytics), `politica-dados.md` (CPF is restricted). Note: `principios-tecnicos.md` says "queries analíticas podem usar SQL raw" — so that part is actually COMPLIANT. The agent should correctly identify this nuance.

- [ ] **Step 4: Commit**

```bash
git add validation-agent/scenarios/
git commit -m "feat(validation-agent): demo scenario prompts with expected findings"
```

---

### Task 21: End-to-End Smoke Test

**Depends on:** All previous tasks

- [ ] **Step 1: Verify FastAPI app starts and serves requests**

```bash
cd demo && uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
sleep 2
curl -s -H "X-API-Key: demo-api-key-2024" http://localhost:8000/health
curl -s -H "X-API-Key: demo-api-key-2024" http://localhost:8000/api/v1/customers | head -20
kill %1
```

Expected: health returns `{"status": "ok"}`, customers returns paginated empty list

- [ ] **Step 2: Verify all tests pass**

```bash
cd demo && python -m pytest -v --tb=short
```

Expected: all tests pass

- [ ] **Step 3: Verify DBT builds**

```bash
cd demo/dbt && dbt seed && dbt build
```

Expected: seeds loaded, models built, no errors

- [ ] **Step 4: Verify MkDocs serves**

```bash
cd demo && pip install mkdocs-material pymdown-extensions && mkdocs build
```

Expected: builds without errors (docs/ may be empty, that's fine)

- [ ] **Step 5: Verify validation-agent CLAUDE.md is readable**

```bash
cat validation-agent/CLAUDE.md | head -30
```

Verify it contains the dual mode instructions and subagent dispatch.

- [ ] **Step 6: Final commit**

```bash
git add -A && git status
```

Review any unstaged files. Commit if needed.

```bash
git commit -m "chore: end-to-end smoke test verification"
```
