"""
E-Waste AI — Executive Industrial & Intelligence Dashboard
==========================================================
Obsidian & Champagne Gold command center backed by live SQLite telemetry,
real saved model counts, interactive workflow navigation, and a live
rule-based recovery sandbox (all estimates clearly labelled).
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from frontend.theme import (
    CHART_PALETTE,
    COLORS,
    apply_theme,
    empty_state_card,
    hero_banner,
    kpi_card,
    plotly_dark_layout,
    section_header,
    status_badge,
)

try:
    from backend.database import SessionLocal
    from backend.models.all_models import (
        AIPrediction,
        Device,
        Inventory,
        ModelEvaluation,
        RecoveryRecord,
        TrainedModel,
        WasteBatch,
    )
    DB_OK = True
except Exception as e:
    DB_OK = False
    DB_ERR = str(e)

try:
    from backend.services.advanced_intelligence import get_engine
    ENG_OK = True
except Exception:
    ENG_OK = False


def _db():
    return SessionLocal() if DB_OK else None


def _navigate(page_key: str):
    st.session_state.current_page = page_key
    st.rerun()


def render_dashboard():
    apply_theme()

    # Check real disk .pkl count transparently
    saved_dir = Path(__file__).resolve().parent.parent.parent / "models" / "saved"
    disk_pkl_count = len(list(saved_dir.glob("*.pkl"))) if saved_dir.exists() else 0

    hero_banner(
        eyebrow="COMBINED INDUSTRIAL INTELLIGENCE & RESEARCH PLATFORM",
        title="E-Waste AI Command Center",
        subtitle=(
            "Real-time operational telemetry, verified material composition estimates, "
            "recovery planning, and reproducible ML experimentation — CPU-ready."
        ),
        icon="♻️",
        badges=[
            ("LIVE SQLITE" if DB_OK else "DB OFFLINE", "live" if DB_OK else "neutral"),
            (f"{disk_pkl_count} SAVED MODELS", "gold"),
            (datetime.now().strftime("%d %b %Y · %H:%M"), "neutral"),
        ],
    )

    # ── Interactive Quick-Launch Workflow Bar ─────────────────────────
    q1, q2, q3, q4 = st.columns(4)
    if q1.button("🏭 Register E-Waste Batch", type="primary", use_container_width=True, key="dash_go_ops"):
        _navigate("industrial_inventory")
    if q2.button("🧠 AI Intelligence Workbench", type="secondary", use_container_width=True, key="dash_go_ai"):
        _navigate("ai_intelligence")
    if q3.button("♻️ Recovery & Economics", type="secondary", use_container_width=True, key="dash_go_rec"):
        _navigate("recovery_intelligence")
    if q4.button("🤖 ML Model Training", type="secondary", use_container_width=True, key="dash_go_ml"):
        _navigate("model_training")

    if not DB_OK:
        st.error(f"⚠️ Database unavailable: {DB_ERR}")
        return

    db = _db()
    try:
        from sqlalchemy import func
        total_batches = db.query(WasteBatch).count()
        total_devices = db.query(Device).count()
        total_models = db.query(TrainedModel).count()
        total_preds = db.query(AIPrediction).count()
        total_weight = db.query(func.sum(WasteBatch.total_weight_kg)).scalar() or 0.0
        total_rec_g = db.query(func.sum(RecoveryRecord.recovered_quantity_g)).scalar() or 0.0
        total_rec_kg = total_rec_g / 1000.0

        stages = ["incoming", "sorting", "dismantling", "processing", "completed", "rejected"]
        status_counts = {s: db.query(WasteBatch).filter(WasteBatch.status == s).count() for s in stages}
        recent_batches = db.query(WasteBatch).order_by(WasteBatch.created_at.desc()).limit(6).all()
        top_inventory = db.query(Inventory).order_by(Inventory.quantity_g.desc()).limit(6).all()

        best_model_name = "—"
        best_acc = None
        for ev in db.query(ModelEvaluation).all():
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
        return
    finally:
        db.close()

    # ── Executive KPI Strip ───────────────────────────────────────────
    section_header("Operations Telemetry", "Live metrics queried directly from the operational database", "📡")
    rec_rate = (total_rec_kg / total_weight * 100) if total_weight else 0.0
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        kpi_card("Total Batches", f"{total_batches:,}", "All logged waste intake lots", "gold")
    with k2:
        kpi_card("Intake Mass", f"{total_weight:,.1f} kg", "Cumulative batch weight", "info")
    with k3:
        kpi_card("Recovered Mass", f"{total_rec_kg:,.3f} kg", f"{total_rec_g:,.0f} g logged", "success")
    with k4:
        kpi_card("Devices Tracked", f"{total_devices:,}", "Disaggregated units", "neutral")
    with k5:
        kpi_card("Recovery Yield", f"{rec_rate:.1f}%", "Recovered / Intake mass", "warning" if rec_rate < 40 and total_weight > 0 else "gold")

    # ── Pipeline Visualization + Model Registry ───────────────────────
    col_l, col_r = st.columns([1.3, 1.0])
    with col_l:
        section_header("Batch Pipeline Distribution", "Live count across processing workflow stages", "⚡")
        if total_batches == 0:
            empty_state_card(
                "📦",
                "No Operational Batches Registered",
                "Register an incoming e-waste batch in Industrial Operations to unlock live pipeline stage analytics and material recovery comparisons.",
                hint="Click 'Register E-Waste Batch' above to begin",
            )
        else:
            import plotly.graph_objects as go
            active_stages = [(k.title(), v) for k, v in status_counts.items() if v > 0]
            if active_stages:
                labels = [s[0] for s in active_stages]
                values = [s[1] for s in active_stages]
                fig = go.Figure(
                    go.Bar(
                        x=values,
                        y=labels,
                        orientation="h",
                        marker=dict(color=CHART_PALETTE[: len(labels)], line=dict(color="#060709", width=1)),
                        text=values,
                        textposition="auto",
                    )
                )
                plotly_dark_layout(fig, title="Batches by Workflow Stage", height=290, xaxis_title="Batch Count")
                st.plotly_chart(fig, use_container_width=True)

    with col_r:
        section_header("AI Model & Registry Telemetry", "Synced database records & CPU artifact files", "🤖")
        m1, m2 = st.columns(2)
        with m1:
            kpi_card("DB Models", str(total_models), "Registered in SQLite", "gold")
        with m2:
            kpi_card("Disk .pkl Files", str(disk_pkl_count), "Synthetic validation artifacts", "info")
        kpi_card("Logged Predictions", str(total_preds), "Audit-tracked AI inference runs", "neutral")
        if best_model_name != "—" and best_acc is not None:
            kpi_card("Top DB Model", best_model_name, f"Recorded accuracy: {best_acc:.4f}", "success", "VERIFIED")

    # ── Interactive Live Material Recovery Explorer ───────────────────
    section_header(
        "Interactive Recovery Yield Explorer",
        "Instant rule-based composition preview powered by UNEP / EEA reference data (Estimate Only)",
        "🧪",
    )
    if ENG_OK:
        eng = get_engine()
        supported = eng.list_supported_device_types()
        with st.container():
            sc1, sc2, sc3 = st.columns([1.2, 1.4, 1.0])
            sim_dev = sc1.selectbox(
                "Device Category",
                supported,
                format_func=lambda x: x.replace("_", " ").title(),
                key="dash_sim_device",
            )
            sim_wt = sc2.slider("Interactive Weight (kg)", min_value=0.5, max_value=250.0, value=10.0, step=0.5, key="dash_sim_wt")
            sim_cond = sc3.selectbox("Device Condition", ["unknown", "poor", "fair", "good", "excellent"], key="dash_sim_cond")

            est = eng.estimate_recovery(sim_dev, sim_wt, sim_cond)
            if est.get("available"):
                mats = est.get("recoverable_materials", {})
                total_g = sum(v.get("estimated_recovered_g", 0.0) for v in mats.values())
                total_val = est.get("total_estimated_value_usd", 0.0)

                s1, s2, s3 = st.columns(3)
                with s1:
                    kpi_card("Input Stream", f"{sim_wt:.1f} kg", sim_dev.replace("_", " ").title(), "neutral", "SIMULATOR")
                with s2:
                    kpi_card("Est. Recoverable Output", f"{total_g:,.1f} g", f"{total_g / 1000:.2f} kg yield", "success", "ESTIMATE")
                with s3:
                    kpi_card("Est. Gross Value", f"${total_val:,.2f} USD", f"Source: {est.get('data_source', 'UNEP/EEA')}", "gold", "ESTIMATE")

                import plotly.graph_objects as go
                mat_names = [k.replace("_", " ").title() for k in mats.keys()]
                mat_g = [v.get("estimated_recovered_g", 0.0) for v in mats.values()]
                mat_usd = [v.get("estimated_value_usd", 0.0) for v in mats.values()]

                ch_l, ch_r = st.columns(2)
                with ch_l:
                    fig_m = go.Figure(
                        go.Bar(
                            x=mat_g,
                            y=mat_names,
                            orientation="h",
                            marker=dict(color="#C9A84C"),
                            hovertemplate="<b>%{y}</b><br>Est. Recovered: %{x:.2f} g<extra></extra>",
                        )
                    )
                    plotly_dark_layout(fig_m, title="Est. Recoverable Mass (g)", height=310, xaxis_title="Grams (g)")
                    st.plotly_chart(fig_m, use_container_width=True)
                with ch_r:
                    fig_v = go.Figure(
                        go.Pie(
                            labels=mat_names,
                            values=mat_usd,
                            hole=0.58,
                            marker=dict(colors=CHART_PALETTE),
                            textinfo="label+percent",
                            hovertemplate="<b>%{label}</b><br>Est. Value: $%{value:.4f}<extra></extra>",
                        )
                    )
                    plotly_dark_layout(fig_v, title="Est. Value Contribution (USD Share)", height=310)
                    fig_v.update_layout(showlegend=False)
                    st.plotly_chart(fig_v, use_container_width=True)

                st.caption(f"⚠️ {est.get('disclaimer', 'Estimates are based on published composition averages only.')}")

    # ── Recent Batches + Top Inventory ────────────────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        section_header("Recent Batches", "Latest waste intake records")
        if not recent_batches:
            empty_state_card("📋", "No Batches Yet", "Incoming batch activity will appear here once registered.")
        else:
            for b in recent_batches:
                sb = status_badge(
                    b.status or "unknown",
                    "success" if b.status == "completed"
                    else "warning" if b.status in ("sorting", "dismantling", "processing")
                    else "info",
                )
                st.markdown(
                    f"""<div class='ewaste-card' style='padding:0.75rem 1rem;margin-bottom:0.5rem;
                    display:flex;align-items:center;gap:10px'>
                    <span style='color:#F2D67B;font-family:JetBrains Mono,monospace;font-weight:600;flex:1'>{b.batch_number}</span>
                    <span style='color:#9CA3AF;font-size:0.82rem'>{(b.total_weight_kg or 0):.1f} kg</span>
                    {sb}</div>""",
                    unsafe_allow_html=True,
                )

    with col_b:
        section_header("Top Inventory Stock", "Recovered fractions stored by mass")
        if not top_inventory:
            empty_state_card("🗄️", "Inventory Empty", "Log material recovery records in Industrial Operations to populate stock.")
        else:
            for item in top_inventory:
                qty_g = item.quantity_g or 0.0
                st.markdown(
                    f"""<div class='ewaste-card' style='padding:0.75rem 1rem;margin-bottom:0.5rem;
                    display:flex;align-items:center;gap:10px'>
                    <span style='color:#F4F4F6;flex:1;text-transform:capitalize;font-weight:500'>{item.material_name}</span>
                    <span style='color:#F2D67B;font-family:JetBrains Mono,monospace;font-weight:600'>{qty_g:,.1f} g</span>
                    <span style='color:#6B7280;font-size:0.76rem'>({qty_g / 1000:.3f} kg)</span>
                    </div>""",
                    unsafe_allow_html=True,
                )

    # ── Environmental Quick Estimates ─────────────────────────────────
    section_header("Environmental Quick Estimates", "Indicative lifecycle savings from recovered output (not certified)")
    st.caption("⚠️ Approximate estimates based on UNEP primary-vs-recycled factor (~2.5 kg CO₂ & 15 kWh per kg recovered).")
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        kpi_card("Est. CO₂ Avoided", f"{total_rec_kg * 2.5:,.2f} kg", "Based on logged recovery", "success", "ESTIMATE")
    with e2:
        kpi_card("Est. Energy Saved", f"{total_rec_kg * 15:,.1f} kWh", "Primary vs secondary prod.", "info", "ESTIMATE")
    with e3:
        kpi_card("Landfill Diverted", f"{total_rec_kg:,.3f} kg", "Recovered mass proxy", "gold", "ESTIMATE")
    with e4:
        kpi_card("Completed Batches", str(status_counts.get("completed", 0)), "Status = completed", "neutral")

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;color:#6B7280;font-size:0.75rem'>"
        "E-Waste AI Platform · Live Database & Rule-Based KB · All financial/environmental metrics are estimates only"
        "</div>",
        unsafe_allow_html=True,
    )
