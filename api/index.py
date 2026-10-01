"""
AccessLens Vercel Serverless Gateway
FastAPI / WSGI serverless application entry point for Vercel deployment.
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sys
import os

# Add parent directory to path to import core algorithms & samples
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wcag_math import calculate_contrast_ratio, evaluate_wcag_compliance, auto_fix_contrast
from core.vision_filters import get_svg_filters_html, get_css_for_mode, get_impairment_descriptions
from core.dom_parser import audit_html_accessibility
from samples.demo_sites import DEMO_SITES

app = FastAPI(title="AccessLens Vercel API & Web App")

@app.get("/", response_class=HTMLResponse)
def read_root():
    svg_defs = get_svg_filters_html()
    demo_html = DEMO_SITES["shoptech_audit_demo"]["html"]
    audit = audit_html_accessibility(demo_html)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AccessLens — Developer Accessibility Suite</title>
        <style>
            body {{
                font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #0b0f19;
                color: #f1f5f9;
                margin: 0;
                padding: 32px;
            }}
            .header {{
                background: #111827;
                border: 1px solid #1f2937;
                padding: 24px 32px;
                border-radius: 12px;
                margin-bottom: 32px;
            }}
            .logo {{ font-size: 28px; font-weight: 800; color: #ffffff; }}
            .logo span {{ color: #6366f1; }}
            .tagline {{ color: #94a3b8; font-size: 14px; margin-top: 4px; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
            .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px; }}
            .score-val {{ font-size: 36px; font-weight: 800; color: #38bdf8; }}
            .issue-box {{ background: #0f172a; padding: 12px; border-radius: 6px; margin-bottom: 12px; border-left: 4px solid #ef4444; }}
        </style>
        {svg_defs}
    </head>
    <body>
        <div class="header">
            <div class="logo">👁️ Access<span>Lens</span></div>
            <div class="tagline">Don't just audit it — experience it! (Vercel Serverless Deployment)</div>
        </div>

        <div class="grid">
            <div class="card">
                <h2>📊 WCAG Audit Scorecard</h2>
                <div class="score-val">{audit['wcag_score']} / 100</div>
                <p>Total Issues Flagged: {audit['total_issues']}</p>
                <hr style="border-color: #334155;" />
                <h3>Top Detected Violations</h3>
                {''.join([f'<div class="issue-box"><strong>[{i["severity"]}] {i["wcag"]}</strong><br/><small>{i["description"]}</small></div>' for i in audit['issues'][:4]])}
            </div>

            <div class="card">
                <h2>👁️ Impairment Simulator (Protanopia Filter)</h2>
                <div style="filter: url(#filter-protanopia); background: white; border-radius: 8px; overflow: hidden; padding: 10px;">
                    {demo_html}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "AccessLens Vercel Serverless Engine"}
