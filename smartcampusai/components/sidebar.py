import streamlit as st
from streamlit_option_menu import option_menu
from components.auth import logout_session

def render_sidebar(current_page: str):
    """
    Renders a premium sidebar with profile card and custom option-menu navigation.
    Handles seamless redirection between main pages and views.
    """
    user = st.session_state.get("user_data")
    if not user:
        return
        
    with st.sidebar:
        # Title Header with Icon
        st.markdown(
            f"""
            <div style="text-align: center; margin-top: 15px; margin-bottom: 15px;">
                <h2 style="margin: 0; color: #2563eb; font-weight: 700; font-size: 1.5rem;">
                    🎓 SmartCampusAI
                </h2>
                <p style="margin: 0; color: #64748b; font-size: 0.8rem; font-weight: 500;">
                    AI-Driven Student Platform
                </p>
            </div>
            <hr style="margin-top: 0; margin-bottom: 15px; border-color: rgba(226, 232, 240, 0.5);"/>
            """,
            unsafe_allow_html=True
        )
        
        # Profile Summary Card
        avatar = user.get("avatar_emoji", "👨‍🎓")
        name = user.get("name", "Student")
        student_id = user.get("student_id", "ID: 20260001")
        dept = user.get("department", "CSE")
        
        st.markdown(
            f"""
            <div style="
                background: rgba(255, 255, 255, 0.4);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 14px;
                padding: 15px;
                margin-bottom: 20px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.01);
            ">
                <div style="font-size: 2.5rem; margin-bottom: 5px;">{avatar}</div>
                <div style="font-weight: 600; color: #1e293b; font-size: 1rem; line-height: 1.2;">{name}</div>
                <div style="color: #64748b; font-size: 0.75rem; margin-top: 3px; font-weight: 500;">{student_id}</div>
                <div style="
                    display: inline-block;
                    background: #dbeafe;
                    color: #1e40af;
                    font-size: 0.7rem;
                    padding: 2px 8px;
                    border-radius: 20px;
                    margin-top: 8px;
                    font-weight: 600;
                ">{dept[:22]}...</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Determine current selection index
        menu_options = [
            "Dashboard",
            "AI Assistant",
            "Student Profile",
            "Attendance",
            "Assignments",
            "Results",
            "Timetable",
            "Notifications",
            "Settings",
            "Logout"
        ]
        
        icons = [
            "grid",
            "chat-quote",
            "person-badge",
            "calendar2-check",
            "journal-text",
            "award",
            "clock",
            "bell",
            "gear",
            "box-arrow-right"
        ]
        
        # Calculate selected index
        selected_index = 0
        if current_page == "Profile":
            selected_index = 2
        elif current_page == "Settings":
            selected_index = 8
        elif current_page == "Dashboard":
            view = st.session_state.get("current_view", "dashboard")
            if view == "dashboard":
                selected_index = 0
            elif view == "ai_assistant":
                selected_index = 1
            elif view == "attendance":
                selected_index = 3
            elif view == "assignments":
                selected_index = 4
            elif view == "results":
                selected_index = 5
            elif view == "timetable":
                selected_index = 6
            elif view == "notifications":
                selected_index = 7
        
        # Render Option Menu
        selected = option_menu(
            menu_title=None,
            options=menu_options,
            icons=icons,
            menu_icon="cast",
            default_index=selected_index,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#64748b", "font-size": "14px"}, 
                "nav-link": {
                    "font-size": "14px", 
                    "text-align": "left", 
                    "margin": "0px 0px 4px 0px", 
                    "border-radius": "10px", 
                    "padding-top": "8px", 
                    "padding-bottom": "8px",
                    "font-family": "Outfit, sans-serif"
                },
                "nav-link-selected": {"background-color": "#2563eb", "color": "white", "font-weight": "500"},
            }
        )
        
        # Handle Navigation based on selection
        if selected == "Logout":
            logout_session()
        elif selected == "Student Profile":
            if current_page != "Profile":
                st.switch_page("pages/Profile.py")
        elif selected == "Settings":
            if current_page != "Settings":
                st.switch_page("pages/Settings.py")
        else:
            # Map dashboard subviews
            view_map = {
                "Dashboard": "dashboard",
                "AI Assistant": "ai_assistant",
                "Attendance": "attendance",
                "Assignments": "assignments",
                "Results": "results",
                "Timetable": "timetable",
                "Notifications": "notifications"
            }
            target_view = view_map.get(selected)
            
            # Update state
            if st.session_state.current_view != target_view:
                st.session_state.current_view = target_view
                if current_page != "Dashboard":
                    st.switch_page("pages/Dashboard.py")
                else:
                    st.rerun()
            elif current_page != "Dashboard":
                st.switch_page("pages/Dashboard.py")
