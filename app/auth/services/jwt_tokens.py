from datetime import datetime, timedelta, timezone
import logging
import uuid
import jwt
from app.auth.services.dto import RefreshTokenCreate
from app.auth.schemas.refresh_token import (
    SuccessRefreshResponse,
)
from app.auth.models.refresh_tokens import RefreshTokenORM
from app.store.postgres.repository.jwt_repo import JWTRepository
from app.users.entities.departments import Department
from app.users.entities.roles import Role
from app.users.entities.users import User
from app.web.config import JWTConfig
from app.lib.web import exeptions

log = logging.getLogger(name=__name__)


class JWTService:
    def __init__(self, config: JWTConfig, jwt_repo: JWTRepository):
        self.config = config
        self.jwt_repo = jwt_repo

    def create_token(
        self,
        payload: dict[str, any],
        expire: int | None = None,
        expire_at: datetime | None = None,
    ):
        encoder = payload.copy()
        if not encoder.get("token_type"):
            encoder.update({"token_type": "access"})

        now = datetime.now(timezone.utc)
        if expire_at is None:
            encoder.update(
                {
                    "exp": now + timedelta(minutes=expire)
                    if expire
                    else now + timedelta(minutes=self.config.access_expire)
                }
            )
        else:
            encoder.update({"exp": expire_at})
        token = jwt.encode(encoder, self.config.secret_key, self.config.algorithm)
        return token

    def verifi_token(self, token: str):
        try:
            payload: dict = jwt.decode(
                token, self.config.secret_key, self.config.algorithm
            )
        except jwt.ExpiredSignatureError:
            raise exeptions.JWT_TOKEN_EXPIRED
        except jwt.InvalidTokenError:
            raise exeptions.JWT_BASE_EXEPTION
        except jwt.DecodeError:
            raise exeptions.JWT_DECODE_ERROR
        if not payload.get("sub") or not payload.get("token_type"):
            raise exeptions.JWT_BAD_CREDENSIALS
        return payload

    def verifi_jwt_access_token(self, token: str) -> User:
        payload = self.verifi_token(token)
        if payload.get("token_type") != "access":
            raise exeptions.JWT_BAD_CREDENSIALS
        user = User(
            id=payload.get("user_id"),
            username=payload.get("sub"),
            role_id=payload.get("role_id"),
            role=Role(id=payload.get("role_id"), name=payload.get("role")),
            department_id=payload.get("dep_id"),
            department=Department(id=payload.get("dep_id"), name=payload.get("dep")),
        )
        return user

    async def create_jwt_access_token(self, user: User) -> str:
        payload = {
            "sub": user.username,
            "user_id": user.id,
            "role_id": user.role_id,
            "role": user.role.name,
            "dep_id": user.department_id,
            "dep": user.department.name,
            "token_type": "access",
        }
        token = self.create_token(payload)
        return token

    async def create_jwt_refresh_token(self, user: User) -> RefreshTokenCreate:
        now = datetime.now(timezone.utc)
        refresh_token_expire = now + timedelta(days=self.config.refresh_expire_days)
        refresh_token_uuid = uuid.uuid4()

        payload = {
            "sub": user.username,
            "user_id": user.id,
            "token": str(refresh_token_uuid),
            "token_type": "refresh",
        }
        token = self.create_token(payload, expire_at=refresh_token_expire)

        return RefreshTokenCreate(
            user_id=user.id,
            token_uuid=refresh_token_uuid,
            token=token,
            expires_at=refresh_token_expire,
        )

    async def create_and_save_jwt_refresh_token(self, user: User) -> str:
        token_data = await self.create_jwt_refresh_token(user)
        await self.jwt_repo.save_refresh_token(token_data)
        return token_data.token

    async def verifi_jwt_refresh_token(self, refresh_token: str):
        payload = self.verifi_token(refresh_token)
        if payload.get("token_type") != "refresh":
            raise exeptions.JWT_BAD_CREDENSIALS

        user_id = payload.get("user_id")
        token = payload.get("token")

        if not user_id or not token:
            raise exeptions.JWT_BAD_CREDENSIALS

        refresh_token_orm = await self.jwt_repo.get_refresh_token(
            token=token,
            user_id=user_id,
        )
        if not refresh_token_orm:
            raise exeptions.REFRESH_TOKEN_NOT_FOUND

        if refresh_token_orm.expires_at < datetime.now(timezone.utc):
            raise exeptions.JWT_TOKEN_EXPIRED
        return refresh_token_orm

    async def refresh_jwt_tokens(
        self, old_refresh_token: str
    ) -> SuccessRefreshResponse:
        old_refresh_token_orm = await self.verifi_jwt_refresh_token(old_refresh_token)
        log.info(old_refresh_token_orm.user.__dict__)
        user = User.orm_validate(old_refresh_token_orm.user)
        access_token = await self.create_jwt_access_token(user)
        refresh_token = await self._rotate_jwt_refresh_token(old_refresh_token_orm)
        return SuccessRefreshResponse(
            access_token=access_token, refresh_token=refresh_token
        )

    async def _rotate_jwt_refresh_token(
        self, old_refresh_token: RefreshTokenORM
    ) -> str:
        new_refresh_data = await self.create_jwt_refresh_token(old_refresh_token.user)
        await self.jwt_repo.rotate_refresh_token(
            old_refresh_token.token, new_refresh_data
        )
        return new_refresh_data.token

    async def delete_jwt_refresh_token(
        self, refresh_token: str, delete_all_tokens: bool = False
    ):
        refresh_token_orm = await self.verifi_jwt_refresh_token(refresh_token)
        if delete_all_tokens:
            await self.jwt_repo.delete_all_refresh_tokens(refresh_token_orm.user_id)
        else:
            await self.jwt_repo.delete_refresh_token(refresh_token_orm.token)
