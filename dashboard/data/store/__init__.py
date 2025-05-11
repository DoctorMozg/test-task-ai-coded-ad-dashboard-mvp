from dashboard.data.store.ad_copy_store import AdCopyStore
from dashboard.data.store.analytics_store import AnalyticsStore
from dashboard.data.store.banner_store import BannerStore
from dashboard.data.store.campaign_store import CampaignStore
from dashboard.data.store.memory_store import InMemoryStore
from dashboard.data.store.targeting_store import InterestStore, TargetingStore
from dashboard.data.store.user_store import UserStore

# Create singleton instances for stores
user_store = UserStore()
campaign_store = CampaignStore()
banner_store = BannerStore()
targeting_store = TargetingStore()
interest_store = InterestStore()
analytics_store = AnalyticsStore()
ad_copy_store = AdCopyStore()

__all__ = [
    "AdCopyStore",
    "AnalyticsStore",
    "BannerStore",
    "CampaignStore",
    "InMemoryStore",
    "InterestStore",
    "TargetingStore",
    "UserStore",
    "ad_copy_store",
    "analytics_store",
    "banner_store",
    "campaign_store",
    "interest_store",
    "targeting_store",
    "user_store",
]
