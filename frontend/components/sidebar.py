"""
E-Waste AI — Interactive Sidebar Navigation
=============================================
Renders the Obsidian & Champagne Gold command rail with live search filter,
active primary pill state, and real database/model telemetry indicator.
"""

from __future__ import annotations

import streamlit as st


NAV_ITEMS = [
    # (key, icon, label, group)
    ("dashboard",            "📊", "Dashboard",             "OVERVIEW"),
    ("dataset_intelligence", "🧠", "Dataset Intelligence",  "DATASET PIPELINE"),
    ("dataset_management",   "📁", "Dataset Management",    "ACADEMIC WORKFLOW"),
    ("data_cleaning",        "🧹", "Data Cleaning",         "ACADEMIC WORKFLOW"),
    ("preprocessing",        "⚙️", "Preprocessing",         "ACADEMIC WORKFLOW"),
    ("model_training",       "🤖", "Model Training",        "ACADEMIC WORKFLOW"),
    ("model_evaluation",     "📈", "Model Evaluation",      "ACADEMIC WORKFLOW"),
    ("image_analysis",       "🔍", "Image Analysis",        "AI ANALYSIS"),
    ("video_analysis",       "🎥", "Video Analysis",        "AI ANALYSIS"),
    ("industrial_inventory", "🏭", "Industrial Inventory",  "INDUSTRIAL"),
    ("erp_admin",            "🏛️", "Company ERP & Admin",   "INDUSTRIAL"),
    ("recovery_intelligence","♻️", "Recovery Intelligence", "INDUSTRIAL"),
    ("economic_analysis",    "💰", "Economic Analysis",     "INDUSTRIAL"),
    ("environmental_impact", "🌍", "Environmental Impact",  "INDUSTRIAL"),
    ("research_experiments", "🔬", "Research Experiments",  "RESEARCH"),
    ("report_generator",     "📄", "Report Generator",      "REPORTS"),
    ("ai_intelligence",      "🧠", "AI Intelligence",       "PHASE 6 — AI"),
    ("settings",             "⚙️", "Settings",              "SYSTEM"),
]


def _get_live_pulse() -> tuple[int, int]:
    """Read live DB batch count & model count safely for sidebar pulse."""
    try:
        from backend.database import SessionLocal
        from backend.models.all_models import WasteBatch, MLModel
        db = SessionLocal()
        try:
            batches = db.query(WasteBatch).count()
            models = db.query(MLModel).count()
            return batches, models
        finally:
            db.close()
    except Exception:
        return 0, 0


def render_sidebar() -> str:
    """Render the interactive sidebar navigation. Returns selected page key."""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    with st.sidebar:
        # ── Bespoke Crest & Brand Header ─────────────────────────────
        st.markdown("""
        <div style="text-align:center; padding: 0.75rem 0 0.85rem 0;">
          <div style="display:inline-flex;align-items:center;justify-content:center;
                      width:48px;height:48px;border-radius:14px;
                      background:linear-gradient(135deg,rgba(201,168,76,0.22),rgba(201,168,76,0.05));
                      border:1px solid rgba(201,168,76,0.45);
                      box-shadow:0 6px 20px rgba(201,168,76,0.18);margin-bottom:0.45rem;">
            <span style="font-size:1.55rem;">♻️</span>
          </div>
          <div style="font-family:'Space Grotesk',sans-serif; font-size:1.18rem;
                      font-weight:700; letter-spacing:0.06em;
                      background:linear-gradient(95deg,#F4F4F6,#F2D67B);
                      -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            E-WASTE AI
          </div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:0.64rem;
                      color:#9CA3AF; letter-spacing:0.12em; text-transform:uppercase; margin-top:2px;">
            Industrial · Research · Ops
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Interactive Quick Workspace Filter ───────────────────────
        query = st.text_input(
            "Filter workspaces",
            value="",
            placeholder="🔎 Filter 17 workspaces...",
            label_visibility="collapsed",
            key="sidebar_nav_filter",
        ).strip().lower()

        filtered = [
            item for item in NAV_ITEMS
            if not query or query in item[2].lower() or query in item[3].lower()
        ]

        if not filtered:
            st.caption("No workspace matches your filter.")
        else:
            current_group = None
            for key, icon, label, group in filtered:
                if group != current_group:
                    current_group = group
                    st.markdown(
                        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;'
                        f'font-weight:600;color:#6B7280;text-transform:uppercase;'
                        f'letter-spacing:0.12em;padding:0.65rem 0.35rem 0.2rem 0.35rem;">{group}</div>',
                        unsafe_allow_html=True,
                    )

                is_active = st.session_state.current_page == key
                if st.button(
                    f"{icon}  {label}",
                    key=f"nav_{key}",
                    type="primary" if is_active else "secondary",
                    use_container_width=True,
                ):
                    st.session_state.current_page = key
                    st.rerun()

        # ── Live Telemetry Card + Footer ─────────────────────────────
        batches_cnt, models_cnt = _get_live_pulse()
        st.markdown(f"""
        <div style="margin-top:0.9rem;padding:0.7rem 0.85rem;border-radius:10px;
                    background:rgba(20,23,32,0.85);border:1px solid rgba(255,255,255,0.07);">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#34D399;
                         display:inline-flex;align-items:center;gap:6px;">
              <span style="width:6px;height:6px;border-radius:50%;background:#10B981;"></span>SYSTEM LIVE
            </span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#C9A84C;">CPU</span>
          </div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#9CA3AF;display:flex;justify-content:space-between;">
            <span>Batches: <strong style="color:#F4F4F6">{batches_cnt}</strong></span>
            <span>DB Models: <strong style="color:#F4F4F6">{models_cnt}</strong></span>
          </div>
        </div>
        <div style="text-align:center;color:#6B7280;font-size:0.68rem;padding:0.75rem 0 0.25rem 0;">
          E-Waste AI v2.0 · <a href="https://github.com/azharlionkgf/ewaste-ai"
             style="color:#C9A84C;text-decoration:none;">GitHub</a>
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.current_page
