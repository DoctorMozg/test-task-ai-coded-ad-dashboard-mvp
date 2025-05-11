from datetime import UTC, datetime, timedelta
from typing import Any, cast

import streamlit as st

from dashboard.app.components.image_uploader import BannerData, image_uploader
from dashboard.app.components.targeting_selector import (
    TargetingData,
    targeting_selector,
)
from dashboard.data.models import (
    AdBannerSchema,
    AudienceTargetingSchema,
    CampaignSchema,
    CampaignStatusEnum,
)
from dashboard.data.store import banner_store, campaign_store, targeting_store

# Session state keys
SESSION_CAMPAIGN_STEP = "campaign_step"
SESSION_CAMPAIGN_DATA = "campaign_data"
SESSION_BANNER_DATA = "banner_data"
SESSION_TARGETING_DATA = "targeting_data"
SESSION_REDIRECT_TO = "redirect_to"

# Step numbers
STEP_1 = 1  # Campaign details
STEP_2 = 2  # Ad Banner
STEP_3 = 3  # Audience targeting
STEP_4 = 4  # Review and submit

# Navigation steps
STEP_CAMPAIGN_DETAILS = "Campaign Details"
STEP_AD_BANNER = "Ad Banner"
STEP_AUDIENCE_TARGETING = "Audience Targeting"
STEP_REVIEW_SUBMIT = "Review & Submit"

# UI text
BUTTON_NEXT_BANNER = "Next: Ad Banner"
BUTTON_NEXT_TARGETING = "Next: Audience Targeting"
BUTTON_NEXT_REVIEW = "Next: Review"
BUTTON_BACK = "← Back"
BUTTON_CREATE_CAMPAIGN = "Create Campaign"

# Form validation messages
ERROR_CAMPAIGN_NAME_REQUIRED = "Campaign name is required."
ERROR_MINIMUM_BUDGET = "Minimum budget is $10."
ERROR_END_DATE = "End date must be after start date."
ERROR_UPLOAD_BANNER = "Please upload a banner image first."
ERROR_LOCATION_REQUIRED = "Please add at least one location."
ERROR_INTERESTS_REQUIRED = "Please select at least one interest."
SUCCESS_CAMPAIGN_CREATED = "Campaign created successfully!"

# Default values
DEFAULT_BUDGET = 100.0
MIN_BUDGET = 10.0
MAX_BUDGET = 10000.0
BUDGET_STEP = 10.0
DEFAULT_DATE_OFFSET_DAYS = 1
DEFAULT_END_DATE_OFFSET_DAYS = 30

# Navigation targets
REDIRECT_CAMPAIGN_LIST = "Campaign List"

# Path constants
ASSETS_PATH_PREFIX = "/assets"
DASHBOARD_ASSETS_PATH_PREFIX = "dashboard/assets"


def display_campaign_preview(
    campaign_data: dict[str, Any],
    banner_data: BannerData,
    targeting_data: TargetingData,
) -> None:
    st.subheader("Campaign Preview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Campaign Details")
        st.write(f"**Name:** {campaign_data.get('name')}")
        st.write(f"**Budget:** ${campaign_data.get('budget_usd', 0):.2f}")

        date_str = campaign_data.get("start_date").strftime("%Y-%m-%d")
        st.write(f"**Start Date:** {date_str}")

        if campaign_data.get("end_date"):
            end_date_str = campaign_data.get("end_date").strftime("%Y-%m-%d")
            st.write(f"**End Date:** {end_date_str}")
        else:
            st.write("**End Date:** Continuous")

    with col2:
        st.markdown("### Targeting Summary")

        age_range = targeting_data.get("age_range")
        st.write(f"**Age Group:** {age_range.min_age}-{age_range.max_age}")

        locations = targeting_data.get("locations", [])
        if locations:
            st.markdown("**Locations:**")
            for loc in locations:
                location_parts = [loc.country]
                if loc.region:
                    location_parts.append(loc.region)
                if loc.city:
                    location_parts.append(loc.city)
                st.write(f"- {', '.join(location_parts)}")

        if targeting_data.get("interests"):
            st.write(f"**Number of Interests:** {len(targeting_data.get('interests'))}")

    st.markdown("### Banner Preview")
    if banner_data:
        img_path = banner_data.get("image_url").replace(
            ASSETS_PATH_PREFIX,
            DASHBOARD_ASSETS_PATH_PREFIX,
        )
        st.image(img_path, caption=banner_data.get("name"))

        dimensions = f"{banner_data.get('width_px')}x{banner_data.get('height_px')}"
        st.write(f"**Dimensions:** {dimensions} pixels")


