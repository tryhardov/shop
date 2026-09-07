from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)


class CategoryCreate(CategoryBase):
    pass 


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)