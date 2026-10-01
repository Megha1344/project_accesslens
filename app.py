"""
AccessLens — Premium Developer Tool for Accessibility Simulation & Remediation
Main Streamlit Application Entry Point
"""
import streamlit as st

# Import Core Engine Modules
from core.url_fetcher import fetch_and_sanitize_url
from core.vision_filters import get_svg_filters_html
from core.wcag_math import calculate_contrast_ratio, auto_fix_contrast
from core.dom_parser import audit_html_accessibility
from core.keyboard_traps import analyze_keyboard_navigation

# Import UI Components
from components.hero import render_hero_section
from components.live_inspector import render_live_inspector
from components.sandbox import render_sandbox
from components.contrast_fixer import render_contrast_fixer_tab
from components.keyboard_tracer import render_keyboard_tracer
from components.audit_summary import render_audit_summary_panel
from samples.demo_sites import DEMO_SITES

# Set Page Config for Production Deployment
st.set_page_config(
    page_title="AccessLens — Developer Accessibility Suite",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Theme & Developer UI Styling
st.markdown(
    """
    <style>
    /* Dark Theme Core */
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    /* Top Header Banner */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #111827;
        border-bottom: 1px solid #1f2937;
        padding: 14px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .app-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .app-logo {
        font-size: 26px;
    }
    .app-name {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    .app-name span {
        color: #6366f1;
    }
    .app-tagline {
        font-size: 13px;
        color: #94a3b8;
    }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #111827;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #1f2937;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #312e81 !important;
        color: #ffffff !important;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600;
    }
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 800;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    # Header Banner
    st.markdown(
        """
        <div class="app-header">
            <div class="app-brand">
                <span class="app-logo">👁️</span>
                <div>
                    <div class="app-name">Access<span>Lens</span></div>
                    <div class="app-tagline">Don't just audit it — experience it!</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Sidebar Controls & Inspection Input Selection
    with st.sidebar:
        st.markdown("### 🔍 Inspection Source")
        input_mode = st.radio(
            "Choose Target:",
            options=["Sample Preset", "Fetch Live Website URL", "Raw HTML/CSS Code"],
            index=0
        )
        
        target_html = ""
        frame_notice = ""
        
        if input_mode == "Sample Preset":
            preset_key = st.selectbox(
                "Select Preset Website:",
                options=list(DEMO_SITES.keys()),
                format_func=lambda k: DEMO_SITES[k]["title"]
            )
            target_html = DEMO_SITES[preset_key]["html"]
            st.caption(DEMO_SITES[preset_key]["description"])
            
        elif input_mode == "Fetch Live Website URL":
            url_input = st.text_input("Enter Web URL:", value="https://example.com")
            if url_input:
                with st.spinner("Fetching target webpage DOM & analyzing headers..."):
                    fetch_res = fetch_and_sanitize_url(url_input)
                    target_html = fetch_res["html"]
                    frame_notice = fetch_res.get("restriction_notice", "")
                    
                    if not fetch_res["success"]:
                        st.error(fetch_res.get("error", "Error fetching URL"))
                    elif fetch_res.get("has_frame_restrictions"):
                        st.info("🔒 Site enforces X-Frame-Options/CSP restrictions. AccessLens DOM proxy rendering active.")
                
        else:
            st.info("Edit your HTML/CSS code snippet directly in the Inspection Sandbox tab.")
            target_html = DEMO_SITES["shoptech_audit_demo"]["html"]

    # Navigation Tabs
    tab_hero, tab_live, tab_sandbox, tab_contrast, tab_keyboard, tab_report = st.tabs([
        "🏠 Overview",
        "👁️ Live Sensory Inspector",
        "🧪 Inspection Sandbox",
        "🎨 Auto Contrast Fixer",
        "⌨️ Keyboard Navigation",
        "📊 WCAG Audit Report"
    ])
    
    with tab_hero:
        render_hero_section()
        st.markdown("---")
        st.markdown("#### ⚡ Quick Sensory Preview of Selected Target")
        render_live_inspector(target_html, frame_notice=frame_notice)

    with tab_live:
        render_live_inspector(target_html, frame_notice=frame_notice)
        
    with tab_sandbox:
        sandbox_code = render_sandbox()
        if sandbox_code:
            st.markdown("---")
            st.markdown("### 👁️ Real-time Sandbox Visual Preview")
            render_live_inspector(sandbox_code)

    with tab_contrast:
        render_contrast_fixer_tab()

    with tab_keyboard:
        render_keyboard_tracer(target_html)

    with tab_report:
        render_audit_summary_panel(target_html)

if __name__ == "__main__":
    main()
