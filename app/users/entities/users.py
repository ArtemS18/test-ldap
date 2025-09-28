from app.base.pydantic_base import Base
from app.users.models.users import UserORM
from .departments import Department
from .roles import Role


class User(Base):
    id: int
    username: str
    department_id: int
    role_id: int

    role: Role | None = None
    department: Department | None = None

    @classmethod
    def orm_validate(cls: "User", value: UserORM):
        return cls(
            id=value.id,
            username=value.username,
            department_id=value.department_id,
            role_id=value.role_id,
            role=Role.model_validate(value.role),
            department=Department.model_validate(value.department)
            if value.department
            else None,
        )
