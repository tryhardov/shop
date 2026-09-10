from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.schemas.product_schema import ProductResponse
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, db: AsyncSession):
        self.product_repository = ProductRepository(db)


    async def get_all_products(self) -> list[ProductResponse]:
        products = await self.product_repository.get_all_products()

        return [ProductResponse.model_validate(product) for product in products]


    async def get_product_by_slug(self, product_slug: str) -> ProductResponse:
        product = await self.product_repository.get_product_by_slug(product_slug)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f'Product with slug {product_slug} not found'
            )

        return ProductResponse.model_validate(product)


    async def get_product_by_category(self, category_id: int) -> list[ProductResponse]:
        products = await self.product_repository.get_products_by_category(category_id)

        return [ProductResponse.model_validate(product) for product in products]