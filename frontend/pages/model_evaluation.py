"""
E-Waste AI — Model Evaluation & Registry
==========================================
Task 6 of Phase 5.
Compare trained models, view metrics, confusion matrices, and manage
the model registry. Uses actual saved evaluation results from DB.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from frontend.theme import apply_theme, page_header, section_header, status_badge, COLORS

try:
    from backend.database import SessionLocal
    from backend.models.all_models import TrainedModel, ModelEvaluation
    DB_OK = True
except Exception as e:
    DB_OK = False
    DB_ERR = str(e)


def _db():
    return SessionLocal() if DB_OK else None


def render_model_evaluation():
    apply_theme()
    page_header(
        "Model Evaluation & Registry",
        "Compare trained models, inspect metrics and manage the model registry",
        "📈",
    )

    if not DB_OK:
        st.error(f"Database unavailable: {DB_ERR}")
        return

    db = _db()
    try:
        models = db.query(TrainedModel).order_by(TrainedModel.created_at.desc()).all()
        evals  = db.query(ModelEvaluation).all()
    except Exception as ex:
        st.error(f"Could not load models: {ex}")
        models, evals = [], []
    finally:
        db.close()

    if not models:
        st.info(
            "No trained models found in the registry. "
            "Go to **Model Training** to train your first model."
        )
        _show_metrics_reference()
        return

    eval_map = {e.model_id: e for e in evals}

    tabs = st.tabs(["📊 Comparison Table", "🔍 Model Detail", "📋 Metrics Reference"])

    # ── TAB 1: COMPARISON TABLE ────────────────────────────────────────
    with tabs[0]:
        section_header("Model Performance Comparison")

        import pandas as pd
        rows = []
        for m in models:
            ev = eval_map.get(m.id)
            sb = status_badge(m.status or "unknown",
                              "success" if m.status == "active" else
                              "warning" if m.status == "trained" else "muted")
            rows.append({
                "Name": m.model_name or f"Model {m.id}",
                "Version": m.version or "1.0",
                "Task": m.task_type or "—",
                "Algorithm": m.algorithm or "—",
                "Status": m.status or "—",
                "Accuracy": f"{ev.accuracy:.4f}" if ev and ev.accuracy else "—",
                "F1 Score": f"{ev.f1_score:.4f}" if ev and ev.f1_score else "—",
                "Precision": f"{ev.precision:.4f}" if ev and hasattr(ev, 'precision') and ev.precision else "—",
                "Recall": f"{ev.recall:.4f}" if ev and hasattr(ev, 'recall') and ev.recall else "—",
                "Train Time (s)": m.training_time_seconds or "—",
                "Created": str(m.created_at)[:10] if m.created_at else "—",
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)

        # Highlight best
        models_with_acc = [(m, eval_map[m.id]) for m in models if m.id in eval_map and eval_map[m.id].accuracy]
        if models_with_acc:
            best_m, best_e = max(models_with_acc, key=lambda x: x[1].accuracy or 0)
            st.success(
                f"🏆 Best Model: **{best_m.model_name}** v{best_m.version} "
                f"— Accuracy: {best_e.accuracy:.4f}"
            )

        # CSV download
        csv = df.to_csv(index=False).encode()
        st.download_button("⬇️ Download Comparison CSV", csv,
                           file_name="model_comparison.csv", mime="text/csv")

    # ── TAB 2: MODEL DETAIL ────────────────────────────────────────────
    with tabs[1]:
        section_header("Model Detail View")

        model_names = {m.id: f"{m.model_name or 'Model'} v{m.version}" for m in models}
        sel_id = st.selectbox("Select Model", list(model_names.keys()),
                              format_func=lambda i: model_names[i])
        sel_m = next(m for m in models if m.id == sel_id)
        sel_e = eval_map.get(sel_id)

        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**Name:** {sel_m.model_name}")
        c1.markdown(f"**Version:** {sel_m.version}")
        c1.markdown(f"**Task:** {sel_m.task_type}")
        c2.markdown(f"**Algorithm:** {sel_m.algorithm}")
        c2.markdown(f"**Status:** {sel_m.status}")
        c2.markdown(f"**Train Time:** {sel_m.training_time_seconds or '—'} s")
        c3.markdown(f"**Created:** {str(sel_m.created_at)[:16] if sel_m.created_at else '—'}")
        if sel_m.model_path:
            exists = os.path.exists(sel_m.model_path)
            c3.markdown(f"**File:** {'✅ Found' if exists else '❌ Missing'}")
            c3.markdown(f"`{sel_m.model_path}`")

        if sel_m.hyperparameters:
            with st.expander("Hyperparameters"):
                try:
                    import json
                    hp = json.loads(sel_m.hyperparameters) if isinstance(sel_m.hyperparameters, str) else sel_m.hyperparameters
                    st.json(hp)
                except Exception:
                    st.code(str(sel_m.hyperparameters))

        # Evaluation metrics
        if sel_e:
            section_header("Evaluation Metrics")
            metric_cols = st.columns(4)
            for idx, (label, attr) in enumerate([
                ("Accuracy", "accuracy"), ("F1 Score", "f1_score"),
                ("Precision", "precision"), ("Recall", "recall"),
            ]):
                val = getattr(sel_e, attr, None)
                metric_cols[idx].metric(label, f"{val:.4f}" if val else "N/A")

            # Confusion matrix if available
            if hasattr(sel_e, 'confusion_matrix') and sel_e.confusion_matrix:
                with st.expander("Confusion Matrix"):
                    try:
                        import json, numpy as np, plotly.figure_factory as ff
                        cm = json.loads(sel_e.confusion_matrix) if isinstance(sel_e.confusion_matrix, str) else sel_e.confusion_matrix
                        cm_arr = np.array(cm)
                        fig = ff.create_annotated_heatmap(
                            cm_arr, colorscale="Blues",
                            showscale=True,
                        )
                        fig.update_layout(
                            paper_bgcolor="#0A0A0A", plot_bgcolor="#141414",
                            font=dict(color="#F2F2F2"),
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as ex:
                        st.code(str(sel_e.confusion_matrix))

            # Classification report
            if hasattr(sel_e, 'classification_report') and sel_e.classification_report:
                with st.expander("Classification Report"):
                    st.code(sel_e.classification_report)
        else:
            st.info("No evaluation metrics recorded for this model. Run an evaluation to populate metrics.")

        # Status toggle
        section_header("Model Status")
        new_status = st.selectbox(
            "Update Status",
            ["active", "trained", "archived", "deprecated"],
            index=["active","trained","archived","deprecated"].index(sel_m.status or "trained"),
        )
        if st.button("Save Status", type="primary"):
            db2 = _db()
            try:
                rec = db2.query(TrainedModel).filter(TrainedModel.id == sel_id).first()
                if rec:
                    rec.status = new_status
                    import datetime
                    rec.updated_at = datetime.datetime.utcnow()
                    db2.commit()
                    st.success(f"Model status updated to: {new_status}")
                    st.rerun()
            except Exception as ex:
                db2.rollback()
                st.error(f"Update failed: {ex}")
            finally:
                db2.close()

        # Model file download
        if sel_m.model_path and os.path.exists(sel_m.model_path):
            with open(sel_m.model_path, "rb") as f:
                model_bytes = f.read()
            fname = os.path.basename(sel_m.model_path)
            st.download_button(
                f"⬇️ Download Model File ({fname})",
                model_bytes,
                file_name=fname,
            )

    # ── TAB 3: METRICS REFERENCE ───────────────────────────────────────
    with tabs[2]:
        _show_metrics_reference()


def _show_metrics_reference():
    section_header("Evaluation Metrics Reference")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**Classification Metrics**
- **Accuracy** — Fraction of correct predictions
- **Precision** — TP / (TP + FP) — reduces false positives
- **Recall** — TP / (TP + FN) — reduces false negatives
- **F1 Score** — Harmonic mean of Precision and Recall
- **ROC-AUC** — Area under ROC curve (discrimination ability)
- **Confusion Matrix** — Actual vs. predicted class breakdown
        """)
    with col2:
        st.markdown("""
**Regression Metrics**
- **MAE** — Mean Absolute Error (average prediction error)
- **MSE** — Mean Squared Error (penalises large errors)
- **RMSE** — Root MSE (same unit as target)
- **R² Score** — Proportion of variance explained (1.0 = perfect)
- **MAPE** — Mean Absolute Percentage Error

**Model Selection Tips**
- For imbalanced classes → prioritise F1 / Recall
- For equal class importance → use Accuracy + ROC-AUC
- Prefer Recall when false negatives are costly
        """)
