import streamlit as st
import time
from datetime import datetime
import os
from utils.helpers import init_page
from components.auth import check_logged_in_redirect, login_session
from services.json_database import authenticate_user, update_user

# Setup Page Config and Custom Styles
init_page("Login", layout="wide")

# Redirect if already logged in
check_logged_in_redirect()

# Main Container Wrapper
st.markdown(
    """
    <div style="text-align: center; margin-top: 30px; margin-bottom: 20px;">
        <h1 style="font-weight: 800; color: #1e3a8a; font-size: 2.5rem; margin-bottom: 5px;">
            🎓 SmartCampusAI
        </h1>
        <p style="color: #64748b; font-size: 1.1rem; font-weight: 500;">
            Your Intelligent Student Hub & Academic Companion
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # Campus Illustration / Graphic Welcome panel
    st.markdown(
        """
        <div class="glass-card" style="padding: 40px; text-align: center; min-height: 480px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <div style="font-size: 6rem; margin-bottom: 20px; filter: drop-shadow(0 8px 16px rgba(37,99,235,0.1));">🏫</div>
            <h2 style="color: #1e3a8a; font-weight: 700; margin-bottom: 15px;">Welcome back to Campus!</h2>
            <p style="color: #475569; font-size: 0.95rem; line-height: 1.6; max-width: 380px; margin: 0 auto 25px auto;">
                Access your personalized courses, timetable, attendance rate, grades tracker, and consult our advanced AI Advisor for academic and career support.
            </p>
            <div style="display: flex; gap: 20px; margin-top: 15px;">
                <div style="text-align: center; width: 90px; background: rgba(37,99,235,0.06); padding: 10px; border-radius: 12px; border: 1px solid rgba(37,99,235,0.1);">
                    <div style="font-size: 1.4rem; margin-bottom: 4px;">📈</div>
                    <div style="font-weight: 600; color: #1e40af; font-size: 0.72rem;">Live Stats</div>
                </div>
                <div style="text-align: center; width: 90px; background: rgba(37,99,235,0.06); padding: 10px; border-radius: 12px; border: 1px solid rgba(37,99,235,0.1);">
                    <div style="font-size: 1.4rem; margin-bottom: 4px;">🤖</div>
                    <div style="font-weight: 600; color: #1e40af; font-size: 0.72rem;">AI Helper</div>
                </div>
                <div style="text-align: center; width: 90px; background: rgba(37,99,235,0.06); padding: 10px; border-radius: 12px; border: 1px solid rgba(37,99,235,0.1);">
                    <div style="font-size: 1.4rem; margin-bottom: 4px;">📅</div>
                    <div style="font-weight: 600; color: #1e40af; font-size: 0.72rem;">Schedules</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_right:
    # Glassmorphism Login Card
    st.markdown(
        """
        <div class="glass-card" style="padding: 35px; min-height: 480px;">
            <div style="text-align: left; margin-bottom: 25px;">
                <h3 style="margin: 0; color: #1e293b; font-weight: 700; font-size: 1.4rem;">Sign In</h3>
                <p style="margin: 3px 0 0 0; color: #64748b; font-size: 0.85rem;">Enter your student email and password below</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # We render the inputs using Streamlit, styled with our custom CSS classes
    # To place them inside the card visual container, we can render the container visually and overlay the fields
    # Streamlit provides container layouts for grouping
    with st.container():
        # Input fields
        email = st.text_input("Student Email", placeholder="e.g. student@campus.edu")
        
        # Password options
        col_pw, col_show = st.columns([3, 1])
        with col_show:
            show_pw = st.checkbox("Show", help="Toggle password visibility")
        with col_pw:
            pw_type = "default" if show_pw else "password"
            password = st.text_input("Password", type=pw_type, placeholder="Enter password")
            
        col_rem, col_forgot = st.columns([1, 1])
        with col_rem:
            remember = st.checkbox("Remember Me", value=True)
        with col_forgot:
            # Custom styled forgot password link
            st.markdown(
                """
                <div style="text-align: right; padding-top: 5px;">
                    <a href="#" style="color: #2563eb; font-size: 0.8rem; font-weight: 500; text-decoration: none;" onclick="alert('Please contact Campus IT support at support@campus.edu to reset your password.')">Forgot Password?</a>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        # Action Buttons
        login_btn = st.button("Sign In")
        
        st.markdown(
            """
            <div style="text-align: center; margin-top: 20px; margin-bottom: 10px; color: #64748b; font-size: 0.85rem; font-weight: 500;">
                Don't have an account yet?
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Register redirect button
        register_btn = st.button("Create Student Account", key="goto_register_btn", help="Register as a new student")
        if register_btn:
            st.switch_page("pages/Register.py")

        # Login logic execution
        if login_btn:
            if not email.strip() or not password.strip():
                st.error("⚠️ All fields are required.")
            else:
                user = authenticate_user(email, password)
                if user:
                    # Update login activity logs
                    user["activities"].insert(0, {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "type": "Auth",
                        "description": "Logged in successfully."
                    })
                    update_user(user)
                    login_session(user)
                    
                    st.success("🎉 Welcome back! Redirecting to dashboard...")
                    time.sleep(1)
                    st.switch_page("pages/Dashboard.py")
                else:
                    st.error("❌ Invalid student email or password. Please try again.")
