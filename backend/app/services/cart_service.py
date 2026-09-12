from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repositories.cart_repository import CartRepository
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart_schema import CartResponse
from app.schemas.cart_item_schema import CartItemCreate, CartItemResponse


class CartService:
    def __init__(self, db: AsyncSession):
        self.cart_repository = CartRepository(db)
        self.user_repository = UserRepository(db)
        self.product_repository = ProductRepository(db)


    async def get_cart(self, user_id: int) -> CartResponse:
        db_cart = await self.cart_repository.get_cart_by_user(user_id)

        if db_cart is None:
            raise HTTPException(404, 'Cart not found')

        total_items_quantity = sum(item.quantity for item in db_cart.items)
        total_price = sum(item.price for item in db_cart.items)

        return CartResponse(
            user_id=db_cart.user_id,
            id=db_cart.id,
            items=db_cart.items,
            total_items_quantity=total_items_quantity,
            total_price=total_price,
            created_at=db_cart.created_at,
            updated_at=db_cart.updated_at
        )


    async def add_item(self, user_id: int, data: CartItemCreate) -> CartItemResponse:
        db_product = await self.product_repository.get_product_by_id(data.product_id)

        if db_product is None:
            raise HTTPException(404, 'Product not found')

        db_cart = await self.cart_repository.get_cart_by_user(user_id)

        if db_cart is None:
            raise HTTPException(404, 'Cart not found')

        db_cart_item = await self.cart_repository.get_cart_item_by_product_and_cart(db_product.id, db_cart.id)

        if db_cart_item is None:
            price = db_product.price * data.quantity
            cart_item = await self.cart_repository.add_product_in_cart(db_cart.id, price, data)
            return CartItemResponse.model_validate(cart_item)
        else:
            quantity = data.quantity + db_cart_item.quantity
            price = db_product.price * quantity
            cart_item = await self.cart_repository.update_cart_item_in_cart(db_cart_item.id, quantity, price)
            return CartItemResponse.model_validate(cart_item)


    async def update_item(self, cart_item_id: int, quantity: int) -> CartItemResponse | None:
        db_cart_item = await self.cart_repository.get_cart_item_by_id(cart_item_id)

        if db_cart_item is None:
            raise HTTPException(404, 'Cart item not found')

        quantity += db_cart_item.quantity

        if quantity <= 0:
            await self.cart_repository.delete_cart_item_by_id(cart_item_id)
            return None

        price = db_cart_item.product.price * quantity

        cart_item = await self.cart_repository.update_cart_item_in_cart(cart_item_id, quantity, price)

        return CartItemResponse.model_validate(cart_item)


    async def delete_cart_item(self, cart_item_id: int) -> None:
        db_cart_item = await self.cart_repository.get_cart_item_by_id(cart_item_id)

        if db_cart_item is None:
            raise HTTPException(404, 'Cart item not found')

        await self.cart_repository.delete_cart_item_by_id(cart_item_id)


    async def delete_all_cart_items(self, user_id: int) -> None:
        db_cart = await self.cart_repository.get_cart_by_user(user_id)

        if db_cart is None: 
            raise HTTPException(404, 'Cart not found')

        await self.cart_repository.delete_all_cart_items(db_cart.id)