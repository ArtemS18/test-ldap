from app.base.pydantic_base import Base


class UserCredentials(Base):
    username: str
    password: str

class SuccessAuthoResponse(Base):
    access_token: str 
    refresh_token: str 
    token_type: str = "bearer"
    role: str = "User"