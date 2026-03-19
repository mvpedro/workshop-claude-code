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
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    setup_event_handlers()
    bus.subscribe(OrderCreated, notification_service.handle_order_created)
    bus.subscribe(OrderStatusChanged, notification_service.handle_status_changed)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    description="API REST para gestão de clientes, produtos e pedidos",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimiterMiddleware)
app.add_middleware(AuthMiddleware)

app.include_router(customers.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
