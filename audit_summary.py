"""
Accessibility Audit Inspector & Summary Panel Component
Provides detailed WCAG violation breakdown, 4-tier category scoring, code snippets,
bottom status bar metrics, and downloadable JSON/CSS fix reports.
"""
import json
import streamlit as st
from core.dom_parser import audit_html_accessibility

def render_audit_summary_panel(html_content: str):
    """Renders the detailed accessibility inspector panel and category score gauges."""
    audit_results = audit_html_accessibility(html_content)
    
    overall_score = audit_results["wcag_score"]
    visual_score = audit_results["visual_score"]
    motor_score = audit_results["motor_score"]
    semantic_score = audit_results["semantic_score"]
    issues = audit_results["issues"]
    
    st.markdown("### 📊 AccessLens Scorecard & Category Breakdown")
    
    # 4-Column Category Metric Bar
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.metric("Overall AccessLens Score", f"{overall_score} / 100", delta=f"{overall_score - 100} vs Pass Target")
    with col_s2:
        st.metric("Visual & Contrast Score", f"{visual_score} / 100")
    with col_s3:
        st.metric("Motor & Keyboard Score", f"{motor_score} / 100")
    with col_s4:
        st.metric("Semantics & Structure", f"{semantic_score} / 100")

    st.markdown("---")
    
    # Category & Severity Filter
    st.markdown("#### 🔎 Filter Detected Violations")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        cat_filter = st.multiselect(
            "Category Filter:",
            options=["Visual", "Motor / Keyboard", "Semantic"],
            default=["Visual", "Motor / Keyboard", "Semantic"]
        )
    with col_f2:
        sev_filter = st.multiselect(
            "Severity Filter:",
            options=["Critical", "Serious", "Moderate", "Minor"],
            default=["Critical", "Serious", "Moderate", "Minor"]
        )
        
    filtered_issues = [
        i for i in issues 
        if i.get("category", "Visual") in cat_filter and i["severity"] in sev_filter
    ]
    
    if not filtered_issues:
        st.success("🎉 No issues matching the selected filters!")
    else:
        for idx, issue in enumerate(filtered_issues, 1):
            severity = issue["severity"]
            badge_color = "#ef4444" if severity == "Critical" else "#f59e0b" if severity == "Serious" else "#3b82f6"
            category_tag = issue.get("category", "General")
            
            with st.expander(f"#{idx} [{severity}] [{category_tag}] {issue['wcag']} — Element: {issue['element']}"):
                st.markdown(
                    f"""
                    <div style="background: #1e293b; padding: 16px; border-radius: 8px; border-left: 4px solid {badge_color};">
                        <strong style="color: #f8fafc; font-size: 15px;">{issue['description']}</strong>
                        <br/><br/>
                        <span style="color: #94a3b8; font-size: 13px;">Target Element Snippet:</span>
                        <pre style="background: #0f172a; color: #38bdf8; padding: 10px; border-radius: 6px; font-size: 12px; margin-top: 4px;">{issue['html_snippet']}</pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown("##### 🛠️ AccessLens Smart Fix Recommendation:")
                st.code(issue["fix_recommendation"], language="html" if "<" in issue["fix_recommendation"] else "css")

    # Export Report & Fixed CSS Section
    st.markdown("---")
    st.markdown("### 📥 Export AccessLens Report & Fixes")
    
    col_exp1, col_exp2 = st.columns(2)
    
    css_fixes = []
    for issue in issues:
        if "fix_recommendation" in issue and "/*" in issue["fix_recommendation"]:
            css_fixes.append(issue["fix_recommendation"])
    combined_css = "\n\n".join(css_fixes) if css_fixes else "/* All WCAG checks passed! No CSS fixes required. */"
    
    json_report = json.dumps(audit_results, indent=2)
    
    with col_exp1:
        st.download_button(
            label="📄 Download AccessLens Audit Report (JSON)",
            data=json_report,
            file_name="accesslens_audit_report.json",
            mime="application/json",
            use_container_width=True
        )
        
    with col_exp2:
        st.download_button(
            label="🎨 Download Auto-Generated CSS Fixes (.css)",
            data=combined_css,
            file_name="accesslens_fixes.css",
            mime="text/css",
            use_container_width=True
        )
