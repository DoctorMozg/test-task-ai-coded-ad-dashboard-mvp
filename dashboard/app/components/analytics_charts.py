from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta

import altair as alt
import pandas as pd
import streamlit as st

from dashboard.data.models.analytics import CampaignAnalyticsSchema, MetricsSchema
from dashboard.data.models.campaign import CampaignSchema
from dashboard.data.store import campaign_store
from dashboard.services.analytics_service import (
    calculate_campaign_performance_summary,
    get_all_campaigns_performance,
    get_campaign_analytics,
)


def display_date_range_selector() -> tuple[date, date]:
    """Display a date range selector and return the selected dates."""
    col1, col2 = st.columns(2)

    end_date = datetime.now(UTC).date()
    start_date = end_date - timedelta(days=30)

    with col1:
        start_date = st.date_input("Start Date", value=start_date)

    with col2:
        end_date = st.date_input("End Date", value=end_date)

    if start_date > end_date:
        st.error("Start date must be before end date")
        start_date = end_date - timedelta(days=1)

    return start_date, end_date


def display_metrics_summary(metrics: MetricsSchema) -> None:
    """Display a summary of metrics in a clean UI."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Impressions", f"{metrics.impressions:,}")

    with col2:
        st.metric("Clicks", f"{metrics.clicks:,}")

    with col3:
        st.metric("CTR", f"{metrics.ctr_pct:.2f}%")

    with col4:
        st.metric("Cost", f"${metrics.cost_usd:.2f}")


def display_campaign_performance_chart(
    analytics_list: list[CampaignAnalyticsSchema],
    metric_name: str = "impressions",
) -> None:
    """Display a time series chart for campaign performance."""
    if not analytics_list:
        st.info("No data available for the selected date range")
        return

    # Prepare data for chart
    chart_data = []
    for analytic in analytics_list:
        metric_value = getattr(analytic.metrics, metric_name)
        chart_data.append(
            {
                "date": analytic.date,
                "value": metric_value,
                "metric": metric_name.replace("_", " ").title(),
            },
        )

    df = pd.DataFrame(chart_data)

    metric_title = metric_name.replace("_", " ").title()
    if metric_name == "cost_usd":
        metric_title = "Cost (USD)"
    elif metric_name == "ctr_pct":
        metric_title = "CTR (%)"

    # Create line chart
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("value:Q", title=metric_title),
            tooltip=["date:T", "value:Q"],
        )
        .properties(
            height=300,
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)


def display_metric_selector(
    on_change: Callable | None = None,
) -> str:
    """Display a metric selector and return the selected metric."""
    metric_options = {
        "impressions": "Impressions",
        "clicks": "Clicks",
        "ctr_pct": "CTR (%)",
        "cost_usd": "Cost (USD)",
    }

    return st.selectbox(
        "Select Metric",
        options=list(metric_options.keys()),
        format_func=lambda x: metric_options[x],
        on_change=on_change if on_change else None,
    )


def display_campaign_comparison_chart(
    campaign_metrics: dict[str, MetricsSchema],
    metric_name: str = "impressions",
) -> None:
    """Display a bar chart comparing campaigns by the selected metric."""
    if not campaign_metrics:
        st.info("No campaign data available")
        return

    # Prepare data for chart
    chart_data = []
    for campaign_id, metrics in campaign_metrics.items():
        campaign = campaign_store.get(campaign_id)
        if not campaign:
            continue

        metric_value = getattr(metrics, metric_name)
        chart_data.append(
            {
                "campaign": campaign.name,
                "value": metric_value,
            },
        )

    df = pd.DataFrame(chart_data)

    if df.empty:
        st.info("No data available for comparison")
        return

    # Sort by value descending
    df = df.sort_values("value", ascending=False)

    metric_title = metric_name.replace("_", " ").title()
    if metric_name == "cost_usd":
        metric_title = "Cost (USD)"
    elif metric_name == "ctr_pct":
        metric_title = "CTR (%)"

    # Create bar chart
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("campaign:N", title="Campaign", sort="-y"),
            y=alt.Y("value:Q", title=metric_title),
            tooltip=["campaign:N", "value:Q"],
        )
        .properties(
            height=300,
        )
    )

    st.altair_chart(chart, use_container_width=True)


def display_campaign_analytics_dashboard(
    campaign: CampaignSchema | None = None,
) -> None:
    """Display a complete analytics dashboard for a campaign or all campaigns."""
    start_date, end_date = display_date_range_selector()

    if campaign:
        # Single campaign view
        st.subheader(f"Campaign: {campaign.name}")

        # Get campaign analytics
        analytics_list = get_campaign_analytics(
            campaign.id,
            start_date,
            end_date,
        )

        # Display summary metrics
        summary = calculate_campaign_performance_summary(
            campaign.id,
            start_date,
            end_date,
        )
        display_metrics_summary(summary)

        # Display performance chart
        st.subheader("Performance Over Time")
        selected_metric = display_metric_selector()
        display_campaign_performance_chart(analytics_list, selected_metric)

    else:
        # All campaigns view
        st.subheader("All Campaigns Performance")

        # Get all campaign analytics summaries
        campaign_metrics = get_all_campaigns_performance(start_date, end_date)

        if not campaign_metrics:
            st.info("No campaign data available for the selected date range")
            return

        # Display overall summary
        overall_metrics = MetricsSchema(
            impressions=sum(m.impressions for m in campaign_metrics.values()),
            clicks=sum(m.clicks for m in campaign_metrics.values()),
            ctr_pct=sum(m.clicks for m in campaign_metrics.values())
            / max(sum(m.impressions for m in campaign_metrics.values()), 1)
            * 100,
            cost_usd=sum(m.cost_usd for m in campaign_metrics.values()),
        )

        display_metrics_summary(overall_metrics)

        # Display comparison chart
        st.subheader("Campaign Comparison")
        selected_metric = display_metric_selector()
        display_campaign_comparison_chart(campaign_metrics, selected_metric)
