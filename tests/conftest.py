from datetime import UTC, datetime
from unittest.mock import Mock

import pytest

from dashboard.data.models.analytics import CampaignAnalyticsSchema, MetricsSchema


@pytest.fixture
def mock_analytics_store():
    """Create a mock analytics store."""
    store = Mock()
    store.count.return_value = 0
    return store


@pytest.fixture
def mock_campaign_store():
    """Create a mock campaign store."""
    store = Mock()
    store.get_all.return_value = []
    return store


@pytest.fixture
def mock_ad_copy_store():
    """Create a mock ad copy store."""
    return Mock()


@pytest.fixture
def sample_analytics_data():
    """Create sample analytics data for testing."""
    return [
        CampaignAnalyticsSchema(
            campaign_id="test-campaign-id",
            date=datetime.now(UTC).date(),
            metrics=MetricsSchema(
                impressions=1000,
                clicks=50,
                ctr_pct=5.0,
                cost_usd=25.0,
            ),
        ),
        CampaignAnalyticsSchema(
            campaign_id="test-campaign-id",
            date=datetime.now(UTC).date().replace(day=datetime.now(UTC).date().day - 1),
            metrics=MetricsSchema(
                impressions=1500,
                clicks=60,
                ctr_pct=4.0,
                cost_usd=30.0,
            ),
        ),
    ]
