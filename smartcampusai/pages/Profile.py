import streamlit as st
import time
from datetime import datetime
from utils.helpers import init_page
from components.auth import require_auth
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from services.json_database import update_user

# Setup page protection and navigation layout
require_auth()
init_page("Profile", layout="wide")

# Render common elements
render_sidebar("Profile")
render_navbar("Student Profile")

user = st.session_state.get("user_data")

st.markdown(
    """
    <div style="margin-bottom: 20px;">
        <p style="margin: 0; font-size: 0.9rem; color: #64748b;">
            View and manage your official student record and portal settings.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col_details, col_edit = st.columns([1, 1], gap="large")

with col_details:
    # Render static visual Card
    avatar = user.get("avatar_emoji", "👨‍🎓")
    st.markdown(
        f"""
        <div class="glass-card" style="text-align: center; padding: 40px; min-height: 480px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <div style="font-size: 5rem; margin-bottom: 15px; filter: drop-shadow(0 6px 12px rgba(37,99,235,0.15));">{avatar}</div>
            <h2 style="color: {'#f8fafc' if st.session_state.dark_mode else '#1e293b'}; margin: 0; font-weight: 700;">{user.get('name')}</h2>
            <p style="color: #2563eb; font-weight: 600; margin-top: 5px; font-size: 0.95rem;">{user.get('department')}</p>
            <p style="color: #64748b; font-size: 0.82rem; margin-top: -10px; font-weight: 500;">{user.get('semester')}</p>
            
            <div style="width: 100%; border-top: 1px solid rgba(226,232,240,0.5); margin-top: 20px; padding-top: 20px;">
                <table style="width: 100%; text-align: left; font-size: 0.85rem; border-collapse: collapse;">
                    <tr style="height: 35px; border-bottom: 1px solid rgba(226,232,240,0.3);">
                        <td style="color:#64748b; font-weight:500;">Student ID:</td>
                        <td style="color:{'#f8fafc' if st.session_state.dark_mode else '#334155'}; font-weight: 600; text-align: right;">{user.get('student_id')}</td>
                    </tr>
                    <tr style="height: 35px; border-bottom: 1px solid rgba(226,232,240,0.3);">
                        <td style="color:#64748b; font-weight:500;">Official Email:</td>
                        <td style="color:{'#f8fafc' if st.session_state.dark_mode else '#334155'}; font-weight: 600; text-align: right;">{user.get('email')}</td>
                    </tr>
                    <tr style="height: 35px; border-bottom: 1px solid rgba(226,232,240,0.3);">
                        <td style="color:#64748b; font-weight:500;">Cumulative CGPA:</td>
                        <td style="color:#2563eb; font-weight: 700; text-align: right;">{user.get('gpa', 3.92):.2f}</td>
                    </tr>
                    <tr style="height: 35px;">
                        <td style="color:#64748b; font-weight:500;">Attendance Rate:</td>
                        <td style="color:#15803d; font-weight: 700; text-align: right;">{user.get('attendance', 92.5):.1f}%</td>
                    </tr>
                </table>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_edit:
    # Edit details form
    st.markdown('<div class="glass-card" style="min-height: 480px; padding: 30px;">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; margin-bottom: 20px;'>✏️ Update Profile Details</h3>", unsafe_allow_html=True)
    
    with st.container():
        # Setup form fields initialized with existing values
        name_input = st.text_input("Full Name", value=user.get("name", ""))
        
        # Dept options list
        depts = [
            "Computer Science & Engineering",
            "Electrical & Electronics Engineering",
            "Mechanical Engineering",
            "Civil Engineering",
            "Business Administration",
            "Information Technology"
        ]
        curr_dept = user.get("department", depts[0])
        dept_idx = depts.index(curr_dept) if curr_dept in depts else 0
        dept_input = st.selectbox("Department", depts, index=dept_idx)
        
        # Semester options list
        semesters = [f"{i}th Semester" for i in range(1, 9)]
        curr_sem = user.get("semester", semesters[4])
        sem_idx = semesters.index(curr_sem) if curr_sem in semesters else 0
        semester_input = st.selectbox("Current Semester", semesters, index=sem_idx)
        
        # Emoji Avatar choices
        emojis = ["👨‍🎓", "👩‍🎓", "🧑‍🎓", "👨‍💻", "👩‍💻", "🦊", "🦁", "🐼", "🚀", "⚡"]
        curr_emoji = user.get("avatar_emoji", emojis[0])
        emoji_idx = emojis.index(curr_emoji) if curr_emoji in emojis else 0
        avatar_input = st.selectbox("Choose Avatar Emoji", emojis, index=emoji_idx)
        
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        
        save_changes = st.button("Save Profile Changes")
        
        if save_changes:
            if not name_input.strip():
                st.error("❌ Name field cannot be left blank.")
            else:
                # Update attributes
                user["name"] = name_input.strip()
                user["department"] = dept_input
                user["semester"] = semester_input
                user["avatar_emoji"] = avatar_input
                
                # Append activity log
                user["activities"].insert(0, {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "type": "Acad",
                    "description": "Updated student profile details."
                })
                
                # Save changes
                if update_user(user):
                    st.session_state.user_data = user
                    st.success("🎉 Profile updated successfully!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Failed to update profile details in database.")
                    
    st.markdown('</div>', unsafe_allow_html=True)
