from typing import Literal
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

from app.auth.depends.services import JWTServiceDepend
from app.users.entities.users import User
from app.lib.web import exeptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth", refreshUrl="/auth/refresh")


def verifi_user(jwt_service: JWTServiceDepend, token: str = Depends(oauth2_scheme)):
    user = jwt_service.verifi_jwt_access_token(token)
    return user


def validate_role(*allowed_roles: tuple[Literal["User", "Admin", "Moderator"]]):
    def wrapper(user: User = Depends(verifi_user)):
        if user.role.name not in allowed_roles:
            raise exeptions.FORBIDDEN_ROLE
        return user

    return wrapper
