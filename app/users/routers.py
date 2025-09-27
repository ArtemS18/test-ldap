from fastapi import APIRouter
from fastapi import Depends

from app.auth.depends.autho import verifi_user
from app.users.entities.users import User
from app.users.schemas.users import UserResponse

router = APIRouter(prefix="/user", tags=["Пользователи"])


@router.get("/me", response_model=UserResponse)
async def get_current_user(user: User = Depends(verifi_user)):
    return UserResponse(
        id=user.id,
        username=user.username,
        role=user.role.name,
        department=user.department.name,
    )
