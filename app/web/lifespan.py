from contextlib import asynccontextmanager
import logging
import typing

if typing.TYPE_CHECKING:
    from app.lib import FastAPI

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifispan_app(app: "FastAPI"):
    await app.store.ldap_accessor.connect()
    await app.store.autho_repo.connect()
    yield
    await app.store.autho_repo.disconnect()
    await app.store.autho_repo.disconnect()
