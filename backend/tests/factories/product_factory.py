import factory

from app.models.product_model import Product



class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'product_{n}')
    slug = factory.Sequence(lambda n: f'product-{n}')
    price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)