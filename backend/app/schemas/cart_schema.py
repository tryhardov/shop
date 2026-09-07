from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime

from app.schemas.cart_item_schema import CartItemResponse


class CartBase(BaseModel):
    user_id: int


class CartCreate(CartBase):
    pass 


class CartResponse(CartBase):
    id: int
    created_at: datetime
    updated_at: datetime
    items: list[CartItemResponse] 
    total_items_quantity: int = Field(..., ge=0)
    total_price: Decimal = Field(..., max_digits=10, decimal_places=2, ge=0)

    model_config = ConfigDict(from_attributes=True)