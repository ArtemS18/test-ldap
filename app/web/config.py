import typing
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


if typing.TYPE_CHECKING:
    from app.lib import FastAPI

ENV_PATH = "env/.local.env"


class LDAPConfig(BaseModel):
    host: str = "localhost"
    port: int = 389
    login: str
    password: str
    base_dn: str


class PostgresDBConfig(BaseModel):
    host: str = "localhost"
    port: int = 5434
    login: str
    password: str
    base_db: str
    driver: str = "postgresql+asyncpg"

    @property
    def url(self):
        return f"{self.driver}://{self.login}:{self.password}@{self.host}:{self.port}/{self.base_db}"


class JWTConfig(BaseModel):
    access_expire: int = 1
    refresh_expire_days: int = 7
    secret_key: str
    algorithm: str


class WebConfig(BaseModel):
    host: str = "localhost"
    port: int = 8082
    jwt: JWTConfig


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=ENV_PATH,
        extra="ignore",
        env_nested_delimiter="__",
        env_prefix="APP__",
    )
    ldap: LDAPConfig
    web: WebConfig
    pg: PostgresDBConfig


def setup_config(app: "FastAPI"):
    app.config = BaseConfig(_env_file=ENV_PATH)
