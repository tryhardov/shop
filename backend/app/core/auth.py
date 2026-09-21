from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from config import settings
import jwt
from jwt.exceptions import InvalidTokenError
import datetime


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/user/login')


def create_access_token(user_id: int):
    payload = {
        'sub': str(user_id),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5)
    }

    return jwt.encode(payload, settings.secret_key, settings.algorithm)


def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Couldn't validate credentials"
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get('sub')

        if user_id is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    return int(user_id)