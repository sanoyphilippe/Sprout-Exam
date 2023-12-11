import base64
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from app.core.config import settings

class Settings(BaseModel):
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = base64.b64decode(
        settings.JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
        settings.JWT_PRIVATE_KEY).decode('utf-8')

@AuthJWT.load_config
def get_config():
    return Settings()

class UserNotAdmin(Exception):
    pass

class UserNotFound(Exception):
    pass

def require_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        username = Authorize.get_jwt_subject()

        if not username:
            raise UserNotFound('User no longer exist')

        if username != settings.SUPER_ADMIN_USERNAME:
            raise UserNotAdmin('User is not an admin')

    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User no longer exist')
        if error == 'UserNotAdmin':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not an admin')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')
    return username

