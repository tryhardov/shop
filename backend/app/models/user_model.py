from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey, func, UniqueConstraint, String
from datetime import datetime
from decimal import Decimal

from database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hash_password: Mapped[str] 
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    cart: Mapped['Cart'] = relationship(back_populates='user', passive_deletes=True)


    def __repr__(self):
        return f'User(id = {self.id} || username = {self.username})'