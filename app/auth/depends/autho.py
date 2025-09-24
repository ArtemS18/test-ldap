from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

from app.auth.depends.services import JWTServiceDepend


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth", refreshUrl="/auth/refresh")


def verifi_user(jwt_service: JWTServiceDepend, token: str = Depends(oauth2_scheme)):
    user = jwt_service.verifi_jwt_access_token(token)
    return user
