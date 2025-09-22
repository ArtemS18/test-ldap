from app.base.orm_base import BaseORM
from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column


class Department(BaseORM):
    __tablename__ = "departments"
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True)
