from typing import AsyncGenerator
from ldap3 import Server, ALL, Connection
import asyncio
from contextlib import asynccontextmanager
from app.lib.web.models import FastAPI


class LdapAccessor:
    def __init__(self, app: "FastAPI"):
        self.app = app
        self.config = self.app.config.ldap
        self.server: Server | None = None
        self._connection_pool = asyncio.Semaphore(20)

    async def connect(self):
        self.server = Server(self.config.host, port=self.config.port, get_info=ALL)

    async def disconnect(self):
        self.server = None

    def _create_connection(self, login: str = None, password: str = None) -> Connection:
        login = login or self.config.login
        password = password or self.config.password
        return Connection(self.server, login, password, auto_bind=True)

    @asynccontextmanager
    async def admin_connection(self) -> AsyncGenerator[Connection, None]:
        async with self._connection_pool:
            conn: Connection = await asyncio.to_thread(self._create_connection)
            try:
                yield conn
            finally:
                await asyncio.to_thread(conn.unbind)

    @asynccontextmanager
    async def user_connection(
        self, login: str, password: str
    ) -> AsyncGenerator[Connection, None]:
        async with self._connection_pool:
            conn: Connection = await asyncio.to_thread(
                self._create_connection, login, password
            )
            try:
                yield conn
            finally:
                await asyncio.to_thread(conn.unbind)
