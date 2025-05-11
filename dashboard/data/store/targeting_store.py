from dashboard.data.models.targeting import AudienceTargetingSchema, InterestSchema
from dashboard.data.store.memory_store import InMemoryStore


class TargetingStore(InMemoryStore[AudienceTargetingSchema]):
    def __init__(self) -> None:
        super().__init__(id_field="id", max_items=5000)


class InterestStore(InMemoryStore[InterestSchema]):
    def __init__(self) -> None:
        super().__init__(id_field="id", max_items=1000)
        self.add_index("category")

    def get_by_category(self, category: str) -> list[InterestSchema]:
        return self.get_by_index("category", category)
