from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey, func, Numeric, UniqueConstraint
from datetime import datetime
from decimal import Decimal

from database import Base


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'), ondelete='CASCADE')
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    quantity: Mapped[int] 
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    cart: Mapped['Cart'] = relationship(back_populates='items')
    product: Mapped['Product'] = relationship(back_populates='cart_items')

    __table_args__ = (UniqueConstraint('cart_id', 'product_id', name='uq_cartitem_product'),)


    def __repr__(self):
        return f'CartItem(id = {self.id} || cart = {self.cart_id} ||)'