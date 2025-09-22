from uuid import UUID
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from app.auth.schemas.refresh_tokens import RefreshToken, RefreshTokenCreate
from app.store.postgres.accessor import PgAccessor
from app.store.postgres.models.refresh_tokens import RefreshTokenORM


class JWTRepository(PgAccessor):
    async def save_refresh_token(self, refresh_token: RefreshTokenCreate) -> int:
        query = (
            insert(RefreshTokenORM)
            .values(
                user_id=refresh_token.user_id,
                token=refresh_token.token,
                expires_at=refresh_token.expires_at,
            )
            .returning(RefreshTokenORM.id)
        )
        res = await self._execute(query)
        return res.scalar_one()

    async def get_refresh_token(
        self, token: UUID, user_id: int
    ) -> RefreshTokenORM | None:
        query = (
            select(RefreshTokenORM)
            .where(
                (RefreshTokenORM.token == token) & (RefreshTokenORM.user_id == user_id)
            )
            .options(selectinload(RefreshTokenORM.user))
        )
        res = await self._execute(query)
        token_orm = res.scalar_one_or_none()
        return token_orm
