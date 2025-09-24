from app.base.pydantic_base import Base


class RefreshTokenRequest(Base):
    refresh_token: str


class SuccessRefreshResponse(Base):
    access_token: str
    refresh_token: str
