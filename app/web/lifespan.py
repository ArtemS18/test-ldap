from contextlib import asynccontextmanager
from app.base.orm_base import BaseORM
import logging
import typing

if typing.TYPE_CHECKING:
    from app.lib import FastAPI

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifispan_app(app: "FastAPI"):
    await app.store.connect_all()
    await app.store.user_repo.init_models()
    yield
    await app.store.disconnect_all()
