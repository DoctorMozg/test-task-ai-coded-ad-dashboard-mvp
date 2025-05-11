from datetime import date

from dashboard.data.models.analytics import CampaignAnalyticsSchema
from dashboard.data.store.memory_store import InMemoryStore


class AnalyticsStore(InMemoryStore[CampaignAnalyticsSchema]):
    def __init__(self) -> None:
        super().__init__(id_field="id", max_items=50000)
        self.add_index("campaign_id")
        self.add_index("date")

    def get_by_campaign(self, campaign_id: str) -> list[CampaignAnalyticsSchema]:
        return self.get_by_index("campaign_id", campaign_id)

    def get_by_date(self, target_date: date) -> list[CampaignAnalyticsSchema]:
        return self.get_by_index("date", target_date)

    def get_by_campaign_and_date_range(
        self,
        campaign_id: str,
        start_date: date,
        end_date: date,
    ) -> list[CampaignAnalyticsSchema]:
        campaign_analytics = self.get_by_campaign(campaign_id)
        return [a for a in campaign_analytics if start_date <= a.date <= end_date]
