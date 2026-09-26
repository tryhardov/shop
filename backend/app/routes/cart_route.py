from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from app.services.cart_service import CartService
from app.schemas.cart_schema import CartResponse
from app.schemas.cart_item_schema import CartItemCreate, CartItemUpdate, CartItemResponse
from app.core.auth import get_current_user


router = APIRouter(
    prefix='/api/cart',
    tags=['cart']
)


@router.get('', response_model=CartResponse, status_code=200)
async def get_cart(user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> CartResponse:
    service = CartService(db)
    return await service.get_cart(user_id)


@router.post('/add', response_model=CartItemResponse, status_code=201)
async def add_item(data: CartItemCreate, user_id: int = Depends(get_current_user),
                   db: AsyncSession = Depends(get_db)) -> CartItemResponse:
    service = CartService(db)
    return await service.add_item(user_id, data)


@router.patch('/update/{cart_item_id}', response_model=CartItemResponse|None, status_code=200)
async def update_item(cart_item_id: int, data: CartItemUpdate, user_id: int = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)) -> CartItemResponse | None:
    service = CartService(db)
    return await service.update_item(user_id, cart_item_id, data.quantity)


@router.delete('/remove/cart_item/{cart_item_id}', status_code=204)
async def delete_cart_item(cart_item_id: int, user_id: int = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)) -> None:
    service = CartService(db)
    return await service.delete_cart_item(user_id, cart_item_id)


@router.delete('/remove/cart', status_code=204)
async def clear_cart(user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> None:
    service = CartService(db)
    return await service.delete_all_cart_items(user_id)