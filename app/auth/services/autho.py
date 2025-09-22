from datetime import datetime, timedelta
from app.auth.schemas.refresh_tokens import RefreshToken, RefreshTokenCreate
from app.auth.schemas.user_autho import SuccessAuthoResponse
from app.auth.services.jwt_tokens import JWTService
from app.lib.web import exeptions
from app.store.ldap.repository import UserAuthoRepository
from app.store.postgres.repository.jwt_repo import JWTRepository
from app.store.postgres.repository.user_repo import UserRepository
from app.users.schemas.users import User


class AuthoService:
    def __init__(
        self,
        autho_user: UserAuthoRepository,
        jwt_service: JWTService,
        user_repo: UserRepository,
        jwt_repo: JWTRepository,
    ):
        self.autho_user = autho_user
        self.jwt_service = jwt_service
        self.user_repo = user_repo
        self.jwt_repo = jwt_repo

    async def ldap_autho(self, username, password) -> User:
        user_dn = await self.autho_user.get_user_dn(username)
        if not user_dn:
            raise exeptions.USER_NOT_FOUND

        if not await self.autho_user.autho_user(user_dn, password):
            raise exeptions.BAD_CREDENSIALS

        user = await self.user_repo.get_user_by_username(username)
        if not user:
            raise exeptions.USER_NOT_FOUND
        return User.model_validate(user)
