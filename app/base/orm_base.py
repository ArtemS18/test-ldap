from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import Integer


class BaseORM(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    pass
