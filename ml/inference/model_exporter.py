"""
ml/inference/model_exporter.py
E-WASTE AI — Model Export and Handover
=======================================
Task 11: Export trained models, evaluation reports, training histories,
         and experiment configurations in research-ready formats.
"""

from __future__ import annotations

import json
import logging
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


class ModelExporter:
    """
    Exports trained models, metrics, and research artifacts.

    Usage::

        exporter = ModelExporter(output_dir="exports")
        path = exporter.export_model_package(entry_id, registry)
        report = exporter.generate_eval_report(metrics, output_path)
    """

    def __init__(self, output_dir: str | Path = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    # MODEL PACKAGE EXPORT                                                 #
    # ------------------------------------------------------------------ #

    def export_model_package(
        self,
        entry_id: str,
        registry,
        output_dir: str | Path | None = None,
    ) -> str:
        """
        Bundle the saved model file + metadata + evaluation report into a zip.

        Returns the path to the generated zip file.
        """
        out_dir = Path(output_dir) if output_dir else self.output_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        entry = registry.get(entry_id)
        if entry is None:
            raise ValueError(f"Model entry '{entry_id}' not found in registry.")

        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        zip_name = f"model_package_{entry_id}_{ts}.zip"
        zip_path = out_dir / zip_name

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            # --- metadata.json ---
            zf.writestr("metadata.json", json.dumps(entry, indent=2, default=str))

            # --- model file ---
            model_path = Path(entry.get("model_path", ""))
            if model_path.exists():
                zf.write(model_path, arcname=model_path.name)
            else:
                logger.warning("Model file not found at %s — skipping.", model_path)
                zf.writestr(
                    "model_missing.txt",
                    f"Model file not found: {model_path}\n"
                    "The file may have been moved or deleted.",
                )

            # --- eval report ---
            report_md = self._build_eval_report_md(entry)
            zf.writestr("evaluation_report.md", report_md)

            # --- training history if available ---
            history_path = Path("models/history") / f"{entry.get('run_name', entry_id)}_history.json"
            if history_path.exists():
                zf.write(history_path, arcname="training_history.json")

            # --- README ---
            zf.writestr("README.md", self._build_package_readme(entry))

        logger.info("Model package exported to %s", zip_path)
        return str(zip_path)

    # ------------------------------------------------------------------ #
    # EVALUATION REPORT                                                    #
    # ------------------------------------------------------------------ #

    def generate_eval_report(
        self,
        metrics: dict,
        output_path: str | Path | None = None,
        run_name: str = "model",
    ) -> str:
        """
        Generate a Markdown evaluation report from a metrics dict.

        Accepts either:
        - A flat metrics dict (from a single split evaluation)
        - An entry dict with train_metrics/val_metrics/test_metrics keys

        Returns the Markdown string; optionally writes to output_path.
        """
        # If the metrics dict is flat (from evaluator.evaluate_tabular),
        # wrap it into the entry structure expected by _build_eval_report_md
        if "train_metrics" not in metrics and "val_metrics" not in metrics and "test_metrics" not in metrics:
            split = metrics.get("split", "test")
            entry = {
                "run_name": run_name,
                "algorithm": metrics.get("algorithm", "N/A"),
                "task": metrics.get("task", "N/A"),
                f"{split}_metrics": metrics,
            }
        else:
            entry = dict(metrics)
            entry.setdefault("run_name", run_name)

        report = self._build_eval_report_md(entry, run_name=run_name)

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_text(report, encoding="utf-8")
            logger.info("Evaluation report written to %s", output_path)

        return report

    def _build_eval_report_md(self, entry: dict, run_name: str | None = None) -> str:
        name = run_name or entry.get("run_name", entry.get("algorithm", "model"))
        ts = datetime.now(timezone.utc).isoformat()
        task = entry.get("task", entry.get("model_type", "classification"))

        lines = [
            f"# Evaluation Report — {name}",
            f"",
            f"**Generated:** {ts}",
            f"**Algorithm:** {entry.get('algorithm', 'N/A')}",
            f"**Task:** {task}",
            f"**Dataset Version:** {entry.get('dataset_version', 'N/A')}",
            f"",
            "---",
            "",
        ]

        for split in ["train", "val", "test"]:
            m = entry.get(f"{split}_metrics") or entry.get("metrics", {})
            if not m and split != "test":
                continue
            if not m:
                continue
            lines.append(f"## {split.capitalize()} Metrics")
            lines.append("")
            if "accuracy" in m:
                lines.append(f"| Metric | Value |")
                lines.append(f"|--------|-------|")
                for k in ["accuracy", "precision", "recall", "f1_macro",
                          "f1_weighted", "kappa", "roc_auc", "pr_auc"]:
                    if k in m:
                        lines.append(f"| {k} | {m[k]:.4f} |")
            elif "mae" in m:
                lines.append(f"| Metric | Value |")
                lines.append(f"|--------|-------|")
                for k in ["mae", "mse", "rmse", "r2", "mape"]:
                    if k in m:
                        lines.append(f"| {k} | {m[k]:.4f} |")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("> **Note:** Scores are computed on the specified data split and reflect")
        lines.append("> performance on the available dataset. They are not generalizable claims")
        lines.append("> without independent validation on held-out or future data.")

        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    # TRAINING HISTORY EXPORT                                              #
    # ------------------------------------------------------------------ #

    def export_training_history(
        self,
        run_name: str,
        output_path: str | Path | None = None,
    ) -> str:
        """
        Export training history JSON for the given run name.

        Returns the JSON string; optionally writes to output_path.
        """
        history_path = Path("models/history") / f"{run_name}_history.json"
        if not history_path.exists():
            raise FileNotFoundError(
                f"Training history not found for run '{run_name}' at {history_path}"
            )

        content = history_path.read_text(encoding="utf-8")

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_text(content, encoding="utf-8")

        return content

    # ------------------------------------------------------------------ #
    # EXPERIMENT CONFIG EXPORT                                             #
    # ------------------------------------------------------------------ #

    def export_experiment_config(
        self,
        experiment_id: str,
        tracker,
        output_path: str | Path | None = None,
    ) -> str:
        """
        Export the experiment configuration as a JSON string.
        """
        exp = tracker.get_experiment(experiment_id)
        if exp is None:
            raise ValueError(f"Experiment '{experiment_id}' not found.")

        content = json.dumps(exp, indent=2, default=str)

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_text(content, encoding="utf-8")

        return content

    # ------------------------------------------------------------------ #
    # RESEARCH DOCUMENTATION                                               #
    # ------------------------------------------------------------------ #

    def generate_dataset_documentation(
        self,
        dataset_info: dict,
        cleaning_report: dict | None = None,
        quality_report: dict | None = None,
        output_path: str | Path | None = None,
    ) -> str:
        """Generate research-ready dataset documentation in Markdown."""
        ts = datetime.now(timezone.utc).isoformat()
        name = dataset_info.get("name", "Dataset")

        lines = [
            f"# Dataset Documentation — {name}",
            f"",
            f"**Generated:** {ts}",
            f"",
            "## Dataset Overview",
            f"",
            f"| Property | Value |",
            f"|----------|-------|",
        ]

        for k, v in dataset_info.items():
            lines.append(f"| {k} | {v} |")

        if cleaning_report:
            lines += [
                "",
                "## Cleaning Summary",
                "",
                f"| Operation | Count |",
                f"|-----------|-------|",
            ]
            for k, v in cleaning_report.items():
                lines.append(f"| {k} | {v} |")

        if quality_report:
            lines += [
                "",
                "## Quality Assessment",
                "",
                f"- **Overall Score:** {quality_report.get('overall_score', 'N/A')}",
                f"- **Grade:** {quality_report.get('grade', 'N/A')}",
                "",
                "> Quality scores are diagnostic indicators, NOT scientific standards.",
            ]

        lines += [
            "",
            "---",
            "",
            "_Generated by E-WASTE AI Dataset Intelligence Engine._",
        ]

        content = "\n".join(lines)

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_text(content, encoding="utf-8")

        return content

    # ------------------------------------------------------------------ #
    # README BUILDER                                                       #
    # ------------------------------------------------------------------ #

    def _build_package_readme(self, entry: dict) -> str:
        return f"""# Model Package — {entry.get("run_name", "model")}

## Contents

| File | Description |
|------|-------------|
| `metadata.json` | Full model metadata and training configuration |
| `{Path(entry.get("model_path", "model.pkl")).name}` | Serialized model file (joblib/pickle) |
| `evaluation_report.md` | Evaluation metrics on train/val/test splits |
| `training_history.json` | Per-epoch training history (if available) |

## Usage

```python
import joblib
model = joblib.load("model_file.pkl")
predictions = model.predict(X_new)
```

## Notes

- Algorithm: {entry.get("algorithm", "N/A")}
- Task: {entry.get("task", "N/A")}
- Trained: {entry.get("registered_at", "N/A")}

> This model was trained on the dataset version recorded in metadata.json.
> Always evaluate on new data before deploying in production.
"""
