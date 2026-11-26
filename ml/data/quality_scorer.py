"""
ml/data/quality_scorer.py
E-WASTE AI — Dataset Quality Assessment Engine
Produces an explainable, multi-dimensional quality score.

IMPORTANT: Scores are based on dataset properties only.
They are NOT a scientific standard — they are diagnostic indicators
to help users understand their data before model training.
"""

import logging
import datetime
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# Score weights — must sum to 1.0
DIMENSION_WEIGHTS = {
    "completeness": 0.25,   # Missing value coverage
    "uniqueness": 0.15,     # Duplicate rows
    "consistency": 0.20,    # Type correctness, mixed types, whitespace
    "validity": 0.20,       # Outliers, zero-variance, format issues
    "balance": 0.10,        # Class imbalance (if target detected)
    "coverage": 0.10,       # Row count adequacy for ML
}


class DatasetQualityScorer:
    """
    Computes an explainable quality score (0–100) across six dimensions.
    Uses an inspection report produced by DatasetInspector.
    Does NOT modify the source data.
    """

    def __init__(self):
        self.scores: dict = {}
        self.issues: list = []
        self.recommendations: list = []

    def score(self, inspection_report: dict, df: pd.DataFrame = None) -> dict:
        """
        Compute quality scores from an inspection report.
        df is optional — only used for balance scoring when inspector didn't run class distribution.
        """
        logger.info(f"Scoring dataset: {inspection_report.get('dataset_name', 'unknown')}")

        shape = inspection_report.get("shape", {})
        n_rows = shape.get("rows", 0)
        n_cols = shape.get("columns", 0)

        dim_scores = {}

        # 1. Completeness
        dim_scores["completeness"] = self._score_completeness(inspection_report)

        # 2. Uniqueness
        dim_scores["uniqueness"] = self._score_uniqueness(inspection_report)

        # 3. Consistency
        dim_scores["consistency"] = self._score_consistency(inspection_report)

        # 4. Validity
        dim_scores["validity"] = self._score_validity(inspection_report)

        # 5. Balance
        dim_scores["balance"] = self._score_balance(inspection_report)

        # 6. Coverage (row count adequacy)
        dim_scores["coverage"] = self._score_coverage(n_rows, n_cols)

        # Weighted overall score
        overall = sum(
            dim_scores[dim] * weight
            for dim, weight in DIMENSION_WEIGHTS.items()
            if dim in dim_scores
        )
        overall = round(min(100.0, max(0.0, overall)), 1)

        grade = _score_to_grade(overall)
        self.issues = self._collect_issues(inspection_report)
        self.recommendations = self._make_recommendations(inspection_report, dim_scores)

        result = {
            "dataset_name": inspection_report.get("dataset_name", "unknown"),
            "scored_at": datetime.datetime.utcnow().isoformat(),
            "overall_score": overall,
            "grade": grade,
            "dimension_scores": {k: round(v, 1) for k, v in dim_scores.items()},
            "dimension_weights": DIMENSION_WEIGHTS,
            "score_explanation": (
                "Score is a weighted average of six data quality dimensions. "
                "It is a diagnostic indicator only, NOT a scientific standard. "
                "A score of 70+ is generally acceptable for initial ML experiments."
            ),
            "issues": self.issues,
            "recommendations": self.recommendations,
            "shape": shape,
        }
        logger.info(f"Quality score: {overall}/100 ({grade})")
        return result

    # ------------------------------------------------------------------
    # Dimension scorers
    # ------------------------------------------------------------------
    def _score_completeness(self, report: dict) -> float:
        missing = report.get("missing", {})
        total_pct = missing.get("total_missing_pct", 0.0)
        # 100 if 0% missing, 0 if 100% missing
        score = max(0.0, 100.0 - total_pct * 2.0)

        # Heavy penalty for columns with >50% missing
        severe = sum(
            1 for c in missing.get("columns_with_missing", [])
            if c.get("pct", 0) > 50
        )
        score -= severe * 10
        return max(0.0, min(100.0, score))

    def _score_uniqueness(self, report: dict) -> float:
        dup = report.get("duplicates", {})
        dup_pct = dup.get("duplicate_pct", 0.0)
        score = max(0.0, 100.0 - dup_pct * 3.0)
        return round(score, 1)

    def _score_consistency(self, report: dict) -> float:
        score = 100.0
        issues = report.get("data_issues", [])

        for issue in issues:
            itype = issue.get("type", "")
            severity = issue.get("severity", "low")
            penalty = {"high": 15, "medium": 8, "low": 3}.get(severity, 3)
            if itype in ("mixed_types", "empty_columns", "zero_variance"):
                score -= penalty

        # Whitespace/case issues in categoricals
        cat_stats = report.get("categorical_stats", {})
        for col_info in cat_stats.values():
            if col_info.get("has_leading_trailing_spaces"):
                score -= 5
            if col_info.get("has_mixed_case"):
                score -= 3

        return round(max(0.0, min(100.0, score)), 1)

    def _score_validity(self, report: dict) -> float:
        score = 100.0
        outliers = report.get("outliers", {})
        # Penalise if many columns have outliers
        for col, info in outliers.items():
            pct = info.get("outlier_pct", 0)
            if pct > 10:
                score -= 10
            elif pct > 5:
                score -= 5
            else:
                score -= 2

        issues = report.get("data_issues", [])
        for issue in issues:
            if issue.get("type") in ("high_missing", "empty_columns"):
                score -= 10

        return round(max(0.0, min(100.0, score)), 1)

    def _score_balance(self, report: dict) -> float:
        """Score based on class imbalance — only if target-like columns detected."""
        class_dist = report.get("class_distribution", {})
        if not class_dist:
            return 80.0  # Neutral — no classification target detected

        min_ratio = min(
            info.get("imbalance_ratio", 1.0)
            for info in class_dist.values()
        )
        if min_ratio <= 1.5:
            return 100.0
        elif min_ratio <= 3.0:
            return 80.0
        elif min_ratio <= 10.0:
            return 50.0
        else:
            return 20.0

    def _score_coverage(self, n_rows: int, n_cols: int) -> float:
        """Score based on dataset size adequacy for ML."""
        if n_rows >= 10000:
            return 100.0
        elif n_rows >= 5000:
            return 90.0
        elif n_rows >= 1000:
            return 75.0
        elif n_rows >= 500:
            return 55.0
        elif n_rows >= 100:
            return 35.0
        else:
            return 10.0

    # ------------------------------------------------------------------
    # Issues & Recommendations
    # ------------------------------------------------------------------
    def _collect_issues(self, report: dict) -> list:
        issues = []
        missing = report.get("missing", {})
        for col_info in missing.get("columns_with_missing", []):
            sev = "high" if col_info["pct"] > 30 else "medium" if col_info["pct"] > 10 else "low"
            issues.append({
                "type": "missing_values",
                "column": col_info["column"],
                "detail": f"{col_info['pct']}% missing ({col_info['count']} rows)",
                "severity": sev,
            })

        dup = report.get("duplicates", {})
        if dup.get("duplicate_rows", 0) > 0:
            issues.append({
                "type": "duplicate_rows",
                "detail": f"{dup['duplicate_rows']} duplicate rows ({dup['duplicate_pct']}%)",
                "severity": "medium",
            })

        for issue in report.get("data_issues", []):
            issues.append(issue)

        for col, info in report.get("outliers", {}).items():
            if info["outlier_pct"] > 5:
                issues.append({
                    "type": "outliers",
                    "column": col,
                    "detail": f"{info['outlier_count']} outliers ({info['outlier_pct']}%)",
                    "severity": "medium",
                })

        for col, dist in report.get("class_distribution", {}).items():
            if dist.get("is_imbalanced"):
                issues.append({
                    "type": "class_imbalance",
                    "column": col,
                    "detail": f"Imbalance ratio {dist['imbalance_ratio']}× in '{col}'",
                    "severity": "medium",
                })
        return issues

    def _make_recommendations(self, report: dict, dim_scores: dict) -> list:
        recs = []

        if dim_scores.get("completeness", 100) < 70:
            recs.append({
                "priority": "HIGH",
                "action": "Handle missing values",
                "detail": "Use median imputation for numeric columns, mode for categorical. "
                          "Consider dropping columns with >50% missing."
            })

        if dim_scores.get("uniqueness", 100) < 85:
            recs.append({
                "priority": "HIGH",
                "action": "Remove duplicate rows",
                "detail": "Use Data Cleaning → Remove Duplicates before training."
            })

        if dim_scores.get("consistency", 100) < 70:
            recs.append({
                "priority": "MEDIUM",
                "action": "Fix data consistency",
                "detail": "Normalize text case, strip whitespace, fix mixed-type columns."
            })

        if dim_scores.get("balance", 100) < 60:
            recs.append({
                "priority": "MEDIUM",
                "action": "Address class imbalance",
                "detail": "Use stratified splitting. Consider oversampling (SMOTE) or class weights."
            })

        if dim_scores.get("coverage", 100) < 55:
            recs.append({
                "priority": "HIGH",
                "action": "Collect more data",
                "detail": "Dataset has fewer than 1,000 rows. ML models typically need 1,000+ samples per class."
            })

        if dim_scores.get("validity", 100) < 70:
            recs.append({
                "priority": "MEDIUM",
                "action": "Review outliers",
                "detail": "Inspect outlier values before training. Remove only if confirmed data errors."
            })

        return recs


def _score_to_grade(score: float) -> str:
    if score >= 90:
        return "A — Excellent"
    elif score >= 80:
        return "B — Good"
    elif score >= 70:
        return "C — Acceptable"
    elif score >= 60:
        return "D — Needs Work"
    else:
        return "F — Poor — Major Issues"
