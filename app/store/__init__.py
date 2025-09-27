import typing


if typing.TYPE_CHECKING:
    from app.lib.web.models import FastAPI


class Store:
    def __init__(self, app: "FastAPI"):
        from .ldap.accessor import LdapAccessor
        from .ldap.repository import UserAuthoRepository
        from .postgres.repository.user_repo import UserRepository
        from .postgres.repository.jwt_repo import JWTRepository
        from .postgres.repository.ord_repo import OrderRepository

        self.app = app

        self.ldap_accessor = LdapAccessor(app)
        self.autho_repo = UserAuthoRepository(app)
        self.user_repo = UserRepository(app)
        self.jwt_repo = JWTRepository(app)
        self.order_repo = OrderRepository(app)

    async def connect_all(self):
        await self.ldap_accessor.connect()
        await self.autho_repo.connect()
        await self.user_repo.connect()
        await self.jwt_repo.connect()
        await self.order_repo.connect()

    async def disconnect_all(self):
        await self.ldap_accessor.disconnect()
        await self.autho_repo.disconnect()
        await self.user_repo.disconnect()
        await self.jwt_repo.disconnect()
        await self.order_repo.disconnect()


def setup_store(app: "FastAPI"):
    app.store = Store(app)
