import jwt

from config import settings
from app.core.auth import create_access_token, get_current_user
from app.core.security import hash_password, verify_password


class TestJwtToken:
    def test_token(self):
        user_id = 7
        token = create_access_token(user_id)
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert payload['sub'] == str(user_id)
        assert get_current_user(token) == user_id


class TestHashPasswords:
    def test_password(self):
        password = 'secretpassword123'
        hashed_password = hash_password(password)

        assert password != hashed_password
        assert isinstance(hashed_password, str)
        assert verify_password(password, hashed_password) is True