"""
E-Waste AI — Report Generation Engine (Phase 4 Task 10)
========================================================
Generates downloadable reports in JSON, CSV, and text formats.
Includes report dates, data sources, and assumptions in every report.
"""

from __future__ import annotations

import csv
import io
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from backend.config import REPORTS_DIR

logger = logging.getLogger(__name__)


class ReportGenerationService:
    """Generate structured reports for batches, inventory, economics, and research."""

    # ── Batch Report ───────────────────────────────────────────────────

    def generate_batch_report(self, batch_data: dict, format: str = "json") -> dict:
        """Generate a comprehensive batch report."""
        report_data = {
            "report_type": "batch_report",
            "title": f"Batch Report — {batch_data.get('batch_number', 'N/A')}",
            "generated_at": datetime.utcnow().isoformat(),
            "data_source": "E-Waste AI Platform Database",
            "batch": batch_data,
            "disclaimer": "Report generated from operational data. Verify figures before compliance use.",
        }
        return self._save_report(report_data, "batch_report", format)

    # ── Material Recovery Report ───────────────────────────────────────

    def generate_recovery_report(self, recovery_data: dict, format: str = "json") -> dict:
        """Generate a material recovery summary report."""
        report_data = {
            "report_type": "material_recovery_report",
            "title": "Material Recovery Report",
            "generated_at": datetime.utcnow().isoformat(),
            "assumptions": recovery_data.get("assumptions", {}),
            "data": recovery_data,
            "disclaimer": recovery_data.get("disclaimer", "Estimates only — not certified."),
        }
        return self._save_report(report_data, "recovery_report", format)

    # ── Financial Report ───────────────────────────────────────────────

    def generate_financial_report(self, economic_data: dict, format: str = "json") -> dict:
        """Generate economic analysis report."""
        report_data = {
            "report_type": "financial_report",
            "title": "Economic Recovery Analysis Report",
            "generated_at": datetime.utcnow().isoformat(),
            "price_data_date": economic_data.get("price_data_date"),
            "data": economic_data,
            "disclaimer": economic_data.get("disclaimer", "Financial estimates only."),
        }
        return self._save_report(report_data, "financial_report", format)

    # ── Environmental Report ───────────────────────────────────────────

    def generate_environmental_report(self, env_data: dict, format: str = "json") -> dict:
        """Generate environmental impact report."""
        report_data = {
            "report_type": "environmental_report",
            "title": "Environmental Impact Estimate Report",
            "generated_at": datetime.utcnow().isoformat(),
            "is_certified": False,
            "certification_note": "NOT legally certified. For planning purposes only.",
            "data": env_data,
        }
        return self._save_report(report_data, "environmental_report", format)

    # ── Inventory Report ───────────────────────────────────────────────

    def generate_inventory_report(self, inventory_items: list, format: str = "json") -> dict:
        """Generate inventory summary report."""
        report_data = {
            "report_type": "inventory_report",
            "title": "Material Inventory Report",
            "generated_at": datetime.utcnow().isoformat(),
            "total_items": len(inventory_items),
            "inventory": inventory_items,
        }
        return self._save_report(report_data, "inventory_report", format)

    # ── AI Prediction Report ───────────────────────────────────────────

    def generate_ai_report(self, predictions: list, format: str = "json") -> dict:
        """Generate AI prediction history report."""
        report_data = {
            "report_type": "ai_prediction_report",
            "title": "AI Prediction Report",
            "generated_at": datetime.utcnow().isoformat(),
            "total_predictions": len(predictions),
            "predictions": predictions,
            "disclaimer": (
                "AI predictions are estimates from trained ML models. "
                "Accuracy depends on training data quality and model version."
            ),
        }
        return self._save_report(report_data, "ai_prediction_report", format)

    # ── Research Experiment Report ─────────────────────────────────────

    def generate_research_report(self, experiments: list, format: str = "json") -> dict:
        """Generate research experiment summary."""
        report_data = {
            "report_type": "research_experiment_report",
            "title": "Research Experiments Summary Report",
            "generated_at": datetime.utcnow().isoformat(),
            "experiment_count": len(experiments),
            "experiments": experiments,
            "note": "All metrics are from actual experiments. Synthetic data experiments are explicitly labeled.",
        }
        return self._save_report(report_data, "research_report", format)

    # ── Save & Format ──────────────────────────────────────────────────

    def _save_report(self, report_data: dict, report_type: str, format: str) -> dict:
        """Save report to disk and return metadata."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{report_type}_{timestamp}.{format}"
        file_path = REPORTS_DIR / filename

        try:
            if format == "json":
                content = json.dumps(report_data, indent=2, default=str)
                file_path.write_text(content, encoding="utf-8")
            elif format == "csv":
                content = self._to_csv(report_data)
                file_path.write_text(content, encoding="utf-8")
            else:
                # Default to JSON
                content = json.dumps(report_data, indent=2, default=str)
                file_path = file_path.with_suffix(".json")
                file_path.write_text(content, encoding="utf-8")

            size = file_path.stat().st_size
            logger.info("Report saved: %s (%d bytes)", file_path, size)

            return {
                "success": True,
                "report_type": report_type,
                "title": report_data.get("title"),
                "file_path": str(file_path),
                "file_format": format,
                "file_size_bytes": size,
                "generated_at": report_data.get("generated_at"),
                "is_available": True,
            }
        except Exception as exc:
            logger.error("Failed to save report: %s", exc)
            return {
                "success": False,
                "report_type": report_type,
                "error": str(exc),
                "data": report_data,  # Return data even if save failed
            }

    def _to_csv(self, data: dict) -> str:
        """Flatten report data to CSV format."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["field", "value"])
        self._flatten_to_rows(data, writer)
        return output.getvalue()

    def _flatten_to_rows(self, obj, writer, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                self._flatten_to_rows(v, writer, f"{prefix}.{k}" if prefix else k)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                self._flatten_to_rows(item, writer, f"{prefix}[{i}]")
        else:
            writer.writerow([prefix, str(obj)])
