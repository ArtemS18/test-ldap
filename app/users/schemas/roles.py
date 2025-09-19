from app.base.pydantic_base import Base


class Role(Base):
    id: int 
    name: str
    description : str 