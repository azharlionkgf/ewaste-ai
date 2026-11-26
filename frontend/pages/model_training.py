"""
frontend/pages/model_training.py
E-WASTE AI - Model Training & Evaluation Page
Train, evaluate and manage ML models.
"""

import streamlit as st
import pandas as pd
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from frontend.theme import apply_theme, section_header


def render():
    apply_theme()
    st.markdown('<h1 class="page-title">🤖 Model Training</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Train, evaluate and compare AI models on your e-waste dataset.</p>',
        unsafe_allow_html=True
    )

    tabs = st.tabs(["🎯 Configure & Train", "📈 Evaluation Results", "🏆 Model Comparison", "💾 Saved Models"])

    with tabs[0]:
        _tab_train()
    with tabs[1]:
        _tab_evaluation()
    with tabs[2]:
        _tab_comparison()
    with tabs[3]:
        _tab_saved_models()


# ============================================================
# TAB 1 — CONFIGURE & TRAIN
# ============================================================
def _tab_train():
    section_header("Configure & Train Model", "Select algorithm, set hyperparameters, train.")

    # Check if preprocessed data is ready
    X_train = st.session_state.get("X_train")
    X_val = st.session_state.get("X_val")
    y_train = st.session_state.get("y_train")
    y_val = st.session_state.get("y_val")
    num_classes = st.session_state.get("num_classes", 0)

    has_tabular = X_train is not None
    has_images = st.session_state.get("current_image_dataset_path") is not None

    if not has_tabular and not has_images:
        st.warning("""
        **No preprocessed data available.**
        
        Please complete the following steps first:
        1. 📊 Go to **Dataset Management** → Upload a dataset
        2. 🔍 Inspect and clean it
        3. ⚙️ Run Preprocessing
        
        Then come back here to train a model.
        """)
        return

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### Model Type")
        model_category = st.radio(
            "Category",
            ["Tabular (CSV/Excel/JSON)", "Image (CNN)"],
            key="training_model_category",
            disabled=not has_tabular and has_images
        )

    with col2:
        st.markdown("#### Algorithm")
        if "Tabular" in model_category:
            algorithm = st.selectbox(
                "Algorithm",
                ["random_forest", "xgboost", "catboost", "svm", "logistic_regression"],
                key="training_algorithm"
            )
        else:
            algorithm = st.selectbox(
                "Architecture",
                ["mobilenet_v3_small", "mobilenet_v3_large", "efficientnet_b0", "resnet50"],
                key="training_cnn_arch"
            )

    model_name = st.text_input(
        "Model Name (for saving)",
        value=f"ewaste_{algorithm}",
        key="training_model_name"
    )

    st.markdown("---")
    st.markdown("#### Hyperparameters")

    if "Tabular" in model_category:
        hyperparams = _tabular_hyperparams(algorithm)
    else:
        hyperparams = _cnn_hyperparams()

    st.markdown("---")

    col1, col2 = st.columns([1, 3])
    with col1:
        train_btn = st.button("🚀 Start Training", type="primary", key="btn_start_training", use_container_width=True)
    with col2:
        if has_tabular:
            st.info(f"**Train:** {X_train.shape[0]} samples | **Val:** {X_val.shape[0]} samples | **Classes:** {num_classes}")

    if train_btn:
        if "Tabular" in model_category:
            _run_tabular_training(algorithm, model_name, hyperparams, X_train, X_val, y_train, y_val, num_classes)
        else:
            _run_cnn_training(algorithm, model_name, hyperparams)


