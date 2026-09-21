from sqlalchemy import select

from .factories.auth_factory import DEFAULT_TEST_PASSWORD
from app.models.user_model import User
from app.models.cart_model import Cart
from app.core.auth import get_current_user



class TestCreateUser:
    async def test_create_user_with_create_cart(self, client, db_session):
        response = await client.post('/api/user/create',
                                     json={'username': 'newuser', 'password': 'password123'})

        assert response.status_code == 201
        assert response.json()['username'] == 'newuser'

        db_cart = await db_session.execute(select(Cart).where(Cart.user_id==response.json()['id']))
        assert db_cart.scalar_one_or_none() is not None


    async def test_duplicate_username_return_error(self, client, user):
        response = await client.post('/api/user/create',
                                     json={'username': user.username, 'password': 'anotherpassword'})
        assert response.status_code == 400


    async def test_missing_fields_return_error(self, client):
        response = await client.post('/api/user/create', json={'username': 'username'})
        assert response.status_code == 422



class TestLoginUser:
    async def test_authenticate_user(self, client, user):
        response = await client.post('/api/user/login', json = {'username': user.username,
                                                                'password': DEFAULT_TEST_PASSWORD})
        data = response.json()

        assert response.status_code == 200
        assert data['token_type'] == 'bearer'
        assert data['access_token']


    async def test_authenticate_with_wrong_username(self, client, user):
        response = await client.post('/api/user/login', json = {'username': 'non-existent',
                                                                'password': DEFAULT_TEST_PASSWORD})
        assert response.status_code == 401


    async def test_authenticate_with_wrong_password(self, client, user):
        response = await client.post('/api/user/login', json = {'username': user.username,
                                                                'password': 'non-existent'})
        assert response.status_code == 401



class TestRemoveUser:
    async def test_remove_user_with_valid_credentials(self, client, user, auth_headers, db_session):
        response = await client.delete('/api/user/remove', headers=auth_headers)
        result = await db_session.execute(select(User).where(User.id==user.id))
        deleted_user = result.scalar_one_or_none()

        assert response.status_code == 204
        assert deleted_user is None


    async def test_remove_user_without_token_return_error(self, client, user):
        response = await client.delete('/api/user/remove')
        assert response.status_code == 401


    async def test_remove_user_with_invalid_token_return_error(self, client, user):
        response = await client.delete('/api/user/remove', headers={'Authorization': 'Bearer invalid_token'})
        assert response.status_code == 401