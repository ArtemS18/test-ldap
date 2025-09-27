from pydantic import Field
from app.base.pydantic_base import Base


class Order(Base):
    id: int
    name: str
    price: float = Field(default=0, ge=0)
