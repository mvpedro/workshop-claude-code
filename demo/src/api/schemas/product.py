from datetime import datetime
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
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
