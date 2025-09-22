import typing
from sqlalchemy import Select, Tuple
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.base.orm_base import BaseORM
from .models import *

if typing.TYPE_CHECKING:
    from app.lib.web.models import FastAPI

V = typing.TypeVar("V")


class PgAccessor:
    def __init__(self, app: "FastAPI"):
        self.app = app
        self.engine: AsyncEngine | None = None
        self.session_maker: async_sessionmaker[AsyncSession] | None = None

    async def connect(self):
        print(self.app.config.pg.url)
        self.engine = create_async_engine(url=self.app.config.pg.url)
        self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def disconnect(self):
        if self.engine is not None:
            await self.engine.dispose()
            self.engine = None
        self.session = None

    async def init_models(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseORM.metadata.create_all)

    async def _execute(self, query: Select[Tuple], commit: bool = True):
        async with self.session_maker() as session:
            result = await session.execute(query)
            if commit:
                await session.commit()
            return result
