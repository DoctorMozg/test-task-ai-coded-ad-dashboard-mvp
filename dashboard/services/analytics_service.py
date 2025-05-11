import random
from datetime import UTC, date, datetime, timedelta

import streamlit as st

from dashboard.data.models.analytics import CampaignAnalyticsSchema, MetricsSchema
from dashboard.data.store import analytics_store, campaign_store


@st.cache_data(ttl=3600)
def generate_mock_analytics_data() -> None:
    """Generate mock analytics data for all campaigns."""
    # Only generate data if analytics store is empty
    if analytics_store.count() > 0:
        return

    campaigns = campaign_store.list()
    if not campaigns:
        return

    # Generate 30 days of data for each campaign
    end_date = datetime.now(UTC).date()
    start_date = end_date - timedelta(days=30)

    for campaign in campaigns:
        current_date = start_date

        # Base metrics that will grow/fluctuate over time
        base_impressions = random.randint(500, 2000)
        base_ctr = random.uniform(1.5, 4.5)
        base_cost = random.uniform(50, 200)

        while current_date <= end_date:
            # Add randomness and trends
            day_factor = 1 + ((current_date - start_date).days / 30) * 0.5
            weekend_boost = 1.2 if current_date.weekday() >= 5 else 1.0  # noqa: PLR2004
            random_factor = random.uniform(0.8, 1.2)

            impressions = int(
                base_impressions * day_factor * weekend_boost * random_factor,
            )
            ctr = base_ctr * random.uniform(0.9, 1.1)
            clicks = int(impressions * (ctr / 100))
            cost = base_cost * day_factor * random.uniform(0.9, 1.1)

            metrics = MetricsSchema(
                impressions=impressions,
                clicks=clicks,
                ctr_pct=ctr,
                cost_usd=round(cost, 2),
            )

            analytics = CampaignAnalyticsSchema(
                campaign_id=campaign.id,
                date=current_date,
                metrics=metrics,
            )

            analytics_store.add(analytics)
            current_date += timedelta(days=1)


def get_campaign_analytics(
    campaign_id: str,
    start_date: date,
    end_date: date,
) -> list[CampaignAnalyticsSchema]:
    """Get analytics for a specific campaign within a date range."""
    return analytics_store.get_by_campaign_and_date_range(
        campaign_id,
        start_date,
        end_date,
    )


def calculate_campaign_performance_summary(
    campaign_id: str,
    start_date: date,
    end_date: date,
) -> MetricsSchema:
    """Calculate summary metrics for a campaign over a date range."""
    analytics_list = get_campaign_analytics(campaign_id, start_date, end_date)

    if not analytics_list:
        return MetricsSchema(
            impressions=0,
            clicks=0,
            ctr_pct=0,
            cost_usd=0,
        )

    total_impressions = sum(a.metrics.impressions for a in analytics_list)
    total_clicks = sum(a.metrics.clicks for a in analytics_list)
    total_cost = sum(a.metrics.cost_usd for a in analytics_list)

    # Calculate overall CTR
    overall_ctr = (
        (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    )

    return MetricsSchema(
        impressions=total_impressions,
        clicks=total_clicks,
        ctr_pct=round(overall_ctr, 2),
        cost_usd=round(total_cost, 2),
    )


def get_all_campaigns_performance(
    start_date: date,
    end_date: date,
) -> dict[str, MetricsSchema]:
    """Get performance metrics for all campaigns in the specified date range."""
    campaigns = campaign_store.list()

    return {
        campaign.id: calculate_campaign_performance_summary(
            campaign.id,
            start_date,
            end_date,
        )
        for campaign in campaigns
    }
