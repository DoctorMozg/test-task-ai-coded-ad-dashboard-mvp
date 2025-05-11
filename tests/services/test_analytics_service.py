from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest

from dashboard.services.analytics_service import (
    calculate_campaign_performance_summary,
)


def test_calculate_campaign_performance_summary_empty():
    """Test calculating performance summary with no data."""
    with patch(
        "dashboard.services.analytics_service.get_campaign_analytics",
        return_value=[],
    ):
        summary = calculate_campaign_performance_summary(
            "test-campaign-id",
            datetime.now(UTC).date(),
            datetime.now(UTC).date(),
        )

        assert summary.impressions == 0
        assert summary.clicks == 0
        assert summary.ctr_pct == 0
        assert summary.cost_usd == 0


def test_calculate_campaign_performance_summary(sample_analytics_data):
    """Test calculating performance summary with sample data."""
    with patch(
        "dashboard.services.analytics_service.get_campaign_analytics",
        return_value=sample_analytics_data,
    ):
        summary = calculate_campaign_performance_summary(
            "test-campaign-id",
            datetime.now(UTC).date() - timedelta(days=1),
            datetime.now(UTC).date(),
        )

        assert summary.impressions == 2500
        assert summary.clicks == 110
        assert summary.ctr_pct == pytest.approx(4.4, 0.01)
        assert summary.cost_usd == 55.0
