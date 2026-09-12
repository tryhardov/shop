from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime


class CartItemBase(BaseModel):
    cart_id: int
    product_id: int
    quantity: int = Field(..., gt=0)
    price: Decimal = Field(..., max_digits=10, decimal_places=2, ge=0)


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemResponse(CartItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)