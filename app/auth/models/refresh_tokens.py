from datetime import datetime
import typing
from app.base.orm_base import BaseORM
import uuid
from sqlalchemy import ForeignKey, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
    from app.users.models.users import UserORM


class RefreshTokenORM(BaseORM):
    __tablename__ = "refresh_tokens"
    token: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    user: Mapped["UserORM"] = relationship(
        "UserORM", back_populates="refresh_tokens", lazy="noload"
    )
