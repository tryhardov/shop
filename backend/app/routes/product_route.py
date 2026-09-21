from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from app.schemas.product_schema import ProductResponse
from app.services.product_service import ProductService


router = APIRouter(
    prefix='/api/products',
    tags=['products']
)


@router.get('', response_model=list[ProductResponse], status_code=200)
async def get_all_products(db: AsyncSession = Depends(get_db)) -> list[ProductResponse]:
    service = ProductService(db)
    return await service.get_all_products()


@router.get('/{product_slug}', response_model=ProductResponse, status_code=200)
async def get_product_by_slug(product_slug: str, db: AsyncSession = Depends(get_db)) -> ProductResponse:
    service = ProductService(db)
    return await service.get_product_by_slug(product_slug)


@router.get('/category/{category_id}', response_model=list[ProductResponse], status_code=200)
async def get_products_by_category(category_id: int, db: AsyncSession = Depends(get_db)) -> list[ProductResponse]:
    service = ProductService(db)
    return await service.get_product_by_category(category_id)