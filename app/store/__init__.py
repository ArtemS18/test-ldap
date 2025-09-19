import typing


if typing.TYPE_CHECKING:
    from app.lib.web.models import FastAPI


class Store:
    def __init__(self, app: "FastAPI"):
        from .ldap.accessor import LdapAccessor
        from .ldap.repository import UserAuthoRepository

        self.app = app

        self.ldap_accessor = LdapAccessor(app)
        self.autho_repo = UserAuthoRepository(app)


def setup_store(app: "FastAPI"):
    app.store = Store(app)
