import factory

from app.models.category_model import Category



class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'category_{n}')
    slug = factory.Sequence(lambda n: f'category-{n}')