def campaign_form_step1() -> None:
    """Handle Step 1: Campaign Details"""
    st.subheader(STEP_CAMPAIGN_DETAILS)

    campaign_name = st.text_input(
        "Campaign Name",
        value=st.session_state[SESSION_CAMPAIGN_DATA].get("name", ""),
    )

    budget_value = float(
        st.session_state[SESSION_CAMPAIGN_DATA].get(
            "budget_usd",
            DEFAULT_BUDGET,
        ),
    )

    budget = st.number_input(
        "Budget (USD)",
        min_value=MIN_BUDGET,
        max_value=MAX_BUDGET,
        value=budget_value,
        step=BUDGET_STEP,
    )

    col1, col2 = st.columns(2)

    with col1:
        default_start = datetime.now(UTC) + timedelta(days=DEFAULT_DATE_OFFSET_DAYS)
        start_date = st.date_input(
            "Start Date",
            value=st.session_state[SESSION_CAMPAIGN_DATA].get(
                "start_date",
                default_start,
            ),
            min_value=datetime.now(UTC).date(),
        )

    with col2:
        end_date_required = st.checkbox(
            "Set End Date",
            value=bool(st.session_state[SESSION_CAMPAIGN_DATA].get("end_date")),
        )

        end_date = None
        if end_date_required:
            default_end = datetime.now(UTC) + timedelta(
                days=DEFAULT_END_DATE_OFFSET_DAYS,
            )
            end_date = st.date_input(
                "End Date",
                value=st.session_state[SESSION_CAMPAIGN_DATA].get(
                    "end_date",
                    default_end,
                ),
                min_value=start_date,
            )

    # Validation
    form_valid = True
    if not campaign_name:
        st.warning(ERROR_CAMPAIGN_NAME_REQUIRED)
        form_valid = False

    if budget < MIN_BUDGET:
        st.warning(ERROR_MINIMUM_BUDGET)
        form_valid = False

    if end_date_required and end_date <= start_date:
        st.warning(ERROR_END_DATE)
        form_valid = False

    if st.button(BUTTON_NEXT_BANNER) and form_valid:
        # Save campaign data to session state
        end_date_value = None
        if end_date_required and end_date:
            end_date_value = datetime.combine(end_date, datetime.min.time())

        st.session_state[SESSION_CAMPAIGN_DATA] = {
            "name": campaign_name,
            "budget_usd": budget,
            "start_date": datetime.combine(start_date, datetime.min.time()),
            "end_date": end_date_value,
            "created_by": st.session_state.user_id,
            "status": CampaignStatusEnum.DRAFT,
        }

        st.session_state[SESSION_CAMPAIGN_STEP] = STEP_2
        st.rerun()


def campaign_form_step2() -> None:
    """Handle Step 2: Ad Banner"""
    # Banner upload step
    banner_data: BannerData | None = image_uploader(st.session_state.user_id)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(BUTTON_BACK):
            st.session_state[SESSION_CAMPAIGN_STEP] = STEP_1
            st.rerun()

    with col2:
        if st.button(BUTTON_NEXT_TARGETING) and banner_data:
            st.session_state[SESSION_BANNER_DATA] = banner_data
            st.session_state[SESSION_CAMPAIGN_STEP] = STEP_3
            st.rerun()
        elif st.button(BUTTON_NEXT_TARGETING):
            st.warning(ERROR_UPLOAD_BANNER)


def campaign_form_step3() -> None:
    """Handle Step 3: Audience Targeting"""
    # Audience targeting step
    targeting_data: TargetingData = targeting_selector("targeting_")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(BUTTON_BACK):
            st.session_state[SESSION_CAMPAIGN_STEP] = STEP_2
            st.rerun()

    with col2:
        if st.button(BUTTON_NEXT_REVIEW):
            if not targeting_data.get("locations"):
                st.warning(ERROR_LOCATION_REQUIRED)
            elif not targeting_data.get("interests"):
                st.warning(ERROR_INTERESTS_REQUIRED)
            else:
                st.session_state[SESSION_TARGETING_DATA] = targeting_data
                st.session_state[SESSION_CAMPAIGN_STEP] = STEP_4
                st.rerun()


