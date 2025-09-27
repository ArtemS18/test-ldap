from httpx import AsyncClient
import pytest

from app.lib.web.models import FastAPI


@pytest.mark.asyncio
async def test_user_200(client: AsyncClient, mock_app: FastAPI):
    resp = await client.post(
        url="/auth/", data={"username": "user.test1", "password": "12345"}
    )
    data: dict = resp.json()
    token = data.get("access_token")
    assert resp.status_code == 200
    assert token
    resp = await client.get(
        url="/user/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_user_401_decode_error(client: AsyncClient, mock_app: FastAPI):
    from app.lib.web import exeptions

    token = "bad_access_token"
    resp = await client.get(
        url="/user/me", headers={"Authorization": f"Bearer {token}"}
    )
    data: dict = resp.json()
    assert resp.status_code == 401
    assert data.get("detail") == exeptions.JWT_BASE_EXEPTION.detail
