"""
E-Waste AI — Industrial Intelligence Dashboard
================================================
Task 3 of Phase 5.
Real-time summary of batches, recovery, inventory, models and
environmental metrics — all from live database records.
Shows clear empty states when no data exists.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from datetime import datetime
from frontend.theme import apply_theme, page_header, section_header, status_badge, COLORS

# ── backend imports ────────────────────────────────────────────────────
try:
    from backend.database import SessionLocal
    from backend.models.all_models import (
        WasteBatch, RecoveryRecord, Inventory,
        TrainedModel, ModelEvaluation, AIPrediction,
        Device,
    )
    DB_OK = True
except Exception as e:
    DB_OK = False
    DB_ERR = str(e)


def _db():
    return SessionLocal() if DB_OK else None


def _safe_count(db, model):
    try:
        return db.query(model).count()
    except Exception:
        return 0


def _safe_sum(db, model, col):
    try:
        from sqlalchemy import func
        result = db.query(func.sum(col)).scalar()
        return result or 0.0
    except Exception:
        return 0.0


def render_dashboard():
    apply_theme()

    # ── Header ─────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style='background:linear-gradient(135deg,#141414,#1C1C1C);
        border:1px solid #2D2D2D;border-radius:12px;padding:2rem 2.5rem;
        margin-bottom:1.5rem;border-left:4px solid #C9A84C'>
        <div style='font-family:Poppins,sans-serif;font-size:0.75rem;
        color:#9A9A9A;text-transform:uppercase;letter-spacing:0.1em'>
        Industrial Intelligence Platform</div>
        <div style='font-family:Poppins,sans-serif;font-size:2rem;
        font-weight:700;color:#C9A84C;margin:0.3rem 0 0.2rem'>
        ♻️ E-Waste AI</div>
        <div style='color:#9A9A9A;font-size:0.9rem'>
        Combined Industrial Intelligence & Research Platform — 
        Last updated: {datetime.now().strftime('%d %b %Y, %H:%M')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not DB_OK:
        st.error(f"⚠️ Database unavailable: {DB_ERR}")
        st.info("The platform is running but cannot connect to the database. Check configuration.")
        return

    # ── Fetch data ─────────────────────────────────────────────────────
    db = _db()
    try:
        total_batches   = _safe_count(db, WasteBatch)
        total_devices   = _safe_count(db, Device)
        total_models    = _safe_count(db, TrainedModel)
        total_preds     = _safe_count(db, AIPrediction)
        total_evals     = _safe_count(db, ModelEvaluation)

        from sqlalchemy import func
        total_weight    = db.query(func.sum(WasteBatch.total_weight_kg)).scalar() or 0.0
        total_recovered = db.query(func.sum(RecoveryRecord.quantity_kg)).scalar() or 0.0
        total_inv_items = _safe_count(db, Inventory)

        # Status breakdowns
        status_counts = {}
        for status in ["incoming", "sorting", "dismantling", "processing", "completed", "rejected"]:
            status_counts[status] = db.query(WasteBatch).filter(
                WasteBatch.status == status
            ).count()

        # Recent batches (last 5)
        recent_batches = db.query(WasteBatch).order_by(
            WasteBatch.created_at.desc()
        ).limit(5).all()

        # Best model
        best_eval = None
        if total_evals > 0:
            from sqlalchemy import desc
            best_eval = db.query(ModelEvaluation).filter(
                ModelEvaluation.accuracy.isnot(None)
            ).order_by(desc(ModelEvaluation.accuracy)).first()
            if best_eval:
                best_model = db.query(TrainedModel).filter(
                    TrainedModel.id == best_eval.model_id
                ).first()
            else:
                best_model = None
        else:
            best_model = None

        # Recent predictions
        recent_preds = db.query(AIPrediction).order_by(
            AIPrediction.created_at.desc()
        ).limit(5).all()

        # Inventory top items
        top_inventory = db.query(Inventory).order_by(
            Inventory.quantity_kg.desc()
        ).limit(5).all()

    except Exception as ex:
        st.error(f"Dashboard data error: {ex}")
        db.close()
        return
    finally:
        db.close()

    # ══════════════════════════════════════════════════════════════════
    # ROW 1 — Key KPIs
    # ══════════════════════════════════════════════════════════════════
    section_header("Operations Overview")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Batches", total_batches,
              help="All registered e-waste batches")
    c2.metric("Total E-Waste", f"{total_weight:.1f} kg",
              help="Sum of all registered batch weights")
    c3.metric("Material Recovered", f"{total_recovered:.1f} kg",
              help="Total from all recovery records")
    c4.metric("Devices Registered", total_devices)
    c5.metric("Recovery Rate",
              f"{(total_recovered/total_weight*100 if total_weight else 0):.1f}%",
              help="Recovered ÷ Total weight")

    # ══════════════════════════════════════════════════════════════════
    # ROW 2 — Batch Pipeline + AI Models
    # ══════════════════════════════════════════════════════════════════
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        section_header("Batch Pipeline Status")
        STATUS_ICONS = {
            "incoming": "📥", "sorting": "🔄", "dismantling": "🔧",
            "processing": "⚙️", "completed": "✅", "rejected": "❌",
        }
        STATUS_COLORS = {
            "incoming": "#2980B9", "sorting": "#E67E22", "dismantling": "#E67E22",
            "processing": "#C9A84C", "completed": "#27AE60", "rejected": "#E74C3C",
        }
        if total_batches == 0:
            st.info("No batches registered yet. Go to **Industrial Operations** to register incoming e-waste.")
        else:
            for status, count in status_counts.items():
                if count > 0:
                    pct = count / total_batches * 100
                    color = STATUS_COLORS.get(status, "#9A9A9A")
                    icon = STATUS_ICONS.get(status, "•")
                    st.markdown(
                        f"""<div style='display:flex;align-items:center;gap:12px;
                        background:#1C1C1C;border:1px solid #2D2D2D;border-radius:8px;
                        padding:10px 14px;margin-bottom:6px'>
                        <span style='font-size:1.2rem'>{icon}</span>
                        <span style='flex:1;color:#F2F2F2;text-transform:capitalize'>{status}</span>
                        <span style='color:{color};font-weight:600'>{count}</span>
                        <span style='color:#666;font-size:0.8rem'>({pct:.0f}%)</span>
                        </div>""",
                        unsafe_allow_html=True,
                    )

    with col_right:
        section_header("AI Model Registry")
        if total_models == 0:
            st.info("No trained models. Use **Model Training** to train your first model.")
        else:
            c1r, c2r = st.columns(2)
            c1r.metric("Models Trained", total_models)
            c2r.metric("Evaluations", total_evals)

            if best_model and best_eval:
                st.markdown(
                    f"""<div style='background:#1C1C1C;border:1px solid #C9A84C33;
                    border-radius:8px;padding:12px 16px;margin-top:8px'>
                    <div style='color:#9A9A9A;font-size:0.75rem;text-transform:uppercase'>
                    🏆 Best Model</div>
                    <div style='color:#C9A84C;font-weight:600;font-size:1rem;margin-top:4px'>
                    {best_model.model_name}</div>
                    <div style='color:#9A9A9A;font-size:0.8rem'>
                    Accuracy: {best_eval.accuracy:.4f} · v{best_model.version}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

            st.metric("AI Predictions Run", total_preds)

    # ══════════════════════════════════════════════════════════════════
    # ROW 3 — Recent Activity + Inventory
    # ══════════════════════════════════════════════════════════════════
    col_a, col_b = st.columns(2)

    with col_a:
        section_header("Recent Batches")
        if not recent_batches:
            st.info("No batches yet.")
        else:
            for b in recent_batches:
                sb = status_badge(b.status or "unknown",
                                  "success" if b.status == "completed"
                                  else "warning" if b.status in ("sorting","dismantling","processing")
                                  else "info")
                st.markdown(
                    f"""<div style='background:#1C1C1C;border:1px solid #2D2D2D;
                    border-radius:8px;padding:10px 14px;margin-bottom:6px;
                    display:flex;align-items:center;gap:10px'>
                    <span style='color:#C9A84C;font-weight:600;flex:1'>
                    {b.batch_id}</span>
                    <span style='color:#9A9A9A;font-size:0.8rem'>{b.total_weight_kg:.1f} kg</span>
                    {sb}
                    </div>""",
                    unsafe_allow_html=True,
                )

    with col_b:
        section_header("Top Inventory Items")
        if not top_inventory:
            st.info("No inventory data. Log recovery records in Industrial Operations.")
        else:
            for item in top_inventory:
                st.markdown(
                    f"""<div style='background:#1C1C1C;border:1px solid #2D2D2D;
                    border-radius:8px;padding:10px 14px;margin-bottom:6px;
                    display:flex;align-items:center;gap:10px'>
                    <span style='color:#F2F2F2;flex:1;text-transform:capitalize'>
                    {item.material_name}</span>
                    <span style='color:#C9A84C;font-weight:600'>
                    {item.quantity_kg:.2f} kg</span>
                    </div>""",
                    unsafe_allow_html=True,
                )

    # ══════════════════════════════════════════════════════════════════
    # ROW 4 — Environmental Quick Stats
    # ══════════════════════════════════════════════════════════════════
    section_header("Environmental Quick Estimates")
    st.caption("⚠️ Approximate estimates based on published research averages — not certified measurements.")

    co2_avoided  = total_recovered * 2.5   # ~2.5 kg CO₂ per kg recovered (average)
    energy_saved = total_recovered * 15.0  # ~15 kWh per kg recovered (average)

    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Est. CO₂ Avoided", f"{co2_avoided:.1f} kg",
              help="Based on ~2.5 kg CO₂ avoided per kg material recovered (UNEP avg.)")
    e2.metric("Est. Energy Saved", f"{energy_saved:.0f} kWh",
              help="Recycling vs. primary production — ~15 kWh/kg average")
    e3.metric("Landfill Diverted", f"{total_recovered:.1f} kg")
    e4.metric("Completed Batches", status_counts.get("completed", 0))

    # ══════════════════════════════════════════════════════════════════
    # ROW 5 — Quick Actions
    # ══════════════════════════════════════════════════════════════════
    section_header("Quick Navigation")
    qa_cols = st.columns(4)
    qa_cols[0].markdown(
        "<div style='background:#1C1C1C;border:1px solid #2D2D2D;border-radius:8px;"
        "padding:1rem;text-align:center'><div style='font-size:1.5rem'>📦</div>"
        "<div style='color:#C9A84C;font-weight:600;font-size:0.85rem;margin-top:4px'>"
        "Register Batch</div>"
        "<div style='color:#666;font-size:0.75rem'>Industrial Operations</div></div>",
        unsafe_allow_html=True,
    )
    qa_cols[1].markdown(
        "<div style='background:#1C1C1C;border:1px solid #2D2D2D;border-radius:8px;"
        "padding:1rem;text-align:center'><div style='font-size:1.5rem'>🔬</div>"
        "<div style='color:#C9A84C;font-weight:600;font-size:0.85rem;margin-top:4px'>"
        "Analyse Image</div>"
        "<div style='color:#666;font-size:0.75rem'>E-Waste Analysis</div></div>",
        unsafe_allow_html=True,
    )
    qa_cols[2].markdown(
        "<div style='background:#1C1C1C;border:1px solid #2D2D2D;border-radius:8px;"
        "padding:1rem;text-align:center'><div style='font-size:1.5rem'>🧠</div>"
        "<div style='color:#C9A84C;font-weight:600;font-size:0.85rem;margin-top:4px'>"
        "Train Model</div>"
        "<div style='color:#666;font-size:0.75rem'>Model Training</div></div>",
        unsafe_allow_html=True,
    )
    qa_cols[3].markdown(
        "<div style='background:#1C1C1C;border:1px solid #2D2D2D;border-radius:8px;"
        "padding:1rem;text-align:center'><div style='font-size:1.5rem'>📄</div>"
        "<div style='color:#C9A84C;font-weight:600;font-size:0.85rem;margin-top:4px'>"
        "Generate Report</div>"
        "<div style='color:#666;font-size:0.75rem'>Report Generator</div></div>",
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════════
    # Footer
    # ══════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;color:#444;font-size:0.75rem'>"
        "E-Waste AI Platform · Phase 5 · "
        "All data from live database · Financial & environmental figures are estimates only"
        "</div>",
        unsafe_allow_html=True,
    )
