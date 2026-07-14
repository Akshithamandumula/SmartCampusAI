import streamlit as st
import os

# Monkey-patch st.switch_page for older Streamlit versions (like 1.23.1)
if not hasattr(st, "switch_page"):
    def custom_switch_page(page: str):
        from streamlit.runtime.scriptrunner import RerunData, RerunException
        from streamlit.source_util import get_pages
        
        target_clean = page.replace("\\", "/").lower()
        target_base = os.path.splitext(os.path.basename(target_clean))[0]
        
        pages = get_pages("app.py")
        for page_hash, config in pages.items():
            script_path_clean = config["script_path"].replace("\\", "/").lower()
            script_base = os.path.splitext(os.path.basename(script_path_clean))[0]
            
            if target_base == script_base or script_path_clean.endswith(target_clean):
                raise RerunException(
                    RerunData(
                        page_script_hash=page_hash,
                        page_name=config["page_name"],
                    )
                )
        raise ValueError(f"Could not find page {page}")
    st.switch_page = custom_switch_page

def load_css(file_path: str = "styles/style.css"):
    """
    Loads and injects custom CSS from styles/style.css.
    """
    # Try resolving relative path if execution context differs
    if not os.path.exists(file_path):
        # Check in parent or package path
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "..", "styles", "style.css"),
            os.path.join(".", "styles", "style.css"),
            "styles/style.css"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                file_path = path
                break

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                css_content = f.read()
            # Injecting CSS wrapped in style tags
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading CSS: {str(e)}")
    else:
        # Avoid crashing, just print warning to logs or show silent indicator
        pass

def init_page(title: str, layout: str = "wide"):
    """
    Initializes standard Streamlit page settings and styles.
    This must be invoked at the very top of each page.
    """
    # Streamlit requires set_page_config to be the very first command.
    # To prevent duplicate calls triggering exceptions, we check session state or let it throw naturally.
    try:
        st.set_page_config(
            page_title=f"{title} | SmartCampusAI",
            page_icon="🎓",
            layout=layout,
            initial_sidebar_state="expanded"
        )
    except st.errors.StreamlitAPIException:
        # If already configured, ignore.
        pass
    
    # Inject CSS
    load_css()

def format_percentage(value: float) -> str:
    """Formats a float value as percentage."""
    return f"{value:.1f}%"

def format_gpa(value: float) -> str:
    """Formats a float value as GPA."""
    return f"{value:.2f}"
