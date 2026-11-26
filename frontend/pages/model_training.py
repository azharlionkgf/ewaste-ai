"""
frontend/pages/model_training.py
E-WASTE AI — AI/ML Training Laboratory (Phase 3 - Full UI)
===========================================================
10-Tab training interface:
  1  Dataset Selection
  2  Task & Target Configuration
  3  Algorithm Selection
  4  Training Configuration
  5  Training & Progress
  6  Evaluation Dashboard
  7  Model Comparison
  8  Model Registry
  9  Experiment History
  10 Export
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from frontend.theme import apply_theme, section_header

# ---------------------------------------------------------------------------
# Lazy imports (heavy ML libs loaded only when needed)
# ---------------------------------------------------------------------------

def _get_training_engine():
    from ml.training.training_engine import TrainingEngine
    return TrainingEngine

def _get_sklearn_models():
    from ml.models.tabular.sklearn_models import (
        CLASSIFIER_REGISTRY, REGRESSOR_REGISTRY,
        build_tabular_classifier, build_tabular_regressor,
    )
    return CLASSIFIER_REGISTRY, REGRESSOR_REGISTRY

def _get_evaluator():
    from ml.evaluation.evaluator import evaluate_tabular, compare_models, cross_validate_model
    return evaluate_tabular, compare_models, cross_validate_model

def _get_optimizer():
    from ml.training.optimizer import ModelOptimizer
    return ModelOptimizer

def _get_registry():
    from ml.models.model_version_registry import ModelRegistry
    return ModelRegistry

def _get_exporter():
    from ml.inference.model_exporter import ModelExporter
    return ModelExporter

def _get_tracker():
    from research.experiments.experiment_tracker import ExperimentTracker
    return ExperimentTracker

def _get_pipelines():
    from ewaste.ai_pipelines import EwastePipelineManager
    return EwastePipelineManager

def _get_dataset_service():
    try:
        from backend.services.dataset_service import DatasetService
        return DatasetService()
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------

def _init_state():
    defaults = {
        "ph3_dataset_df": None,
        "ph3_dataset_name": None,
        "ph3_target_col": None,
        "ph3_feature_cols": [],
        "ph3_task": "classification",
        "ph3_algorithm": "random_forest",
        "ph3_config": {},
        "ph3_last_result": None,
        "ph3_training_history": {},  # {run_name: result}
        "ph3_registry_dir": str(PROJECT_ROOT / "models" / "registry"),
        "ph3_experiment_tracker": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _gold(text: str) -> str:
    return f'<span style="color:#C9A84C;font-weight:600">{text}</span>'


# ===========================================================================
# MAIN RENDER
# ===========================================================================

def render():
    apply_theme()
    _init_state()

    st.markdown(
        '<h1 class="page-title">🤖 AI/ML Training Laboratory</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="page-subtitle">Train, evaluate, compare and manage AI models on your e-waste dataset.</p>',
        unsafe_allow_html=True,
    )

    tabs = st.tabs([
        "📂 Dataset",
        "🎯 Task & Target",
        "🧠 Algorithm",
        "⚙️ Config",
        "🚀 Train",
        "📊 Evaluation",
        "🏆 Comparison",
        "💾 Registry",
        "🔬 Experiments",
        "📤 Export",
    ])

    with tabs[0]:  _tab_dataset()
    with tabs[1]:  _tab_task_target()
    with tabs[2]:  _tab_algorithm()
    with tabs[3]:  _tab_config()
    with tabs[4]:  _tab_train()
    with tabs[5]:  _tab_evaluation()
    with tabs[6]:  _tab_comparison()
    with tabs[7]:  _tab_registry()
    with tabs[8]:  _tab_experiments()
    with tabs[9]:  _tab_export()


# ===========================================================================
# TAB 1 — DATASET SELECTION
# ===========================================================================

def _tab_dataset():
    section_header("📂 Dataset Selection", "Select or upload a dataset to train on.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### Upload Dataset")
        uploaded = st.file_uploader(
            "Upload CSV or Excel file",
            type=["csv", "xlsx", "xls"],
            key="ph3_uploader",
        )
        if uploaded:
            try:
                if uploaded.name.endswith(".csv"):
                    df = pd.read_csv(uploaded)
                else:
                    df = pd.read_excel(uploaded)
                st.session_state["ph3_dataset_df"] = df
                st.session_state["ph3_dataset_name"] = uploaded.name
                st.success(f"✅ Loaded **{uploaded.name}** — {len(df):,} rows × {df.shape[1]} columns")
            except Exception as e:
                st.error(f"Failed to read file: {e}")

    with col2:
        st.markdown("#### E-Waste Pipelines")
        try:
            PipelineManager = _get_pipelines()
            manager = PipelineManager()
            for p in manager.list_pipelines():
                task_icon = "🔵" if p["task"] == "classification" else "🟠"
                st.markdown(f"{task_icon} **{p['label']}**")
        except Exception as e:
            st.warning(f"Pipeline info unavailable: {e}")

    # --- Dataset preview ---
    df = st.session_state.get("ph3_dataset_df")
    if df is not None:
        st.divider()
        st.markdown("#### Dataset Preview")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", f"{len(df):,}")
        c2.metric("Columns", df.shape[1])
        c3.metric("Missing", f"{df.isna().sum().sum():,}")
        c4.metric("Duplicates", f"{df.duplicated().sum():,}")

        with st.expander("📋 Column Info", expanded=False):
            info_df = pd.DataFrame({
                "Column": df.columns,
                "Type": [str(df[c].dtype) for c in df.columns],
                "Missing": [df[c].isna().sum() for c in df.columns],
                "Unique": [df[c].nunique() for c in df.columns],
            })
            st.dataframe(info_df, use_container_width=True)

        with st.expander("👁️ Sample Rows", expanded=True):
            st.dataframe(df.head(10), use_container_width=True)

        # --- E-waste pipeline compatibility check ---
        st.divider()
        st.markdown("#### 🔍 E-Waste Pipeline Compatibility")
        try:
            PipelineManager = _get_pipelines()
            manager = PipelineManager()
            results = []
            for p in manager.list_pipelines():
                r = manager.validate_dataset(df, p["pipeline_id"])
                results.append({
                    "Pipeline": p["label"],
                    "Task": p["task"],
                    "Compatible": "✅" if r["compatible"] else "❌",
                    "Target": r["detected_target"] or "—",
                    "Features": len(r["available_features"]),
                    "Issues": "; ".join(r["issues"][:1]) if r["issues"] else "None",
                })
            st.dataframe(pd.DataFrame(results), use_container_width=True)
        except Exception as e:
            st.info(f"Pipeline check skipped: {e}")
    else:
        st.info("👆 Upload a dataset to begin, or proceed to the Task tab to use a synthetic demo dataset.")


# ===========================================================================
# TAB 2 — TASK & TARGET SELECTION
# ===========================================================================

def _tab_task_target():
    section_header("🎯 Task & Target Configuration", "Choose what to predict and from which features.")

    df = st.session_state.get("ph3_dataset_df")

    # --- Synthetic demo dataset option ---
    if df is None:
        if st.button("🎲 Use Synthetic Demo Dataset (200 rows)", type="secondary"):
            from sklearn.datasets import make_classification
            X, y = make_classification(
                n_samples=200, n_features=8, n_informative=5,
                n_classes=3, n_clusters_per_class=1, random_state=42,
            )
            cols = [f"feature_{i}" for i in range(8)]
            df = pd.DataFrame(X, columns=cols)
            df["target"] = y
            # Add e-waste flavor
            cats = ["Laptop", "Mobile", "Monitor"]
            df["device_category"] = [cats[v % 3] for v in y]
            df["weight_kg"] = np.abs(X[:, 0]) * 2 + 0.5
            df["recovery_kg"] = np.abs(X[:, 1]) + 0.1
            st.session_state["ph3_dataset_df"] = df
            st.session_state["ph3_dataset_name"] = "synthetic_demo_200rows.csv"
            st.rerun()
        st.info("No dataset loaded. Upload a dataset in the **📂 Dataset** tab, or use the synthetic demo above.")
        return

    cols = list(df.columns)

    col1, col2 = st.columns(2)
    with col1:
        task = st.selectbox(
            "Task Type",
            ["classification", "regression"],
            index=0 if st.session_state["ph3_task"] == "classification" else 1,
            key="task_select",
        )
        st.session_state["ph3_task"] = task

    with col2:
        default_target = st.session_state.get("ph3_target_col")
        idx = cols.index(default_target) if default_target in cols else len(cols) - 1
        target_col = st.selectbox("Target Column (what to predict)", cols, index=idx)
        st.session_state["ph3_target_col"] = target_col

    # --- Target analysis ---
    st.divider()
    st.markdown(f"#### Target: `{target_col}`")
    target = df[target_col]

    tc1, tc2, tc3 = st.columns(3)
    tc1.metric("Unique Values", target.nunique())
    tc2.metric("Missing", target.isna().sum())
    tc3.metric("Type", str(target.dtype))

    if task == "classification":
        vc = target.value_counts().reset_index()
        vc.columns = ["Class", "Count"]
        vc["Percentage"] = (vc["Count"] / len(df) * 100).round(1)
        st.dataframe(vc.head(20), use_container_width=True)
        if target.nunique() < 2:
            st.error("⚠️ Target has fewer than 2 unique values — classification requires at least 2 classes.")
    else:
        if not np.issubdtype(target.dtype, np.number):
            st.warning("⚠️ Target column is not numeric. Regression requires a numeric target.")
        else:
            tc1, tc2, tc3, tc4 = st.columns(4)
            tc1.metric("Min", f"{target.min():.3f}")
            tc2.metric("Max", f"{target.max():.3f}")
            tc3.metric("Mean", f"{target.mean():.3f}")
            tc4.metric("Std", f"{target.std():.3f}")

    # --- Feature selection ---
    st.divider()
    st.markdown("#### Feature Columns")
    available = [c for c in cols if c != target_col]
    defaults = st.session_state.get("ph3_feature_cols") or available
    defaults = [c for c in defaults if c in available]
    if not defaults:
        defaults = available

    feature_cols = st.multiselect(
        "Select feature columns (all selected by default)",
        available,
        default=defaults,
    )
    st.session_state["ph3_feature_cols"] = feature_cols

    if not feature_cols:
        st.warning("⚠️ No features selected.")
    else:
        st.success(f"✅ {len(feature_cols)} feature columns selected.")

        # Numerical vs categorical breakdown
        num_cols = [c for c in feature_cols if np.issubdtype(df[c].dtype, np.number)]
        cat_cols = [c for c in feature_cols if c not in num_cols]
        st.caption(f"Numerical: {len(num_cols)}  |  Categorical: {len(cat_cols)}")


# ===========================================================================
# TAB 3 — ALGORITHM SELECTION
# ===========================================================================

def _tab_algorithm():
    section_header("🧠 Algorithm Selection", "Choose the ML algorithm for training.")

    task = st.session_state.get("ph3_task", "classification")

    try:
        CLASSIFIER_REGISTRY, REGRESSOR_REGISTRY = _get_sklearn_models()
        registry = CLASSIFIER_REGISTRY if task == "classification" else REGRESSOR_REGISTRY
    except Exception as e:
        st.error(f"Could not load algorithm registry: {e}")
        return

    st.markdown(f"**Task:** {task.capitalize()}   |   **Available algorithms:** {len(registry)}")
    st.divider()

    algo_data = []
    for key, info in registry.items():
        algo_data.append({
            "ID": key,
            "Name": info.get("label", key),
            "Speed": info.get("speed", "Medium"),
            "Interpretable": info.get("interpretable", "—"),
            "Description": info.get("description", ""),
        })
    st.dataframe(pd.DataFrame(algo_data), use_container_width=True, hide_index=True)

    st.divider()
    current = st.session_state.get("ph3_algorithm", "random_forest")
    keys = list(registry.keys())
    idx = keys.index(current) if current in keys else 0

    selected = st.selectbox(
        "Select Algorithm",
        keys,
        index=idx,
        format_func=lambda k: registry[k].get("label", k),
    )
    st.session_state["ph3_algorithm"] = selected

    # Show algorithm details
    info = registry.get(selected, {})
    with st.expander(f"ℹ️ About {info.get('label', selected)}", expanded=True):
        st.markdown(info.get("description", "No description available."))
        if "params" in info:
            st.markdown("**Key Parameters:**")
            for p, desc in info["params"].items():
                st.markdown(f"- `{p}`: {desc}")

    # E-waste pipeline recommendation
    df = st.session_state.get("ph3_dataset_df")
    target = st.session_state.get("ph3_target_col")
    if df is not None and target:
        st.divider()
        st.markdown("#### 🔍 E-Waste Pipeline Recommendations")
        try:
            PipelineManager = _get_pipelines()
            manager = PipelineManager()
            for p in manager.list_pipelines():
                r = manager.validate_dataset(df, p["pipeline_id"])
                if r["compatible"] and r["detected_target"] == target:
                    algos = manager.get_recommended_algorithms(p["pipeline_id"])
                    st.info(
                        f"**{p['label']}** recommends: `{'`, `'.join(algos)}`"
                    )
        except Exception:
            pass


# ===========================================================================
# TAB 4 — TRAINING CONFIGURATION
# ===========================================================================

def _tab_config():
    section_header("⚙️ Training Configuration", "Set hyperparameters and training options.")

    col1, col2 = st.columns(2)

    with col1:
        seed = st.number_input("Random Seed", value=42, min_value=0, max_value=99999, step=1)
        test_size = st.slider("Test Split %", 10, 40, 20) / 100
        val_size = st.slider("Validation Split % (of remaining)", 10, 30, 20) / 100

    with col2:
        run_name = st.text_input(
            "Run Name",
            value=f"{st.session_state.get('ph3_algorithm', 'model')}_{int(time.time()) % 10000}",
        )
        imbalance_strategy = st.selectbox(
            "Class Imbalance Strategy",
            ["none", "oversample", "smote", "class_weight"],
            help="Only applies to classification tasks.",
        )
        enable_cv = st.checkbox("Enable Cross-Validation", value=False)
        cv_folds = st.number_input("CV Folds", value=5, min_value=2, max_value=10, disabled=not enable_cv)

    st.divider()
    st.markdown("#### Hyperparameter Tuning")
    enable_tuning = st.checkbox("Enable Hyperparameter Tuning", value=False)
    if enable_tuning:
        tune_method = st.selectbox("Search Method", ["random", "grid"])
        tune_n_iter = st.number_input("Iterations (Random Search)", value=10, min_value=3, max_value=50)
        tune_cv = st.number_input("Tuning CV Folds", value=3, min_value=2, max_value=5)
    else:
        tune_method = "random"
        tune_n_iter = 10
        tune_cv = 3

    # Persist config
    st.session_state["ph3_config"] = {
        "seed": int(seed),
        "test_size": test_size,
        "val_size": val_size,
        "run_name": run_name,
        "imbalance_strategy": imbalance_strategy,
        "enable_cv": enable_cv,
        "cv_folds": int(cv_folds),
        "enable_tuning": enable_tuning,
        "tune_method": tune_method,
        "tune_n_iter": int(tune_n_iter),
        "tune_cv": int(tune_cv),
    }

    st.info(
        "✅ Configuration saved. Proceed to the **🚀 Train** tab to start training."
    )


# ===========================================================================
# TAB 5 — TRAINING & PROGRESS
# ===========================================================================

def _tab_train():
    section_header("🚀 Train Model", "Execute training with current configuration.")

    df = st.session_state.get("ph3_dataset_df")
    target_col = st.session_state.get("ph3_target_col")
    feature_cols = st.session_state.get("ph3_feature_cols", [])
    task = st.session_state.get("ph3_task", "classification")
    algorithm = st.session_state.get("ph3_algorithm", "random_forest")
    cfg = st.session_state.get("ph3_config", {})

    # --- Validation ---
    ready = True
    if df is None:
        st.error("❌ No dataset loaded. Go to **📂 Dataset** tab.")
        ready = False
    if not target_col:
        st.error("❌ No target column selected. Go to **🎯 Task & Target** tab.")
        ready = False
    if not feature_cols:
        st.error("❌ No feature columns selected. Go to **🎯 Task & Target** tab.")
        ready = False

    if not ready:
        return

    # --- Summary ---
    st.markdown("#### Training Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Algorithm", algorithm)
    c2.metric("Task", task)
    c3.metric("Features", len(feature_cols))
    c4.metric("Rows", len(df))

    st.divider()

    if st.button("🚀 Start Training", type="primary", use_container_width=True):
        _run_training(df, target_col, feature_cols, task, algorithm, cfg)


def _run_training(df, target_col, feature_cols, task, algorithm, cfg):
    """Execute the full training pipeline."""
    seed = cfg.get("seed", 42)
    test_size = cfg.get("test_size", 0.2)
    val_size = cfg.get("val_size", 0.2)
    run_name = cfg.get("run_name", f"{algorithm}_{int(time.time()) % 10000}")
    imbalance_strategy = cfg.get("imbalance_strategy", "none")
    enable_tuning = cfg.get("enable_tuning", False)

    progress = st.progress(0, text="Preparing data...")

    try:
        # --- 1. Prepare data ---
        from sklearn.preprocessing import LabelEncoder, StandardScaler

        df_work = df[feature_cols + [target_col]].dropna(subset=[target_col]).copy()

        # Encode categorical features
        X_parts = []
        for col in feature_cols:
            if col not in df_work.columns:
                continue
            s = df_work[col]
            if np.issubdtype(s.dtype, np.number):
                arr = s.fillna(s.median()).values.astype(float)
            else:
                le = LabelEncoder()
                arr = le.fit_transform(s.fillna("__missing__").astype(str)).astype(float)
            X_parts.append(arr.reshape(-1, 1))

        if not X_parts:
            st.error("No valid features after encoding.")
            return

        X = np.hstack(X_parts)

        y_raw = df_work[target_col]
        class_names = None
        if task == "classification":
            if not np.issubdtype(y_raw.dtype, np.number):
                le_target = LabelEncoder()
                y = le_target.fit_transform(y_raw.astype(str))
                class_names = list(le_target.classes_)
            else:
                y = y_raw.values.astype(int)
                class_names = [str(c) for c in sorted(np.unique(y))]
        else:
            y = y_raw.values.astype(float)

        progress.progress(10, text="Splitting dataset...")

        # --- 2. Split ---
        from sklearn.model_selection import train_test_split
        stratify = y if task == "classification" and len(np.unique(y)) >= 2 else None
        X_tmp, X_test, y_tmp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=seed, stratify=stratify
        )
        stratify2 = y_tmp if task == "classification" and len(np.unique(y_tmp)) >= 2 else None
        X_train, X_val, y_train, y_val = train_test_split(
            X_tmp, y_tmp, test_size=val_size, random_state=seed, stratify=stratify2
        )

        st.caption(f"Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")
        progress.progress(20, text="Handling class imbalance...")

        # --- 3. Imbalance ---
        if task == "classification" and imbalance_strategy != "none":
            try:
                Optimizer = _get_optimizer()
                opt = Optimizer()
                X_train, y_train = opt.handle_class_imbalance(
                    X_train, y_train, strategy=imbalance_strategy, seed=seed
                )
                st.caption(f"After resampling: {len(X_train)} training samples")
            except Exception as e:
                st.warning(f"Imbalance handling skipped: {e}")

        progress.progress(35, text="Hyperparameter tuning..." if cfg.get("enable_tuning") else "Building model...")

        # --- 4. Tune or train ---
        if enable_tuning:
            Optimizer = _get_optimizer()
            opt = Optimizer()
            model, best_params = opt.tune(
                algorithm=algorithm,
                X_train=X_train, y_train=y_train,
                task=task,
                method=cfg.get("tune_method", "random"),
                n_iter=cfg.get("tune_n_iter", 10),
                cv=cfg.get("tune_cv", 3),
                seed=seed,
            )
            st.caption(f"Best params: {best_params}")
        else:
            TrainingEngine = _get_training_engine()
            engine = TrainingEngine(seed=seed)

        progress.progress(50, text="Training model...")

        # --- 5. Train ---
        TrainingEngine = _get_training_engine()
        engine = TrainingEngine(seed=seed)
        result = engine.train_tabular(
            X_train, y_train, X_val, y_val,
            algorithm=algorithm,
            task=task,
            run_name=run_name,
            config={"class_names": class_names},
        )
        if enable_tuning:
            result["best_params"] = best_params

        progress.progress(70, text="Evaluating on test set...")

        # --- 6. Test evaluation ---
        evaluate_tabular, _, _ = _get_evaluator()
        test_metrics = evaluate_tabular(result["model"], X_test, y_test, task=task, split="test")
        result["test_metrics"] = test_metrics
        result["class_names"] = class_names
        result["feature_names"] = feature_cols
        result["target_name"] = target_col

        progress.progress(80, text="Cross-validating...")

        # --- 7. CV (optional) ---
        if cfg.get("enable_cv"):
            _, _, cross_validate_model = _get_evaluator()
            cv_result = cross_validate_model(
                result["model"], X, y, task=task,
                cv=cfg.get("cv_folds", 5), seed=seed,
            )
            result["cv_result"] = cv_result

        progress.progress(90, text="Registering model...")

        # --- 8. Register ---
        Registry = _get_registry()
        registry = Registry(registry_dir=st.session_state["ph3_registry_dir"])
        entry_id = registry.register(
            run_name=run_name,
            model_path=result.get("model_path", ""),
            metadata={
                "algorithm": algorithm,
                "task": task,
                "run_name": run_name,
                "feature_names": feature_cols,
                "target_name": target_col,
                "class_names": class_names,
                "train_metrics": result.get("train_metrics", {}),
                "val_metrics": result.get("val_metrics", {}),
                "test_metrics": test_metrics,
                "duration_sec": result.get("duration_sec", 0),
                "seed": seed,
                "dataset_name": st.session_state.get("ph3_dataset_name", "unknown"),
            }
        )
        result["registry_entry_id"] = entry_id

        # Track experiment
        try:
            Tracker = _get_tracker()
            tracker = Tracker()
            exp_id = tracker.start_experiment(
                name=run_name,
                objective=f"{task} with {algorithm}",
                dataset_info={"name": st.session_state.get("ph3_dataset_name", "unknown"), "n_rows": len(df)},
                config={"algorithm": algorithm, "seed": seed, **cfg},
            )
            tracker.log_metrics(exp_id, {
                **result.get("val_metrics", {}),
                "test_accuracy": test_metrics.get("accuracy"),
            })
            tracker.end_experiment(exp_id, status="completed")
            result["experiment_id"] = exp_id
        except Exception as e:
            st.caption(f"Experiment tracking skipped: {e}")

        progress.progress(100, text="Done!")

        # Store result
        st.session_state["ph3_last_result"] = result
        if "ph3_training_history" not in st.session_state:
            st.session_state["ph3_training_history"] = {}
        st.session_state["ph3_training_history"][run_name] = result

        st.success(f"✅ Training complete! Run: **{run_name}**")
        _show_quick_metrics(result, task)

    except Exception as e:
        progress.empty()
        st.error(f"Training failed: {e}")
        import traceback
        st.code(traceback.format_exc())


def _show_quick_metrics(result: dict, task: str):
    val_m = result.get("val_metrics", {})
    test_m = result.get("test_metrics", {})
    st.markdown("#### Quick Results")
    if task == "classification":
        cols = st.columns(4)
        cols[0].metric("Val Accuracy", f"{val_m.get('accuracy', 0):.4f}")
        cols[1].metric("Val F1 (macro)", f"{val_m.get('f1_macro', 0):.4f}")
        cols[2].metric("Test Accuracy", f"{test_m.get('accuracy', 0):.4f}")
        cols[3].metric("Duration (s)", f"{result.get('duration_sec', 0):.2f}")
    else:
        cols = st.columns(4)
        cols[0].metric("Val MAE", f"{val_m.get('mae', 0):.4f}")
        cols[1].metric("Val R²", f"{val_m.get('r2', 0):.4f}")
        cols[2].metric("Test MAE", f"{test_m.get('mae', 0):.4f}")
        cols[3].metric("Duration (s)", f"{result.get('duration_sec', 0):.2f}")


# ===========================================================================
# TAB 6 — EVALUATION DASHBOARD
# ===========================================================================

def _tab_evaluation():
    section_header("📊 Evaluation Dashboard", "Detailed model evaluation metrics.")

    result = st.session_state.get("ph3_last_result")
    if result is None:
        st.info("No training result yet. Run training in the **🚀 Train** tab.")
        return

    task = result.get("task", "classification")
    run_name = result.get("run_name", "model")

    st.markdown(f"**Run:** `{run_name}` | **Algorithm:** `{result.get('algorithm', '?')}` | **Task:** {task}")

    for split in ["train", "val", "test"]:
        m = result.get(f"{split}_metrics", {})
        if not m:
            continue
        with st.expander(f"📈 {split.capitalize()} Metrics", expanded=(split == "test")):
            if task == "classification":
                metric_cols = st.columns(4)
                metric_cols[0].metric("Accuracy", f"{m.get('accuracy', 0):.4f}")
                metric_cols[1].metric("Precision", f"{m.get('precision', 0):.4f}")
                metric_cols[2].metric("Recall", f"{m.get('recall', 0):.4f}")
                metric_cols[3].metric("F1 (macro)", f"{m.get('f1_macro', 0):.4f}")

                if "kappa" in m:
                    st.caption(f"Cohen's Kappa: {m['kappa']:.4f}")
                if "roc_auc" in m:
                    st.caption(f"ROC-AUC: {m['roc_auc']:.4f}  |  PR-AUC: {m.get('pr_auc', '—')}")

                # Confusion matrix
                cm = m.get("confusion_matrix")
                if cm:
                    try:
                        import plotly.figure_factory as ff
                        class_names = result.get("class_names") or [str(i) for i in range(len(cm))]
                        fig = ff.create_annotated_heatmap(
                            z=cm, x=class_names, y=class_names,
                            colorscale="Blues", showscale=True,
                        )
                        fig.update_layout(
                            title=f"Confusion Matrix ({split})",
                            xaxis_title="Predicted",
                            yaxis_title="Actual",
                            paper_bgcolor="#0A0A0A",
                            plot_bgcolor="#0A0A0A",
                            font=dict(color="#E5E5E5"),
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.caption(f"Confusion matrix plot skipped: {e}")
                        st.write(pd.DataFrame(cm))
            else:
                cols = st.columns(4)
                cols[0].metric("MAE", f"{m.get('mae', 0):.4f}")
                cols[1].metric("MSE", f"{m.get('mse', 0):.4f}")
                cols[2].metric("RMSE", f"{m.get('rmse', 0):.4f}")
                cols[3].metric("R²", f"{m.get('r2', 0):.4f}")
                if "mape" in m:
                    st.caption(f"MAPE: {m['mape']:.2f}%")

    # Feature importance
    model = result.get("model")
    feature_names = result.get("feature_names", [])
    if model is not None and feature_names:
        try:
            from ml.models.tabular.sklearn_models import get_feature_importance
            fi = get_feature_importance(model, feature_names)
            if fi:
                st.divider()
                st.markdown("#### 🔑 Feature Importance")
                fi_df = pd.DataFrame(fi).sort_values("importance", ascending=False)
                try:
                    import plotly.express as px
                    fig = px.bar(
                        fi_df.head(15), x="importance", y="feature", orientation="h",
                        title="Top Feature Importances",
                        color_discrete_sequence=["#C9A84C"],
                    )
                    fig.update_layout(
                        paper_bgcolor="#0A0A0A", plot_bgcolor="#0A0A0A",
                        font=dict(color="#E5E5E5"), yaxis={"autorange": "reversed"},
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    st.dataframe(fi_df, use_container_width=True)
        except Exception:
            pass

    # CV results
    if "cv_result" in result:
        st.divider()
        st.markdown("#### 🔁 Cross-Validation Results")
        cv = result["cv_result"]
        if "cv_scores" in cv:
            scores = cv["cv_scores"]
            c1, c2, c3 = st.columns(3)
            c1.metric("Mean", f"{np.mean(scores):.4f}")
            c2.metric("Std", f"{np.std(scores):.4f}")
            c3.metric("Min", f"{np.min(scores):.4f}")
        st.json(cv)


# ===========================================================================
# TAB 7 — MODEL COMPARISON
# ===========================================================================

def _tab_comparison():
    section_header("🏆 Model Comparison", "Compare multiple training runs side-by-side.")

    history = st.session_state.get("ph3_training_history", {})

    if len(history) < 1:
        st.info("No training runs yet. Train models in the **🚀 Train** tab.")
        return

    task = st.session_state.get("ph3_task", "classification")

    # Build comparison table
    rows = []
    for run_name, r in history.items():
        val_m = r.get("val_metrics", {})
        test_m = r.get("test_metrics", {})
        row = {
            "Run Name": run_name,
            "Algorithm": r.get("algorithm", "?"),
            "Task": r.get("task", task),
            "Duration (s)": round(r.get("duration_sec", 0), 2),
        }
        if task == "classification":
            row["Val Accuracy"] = val_m.get("accuracy", 0)
            row["Val F1 (macro)"] = val_m.get("f1_macro", 0)
            row["Test Accuracy"] = test_m.get("accuracy", 0)
            row["Test F1 (macro)"] = test_m.get("f1_macro", 0)
        else:
            row["Val MAE"] = val_m.get("mae", 0)
            row["Val R²"] = val_m.get("r2", 0)
            row["Test MAE"] = test_m.get("mae", 0)
            row["Test R²"] = test_m.get("r2", 0)
        rows.append(row)

    cmp_df = pd.DataFrame(rows)

    # Sort
    if task == "classification":
        sort_col = "Test Accuracy"
    else:
        sort_col = "Test R²"

    if sort_col in cmp_df.columns:
        cmp_df = cmp_df.sort_values(sort_col, ascending=(task == "regression"))

    st.dataframe(cmp_df, use_container_width=True, hide_index=True)

    # Best model
    if len(cmp_df) > 0:
        best_row = cmp_df.iloc[0]
        st.success(f"🏆 Best model: **{best_row['Run Name']}** ({best_row['Algorithm']})")

    # Bar chart comparison
    if len(cmp_df) > 1:
        try:
            import plotly.express as px
            fig = px.bar(
                cmp_df,
                x="Run Name",
                y=sort_col,
                color="Algorithm",
                title=f"Model Comparison — {sort_col}",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig.update_layout(
                paper_bgcolor="#0A0A0A", plot_bgcolor="#0A0A0A",
                font=dict(color="#E5E5E5"),
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.caption(f"Chart skipped: {e}")

    # Overfitting check
    st.divider()
    st.markdown("#### ⚠️ Overfitting Analysis")
    for run_name, r in history.items():
        val_m = r.get("val_metrics", {})
        train_m = r.get("train_metrics", {})
        if task == "classification":
            train_acc = train_m.get("accuracy", 0)
            val_acc = val_m.get("accuracy", 0)
            gap = train_acc - val_acc
            if gap > 0.15:
                st.warning(f"⚠️ **{run_name}**: Possible overfitting — train={train_acc:.3f}, val={val_acc:.3f} (gap={gap:.3f})")
            elif gap > 0.05:
                st.info(f"ℹ️ **{run_name}**: Slight overfit — train={train_acc:.3f}, val={val_acc:.3f}")
            else:
                st.success(f"✅ **{run_name}**: Good generalization — train={train_acc:.3f}, val={val_acc:.3f}")


# ===========================================================================
# TAB 8 — MODEL REGISTRY
# ===========================================================================

def _tab_registry():
    section_header("💾 Model Registry", "Browse, activate, and manage saved model versions.")

    try:
        Registry = _get_registry()
        registry = Registry(registry_dir=st.session_state["ph3_registry_dir"])
        entries = registry.list_all()
    except Exception as e:
        st.error(f"Registry unavailable: {e}")
        return

    if not entries:
        st.info("No models registered yet. Train a model to see it here.")
        return

    st.metric("Total Registered Models", len(entries))

    df_reg = pd.DataFrame([{
        "ID": e["entry_id"],
        "Run Name": e.get("run_name", "?"),
        "Algorithm": e.get("algorithm", "?"),
        "Task": e.get("task", "?"),
        "Status": e.get("status", "?"),
        "Val Acc": e.get("val_metrics", {}).get("accuracy", "—"),
        "Test Acc": e.get("test_metrics", {}).get("accuracy", "—"),
        "Registered": e.get("registered_at", "?")[:10] if e.get("registered_at") else "?",
    } for e in entries])

    st.dataframe(df_reg, use_container_width=True, hide_index=True)

    # Actions
    st.divider()
    entry_ids = [e["entry_id"] for e in entries]
    selected_id = st.selectbox("Select Model Entry", entry_ids)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Activate", use_container_width=True):
            try:
                registry.activate(selected_id)
                st.success(f"Model {selected_id} activated.")
                st.rerun()
            except Exception as e:
                st.error(str(e))
    with col2:
        if st.button("🗄️ Archive", use_container_width=True):
            try:
                registry.archive(selected_id)
                st.success(f"Model {selected_id} archived.")
                st.rerun()
            except Exception as e:
                st.error(str(e))
    with col3:
        entry = registry.get(selected_id)
        if entry:
            st.download_button(
                "📥 Download Metadata",
                data=json.dumps(entry, indent=2, default=str),
                file_name=f"{selected_id}_metadata.json",
                mime="application/json",
                use_container_width=True,
            )

    # Full entry details
    if entry:
        with st.expander("📋 Full Entry Details"):
            st.json(entry)


# ===========================================================================
# TAB 9 — EXPERIMENT HISTORY
# ===========================================================================

def _tab_experiments():
    section_header("🔬 Research Experiments", "Track and compare research experiments.")

    try:
        Tracker = _get_tracker()
        tracker = Tracker()
        experiments = tracker.list_experiments()
    except Exception as e:
        st.error(f"Experiment tracker unavailable: {e}")
        return

    if not experiments:
        st.info("No experiments recorded yet. Run training to auto-track experiments.")
        return

    st.metric("Total Experiments", len(experiments))

    rows = []
    for exp in experiments:
        metrics = exp.get("metrics", {})
        rows.append({
            "ID": exp.get("experiment_id", "?")[:8],
            "Name": exp.get("name", "?"),
            "Status": exp.get("status", "?"),
            "Accuracy": metrics.get("accuracy", "—"),
            "F1 (macro)": metrics.get("f1_macro", "—"),
            "Duration (s)": exp.get("duration_sec", "—"),
            "Started": str(exp.get("start_time", "?"))[:16],
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Comparison
    if len(experiments) >= 2:
        st.divider()
        st.markdown("#### 📊 Comparison Table")
        try:
            exp_ids = [e.get("experiment_id") for e in experiments]
            table = tracker.generate_comparison_table(exp_ids)
            if table is not None:
                if hasattr(table, "to_string"):
                    st.dataframe(table, use_container_width=True)
                else:
                    st.write(table)
        except Exception as e:
            st.caption(f"Comparison table skipped: {e}")

    # Detailed view
    exp_id_map = {e.get("name", e.get("experiment_id", "?")): e.get("experiment_id") for e in experiments}
    selected_name = st.selectbox("View Experiment Details", list(exp_id_map.keys()))
    selected_exp_id = exp_id_map.get(selected_name)
    if selected_exp_id:
        exp_detail = tracker.get_experiment(selected_exp_id)
        if exp_detail:
            with st.expander("📋 Experiment Details", expanded=True):
                st.json(exp_detail)


# ===========================================================================
# TAB 10 — EXPORT
# ===========================================================================

def _tab_export():
    section_header("📤 Export & Download", "Download model packages, reports, and experiment configs.")

    result = st.session_state.get("ph3_last_result")
    history = st.session_state.get("ph3_training_history", {})

    if not result and not history:
        st.info("No trained models available. Train a model first.")
        return

    # --- Evaluation report download ---
    st.markdown("#### 📄 Evaluation Report")
    if result:
        try:
            Exporter = _get_exporter()
            exporter = Exporter()
            test_m = result.get("test_metrics", {})
            test_m["algorithm"] = result.get("algorithm")
            test_m["task"] = result.get("task", "classification")
            report_md = exporter.generate_eval_report(test_m, run_name=result.get("run_name", "model"))
            st.download_button(
                "📥 Download Evaluation Report (Markdown)",
                data=report_md,
                file_name=f"eval_report_{result.get('run_name', 'model')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Report generation failed: {e}")

    # --- Model metadata download ---
    st.divider()
    st.markdown("#### 💾 Model Metadata")
    if result:
        metadata = {
            "run_name": result.get("run_name"),
            "algorithm": result.get("algorithm"),
            "task": result.get("task"),
            "feature_names": result.get("feature_names"),
            "target_name": result.get("target_name"),
            "class_names": result.get("class_names"),
            "train_metrics": result.get("train_metrics"),
            "val_metrics": result.get("val_metrics"),
            "test_metrics": result.get("test_metrics"),
            "model_path": result.get("model_path"),
            "duration_sec": result.get("duration_sec"),
        }
        st.download_button(
            "📥 Download Model Metadata (JSON)",
            data=json.dumps(metadata, indent=2, default=str),
            file_name=f"metadata_{result.get('run_name', 'model')}.json",
            mime="application/json",
            use_container_width=True,
        )

    # --- All runs comparison ---
    st.divider()
    st.markdown("#### 📊 All Runs Comparison")
    if history:
        rows = []
        for rn, r in history.items():
            val_m = r.get("val_metrics", {})
            test_m = r.get("test_metrics", {})
            rows.append({
                "run_name": rn,
                "algorithm": r.get("algorithm"),
                "task": r.get("task"),
                "val_accuracy": val_m.get("accuracy"),
                "val_f1_macro": val_m.get("f1_macro"),
                "test_accuracy": test_m.get("accuracy"),
                "test_f1_macro": test_m.get("f1_macro"),
                "val_mae": val_m.get("mae"),
                "test_mae": test_m.get("mae"),
                "duration_sec": r.get("duration_sec"),
            })
        csv_data = pd.DataFrame(rows).to_csv(index=False)
        st.download_button(
            "📥 Download All Runs (CSV)",
            data=csv_data,
            file_name="all_training_runs.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # --- Research note ---
    st.divider()
    st.info(
        "📌 **Research Note:** Evaluation metrics are computed on the specific dataset splits used during training. "
        "For peer-reviewed research, always validate on completely independent held-out data "
        "and report confidence intervals where possible. "
        "Quality scores are diagnostic indicators, NOT scientific standards."
    )
