import uuid
from datetime import datetime

from app.base.pydantic_base import Base


class RefreshToken(Base):
    id: int
    user_id: int
    token: uuid.UUID = uuid.uuid4()
    expires_at: datetime
