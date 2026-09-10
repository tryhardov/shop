from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.models.cart_model import Cart
from app.core.security import hash_password


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_user_by_id(self, user_id: int) -> User | None:
        db_user = await self.db.execute(
            select(User)
            .where(User.id==user_id)
        )

        return db_user.scalar_one_or_none()


    async def get_user_by_username(self, username: str) -> User | None:
        db_user = await self.db.execute(
            select(User)
            .where(User.username==username)
        )

        return db_user.scalar_one_or_none()


    async def create_user(self, data: UserCreate) -> User:
        user_data = data.model_dump(exclude={'password'})
        user_data['hash_password'] = hash_password(data.password)

        user = User(**user_data)

        self.db.add(user)
        await self.db.flush()

        cart = Cart(user_id=user.id)

        self.db.add(cart)
        await self.db.commit()
        await self.db.refresh(user)
        await self.db.refresh(cart)

        return user
    

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user_by_id(user_id)

        await self.db.delete(user)
        await self.db.commit()