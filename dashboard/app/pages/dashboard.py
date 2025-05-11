from datetime import UTC, datetime, timedelta

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Dashboard - Advertising Dashboard",
    page_icon="📊",
    layout="wide",
)


def main() -> None:
    # Authentication check
    if not st.session_state.get("authenticated", False):
        st.warning("Please log in to access this page")
        st.stop()

    # Dashboard header
    st.title("Campaign Dashboard")
    st.markdown("Overview of your advertising campaigns and performance metrics")

    # Date filter
    col1, col2 = st.columns([3, 1])
    with col2:
        days = st.selectbox(
            "Time period",
            options=[7, 14, 30, 90],
            format_func=lambda x: f"Last {x} days",
            index=1,
        )

    # Generate mock data for demonstration
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=days)
    date_range = [start_date + timedelta(days=x) for x in range(days)]

    data = pd.DataFrame(
        {
            "date": date_range,
            "impressions": [1000 + i * 50 + (i % 3) * 200 for i in range(days)],
            "clicks": [50 + i * 2 + (i % 5) * 10 for i in range(days)],
            "conversions": [5 + (i // 2) for i in range(days)],
            "cost": [20 + i * 1.5 for i in range(days)],
        },
    )

    data["ctr"] = (data["clicks"] / data["impressions"] * 100).round(2)
    data["cpa"] = (data["cost"] / data["conversions"]).round(2)
    data["date_str"] = data["date"].dt.strftime("%b %d")

    # Key metrics
    st.subheader("Key Performance Metrics")
    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        total_impressions = data["impressions"].sum()
        st.metric("Total Impressions", f"{total_impressions:,}")

    with metric2:
        total_clicks = data["clicks"].sum()
        st.metric("Total Clicks", f"{total_clicks:,}")

    with metric3:
        avg_ctr = (total_clicks / total_impressions * 100).round(2)
        st.metric("Average CTR", f"{avg_ctr}%")

    with metric4:
        total_cost = data["cost"].sum().round(2)
        st.metric("Total Spend", f"${total_cost:,}")

    # Charts
    st.subheader("Performance Trends")

    tab1, tab2 = st.tabs(["Impressions & Clicks", "Conversions & Cost"])

    with tab1:
        # Create a base chart for impressions
        base = alt.Chart(data).encode(
            x=alt.X("date_str:O", title="Date", axis=alt.Axis(labelAngle=-45)),
            tooltip=["date_str", "impressions", "clicks", "ctr"],
        )

        # Add bars for impressions
        bars = base.mark_bar().encode(
            y=alt.Y("impressions:Q", title="Impressions"),
            color=alt.value("#1f77b4"),
        )

        # Add line for clicks
        line = base.mark_line(color="red").encode(
            y=alt.Y("clicks:Q", title="Clicks", axis=alt.Axis(titleColor="red")),
        )

        # Combine the charts with dual y-axes
        chart = alt.layer(bars, line).resolve_scale(y="independent")

        st.altair_chart(chart, use_container_width=True)

    with tab2:
        # Create a base chart for conversions
        base = alt.Chart(data).encode(
            x=alt.X("date_str:O", title="Date", axis=alt.Axis(labelAngle=-45)),
            tooltip=["date_str", "conversions", "cost", "cpa"],
        )

        # Add bars for conversions
        bars = base.mark_bar().encode(
            y=alt.Y("conversions:Q", title="Conversions"),
            color=alt.value("#2ca02c"),
        )

        # Add line for cost
        line = base.mark_line(color="orange").encode(
            y=alt.Y("cost:Q", title="Cost ($)", axis=alt.Axis(titleColor="orange")),
        )

        # Combine the charts with dual y-axes
        chart = alt.layer(bars, line).resolve_scale(y="independent")

        st.altair_chart(chart, use_container_width=True)

    # Campaign performance table (placeholder)
    st.subheader("Campaign Performance")

    # Mock campaign data
    campaigns = pd.DataFrame(
        {
            "Campaign": [f"Campaign {i}" for i in range(1, 6)],
            "Status": ["Active", "Active", "Paused", "Active", "Draft"],
            "Impressions": [5234, 3245, 1254, 4521, 0],
            "Clicks": [234, 145, 42, 187, 0],
            "CTR (%)": [4.47, 4.47, 3.35, 4.14, 0],
            "Conversions": [12, 8, 2, 14, 0],
            "CPA ($)": [23.45, 18.75, 31.50, 20.10, 0],
        },
    )

    st.dataframe(campaigns, use_container_width=True)


if __name__ == "__main__":
    main()
