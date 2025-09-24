from app.base.orm_base import BaseORM
from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column


class RoleORM(BaseORM):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
