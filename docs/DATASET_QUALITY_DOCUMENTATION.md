# Dataset Quality Assessment Documentation

## Overview

`DatasetQualityScorer` (`ml/data/quality_scorer.py`) evaluates tabular datasets across six dimensions and generates an overall score (0–100) with a letter grade (A–F).

> [!WARNING]
> Quality scores are **diagnostic indicators, NOT scientific standards**. They are intended to guide preprocessing decisions, not to be reported as objective metrics in research papers.

## Scoring Dimensions & Weights

| Dimension | Weight | What is Measured |
|-----------|--------|-----------------|
| Completeness | 25% | Proportion of non-missing values across all cells |
| Consistency | 20% | Consistency of data types and categorical values |
| Validity | 20% | Proportion of values within expected ranges |
| Uniqueness | 15% | Absence of duplicate rows |
| Balance | 10% | Class distribution evenness (for classification datasets) |
| Coverage | 10% | Breadth of distinct values per categorical column |

## Score Formula

```
overall_score = sum(dimension_score_i × weight_i) × 100
```

Each dimension score is in [0.0, 1.0] before weighting.

## Grade Thresholds

| Grade | Score Range | Interpretation |
|-------|------------|----------------|
| A | 90–100 | Excellent — ready for training |
| B | 75–89  | Good — minor issues |
| C | 60–74  | Fair — cleaning recommended |
| D | 45–59  | Poor — significant issues |
| F | 0–44   | Failing — major problems |

## Output Structure

```json
{
  "overall_score": 73.5,
  "grade": "C",
  "dimension_scores": {
    "completeness": 85,
    "consistency": 72,
    "validity": 68,
    "uniqueness": 95,
    "balance": 61,
    "coverage": 70
  },
  "issues": ["Class imbalance detected", "12 columns with >10% missing"],
  "recommendations": ["Apply SMOTE or class weights", "Impute missing values"],
  "timestamp": "2026-11-26T06:40:00Z"
}
```

## Limitations

- Quality scores are heuristic — a score of 80 does not guarantee a model will perform well
- Balance scoring assumes the dataset is for classification — not applicable to regression datasets
- Coverage scoring may not apply to continuous numerical datasets
