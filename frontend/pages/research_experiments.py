"""
E-Waste AI — Research Experiments (fixed column names for ResearchExperiment)
"""
import os, sys, json as _json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from datetime import datetime
from frontend.theme import apply_theme, page_header, section_header

try:
    from backend.database import SessionLocal
    from backend.models.all_models import ResearchExperiment, TrainedModel, ModelEvaluation
    DB_OK = True
except Exception as e:
    DB_OK = False; DB_ERR = str(e)


def _db():
    return SessionLocal() if DB_OK else None


def _get_metric(ev, key):
    if not ev or not ev.metrics:
        return None
    try:
        m = _json.loads(ev.metrics) if isinstance(ev.metrics, str) else ev.metrics
        return m.get(key) or m.get(f"val_{key}") or m.get(f"test_{key}")
    except Exception:
        return None


def render_research_experiments():
    apply_theme()
    page_header("Research Experiments",
                "Browse ML experiments, compare model performance, and explore reproducibility", "🔬")

    if not DB_OK:
        st.error(f"Database unavailable: {DB_ERR}"); return

    tabs = st.tabs(["📋 Experiments", "📊 Model Comparison", "🔁 Reproducibility", "📝 New Experiment"])

    with tabs[0]:
        section_header("All Research Experiments")
        db = _db()
        try:
            exps = db.query(ResearchExperiment).order_by(ResearchExperiment.created_at.desc()).all()
        except Exception as ex:
            st.error(str(ex)); exps = []
        finally:
            db.close()

        if not exps:
            st.info("No experiments yet. Train a model in **Model Training** — experiments are recorded automatically.")
        else:
            import pandas as pd
            rows = [{"Name": e.experiment_name, "Architecture": e.model_architecture or "—",
                     "Status": e.status, "Dataset": e.dataset_id or "—",
                     "Seed": e.random_seed, "Duration s": e.duration_sec,
                     "Created": str(e.created_at)[:16] if e.created_at else "—"} for e in exps]
            st.dataframe(pd.DataFrame(rows), use_container_width=True)

            emap = {e.id: e.experiment_name for e in exps}
            sel = st.selectbox("View Detail", list(emap.keys()), format_func=lambda i: emap[i])
            e = next(x for x in exps if x.id == sel)
            with st.expander(f"📋 {e.experiment_name}", expanded=True):
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**Architecture:** {e.model_architecture or '—'}")
                c1.markdown(f"**Status:** {e.status or '—'}")
                c2.markdown(f"**Dataset:** {e.dataset_id or '—'} v{e.dataset_version or '—'}")
                c2.markdown(f"**Seed:** {e.random_seed or '—'}")
                c3.markdown(f"**Duration:** {e.duration_sec or '—'} s")
                c3.markdown(f"**Eval Protocol:** {e.evaluation_protocol or '—'}")
                if e.hyperparameters:
                    with st.expander("Hyperparameters"):
                        try:
                            st.json(_json.loads(e.hyperparameters) if isinstance(e.hyperparameters, str) else e.hyperparameters)
                        except Exception:
                            st.code(str(e.hyperparameters))
                if e.metrics:
                    with st.expander("Metrics"):
                        try:
                            st.json(_json.loads(e.metrics) if isinstance(e.metrics, str) else e.metrics)
                        except Exception:
                            st.code(str(e.metrics))
                if e.notes:
                    st.markdown(f"**Notes:** {e.notes}")

    with tabs[1]:
        section_header("Model Performance Comparison")
        db2 = _db()
        try:
            models = db2.query(TrainedModel).all()
            evals = db2.query(ModelEvaluation).all()
        except Exception as ex:
            st.error(str(ex)); models, evals = [], []
        finally:
            db2.close()

        if not models:
            st.info("No trained models. Use **Model Training**.")
        else:
            import pandas as pd
            eval_map = {e.model_id: e for e in evals}
            rows = []
            for m in models:
                ev = eval_map.get(m.id)
                rows.append({"Name": m.name, "v": m.version, "Task": m.task_type,
                              "Algo": m.algorithm, "Status": m.status,
                              "Accuracy": _get_metric(ev,"accuracy"),
                              "F1": _get_metric(ev,"f1"),
                              "Train s": m.training_duration_sec})
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
            best = [(m, eval_map[m.id]) for m in models
                    if m.id in eval_map and _get_metric(eval_map[m.id],"accuracy")]
            if best:
                bm, be = max(best, key=lambda x: _get_metric(x[1],"accuracy") or 0)
                st.success(f"🏆 Best: **{bm.name}** — Accuracy: {_get_metric(be,'accuracy'):.4f}")

    with tabs[2]:
        section_header("Reproducibility Checklist")
        st.markdown("""
| Requirement | Description |
|------------|-------------|
| ✅ Fixed Random Seed | Stored in experiment record |
| ✅ Dataset Version | Linked to dataset_id + version |
| ✅ Hyperparameters | Stored as JSON in experiment |
| ✅ Evaluation Protocol | Recorded per experiment |
| ✅ Model Artefacts | Saved to saved_models/ |
| ⚠️ Library Versions | Stored if recorded at training time |

> ⚠️ **Synthetic data** experiments are labelled — never mix with real research without disclosure.
        """)

    with tabs[3]:
        section_header("Log New Experiment")
        with st.form("new_exp"):
            c1, c2 = st.columns(2)
            name   = c1.text_input("Experiment Name")
            arch   = c2.text_input("Model Architecture", placeholder="e.g. RandomForest, XGBoost")
            ds_id  = c1.text_input("Dataset ID / Name")
            ds_ver = c2.text_input("Dataset Version")
            seed   = c1.number_input("Random Seed", value=42, step=1)
            status = c2.selectbox("Status", ["planned","running","completed","failed"])
            protocol = c1.text_input("Evaluation Protocol", placeholder="e.g. 5-fold CV")
            duration = c2.number_input("Duration (s)", min_value=0.0, step=0.1)
            hp_text = st.text_area("Hyperparameters (JSON)", placeholder='{"n_estimators": 200}')
            notes_e = st.text_area("Notes / Objective")
            sub = st.form_submit_button("Save Experiment", type="primary")
        if sub:
            db3 = _db()
            try:
                hp = None
                if hp_text.strip():
                    try: hp = _json.dumps(_json.loads(hp_text))
                    except: hp = hp_text
                e = ResearchExperiment(
                    experiment_name=name or "Unnamed",
                    model_architecture=arch,
                    dataset_id=ds_id or None,
                    dataset_version=ds_ver or None,
                    random_seed=int(seed),
                    status=status,
                    evaluation_protocol=protocol,
                    duration_sec=float(duration),
                    hyperparameters=hp,
                    notes=notes_e,
                    created_at=datetime.utcnow(),
                )
                db3.add(e); db3.commit()
                st.success(f"✅ Experiment '{name}' saved."); st.rerun()
            except Exception as ex:
                db3.rollback(); st.error(str(ex))
            finally:
                db3.close()
