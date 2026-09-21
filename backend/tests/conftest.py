import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport
import random

from config import settings
from database import Base, get_db
from main import app
from app.core.auth import create_access_token
from .factories import create, create_batch, ProductFactory, CategoryFactory, UserFactory, CartFactory, CartItemFactory


test_engine = create_async_engine(settings.test_database_url, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope='function')
async def init_test_db():   
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='function')
async def db_session(init_test_db):
    async with TestSessionLocal() as db_session:
        yield db_session

        await db_session.rollback()


async def override_db_session():
    async with TestSessionLocal() as db_session:
        yield db_session


@pytest_asyncio.fixture(scope='function')
async def client(init_test_db):
    app.dependency_overrides[get_db] = override_db_session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test'
    ) as client:
        yield client
    app.dependency_overrides.clear()



#Фикстуры для тестирования
@pytest_asyncio.fixture
async def category(db_session):
    return await create(CategoryFactory, db_session)


@pytest_asyncio.fixture
async def categories(db_session):
    return await create_batch(CategoryFactory, db_session, qt=3)


@pytest_asyncio.fixture
async def product(db_session, category):
    return await create(ProductFactory, db_session, category_id=category.id)


@pytest_asyncio.fixture
async def products(db_session, category):
    return await create_batch(ProductFactory, db_session, qt=3, category_id=category.id)


@pytest_asyncio.fixture
async def user(db_session):
    return await create(UserFactory, db_session)


@pytest_asyncio.fixture
async def auth_headers(db_session, user):
    token = create_access_token(user.id)
    return {'Authorization': f'Bearer {token}'}


@pytest_asyncio.fixture
async def cart(user, db_session):
    return await create(CartFactory, db_session, user_id=user.id)


@pytest_asyncio.fixture
async def cart_item(cart, product, db_session):
    quantity = random.randint(1, 8)
    return await create(CartItemFactory, db_session, cart_id=cart.id,
                        product_id=product.id, quantity=quantity, price=product.price*quantity)


@pytest_asyncio.fixture
async def cart_items(cart, products, db_session):
    items = []
    for product in products:
        quantity = random.randint(1, 8)
        item = await create(CartItemFactory, db_session, cart_id=cart.id, product_id=product.id,
                                  quantity=quantity, price=product.price*quantity)
        items.append(item)
    return items