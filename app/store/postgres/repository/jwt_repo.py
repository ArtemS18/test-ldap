from uuid import UUID
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import selectinload
from app.auth.services.dto import RefreshTokenCreate
from app.store.postgres.accessor import PgAccessor
from app.auth.models.refresh_tokens import RefreshTokenORM
from app.users.models.users import UserORM


class JWTRepository(PgAccessor):
    async def save_refresh_token(self, refresh_token: RefreshTokenCreate) -> UUID:
        create_query = (
            insert(RefreshTokenORM)
            .values(
                user_id=refresh_token.user_id,
                token=refresh_token.token_uuid,
                expires_at=refresh_token.expires_at,
            )
            .returning(RefreshTokenORM.token)
        )
        res = await self._execute(create_query)
        return res.scalar_one_or_none()

    async def get_refresh_token(
        self, token: UUID, user_id: int
    ) -> RefreshTokenORM | None:
        query = (
            select(RefreshTokenORM)
            .where(
                (RefreshTokenORM.token == token) & (RefreshTokenORM.user_id == user_id)
            )
            .options(
                selectinload(RefreshTokenORM.user).selectinload(UserORM.role),
                selectinload(RefreshTokenORM.user).selectinload(UserORM.department),
            )
        )
        res = await self._execute(query, commit=False)
        token_orm = res.scalar_one_or_none()
        return token_orm

    async def delete_refresh_token(self, token: UUID):
        query = (
            delete(RefreshTokenORM)
            .where(RefreshTokenORM.token == token)
            .returning(RefreshTokenORM.token)
        )
        res = await self._execute(query)
        token_orm = res.scalar_one_or_none()
        return token_orm

    async def delete_all_refresh_tokens(self, user_id: int):
        query = (
            delete(RefreshTokenORM)
            .where(RefreshTokenORM.user_id == user_id)
            .returning(RefreshTokenORM.token)
        )
        res = await self._execute(query)
        tokens = res.scalars().all()
        return tokens

    async def rotate_refresh_token(
        self, prev_token: UUID, new_token_data: RefreshTokenCreate
    ):
        query_delete = (
            delete(RefreshTokenORM)
            .where(RefreshTokenORM.token == prev_token)
            .returning(RefreshTokenORM.token)
        )
        query_create = (
            insert(RefreshTokenORM)
            .values(
                user_id=new_token_data.user_id,
                token=new_token_data.token_uuid,
                expires_at=new_token_data.expires_at,
            )
            .returning(RefreshTokenORM.token)
        )
        async with self.get_tansaction() as trans:
            res = await trans.session.execute(query_delete)
            if res.scalar_one_or_none() is not None:
                res = await trans.session.execute(query_create)
                new_token_uuid = res.scalar_one()
                return new_token_uuid
            else:
                trans.rollback()
