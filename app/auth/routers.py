from fastapi import APIRouter, HTTPException, status

from app.auth.schemas.user_autho import UserCredentials, SuccessAuthoResponse
from app.lib.web.models import Request
from app.lib.web import exeptions

router = APIRouter(prefix="/auth", tags=["Авторизация LDAP"])


# @router.post("/")
# async def handel_autho(credentials: UserCredentials) -> SuccessAuthoResponse: ...


@router.post("/")
async def autho_handler(
    credentials: UserCredentials, req: Request
) -> SuccessAuthoResponse:
    user_dn = await req.app.store.autho_repo.get_user_dn(credentials.username)
    if not user_dn:
        raise exeptions.USER_NOT_FOUND

    is_user_authoreized = await req.app.store.autho_repo.autho_user(
        user_dn, credentials.password
    )

    if not is_user_authoreized:
        raise exeptions.BAD_CREDENSIALS

    return SuccessAuthoResponse(
        access_token="access",
        refresh_token="refresh",
    )
