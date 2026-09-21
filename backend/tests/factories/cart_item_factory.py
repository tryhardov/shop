import factory
import random

from app.models.cart_item_model import CartItem


class CartItemFactory(factory.Factory):
    class Meta:
        model = CartItem