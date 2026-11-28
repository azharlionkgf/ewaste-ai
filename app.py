"""
E-Waste AI — Streamlit Application Entry Point
===============================================
Combined Industrial Intelligence & Research Platform

Run with: streamlit run app.py
Backend:  uvicorn backend.main:app --port 8000 --reload
"""

import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from pathlib import Path

# ── Database bootstrap (must run before any page import) ───────────────
# On Streamlit Cloud the SQLite file is ephemeral; create tables on every
# cold start. `create_all` is idempotent — safe to call if tables exist.
def _bootstrap_db():
    try:
        db_path = Path(__file__).parent / "database"
        db_path.mkdir(parents=True, exist_ok=True)
        from backend.database import init_db
        init_db()
    except Exception as _e:
        import logging
        logging.getLogger(__name__).warning("DB bootstrap warning: %s", _e)

_bootstrap_db()

# ── Page Configuration ─────────────────────────────────────────────────
st.set_page_config(
    page_title="E-Waste AI Platform",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/azharlionkgf/ewaste-ai",
        "Report a bug": "https://github.com/azharlionkgf/ewaste-ai/issues",
        "About": "E-Waste AI — Combined Industrial Intelligence & Research Platform v2.0.0",
    },
)

# ── Theme Injection ────────────────────────────────────────────────────
# Applied before anything else renders
from frontend.theme import inject_theme
inject_theme()

# ── Navigation ─────────────────────────────────────────────────────────
from frontend.components.sidebar import render_sidebar
page = render_sidebar()

# ── Page Router ────────────────────────────────────────────────────────
if page == "dashboard":
    from frontend.pages.dashboard import render_dashboard
    render_dashboard()

elif page == "dataset_intelligence":
    from frontend.pages.dataset_intelligence import render
    render()

elif page == "dataset_management":
    from frontend.pages.dataset_management import render
    render()

elif page == "data_cleaning":
    from frontend.pages.data_cleaning import render_data_cleaning
    render_data_cleaning()

elif page == "preprocessing":
    from frontend.pages.preprocessing import render_preprocessing
    render_preprocessing()

elif page == "model_training":
    from frontend.pages.model_training import render
    render()

elif page == "model_evaluation":
    from frontend.pages.model_evaluation import render_model_evaluation
    render_model_evaluation()

elif page == "image_analysis":
    from frontend.pages.image_analysis import render
    render()

elif page == "video_analysis":
    from frontend.pages.video_analysis import render_video_analysis
    render_video_analysis()

elif page == "industrial_inventory":
    from frontend.pages.industrial_inventory import render_industrial_inventory
    render_industrial_inventory()

elif page == "erp_admin":
    from frontend.pages.erp_admin import render_erp_admin
    render_erp_admin()

elif page == "recovery_intelligence":
    from frontend.pages.recovery_intelligence import render
    render()

elif page == "economic_analysis":
    from frontend.pages.economic_analysis import render_economic_analysis
    render_economic_analysis()

elif page == "environmental_impact":
    from frontend.pages.environmental_impact import render_environmental_impact
    render_environmental_impact()

elif page == "research_experiments":
    from frontend.pages.research_experiments import render_research_experiments
    render_research_experiments()

elif page == "report_generator":
    from frontend.pages.report_generator import render_report_generator
    render_report_generator()

elif page == "settings":
    from frontend.pages.settings import render_settings
    render_settings()

elif page == "ai_intelligence":
    from frontend.pages.ai_intelligence import render_ai_intelligence
    render_ai_intelligence()

else:
    st.error(f"Page '{page}' not found.")
