import uuid
import pytest
from app.lib.web.models import FastAPI
from httpx import AsyncClient
from tests.conftest import make_refresh_token
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_auth_200(client: AsyncClient, mock_app: FastAPI):
    resp = await client.post(
        url="/auth/", data={"username": "user.test1", "password": "12345"}
    )
    assert resp.status_code == 200
    assert resp.json().get("access_token")
    assert resp.json().get("refresh_token")


@pytest.mark.asyncio
async def test_auth_401_bad_credentials(client: AsyncClient, mock_app: FastAPI):
    from app.lib.web import exeptions

    mock_app.store.autho_repo.autho_user.return_value = False
    resp = await client.post(
        url="/auth/", data={"username": "user.test1", "password": "12345"}
    )
    assert resp.status_code == 401
    assert resp.json().get("detail") == exeptions.BAD_CREDENSIALS.detail


@pytest.mark.asyncio
async def test_auth_401_user_not_found(client: AsyncClient, mock_app: FastAPI):
    from app.lib.web import exeptions

    mock_app.store.user_repo.get_user_by_username.return_value = None
    resp = await client.post(
        url="/auth/", data={"username": "user.test1", "password": "12345"}
    )
    assert resp.status_code == 401
    assert resp.json().get("detail") == exeptions.USER_NOT_FOUND.detail


@pytest.mark.asyncio
async def test_refresh_200(client: AsyncClient, mock_app: FastAPI, monkeypatch):
    refresh_token = make_refresh_token(10)
    monkeypatch.setattr(uuid, "uuid4", lambda: refresh_token.token)
    mock_app.store.jwt_repo.get_refresh_token = AsyncMock(return_value=refresh_token)
    resp = await client.post(
        url="/auth/", data={"username": "user.test1", "password": "12345"}
    )
    token = resp.json().get("refresh_token")

    resp_refresh = await client.post(url="/auth/refresh", json={"refresh_token": token})
    assert resp_refresh.status_code == 200
    assert resp_refresh.json().get("access_token")
    assert resp_refresh.json().get("refresh_token")


@pytest.mark.asyncio
async def test_refresh_401_token_not_found(client: AsyncClient, mock_app: FastAPI):
    from app.lib.web import exeptions

    resp_auth = await client.post(
        url="/auth/", data={"username": "user.test1", "password": "12345"}
    )
    refresh_token = resp_auth.json().get("refresh_token")
    mock_app.store.jwt_repo.get_refresh_token = AsyncMock(return_value=None)
    resp_refresh = await client.post(
        url="/auth/refresh", json={"refresh_token": refresh_token}
    )
    data: dict = resp_refresh.json()
    assert resp_refresh.status_code == 401
    assert data.get("detail") == exeptions.REFRESH_TOKEN_NOT_FOUND.detail


@pytest.mark.asyncio
async def test_refresh_401_expire_in_db(client: AsyncClient, mock_app: FastAPI):
    from app.lib.web import exeptions
    from app.auth.models.refresh_tokens import RefreshTokenORM

    resp_auth = await client.post(
        url="/auth/", data={"username": "user.test1", "password": "12345"}
    )
    refresh_token = resp_auth.json().get("refresh_token")
    test_token: RefreshTokenORM = make_refresh_token(-10)
    mock_app.store.jwt_repo.get_refresh_token = AsyncMock(return_value=test_token)
    resp_refresh = await client.post(
        url="/auth/refresh", json={"refresh_token": refresh_token}
    )
    data: dict = resp_refresh.json()
    assert resp_refresh.status_code == 401
    assert data.get("detail") == exeptions.JWT_TOKEN_EXPIRED.detail


@pytest.mark.asyncio
async def test_refresh_401_decode_error(client: AsyncClient, mock_app: FastAPI):
    from app.lib.web import exeptions

    refresh_token = "bad_token"
    resp_refresh = await client.post(
        url="/auth/refresh", json={"refresh_token": refresh_token}
    )
    data: dict = resp_refresh.json()
    assert resp_refresh.status_code == 401
    assert data.get("detail") == exeptions.JWT_BASE_EXEPTION.detail


