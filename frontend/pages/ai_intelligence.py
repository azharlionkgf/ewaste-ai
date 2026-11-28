"""
E-Waste AI — Interactive AI Intelligence Dashboard
===================================================
Luxury Obsidian & Gold interactive workspace integrating:
- Live reactive device material composition & recovery yield analysis
- Batch-level recovery priority optimization & interactive charts
- Predictive volume/recovery trends
- Interactive anomaly detection & severity filtering
- Model Explainability (SHAP / feature importance) with optional sample test vector
- Hazardous substance reference & risk matrix
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from frontend.theme import (
    CHART_PALETTE,
    apply_theme,
    empty_state_card,
    hero_banner,
    kpi_card,
    plotly_dark_layout,
    section_header,
    status_badge,
)

try:
    from backend.services.advanced_intelligence import (
        HAZARDOUS_REFERENCE,
        MATERIAL_KNOWLEDGE_BASE,
        get_engine,
    )
    AI6_OK = True
except Exception as e:
    AI6_OK = False
    AI6_ERR = str(e)

try:
    from backend.database import SessionLocal
    from backend.models.all_models import WasteBatch
    DB_OK = True
except Exception:
    DB_OK = False


def _db():
    return SessionLocal() if DB_OK else None


def render_ai_intelligence():
    apply_theme()
    hero_banner(
        eyebrow="PHASE 6 · EXPLAINABLE & RECOVERY INTELLIGENCE",
        title="AI Intelligence Workbench",
        subtitle=(
            "Interactive material recovery estimation, batch planning, time-based trends, "
            "anomaly checks, CPU model explainability, and hazardous substance reference."
        ),
        icon="🧠",
        badges=[
            ("6 INTERACTIVE MODULES", "gold"),
            ("ENGINE ACTIVE" if AI6_OK else "ENGINE OFFLINE", "live" if AI6_OK else "neutral"),
        ],
    )

    if not AI6_OK:
        st.error(f"Advanced Intelligence Engine unavailable: {AI6_ERR}")
        return

    engine = get_engine()

    tabs = st.tabs([
        "🔍 Live Device Analyzer",
        "📦 Batch Recovery Plan",
        "📈 Trends & Forecasts",
        "⚠️ Anomaly Monitor",
        "🤖 Model Explainer",
        "☣️ Hazardous Guide",
    ])

    # ── TAB 1: REACTIVE DEVICE ANALYSIS ───────────────────────────────
    with tabs[0]:
        section_header(
            "Reactive Device Material Analysis",
            "Adjust sliders and condition to inspect composition & recovery estimates in real time (UNEP/EEA)",
        )
        c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.0, 1.0])
        device_type = c1.selectbox(
            "Device Type",
            engine.list_supported_device_types(),
            format_func=lambda x: x.replace("_", " ").title(),
            key="ai_dev_type",
        )
        weight_kg = c2.slider("Unit Weight (kg)", min_value=0.05, max_value=50.0, value=2.0, step=0.05, key="ai_unit_wt")
        units_cnt = c3.number_input("Quantity (Units)", min_value=1, max_value=5000, value=1, step=1, key="ai_units_cnt")
        condition = c4.selectbox("Condition", ["unknown", "poor", "fair", "good", "excellent"], key="ai_dev_cond")

        total_weight_kg = round(weight_kg * units_cnt, 4)
        result = engine.estimate_recovery(device_type, total_weight_kg, condition)

        if not result.get("available"):
            st.error(result.get("message", "Device category not available."))
        else:
            _display_recovery_estimate(result, total_weight_kg)

        kb = engine.get_device_knowledge(device_type)
        if kb.get("available"):
            with st.expander(f"📚 Reference Knowledge Base: {device_type.replace('_', ' ').title()}"):
                st.markdown(f"**Source:** {kb['source']}  ·  **Reference Unit Avg Weight:** {kb['avg_weight_kg']} kg  ·  **Confidence:** {kb['confidence']}")
                st.markdown(f"**Components:** {', '.join(kb.get('components', []))}")
                st.markdown(f"**Notes:** {kb.get('notes', '')}")
                import pandas as pd
                comp_rows = [{"Material": k.replace("_", " ").title(), "Composition %": v} for k, v in kb["material_composition_percent"].items()]
                st.dataframe(pd.DataFrame(comp_rows), use_container_width=True)

    # ── TAB 2: BATCH RECOVERY PLAN ────────────────────────────────────
    with tabs[1]:
        section_header("Batch Recovery Plan", "Priority recovery ranking & safety warnings from batch device records")
        if not DB_OK:
            empty_state_card("🔌", "Database Unavailable", "Database connection required to load industrial waste batches.")
        else:
            db = _db()
            try:
                batches = db.query(WasteBatch).order_by(WasteBatch.created_at.desc()).all()
            except Exception as ex:
                st.error(str(ex))
                batches = []
            finally:
                db.close()

            if not batches:
                empty_state_card(
                    "📦",
                    "No Batches Registered",
                    "Register a waste batch and its disaggregated devices in Industrial Operations to generate a recovery plan.",
                    hint="Navigate to Industrial Inventory → Batches",
                )
            else:
                bmap = {f"{b.batch_number} ({(b.total_weight_kg or 0):.1f} kg · {b.status})": b.id for b in batches}
                sel = st.selectbox("Select Waste Batch", list(bmap.keys()), key="ai_plan_batch")
                col1, col2 = st.columns(2)
                if col1.button("📊 Estimate Batch Recovery", type="primary", use_container_width=True):
                    with st.spinner("Calculating batch recovery estimate…"):
                        _display_batch_recovery(engine.estimate_batch_recovery(bmap[sel]))
                if col2.button("📋 Generate Recovery Priority Plan", type="secondary", use_container_width=True):
                    with st.spinner("Generating prioritized plan…"):
                        _display_recovery_plan(engine.recommend_recovery_plan(bmap[sel]))

    # ── TAB 3: TRENDS & FORECASTS ─────────────────────────────────────
    with tabs[2]:
        section_header("Operational Volume & Recovery Trends", "Time-window comparison built from actual logged batch dates")
        tc1, tc2 = st.columns([2, 1])
        period = tc1.slider("Lookback Period (Days)", min_value=7, max_value=180, value=30, step=1, key="ai_trend_days")
        if tc2.button("📈 Compute Live Trends", type="primary", use_container_width=True):
            with st.spinner("Computing trends…"):
                trends = engine.compute_trends(days=period)
            _display_trends(trends)
        else:
            _display_trends(engine.compute_trends(days=period))

    # ── TAB 4: ANOMALY MONITOR ────────────────────────────────────────
    with tabs[3]:
        section_header("Anomaly & Quality Monitor", "Automated consistency, duplicate, and yield checks (flags require manual review)")
        st.info("ℹ️ Rule-based flags identify unusual quantities or missing operational links. A flag is NEVER proof of wrongdoing.")

        ac1, ac2 = st.columns([2, 1])
        sev_filter = ac1.multiselect("Severity Filter", ["high", "medium", "low"], default=["high", "medium", "low"], key="ai_anom_sev")
        scan_clicked = ac2.button("🔎 Scan Database Records", type="primary", use_container_width=True)
        flags = engine.detect_anomalies() if (scan_clicked or True) else []
        filtered_flags = [f for f in flags if f.get("severity", "low") in sev_filter]
        _display_anomalies(filtered_flags, total_count=len(flags))

    # ── TAB 5: MODEL EXPLAINER ────────────────────────────────────────
    with tabs[4]:
        section_header("Explainable AI Inspector", "Feature attribution via SHAP (tree/linear) or intrinsic feature importance")
        available_models = engine.list_available_models()
        file_models = [m for m in available_models if m.get("file_exists")]

        if not file_models:
            empty_state_card(
                "🤖",
                "No .pkl Model Artifacts Found",
                "Train a model in Model Training to unlock feature attribution and prediction explanations.",
            )
        else:
            model_opts = {m["model_id"]: f"{m['name']} v{m['version']}" for m in file_models}
            mc1, mc2 = st.columns([2, 1])
            sel_model = mc1.selectbox("Select Trained Model Artifact", list(model_opts.keys()), format_func=lambda i: model_opts[i])
            sel_m_meta = next(m for m in file_models if m["model_id"] == sel_model)

            st.caption("⚠️ Saved repository models were trained on synthetic validation data (not live facility records).")
            n_features = int(mc2.number_input("Feature Dimensions", 2, 20, 10, step=1, key="exp_nfeat"))

            if st.button("🎲 Populate Sample Test Vector (Seed 42)", type="secondary", key="exp_seed_btn"):
                import numpy as np
                rng = np.random.default_rng(42)
                for i in range(n_features):
                    st.session_state[f"fv_{i}"] = round(float(rng.uniform(-1.5, 1.5)), 3)

            features = {}
            feat_cols = st.columns(min(n_features, 5))
            for i in range(n_features):
                with feat_cols[i % 5]:
                    fname = st.text_input(f"Feature {i+1}", value=f"feature_{i}", key=f"fn_{i}")
                    fval = st.number_input(f"Val {i+1}", value=float(st.session_state.get(f"fv_{i}", 0.0)), step=0.1, key=f"fv_{i}")
                    features[fname] = fval

            if st.button("🔬 Run Model Prediction & Explain", type="primary"):
                ok, msg = engine.load_model(sel_m_meta["file_path"], sel_model)
                if not ok:
                    st.error(f"Could not load model: {msg}")
                else:
                    pred_res = engine.predict(sel_model, features)
                    exp = engine.explain_prediction(sel_model, features)
                    if "error" not in pred_res:
                        pc1, pc2 = st.columns(2)
                        with pc1:
                            kpi_card("Model Prediction", str(pred_res.get("prediction", "—")), "Actual model output", "gold", "INFERENCE")
                        with pc2:
                            conf = pred_res.get("confidence")
                            kpi_card("Confidence", f"{conf:.2%}" if isinstance(conf, float) else "N/A", "Top class probability", "info")
                    _display_explanation(exp)

    # ── TAB 6: HAZARDOUS GUIDE ────────────────────────────────────────
    with tabs[5]:
        section_header("Hazardous Substance Reference", "Documented e-waste hazard categories (awareness only — not certified instructions)")
        st.error(
            "🚨 **Safety Warning:** Hazardous e-waste handling requires licensed operators and statutory PPE. "
            "This system does NOT grant regulatory certification or dismantling clearance."
        )
        hc1, hc2 = st.columns([1.4, 1.0])
        risk_filter = hc1.multiselect("Filter Risk Level", ["high", "medium", "low"], default=["high", "medium", "low"], key="haz_risk_flt")
        dev_sel = hc2.selectbox(
            "Highlight Substances in Device",
            list(MATERIAL_KNOWLEDGE_BASE.keys()),
            format_func=lambda x: x.replace("_", " ").title(),
            key="haz_dev",
        )

        import pandas as pd
        haz_rows = [
            {
                "Substance": sub.replace("_", " ").title(),
                "Risk": info["risk_level"].upper(),
                "Regulation": info["regulation"],
                "Handling Guidance": info["handling"],
            }
            for sub, info in HAZARDOUS_REFERENCE.items()
            if info["risk_level"] in risk_filter
        ]
        if haz_rows:
            st.dataframe(pd.DataFrame(haz_rows), use_container_width=True)

        section_header(f"Device Hazard Profile: {dev_sel.replace('_', ' ').title()}")
        kb = MATERIAL_KNOWLEDGE_BASE[dev_sel]
        for hz in kb.get("hazardous_substances", []):
            ref = HAZARDOUS_REFERENCE.get(hz, {})
            risk = ref.get("risk_level", "unknown")
            color = {"high": "error", "medium": "warning", "low": "info"}.get(risk, "muted")
            sb = status_badge(risk.upper(), color)
            st.markdown(
                f"<div class='ewaste-card' style='padding:0.7rem 1rem;margin-bottom:0.45rem'>"
                f"{sb} <strong style='margin-left:8px;color:#F4F4F6'>{hz.replace('_', ' ').title()}</strong>"
                f"<span style='color:#9CA3AF;font-size:0.85rem'> — {ref.get('handling', 'Consult specialist')}</span></div>",
                unsafe_allow_html=True,
            )


# ── Display Helpers ───────────────────────────────────────────────────

def _display_recovery_estimate(result: dict, total_weight_kg: float):
    import pandas as pd
    import plotly.graph_objects as go

    mats = result.get("recoverable_materials", {})
    total_val = result.get("total_estimated_value_usd", 0.0)
    total_rec_g = sum(d.get("estimated_recovered_g", 0.0) for d in mats.values())
    yield_pct = (total_rec_g / (total_weight_kg * 1000.0) * 100.0) if total_weight_kg > 0 else 0.0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Input Stream", f"{total_weight_kg:,.2f} kg", f"{total_weight_kg * 1000:,.0f} g", "neutral")
    with k2:
        kpi_card("Est. Recovered Mass", f"{total_rec_g:,.1f} g", f"{yield_pct:.1f}% mass yield", "success", "ESTIMATE")
    with k3:
        kpi_card("Est. Gross Value", f"${total_val:,.2f}", result.get("knowledge_confidence", "—"), "gold", "ESTIMATE")
    with k4:
        kpi_card("Material Streams", str(len(mats)), result.get("data_source", "UNEP/EEA"), "info")

    if mats:
        names = [m.replace("_", " ").title() for m in mats.keys()]
        rec_g = [d["estimated_recovered_g"] for d in mats.values()]
        tot_g = [d["total_mass_g"] for d in mats.values()]
        usd = [d["estimated_value_usd"] for d in mats.values()]

        c_l, c_r = st.columns([1.25, 1.0])
        with c_l:
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Total Mass (g)", x=names, y=tot_g, marker_color="rgba(148,163,184,0.35)"))
            fig.add_trace(go.Bar(name="Est. Recovered (g)", x=names, y=rec_g, marker_color="#C9A84C"))
            fig.update_layout(barmode="group")
            plotly_dark_layout(fig, title="Material Mass vs Recoverable Fraction (g)", height=330, yaxis_title="Mass (g)")
            st.plotly_chart(fig, use_container_width=True)
        with c_r:
            fig2 = go.Figure(go.Pie(labels=names, values=usd, hole=0.58, marker=dict(colors=CHART_PALETTE), textinfo="label+percent"))
            plotly_dark_layout(fig2, title="Estimated Value Breakdown (USD)", height=330)
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        rows = [
            {
                "Material": mat.replace("_", " ").title(),
                "Composition %": data["composition_pct"],
                "Total Mass (g)": data["total_mass_g"],
                "Recovery Eff. %": data["recovery_efficiency_pct"],
                "Est. Recovered (g)": data["estimated_recovered_g"],
                "Method": data["recovery_method"],
                "Est. Value (USD)": f"${data['estimated_value_usd']:,.4f}",
            }
            for mat, data in mats.items()
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        st.download_button(
            "⬇️ Export Material Estimate CSV",
            pd.DataFrame(rows).to_csv(index=False).encode(),
            "recovery_estimate.csv",
            "text/csv",
        )
    st.caption(f"⚠️ {result.get('disclaimer', 'Estimates only.')}")


def _display_batch_recovery(result: dict):
    if not result.get("available"):
        st.error(result.get("message"))
        return
    import pandas as pd
    import plotly.graph_objects as go

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Batch", str(result.get("batch_number", "—")), f"{result.get('device_count', 0)} devices", "info")
    with c2:
        kpi_card("Est. Batch Value", f"${result['total_estimated_value_usd']:,.2f}", result.get("estimation_basis", "—"), "gold", "ESTIMATE")
    with c3:
        mats = result.get("recoverable_materials", {})
        tot_g = sum(v.get("estimated_recovered_g", 0) for v in mats.values())
        kpi_card("Est. Recovered Output", f"{tot_g:,.1f} g", f"{tot_g/1000:.2f} kg", "success", "ESTIMATE")

    if mats:
        names = [k.replace("_", " ").title() for k in mats.keys()]
        vals = [v.get("estimated_value_usd", 0.0) for v in mats.values()]
        fig = go.Figure(go.Bar(x=vals, y=names, orientation="h", marker=dict(color="#10B981")))
        plotly_dark_layout(fig, title="Estimated Batch Recovery Value by Material (USD)", height=300, xaxis_title="Est. Value ($)")
        st.plotly_chart(fig, use_container_width=True)

        rows = [
            {
                "Material": k.replace("_", " ").title(),
                "Est. Recovered (g)": v.get("estimated_recovered_g", 0),
                "Est. Value (USD)": f"${v.get('estimated_value_usd', 0):,.2f}",
            }
            for k, v in mats.items()
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    st.warning(result.get("disclaimer", "Estimates only."))


def _display_recovery_plan(plan: dict):
    if not plan.get("available"):
        st.error(plan.get("message"))
        return
    section_header("Recovery Priority Queue")
    priorities = plan.get("recovery_priorities", [])
    if priorities:
        import plotly.graph_objects as go
        names = [f"#{p['priority_rank']} {p['material'].replace('_', ' ').title()}" for p in priorities]
        vals = [p["estimated_value_usd"] for p in priorities]
        fig = go.Figure(go.Bar(x=vals[::-1], y=names[::-1], orientation="h", marker=dict(color="#C9A84C")))
        plotly_dark_layout(fig, title="Recovery Priorities Ranked by Est. Value (USD)", height=max(260, len(names) * 42), xaxis_title="Est. Value ($)")
        st.plotly_chart(fig, use_container_width=True)

        for p in priorities:
            st.markdown(
                f"""<div class='ewaste-card' style='padding:0.85rem 1.1rem;margin-bottom:0.5rem'>
                <span style='color:#F2D67B;font-weight:700'>#{p['priority_rank']} {p['material'].replace('_',' ').title()}</span>
                <span style='color:#9CA3AF;font-family:JetBrains Mono,monospace;font-size:0.8rem;margin-left:12px'>
                Est. {p['estimated_recovered_g']:.2f} g · ${p['estimated_value_usd']:,.4f}</span>
                <div style='color:#9CA3AF;font-size:0.82rem;margin-top:4px'>{p['reason']}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    warnings = plan.get("hazardous_warnings", [])
    if warnings:
        st.error(f"⚠️ {len(warnings)} hazardous substance(s) detected — specialist handling required.")
        for w in warnings:
            st.markdown(f"- **{w['substance']}** ({w['risk_level']} risk) in {w['device_type']}: {w['handling']}")


