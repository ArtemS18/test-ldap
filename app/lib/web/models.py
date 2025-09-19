import typing
from fastapi import FastAPI as FastApiLib, Request as RequestLib

if typing.TYPE_CHECKING:
    from app.web.config import BaseConfig
    from app.store import Store


class FastAPI(FastApiLib):
    config: "BaseConfig"
    store: "Store"


class Request(RequestLib):
    @property
    def app(*args, **kwargs) -> FastAPI:
        return super().app
