"""
Live Website & Inspection Display Component
Renders website previews with SVG vision filters, side-by-side comparative view,
Before/After auto-fixed mode, and motor tremor simulation overlays.
"""

import streamlit as st
import streamlit.components.v1 as components

from core.vision_filters import (
    get_svg_filters_html,
    get_css_for_mode,
    get_impairment_descriptions,
)


def apply_auto_fixes_to_html(html_code: str) -> str:
    """Injects high-contrast CSS overrides and visible focus ring fixes into HTML."""

    fix_stylesheet = """
    <style id="accesslens-auto-fixes">
        /* AccessLens Smart Contrast & Focus Fixes Override */

        body, p, span, div, td, th {
            color: #0f172a !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #1e293b !important;
        }

        .hdr-main {
            color: #0f172a !important;
        }

        .title-sub, .metric-label {
            color: #475569 !important;
        }

        .metric-val {
            color: #0284c7 !important;
        }

        .btn-submit {
            background-color: #0284c7 !important;
            color: #ffffff !important;
        }

        /* 1-Click Focus Ring Fix */
        *:focus-visible,
        button:focus-visible,
        input:focus-visible,
        a:focus-visible,
        div:focus-visible {
            outline: 3px solid #2563eb !important;
            outline-offset: 3px !important;
        }

        /* Colorblind Status Dot Fix */
        .status-dot-green::after {
            content: " ✓ Active";
            font-size: 12px;
            color: #166534;
            font-weight: bold;
            margin-left: 14px;
        }

        .status-dot-red::after {
            content: " ❌ Offline";
            font-size: 12px;
            color: #991b1b;
            font-weight: bold;
            margin-left: 14px;
        }
    </style>
    """

    if "</head>" in html_code.lower():
        return html_code.replace(
            "</head>",
            f"{fix_stylesheet}\n</head>",
        )
    else:
        return fix_stylesheet + html_code


def render_simulated_iframe(
    html_code: str,
    vision_mode: str,
    height: int = 560,
    enable_tremor: bool = False,
) -> str:
    """Creates the HTML used to simulate different visual/motor experiences."""

    svg_defs = get_svg_filters_html()
    filter_css = get_css_for_mode(vision_mode)

    tremor_css = ""

    if enable_tremor:
        tremor_css = """
        @keyframes motorTremor {
            0% {
                transform: translate(0px, 0px) rotate(0deg);
            }

            20% {
                transform: translate(-3px, 2px) rotate(0.4deg);
            }

            40% {
                transform: translate(3px, -2px) rotate(-0.4deg);
            }

            60% {
                transform: translate(-2px, -3px) rotate(0.2deg);
            }

            80% {
                transform: translate(2px, 3px) rotate(-0.2deg);
            }

            100% {
                transform: translate(0px, 0px) rotate(0deg);
            }
        }

        body * {
            animation: motorTremor 0.16s infinite ease-in-out !important;
        }
        """

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">

        <style>
            {svg_defs}

            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                background: #ffffff;
            }}

            .simulation-container {{
                {filter_css}
                width: 100%;
                min-height: 100vh;
                box-sizing: border-box;
            }}

            {tremor_css}
        </style>
    </head>

    <body>
        {svg_defs}

        <div class="simulation-container">
            {html_code}
        </div>
    </body>
    </html>
    """

    return full_html


def render_live_inspector(
    html_content: str,
    frame_notice: str = "",
    key_prefix: str = "live",
):
    """
    Renders the AccessLens sensory vision and impairment inspector.

    key_prefix gives every instance of this component unique Streamlit widget keys.
    This is necessary because the inspector can be rendered multiple times
    within the same Streamlit application.
    """

    st.markdown("### 👁️ Sensory Vision & Impairment Inspector")

    if frame_notice and "restrictions" in frame_notice.lower():
        st.warning(
            f"🔒 **Browser Framing Security Notice**: "
            f"{frame_notice} "
            f"AccessLens DOM proxy rendering active to bypass iframe blocking."
        )

    descriptions = get_impairment_descriptions()

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 1, 1])

    # ---------------------------------------------------------
    # Vision / Impairment Selection
    # ---------------------------------------------------------
    with col_ctrl1:
        vision_mode = st.selectbox(
            "Select Impairment Experience:",
            options=list(descriptions.keys()),
            format_func=lambda k: (
                f"{descriptions[k]['name']} — "
                f"{descriptions[k]['tagline']}"
            ),
            index=1,
            key=f"{key_prefix}_vision_mode",
        )

    # ---------------------------------------------------------
    # Display Mode
    # ---------------------------------------------------------
    with col_ctrl2:
        view_mode = st.radio(
            "Display Mode:",
            options=[
                "Impairment Only",
                "Side-by-Side Comparison",
                "Before/After Smart Fix",
            ],
            index=1,
            key=f"{key_prefix}_view_mode",
        )

    # ---------------------------------------------------------
    # Motor Tremor
    # ---------------------------------------------------------
    with col_ctrl3:
        enable_tremor = st.checkbox(
            "Motor Tremor Simulation",
            value=False,
            key=f"{key_prefix}_tremor",
        )

    # ---------------------------------------------------------
    # Information about selected impairment
    # ---------------------------------------------------------
    info = descriptions.get(
        vision_mode,
        descriptions["normal"],
    )

    st.info(
        f"**{info['name']}**: {info['details']}"
    )

    # =========================================================
    # BEFORE / AFTER SMART FIX
    # =========================================================
    if view_mode == "Before/After Smart Fix":

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(
                "##### ❌ Original Website "
                "(With Accessibility Violations)"
            )

            orig_frame = render_simulated_iframe(
                html_content,
                vision_mode,
                enable_tremor=enable_tremor,
            )

            components.html(
                orig_frame,
                height=520,
                scrolling=True,
            )

        with col_right:
            st.markdown(
                "##### ✅ AccessLens Auto-Fixed "
                "(Compliant Contrast & Indicators)"
            )

            fixed_html = apply_auto_fixes_to_html(
                html_content
            )

            fixed_frame = render_simulated_iframe(
                fixed_html,
                vision_mode,
                enable_tremor=enable_tremor,
            )

            components.html(
                fixed_frame,
                height=520,
                scrolling=True,
            )

    # =========================================================
    # SIDE-BY-SIDE COMPARISON
    # =========================================================
    elif (
        view_mode == "Side-by-Side Comparison"
        and vision_mode != "normal"
    ):

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(
                "##### 🟢 Normal Vision Baseline"
            )

            normal_frame = render_simulated_iframe(
                html_content,
                "normal",
                enable_tremor=False,
            )

            components.html(
                normal_frame,
                height=520,
                scrolling=True,
            )

        with col_right:
            st.markdown(
                f"##### 👁️ Simulated Experience "
                f"({info['name']})"
            )

            sim_frame = render_simulated_iframe(
                html_content,
                vision_mode,
                enable_tremor=enable_tremor,
            )

            components.html(
                sim_frame,
                height=520,
                scrolling=True,
            )

    # =========================================================
    # IMPAIRMENT ONLY / NORMAL VIEW
    # =========================================================
    else:

        st.markdown(
            f"##### 👁️ Live Website Display "
            f"({info['name']})"
        )

        sim_frame = render_simulated_iframe(
            html_content,
            vision_mode,
            enable_tremor=enable_tremor,
        )

        components.html(
            sim_frame,
            height=550,
            scrolling=True,
        )
