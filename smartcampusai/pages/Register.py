import streamlit as st
import time
from utils.helpers import init_page
from utils.validation import validate_email, validate_password
from components.auth import check_logged_in_redirect
from services.json_database import register_user

# Setup Page Config and Custom Styles
init_page("Register", layout="wide")

# Redirect if already logged in
check_logged_in_redirect()

# Header block
st.markdown(
    """
    <div style="text-align: center; margin-top: 30px; margin-bottom: 20px;">
        <h1 style="font-weight: 800; color: #1e3a8a; font-size: 2.5rem; margin-bottom: 5px;">
            🎓 SmartCampusAI
        </h1>
        <p style="color: #64748b; font-size: 1.1rem; font-weight: 500;">
            Join your campus AI companion network
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # Rich Information graphic
    st.markdown(
        """
        <div class="glass-card" style="padding: 40px; text-align: center; min-height: 520px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <div style="font-size: 6rem; margin-bottom: 20px; filter: drop-shadow(0 8px 16px rgba(37,99,235,0.1));">📝</div>
            <h2 style="color: #1e3a8a; font-weight: 700; margin-bottom: 15px;">Create Student Account</h2>
            <p style="color: #475569; font-size: 0.95rem; line-height: 1.6; max-width: 380px; margin: 0 auto 25px auto;">
                Create your student record today to track your course GPA, attendance records, organize pending assignments, and get AI-assisted recommendations.
            </p>
            <div style="text-align: left; background: rgba(37, 99, 235, 0.05); padding: 15px 20px; border-radius: 12px; border-left: 4px solid #2563eb; width: 100%; max-width: 380px;">
                <div style="font-weight: 600; color: #1e40af; font-size: 0.85rem; margin-bottom: 4px;">Password Checklist:</div>
                <ul style="margin: 0; padding-left: 15px; color: #475569; font-size: 0.78rem; font-weight: 500; line-height: 1.4;">
                    <li>Minimum 8 characters in length</li>
                    <li>Contains at least one letter (a-z)</li>
                    <li>Contains at least one digit (0-9)</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_right:
    # Registration form panel
    st.markdown(
        """
        <div class="glass-card" style="padding: 35px; min-height: 520px;">
            <div style="text-align: left; margin-bottom: 20px;">
                <h3 style="margin: 0; color: #1e293b; font-weight: 700; font-size: 1.4rem;">Student Registration</h3>
                <p style="margin: 3px 0 0 0; color: #64748b; font-size: 0.85rem;">Register using your valid campus details</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.container():
        # Input parameters
        full_name = st.text_input("Full Name", placeholder="e.g. John Doe")
        student_id = st.text_input("Student ID", placeholder="e.g. CS20261094")
        email = st.text_input("Student Email", placeholder="e.g. john.doe@campus.edu")
        
        col_p1, col_p2 = st.columns([1, 1])
        with col_p1:
            password = st.text_input("Password", type="password", placeholder="Create password")
        with col_p2:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Verify password")
            
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        # Submit execution
        register_submit = st.button("Register Account")
        
        st.markdown(
            """
            <div style="text-align: center; margin-top: 15px; margin-bottom: 10px; color: #64748b; font-size: 0.85rem; font-weight: 500;">
                Already have an account?
            </div>
            """,
            unsafe_allow_html=True
        )
        
        goto_login = st.button("Sign In with Existing Account", key="goto_login_btn")
        if goto_login:
            st.switch_page("pages/Login.py")
            
        # Form Validation
        if register_submit:
            if not full_name.strip() or not student_id.strip() or not email.strip() or not password or not confirm_password:
                st.error("⚠️ All fields are required. Please fill in the registration form completely.")
            elif not validate_email(email):
                st.error("❌ Invalid email format. Please enter a valid student email address (e.g. student@campus.edu).")
            elif password != confirm_password:
                st.error("❌ Password confirmation does not match the entered password.")
            else:
                # Validate password strength
                is_valid_pw, pw_message = validate_password(password)
                if not is_valid_pw:
                    st.error(f"❌ {pw_message}")
                else:
                    # Proceed with registration
                    success, message = register_user(full_name, student_id, email, password)
                    if success:
                        st.success(f"🎉 {message}")
                        time.sleep(1.5)
                        st.switch_page("pages/Login.py")
                    else:
                        st.error(f"❌ {message}")
