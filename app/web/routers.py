import typing
from app.auth.routers import router as auth_router
from app.users.routers import router as user_router
from app.ord.routers import router as ord_router

if typing.TYPE_CHECKING:
    from app.lib.web.models import FastAPI


def setup_routers(app: "FastAPI"):
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(ord_router)
