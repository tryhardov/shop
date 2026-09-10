from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cart_model import Cart
from app.models.cart_item_model import CartItem
from app.schemas.cart_item_schema import CartItemCreate
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository


class CartRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_repository = ProductRepository(db)
        self.user_repository = UserRepository(db)


    async def get_cart_by_user(self, user_id: int) -> Cart | None:
        db_cart = await self.db.execute(
            select(Cart)
            .options(selectinload(Cart.items).selectinload(CartItem.product),
                     selectinload(Cart.user))
            .where(Cart.user_id==user_id)
        )

        return db_cart.scalar_one_or_none()


    async def get_cart_by_id(self, cart_id: int) -> Cart | None:
        db_cart = await self.db.execute(
            select(Cart)
            .where(Cart.id==cart_id)
        )

        return db_cart.scalar_one_or_none()


    async def get_cart_item_by_id(self, cart_item_id: int) -> CartItem | None:
        db_cart_item = await self.db.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.id==cart_item_id)
        )

        return db_cart_item.scalar_one_or_none()


    async def get_cart_item_by_product_and_cart(self, product_id: int, cart_id: int) -> CartItem | None:
        db_cart_item = await self.db.execute(
            select(CartItem)
            .where(CartItem.product_id==product_id, CartItem.cart_id==cart_id)
        )

        return db_cart_item.scalar_one_or_none()


    async def add_product_in_cart(self, cart_id: int, price, data: CartItemCreate) -> CartItem:
        cart_item = CartItem(cart_id=cart_id, product_id=data.product_id, quantity=data.quantity, price=price)

        self.db.add(cart_item)
        await self.db.commit()
        await self.db.refresh(cart_item)

        return cart_item


    async def update_cart_item_in_cart(self, cart_item_id: int, quantity: int, price) -> CartItem | None:
        db_cart_item = await self.get_cart_item_by_id(cart_item_id)

        db_cart_item.price = price
        db_cart_item.quantity = quantity

        await self.db.commit()
        await self.db.refresh(db_cart_item)

        return db_cart_item


    async def delete_cart_item_by_id(self, cart_item_id: int) -> None:
        db_cart_item = await self.get_cart_item_by_id(cart_item_id)

        await self.db.delete(db_cart_item)
        await self.db.commit()


    async def delete_all_cart_items(self, cart_id: int) -> None:
        db_cart_items = await self.db.execute(
            select(CartItem)
            .where(CartItem.cart_id==cart_id)
        )

        cart_items = db_cart_items.scalars().all()

        for item in cart_items:
            await self.db.delete(item)

        await self.db.commit()