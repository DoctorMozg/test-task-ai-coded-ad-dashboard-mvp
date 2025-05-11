from dashboard.data.models.campaign import AdBannerSchema
from dashboard.data.store.memory_store import InMemoryStore


class BannerStore(InMemoryStore[AdBannerSchema]):
    def __init__(self) -> None:
        super().__init__(id_field="id", max_items=10000)
        self.add_index("created_by")

    def get_by_user(self, user_id: str) -> list[AdBannerSchema]:
        return self.get_by_index("created_by", user_id)

    def count_by_user(self, user_id: str) -> int:
        return len(self.get_by_user(user_id))
