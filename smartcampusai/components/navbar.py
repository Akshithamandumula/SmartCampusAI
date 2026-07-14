import streamlit as st
from services.json_database import update_user

def render_navbar(page_title: str):
    """
    Renders a top navigation bar with search summary, dark mode toggle, and notification count.
    Also handles global dark mode stylesheet injection when toggled.
    """
    user = st.session_state.get("user_data")
    if not user:
        return

    # Invalidate session theme state with user data if out of sync
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = user.get("theme", "light") == "dark"

    # Inject dark mode styles if dark_mode is active
    if st.session_state.dark_mode:
        st.markdown(
            """
            <style>
                /* Force Dark Theme Variables and Backgrounds */
                html, body, [data-testid="stAppViewContainer"], .stApp {
                    background: radial-gradient(circle at top left, #0f172a 0%, #020617 100%) !important;
                    color: #f8fafc !important;
                }
                
                /* Sidebar container styling */
                [data-testid="stSidebar"] {
                    background-color: #0b0f19 !important;
                    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
                }
                
                /* Subviews & Glass cards override */
                .glass-card {
                    background: rgba(15, 23, 42, 0.65) !important;
                    border: 1px solid rgba(255, 255, 255, 0.08) !important;
                    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
                }
                
                .glass-card:hover {
                    box-shadow: 0 12px 40px 0 rgba(59, 130, 246, 0.15) !important;
                    border: 1px solid rgba(59, 130, 246, 0.3) !important;
                }
                
                .navbar-container {
                    background: rgba(15, 23, 42, 0.8) !important;
                    border: 1px solid rgba(255, 255, 255, 0.08) !important;
                }
                
                .metric-value {
                    color: #60a5fa !important;
                }
                
                .metric-label {
                    color: #94a3b8 !important;
                }
                
                .custom-table th {
                    background: rgba(30, 41, 59, 0.6) !important;
                    color: #94a3b8 !important;
                    border-bottom: 2px solid #334155 !important;
                }
                
                .custom-table td {
                    border-bottom: 1px solid #1e293b !important;
                    color: #e2e8f0 !important;
                }
                
                .custom-table tr:hover {
                    background: rgba(30, 41, 59, 0.4) !important;
                }
                
                /* Streamlit standard UI elements override */
                div[data-baseweb="input"] > input, 
                div[data-baseweb="textarea"] > textarea,
                div[role="combobox"] {
                    background-color: #1e293b !important;
                    color: #f8fafc !important;
                    border-color: #334155 !important;
                }
                
                div[data-baseweb="select"] > div {
                    background-color: #1e293b !important;
                    color: #f8fafc !important;
                }
                
                label, [data-testid="stMarkdownContainer"] p {
                    color: #e2e8f0 !important;
                }
                
                header {
                    background-color: transparent !important;
                }
                
                /* Tab headers */
                button[data-baseweb="tab"] {
                    color: #94a3b8 !important;
                }
                button[data-baseweb="tab"][aria-selected="true"] {
                    color: #3b82f6 !important;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

    # Compute unread notifications count
    notifications = user.get("notifications", [])
    unread_count = sum(1 for n in notifications if not n.get("read", False))
    unread_badge = f"<span style='background:#ef4444; color:white; border-radius:50%; padding:2px 6px; font-size:10px; font-weight:700; margin-left:5px; vertical-align:top;'>{unread_count}</span>" if unread_count > 0 else ""

    # UI structure using layout columns
    col_title, col_right = st.columns([3, 1])
    
    with col_title:
        st.markdown(
            f"""
            <div class="navbar-container" style="padding: 10px 20px; border-radius: 12px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                    <div>
                        <span style="color: #64748b; font-size: 0.8rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Portal / {page_title}</span>
                        <h2 style="margin: 0; color: {'#f8fafc' if st.session_state.dark_mode else '#1e293b'}; font-weight: 700; font-size: 1.5rem;">
                            Smart Campus AI
                        </h2>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        # Inline action container with dark mode toggle
        subcol1, subcol2 = st.columns([1, 1])
        with subcol1:
            theme_btn = st.button("☀️" if st.session_state.dark_mode else "🌙", key="theme_toggle_btn", help="Toggle Theme mode")
            if theme_btn:
                # Toggle and save
                st.session_state.dark_mode = not st.session_state.dark_mode
                user["theme"] = "dark" if st.session_state.dark_mode else "light"
                
                # Append activity log
                theme_str = "Dark" if st.session_state.dark_mode else "Light"
                user["activities"].insert(0, {
                    "time": "Just now",
                    "type": "Preference",
                    "description": f"Switched display to {theme_str} Mode."
                })
                
                st.session_state.user_data = user
                update_user(user)
                st.rerun()
                
        with subcol2:
            st.markdown(
                f"""
                <div style="text-align: center; padding-top: 10px; cursor: pointer;" title="Notifications">
                    <span style="font-size: 1.4rem;">🔔</span>{unread_badge}
                </div>
                """,
                unsafe_allow_html=True
            )
