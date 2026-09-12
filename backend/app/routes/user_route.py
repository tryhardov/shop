from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from app.schemas.user_schema import UserResponse, UserCreate, UserLogin
from app.services.user_service import UserService


router = APIRouter(
    prefix='/api/user',
    tags=['user']
)


@router.post('/login', response_model=UserResponse, status_code=200)
async def authenticate_user(data: UserLogin, db: AsyncSession = Depends(get_db)) -> UserResponse:
    service = UserService(db)
    return await service.authenticate_user(data.username, data.password)


@router.post('/create', response_model=UserResponse, status_code=201)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    service = UserService(db)
    return await service.create_user(data)


@router.delete('/remove', status_code=204)
async def remove_user(user_id: int, db: AsyncSession = Depends(get_db)) -> None:
    service = UserService(db)
    return await service.delete_user(user_id)