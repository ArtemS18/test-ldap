from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
import jwt
from app.lib.web import exeptions


class JWTService:
    def __init__(self, config):
        self.config = config

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
                    else now + timedelta(minutes=self.config.jwt.access_expire)
                }
            )
        else:
            encoder.update({"exp": expire_at})

        token = jwt.encode(
            encoder, self.config.jwt.secret_key, self.config.jwt.algorithm
        )
        return token

    def verifi_token(self, token: str):
        try:
            payload: dict = jwt.decode(
                token, self.config.jwt.secret_key, self.config.jwt.algorithm
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
