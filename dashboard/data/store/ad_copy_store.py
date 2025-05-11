from dashboard.data.models.ad_copy import AdCopySchema
from dashboard.data.store.memory_store import InMemoryStore


class AdCopyStore(InMemoryStore[AdCopySchema]):
    def __init__(self) -> None:
        super().__init__(id_field="id", max_items=10000)
        self.add_index("campaign_id")

    def get_by_campaign(self, campaign_id: str) -> list[AdCopySchema]:
        return self.get_by_index("campaign_id", campaign_id)

    def count_by_campaign(self, campaign_id: str) -> int:
        return len(self.get_by_campaign(campaign_id))