def _tabular_hyperparams(algorithm: str) -> dict:
    params = {}
    col1, col2, col3 = st.columns(3)

    if algorithm == "random_forest":
        with col1: params["n_estimators"] = st.number_input("N Estimators", 50, 500, 100, step=50, key="rf_n_est")
        with col2: params["max_depth"] = st.number_input("Max Depth (0=None)", 0, 50, 0, key="rf_max_depth")
        with col3: params["random_state"] = st.number_input("Random State", 0, 999, 42, key="rf_seed")
        if params["max_depth"] == 0:
            params["max_depth"] = None

    elif algorithm == "xgboost":
        with col1: params["n_estimators"] = st.number_input("N Estimators", 50, 1000, 200, step=50, key="xgb_n_est")
        with col2: params["learning_rate"] = st.number_input("Learning Rate", 0.001, 0.5, 0.1, step=0.01, format="%.3f", key="xgb_lr")
        with col3: params["max_depth"] = st.number_input("Max Depth", 2, 15, 6, key="xgb_max_depth")
        params["random_state"] = 42

    elif algorithm == "catboost":
        with col1: params["iterations"] = st.number_input("Iterations", 100, 2000, 500, step=100, key="cb_iter")
        with col2: params["learning_rate"] = st.number_input("Learning Rate", 0.01, 0.5, 0.05, step=0.01, format="%.2f", key="cb_lr")
        with col3: params["depth"] = st.number_input("Depth", 2, 12, 6, key="cb_depth")
        params["random_seed"] = 42
        params["verbose"] = 0

    elif algorithm == "svm":
        with col1: params["C"] = st.number_input("C (Regularisation)", 0.01, 100.0, 1.0, step=0.1, format="%.2f", key="svm_c")
        with col2: params["kernel"] = st.selectbox("Kernel", ["rbf", "linear", "poly"], key="svm_kernel")
        with col3: params["probability"] = True

    else:  # logistic regression
        with col1: params["C"] = st.number_input("C (Regularisation)", 0.01, 100.0, 1.0, format="%.2f", key="lr_c")
        with col2: params["max_iter"] = st.number_input("Max Iterations", 100, 5000, 1000, step=100, key="lr_max_iter")
        with col3: params["random_state"] = 42
        params["class_weight"] = "balanced"

    return params


def _cnn_hyperparams() -> dict:
    params = {}
    col1, col2, col3 = st.columns(3)
    with col1: params["epochs"] = st.number_input("Epochs", 1, 100, 20, key="cnn_epochs")
    with col2: params["lr"] = st.number_input("Learning Rate", 0.0001, 0.01, 0.001, step=0.0001, format="%.4f", key="cnn_lr")
    with col3: params["batch_size"] = st.selectbox("Batch Size", [8, 16, 32, 64], index=2, key="cnn_batch")
    col4, col5 = st.columns(2)
    with col4: params["patience"] = st.number_input("Early Stopping Patience", 1, 20, 5, key="cnn_patience")
    with col5: params["freeze_backbone"] = st.checkbox("Freeze Backbone (faster, less data)", value=True, key="cnn_freeze")
    return params


def _run_tabular_training(algorithm, model_name, hyperparams, X_train, X_val, y_train, y_val, num_classes):
    try:
        from ml.training.trainer import ModelTrainer

        progress_bar = st.progress(0, text="Initialising training...")
        status_area = st.empty()

        with st.spinner(f"Training {algorithm}..."):
            trainer = ModelTrainer(
                model_type="tabular",
                model_name=model_name,
                num_classes=num_classes,
                device="cpu"
            )
            progress_bar.progress(20, text="Building model...")
            history = trainer.train_tabular(X_train, y_train, X_val, y_val, **hyperparams)
            progress_bar.progress(80, text="Evaluating on validation set...")

            save_dir = str(PROJECT_ROOT / "saved_models")
            save_path = trainer.save_model(save_dir)
            progress_bar.progress(100, text="Done!")

        st.session_state["last_training_history"] = history
        st.session_state["last_model_path"] = save_path
        st.session_state["last_trainer"] = trainer

        st.success(f"✅ **{algorithm}** trained successfully! Best val accuracy: **{history.get('best_val_accuracy', 0):.4f}**")
        st.info(f"Model saved to: `{save_path}`")
        st.info("👉 Switch to the **Evaluation Results** tab to see detailed metrics.")

    except Exception as e:
        st.error(f"❌ Training failed: {e}")
        import traceback
        st.code(traceback.format_exc())


