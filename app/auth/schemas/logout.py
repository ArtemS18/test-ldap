from app.base.pydantic_base import Base


class LogoutRequest(Base):
    refresh_token: str
    all: bool = False
