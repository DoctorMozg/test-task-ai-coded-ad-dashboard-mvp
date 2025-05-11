import streamlit as st

from dashboard.app.components import display_campaign_analytics_dashboard
from dashboard.data.store import campaign_store
from dashboard.services.analytics_service import generate_mock_analytics_data


def main() -> None:
    # Authentication check
    if not st.session_state.get("authenticated", False):
        st.warning("Please log in to access this page")
        st.stop()

    # Generate mock analytics data if needed
    with st.spinner("Preparing analytics data..."):
        generate_mock_analytics_data()

    # Dashboard header
    st.title("Campaign Dashboard")
    st.markdown("Overview of your advertising campaigns and performance metrics")

    # Get all campaigns
    campaigns = campaign_store.list()

    if not campaigns:
        st.info("No campaigns found. Create a campaign to see analytics.")
        if st.button("Create Your First Campaign"):
            st.switch_page("pages/create_campaign.py")
        return

    # Add campaign selector in sidebar
    with st.sidebar:
        st.header("Dashboard Controls")

        view_options = ["All Campaigns", "Individual Campaign"]
        selected_view = st.radio("Select View", options=view_options)

        selected_campaign = None
        if selected_view == "Individual Campaign":
            campaign_options = {c.id: c.name for c in campaigns}
            selected_campaign_id = st.selectbox(
                "Select Campaign",
                options=list(campaign_options.keys()),
                format_func=lambda x: campaign_options[x],
            )
            selected_campaign = campaign_store.get(selected_campaign_id)

    # Display campaign analytics based on selection
    if selected_campaign:
        display_campaign_analytics_dashboard(selected_campaign)
    else:
        display_campaign_analytics_dashboard()


if __name__ == "__main__":
    main()