def _run_cnn_training(architecture, model_name, hyperparams):
    image_path = st.session_state.get("current_image_dataset_path")
    if not image_path:
        st.error("No image dataset loaded. Upload one in Dataset Management.")
        return
    try:
        from ml.data.loaders.image_dataset import EwasteImageDataset
        from ml.models.cnn.classifier import get_imagenet_transforms
        from ml.training.trainer import ModelTrainer
        from torch.utils.data import DataLoader

        progress_bar = st.progress(0, text="Loading image dataset...")
        transform_train, transform_val = get_imagenet_transforms(augment=True)
        transform_val_only, _ = get_imagenet_transforms(augment=False)

        dataset = EwasteImageDataset.from_directory(image_path, transform=transform_train)
        num_classes = len(dataset.get_class_names())

        # Simple 80/20 split for CNN
        from torch.utils.data import random_split
        import torch
        n_val = max(1, int(0.2 * len(dataset)))
        n_train = len(dataset) - n_val
        train_ds, val_ds = random_split(dataset, [n_train, n_val], generator=torch.Generator().manual_seed(42))

        train_loader = DataLoader(train_ds, batch_size=hyperparams["batch_size"], shuffle=True, num_workers=0)
        val_loader = DataLoader(val_ds, batch_size=hyperparams["batch_size"], shuffle=False, num_workers=0)

        progress_bar.progress(20, text=f"Training {architecture}... (this may take several minutes on CPU)")

        trainer = ModelTrainer(
            model_type="cnn",
            model_name=model_name,
            num_classes=num_classes,
            device="cpu"
        )
        history = trainer.train_cnn(
            train_loader, val_loader,
            epochs=hyperparams["epochs"],
            lr=hyperparams["lr"],
            patience=hyperparams["patience"],
        )
        progress_bar.progress(90, text="Saving model...")
        save_path = trainer.save_model(str(PROJECT_ROOT / "saved_models"))
        progress_bar.progress(100, text="Done!")

        st.session_state["last_training_history"] = history
        st.session_state["last_model_path"] = save_path
        st.session_state["last_trainer"] = trainer

        st.success(f"✅ **{architecture}** trained! Best val accuracy: **{history.get('best_val_accuracy', 0):.4f}**")

    except Exception as e:
        st.error(f"❌ CNN training failed: {e}")
        import traceback
        st.code(traceback.format_exc())


# ============================================================
# TAB 2 — EVALUATION
# ============================================================
def _tab_evaluation():
    section_header("Evaluation Results", "Detailed metrics on the test set.")

    history = st.session_state.get("last_training_history")
    trainer = st.session_state.get("last_trainer")

    if history is None:
        st.info("No training results yet. Train a model in the **Configure & Train** tab.")
        return

    # Training summary
    st.markdown("### Training Summary")
    cols = st.columns(4)
    with cols[0]: st.metric("Best Val Accuracy", f"{history.get('best_val_accuracy', 0):.4f}")
    with cols[1]: st.metric("Epochs Run", history.get("epochs_run", "—"))
    with cols[2]: st.metric("Model Type", history.get("model_type", "—"))
    with cols[3]: st.metric("Classes", history.get("num_classes", "—"))

    # Training history chart for CNN
    if "train_loss" in history and history["train_loss"]:
        st.markdown("### Training History")
        hist_df = pd.DataFrame({
            "Train Loss": history.get("train_loss", []),
            "Val Loss": history.get("val_loss", []),
        })
        st.line_chart(hist_df, use_container_width=True)

        if "train_acc" in history:
            acc_df = pd.DataFrame({
                "Train Accuracy": history.get("train_acc", []),
                "Val Accuracy": history.get("val_acc", []),
            })
            st.line_chart(acc_df, use_container_width=True)

    # Evaluate on test set
    X_test = st.session_state.get("X_test")
    y_test = st.session_state.get("y_test")

    if X_test is not None and y_test is not None and trainer is not None:
        st.markdown("---")
        st.markdown("### Test Set Evaluation")

        if st.button("🔬 Evaluate on Test Set", key="btn_eval_test"):
            _run_test_evaluation(trainer, X_test, y_test)

    if "test_eval_result" in st.session_state:
        _show_evaluation_metrics(st.session_state["test_eval_result"])


def _run_test_evaluation(trainer, X_test, y_test):
    try:
        from ml.evaluation.metrics import compute_classification_metrics
        import numpy as np

        with st.spinner("Evaluating on test set..."):
            model = trainer._model
            if hasattr(model, "predict"):
                y_pred = model.predict(X_test)
                y_proba = model.predict_proba(X_test) if hasattr(model, "predict_proba") else None
            else:
                y_pred = np.zeros(len(y_test), dtype=int)
                y_proba = None

            metrics = compute_classification_metrics(y_test, y_pred, y_proba)

        st.session_state["test_eval_result"] = metrics
        st.success("✅ Evaluation complete!")

    except Exception as e:
        st.error(f"Evaluation failed: {e}")
        import traceback
        st.code(traceback.format_exc())


