import typing
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

if typing.TYPE_CHECKING:
    from app.lib.web.models import FastAPI


class PgAccessor:
    def __init__(self, app: FastAPI):
        self.app = app
        self.engine: AsyncEngine | None = None
        self.session_maker: async_sessionmaker[AsyncSession] | None = None

    async def connect(self):
        self.engine = create_async_engine(url=self.app.config.pg.url)
        self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def disconnect(self):
        if self.engine is not None:
            await self.engine.dispose()
            self.engine = None
        self.session = None
