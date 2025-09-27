import datetime
from typing import cast
from unittest.mock import AsyncMock, create_autospec
import pytest
from httpx import ASGITransport, AsyncClient
import pytest_asyncio

from app.lib.web.models import FastAPI
from app.web.app import setup_app


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
async def mock_app(app: FastAPI, monkeypatch):
    from app.store.ldap.repository import UserAuthoRepository
    from app.store.postgres.repository.jwt_repo import JWTRepository
    from app.store.postgres.repository.user_repo import UserRepository
    from app.auth.models.refresh_tokens import RefreshTokenORM
    from app.users.models.departments import DepartmentORM
    from app.users.models.role import RoleORM
    from app.users.models.users import UserORM
    import uuid

    test_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")
    monkeypatch.setattr(uuid, "uuid4", lambda: test_uuid)

    test_user = UserORM(
        id=1,
        username="user test1",
        department_id=1,
        role_id=1,
        role=RoleORM(id=1, name="User"),
        department=DepartmentORM(id=1, name="User"),
    )
    test_refresh_token = RefreshTokenORM(
        id=1,
        token=test_uuid,
        user_id=test_user.id,
        expires_at=datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=1),
        user=test_user,
    )

    mock_jwt_repo = cast(JWTRepository, create_autospec(JWTRepository, instance=True))
    mock_jwt_repo.save_refresh_token = AsyncMock(
        spec=JWTRepository.save_refresh_token, return_value=None
    )
    mock_jwt_repo.rotate_refresh_token = AsyncMock(
        return_value=test_refresh_token.token
    )
    mock_jwt_repo.get_refresh_token = AsyncMock(return_value=test_refresh_token)
    mock_jwt_repo.delete_refresh_token = AsyncMock(
        return_value=test_refresh_token.token
    )
    mock_jwt_repo.delete_all_refresh_tokens = AsyncMock(
        return_value=test_refresh_token.token
    )

    mock_user_repo = cast(
        UserRepository, create_autospec(UserRepository, instance=True)
    )
    mock_user_repo.get_user_by_username = AsyncMock(
        spec=UserRepository.get_user_by_username, return_value=test_user
    )

    mock_autho_repo = cast(
        UserAuthoRepository, create_autospec(UserAuthoRepository, instance=True)
    )
    mock_autho_repo.get_user_dn = AsyncMock(
        return_value="cn=user test1,ou=users,dc=mycompany,dc=local"
    )
    mock_autho_repo.autho_user = AsyncMock(return_value=True)

    app.store.user_repo = mock_user_repo
    app.store.autho_repo = mock_autho_repo
    app.store.jwt_repo = mock_jwt_repo
    return app
