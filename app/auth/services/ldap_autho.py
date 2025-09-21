from fastapi import HTTPException, status
from app.auth.schemas.user_autho import SuccessAuthoResponse
from app.store.ldap.repository import UserAuthoRepository


class AuthoService:
    def __init__(self, user_repo: UserAuthoRepository):
        self.user_repo = user_repo

    async def ldap_autho(self, username, password):
        user_dn = await self.user_repo.get_user_dn(username)
        if not user_dn:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if not await self.user_repo.autho_user(user_dn, password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return SuccessAuthoResponse(
            access_token="access",
            refresh_token="refresh",
        )
