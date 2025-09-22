from datetime import datetime, timedelta, timezone
import uuid
import jwt
from app.auth.schemas.refresh_tokens import RefreshTokenCreate
from app.store.postgres.repository.jwt_repo import JWTRepository
from app.users.schemas.users import User
from app.web.config import JWTConfig
from app.lib.web import exeptions


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

    async def create_jwt_access_token(self, user: User) -> str:
        payload = {
            "sub": user.username,
            "user_id": user.id,
            "role": user.role_id,
            "dep": user.department_id,
            "token_type": "access",
        }
        token = self.create_token(payload)
        return token

    async def create_jwt_refresh_token(self, user: User) -> str:
        now = datetime.now(timezone.utc)
        refresh_token_expire = now + timedelta(days=self.config.refresh_expire_days)
        refresh_token_uuid = uuid.uuid4()

        payload = {
            "sub": user.username,
            "id": user.id,
            "token": str(refresh_token_uuid),
            "token_type": "access",
        }
        token = self.create_token(payload, expire_at=refresh_token_expire)
        await self.jwt_repo.save_refresh_token(
            RefreshTokenCreate(
                user_id=user.id,
                token=refresh_token_uuid,
                expires_at=refresh_token_expire,
            )
        )
        return token

    async def refresh_jwt_access_token(self, refresh_token: str) -> str:
        payload = self.verifi_token(refresh_token)
        if payload.get("token_type") != "refresh":
            raise exeptions.JWT_BAD_CREDENSIALS

        user_id = payload.get("user_id")
        token = payload.get("sub")

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

        user = User.model_validate(refresh_token_orm.user)

        token = await self.create_jwt_access_token(user)
        return token