@pytest.mark.asyncio
async def test_refresh_401_wrong_type(
    client: AsyncClient, mock_app: FastAPI, monkeypatch
):
    from app.lib.web import exeptions
    from app.auth.services.jwt_tokens import JWTService

    monkeypatch.setattr(
        JWTService,
        "verifi_token",
        lambda *x: {
            "sub": "any",
            "user_id": 1,
            "token": "any",
            "token_type": "access",
        },
    )

    refresh_token = "any_token"
    resp_refresh = await client.post(
        url="/auth/refresh", json={"refresh_token": refresh_token}
    )
    data: dict = resp_refresh.json()
    assert resp_refresh.status_code == 401
    assert data.get("detail") == exeptions.JWT_BAD_CREDENSIALS.detail


@pytest.mark.asyncio
async def test_logout_delete_current_204(client: AsyncClient, mock_app: FastAPI):
    resp_auth = await client.post(
        url="/auth/", data={"username": "user.test1", "password": "12345"}
    )
    refresh_token = resp_auth.json().get("refresh_token")
    resp_refresh = await client.post(
        url="/auth/logout", json={"refresh_token": refresh_token, "all": False}
    )
    assert resp_refresh.status_code == 204


@pytest.mark.asyncio
async def test_logout_delete_all_204(client: AsyncClient, mock_app: FastAPI):
    resp_auth = await client.post(
        url="/auth/", data={"username": "user.test1", "password": "12345"}
    )
    refresh_token = resp_auth.json().get("refresh_token")
    resp_refresh = await client.post(
        url="/auth/logout", json={"refresh_token": refresh_token, "all": True}
    )
    assert resp_refresh.status_code == 204


@pytest.mark.asyncio
async def test_logout_401_decode_error(client: AsyncClient, mock_app: FastAPI):
    from app.lib.web import exeptions

    refresh_token = "bad_token"
    resp_refresh = await client.post(
        url="/auth/logout", json={"refresh_token": refresh_token}
    )
    data: dict = resp_refresh.json()
    assert resp_refresh.status_code == 401
    assert data.get("detail") == exeptions.JWT_BASE_EXEPTION.detail


@pytest.mark.asyncio
async def test_logout_401_token_not_found(client: AsyncClient, mock_app: FastAPI):
    from app.lib.web import exeptions

    resp_auth = await client.post(
        url="/auth/", data={"username": "user.test1", "password": "12345"}
    )
    refresh_token = resp_auth.json().get("refresh_token")
    mock_app.store.jwt_repo.get_refresh_token.return_value = None
    resp_refresh = await client.post(
        url="/auth/logout", json={"refresh_token": refresh_token}
    )
    data: dict = resp_refresh.json()
    assert resp_refresh.status_code == 401
    assert data.get("detail") == exeptions.REFRESH_TOKEN_NOT_FOUND.detail


@pytest.mark.asyncio
async def test_logout_401_expire(client: AsyncClient, mock_app: FastAPI):
    from app.lib.web import exeptions
    from app.auth.models.refresh_tokens import RefreshTokenORM

    resp_auth = await client.post(
        url="/auth/", data={"username": "user.test1", "password": "12345"}
    )
    refresh_token = resp_auth.json().get("refresh_token")
    test_token: RefreshTokenORM = make_refresh_token(-10)
    mock_app.store.jwt_repo.get_refresh_token.return_value = test_token
    resp_refresh = await client.post(
        url="/auth/logout", json={"refresh_token": refresh_token}
    )
    data: dict = resp_refresh.json()
    assert resp_refresh.status_code == 401
    assert data.get("detail") == exeptions.JWT_TOKEN_EXPIRED.detail
