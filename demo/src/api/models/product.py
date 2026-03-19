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
