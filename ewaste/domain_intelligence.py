"""
E-Waste Domain Intelligence Analyzer — Phase 2
Domain-specific analysis for electronic waste datasets.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Known E-Waste domain vocabulary (expandable via config/ewaste_categories.json)
# ---------------------------------------------------------------------------

KNOWN_DEVICE_CATEGORIES = {
    "laptop", "desktop", "monitor", "smartphone", "mobile", "phone",
    "tablet", "printer", "scanner", "keyboard", "mouse", "speaker",
    "television", "tv", "refrigerator", "washing machine", "microwave",
    "air conditioner", "camera", "hard drive", "ssd", "battery",
    "charger", "cable", "router", "switch", "server", "projector",
    "headphones", "earphones", "smartwatch", "gaming console",
}

KNOWN_MATERIAL_CATEGORIES = {
    "copper", "aluminum", "gold", "silver", "palladium", "platinum",
    "iron", "steel", "lead", "mercury", "cadmium", "lithium",
    "nickel", "zinc", "tin", "plastic", "glass", "rubber",
    "pcb", "circuit board", "lcd", "oled",
}

KNOWN_COMPONENT_CATEGORIES = {
    "cpu", "gpu", "ram", "motherboard", "power supply", "hard disk",
    "battery", "display", "keyboard", "trackpad", "fan", "heatsink",
    "capacitor", "resistor", "transistor", "diode", "transformer",
    "connector", "port",
}

HAZARDOUS_MATERIALS = {
    "lead", "mercury", "cadmium", "chromium", "beryllium",
    "arsenic", "barium", "pvc", "brominated flame retardant",
    "bfr", "antimony",
}

# Column name hints by role
ROLE_KEYWORDS = {
    "device_type":    ["device", "type", "category", "product", "equipment", "item"],
    "material":       ["material", "substance", "composition", "element"],
    "weight":         ["weight", "mass", "kg", "gram", "quantity", "amount"],
    "condition":      ["condition", "status", "grade", "quality", "state"],
    "economic_value": ["value", "price", "cost", "revenue", "worth", "dollar", "usd", "inr"],
    "environmental":  ["co2", "carbon", "emission", "environmental", "impact", "hazard"],
    "recovery":       ["recovery", "recovered", "recycle", "recycled", "extract"],
    "label":          ["label", "class", "target", "category"],
}


class EwasteDomainAnalyzer:
    """
    Performs e-waste domain-specific analysis on a DataFrame.

    Usage::

        analyzer = EwasteDomainAnalyzer()
        report = analyzer.analyze(df, inspection_report)
    """

    def __init__(self, categories_config_path: str | Path | None = None):
        self._extra_devices: set[str] = set()
        self._extra_materials: set[str] = set()
        if categories_config_path:
            self._load_extra_categories(Path(categories_config_path))

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def analyze(
        self,
        df: pd.DataFrame,
        inspection_report: dict | None = None,
    ) -> dict:
        """
        Analyze a DataFrame for e-waste domain properties.

        Returns a domain_report dict:
        {
          is_ewaste_dataset, confidence, detected_columns_by_role,
          inconsistent_categories, suspicious_records,
          hazardous_material_flags, suggestions, summary
        }
        """
        report: dict[str, Any] = {
            "is_ewaste_dataset": False,
            "confidence": 0.0,
            "detected_columns_by_role": {},
            "inconsistent_categories": {},
            "suspicious_records": [],
            "hazardous_material_flags": [],
            "domain_issues": [],
            "suggestions": [],
            "summary": "",
        }

        # 1. Column role detection
        role_map = self.get_column_role_suggestions(df)
        report["detected_columns_by_role"] = role_map

        # 2. Is this an e-waste dataset?
        confidence = self._compute_ewaste_confidence(df, role_map)
        report["is_ewaste_dataset"] = confidence >= 0.3
        report["confidence"] = round(confidence, 2)

        # 3. Validate known device/material categories
        inconsistencies = self._find_inconsistent_categories(df, role_map)
        report["inconsistent_categories"] = inconsistencies

        # 4. Suspicious records (negative weights, impossible recovery %)
        suspicious = self._find_suspicious_records(df, role_map)
        report["suspicious_records"] = suspicious

        # 5. Hazardous material flags
        hazmat = self._find_hazardous_materials(df, role_map)
        report["hazardous_material_flags"] = hazmat

        # 6. Domain issues
        issues = []
        if not role_map.get("device_type"):
            issues.append("No device-type column detected")
        if not role_map.get("weight"):
            issues.append("No weight/quantity column detected")
        if inconsistencies:
            issues.append(f"Inconsistent category values in {len(inconsistencies)} column(s)")
        if suspicious:
            issues.append(f"{len(suspicious)} suspicious records found (negative/impossible values)")
        if hazmat:
            issues.append(f"{len(hazmat)} hazardous material references detected")
        report["domain_issues"] = issues

        # 7. Suggestions
        suggestions = self._generate_suggestions(df, role_map, report)
        report["suggestions"] = suggestions

        # 8. Summary
        report["summary"] = self._build_summary(report)

        return report

    def get_column_role_suggestions(self, df: pd.DataFrame) -> dict[str, list[str]]:
        """
        Suggest which columns likely correspond to which e-waste domain role.

        Returns a dict: {role: [col1, col2, ...]}
        """
        role_map: dict[str, list[str]] = {role: [] for role in ROLE_KEYWORDS}
        for col in df.columns:
            col_lower = col.lower()
            for role, keywords in ROLE_KEYWORDS.items():
                if any(kw in col_lower for kw in keywords):
                    role_map[role].append(col)
        return role_map

    # ------------------------------------------------------------------ #
    # Private helpers                                                      #
    # ------------------------------------------------------------------ #

    def _load_extra_categories(self, path: Path) -> None:
        try:
            data = json.loads(path.read_text())
            self._extra_devices = {c.lower() for c in data.get("devices", [])}
            self._extra_materials = {m.lower() for m in data.get("materials", [])}
        except Exception as exc:
            logger.warning("Could not load categories config: %s", exc)

    def _compute_ewaste_confidence(
        self, df: pd.DataFrame, role_map: dict
    ) -> float:
        score = 0.0
        # Column name signals
        if role_map.get("device_type"):
            score += 0.3
        if role_map.get("material"):
            score += 0.2
        if role_map.get("weight"):
            score += 0.15
        if role_map.get("recovery"):
            score += 0.15
        if role_map.get("economic_value"):
            score += 0.1
        if role_map.get("environmental"):
            score += 0.1

        # Value signals — look for known device/material names in string columns
        for col in df.select_dtypes(include="object").columns:
            vals = df[col].dropna().astype(str).str.lower()
            ewaste_hits = vals.apply(
                lambda v: any(d in v for d in KNOWN_DEVICE_CATEGORIES | KNOWN_MATERIAL_CATEGORIES)
            ).sum()
            if ewaste_hits > len(vals) * 0.1:
                score = min(score + 0.1, 1.0)
                break

        return min(score, 1.0)

    def _find_inconsistent_categories(
        self, df: pd.DataFrame, role_map: dict
    ) -> dict[str, list]:
        """Find values in categorical columns that likely refer to same thing."""
        result: dict[str, list] = {}
        categorical_role_cols = (
            role_map.get("device_type", [])
            + role_map.get("material", [])
            + role_map.get("condition", [])
            + role_map.get("label", [])
        )
        for col in categorical_role_cols:
            if col not in df.columns:
                continue
            unique_vals = df[col].dropna().unique()
            canonical: dict[str, list] = {}
            for v in unique_vals:
                key = str(v).strip().lower()
                canonical.setdefault(key, []).append(str(v))
            conflicts = {k: v for k, v in canonical.items() if len(v) > 1}
            if conflicts:
                result[col] = [
                    {"canonical": k, "variants": v}
                    for k, v in conflicts.items()
                ]
        return result

    def _find_suspicious_records(
        self, df: pd.DataFrame, role_map: dict
    ) -> list[dict]:
        suspicious = []
        weight_cols = role_map.get("weight", [])
        recovery_cols = role_map.get("recovery", [])
        value_cols = role_map.get("economic_value", [])

        for col in weight_cols:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                neg_mask = df[col] < 0
                if neg_mask.any():
                    suspicious.append({
                        "column": col,
                        "issue": "negative_weight",
                        "count": int(neg_mask.sum()),
                        "row_indices": df.index[neg_mask].tolist()[:10],
                    })

        for col in recovery_cols:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                # Recovery percentage > 100 is suspicious
                high_mask = df[col] > 100
                if high_mask.any():
                    suspicious.append({
                        "column": col,
                        "issue": "recovery_pct_over_100",
                        "count": int(high_mask.sum()),
                        "row_indices": df.index[high_mask].tolist()[:10],
                    })
                neg_mask = df[col] < 0
                if neg_mask.any():
                    suspicious.append({
                        "column": col,
                        "issue": "negative_recovery",
                        "count": int(neg_mask.sum()),
                        "row_indices": df.index[neg_mask].tolist()[:10],
                    })

        for col in value_cols:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                neg_mask = df[col] < 0
                if neg_mask.any():
                    suspicious.append({
                        "column": col,
                        "issue": "negative_economic_value",
                        "count": int(neg_mask.sum()),
                        "row_indices": df.index[neg_mask].tolist()[:10],
                    })

        return suspicious

    def _find_hazardous_materials(
        self, df: pd.DataFrame, role_map: dict
    ) -> list[dict]:
        flags = []
        material_cols = role_map.get("material", [])
        for col in material_cols:
            if col not in df.columns:
                continue
            vals = df[col].dropna().astype(str).str.lower()
            for hazmat in HAZARDOUS_MATERIALS:
                matches = vals[vals.str.contains(hazmat, na=False)]
                if not matches.empty:
                    flags.append({
                        "column": col,
                        "material": hazmat,
                        "count": len(matches),
                        "is_hazardous": True,
                        "note": "Requires special handling under WEEE/RoHS regulations",
                    })
        return flags

    def _generate_suggestions(
        self, df: pd.DataFrame, role_map: dict, report: dict
    ) -> list[str]:
        suggestions = []
        if not role_map.get("device_type"):
            suggestions.append(
                "Consider adding a 'device_type' or 'category' column to classify waste items"
            )
        if not role_map.get("weight"):
            suggestions.append(
                "Adding a weight/quantity column enables material recovery estimation"
            )
        if not role_map.get("economic_value"):
            suggestions.append(
                "Economic value columns allow recycling ROI analysis"
            )
        if report.get("hazardous_material_flags"):
            suggestions.append(
                "Hazardous materials detected — ensure WEEE/RoHS compliance documentation"
            )
        if report.get("suspicious_records"):
            suggestions.append(
                "Inspect and correct suspicious records before model training"
            )
        if not role_map.get("label"):
            suggestions.append(
                "No label/target column detected — define one before training a classifier"
            )
        return suggestions

    @staticmethod
    def _build_summary(report: dict) -> str:
        ewaste = "YES" if report["is_ewaste_dataset"] else "NO"
        confidence = int(report["confidence"] * 100)
        n_issues = len(report["domain_issues"])
        n_suspicious = len(report["suspicious_records"])
        n_hazmat = len(report["hazardous_material_flags"])
        return (
            f"E-Waste dataset: {ewaste} (confidence {confidence}%). "
            f"{n_issues} domain issue(s), {n_suspicious} suspicious record(s), "
            f"{n_hazmat} hazardous material flag(s)."
        )
