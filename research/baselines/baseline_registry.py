"""
research/baselines/baseline_registry.py
E-WASTE AI - Baseline Model Registry
Defines baseline models for comparison in research experiments.
"""

import logging
import json

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Baseline Definitions
# ------------------------------------------------------------------

EWASTE_BASELINES = {
    "random_classifier": {
        "name": "Random Classifier",
        "type": "statistical",
        "description": "Assigns random class with uniform probability. Used as absolute lower bound.",
        "expected_accuracy_range": [0.05, 0.15],
        "expected_f1_range": [0.03, 0.12],
        "notes": "For N classes, expected accuracy ≈ 1/N. E.g. for 15 categories ≈ 6.7%.",
        "implementation": "sklearn.dummy.DummyClassifier(strategy='uniform')",
    },
    "majority_class": {
        "name": "Majority Class Classifier",
        "type": "statistical",
        "description": "Always predicts the most frequent class in the training set.",
        "expected_accuracy_range": [0.10, 0.30],
        "expected_f1_range": [0.05, 0.20],
        "notes": "Performance depends on class imbalance. Useful for imbalanced datasets.",
        "implementation": "sklearn.dummy.DummyClassifier(strategy='most_frequent')",
    },
    "logistic_regression_baseline": {
        "name": "Logistic Regression (Baseline)",
        "type": "classical_ml",
        "description": "Simple linear classifier. Establishes linear separability baseline.",
        "expected_accuracy_range": [0.45, 0.72],
        "expected_f1_range": [0.40, 0.70],
        "notes": "Uses L2 regularization, max_iter=1000, balanced class weights.",
        "implementation": "sklearn.linear_model.LogisticRegression(max_iter=1000, class_weight='balanced')",
    },
    "random_forest_baseline": {
        "name": "Random Forest (100 trees)",
        "type": "classical_ml",
        "description": "Ensemble tree model. Strong tabular baseline with feature importance.",
        "expected_accuracy_range": [0.60, 0.85],
        "expected_f1_range": [0.58, 0.83],
        "notes": "n_estimators=100, max_depth=None. Generally solid baseline for tabular e-waste data.",
        "implementation": "sklearn.ensemble.RandomForestClassifier(n_estimators=100, random_state=42)",
    },
    "mobilenet_v2_imagenet": {
        "name": "MobileNetV2 (ImageNet pretrained, frozen)",
        "type": "deep_learning",
        "description": "Feature extraction using ImageNet weights. No fine-tuning. Tests transfer learning value.",
        "expected_accuracy_range": [0.30, 0.65],
        "expected_f1_range": [0.28, 0.62],
        "notes": "Frozen backbone, only classification head trained. Varies greatly by domain similarity.",
        "implementation": "torchvision.models.mobilenet_v2(pretrained=True) + frozen backbone",
    },
}


# ------------------------------------------------------------------
# Registry Class
# ------------------------------------------------------------------

class BaselineRegistry:
    """Registry of baseline models for research comparison."""

    def __init__(self):
        self._baselines = EWASTE_BASELINES.copy()

    def list_baselines(self) -> list:
        """Return all registered baselines as a list of dicts."""
        return [
            {"key": k, **v}
            for k, v in self._baselines.items()
        ]

    def get_baseline(self, name: str) -> dict:
        """Get a specific baseline by key name."""
        b = self._baselines.get(name)
        if b is None:
            available = list(self._baselines.keys())
            raise KeyError(f"Baseline '{name}' not found. Available: {available}")
        return {"key": name, **b}

    def register_custom_baseline(self, key: str, definition: dict) -> None:
        """Register a custom baseline model."""
        required = ["name", "type", "description"]
        for field in required:
            if field not in definition:
                raise ValueError(f"Baseline definition missing required field: '{field}'")
        self._baselines[key] = definition
        logger.info(f"Registered custom baseline: {key}")

    def evaluate_against_baseline(self, actual_results: dict, baseline_name: str) -> dict:
        """
        Compare actual model results against a named baseline.
        actual_results: {"accuracy": float, "f1": float, ...}
        Returns: improvement percentages and pass/fail flags.
        """
        baseline = self.get_baseline(baseline_name)
        acc_range = baseline.get("expected_accuracy_range", [0, 1])
        f1_range = baseline.get("expected_f1_range", [0, 1])

        actual_acc = actual_results.get("accuracy")
        actual_f1 = actual_results.get("f1")

        baseline_acc_mid = sum(acc_range) / 2
        baseline_f1_mid = sum(f1_range) / 2

        result = {
            "baseline_name": baseline["name"],
            "baseline_key": baseline_name,
        }

        if actual_acc is not None:
            improvement_acc = ((actual_acc - baseline_acc_mid) / max(baseline_acc_mid, 1e-9)) * 100
            result["accuracy"] = {
                "actual": round(actual_acc, 4),
                "baseline_midpoint": round(baseline_acc_mid, 4),
                "baseline_range": acc_range,
                "improvement_pct": round(improvement_acc, 2),
                "beats_baseline": actual_acc > acc_range[1],
            }

        if actual_f1 is not None:
            improvement_f1 = ((actual_f1 - baseline_f1_mid) / max(baseline_f1_mid, 1e-9)) * 100
            result["f1"] = {
                "actual": round(actual_f1, 4),
                "baseline_midpoint": round(baseline_f1_mid, 4),
                "baseline_range": f1_range,
                "improvement_pct": round(improvement_f1, 2),
                "beats_baseline": actual_f1 > f1_range[1],
            }

        return result

    def generate_comparison_table(self, results_list: list) -> str:
        """
        Generate a markdown comparison table.
        results_list: [{"model_name": str, "accuracy": float, "f1": float, ...}, ...]
        """
        if not results_list:
            return "_No results to compare._"

        headers = ["Model", "Accuracy", "F1-Score", "Precision", "Recall"]
        rows = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
        ]

        for r in results_list:
            row = [
                r.get("model_name", "Unknown"),
                f"{r.get('accuracy', 0):.4f}" if r.get("accuracy") is not None else "N/A",
                f"{r.get('f1', 0):.4f}" if r.get("f1") is not None else "N/A",
                f"{r.get('precision', 0):.4f}" if r.get("precision") is not None else "N/A",
                f"{r.get('recall', 0):.4f}" if r.get("recall") is not None else "N/A",
            ]
            rows.append("| " + " | ".join(row) + " |")

        return "\n".join(rows)
