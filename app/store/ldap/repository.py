from ldap3 import SUBTREE
from .accessor import LdapAccessor


class UserAuthoRepository(LdapAccessor):
    @property
    def users_ou(self):
        users_ou = "users"
        return f"ou={users_ou},{self.config.base_dn}"

    async def find_all_users(self):
        async with self.admin_connection() as conn:
            conn.search(
                search_base=self.config.base_dn,
                search_filter="(objectClass=organizationalPerson)",
                search_scope=SUBTREE,
                attributes=["cn", "sn", "uid", "gidNumber"],
            )
            users = []
            for entry in conn.entries:
                users.append(entry.entry_attributes_as_dict)

            return {"users": users}

    async def autho_user(self, login: str, password: str):
        try:
            async with self.user_connection(login, password) as conn:
                return True
        except Exception:
            return False
