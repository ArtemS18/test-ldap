from sqlalchemy import VARCHAR, CheckConstraint, Float
from app.base.orm_base import BaseORM
from sqlalchemy.orm import Mapped, mapped_column


class OrderORM(BaseORM):
    __tablename__ = "orders"
    name: Mapped[str] = mapped_column(VARCHAR(25), index=True, unique=True)
    price: Mapped[float] = mapped_column(Float, CheckConstraint("price>=0"), default=0)
