from datetime import timedelta
from app.base.pydantic_base import Base

class RefreshToken(Base):
    id: int 
    user_id: int 
    token: int 
    expires_at: timedelta