from typing import Literal
from app.base.pydantic_base import Base


class Role(Base):
    id: int
    name: Literal["User", "Admin", "Moderator"]
    description: str | None = None
