from typing import cast

import streamlit as st

# Constants
# Session state keys
SESSION_AUTHENTICATED = "authenticated"
SESSION_USER_ID = "user_id"
SESSION_USERNAME = "username"
SESSION_REDIRECT_TO = "redirect_to"

# Page settings
PAGE_TITLE = "Advertising Dashboard MVP"
PAGE_ICON = "🚀"
PAGE_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# Navigation options
NAV_DASHBOARD = "Dashboard"
NAV_CREATE_CAMPAIGN = "Create Campaign"
NAV_CAMPAIGN_LIST = "Campaign List"

# UI text
SIDEBAR_TITLE = "Advertising Dashboard"
LOGGED_IN_AS = "Logged in as:"
NOT_LOGGED_IN = "Not logged in"
BUTTON_LOGOUT = "Logout"
BUTTON_LOGIN = "Login"
WELCOME_TITLE = "Welcome to Advertising Dashboard"
WELCOME_MESSAGE = """
Please log in to access the dashboard features.

Navigate to the Login page using the sidebar.
"""

# Initialize session state if not already initialized
if SESSION_AUTHENTICATED not in st.session_state:
    st.session_state[SESSION_AUTHENTICATED] = False
    st.session_state[SESSION_USER_ID] = None
    st.session_state[SESSION_USERNAME] = None

if SESSION_REDIRECT_TO not in st.session_state:
    st.session_state[SESSION_REDIRECT_TO] = None

# Set page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE,
)


def navigation() -> bool:
    """Handles the application navigation"""
    # Check for redirects
    if st.session_state[SESSION_REDIRECT_TO]:
        page = cast(str, st.session_state[SESSION_REDIRECT_TO])
        st.session_state[SESSION_REDIRECT_TO] = None

        if page == NAV_CREATE_CAMPAIGN:
            from dashboard.app.pages.create_campaign import create_campaign_page

            create_campaign_page()
            return True

        if page == NAV_CAMPAIGN_LIST:
            from dashboard.app.pages.campaign_list import campaign_list_page

            campaign_list_page()
            return True

    return False


# Main app
def main() -> None:
    # Sidebar logo/branding
    st.sidebar.title(SIDEBAR_TITLE)
    st.sidebar.markdown("---")

    # Authentication status
    if st.session_state[SESSION_AUTHENTICATED]:
        st.sidebar.success(f"{LOGGED_IN_AS} {st.session_state[SESSION_USERNAME]}")

        # Navigation options
        options: list[str] = [NAV_DASHBOARD, NAV_CREATE_CAMPAIGN, NAV_CAMPAIGN_LIST]
        selection: str = st.sidebar.radio("Navigation", options)

        # Handle navigation
        if selection == NAV_DASHBOARD:
            from dashboard.app.pages.dashboard import main as dashboard_page

            dashboard_page()

        elif selection == NAV_CREATE_CAMPAIGN:
            from dashboard.app.pages.create_campaign import main as create_campaign_page

            create_campaign_page()

        elif selection == NAV_CAMPAIGN_LIST:
            from dashboard.app.pages.campaign_list import main as campaign_list_page

            campaign_list_page()

        # Logout button
        if st.sidebar.button(BUTTON_LOGOUT):
            st.session_state[SESSION_AUTHENTICATED] = False
            st.session_state[SESSION_USER_ID] = None
            st.session_state[SESSION_USERNAME] = None
            st.rerun()
    else:
        st.sidebar.warning(NOT_LOGGED_IN)

        # Login button
        if st.sidebar.button(BUTTON_LOGIN):
            from dashboard.app.pages.login import main as login_page

            login_page()
            return

        # Main content for not logged in users
        st.title(WELCOME_TITLE)
        st.markdown(WELCOME_MESSAGE)


if __name__ == "__main__":
    # Check for redirects first
    if not navigation():
        main()
