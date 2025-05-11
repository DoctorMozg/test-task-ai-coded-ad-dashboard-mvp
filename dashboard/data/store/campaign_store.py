from dashboard.data.models.campaign import CampaignSchema, CampaignStatusEnum
from dashboard.data.store.memory_store import InMemoryStore


class CampaignStore(InMemoryStore[CampaignSchema]):
    def __init__(self) -> None:
        super().__init__(id_field="id", max_items=5000)
        self.add_index("created_by")
        self.add_index("status")

    def get_by_user(self, user_id: str) -> list[CampaignSchema]:
        return self.get_by_index("created_by", user_id)

    def get_by_status(self, status: CampaignStatusEnum) -> list[CampaignSchema]:
        return self.get_by_index("status", status)

    def count_by_user(self, user_id: str) -> int:
        return len(self.get_by_user(user_id))

    def count_by_status(self, status: CampaignStatusEnum) -> int:
        return len(self.get_by_status(status))
