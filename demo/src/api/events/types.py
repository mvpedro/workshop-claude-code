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
