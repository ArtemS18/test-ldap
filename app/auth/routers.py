from typing import Annotated
from fastapi import APIRouter
from fastapi import Form

from app.auth.schemas.logout import LogoutRequest
from app.lib.web.swagger import jwt_unauthorized_responses, auth_unauthorized_responses
from app.auth.depends.services import AuthoServiceDepend, JWTServiceDepend
from app.auth.schemas.user_autho import UserCredentials, SuccessAuthoResponse
from app.auth.schemas.refresh_token import (
    RefreshTokenRequest,
    SuccessRefreshResponse,
)

router = APIRouter(prefix="/auth", tags=["OAuth2 Авторизация"])


@router.post(
    "/",
    responses=auth_unauthorized_responses,
    summary="Авторизация через LDAP",
    response_model=SuccessAuthoResponse,
)
async def autho_handler(
    credentials: Annotated[UserCredentials, Form()],
    autho_service: AuthoServiceDepend,
    jwt_service: JWTServiceDepend,
):
    user = await autho_service.ldap_autho(credentials.username, credentials.password)
    access_token = await jwt_service.create_jwt_access_token(user)
    refresh_token = await jwt_service.create_and_save_jwt_refresh_token(user)
    return SuccessAuthoResponse(
        access_token=access_token, refresh_token=refresh_token, role=user.role
    )


@router.post(
    "/refresh",
    response_model=SuccessRefreshResponse,
    responses=jwt_unauthorized_responses,
)
async def refresh_token_handler(
    refresh_schema: RefreshTokenRequest,
    jwt_service: JWTServiceDepend,
):
    new_tokens = await jwt_service.refresh_jwt_tokens(refresh_schema.refresh_token)
    return new_tokens


@router.post("/logout", status_code=204, responses=jwt_unauthorized_responses)
async def logout_handler(
    logout_schema: LogoutRequest,
    jwt_service: JWTServiceDepend,
):
    await jwt_service.delete_jwt_refresh_token(
        logout_schema.refresh_token, delete_all_tokens=logout_schema.all
    )
