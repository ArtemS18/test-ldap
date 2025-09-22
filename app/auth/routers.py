from fastapi import APIRouter, HTTPException, status

from app.auth.depends.services import AuthoServiceDepend, JWTServiceDepend
from app.auth.schemas.user_autho import UserCredentials, SuccessAuthoResponse
from app.lib.web.models import Request
from app.lib.web import exeptions

router = APIRouter(prefix="/auth", tags=["Авторизация LDAP"])


# @router.post("/")
# async def handel_autho(credentials: UserCredentials) -> SuccessAuthoResponse: ...


@router.post("/")
async def autho_handler(
    credentials: UserCredentials,
    autho_service: AuthoServiceDepend,
    jwt_service: JWTServiceDepend,
) -> SuccessAuthoResponse:
    user = await autho_service.ldap_autho(credentials.username, credentials.password)
    access_token = await jwt_service.create_jwt_access_token(user)
    refresh_token = await jwt_service.create_jwt_refresh_token(user)
    return SuccessAuthoResponse(
        access_token=access_token, refresh_token=refresh_token, role=str(user.role_id)
    )