def campaign_form_step4() -> None:
    """Handle Step 4: Review and Submit"""
    # Review and submit step
    display_campaign_preview(
        cast(dict[str, Any], st.session_state[SESSION_CAMPAIGN_DATA]),
        cast(BannerData, st.session_state[SESSION_BANNER_DATA]),
        cast(TargetingData, st.session_state[SESSION_TARGETING_DATA]),
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(BUTTON_BACK):
            st.session_state[SESSION_CAMPAIGN_STEP] = STEP_3
            st.rerun()

    with col2:
        if st.button(BUTTON_CREATE_CAMPAIGN):
            # Create banner
            banner = AdBannerSchema.model_validate(
                st.session_state[SESSION_BANNER_DATA],
            )
            added_banner = banner_store.add(banner)

            # Create targeting
            targeting_data = cast(
                TargetingData,
                st.session_state[SESSION_TARGETING_DATA],
            )
            targeting = AudienceTargetingSchema(
                age_range=targeting_data["age_range"],
                locations=targeting_data["locations"],
                interests=targeting_data["interests"],
            )
            added_targeting = targeting_store.add(targeting)

            # Create campaign
            campaign_data = st.session_state[SESSION_CAMPAIGN_DATA]
            campaign_data["banner_id"] = added_banner.id
            campaign_data["targeting_id"] = added_targeting.id

            campaign = CampaignSchema.model_validate(campaign_data)
            campaign_store.add(campaign)

            # Success message and reset
            st.success(SUCCESS_CAMPAIGN_CREATED)

            # Reset session state
            st.session_state[SESSION_CAMPAIGN_STEP] = STEP_1
            st.session_state[SESSION_CAMPAIGN_DATA] = {}
            st.session_state[SESSION_BANNER_DATA] = None
            st.session_state[SESSION_TARGETING_DATA] = None

            # Redirect to campaign list
            st.session_state[SESSION_REDIRECT_TO] = REDIRECT_CAMPAIGN_LIST
            st.rerun()


def create_campaign_page() -> None:  # noqa: C901,PLR0912
    st.title("Create Campaign")

    # Check if user is authenticated
    if not st.session_state.get("authenticated"):
        st.warning("Please log in to create a campaign.")
        st.stop()

    # Initialize session state for multi-step form
    if SESSION_CAMPAIGN_STEP not in st.session_state:
        st.session_state[SESSION_CAMPAIGN_STEP] = STEP_1

    if SESSION_CAMPAIGN_DATA not in st.session_state:
        st.session_state[SESSION_CAMPAIGN_DATA] = {}

    if SESSION_BANNER_DATA not in st.session_state:
        st.session_state[SESSION_BANNER_DATA] = None

    if SESSION_TARGETING_DATA not in st.session_state:
        st.session_state[SESSION_TARGETING_DATA] = None

    # Progress indicator
    steps = [
        STEP_CAMPAIGN_DETAILS,
        STEP_AD_BANNER,
        STEP_AUDIENCE_TARGETING,
        STEP_REVIEW_SUBMIT,
    ]
    current_step: int = st.session_state[SESSION_CAMPAIGN_STEP]

    progress_html = ""
    for i, step in enumerate(steps, 1):
        if i < current_step:
            progress_html += f'<span style="color:green;">✓ {step}</span> → '
        elif i == current_step:
            progress_html += (
                f'<span style="color:blue;font-weight:bold;">● {step}</span> → '
            )
        else:
            progress_html += f'<span style="color:gray;">○ {step}</span> → '

    progress_html = progress_html[:-3]  # Remove last arrow
    st.markdown(
        f'<div style="text-align:center;">{progress_html}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # Handle current step
    if current_step == STEP_1:
        campaign_form_step1()
    elif current_step == STEP_2:
        campaign_form_step2()
    elif current_step == STEP_3:
        campaign_form_step3()
    elif current_step == STEP_4:
        campaign_form_step4()


# Main function to run the page
def main() -> None:
    create_campaign_page()


if __name__ == "__main__":
    main()
