from app.auth.services.autho import AuthoService
from app.auth.services.jwt_tokens import JWTService
from app.lib.web.models import Request
from typing import Annotated
from fastapi import Depends


def get_jwt_service(req: Request):
    jwt_config = req.app.config.web.jwt
    jwt_repo = req.app.store.jwt_repo
    return JWTService(jwt_config, jwt_repo)


def get_autho_service(req: Request, jwt_service: JWTService = Depends(get_jwt_service)):
    ldap = req.app.store.autho_repo
    user_repo = req.app.store.user_repo
    jwt_repo = req.app.store.jwt_repo
    return AuthoService(ldap, jwt_service, user_repo=user_repo, jwt_repo=jwt_repo)


JWTServiceDepend = Annotated[JWTService, Depends(get_jwt_service)]
AuthoServiceDepend = Annotated[AuthoService, Depends(get_autho_service)]
