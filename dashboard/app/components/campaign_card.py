from collections.abc import Callable

import streamlit as st

from dashboard.data.models import CampaignSchema, CampaignStatusEnum

# Status color mapping
STATUS_COLORS: dict[CampaignStatusEnum, str] = {
    CampaignStatusEnum.DRAFT: "gray",
    CampaignStatusEnum.SCHEDULED: "blue",
    CampaignStatusEnum.ACTIVE: "green",
    CampaignStatusEnum.PAUSED: "orange",
    CampaignStatusEnum.COMPLETED: "purple",
    CampaignStatusEnum.REJECTED: "red",
}

# Button keys
EDIT_BUTTON_PREFIX = "edit_"
STATUS_SELECTOR_PREFIX = "status_"
UPDATE_BUTTON_PREFIX = "update_"


def get_status_color(status: CampaignStatusEnum) -> str:
    return STATUS_COLORS.get(status, "gray")


def campaign_card(
    campaign: CampaignSchema,
    on_edit: Callable[[str], None] | None = None,
    on_status_change: Callable[[str, CampaignStatusEnum], None] | None = None,
) -> None:
    status_color = get_status_color(campaign.status)

    with st.container():
        card_html = f"""
        <div style="padding: 10px; border: 1px solid #ddd;
             border-radius: 5px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between;
                 align-items: center;">
                <h3 style="margin: 0;">{campaign.name}</h3>
                <span style="background-color: {status_color}; color: white;
                      padding: 3px 8px; border-radius: 10px;
                      font-size: 0.8em;">
                    {campaign.status.value.upper()}
                </span>
            </div>
            <p>Budget: ${campaign.budget_usd:.2f}</p>
            <p>Start Date: {campaign.start_date.strftime("%Y-%m-%d")}</p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if (
                on_edit
                and callable(on_edit)
                and st.button(
                    "Edit",
                    key=f"{EDIT_BUTTON_PREFIX}{campaign.id}",
                )
            ):
                on_edit(campaign.id)

        with col2:
            if on_status_change and callable(on_status_change):
                available_status_changes: list[CampaignStatusEnum] = []

                if campaign.status == CampaignStatusEnum.DRAFT:
                    available_status_changes = [CampaignStatusEnum.SCHEDULED]
                elif campaign.status == CampaignStatusEnum.SCHEDULED:
                    available_status_changes = [
                        CampaignStatusEnum.ACTIVE,
                        CampaignStatusEnum.DRAFT,
                    ]
                elif campaign.status == CampaignStatusEnum.ACTIVE:
                    available_status_changes = [
                        CampaignStatusEnum.PAUSED,
                        CampaignStatusEnum.COMPLETED,
                    ]
                elif campaign.status == CampaignStatusEnum.PAUSED:
                    available_status_changes = [
                        CampaignStatusEnum.ACTIVE,
                        CampaignStatusEnum.COMPLETED,
                    ]

                if available_status_changes:
                    new_status = st.selectbox(
                        "Change status",
                        options=available_status_changes,
                        format_func=lambda x: x.value.capitalize(),
                        key=f"{STATUS_SELECTOR_PREFIX}{campaign.id}",
                    )

                    if st.button(
                        "Update Status",
                        key=f"{UPDATE_BUTTON_PREFIX}{campaign.id}",
                    ):
                        on_status_change(campaign.id, new_status)
