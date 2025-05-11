from dashboard.data.models.user import UserSchema
from dashboard.data.store.memory_store import InMemoryStore


class UserStore(InMemoryStore[UserSchema]):
    def __init__(self) -> None:
        super().__init__(id_field="id", max_items=1000)
        self.add_index("username")
        self.add_index("email")

    def get_by_username(self, username: str) -> UserSchema | None:
        users = self.get_by_index("username", username)
        return users[0] if users else None

    def get_by_email(self, email: str) -> UserSchema | None:
        users = self.get_by_index("email", email)
        return users[0] if users else None

    def username_exists(self, username: str) -> bool:
        return bool(self.get_by_username(username))

    def email_exists(self, email: str) -> bool:
        return bool(self.get_by_email(email))
