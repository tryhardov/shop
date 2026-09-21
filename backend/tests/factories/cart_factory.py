import factory

from app.models.cart_model import Cart


class CartFactory(factory.Factory):
    class Meta:
        model = Cart