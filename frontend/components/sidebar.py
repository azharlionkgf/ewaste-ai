"""
E-Waste AI — Sidebar Navigation
=================================
Renders the premium sidebar with navigation menu.
Returns the selected page key.
"""

import streamlit as st


NAV_ITEMS = [
    # (key, icon, label, group)
    ("dashboard",           "📊", "Dashboard",             "OVERVIEW"),
    ("dataset_intelligence",  "🧠", "Dataset Intelligence",    "DATASET PIPELINE"),
    ("dataset_management",  "📁", "Dataset Management",    "ACADEMIC WORKFLOW"),
    ("data_cleaning",       "🧹", "Data Cleaning",         "ACADEMIC WORKFLOW"),
    ("preprocessing",       "⚙️",  "Preprocessing",         "ACADEMIC WORKFLOW"),
    ("model_training",      "🤖", "Model Training",        "ACADEMIC WORKFLOW"),
    ("model_evaluation",    "📈", "Model Evaluation",      "ACADEMIC WORKFLOW"),
    ("image_analysis",      "🔍", "Image Analysis",        "AI ANALYSIS"),
    ("video_analysis",      "🎥", "Video Analysis",        "AI ANALYSIS"),
    ("industrial_inventory","🏭", "Industrial Inventory",  "INDUSTRIAL"),
    ("recovery_intelligence","♻️", "Recovery Intelligence", "INDUSTRIAL"),
    ("economic_analysis",   "💰", "Economic Analysis",     "INDUSTRIAL"),
    ("environmental_impact","🌍", "Environmental Impact",  "INDUSTRIAL"),
    ("research_experiments","🔬", "Research Experiments",  "RESEARCH"),
    ("report_generator",    "📄", "Report Generator",      "REPORTS"),
    ("ai_intelligence",     "🧠", "AI Intelligence",       "PHASE 6 — AI"),
    ("settings",            "⚙️",  "Settings",              "SYSTEM"),
]


def render_sidebar() -> str:
    """Render the sidebar navigation. Returns the selected page key."""

    with st.sidebar:
        # ── Logo / Title ────────────────────────────────────────────
        st.markdown("""
        <div style="text-align:center; padding: 1rem 0 1.5rem 0;">
            <div style="font-size:2.5rem; margin-bottom:0.25rem;">♻️</div>
            <div style="font-family:'Poppins',sans-serif; font-size:1.2rem;
                        font-weight:700; color:#C9A84C; letter-spacing:0.05em;">
                E-WASTE AI
            </div>
            <div style="font-size:0.7rem; color:#666; letter-spacing:0.1em;
                        text-transform:uppercase; margin-top:2px;">
                Industrial · Academic · Research
            </div>
        </div>
        <hr style="border-color:#2D2D2D; margin: 0 0 1rem 0;">
        """, unsafe_allow_html=True)

        # ── Navigation ──────────────────────────────────────────────
        if "current_page" not in st.session_state:
            st.session_state.current_page = "dashboard"

        current_group = None

        for key, icon, label, group in NAV_ITEMS:
            # Group header
            if group != current_group:
                current_group = group
                st.markdown(
                    f'<div style="font-size:0.65rem; font-weight:600; color:#666; '
                    f'text-transform:uppercase; letter-spacing:0.1em; '
                    f'padding: 0.75rem 0.5rem 0.25rem 0.5rem;">{group}</div>',
                    unsafe_allow_html=True
                )

            # Nav item
            is_active = st.session_state.current_page == key
            btn_style = (
                "background:rgba(201,168,76,0.15); color:#C9A84C; "
                "border-left:3px solid #C9A84C;"
                if is_active else
                "background:transparent; color:#9A9A9A; border-left:3px solid transparent;"
            )

            if st.button(
                f"{icon}  {label}",
                key=f"nav_{key}",
                use_container_width=True,
                help=label,
            ):
                st.session_state.current_page = key
                st.rerun()

        # ── Footer ──────────────────────────────────────────────────
        st.markdown("""
        <hr style="border-color:#2D2D2D; margin: 1rem 0 0.75rem 0;">
        <div style="text-align:center; color:#444; font-size:0.7rem; padding-bottom:0.5rem;">
            E-Waste AI v2.0.0<br>
            <a href="https://github.com/azharlionkgf/ewaste-ai"
               style="color:#666; text-decoration:none;">
               github.com/azharlionkgf
            </a>
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.current_page
