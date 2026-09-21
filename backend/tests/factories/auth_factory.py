import factory

from app.models.user_model import User
from app.core.security import hash_password


DEFAULT_TEST_PASSWORD = 'testpassword123'

class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'username_{n}')
    hash_password = factory.LazyFunction(lambda: hash_password(DEFAULT_TEST_PASSWORD))