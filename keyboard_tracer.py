"""
Keyboard Navigation Journey Center & Focus Auditor Component
Visualizes ordered keyboard tab flow, detects focus ring failures, and simulates tab navigation.
"""
import streamlit as st
from core.keyboard_traps import analyze_keyboard_navigation

def render_keyboard_tracer(html_content: str):
    """Renders the interactive keyboard navigation journey tracer."""
    st.markdown("## ⌨️ Keyboard Navigation Journey Center")
    st.markdown(
        "Users with motor impairments or visual conditions rely entirely on keyboard `Tab` navigation. AccessLens maps your website's exact focus order, audits visible focus rings (`WCAG 2.4.7`), and flags potential keyboard traps (`WCAG 2.1.2`)."
    )
    
    result = analyze_keyboard_navigation(html_content)
    tab_sequence = result["tab_sequence"]
    warnings = result["warnings"]
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.metric("Total Focusable Elements", result["total_focusable_elements"])
    with col_k2:
        st.metric("Positive Tabindex Warnings", result["positive_tabindex_count"])

    # Warnings Display
    if warnings:
        st.markdown("### ⚠️ Keyboard Accessibility Flags")
        for warn in warnings:
            severity_color = "#ef4444" if warn["severity"] == "Critical" else "#f59e0b"
            st.markdown(
                f"""
                <div style="border-left: 4px solid {severity_color}; background: #1e293b; padding: 12px 16px; border-radius: 6px; margin-bottom: 12px;">
                    <span style="color: {severity_color}; font-weight: 700;">[{warn['severity']}] {warn['wcag']}</span><br/>
                    <strong style="color: #f8fafc;">Element:</strong> <code>{warn['element']}</code><br/>
                    <span style="color: #94a3b8; font-size: 14px;">{warn['description']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.success("✅ No critical keyboard navigation traps or positive tabindex issues detected in the DOM structure!")

    # Interactive Step-by-Step Focus Simulator
    st.markdown("---")
    st.markdown("### 🗺️ Visual Keyboard Tab Sequence Map")
    
    if not tab_sequence:
        st.warning("No natively focusable elements (buttons, links, inputs) detected in the provided HTML.")
        return

    # Render sequence flow diagram
    steps_html = []
    for item in tab_sequence:
        status_color = "#ef4444" if item["has_outline_none"] else "#3b82f6"
        badge = f'<span style="background: {status_color}; color: #fff; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{item["focus_indicator_status"]}</span>'
        steps_html.append(
            f"""
            <div style="display: inline-block; background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 12px; margin: 6px; min-width: 140px; vertical-align: top;">
                <div style="font-size: 12px; color: #64748b; font-weight: 700;">STEP #{item['step']}</div>
                <div style="font-size: 15px; color: #f8fafc; font-weight: 600; margin: 4px 0;">&lt;{item['tag']}&gt;</div>
                <div style="font-size: 13px; color: #94a3b8;">"{item['label']}"</div>
                <div style="margin-top: 6px;">{badge}</div>
            </div>
            """
        )
        
    st.markdown(
        f"""
        <div style="background: #1e293b; padding: 16px; border-radius: 12px; overflow-x: auto; white-space: nowrap; margin-bottom: 24px;">
            {' → '.join(steps_html)}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Detailed Focusable Element List Table
    st.markdown("#### 📋 Detailed Focusable Element Table")
    table_data = []
    for s in tab_sequence:
        table_data.append({
            "Step": s["step"],
            "Tag": s["tag"],
            "Label / Content": s["label"],
            "Tabindex": s["tabindex"],
            "Focus Indicator": s["focus_indicator_status"]
        })
    st.dataframe(table_data, use_container_width=True)
