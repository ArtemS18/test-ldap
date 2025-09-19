import logging
from app.lib import FastAPI

from app.store import setup_store
from app.web.lifespan import lifispan_app
from app.web.config import setup_config
from app.web.loger import setup_logger
from app.web.routers import setup_routers

app = FastAPI(lifespan=lifispan_app)
log = logging.getLogger(__name__)


def setup_app():
    setup_logger()
    setup_config(app)
    setup_store(app)
    setup_routers(app)
    return app
