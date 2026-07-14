import streamlit as st
import time
import pandas as pd
import numpy as np
from datetime import datetime
from utils.helpers import init_page
from components.auth import require_auth
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from components.cards import (
    render_metric_card, 
    render_attendance_card, 
    render_ai_suggestion_card, 
    render_recent_activity_item
)
from services.json_database import update_user, save_chat_history, load_chat_history
from services.ai_service import generate_ai_response

# 1. Enforce authentication and load page config
require_auth()
init_page("Dashboard", layout="wide")

# 2. Render sidebar and header navbar components
render_sidebar("Dashboard")

user = st.session_state.get("user_data")
view = st.session_state.get("current_view", "dashboard")

# Map view internal name to printable header title
view_titles = {
    "dashboard": "Dashboard Overview",
    "ai_assistant": "AI Academic Assistant",
    "attendance": "Attendance Tracker",
    "assignments": "My Assignments",
    "results": "Grades & Results",
    "timetable": "Weekly Timetable",
    "notifications": "Notification Center"
}

render_navbar(view_titles.get(view, "Dashboard"))

# 3. View Router rendering
if view == "dashboard":
    # ----------------------------------------------------
    # VIEW: MAIN DASHBOARD OVERVIEW
    # ----------------------------------------------------
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <h3 style="margin:0; font-weight:600; color: {'#f8fafc' if st.session_state.dark_mode else '#1e293b'};">
                Welcome back, {user.get('name')}! 👋
            </h3>
            <p style="margin: 0; font-size: 0.9rem; color: #64748b;">
                Here is your academic overview for today.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Row 1: Primary academic metrics (4 columns grid)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        render_attendance_card(user.get("attendance", 92.5))
        
    with col2:
        render_metric_card(
            label="Pending Assignments",
            value=str(user.get("pending_assignments", 3)),
            icon="📝",
            description="2 tasks due this week"
        )
        
    with col3:
        render_metric_card(
            label="Upcoming Exams",
            value=str(user.get("exams", 2)),
            icon="🧠",
            description="Next: Linear Algebra (July 25)"
        )
        
    with col4:
        render_metric_card(
            label="Cumulative GPA",
            value=f"{user.get('gpa', 3.92):.2f}",
            icon="🏆",
            description="Top 5% of your class"
        )
        
    # Row 2: Secondary Content (Quick Actions, AI Suggestion, Recent Activities, Charts)
    col_left, col_right = st.columns([2, 1], gap="medium")
    
    with col_left:
        # GPA Trend / Semester Marks chart (using standard Streamlit charts with Pandas)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0;'>📊 Semester Performance Analytics</h4>", unsafe_allow_html=True)
        
        # Build DataFrame out of academic records
        results = user.get("results", [])
        if results:
            df = pd.DataFrame(results)
            # Create a clean visual representation
            col_chart1, col_chart2 = st.columns([3, 2])
            with col_chart1:
                st.markdown("<p style='font-size: 0.85rem; color:#64748b; margin-bottom: 10px;'>Exam Marks comparison across courses</p>", unsafe_allow_html=True)
                chart_data = pd.DataFrame({
                    'Marks Obtained': df['marks'].values
                }, index=df['course_code'].values)
                st.bar_chart(chart_data)
            with col_chart2:
                # Summary table
                st.markdown(
                    """
                    <table class="custom-table" style="font-size: 0.85rem; width: 100%;">
                        <thead>
                            <tr><th>Code</th><th>Course</th><th>Grade</th></tr>
                        </thead>
                        <tbody>
                    """,
                    unsafe_allow_html=True
                )
                for res in results[:4]:
                    st.markdown(
                        f"<tr><td>{res['course_code']}</td><td>{res['course_name']}</td><td><b>{res['grade']}</b></td></tr>",
                        unsafe_allow_html=True
                    )
                st.markdown("</tbody></table>", unsafe_allow_html=True)
        else:
            st.info("No grading records available.")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Actions Panel
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0;'>⚡ Student Quick Actions</h4>", unsafe_allow_html=True)
        
        qa_col1, qa_col2, qa_col3 = st.columns(3)
        with qa_col1:
            btn_ai = st.button("💬 Ask AI Advisor", key="qa_btn_ai")
            if btn_ai:
                st.session_state.current_view = "ai_assistant"
                st.rerun()
        with qa_col2:
            btn_tt = st.button("📅 View Timetable", key="qa_btn_tt")
            if btn_tt:
                st.session_state.current_view = "timetable"
                st.rerun()
        with qa_col3:
            btn_prof = st.button("👤 Edit Profile", key="qa_btn_prof")
            if btn_prof:
                st.switch_page("pages/Profile.py")
                
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        # Dynamic AI Advice Card
        gpa = user.get("gpa", 3.9)
        att = user.get("attendance", 90.0)
        
        if gpa >= 3.8 and att >= 90:
            advice = "Outstanding performance! You are tracking toward Honours. Focus on your Neural Networks Project (due in 6 days) to maintain your strong 3.92 CGPA."
        elif gpa < 3.0 or att < 75:
            advice = "⚠️ Attention required. Keep check of assignments and attend classes to stay above the 75% graduation threshold. Ask me for exam study tips!"
        else:
            advice = "Good job. Try submitting your Linear Algebra assignment early this week to free up prep time for upcoming exams."
            
        render_ai_suggestion_card(advice)
        
        # Recent Activities Card
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0; margin-bottom: 15px;'>🕒 Recent Activities</h4>", unsafe_allow_html=True)
        
        activities = user.get("activities", [])
        if activities:
            for act in activities[:4]:
                render_recent_activity_item(
                    time_str=act.get("time", "Just now"),
                    activity_type=act.get("type", "System"),
                    desc=act.get("description", "")
                )
        else:
            st.markdown("<p style='font-size:0.85rem; color:#64748b;'>No recent activities logged.</p>", unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

elif view == "ai_assistant":
    # ----------------------------------------------------
    # VIEW: AI ASSISTANT CHATBOT
    # ----------------------------------------------------
    st.markdown(
        """
        <div style="margin-bottom: 15px;">
            <p style="margin: 0; font-size: 0.9rem; color: #64748b;">
                Ask academic questions, program help, study planners, or check campus guidelines below.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load past chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = load_chat_history(user.get("email"))
        
        # Initialize default greeting if history is empty
        if not st.session_state.chat_messages:
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": f"Hi {user.get('name')}! I am your SmartCampusAI Academic Advisor. I am ready to help you prepare for exams, check due dates, explain code, or advise on career paths. What's on your mind today?"
                }
            ]
            
    # Clear conversation history button
    col_chat_title, col_chat_clear = st.columns([4, 1])
    with col_chat_clear:
        clear_chat = st.button("🗑️ Clear Chat", key="clear_chat_button")
        if clear_chat:
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": f"Chat history cleared. How can I help you, {user.get('name')}?"
                }
            ]
            save_chat_history(user.get("email"), st.session_state.chat_messages)
            st.rerun()

    # Create message bubbles frame
    st.markdown('<div style="min-height: 400px; padding: 10px; border-radius: 12px; margin-bottom: 10px;">', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat Input Box
    prompt = st.chat_input("Ask a question (e.g., 'What assignments do I have due?' or 'Explain Binary Trees')")
    
    if prompt:
        # 1. Render user message
        with st.chat_message("user"):
            st.markdown(prompt)
            
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # 2. Render Assistant response with custom visual typing dots
        with st.chat_message("assistant"):
            placeholder = st.empty()
            
            # Show animated typing status
            placeholder.markdown(
                """
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Generate AI response passing student profile details
            response_content = generate_ai_response(
                prompt=prompt, 
                chat_history=st.session_state.chat_messages[:-1],
                student_info=user
            )
            
            # Render final markdown response
            placeholder.markdown(response_content)
            
        st.session_state.chat_messages.append({"role": "assistant", "content": response_content})
        
        # 3. Log Chat Activity and save database
        user["activities"].insert(0, {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": "Chat",
            "description": f"Asked AI: \"{prompt[:35]}...\""
        })
        st.session_state.user_data = user
        update_user(user)
        save_chat_history(user.get("email"), st.session_state.chat_messages)

elif view == "attendance":
    # ----------------------------------------------------
    # VIEW: ATTENDANCE DETAILS
    # ----------------------------------------------------
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>📅 Course Attendance Analysis</h3>", unsafe_allow_html=True)
    
    # Progress gauge
    att = user.get("attendance", 92.5)
    st.markdown(f"<h4>Total Attendance Rate: <b>{att:.1f}%</b></h4>", unsafe_allow_html=True)
    color = "#2563eb" if att >= 75 else "#ef4444"
    st.markdown(
        f"""
        <div class="progress-bar-container" style="height: 14px; margin-bottom: 20px;">
            <div class="progress-bar-fill" style="width: {att}%; background: {color};"></div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Attendance details list
    attendance_data = [
        {"Course Code": "CS 301", "Subject": "Artificial Intelligence", "Lectures Conducted": 30, "Attended": 28, "Rate": "93.3%", "Status": "Good"},
        {"Course Code": "MAT 204", "Subject": "Linear Algebra", "Lectures Conducted": 24, "Attended": 22, "Rate": "91.7%", "Status": "Good"},
        {"Course Code": "CS 302", "Subject": "Software Engineering", "Lectures Conducted": 20, "Attended": 18, "Rate": "90.0%", "Status": "Good"},
        {"Course Code": "CS 205", "Subject": "Data Structures Lab", "Lectures Conducted": 15, "Attended": 14, "Rate": "93.3%", "Status": "Good"}
    ]
    
    st.markdown(
        """
        <table class="custom-table">
            <thead>
                <tr>
                    <th>Code</th><th>Subject</th><th>Total Lectures</th><th>Attended</th><th>Rate</th><th>Status</th>
                </tr>
            </thead>
            <tbody>
        """,
        unsafe_allow_html=True
    )
    for course in attendance_data:
        st.markdown(
            f"""
            <tr>
                <td>{course['Course Code']}</td>
                <td>{course['Subject']}</td>
                <td>{course['Lectures Conducted']}</td>
                <td>{course['Attended']}</td>
                <td><b>{course['Rate']}</b></td>
                <td><span style="color: #15803d; font-weight:600;">{course['Status']}</span></td>
            </tr>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</tbody></table>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif view == "assignments":
    # ----------------------------------------------------
    # VIEW: ASSIGNMENTS TRACKER
    # ----------------------------------------------------
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>📝 Assignments Manager</h3>", unsafe_allow_html=True)
    
    assignments = user.get("assignments", [])
    if assignments:
        st.markdown(
            """
            <table class="custom-table" style="margin-bottom: 20px;">
                <thead>
                    <tr>
                        <th>Subject</th><th>Assignment Title</th><th>Due Date</th><th>Status</th><th>Grade</th>
                    </tr>
                </thead>
                <tbody>
            """,
            unsafe_allow_html=True
        )
        for i, task in enumerate(assignments):
            status_style = "color:#d97706; font-weight:600;" if task['status'] == "Pending" else "color:#15803d; font-weight:600;"
            grade_val = task.get("grade", "-")
            st.markdown(
                f"""
                <tr>
                    <td>{task['subject']}</td>
                    <td>{task['title']}</td>
                    <td>{task['due_date']}</td>
                    <td><span style="{status_style}">{task['status']}</span></td>
                    <td><b>{grade_val}</b></td>
                </tr>
                """,
                unsafe_allow_html=True
            )
        st.markdown("</tbody></table>", unsafe_allow_html=True)
        
        # Interactive status submit control
        st.markdown("---")
        st.markdown("<h5>✏️ Submit/Complete Assignment</h5>", unsafe_allow_html=True)
        pending_titles = [t['title'] for t in assignments if t['status'] == "Pending"]
        
        if pending_titles:
            select_col, submit_col = st.columns([3, 1])
            with select_col:
                selected_task_title = st.selectbox("Select Pending Assignment", pending_titles)
            with submit_col:
                st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                mark_submitted = st.button("Mark Completed", key="mark_submitted_btn")
                
            if mark_submitted:
                for task in assignments:
                    if task['title'] == selected_task_title:
                        task['status'] = "Submitted"
                        task['grade'] = "Pending Grading"
                        break
                        
                # Update task metrics
                user["pending_assignments"] = sum(1 for t in assignments if t['status'] == "Pending")
                user["assignments"] = assignments
                user["activities"].insert(0, {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "type": "Acad",
                    "description": f"Submitted assignment: \"{selected_task_title}\""
                })
                
                st.session_state.user_data = user
                update_user(user)
                st.success("Assignment status submitted successfully!")
                time.sleep(1)
                st.rerun()
        else:
            st.success("🎉 Outstanding work! All current assignments are completed.")
    else:
        st.info("No assignments are currently registered for this student.")
        
    st.markdown('</div>', unsafe_allow_html=True)

elif view == "results":
    # ----------------------------------------------------
    # VIEW: GRADES AND RESULTS
    # ----------------------------------------------------
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>🏆 Grades Summary</h3>", unsafe_allow_html=True)
    
    st.markdown(f"<h4>Current Semester CGPA: <span style='color:#2563eb;'>{user.get('gpa', 3.92):.2f}</span></h4>", unsafe_allow_html=True)
    
    results = user.get("results", [])
    if results:
        st.markdown(
            """
            <table class="custom-table">
                <thead>
                    <tr>
                        <th>Course Code</th><th>Course Name</th><th>Credits</th><th>Marks</th><th>Letter Grade</th>
                    </tr>
                </thead>
                <tbody>
            """,
            unsafe_allow_html=True
        )
        total_credits = 0
        total_weighted_gpa = 0
        for course in results:
            total_credits += course['credits']
            st.markdown(
                f"""
                <tr>
                    <td>{course['course_code']}</td>
                    <td>{course['course_name']}</td>
                    <td>{course['credits']}</td>
                    <td>{course['marks']}</td>
                    <td><b>{course['grade']}</b></td>
                </tr>
                """,
                unsafe_allow_html=True
            )
        st.markdown(
            f"""
            <tr style="background: rgba(37,99,235,0.05); font-weight:700;">
                <td colspan="2">Total Core Credits Earned</td>
                <td>{total_credits}</td>
                <td colspan="2" style="text-align: right;">CGPA: {user.get('gpa', 3.92):.2f}</td>
            </tr>
            </tbody></table>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("No grade results are currently registered.")
    st.markdown('</div>', unsafe_allow_html=True)

elif view == "timetable":
    # ----------------------------------------------------
    # VIEW: TIMETABLE WEEKDAYS
    # ----------------------------------------------------
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>📅 Weekly Timetable</h3>", unsafe_allow_html=True)
    
    timetable = user.get("timetable", {})
    if timetable:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in days:
            classes = timetable.get(day, [])
            if classes:
                st.markdown(f"<h5 style='color:#2563eb; border-bottom: 1px solid rgba(37, 99, 235, 0.2); padding-bottom: 5px; margin-top:15px;'>{day}</h5>", unsafe_allow_html=True)
                st.markdown(
                    """
                    <table class="custom-table" style="font-size: 0.9rem;">
                        <thead>
                            <tr><th style="width: 30%;">Time Block</th><th style="width: 50%;">Course</th><th style="width: 20%;">Room / Hall</th></tr>
                        </thead>
                        <tbody>
                    """,
                    unsafe_allow_html=True
                )
                for class_row in classes:
                    st.markdown(
                        f"""
                        <tr>
                            <td>🕒 {class_row['time']}</td>
                            <td><b>{class_row['subject']}</b></td>
                            <td>🏢 {class_row['room']}</td>
                        </tr>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown("</tbody></table>", unsafe_allow_html=True)
    else:
        st.info("No timetable schedule loaded.")
    st.markdown('</div>', unsafe_allow_html=True)

elif view == "notifications":
    # ----------------------------------------------------
    # VIEW: NOTIFICATION CENTER
    # ----------------------------------------------------
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>🔔 Notifications</h3>", unsafe_allow_html=True)
    
    notifications = user.get("notifications", [])
    
    col_act_left, col_act_right = st.columns([4, 1])
    with col_act_right:
        # Mark all as read feature
        unread_nots = [n for n in notifications if not n.get("read", False)]
        if unread_nots:
            mark_read = st.button("Mark All Read", key="mark_all_read_notif")
            if mark_read:
                for n in notifications:
                    n["read"] = True
                user["notifications"] = notifications
                user["activities"].insert(0, {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "type": "Preference",
                    "description": "Cleared all unread notifications."
                })
                st.session_state.user_data = user
                update_user(user)
                st.success("Notifications marked read.")
                time.sleep(1)
                st.rerun()
                
    st.markdown("---")
    
    if notifications:
        for notif in notifications:
            bg_color = "rgba(37, 99, 235, 0.04)" if not notif.get("read", False) else "transparent"
            border_style = "left: 3px solid #2563eb" if not notif.get("read", False) else "left: 1px solid rgba(0,0,0,0.05)"
            read_status_lbl = "🔵" if not notif.get("read", False) else ""
            
            st.markdown(
                f"""
                <div style="background: {bg_color}; border-left: {border_style.split(':')[1]}; padding: 12px 18px; border-radius: 8px; margin-bottom: 12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight: 600; font-size: 0.95rem; color:{'#f8fafc' if st.session_state.dark_mode else '#1e293b'}">{read_status_lbl} {notif['title']}</span>
                        <span style="font-size: 0.72rem; color: #94a3b8;">{notif['time']}</span>
                    </div>
                    <p style="margin: 4px 0 0 0; font-size: 0.85rem; color:#64748b;">{notif['message']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown("<p style='font-size:0.9rem; color:#64748b;'>No notifications available.</p>", unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
