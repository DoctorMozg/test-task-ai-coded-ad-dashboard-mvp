import streamlit as st

# Initialize session state if not already initialized
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None

# Set page configuration
st.set_page_config(
    page_title="Advertising Dashboard MVP",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Main app
def main() -> None:
    # Sidebar logo/branding
    st.sidebar.title("Advertising Dashboard")
    st.sidebar.markdown("---")

    # Authentication status
    if st.session_state.authenticated:
        st.sidebar.success(f"Logged in as: {st.session_state.username}")

        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    else:
        st.sidebar.warning("Not logged in")

    # Main content
    if not st.session_state.authenticated:
        # Redirect to login (this will be handled by Streamlit's pages feature)
        # Just show a welcome message here
        st.title("Welcome to Advertising Dashboard")
        st.markdown(
            """
            Please log in to access the dashboard features.

            Navigate to the Login page using the sidebar.
            """,
        )
    else:
        # Show dashboard overview when logged in
        st.title("Dashboard Overview")
        st.markdown(
            """
            Use the sidebar navigation to access different sections:

            - Dashboard Overview
            - Create Campaign
            - Campaign List
            """,
        )

        # Placeholder for dashboard stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Campaigns", "0")
        with col2:
            st.metric("Total Impressions", "0")
        with col3:
            st.metric("Conversion Rate", "0%")


if __name__ == "__main__":
    main()
