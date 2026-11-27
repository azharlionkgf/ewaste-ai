"""
E-Waste AI — Industrial Intelligence Dashboard
Phase 5 Task 3 / Phase 6 enhanced.
Real DB data using actual ORM column names.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from datetime import datetime
from frontend.theme import apply_theme, page_header, section_header, status_badge, COLORS

try:
    from backend.database import SessionLocal
    from backend.models.all_models import (
        WasteBatch, RecoveryRecord, Inventory,
        TrainedModel, ModelEvaluation, AIPrediction, Device,
    )
    DB_OK = True
except Exception as e:
    DB_OK = False
    DB_ERR = str(e)


def _db():
    return SessionLocal() if DB_OK else None


def render_dashboard():
    apply_theme()

    st.markdown(
        f"""<div style='background:linear-gradient(135deg,#141414,#1C1C1C);
        border:1px solid #2D2D2D;border-radius:12px;padding:2rem 2.5rem;
        margin-bottom:1.5rem;border-left:4px solid #C9A84C'>
        <div style='font-family:Poppins,sans-serif;font-size:0.75rem;
        color:#9A9A9A;text-transform:uppercase;letter-spacing:0.1em'>Industrial Intelligence Platform</div>
        <div style='font-family:Poppins,sans-serif;font-size:2rem;font-weight:700;color:#C9A84C;margin:0.3rem 0 0.2rem'>
        ♻️ E-Waste AI</div>
        <div style='color:#9A9A9A;font-size:0.9rem'>
        Combined Industrial Intelligence & Research Platform — Last updated: {datetime.now().strftime('%d %b %Y, %H:%M')}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    if not DB_OK:
        st.error(f"⚠️ Database unavailable: {DB_ERR}")
        st.info("Platform running but cannot connect to database. Check configuration.")
        return

    db = _db()
    try:
        from sqlalchemy import func
        total_batches   = db.query(WasteBatch).count()
        total_devices   = db.query(Device).count()
        total_models    = db.query(TrainedModel).count()
        total_preds     = db.query(AIPrediction).count()
        total_weight    = db.query(func.sum(WasteBatch.total_weight_kg)).scalar() or 0.0
        total_rec_g     = db.query(func.sum(RecoveryRecord.recovered_quantity_g)).scalar() or 0.0
        total_rec_kg    = total_rec_g / 1000.0

        status_counts = {s: db.query(WasteBatch).filter(WasteBatch.status == s).count()
                         for s in ["incoming","sorting","dismantling","processing","completed","rejected"]}
        recent_batches  = db.query(WasteBatch).order_by(WasteBatch.created_at.desc()).limit(5).all()
        top_inventory   = db.query(Inventory).order_by(Inventory.quantity_g.desc()).limit(5).all()

        # Best model — parse accuracy from JSON metrics
        best_model_name = "—"
        best_acc        = None
        evals = db.query(ModelEvaluation).all()
        for ev in evals:
            try:
                import json as _json
                m = _json.loads(ev.metrics) if isinstance(ev.metrics, str) else (ev.metrics or {})
                acc = m.get("accuracy") or m.get("val_accuracy") or m.get("test_accuracy")
                if acc and (best_acc is None or acc > best_acc):
                    best_acc = acc
                    mdl = db.query(TrainedModel).filter(TrainedModel.id == ev.model_id).first()
                    best_model_name = mdl.name if mdl else "—"
            except Exception:
                pass

    except Exception as ex:
        st.error(f"Dashboard data error: {ex}")
        db.close(); return
    finally:
        db.close()

    # ── KPIs ───────────────────────────────────────────────────────────
    section_header("Operations Overview")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Batches", total_batches)
    c2.metric("Total E-Waste", f"{total_weight:.1f} kg")
    c3.metric("Material Recovered", f"{total_rec_kg:.3f} kg")
    c4.metric("Devices Registered", total_devices)
    c5.metric("Recovery Rate",
              f"{(total_rec_kg/total_weight*100 if total_weight else 0):.1f}%")

    # ── Pipeline + Models ──────────────────────────────────────────────
    col_l, col_r = st.columns([1.2, 1])
    with col_l:
        section_header("Batch Pipeline Status")
        STATUS_ICONS = {"incoming":"📥","sorting":"🔄","dismantling":"🔧",
                        "processing":"⚙️","completed":"✅","rejected":"❌"}
        STATUS_COLORS = {"incoming":"#2980B9","sorting":"#E67E22","dismantling":"#E67E22",
                         "processing":"#C9A84C","completed":"#27AE60","rejected":"#E74C3C"}
        if total_batches == 0:
            st.info("No batches yet. Go to **Industrial Operations** to register e-waste.")
        else:
            for status, count in status_counts.items():
                if count > 0:
                    pct = count / total_batches * 100
                    color = STATUS_COLORS.get(status, "#9A9A9A")
                    st.markdown(
                        f"""<div style='display:flex;align-items:center;gap:12px;
                        background:#1C1C1C;border:1px solid #2D2D2D;border-radius:8px;
                        padding:10px 14px;margin-bottom:6px'>
                        <span style='font-size:1.2rem'>{STATUS_ICONS[status]}</span>
                        <span style='flex:1;color:#F2F2F2;text-transform:capitalize'>{status}</span>
                        <span style='color:{color};font-weight:600'>{count}</span>
                        <span style='color:#666;font-size:0.8rem'>({pct:.0f}%)</span>
                        </div>""", unsafe_allow_html=True)

    with col_r:
        section_header("AI Model Registry")
        if total_models == 0:
            st.info("No trained models. Use **Model Training** to train your first model.")
        else:
            c1r, c2r = st.columns(2)
            c1r.metric("Models Trained", total_models)
            c2r.metric("AI Predictions", total_preds)
            if best_model_name != "—" and best_acc:
                st.markdown(
                    f"""<div style='background:#1C1C1C;border:1px solid #C9A84C33;
                    border-radius:8px;padding:12px 16px;margin-top:8px'>
                    <div style='color:#9A9A9A;font-size:0.75rem;text-transform:uppercase'>🏆 Best Model</div>
                    <div style='color:#C9A84C;font-weight:600;font-size:1rem;margin-top:4px'>{best_model_name}</div>
                    <div style='color:#9A9A9A;font-size:0.8rem'>Accuracy: {best_acc:.4f}</div>
                    </div>""", unsafe_allow_html=True)

    # ── Recent Batches + Top Inventory ─────────────────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        section_header("Recent Batches")
        if not recent_batches:
            st.info("No batches yet.")
        else:
            for b in recent_batches:
                sb = status_badge(b.status or "unknown",
                    "success" if b.status == "completed" else
                    "warning" if b.status in ("sorting","dismantling","processing") else "info")
                st.markdown(
                    f"""<div style='background:#1C1C1C;border:1px solid #2D2D2D;
                    border-radius:8px;padding:10px 14px;margin-bottom:6px;
                    display:flex;align-items:center;gap:10px'>
                    <span style='color:#C9A84C;font-weight:600;flex:1'>{b.batch_number}</span>
                    <span style='color:#9A9A9A;font-size:0.8rem'>{b.total_weight_kg:.1f} kg</span>
                    {sb}</div>""", unsafe_allow_html=True)

    with col_b:
        section_header("Top Inventory Items")
        if not top_inventory:
            st.info("No inventory data. Log recovery records in Industrial Operations.")
        else:
            for item in top_inventory:
                qty_kg = (item.quantity_g or 0) / 1000
                st.markdown(
                    f"""<div style='background:#1C1C1C;border:1px solid #2D2D2D;
                    border-radius:8px;padding:10px 14px;margin-bottom:6px;
                    display:flex;align-items:center;gap:10px'>
                    <span style='color:#F2F2F2;flex:1;text-transform:capitalize'>{item.material_name}</span>
                    <span style='color:#C9A84C;font-weight:600'>{item.quantity_g:.1f} g</span>
                    <span style='color:#666;font-size:0.75rem'>({qty_kg:.4f} kg)</span>
                    </div>""", unsafe_allow_html=True)

    # ── Environmental Quick Stats ───────────────────────────────────────
    section_header("Environmental Quick Estimates")
    st.caption("⚠️ Approximate estimates based on published research averages — not certified measurements.")
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Est. CO₂ Avoided", f"{total_rec_kg * 2.5:.2f} kg",
              help="~2.5 kg CO₂ per kg recovered (UNEP avg.)")
    e2.metric("Est. Energy Saved", f"{total_rec_kg * 15:.1f} kWh",
              help="Recycling vs. primary production avg.")
    e3.metric("Landfill Diverted", f"{total_rec_kg:.3f} kg")
    e4.metric("Completed Batches", status_counts.get("completed", 0))

    # ── Footer ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;color:#444;font-size:0.75rem'>"
        "E-Waste AI Platform · Phase 6 · All data from live database · "
        "Financial & environmental figures are estimates only</div>",
        unsafe_allow_html=True)
