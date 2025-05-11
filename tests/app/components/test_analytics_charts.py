from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from matplotlib.dates import UTC

from dashboard.app.components.analytics_charts import (
    display_campaign_comparison_chart,
    display_campaign_performance_chart,
    display_metrics_summary,
)
from dashboard.data.models.analytics import MetricsSchema
from dashboard.data.models.campaign import CampaignSchema


@pytest.fixture
def metrics_sample():
    """Sample metrics for testing."""
    return MetricsSchema(
        impressions=10000,
        clicks=500,
        ctr_pct=5.0,
        cost_usd=250.0,
    )


@pytest.fixture
def campaign_sample():
    """Sample campaign for testing."""
    return CampaignSchema(
        id="test-campaign-1",
        name="Test Campaign 1",
        budget_usd=1000.0,
        start_date=datetime.now(UTC).date(),
        created_by="test-user",
        status="active",
        banner_id="test-banner",
        targeting_id="test-targeting",
    )


@pytest.mark.unit
def test_display_metrics_summary(metrics_sample):
    """Test metrics summary display."""
    with patch("streamlit.columns") as mock_cols:
        # Create mock column objects that support context manager
        col1, col2, col3, col4 = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        mock_cols.return_value = [col1, col2, col3, col4]

        with patch("streamlit.metric") as mock_metric:
            # Call function
            display_metrics_summary(metrics_sample)

            # Verify metrics are displayed correctly
            mock_metric.assert_any_call("Impressions", "10,000")
            mock_metric.assert_any_call("Clicks", "500")
            mock_metric.assert_any_call("CTR", "5.00%")
            mock_metric.assert_any_call("Cost", "$250.00")


@pytest.mark.unit
def test_display_campaign_performance_chart(sample_analytics_data):
    """Test campaign performance chart display."""
    with (
        patch("streamlit.altair_chart") as mock_chart,
        patch("streamlit.info") as mock_info,
        patch("pandas.DataFrame", return_value=MagicMock()),
    ):
        # Call function with sample data
        display_campaign_performance_chart(sample_analytics_data, "impressions")

        # Verify chart is displayed
        mock_chart.assert_called_once()
        mock_info.assert_not_called()

        # Test empty data case
        display_campaign_performance_chart([])
        mock_info.assert_called_once()


@pytest.mark.unit
def test_display_campaign_comparison_chart():
    """Test campaign comparison chart display."""
    campaign_metrics = {
        "campaign-1": MetricsSchema(
            impressions=1000,
            clicks=50,
            ctr_pct=5.0,
            cost_usd=100,
        ),
        "campaign-2": MetricsSchema(
            impressions=2000,
            clicks=80,
            ctr_pct=4.0,
            cost_usd=150,
        ),
    }

    mock_campaigns = [
        CampaignSchema(
            id="campaign-1",
            name="Campaign One",
            budget_usd=500,
            start_date=datetime.now(UTC).date(),
            created_by="user",
            status="active",
            banner_id="banner1",
            targeting_id="targeting1",
        ),
        CampaignSchema(
            id="campaign-2",
            name="Campaign Two",
            budget_usd=800,
            start_date=datetime.now(UTC).date(),
            created_by="user",
            status="active",
            banner_id="banner2",
            targeting_id="targeting2",
        ),
    ]

    # Create mock DataFrame with necessary attributes
    mock_df = MagicMock()
    mock_df.empty = False
    mock_df.sort_values.return_value = mock_df

    with (
        patch("streamlit.altair_chart") as mock_chart,
        patch("streamlit.info") as mock_info,
        patch("pandas.DataFrame", return_value=mock_df),
        patch("dashboard.data.store.campaign_store") as mock_campaign_store,
    ):
        # Setup mock campaign store to return correct campaign by ID
        mock_campaign_store.get = lambda id: next(  # noqa: A006
            (c for c in mock_campaigns if c.id == id),
            None,
        )

        # Call function with metrics
        display_campaign_comparison_chart(campaign_metrics, "impressions")

        # Verify chart is displayed
        assert mock_chart.call_count >= 1
        mock_info.assert_not_called()

        # Test empty data case
        mock_info.reset_mock()
        display_campaign_comparison_chart({})
        mock_info.assert_called_once()
