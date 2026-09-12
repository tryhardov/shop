from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: str | None = Field(None, max_length=100)
    password: str | None = Field(None, min_length=8)


class UserLogin(UserBase):
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)