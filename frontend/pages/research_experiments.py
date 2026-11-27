"""
E-Waste AI — Research Experiments Workspace
=============================================
Task 11 of Phase 5.
Browse, compare and manage ML experiments.
Connects to database ResearchExperiment model and ai_model_service.
Synthetic / test data is clearly labelled.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from frontend.theme import apply_theme, page_header, section_header, COLORS

try:
    from backend.database import SessionLocal
    from backend.models.all_models import ResearchExperiment, TrainedModel, ModelEvaluation
    DB_OK = True
except Exception as e:
    DB_OK = False
    DB_ERR = str(e)

try:
    from backend.services.ai_model_service import AIModelService
    AI_OK = True
except Exception:
    AI_OK = False


def _db():
    if not DB_OK:
        return None
    return SessionLocal()


def render_research_experiments():
    apply_theme()
    page_header(
        "Research Experiments",
        "Browse ML experiments, compare model performance, and explore reproducibility",
        "🔬",
    )

    if not DB_OK:
        st.error(f"Database unavailable: {DB_ERR}")
        return

    tabs = st.tabs(["📋 Experiments", "📊 Model Comparison", "🔁 Reproducibility", "📝 New Experiment"])

    # ── TAB 1: EXPERIMENTS ─────────────────────────────────────────────
    with tabs[0]:
        section_header("All Research Experiments")

        db = _db()
        try:
            experiments = db.query(ResearchExperiment).order_by(
                ResearchExperiment.created_at.desc()
            ).all()
        except Exception as ex:
            st.error(f"Could not load experiments: {ex}")
            experiments = []
        finally:
            db.close()

        if not experiments:
            st.info(
                "No research experiments found. "
                "Start a training run from the **Model Training** workspace — "
                "experiments are recorded automatically when models are trained."
            )
        else:
            import pandas as pd
            exp_data = []
            for e in experiments:
                exp_data.append({
                    "ID": e.id,
                    "Name": e.experiment_name or f"Experiment {e.id}",
                    "Task": e.task_type or "—",
                    "Algorithm": e.algorithm or "—",
                    "Status": e.status or "—",
                    "Dataset": e.dataset_name or "—",
                    "Created": str(e.created_at)[:16] if e.created_at else "—",
                })
            df = pd.DataFrame(exp_data)
            st.dataframe(df, use_container_width=True)

            # Detailed view
            exp_names = {e.id: (e.experiment_name or f"Experiment {e.id}") for e in experiments}
            sel_id = st.selectbox("View Experiment Details", list(exp_names.keys()),
                                  format_func=lambda i: exp_names[i])
            sel_exp = next(e for e in experiments if e.id == sel_id)

            with st.expander(f"📋 {exp_names[sel_id]}", expanded=True):
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**Task:** {sel_exp.task_type or '—'}")
                c1.markdown(f"**Algorithm:** {sel_exp.algorithm or '—'}")
                c2.markdown(f"**Status:** {sel_exp.status or '—'}")
                c2.markdown(f"**Dataset:** {sel_exp.dataset_name or '—'}")
                c3.markdown(f"**Random Seed:** {sel_exp.random_seed or '—'}")
                c3.markdown(f"**Created:** {str(sel_exp.created_at)[:16] if sel_exp.created_at else '—'}")

                if sel_exp.hyperparameters:
                    st.markdown("**Hyperparameters:**")
                    try:
                        import json
                        hp = json.loads(sel_exp.hyperparameters) if isinstance(sel_exp.hyperparameters, str) else sel_exp.hyperparameters
                        st.json(hp)
                    except Exception:
                        st.code(str(sel_exp.hyperparameters))

                if sel_exp.metrics:
                    st.markdown("**Metrics:**")
                    try:
                        import json
                        m = json.loads(sel_exp.metrics) if isinstance(sel_exp.metrics, str) else sel_exp.metrics
                        st.json(m)
                    except Exception:
                        st.code(str(sel_exp.metrics))

                if sel_exp.notes:
                    st.markdown(f"**Notes:** {sel_exp.notes}")

    # ── TAB 2: MODEL COMPARISON ────────────────────────────────────────
    with tabs[1]:
        section_header("Model Performance Comparison")

        db2 = _db()
        try:
            models = db2.query(TrainedModel).all()
            evals = db2.query(ModelEvaluation).all()
        except Exception as ex:
            st.error(f"Database error: {ex}")
            models, evals = [], []
        finally:
            db2.close()

        if not models:
            st.info("No trained models found. Train models in the **Model Training** workspace.")
        else:
            import pandas as pd

            eval_map = {e.model_id: e for e in evals}

            comp_data = []
            for m in models:
                ev = eval_map.get(m.id)
                row = {
                    "Model Name": m.model_name or f"Model {m.id}",
                    "Version": m.version or "1.0",
                    "Task": m.task_type or "—",
                    "Algorithm": m.algorithm or "—",
                    "Status": m.status or "—",
                    "Accuracy": f"{ev.accuracy:.4f}" if ev and ev.accuracy else "—",
                    "F1 Score": f"{ev.f1_score:.4f}" if ev and ev.f1_score else "—",
                    "AUC": f"{ev.auc:.4f}" if ev and hasattr(ev, 'auc') and ev.auc else "—",
                    "Train Time (s)": m.training_time_seconds or "—",
                }
                comp_data.append(row)

            df_comp = pd.DataFrame(comp_data)
            st.dataframe(df_comp, use_container_width=True)

            # Best model highlight
            models_with_eval = [(m, eval_map.get(m.id)) for m in models if eval_map.get(m.id)]
            if models_with_eval:
                best = max(models_with_eval, key=lambda x: x[1].accuracy or 0)
                best_m, best_e = best
                st.success(
                    f"🏆 Best Model: **{best_m.model_name}** v{best_m.version} "
                    f"— Accuracy: {best_e.accuracy:.4f}"
                )

    # ── TAB 3: REPRODUCIBILITY ─────────────────────────────────────────
    with tabs[2]:
        section_header("Reproducibility Checklist", "Best practices for reproducible ML experiments")

        st.markdown("""
