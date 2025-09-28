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
                search_filter="(objectClass=inetOrgPerson)",
                search_scope=SUBTREE,
                attributes=["cn", "sn", "uid", "gidNumber"],
            )
            users = []
            for entry in conn.entries:
                users.append(entry.entry_attributes_as_dict)

            return {"users": users}

    async def autho_user(self, user_dn: str, password: str):
        try:
            async with self.user_connection(user_dn, password) as conn:
                if conn.result["result"] == 0:
                    return True
        except Exception:
            return False

    async def get_user_dn(self, username: str):
        firstname, lastname = username.split(".")
        async with self.admin_connection() as conn:
            conn.search(
                search_base={self.config.base_dn},
                search_filter=f"(cn={firstname} {lastname})",
                search_scope=SUBTREE,
                attributes=["cn"],
            )
            if not conn.entries:
                return None
            return conn.entries[0].entry_dn
