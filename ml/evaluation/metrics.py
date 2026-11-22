"""
E-Waste AI — Evaluation Metrics Engine
=========================================
Computes all classification metrics: accuracy, precision, recall,
F1, ROC-AUC, Cohen's Kappa, confusion matrix, per-class breakdown.
Generates Plotly charts for the frontend.

Used in Phase 3 (Evaluation) and Phase 5 (Research).
"""

import json
import logging
import numpy as np
from typing import List, Optional, Dict, Any, Tuple

logger = logging.getLogger(__name__)


def compute_classification_metrics(
    y_true: List[int],
    y_pred: List[int],
    y_proba: Optional[np.ndarray] = None,
    class_names: Optional[List[str]] = None,
    split: str = "test",
) -> Dict[str, Any]:
    """
    Compute comprehensive classification metrics.

    Args:
        y_true:       Ground truth labels (int encoded)
        y_pred:       Predicted labels (int encoded)
        y_proba:      Predicted probabilities (N × C array), optional
        class_names:  List of class names for the report
        split:        Dataset split name (train|val|test)

    Returns:
        dict with all metrics, confusion matrix, and classification report
    """
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        confusion_matrix, classification_report, cohen_kappa_score,
        roc_auc_score
    )

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    num_classes = len(np.unique(y_true))

    metrics: Dict[str, Any] = {
        "split":              split,
        "num_samples":        len(y_true),
        "num_classes":        num_classes,
        "accuracy":           round(float(accuracy_score(y_true, y_pred)), 6),
        "precision_macro":    round(float(precision_score(y_true, y_pred, average="macro",   zero_division=0)), 6),
        "precision_weighted": round(float(precision_score(y_true, y_pred, average="weighted",zero_division=0)), 6),
        "recall_macro":       round(float(recall_score(y_true, y_pred,    average="macro",   zero_division=0)), 6),
        "recall_weighted":    round(float(recall_score(y_true, y_pred,    average="weighted",zero_division=0)), 6),
        "f1_macro":           round(float(f1_score(y_true, y_pred,        average="macro",   zero_division=0)), 6),
        "f1_weighted":        round(float(f1_score(y_true, y_pred,        average="weighted",zero_division=0)), 6),
        "cohen_kappa":        round(float(cohen_kappa_score(y_true, y_pred)), 6),
        "confusion_matrix":   confusion_matrix(y_true, y_pred).tolist(),
    }

    # ROC-AUC (requires probabilities)
    if y_proba is not None:
        try:
            if num_classes == 2:
                roc = roc_auc_score(y_true, y_proba[:, 1])
            else:
                roc = roc_auc_score(y_true, y_proba, multi_class="ovr", average="weighted")
            metrics["roc_auc"] = round(float(roc), 6)
        except Exception as e:
            logger.warning(f"ROC-AUC computation failed: {e}")
            metrics["roc_auc"] = None

    # Per-class metrics
    report = classification_report(y_true, y_pred,
                                   target_names=class_names,
                                   output_dict=True,
                                   zero_division=0)
    metrics["classification_report"] = report

    # Per-class F1 for quick access
    per_class_f1 = {}
    if class_names:
        for cls in class_names:
            if cls in report:
                per_class_f1[cls] = round(report[cls]["f1-score"], 6)
    metrics["per_class_f1"] = per_class_f1

    logger.info(
        f"Metrics computed [{split}] | "
        f"Acc={metrics['accuracy']:.4f} | "
        f"F1={metrics['f1_weighted']:.4f} | "
        f"Kappa={metrics['cohen_kappa']:.4f}"
    )
    return metrics


def generate_confusion_matrix_chart(
    confusion_matrix: List[List[int]],
    class_names: List[str],
    title: str = "Confusion Matrix",
) -> Dict:
    """Generate a Plotly heatmap figure dict for the confusion matrix."""
    try:
        import plotly.graph_objects as go
        cm = np.array(confusion_matrix)
        # Normalize row-wise for % display
        cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)
        cm_norm = np.nan_to_num(cm_norm)

        text = [[f"{cm[i][j]}<br>({cm_norm[i][j]*100:.1f}%)"
                 for j in range(len(class_names))]
                for i in range(len(class_names))]

        fig = go.Figure(data=go.Heatmap(
            z=cm_norm,
            x=class_names,
            y=class_names,
            text=text,
            texttemplate="%{text}",
            colorscale="YlOrRd",
            showscale=True,
        ))
        fig.update_layout(
            title=title,
            xaxis_title="Predicted Label",
            yaxis_title="True Label",
            font=dict(family="Inter", size=12),
            paper_bgcolor="#141414",
            plot_bgcolor="#141414",
            font_color="#F2F2F2",
        )
        return fig.to_dict()
    except Exception as e:
        logger.error(f"Confusion matrix chart failed: {e}")
        return {}


def generate_training_history_chart(
    history: Dict[str, List[float]],
    title: str = "Training History",
) -> Dict:
    """
    Generate a Plotly chart for training/validation loss and accuracy.

    Args:
        history: {"train_loss": [...], "val_loss": [...], "train_acc": [...], "val_acc": [...]}
    """
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        epochs = list(range(1, len(history.get("train_loss", [])) + 1))

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Loss", "Accuracy"),
        )

        gold  = "#C9A84C"
        green = "#27AE60"
        red   = "#E74C3C"
        blue  = "#2980B9"

        if "train_loss" in history:
            fig.add_trace(go.Scatter(x=epochs, y=history["train_loss"],
                                     name="Train Loss", line=dict(color=gold)), row=1, col=1)
        if "val_loss" in history:
            fig.add_trace(go.Scatter(x=epochs, y=history["val_loss"],
                                     name="Val Loss", line=dict(color=red, dash="dash")), row=1, col=1)
        if "train_acc" in history:
            fig.add_trace(go.Scatter(x=epochs, y=history["train_acc"],
                                     name="Train Acc", line=dict(color=green)), row=1, col=2)
        if "val_acc" in history:
            fig.add_trace(go.Scatter(x=epochs, y=history["val_acc"],
                                     name="Val Acc", line=dict(color=blue, dash="dash")), row=1, col=2)

        fig.update_layout(
            title=title,
            paper_bgcolor="#141414",
            plot_bgcolor="#1C1C1C",
            font_color="#F2F2F2",
            font=dict(family="Inter"),
        )
        return fig.to_dict()
    except Exception as e:
        logger.error(f"Training history chart failed: {e}")
        return {}
