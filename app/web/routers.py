import typing
from app.auth.routers import router as auth_router

if typing.TYPE_CHECKING:
    from app.lib.web.models import FastAPI


def setup_routers(app: "FastAPI"):
    app.include_router(auth_router)
