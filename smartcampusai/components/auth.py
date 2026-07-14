import streamlit as st
import utils.helpers  # Apply early page-switch patch for old Streamlit versions

def init_session():
    """Initializes standard SmartCampusAI session state parameters."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_data" not in st.session_state:
        st.session_state.user_data = None
    if "current_view" not in st.session_state:
        st.session_state.current_view = "dashboard"
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

def require_auth():
    """
    Enforces authentication check.
    If the user is not logged in, redirects immediately to Login page.
    """
    init_session()
    if not st.session_state.logged_in:
        st.warning("Please log in to access this page.")
        st.switch_page("pages/Login.py")
        st.stop()

def check_logged_in_redirect():
    """
    If the user is already logged in, redirects away from Login/Register pages.
    """
    init_session()
    if st.session_state.logged_in:
        st.switch_page("pages/Dashboard.py")
        st.stop()

def login_session(user_data: dict):
    """Sets session state variables on successful login."""
    st.session_state.logged_in = True
    st.session_state.user_data = user_data
    if "dark_mode" in user_data:
        st.session_state.dark_mode = user_data.get("theme", "light") == "dark"
    # Set default view to dashboard
    st.session_state.current_view = "dashboard"

def logout_session():
    """Clears authentication session parameters and redirects to Login."""
    st.session_state.logged_in = False
    st.session_state.user_data = None
    st.session_state.current_view = "dashboard"
    st.switch_page("pages/Login.py")
    st.stop()
