from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserResponse
from app.core.security import verify_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)


    async def create_user(self, data: UserCreate) -> UserResponse:
        db_user = await self.user_repository.get_user_by_username(data.username)

        if db_user is not None:
            raise HTTPException(400, 'Username already taken')

        user = await self.user_repository.create_user(data)

        return UserResponse.model_validate(user)


    async def authenticate_user(self, username: str, password: str) -> UserResponse:
        db_user = await self.user_repository.get_user_by_username(username)

        if db_user is None or not verify_password(password, db_user.hash_password):
            raise HTTPException(401, 'Invalid username or password')

        return UserResponse.model_validate(db_user)


    async def delete_user(self, user_id: int) -> None:
        db_user = await self.user_repository.get_user_by_id(user_id)

        if db_user is None:
            raise HTTPException(404, 'User not found')

        await self.user_repository.delete_user(user_id)