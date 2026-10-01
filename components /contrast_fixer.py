"""
Auto-Suggested Contrast Ratio Fixer Component
Provides interactive color pickers, WCAG 2.1 relative luminance math solver,
and 1-click hue-preserving color contrast repair engine.
"""
import streamlit as st
from core.wcag_math import (
    calculate_contrast_ratio,
    evaluate_wcag_compliance,
    auto_fix_contrast,
    calculate_relative_luminance,
    parse_color_to_rgb,
    hex_to_rgb,
    rgb_to_hex
)

def render_contrast_fixer_tab():
    """Renders the standalone WCAG Contrast Engine & Auto-Fixer tool."""
    st.markdown("## 🎨 Auto-Suggested Contrast Ratio Engine")
    st.markdown(
        "Enter or pick foreground and background colors to evaluate exact WCAG 2.1 relative luminance, check AA/AAA compliance, and automatically generate optimal contrast color fixes while preserving hue."
    )
    
    col_input1, col_input2, col_input3 = st.columns(3)
    
    with col_input1:
        fg_color = st.color_picker("Text / Foreground Color:", value="#94A3B8")
        fg_hex = st.text_input("Foreground Hex:", value=fg_color)
        
    with col_input2:
        bg_color = st.color_picker("Background Color:", value="#FFFFFF")
        bg_hex = st.text_input("Background Hex:", value=bg_color)
        
    with col_input3:
        target_standard = st.radio(
            "WCAG Conformance Target:",
            options=["WCAG AA (4.5:1)", "WCAG AAA (7.0:1)", "Large Text / UI (3.0:1)"],
            index=0
        )
        
    target_ratio = 4.5
    is_large = False
    if "7.0" in target_standard:
        target_ratio = 7.0
    elif "3.0" in target_standard:
        target_ratio = 3.0
        is_large = True
        
    # Calculate Ratios
    ratio = calculate_contrast_ratio(fg_hex, bg_hex)
    compliance = evaluate_wcag_compliance(ratio, is_large_text=is_large)
    
    fg_rgb = parse_color_to_rgb(fg_hex)
    bg_rgb = parse_color_to_rgb(bg_hex)
    l_fg = round(calculate_relative_luminance(fg_rgb), 4)
    l_bg = round(calculate_relative_luminance(bg_rgb), 4)
    
    # Display Metric Cards
    st.markdown("<br/>", unsafe_allow_html=True)
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.metric("Current Contrast Ratio", f"{ratio} : 1")
    with m_col2:
        st.metric("Status", compliance["status"])
    with m_col3:
        st.metric("FG Luminance (L1)", f"{l_fg}")
    with m_col4:
        st.metric("BG Luminance (L2)", f"{l_bg}")

    # Live Color Preview Box
    st.markdown("#### 🔍 Live Visual Text Preview")
    st.markdown(
        f"""
        <div style="background-color: {bg_hex}; color: {fg_hex}; padding: 24px; border-radius: 10px; border: 2px solid #334155; text-align: center; margin-bottom: 24px;">
            <span style="font-size: 22px; font-weight: 700;">Sample Heading Text (22px)</span><br/>
            <span style="font-size: 15px;">The quick brown fox jumps over the lazy dog. Standard body text sample.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Auto-Fix Algorithm Section
    st.markdown("---")
    st.markdown("### ⚡ Auto-Suggested Color Fix Generator")
    
    fix_target = st.radio("Fix Target Strategy:", options=["Adjust Foreground Text Color", "Adjust Background Color"], index=0)
    target_param = "fg" if "Foreground" in fix_target else "bg"
    
    fixed_result = auto_fix_contrast(fg_hex, bg_hex, target_ratio=target_ratio, fix_target=target_param)
    
    if fixed_result["changed"]:
        st.warning(f"⚠️ Current ratio of {ratio}:1 fails target requirement of {target_ratio}:1.")
        
        fix_col1, fix_col2 = st.columns(2)
        with fix_col1:
            st.markdown("##### ❌ Before (Failing)")
            st.markdown(
                f"""
                <div style="background-color: {bg_hex}; color: {fg_hex}; padding: 18px; border-radius: 8px; border: 1px solid #ef4444; font-weight: 600;">
                    {fg_hex} on {bg_hex} — Ratio: {ratio}:1
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with fix_col2:
            st.markdown("##### ✅ Auto-Suggested Fix (Passing)")
            st.markdown(
                f"""
                <div style="background-color: {fixed_result['fixed_bg']}; color: {fixed_result['fixed_fg']}; padding: 18px; border-radius: 8px; border: 2px solid #10b981; font-weight: 600;">
                    {fixed_result['fixed_fg']} on {fixed_result['fixed_bg']} — Ratio: {fixed_result['fixed_ratio']}:1
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("##### 📋 Recommended CSS Fix Snippet")
        st.code(
            f"""/* WCAG {target_standard} Compliant Color Pair */
color: {fixed_result['fixed_fg']};
background-color: {fixed_result['fixed_bg']};""",
            language="css"
        )
    else:
        st.success(f"🎉 Excellent! This color pair already passes WCAG compliance ({ratio}:1 >= {target_ratio}:1 target).")
