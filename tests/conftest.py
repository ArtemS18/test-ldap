from httpx import ASGITransport, AsyncClient
import pytest_asyncio

from app.lib.web.models import FastAPI
from app.web.app import setup_app
from tests.utils import (
    make_mock_auth_repo,
    make_mock_jwt_repo,
    make_mock_user_repo,
    make_refresh_token,
)


@pytest_asyncio.fixture()
async def app():
    app = setup_app()
    await app.store.connect_all()
    yield app
    await app.store.disconnect_all()


@pytest_asyncio.fixture(scope="function")
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test.com"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def mock_app(app: FastAPI):
    test_refresh_token = make_refresh_token(10)

    app.store.jwt_repo = make_mock_jwt_repo(test_refresh_token)
    app.store.user_repo = make_mock_user_repo(test_refresh_token.user)
    app.store.autho_repo = make_mock_auth_repo()
    return app
