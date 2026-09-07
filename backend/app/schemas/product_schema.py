from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime


class ProductBase(BaseModel):
    category_id: int
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    description: str | None = None
    price: Decimal = Field(..., max_digits=10, decimal_places=2)
    image_url: str | None = None


class ProductCreate(ProductBase):
    pass 


class ProductUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = Field(None, max_length=100)
    slug: str | None = Field(None, max_length=100)
    description: str | None = None
    price: Decimal | None = Field(None, max_digits=10, decimal_places=2)
    image_url: str | None = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)