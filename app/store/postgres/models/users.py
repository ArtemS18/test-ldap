import typing
from sqlalchemy import ForeignKey, Integer, VARCHAR
from app.base.orm_base import BaseORM
from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
    from app.store.postgres.models import RoleORM, RefreshTokenORM, Department
from app.store.postgres.models.role import RoleORM
from app.users.schemas.departments import Department


class UserORM(BaseORM):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True)
    department_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("departments.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roles.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    role: Mapped["RoleORM"] = relationship("RoleORM", lazy="noload")
    refresh_tokens: Mapped[list["RefreshTokenORM"]] = relationship(
        "RefreshTokenORM",
        back_populates="user",
        lazy="noload",
    )
    department: Mapped["Department"] = relationship("Department", lazy="noload")