def _show_evaluation_metrics(metrics: dict):
    st.markdown("#### Classification Metrics")
    cols = st.columns(4)
    with cols[0]: st.metric("Accuracy", f"{metrics.get('accuracy', 0):.4f}")
    with cols[1]: st.metric("F1 (Macro)", f"{metrics.get('f1_macro', 0):.4f}")
    with cols[2]: st.metric("Precision", f"{metrics.get('precision_macro', 0):.4f}")
    with cols[3]: st.metric("Recall", f"{metrics.get('recall_macro', 0):.4f}")

    if "confusion_matrix_fig" in metrics:
        st.markdown("#### Confusion Matrix")
        st.pyplot(metrics["confusion_matrix_fig"])

    if "classification_report" in metrics:
        st.markdown("#### Per-Class Report")
        report = metrics["classification_report"]
        if isinstance(report, dict):
            report_df = pd.DataFrame(report).T
            st.dataframe(report_df.round(4), use_container_width=True)


# ============================================================
# TAB 3 — MODEL COMPARISON
# ============================================================
def _tab_comparison():
    section_header("Model Comparison", "Compare all saved models side by side.")

    saved_models_dir = PROJECT_ROOT / "saved_models"
    models = []

    if saved_models_dir.exists():
        for model_dir in saved_models_dir.iterdir():
            if model_dir.is_dir():
                meta_file = model_dir / "metadata.json"
                if meta_file.exists():
                    try:
                        with open(meta_file) as f:
                            meta = json.load(f)
                        models.append(meta)
                    except Exception:
                        pass

    if not models:
        st.info("No trained models saved yet. Train models in the **Configure & Train** tab.")
        return

    df = pd.DataFrame(models)
    display_cols = ["model_name", "model_type", "num_classes", "best_val_accuracy", "epochs_run", "training_date"]
    display_cols = [c for c in display_cols if c in df.columns]

    st.dataframe(df[display_cols].sort_values("best_val_accuracy", ascending=False), use_container_width=True)

    st.markdown("#### Select Model for Deployment")
    model_names = [m.get("model_name", "unknown") for m in models]
    selected = st.selectbox("Select Model", model_names, key="compare_select_model")
    if st.button("✅ Set as Active Model", key="btn_set_active"):
        st.session_state["active_model_name"] = selected
        st.success(f"Active model set to: **{selected}**")


# ============================================================
# TAB 4 — SAVED MODELS
# ============================================================
def _tab_saved_models():
    section_header("Saved Models", "Browse and load trained models.")

    saved_models_dir = PROJECT_ROOT / "saved_models"

    if not saved_models_dir.exists() or not any(saved_models_dir.iterdir()):
        st.info("No models saved yet.")
        return

    for model_dir in sorted(saved_models_dir.iterdir()):
        if not model_dir.is_dir():
            continue
        meta_file = model_dir / "metadata.json"
        meta = {}
        if meta_file.exists():
            try:
                with open(meta_file) as f:
                    meta = json.load(f)
            except Exception:
                pass

        with st.expander(f"🤖 {model_dir.name}", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Type:** {meta.get('model_type', '—')}")
                st.markdown(f"**Algorithm:** {meta.get('model_name', model_dir.name)}")
            with col2:
                st.markdown(f"**Classes:** {meta.get('num_classes', '—')}")
                st.markdown(f"**Best Val Acc:** {meta.get('best_val_accuracy', '—')}")
            with col3:
                st.markdown(f"**Trained:** {meta.get('training_date', '—')}")
                st.markdown(f"**Epochs:** {meta.get('epochs_run', '—')}")

            if meta.get("class_names"):
                st.markdown(f"**Classes:** {', '.join(meta['class_names'][:10])}")

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🎯 Use for Prediction", key=f"use_{model_dir.name}"):
                    st.session_state["active_model_path"] = str(model_dir)
                    st.session_state["active_model_meta"] = meta
                    st.success(f"Active model: {model_dir.name}")
            with col_b:
                if st.button("🗑️ Delete", key=f"del_{model_dir.name}"):
                    import shutil
                    shutil.rmtree(model_dir)
                    st.success(f"Deleted {model_dir.name}")
                    st.rerun()
