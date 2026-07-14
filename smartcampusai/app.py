import streamlit as st
import utils.helpers  # Apply early page-switch patch for old Streamlit versions
from components.auth import init_session

# This is the main entry point of the SmartCampusAI application.
# It initializes the session state and redirects to the appropriate page based on auth state.

# In Streamlit, page config must be set at the entrypoint first.
try:
    st.set_page_config(
        page_title="SmartCampusAI",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
except st.errors.StreamlitAPIException:
    pass

# Initialize session parameters
init_session()

# Check authentication status and redirect
if st.session_state.get("logged_in", False):
    st.switch_page("pages/Dashboard.py")
else:
    st.switch_page("pages/Login.py")
