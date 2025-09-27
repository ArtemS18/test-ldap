from pydantic import Field
from app.base.pydantic_base import Base
from app.ord.entities.orders import Order


class OrderResponse(Order):
    pass


class OrderCreate(Base):
    name: str
    price: float = Field(default=0, ge=0)


class OrderListResponse(Base):
    orders: list[OrderResponse]
