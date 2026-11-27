"""
E-Waste AI — Phase 6 AI Intelligence Dashboard
================================================
Integrates: material recovery estimates, economic analysis,
anomaly detection, predictive analytics, explainable AI.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from frontend.theme import apply_theme, page_header, section_header, status_badge, COLORS

try:
    from backend.services.advanced_intelligence import (
        get_engine, MATERIAL_KNOWLEDGE_BASE, HAZARDOUS_REFERENCE,
        MATERIAL_PRICES_USD_PER_G, PRICE_SOURCE, PRICE_DATE,
    )
    AI6_OK = True
except Exception as e:
    AI6_OK = False
    AI6_ERR = str(e)

try:
    from backend.database import SessionLocal
    from backend.models.all_models import WasteBatch, Device, RecoveryRecord, Inventory, TrainedModel
    DB_OK = True
except Exception as e:
    DB_OK = False


def _db():
    return SessionLocal() if DB_OK else None


def render_ai_intelligence():
    apply_theme()
    page_header("AI Intelligence Dashboard",
                "Material estimates, recovery planning, anomaly detection and predictive analytics", "🧠")

    if not AI6_OK:
        st.error(f"Advanced Intelligence Engine unavailable: {AI6_ERR}")
        return

    engine = get_engine()

    tabs = st.tabs([
        "🔍 Device Analysis",
        "📦 Batch Recovery Plan",
        "📈 Trends & Forecasts",
        "⚠️ Anomaly Monitor",
        "🤖 Model Explainer",
        "☣️ Hazardous Guide",
    ])

    # ── TAB 1: DEVICE ANALYSIS ─────────────────────────────────────────
    with tabs[0]:
        section_header("Device Material Analysis",
                       "Estimate recoverable materials from known device types")
        st.info(
            "ℹ️ Estimates are based on published composition averages (UNEP/EEA). "
            "Actual yields vary by manufacturer, model, year and processing method."
        )

        c1, c2, c3 = st.columns(3)
        device_type = c1.selectbox("Device Type",
                                   engine.list_supported_device_types(),
                                   format_func=lambda x: x.replace("_"," ").title())
        weight_kg = c2.number_input("Device Weight (kg)", min_value=0.01, step=0.1, value=2.0)
        condition = c3.selectbox("Condition", ["unknown","poor","fair","good","excellent"])

        if st.button("🔍 Estimate Recovery", type="primary"):
            result = engine.estimate_recovery(device_type, weight_kg, condition)
            if not result.get("available"):
                st.error(result.get("message"))
            else:
                _display_recovery_estimate(result)

        # Knowledge base info
        kb = engine.get_device_knowledge(device_type)
        if kb.get("available"):
            with st.expander(f"📚 Knowledge Base: {device_type.replace('_',' ').title()}"):
                st.markdown(f"**Source:** {kb['source']}")
                st.markdown(f"**Avg Weight:** {kb['avg_weight_kg']} kg")
                st.markdown(f"**Confidence:** {kb['confidence']}")
                st.markdown(f"**Components:** {', '.join(kb.get('components',[]))}")
                st.markdown(f"**Notes:** {kb.get('notes','')}")
                import pandas as pd
                comp_rows = [{"Material": k, "Composition %": v}
                             for k, v in kb["material_composition_percent"].items()]
                st.dataframe(pd.DataFrame(comp_rows), use_container_width=True)

    # ── TAB 2: BATCH RECOVERY PLAN ─────────────────────────────────────
    with tabs[1]:
        section_header("Batch Recovery Plan",
                       "Full recovery estimate and priority recommendations for a batch")
        if not DB_OK:
            st.warning("Database unavailable.")
        else:
            db = _db()
            try:
                batches = db.query(WasteBatch).all()
            except Exception as ex:
                st.error(str(ex)); batches = []
            finally:
                db.close()

            if not batches:
                st.info("No batches registered. Go to Industrial Operations to register e-waste.")
            else:
                bmap = {b.batch_number: b.id for b in batches}
                sel = st.selectbox("Select Batch", list(bmap.keys()))
                col1, col2 = st.columns(2)
                if col1.button("📊 Estimate Recovery", type="primary"):
                    with st.spinner("Calculating batch recovery estimate…"):
                        result = engine.estimate_batch_recovery(bmap[sel])
                    _display_batch_recovery(result)

                if col2.button("📋 Get Recovery Plan"):
                    with st.spinner("Generating recovery plan…"):
                        plan = engine.recommend_recovery_plan(bmap[sel])
                    _display_recovery_plan(plan)

    # ── TAB 3: TRENDS & FORECASTS ──────────────────────────────────────
    with tabs[2]:
        section_header("Operational Trends",
                       "Volume, recovery and cost trends from historical records")
        period = st.selectbox("Analysis Period", [7, 14, 30, 60, 90],
                              format_func=lambda x: f"Last {x} days")
        if st.button("📈 Compute Trends"):
            with st.spinner("Computing trends…"):
                trends = engine.compute_trends(days=period)
            _display_trends(trends)

    # ── TAB 4: ANOMALY MONITOR ─────────────────────────────────────────
    with tabs[3]:
        section_header("Anomaly Monitor",
                       "Automated checks for unusual records, duplicates and inconsistencies")
        st.info(
            "ℹ️ Anomalies are flagged by rule-based checks. "
            "A flag does NOT imply fraud or misconduct — always investigate before concluding."
        )
        if st.button("🔎 Run Anomaly Detection", type="primary"):
            with st.spinner("Scanning records…"):
                flags = engine.detect_anomalies()
            _display_anomalies(flags)

    # ── TAB 5: MODEL EXPLAINER ─────────────────────────────────────────
    with tabs[4]:
        section_header("Model Explainer",
                       "Feature importance and SHAP explanations for trained models")
        available_models = engine.list_available_models()
        file_models = [m for m in available_models if m.get("file_exists")]

        if not file_models:
            st.info(
                "No model files found on disk. Train a model in **Model Training** "
                "to enable explainability features."
            )
        else:
            model_opts = {m["model_id"]: f"{m['name']} v{m['version']}" for m in file_models}
            sel_model = st.selectbox("Select Model", list(model_opts.keys()),
                                     format_func=lambda i: model_opts[i])
            sel_m_meta = next(m for m in file_models if m["model_id"] == sel_model)

            st.markdown("**Enter feature values (for demonstration):**")
            st.caption(
                "In production this is populated automatically from the prediction pipeline. "
                "Enter sample feature values to demonstrate explanation."
            )
            n_features = st.number_input("Number of Features", 2, 20, 4, step=1)
            features = {}
            feat_cols = st.columns(min(int(n_features), 4))
            for i in range(int(n_features)):
                with feat_cols[i % 4]:
                    name = st.text_input(f"Feature {i+1} name", value=f"feature_{i+1}", key=f"fn_{i}")
                    val  = st.number_input(f"Value {i+1}", value=0.0, key=f"fv_{i}")
                    features[name] = val

            if st.button("🔬 Explain", type="primary"):
                ok, msg = engine.load_model(sel_m_meta["file_path"], sel_model)
                if not ok:
                    st.error(f"Could not load model: {msg}")
                else:
                    exp = engine.explain_prediction(sel_model, features)
                    _display_explanation(exp)

    # ── TAB 6: HAZARDOUS GUIDE ─────────────────────────────────────────
    with tabs[5]:
        section_header("Hazardous Material Reference",
                       "Substances commonly found in e-waste — for awareness only")
        st.error(
            "🚨 **Safety Warning:** This is a reference guide ONLY. "
            "Handling hazardous e-waste requires professional training and compliance "
            "with local regulations. This AI system does NOT provide certified safety instructions."
        )
        import pandas as pd
        haz_rows = []
        for sub, info in HAZARDOUS_REFERENCE.items():
            haz_rows.append({
                "Substance": sub.replace("_"," ").title(),
                "Risk Level": info["risk_level"],
                "Regulation": info["regulation"],
                "Handling Guidance": info["handling"],
            })
        df_haz = pd.DataFrame(haz_rows)
        st.dataframe(df_haz, use_container_width=True)

        # Device lookup
        section_header("Hazardous Substances by Device Type")
        dev_sel = st.selectbox("Device", list(MATERIAL_KNOWLEDGE_BASE.keys()),
                               format_func=lambda x: x.replace("_"," ").title(),
                               key="haz_dev")
        kb = MATERIAL_KNOWLEDGE_BASE[dev_sel]
        for hz in kb.get("hazardous_substances", []):
            ref = HAZARDOUS_REFERENCE.get(hz, {})
            risk = ref.get("risk_level","unknown")
            color = {"high":"error","medium":"warning","low":"info"}.get(risk,"muted")
            sb = status_badge(risk.upper(), color)
            st.markdown(
                f"{sb} **{hz.replace('_',' ').title()}** — {ref.get('handling','Consult specialist')}",
                unsafe_allow_html=True,
            )


# ── Display helpers ────────────────────────────────────────────────────

def _display_recovery_estimate(result: dict):
    import pandas as pd
    total = result.get("total_estimated_value_usd", 0)
    st.success(f"**Est. Total Recovery Value: ${total:,.4f} USD**")
    st.caption(f"Source: {result.get('data_source','—')} · Confidence: {result.get('knowledge_confidence','—')}")
    st.warning(result.get("disclaimer","Estimates only."))

    mats = result.get("recoverable_materials", {})
    rows = []
    for mat, data in mats.items():
        rows.append({
            "Material": mat.replace("_"," ").title(),
            "Composition %": data["composition_pct"],
            "Total Mass (g)": data["total_mass_g"],
            "Recovery Eff. %": data["recovery_efficiency_pct"],
            "Est. Recovered (g)": data["estimated_recovered_g"],
            "Method": data["recovery_method"],
            "Est. Value (USD)": f"${data['estimated_value_usd']:,.4f}",
        })
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        csv = pd.DataFrame(rows).to_csv(index=False).encode()
        st.download_button("⬇️ Download CSV", csv, "recovery_estimate.csv", "text/csv")


def _display_batch_recovery(result: dict):
    if not result.get("available"):
        st.error(result.get("message")); return
    import pandas as pd
    st.success(f"**Est. Batch Recovery Value: ${result['total_estimated_value_usd']:,.2f} USD**")
    st.markdown(f"Batch: **{result.get('batch_number','—')}** · "
                f"Devices: {result.get('device_count',0)} · "
                f"Basis: {result.get('estimation_basis','—')}")
    st.warning(result.get("disclaimer","Estimates only."))
    mats = result.get("recoverable_materials", {})
    if mats:
        rows = [{"Material": k.replace("_"," ").title(),
                 "Est. Recovered (g)": v.get("estimated_recovered_g",0),
                 "Est. Value (USD)": f"${v.get('estimated_value_usd',0):,.2f}"}
                for k, v in mats.items()]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)


def _display_recovery_plan(plan: dict):
    if not plan.get("available"):
        st.error(plan.get("message")); return
    section_header("Recovery Priorities")
    for p in plan.get("recovery_priorities", []):
        st.markdown(
            f"""<div style='background:#1C1C1C;border:1px solid #2D2D2D;border-radius:8px;
            padding:12px 16px;margin-bottom:8px'>
            <span style='color:#C9A84C;font-weight:600'>#{p['priority_rank']} {p['material'].replace('_',' ').title()}</span>
            <span style='color:#9A9A9A;font-size:0.8rem;margin-left:12px'>
            Est. {p['estimated_recovered_g']:.2f} g · ${p['estimated_value_usd']:,.4f}</span>
            <div style='color:#9A9A9A;font-size:0.8rem;margin-top:4px'>{p['reason']}</div>
            </div>""", unsafe_allow_html=True)
    warnings = plan.get("hazardous_warnings", [])
    if warnings:
        st.error(f"⚠️ {len(warnings)} hazardous substance(s) detected — specialist handling required.")
        for w in warnings:
            st.markdown(f"- **{w['substance']}** ({w['risk_level']} risk) in {w['device_type']}: {w['handling']}")


def _display_trends(trends: dict):
    if trends.get("error"):
        st.error(f"Trend computation failed: {trends['error']}"); return
    if not trends.get("data_sufficient"):
        st.warning(f"⚠️ Insufficient data: {trends.get('insufficient_data_note','Not enough records.')}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Batches in Period", trends.get("batches_in_period", 0))
    c2.metric("Weight in Period", f"{trends.get('total_weight_period_kg',0):.1f} kg")
    c3.metric("Recovered in Period", f"{trends.get('total_recovered_period_g',0):.1f} g")
    chg = trends.get("weight_change_pct")
    c4.metric("Volume vs Prior Period",
              f"{chg:+.1f}%" if chg is not None else "N/A",
              delta=f"{chg:+.1f}%" if chg is not None else None)
    st.caption(f"Period: last {trends.get('period_days',30)} days")


def _display_anomalies(flags: list):
    if not flags:
        st.success("✅ No anomalies detected in current records.")
        return
    sev_colors = {"high":"error","medium":"warning","low":"info"}
    st.warning(f"⚠️ {len(flags)} anomaly flag(s) found.")
    for f in flags:
        color = sev_colors.get(f.get("severity","low"), "info")
        sb = status_badge(f.get("severity","low").upper(), color)
        with st.expander(f"{sb} {f['type'].replace('_',' ').title()}", expanded=f.get("severity")=="high"):
            st.markdown(f["detail"])
            st.markdown(f"**Recommended action:** {f.get('action','Review manually.')}")
        st.write("")


def _display_explanation(exp: dict):
    if not exp.get("available"):
        st.warning(exp.get("message")); return
    method = exp.get("method","unknown")
    st.success(f"Explanation method: **{method}**")
    st.caption(exp.get("disclaimer",""))
    importance = exp.get("importance",[])
    if importance:
        import pandas as pd, plotly.graph_objects as go
        names = [str(x[0]) for x in importance]
        vals  = [float(x[1]) for x in importance]
        colors = ["#C9A84C" if v >= 0 else "#E74C3C" for v in vals]
        fig = go.Figure(go.Bar(x=vals, y=names, orientation="h", marker_color=colors))
        fig.update_layout(
            title=f"Feature Importance ({method})",
            paper_bgcolor="#0A0A0A", plot_bgcolor="#141414",
            font=dict(color="#F2F2F2"), height=max(300, len(names)*35),
            xaxis_title="Importance / SHAP Value",
        )
        st.plotly_chart(fig, use_container_width=True)
