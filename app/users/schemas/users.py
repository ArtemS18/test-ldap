from app.base.pydantic_base import Base


class User(Base):
    id: int
    username: str
    department_id: int
    role_id: int
