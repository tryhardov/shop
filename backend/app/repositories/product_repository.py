from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_model import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all_products(self) -> list[Product]:
        db_products = await self.db.execute(
            select(Product)
        )

        return db_products.scalars().all()


    async def get_product_by_id(self, product_id: int) -> Product | None:
        db_product = await self.db.execute(
            select(Product)
            .where(Product.id==product_id)
        )

        return db_product.scalar_one_or_none()

    
    async def get_product_by_slug(self, product_slug: str) -> Product | None:
        db_product = await self.db.execute(
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.slug==product_slug)
        )

        return db_product.scalar_one_or_none()


    async def get_products_by_category(self, category_id: int) -> list[Product]:
        db_products = await self.db.execute(
            select(Product)
            .where(Product.category_id==category_id)
        )

        return db_products.scalars().all()