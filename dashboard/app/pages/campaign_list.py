from datetime import UTC, datetime
from typing import Any, TypedDict, cast

import streamlit as st

from dashboard.app.components.campaign_card import campaign_card
from dashboard.app.utils.sample_data import create_sample_campaign
from dashboard.data.models import CampaignSchema, CampaignStatusEnum
from dashboard.data.store import banner_store, campaign_store, targeting_store

# Session state keys
SESSION_REDIRECT_TO = "redirect_to"
SESSION_EDIT_CAMPAIGN_ID = "edit_campaign_id"

# UI text
BUTTON_CREATE_CAMPAIGN = "+ Create New Campaign"
BUTTON_CREATE_SAMPLE = "Create Sample Campaign"
NO_CAMPAIGNS_MESSAGE = (
    "You don't have any campaigns yet. Let's create a sample one for demonstration."
)
NO_MATCHING_CAMPAIGNS = "No campaigns match the selected filters."
SUCCESS_SAMPLE_CREATED = "Sample campaign created!"
LOGIN_WARNING = "Please log in to view campaigns."

# Sort options
SORT_NEWEST = "Newest"
SORT_OLDEST = "Oldest"
SORT_BUDGET_HIGH_LOW = "Budget (High to Low)"
SORT_BUDGET_LOW_HIGH = "Budget (Low to High)"

# Navigation targets
REDIRECT_CREATE_CAMPAIGN = "Create Campaign"
REDIRECT_EDIT_CAMPAIGN = "Edit Campaign"


class CampaignDetails(TypedDict):
    campaign: CampaignSchema
    banner: Any
    targeting: Any


def get_campaign_with_details(campaign_id: str) -> CampaignDetails | None:
    campaign = campaign_store.get(campaign_id)
    if not campaign:
        return None

    banner = banner_store.get(campaign.banner_id)
    targeting = targeting_store.get(campaign.targeting_id)

    return {
        "campaign": campaign,
        "banner": banner,
        "targeting": targeting,
    }


def update_campaign_status(campaign_id: str, new_status: CampaignStatusEnum) -> bool:
    campaign = campaign_store.get(campaign_id)
    if campaign:
        campaign_store.update(
            campaign_id,
            {
                "status": new_status,
                "updated_at": datetime.now(UTC),
            },
        )
        return True
    return False


def handle_no_campaigns(user_id: str) -> None:
    """Display UI for when user has no campaigns"""
    st.info(NO_CAMPAIGNS_MESSAGE)

    if st.button(BUTTON_CREATE_SAMPLE):
        create_sample_campaign(user_id)
        st.success(SUCCESS_SAMPLE_CREATED)
        st.rerun()


def filter_and_sort_campaigns(
    campaigns: list[CampaignSchema],
    status_filter: list[str],
    sort_by: str,
) -> list[CampaignSchema]:
    """Filter and sort campaigns based on selected criteria"""
    # Apply status filter
    if status_filter:
        campaigns = [c for c in campaigns if c.status.value in status_filter]

    # Apply sorting
    if sort_by == SORT_NEWEST:
        return sorted(
            campaigns,
            key=lambda c: c.created_at,
            reverse=True,
        )
    if sort_by == SORT_OLDEST:
        return sorted(campaigns, key=lambda c: c.created_at)
    if sort_by == SORT_BUDGET_HIGH_LOW:
        return sorted(
            campaigns,
            key=lambda c: c.budget_usd,
            reverse=True,
        )
    if sort_by == SORT_BUDGET_LOW_HIGH:
        return sorted(campaigns, key=lambda c: c.budget_usd)

    # Default case
    return campaigns


def display_campaigns(campaigns: list[CampaignSchema]) -> None:
    """Display the filtered campaigns"""
    st.subheader(f"Your Campaigns ({len(campaigns)})")

    if not campaigns:
        st.info(NO_MATCHING_CAMPAIGNS)
        return

    for campaign in campaigns:
        campaign_card(
            campaign,
            on_edit=lambda campaign_id: st.session_state.update(
                {
                    SESSION_EDIT_CAMPAIGN_ID: campaign_id,
                    SESSION_REDIRECT_TO: REDIRECT_EDIT_CAMPAIGN,
                },
            ),
            on_status_change=update_campaign_status,
        )
        st.markdown("---")


def campaign_list_page() -> None:
    st.title("Campaign List")

    # Check if user is authenticated
    if not st.session_state.get("authenticated"):
        st.warning(LOGIN_WARNING)
        st.stop()

    # Add campaign button
    if st.button(BUTTON_CREATE_CAMPAIGN):
        st.session_state[SESSION_REDIRECT_TO] = REDIRECT_CREATE_CAMPAIGN
        st.rerun()

    # Get user campaigns
    user_id = cast(str, st.session_state.user_id)
    user_campaigns: list[CampaignSchema] = campaign_store.get_by_user(user_id)

    # Create some sample campaigns if none exist
    if not user_campaigns:
        handle_no_campaigns(user_id)
        return

    # Filter options
    st.subheader("Filter Campaigns")

    col1, col2 = st.columns(2)

    with col1:
        status_filter: list[str] = st.multiselect(
            "Status",
            options=[status.value for status in CampaignStatusEnum],
            format_func=lambda x: x.capitalize(),
        )

    with col2:
        # Sort options
        sort_options = [
            SORT_NEWEST,
            SORT_OLDEST,
            SORT_BUDGET_HIGH_LOW,
            SORT_BUDGET_LOW_HIGH,
        ]
        sort_by: str = st.selectbox(
            "Sort By",
            options=sort_options,
        )

    # Filter and sort campaigns
    filtered_campaigns = filter_and_sort_campaigns(
        user_campaigns,
        status_filter,
        sort_by,
    )

    # Display the campaigns
    display_campaigns(filtered_campaigns)


# Main function to run the page
def main() -> None:
    campaign_list_page()


if __name__ == "__main__":
    main()
