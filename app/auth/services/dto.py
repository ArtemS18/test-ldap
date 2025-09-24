import uuid
from datetime import datetime

from app.base.pydantic_base import Base


class RefreshTokenCreate(Base):
    user_id: int
    token_uuid: uuid.UUID = uuid.uuid4()
    token: str
    expires_at: datetime
