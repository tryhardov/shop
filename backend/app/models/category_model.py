from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String

from database import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    products: Mapped[list['Product']] = relationship(back_populates='category')


    def __repr__(self):
        return f'Category(id = {self.id} || name = {self.name})'