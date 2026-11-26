# Dataset Intelligence Engine — Phase 2

## Overview

The Dataset Intelligence Engine is the core data processing layer of E-WASTE AI. It transforms raw e-waste datasets into clean, validated, ML-ready datasets — with full audit trail and research reproducibility.

## Pipeline Flow

```
Raw Dataset Upload
       ↓
  Dataset Inspection (DatasetInspector)
       ↓
  Quality Scoring (DatasetQualityScorer)
       ↓
  Data Cleaning (AdvancedDataCleaner)
       ↓
  Domain Analysis (EwasteDomainAnalyzer)
       ↓
  Preprocessing (AdvancedPreprocessor)
       ↓
  Dataset Preparation (DatasetPreparer)
       ↓
  Export & Versioning (DatasetExporter)
       ↓
  Database Registration (DatasetService)
```

## Modules

| Module | Location | Responsibility |
|--------|----------|---------------|
| `DatasetInspector` | `ml/data/inspector.py` | Automated profiling of tabular and image datasets |
| `DatasetQualityScorer` | `ml/data/quality_scorer.py` | Multi-dimension quality scoring (0–100, A–F grade) |
| `AdvancedDataCleaner` | `ml/data/cleaner_advanced.py` | Cleaning with full audit log; never modifies original |
| `AdvancedPreprocessor` | `ml/data/preprocessor_advanced.py` | Scaling, encoding, stratified train/val/test split |
| `ImageDatasetValidator` | `ml/data/image_validator.py` | Corrupt image detection, duplicate detection, class balance |
| `EwasteDomainAnalyzer` | `ewaste/domain_intelligence.py` | Domain-specific analysis and hazardous material flags |
| `DatasetPreparer` | `ml/data/dataset_preparer.py` | Final splitting with provenance JSON |
| `DatasetExporter` | `ml/data/dataset_exporter.py` | CSV/Excel/JSON export, research doc generation |
| `DatasetService` | `backend/services/dataset_service.py` | SQLAlchemy-based database registration |

## Data Preservation Rules

> [!IMPORTANT]
> Raw datasets are **never modified**. Every operation creates a new copy in the appropriate directory.

| Directory | Contents |
|-----------|----------|
| `data/raw/` | Original uploaded files (read-only after upload) |
| `data/cleaned/` | Output of AdvancedDataCleaner |
| `data/processed/` | Output of AdvancedPreprocessor |
| `data/splits/{name}/` | train.csv, val.csv, test.csv + provenance.json |
| `data/versions/{name}/{tag}/` | Versioned snapshots |
| `data/exports/` | User-downloaded exports |

## Supported Dataset Types

- **Tabular**: CSV, Excel (XLSX/XLS), JSON
- **Image**: ZIP archive with class-per-folder structure, individual images
- **Mixed**: CSV with image paths

## Key Design Decisions

1. **Schema-agnostic**: No column names are hardcoded. All analysis adapts to the actual schema.
2. **Audit trail**: Every operation generates a timestamped log entry.
3. **Reproducibility**: Random seeds, preprocessing configs, and provenance JSONs are saved alongside splits.
4. **Honest quality scores**: Labeled as "diagnostic indicators, NOT scientific standards."
5. **Domain-aware**: E-waste specific checks (hazardous materials, suspicious recovery values) are built in.
