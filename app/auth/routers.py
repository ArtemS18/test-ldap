from fastapi import APIRouter

from app.auth.schemas.user_autho import UserCredentials, SuccessAuthoResponse
from app.lib.web.models import Request

router = APIRouter(prefix="/auth", tags=["Авторизация LDAP"])


# @router.post("/")
# async def handel_autho(credentials: UserCredentials) -> SuccessAuthoResponse: ...


@router.get("/")
async def test(req: Request):
    users = await req.app.store.autho_repo.find_all_users()
    return {"status": "ok", "users": users["users"]}
