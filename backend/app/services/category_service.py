from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryResponse


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.category_repository = CategoryRepository(db)


    async def get_all_categories(self) -> list[CategoryResponse]:
        categories = await self.category_repository.get_all_categories()

        return [CategoryResponse.model_validate(cat) for cat in categories]