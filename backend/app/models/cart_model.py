from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey, func, UniqueConstraint
from datetime import datetime

from database import Base


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True, ondelete='CASCADE')
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    items: Mapped[list['CartItem']] = relationship(back_populates='cart', passive_deletes=True)
    user: Mapped['User'] = relationship(back_populates='cart')


    def __repr__(self):
        return f'Cart(id = {self.id} || user = {self.user_id})'