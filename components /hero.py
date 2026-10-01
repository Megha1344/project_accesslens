"""
Hero Section Component for AccessLens
Modern developer-focused landing section with hero copy, feature highlights, and interactive preview switcher.
"""
import streamlit as st
from core.vision_filters import get_impairment_descriptions

def render_hero_section(on_inspect_click_callback=None):
    """Renders modern developer tool hero section with CSS styling."""
    st.markdown("""
        <style>
            .hero-container {
                background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
                border: 1px solid #312e81;
                border-radius: 16px;
                padding: 40px 32px;
                color: #ffffff;
                margin-bottom: 32px;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            }
            .hero-badge {
                display: inline-block;
                background: rgba(99, 102, 241, 0.15);
                color: #818cf8;
                border: 1px solid #4f46e5;
                font-size: 13px;
                font-weight: 600;
                padding: 6px 14px;
                border-radius: 20px;
                letter-spacing: 0.5px;
                margin-bottom: 16px;
            }
            .hero-title {
                font-size: 42px;
                font-weight: 800;
                line-height: 1.15;
                background: linear-gradient(90deg, #ffffff 0%, #c7d2fe 50%, #818cf8 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 16px;
            }
            .hero-subtitle {
                font-size: 18px;
                color: #94a3b8;
                max-width: 760px;
                line-height: 1.6;
                margin-bottom: 28px;
            }
            .feature-card {
                background: rgba(30, 41, 59, 0.7);
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 20px;
                transition: transform 0.2s ease;
            }
            .feature-card:hover {
                border-color: #6366f1;
            }
            .feature-icon {
                font-size: 28px;
                margin-bottom: 10px;
            }
            .feature-title {
                font-size: 16px;
                font-weight: 700;
                color: #f8fafc;
                margin-bottom: 6px;
            }
            .feature-desc {
                font-size: 13px;
                color: #94a3b8;
                line-height: 1.5;
            }
        </style>
        
        <div class="hero-container">
            <div class="hero-badge">⚡ ACCESSLENS PREMIUM DEVELOPER SUITE</div>
            <h1 class="hero-title">Don't just audit accessibility.<br/>Experience it.</h1>
            <p class="hero-subtitle">
                Automated audits report numbers and rules—AccessLens shows you what your website actually feels like to users with Protanopia, Low Acuity, Cataracts, or keyboard motor limitations. Understand problems visually, fix them instantly, and verify WCAG compliance in real time.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Feature Highlights 4-column Grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">👁️</div>
                <div class="feature-title">Sensory Vision Engine</div>
                <div class="feature-desc">Simulate Protanopia, Deuteranopia, Tritanopia, Low Acuity, Cataracts & Glaucoma using real SVG matrices.</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">⌨️</div>
                <div class="feature-title">Keyboard Journey Tracer</div>
                <div class="feature-desc">Visualize DOM tab sequences, detect outline:none focus ring failures and focus traps interactively.</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🎨</div>
                <div class="feature-title">Auto Contrast Fixer</div>
                <div class="feature-desc">WCAG 2.1 relative luminance math engine generating 1-click hue-preserving color fixes for AA/AAA.</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🛠️</div>
                <div class="feature-title">Inspection Sandbox</div>
                <div class="feature-desc">Paste raw HTML/CSS snippets or enter live web URLs to get instant DOM diagnostics and downloadable CSS fixes.</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br/>", unsafe_allow_html=True)
