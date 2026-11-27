"""
E-Waste AI — Model Evaluation & Registry (fixed column names)
"""
import os, sys, json as _json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from frontend.theme import apply_theme, page_header, section_header, status_badge

try:
    from backend.database import SessionLocal
    from backend.models.all_models import TrainedModel, ModelEvaluation
    DB_OK = True
except Exception as e:
    DB_OK = False; DB_ERR = str(e)


def _db():
    return SessionLocal() if DB_OK else None


def _get_metric(ev, key):
    """Extract a numeric metric from ModelEvaluation.metrics JSON."""
    if not ev or not ev.metrics:
        return None
    try:
        m = _json.loads(ev.metrics) if isinstance(ev.metrics, str) else ev.metrics
        return m.get(key) or m.get(f"val_{key}") or m.get(f"test_{key}")
    except Exception:
        return None


def render_model_evaluation():
    apply_theme()
    page_header("Model Evaluation & Registry",
                "Compare trained models, inspect metrics and manage the model registry", "📈")

    if not DB_OK:
        st.error(f"Database unavailable: {DB_ERR}"); _show_ref(); return

    db = _db()
    try:
        models = db.query(TrainedModel).order_by(TrainedModel.created_at.desc()).all()
        evals  = db.query(ModelEvaluation).all()
    except Exception as ex:
        st.error(f"Load error: {ex}"); models, evals = [], []
    finally:
        db.close()

    if not models:
        st.info("No trained models found. Go to **Model Training** to train your first model.")
        _show_ref(); return

    eval_map = {e.model_id: e for e in evals}
    tabs = st.tabs(["📊 Comparison", "🔍 Detail", "📋 Metrics Reference"])

    with tabs[0]:
        section_header("Model Performance Comparison")
        import pandas as pd
        rows = []
        for m in models:
            ev = eval_map.get(m.id)
            rows.append({
                "Name": m.name, "Version": m.version, "Task": m.task_type,
                "Algorithm": m.algorithm, "Status": m.status,
                "Accuracy": f"{_get_metric(ev,'accuracy'):.4f}" if _get_metric(ev,'accuracy') else "—",
                "F1": f"{_get_metric(ev,'f1'):.4f}" if _get_metric(ev,'f1') else "—",
                "ROC-AUC": f"{ev.roc_auc:.4f}" if ev and ev.roc_auc else "—",
                "Train s": m.training_duration_sec or "—",
                "Created": str(m.created_at)[:10] if m.created_at else "—",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        best = [(m, eval_map[m.id]) for m in models
                if m.id in eval_map and _get_metric(eval_map[m.id], "accuracy")]
        if best:
            bm, be = max(best, key=lambda x: _get_metric(x[1], "accuracy") or 0)
            st.success(f"🏆 Best: **{bm.name}** v{bm.version} — Accuracy: {_get_metric(be,'accuracy'):.4f}")
        import io
        csv = pd.DataFrame(rows).to_csv(index=False).encode()
        st.download_button("⬇️ CSV", csv, "model_comparison.csv", "text/csv")

    with tabs[1]:
        section_header("Model Detail")
        mmap = {m.id: f"{m.name} v{m.version}" for m in models}
        sel_id = st.selectbox("Select Model", list(mmap.keys()), format_func=lambda i: mmap[i])
        m = next(x for x in models if x.id == sel_id)
        ev = eval_map.get(sel_id)
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**Name:** {m.name}")
        c1.markdown(f"**Version:** {m.version}")
        c1.markdown(f"**Task:** {m.task_type}")
        c2.markdown(f"**Algorithm:** {m.algorithm}")
        c2.markdown(f"**Status:** {m.status}")
        c2.markdown(f"**Train time:** {m.training_duration_sec or '—'} s")
        c3.markdown(f"**Created:** {str(m.created_at)[:16] if m.created_at else '—'}")
        if m.file_path:
            exists = os.path.exists(m.file_path)
            c3.markdown(f"**File:** {'✅' if exists else '❌'} `{m.file_path}`")

        if m.hyperparameters:
            with st.expander("Hyperparameters"):
                try:
                    st.json(_json.loads(m.hyperparameters) if isinstance(m.hyperparameters, str) else m.hyperparameters)
                except Exception:
                    st.code(str(m.hyperparameters))

        if ev:
            section_header("Evaluation Metrics")
            c1m, c2m, c3m, c4m = st.columns(4)
            for col, key in zip([c1m,c2m,c3m,c4m],["accuracy","f1","precision","recall"]):
                val = _get_metric(ev, key)
                col.metric(key.capitalize(), f"{val:.4f}" if val else "N/A")
            if ev.roc_auc:
                st.metric("ROC-AUC", f"{ev.roc_auc:.4f}")
            if ev.class_report:
                with st.expander("Classification Report"):
                    st.code(ev.class_report)
            if ev.confusion_matrix:
                with st.expander("Confusion Matrix"):
                    try:
                        import numpy as np, plotly.figure_factory as ff
                        cm = _json.loads(ev.confusion_matrix) if isinstance(ev.confusion_matrix, str) else ev.confusion_matrix
                        fig = ff.create_annotated_heatmap(np.array(cm), colorscale="Blues", showscale=True)
                        fig.update_layout(paper_bgcolor="#0A0A0A", plot_bgcolor="#141414",
                                          font=dict(color="#F2F2F2"))
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as ex:
                        st.code(str(ev.confusion_matrix))
        else:
            st.info("No evaluation metrics for this model.")

        new_st = st.selectbox("Status", ["active","trained","archived","deprecated"],
                              index=["active","trained","archived","deprecated"].index(m.status or "trained"))
        if st.button("Save Status", type="primary"):
            db2 = _db()
            try:
                r = db2.query(TrainedModel).filter(TrainedModel.id == sel_id).first()
                if r: r.status = new_st; db2.commit(); st.success("Updated."); st.rerun()
            except Exception as ex:
                db2.rollback(); st.error(str(ex))
            finally:
                db2.close()

        if m.file_path and os.path.exists(m.file_path):
            with open(m.file_path, "rb") as f:
                st.download_button(f"⬇️ Download {os.path.basename(m.file_path)}", f.read(),
                                   file_name=os.path.basename(m.file_path))

    with tabs[2]:
        _show_ref()


def _show_ref():
    section_header("Evaluation Metrics Reference")
    c1, c2 = st.columns(2)
    c1.markdown("""
**Classification**
- **Accuracy** — Fraction correct
- **Precision** — TP/(TP+FP)
- **Recall** — TP/(TP+FN)
- **F1** — Harmonic mean of P & R
- **ROC-AUC** — Discrimination ability
    """)
    c2.markdown("""
**Regression**
- **MAE** — Mean Absolute Error
- **RMSE** — Root Mean Squared Error
- **R²** — Variance explained

**Selection Tips**
- Imbalanced classes → F1 / Recall
- Equal classes → Accuracy + ROC-AUC
    """)
