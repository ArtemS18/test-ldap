from app.base.pydantic_base import Base


class Department(Base):
    id: int
    name: str
