"""
Inspection Sandbox Component
Allows developers to paste raw HTML/CSS, test custom snippets, select sample sites,
and run live real-time DOM audits.
"""
import streamlit as st
from samples.demo_sites import DEMO_SITES

def render_sandbox():
    """Renders the HTML/CSS Inspection Sandbox UI."""
    st.markdown("## 🧪 Inspection Sandbox")
    st.markdown(
        "Experiment with your own HTML/CSS snippets or choose a sample site to inspect real-time DOM accessibility violations, test contrast ratios, and view keyboard navigation paths."
    )
    
    col_sel1, col_sel2 = st.columns([2, 1])
    with col_sel1:
        site_choice = st.selectbox(
            "Load Sample Preset:",
            options=["custom"] + list(DEMO_SITES.keys()),
            format_func=lambda k: "Custom Raw HTML/CSS Snippet" if k == "custom" else DEMO_SITES[k]["title"]
        )
        
    initial_code = ""
    if site_choice != "custom":
        initial_code = DEMO_SITES[site_choice]["html"]
        st.caption(DEMO_SITES[site_choice]["description"])
    else:
        initial_code = """<div style="background-color: #ffffff; padding: 20px; font-family: sans-serif;">
  <h2 style="color: #94a3b8;">Low Contrast Heading Fail</h2>
  <p style="color: #cbd5e1; font-size: 14px;">This paragraph text is extremely hard to read.</p>
  <button style="background-color: #93c5fd; color: #ffffff; outline: none; border: none; padding: 10px;">Submit Action</button>
  <img src="avatar.jpg" />
</div>"""

    code_input = st.text_area(
        "HTML / CSS Code Editor:",
        value=initial_code,
        height=320,
        help="Paste your HTML layout code here."
    )
    
    return code_input
