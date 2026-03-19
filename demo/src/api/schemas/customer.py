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
