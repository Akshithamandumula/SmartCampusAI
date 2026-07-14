import streamlit as st
import time
from datetime import datetime
from utils.helpers import init_page
from utils.validation import validate_password
from components.auth import require_auth
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from services.json_database import update_user, check_password, hash_password

# Setup protection and page structure
require_auth()
init_page("Settings", layout="wide")

# Render common elements
render_sidebar("Settings")
render_navbar("Portal Settings")

user = st.session_state.get("user_data")

st.markdown(
    """
    <div style="margin-bottom: 20px;">
        <p style="margin: 0; font-size: 0.9rem; color: #64748b;">
            Manage portal preferences, security credentials, and email updates.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col_pref, col_security = st.columns([1, 1], gap="large")

with col_pref:
    # Portal Preferences panel
    st.markdown('<div class="glass-card" style="min-height: 480px; padding: 30px;">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; margin-bottom: 20px;'>⚙️ System Preferences</h3>", unsafe_allow_html=True)
    
    # Render theme selection
    theme_choice = st.radio(
        "Application Theme",
        options=["Light Mode", "Dark Mode"],
        index=1 if st.session_state.dark_mode else 0,
        help="Switches visual portal appearance"
    )
    
    # Detect theme toggle from radio
    radio_dark = theme_choice == "Dark Mode"
    if radio_dark != st.session_state.dark_mode:
        st.session_state.dark_mode = radio_dark
        user["theme"] = "dark" if radio_dark else "light"
        user["activities"].insert(0, {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": "Preference",
            "description": f"Switched theme preference to {theme_choice}."
        })
        st.session_state.user_data = user
        update_user(user)
        st.rerun()

    st.markdown("<hr style='margin: 20px 0; border-color: rgba(226, 232, 240, 0.4);'/>", unsafe_allow_html=True)
    
    # Mock settings toggles
    st.markdown("<h5>Notifications & Alerts</h5>", unsafe_allow_html=True)
    
    user_settings = user.get("settings", {"email_alerts": True, "ai_suggestions": True})
    
    email_alert = st.toggle("Email Notifications", value=user_settings.get("email_alerts", True), help="Receive weekly GPA reports by email")
    ai_alert = st.toggle("AI Suggestion Alerts", value=user_settings.get("ai_suggestions", True), help="Prompt alerts on new assignments and exams")
    
    save_pref = st.button("Save Preferences", key="save_pref_btn")
    
    if save_pref:
        user["settings"] = {
            "email_alerts": email_alert,
            "ai_suggestions": ai_alert
        }
        user["activities"].insert(0, {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": "Preference",
            "description": "Updated notification settings."
        })
        if update_user(user):
            st.session_state.user_data = user
            st.success("🎉 Preferences saved successfully!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Failed to update preferences.")
            
    st.markdown('</div>', unsafe_allow_html=True)

with col_security:
    # Security / Password management panel
    st.markdown('<div class="glass-card" style="min-height: 480px; padding: 30px;">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; margin-bottom: 20px;'>🔒 Account Security</h3>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<p style='font-size: 0.85rem; color:#64748b;'>Update your student login password</p>", unsafe_allow_html=True)
        
        current_pw = st.text_input("Current Password", type="password", placeholder="Enter current password")
        new_pw = st.text_input("New Password", type="password", placeholder="Enter new password")
        confirm_new_pw = st.text_input("Confirm New Password", type="password", placeholder="Re-enter new password")
        
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        update_pw_btn = st.button("Update Password")
        
        if update_pw_btn:
            if not current_pw or not new_pw or not confirm_new_pw:
                st.error("⚠️ All password fields are required.")
            elif not check_password(current_pw, user.get("password", "")):
                st.error("❌ The current password entered is incorrect.")
            elif new_pw != confirm_new_pw:
                st.error("❌ The new password and confirmation password do not match.")
            elif current_pw == new_pw:
                st.warning("⚠️ The new password cannot be the same as your current password.")
            else:
                # Validate strength
                is_valid_pw, pw_message = validate_password(new_pw)
                if not is_valid_pw:
                    st.error(f"❌ {pw_message}")
                else:
                    # Update hashed password
                    user["password"] = hash_password(new_pw)
                    user["activities"].insert(0, {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "type": "Preference",
                        "description": "Student password updated successfully."
                    })
                    
                    if update_user(user):
                        st.session_state.user_data = user
                        st.success("🎉 Password updated successfully! Please use this new password next time you sign in.")
                        # Clear password fields by reloading
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error("❌ Failed to update password in the database.")
                        
    st.markdown('</div>', unsafe_allow_html=True)
