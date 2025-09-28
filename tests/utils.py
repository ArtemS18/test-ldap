import datetime
from typing import cast
from unittest.mock import AsyncMock, create_autospec
import uuid
from app.auth.models.refresh_tokens import RefreshTokenORM
from app.store.ldap.repository import UserAuthoRepository
from app.store.postgres.repository.jwt_repo import JWTRepository
from app.store.postgres.repository.user_repo import UserRepository
from app.users import models as users
from app.users.models.users import UserORM


def make_refresh_token(
    expire: int, token_uuid: uuid.UUID | None = None
) -> RefreshTokenORM:
    test_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678") or token_uuid

    test_user = users.UserORM(
        id=1,
        username="user test1",
        department_id=1,
        role_id=1,
        role=users.RoleORM(id=1, name="User"),
        department=users.DepartmentORM(id=1, name="User"),
    )
    test_refresh_token = RefreshTokenORM(
        id=1,
        token=test_uuid,
        user_id=test_user.id,
        expires_at=datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=expire),
        user=test_user,
    )
    return test_refresh_token


def make_mock_jwt_repo(test_refresh_token: RefreshTokenORM):
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
    return mock_jwt_repo


def make_mock_user_repo(user: UserORM):
    mock_user_repo = cast(
        UserRepository, create_autospec(UserRepository, instance=True)
    )
    mock_user_repo.get_user_by_username = AsyncMock(
        spec=UserRepository.get_user_by_username, return_value=user
    )
    return mock_user_repo


def make_mock_auth_repo():
    mock_autho_repo = cast(
        UserAuthoRepository, create_autospec(UserAuthoRepository, instance=True)
    )
    mock_autho_repo.get_user_dn = AsyncMock(
        return_value="cn=user test1,ou=users,dc=mycompany,dc=local"
    )
    mock_autho_repo.autho_user = AsyncMock(return_value=True)
    return mock_autho_repo
