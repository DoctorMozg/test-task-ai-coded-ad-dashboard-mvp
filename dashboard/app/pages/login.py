import streamlit as st


def main() -> None:
    # Check if already authenticated
    if st.session_state.get("authenticated", False):
        st.success("You are already logged in.")
        st.info("You can access the dashboard from the sidebar navigation.")
        return

    # Login/Register tabs
    tab1, tab2 = st.tabs(["Login", "Register"])

    # Login form
    with tab1:
        st.header("Login")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")

            if submit_button:
                if username and password:
                    # For MVP, simple authentication with hardcoded user
                    if username == "demo" and password == "demo123":  # noqa: S105
                        st.session_state.authenticated = True
                        st.session_state.user_id = "1"
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")

    # Registration form
    with tab2:
        st.header("Register")

        with st.form("register_form"):
            new_username = st.text_input("Username")
            email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            register_button = st.form_submit_button("Register")

            if register_button:
                if not all([new_username, email, new_password, confirm_password]):
                    st.warning("Please fill out all fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    # In the real implementation, we would register the user
                    # For MVP, just show a success message
                    st.success("Registration successful! You can now login.")
                    # Automatically switch to login tab
                    st.info("Please log in with your new credentials.")


if __name__ == "__main__":
    main()