def _display_trends(trends: dict):
    if trends.get("error"):
        st.error(f"Trend computation failed: {trends['error']}")
        return
    if not trends.get("data_sufficient"):
        st.warning(f"⚠️ Insufficient historical data: {trends.get('insufficient_data_note', 'Not enough records.')}")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Batches in Window", str(trends.get("batches_in_period", 0)), f"Last {trends.get('period_days', 30)} days", "gold")
    with c2:
        kpi_card("Weight in Window", f"{trends.get('total_weight_period_kg', 0):.1f} kg", "Intake volume", "info")
    with c3:
        kpi_card("Recovered in Window", f"{trends.get('total_recovered_period_g', 0):.1f} g", "Logged recovered mass", "success")
    with c4:
        chg = trends.get("weight_change_pct")
        kpi_card("Volume Change", f"{chg:+.1f}%" if chg is not None else "N/A", "vs prior window", "warning" if (chg or 0) < 0 else "gold")


def _display_anomalies(flags: list, total_count: int = 0):
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Total Flags Found", str(total_count), "Across all rules", "warning" if total_count else "success")
    with c2:
        high_c = sum(1 for f in flags if f.get("severity") == "high")
        kpi_card("High Severity", str(high_c), "Requires manual verification", "error" if high_c else "neutral")
    with c3:
        kpi_card("Showing Filtered", str(len(flags)), "Matching current filter", "gold")

    if not flags:
        empty_state_card("✅", "No Matching Anomaly Flags", "No records matched your severity filter or current database audit checks.")
        return

    sev_icons = {"high": "🔴 HIGH", "medium": "🟠 MEDIUM", "low": "🔵 LOW"}
    sev_colors = {"high": "error", "medium": "warning", "low": "info"}
    for f in flags:
        sev = f.get("severity", "low")
        with st.expander(f"{sev_icons.get(sev, '⚪')} · {f['type'].replace('_', ' ').title()}", expanded=(sev == "high")):
            st.markdown(status_badge(sev.upper(), sev_colors.get(sev, "info")), unsafe_allow_html=True)
            st.markdown(f["detail"])
            st.markdown(f"**Recommended Action:** {f.get('action', 'Review manually.')}")


def _display_explanation(exp: dict):
    if not exp.get("available"):
        st.warning(exp.get("message"))
        return
    method = exp.get("method", "unknown")
    st.success(f"Explanation Method: **{method}**  ·  Correlation / attribution does not prove causation.")
    importance = exp.get("importance", [])
    if importance:
        import plotly.graph_objects as go
        names = [str(x[0]) for x in importance]
        vals = [float(x[1]) for x in importance]
        colors = ["#C9A84C" if v >= 0 else "#EF4444" for v in vals]
        fig = go.Figure(go.Bar(x=vals, y=names, orientation="h", marker=dict(color=colors)))
        plotly_dark_layout(fig, title=f"Feature Attribution ({method})", height=max(320, len(names) * 34), xaxis_title="Importance / Attribution")
        st.plotly_chart(fig, use_container_width=True)
    st.caption(exp.get("disclaimer", ""))
