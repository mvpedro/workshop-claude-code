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
