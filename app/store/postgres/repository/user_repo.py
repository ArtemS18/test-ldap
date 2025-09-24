from app.store.postgres.accessor import PgAccessor
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ..models import UserORM


class UserRepository(PgAccessor):
    async def get_user_by_username(self, username: str) -> UserORM:
        query = (
            select(UserORM)
            .where(UserORM.username == username)
            .options(selectinload(UserORM.role), selectinload(UserORM.department))
        )
        result = await self._execute(query)
        return result.scalar_one_or_none()
