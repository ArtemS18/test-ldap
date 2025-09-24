from app.base.pydantic_base import Base


class UserResponse(Base):
    id: int
    username: str
    role: str
    department: str