### Reproducibility Requirements

| Requirement | Description |
|------------|-------------|
| ✅ **Fixed Random Seed** | All experiments record the random seed used |
| ✅ **Dataset Version** | Each experiment links to a specific dataset version |
| ✅ **Algorithm & Hyperparameters** | All HP stored in experiment record |
| ✅ **Environment Info** | Python, library versions recorded at training time |
| ✅ **Evaluation Metrics** | Stored with model, not just reported in logs |
| ✅ **Model Artefacts** | Trained model files saved to `saved_models/` |
| ⚠️ **External Data** | Ensure any external data is versioned and cited |

### How to Reproduce an Experiment
1. Select the experiment in the **Experiments** tab
2. Note the random seed, dataset version, algorithm, and hyperparameters
3. Load the same dataset version from **Dataset Management**
4. Configure the same settings in **Model Training**
5. The model file hash can be compared to verify identical training

### Synthetic vs. Real Data
> ⚠️ **Important:** Any experiment using synthetic or augmented data is clearly labelled.
> Never mix synthetic data results with real-world research without disclosure.
        """)

        if DB_OK:
            db3 = _db()
            try:
                exps = db3.query(ResearchExperiment).all()
            except Exception:
                exps = []
            finally:
                db3.close()

            if exps:
                seeds = [e.random_seed for e in exps if e.random_seed]
                if seeds:
                    st.metric("Experiments with Fixed Seed", f"{len(seeds)} / {len(exps)}")
                else:
                    st.warning("No random seeds recorded — reproducibility may be limited.")

    # ── TAB 4: NEW EXPERIMENT ──────────────────────────────────────────
    with tabs[3]:
        section_header("Log New Experiment", "Manually record an experiment or hypothesis")

        with st.form("new_exp_form"):
            c1, c2 = st.columns(2)
            exp_name = c1.text_input("Experiment Name", placeholder="e.g. ResNet50 vs XGBoost comparison")
            task_type = c2.selectbox("Task Type", [
                "image_classification", "text_classification", "regression",
                "clustering", "object_detection", "other",
            ])
            algorithm = c1.text_input("Algorithm(s)", placeholder="e.g. XGBoost, Random Forest")
            dataset_name = c2.text_input("Dataset Used", placeholder="e.g. ewaste_v2_cleaned")
            random_seed = c1.number_input("Random Seed", value=42, step=1)
            status = c2.selectbox("Status", ["planned", "running", "completed", "failed"])
            hp_text = st.text_area(
                "Hyperparameters (JSON)",
                placeholder='{"n_estimators": 200, "max_depth": 6}',
            )
            notes_e = st.text_area("Notes / Hypothesis")
            sub_exp = st.form_submit_button("Save Experiment", type="primary")

        if sub_exp:
            db4 = _db()
            try:
                import json as _json
                hp = None
                if hp_text.strip():
                    try:
                        hp = _json.dumps(_json.loads(hp_text))
                    except Exception:
                        hp = hp_text
                new_e = ResearchExperiment(
                    experiment_name=exp_name,
                    task_type=task_type,
                    algorithm=algorithm,
                    dataset_name=dataset_name,
                    random_seed=int(random_seed),
                    status=status,
                    hyperparameters=hp,
                    notes=notes_e,
                    created_at=__import__('datetime').datetime.utcnow(),
                )
                db4.add(new_e)
                db4.commit()
                st.success(f"✅ Experiment **{exp_name}** saved.")
                st.rerun()
            except Exception as ex:
                db4.rollback()
                st.error(f"Save failed: {ex}")
            finally:
                db4.close()
