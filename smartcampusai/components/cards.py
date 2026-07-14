import streamlit as st

def render_metric_card(label: str, value: str, icon: str, description: str = ""):
    """Renders a standard premium glassmorphism metric card."""
    st.markdown(
        f"""
        <div class="glass-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px;">
                <span class="metric-label">{label}</span>
                <span style="font-size: 1.6rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.05));">{icon}</span>
            </div>
            <div class="metric-value">{value}</div>
            <p style="margin: 0; font-size: 0.75rem; color: #64748b; font-weight: 500;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_attendance_card(attendance_pct: float):
    """Renders an attendance card complete with a responsive progress bar indicator."""
    color = "#2563eb" if attendance_pct >= 75 else "#ef4444"
    st.markdown(
        f"""
        <div class="glass-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px;">
                <span class="metric-label">Attendance Rate</span>
                <span style="font-size: 1.6rem;">📅</span>
            </div>
            <div class="metric-value">{attendance_pct:.1f}%</div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width: {attendance_pct}%; background: {color};"></div>
            </div>
            <p style="margin: 8px 0 0 0; font-size: 0.72rem; color: #64748b; font-weight: 500;">
                {"Requirement met (Min 75%)" if attendance_pct >= 75 else "Below requirements! Check classes."}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_ai_suggestion_card(suggestion: str):
    """Renders a card featuring dynamic AI advice with a soft custom color theme."""
    st.markdown(
        f"""
        <div class="glass-card" style="
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.05) 0%, rgba(255,255,255,0.7) 100%) !important;
            border-left: 4px solid #2563eb !important;
        ">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                <span style="font-size: 1.3rem;">💡</span>
                <span style="font-size: 0.8rem; font-weight: 600; color: #2563eb; text-transform: uppercase; letter-spacing: 0.5px;">AI Suggestions</span>
            </div>
            <p style="margin: 0; font-size: 0.9rem; font-weight: 500; color: #334155; line-height: 1.4;">
                {suggestion}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_recent_activity_item(time_str: str, activity_type: str, desc: str):
    """Renders a modern timeline row item for the activities list."""
    # Determine color tag
    color_map = {
        "System": {"bg": "#dbeafe", "fg": "#1e40af"},
        "Auth": {"bg": "#e0f2fe", "fg": "#0369a1"},
        "Acad": {"bg": "#dcfce7", "fg": "#15803d"},
        "Chat": {"bg": "#f3e8ff", "fg": "#6b21a8"},
        "Preference": {"bg": "#fef3c7", "fg": "#b45309"}
    }
    tag = color_map.get(activity_type, {"bg": "#f1f5f9", "fg": "#475569"})
    
    st.markdown(
        f"""
        <div style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid rgba(226, 232, 240, 0.3);">
            <div style="
                background: {tag['bg']};
                color: {tag['fg']};
                font-size: 0.65rem;
                padding: 3px 8px;
                border-radius: 6px;
                font-weight: 700;
                min-width: 70px;
                text-align: center;
                text-transform: uppercase;
            ">
                {activity_type}
            </div>
            <div style="flex-grow: 1;">
                <p style="margin: 0; font-size: 0.85rem; font-weight: 500; color: #334155;">{desc}</p>
                <span style="font-size: 0.72rem; color: #94a3b8; font-weight: 500;">{time_str}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
