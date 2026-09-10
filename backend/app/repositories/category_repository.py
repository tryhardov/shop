from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category_model import Category


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all_categories(self) -> list[Category]:
        db_categories = await self.db.execute(
            select(Category)
        )

        return db_categories.scalars().all()