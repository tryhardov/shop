from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from app.schemas.category_schema import CategoryResponse
from app.services.category_service import CategoryService


router = APIRouter(
    prefix='/api/categories',
    tags=['categories']
)


@router.get('', response_model=list[CategoryResponse], status_code=200)
async def get_all_categories(db: AsyncSession = Depends(get_db)) -> list[CategoryResponse]:
    service = CategoryService(db)
    return await service.get_all_categories()