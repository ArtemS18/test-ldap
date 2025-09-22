from datetime import datetime
from app.base.pydantic_base import Base
from uuid import UUID, uuid4


class RefreshToken(Base):
    id: int
    user_id: int
    token: UUID = uuid4()
    expires_at: datetime


class RefreshTokenCreate(Base):
    user_id: int
    token: UUID = uuid4()
    expires_at: datetime
