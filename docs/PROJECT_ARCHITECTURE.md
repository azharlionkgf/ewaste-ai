# ♻️ E-WASTE AI — PROJECT ARCHITECTURE
## Combined Industrial Intelligence & Research Platform

**Version:** 2.0.0 | **Author:** Adil | **Date:** 2026-11-22  
**Classification:** Academic + Industrial + Research Platform

---

## 1. EXECUTIVE SUMMARY

E-Waste AI is a full-stack, AI-powered platform that serves three simultaneous roles:

| Role | Audience | Purpose |
|------|----------|---------|
| **Academic Platform** | Students, Professors | Follow dataset → training → evaluation workflow |
| **Industrial Tool** | E-Waste Recycling Companies | Manage incoming waste, classify, estimate recovery |
| **Research Platform** | Researchers | Conduct experiments, track provenance, generate papers |

The system handles the complete lifecycle of electronic waste — from intake registration to material recovery valuation — while maintaining rigorous ML experiment tracking for academic credibility.

---

## 2. SYSTEM ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────┐
│                    E-WASTE AI PLATFORM                               │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                   FRONTEND LAYER                              │   │
│  │          Streamlit UI  |  Custom CSS Theme                   │   │
│  │  Dashboard | Dataset | Training | Evaluation | Industrial    │   │
│  │  Classification | Recovery | Research | Reports | Settings   │   │
│  └──────────────────────┬───────────────────────────────────────┘   │
│                         │ HTTP / WebSocket                           │
│  ┌──────────────────────▼───────────────────────────────────────┐   │
│  │                   BACKEND LAYER                               │   │
│  │                FastAPI + Uvicorn                              │   │
│  │  Datasets | Cleaning | Preprocessing | Training | Inference  │   │
│  │  Evaluation | Recovery | Inventory | Research | Reports      │   │
│  └──────┬────────────┬────────────┬──────────────────┬──────────┘   │
│         │            │            │                  │               │
│  ┌──────▼──┐  ┌──────▼───┐  ┌────▼──────┐  ┌───────▼──────┐       │
│  │ ML/DL   │  │ Domain   │  │  Storage  │  │  Reporting   │       │
│  │ Engine  │  │ Intel.   │  │  Layer    │  │  Engine      │       │
│  │ PyTorch │  │ Recovery │  │ SQLite +  │  │  ReportLab   │       │
│  │ sklearn │  │ Material │  │ File Sys  │  │  Plotly      │       │
│  │ XGBoost │  │ Economic │  │           │  │              │       │
│  └─────────┘  └──────────┘  └───────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. PLATFORM MODULES

### 3.1 Core Academic Modules (Academic Workflow)

| Module | Description | Phase |
|--------|-------------|-------|
| **Dataset Management** | Upload, register, version, inspect CSV/Excel/JSON/Images | P1 |
| **Data Cleaning** | Automated detection of missing values, duplicates, outliers, type errors | P2 |
| **Data Preprocessing** | Feature engineering, encoding, scaling, train/val/test splitting | P3 |
| **Model Training** | Train CNN, Random Forest, XGBoost, CatBoost, SVM with config control | P4 |
| **Model Evaluation** | Accuracy, F1, confusion matrix, ROC-AUC, model comparison | P5 |

### 3.2 Core Industrial Modules

| Module | Description |
|--------|-------------|
| **E-Waste Classification** | AI-powered identification of device type, condition, hazard level |
| **Component Recognition** | Identify individual components (CPU, RAM, HDD, battery, PCB) |
| **Material Identification** | Identify material composition (Au, Ag, Cu, Pb, Li, plastics) |
| **Recovery Quantity Prediction** | Estimate recoverable material weights per unit |
| **Economic Valuation** | Calculate estimated recovery value based on material prices |
| **Industrial Inventory** | Register incoming batches, track processing, record outputs |
| **Recycling Workflow** | End-to-end: Intake → Classification → Sorting → Processing → Reporting |

### 3.3 Research & Analysis Modules

| Module | Description |
|--------|-------------|
| **Experiment Tracker** | Record hyperparameters, datasets, metrics, results per run |
| **Baseline Comparison** | Compare custom models vs. published benchmarks |
| **Environmental Analysis** | CO₂ saved, landfill avoided, toxicity reduction estimation |
| **Research Reporting** | Auto-generate structured reports for academic submission |

---

## 4. INDUSTRIAL WORKFLOW DESIGN

```
INCOMING E-WASTE
       │
       ▼
┌─────────────────┐
│  1. INTAKE &    │   Register batch → capture quantity, source,
│  REGISTRATION   │   condition, date received
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. VISUAL      │   Upload images → AI classifies device type,
│  CLASSIFICATION │   model, condition, hazard rating
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. COMPONENT   │   Identify internal components from classification
│  ANALYSIS       │   result + device database lookup
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. MATERIAL    │   Map components → material composition
│  IDENTIFICATION │   (% by weight, recoverable quantities)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. SORTING &   │   Generate sorting instructions per unit
│  PRIORITIZATION │   (high-value first, hazardous handling flags)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  6. RECOVERY    │   Recommend extraction processes,
│  PLANNING       │   equipment needed, safety protocols
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  7. ECONOMIC    │   Calculate estimated value per batch,
│  VALUATION      │   ROI on processing, market price lookup
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  8. REPORTING   │   Generate PDF/JSON report:
│  & COMPLIANCE   │   batch summary, material recovery, valuation
└─────────────────┘
```

---

## 5. MODULE DEPENDENCY MAP

```
Dataset Management
       │
       ├──► Data Cleaning
       │         │
       │         └──► Data Preprocessing
       │                    │
       │                    └──► Model Training ──► Model Evaluation
       │                                │
       │                                └──► Inference Engine
       │                                          │
       ├──► Industrial Inventory                  │
       │         │                                │
       │         └──► E-Waste Classification ◄────┘
       │                    │
       │                    ├──► Component Analysis
       │                    │         │
       │                    │         └──► Material Identification
       │                    │                    │
       │                    │                    ├──► Recovery Planning
       │                    │                    └──► Economic Valuation
       │                    │
       │                    └──► Environmental Analysis
       │
       └──► Research Experiment Tracker
                   │
                   └──► Research Reports
```

---

## 6. SECURITY & DATA HANDLING

| Concern | Solution |
|---------|----------|
| **File Validation** | MIME type checking + size limits on all uploads |
| **Path Traversal** | Sanitized paths using `pathlib.Path` |
| **SQL Injection** | SQLAlchemy ORM (parameterized queries only) |
| **Sensitive Data** | No user PII collected; device data only |
| **Model Files** | Checksum verification on model load |
| **Error Logging** | Structured logging; no stack traces in UI |

---

## 7. PERFORMANCE STRATEGY

| Concern | Approach |
|---------|----------|
| **CPU-only ML** | PyTorch CPU mode; batch size ≤ 16 for training |
| **Large Dataset** | Chunked pandas reading (`chunksize` param) |
| **Background Training** | FastAPI `BackgroundTasks` + WebSocket progress |
| **Image Processing** | Resize to 224×224 before inference |
| **Memory** | Generator-based data loading for large image sets |
| **Caching** | Model loaded once per session, cached in memory |

---

## 8. INTEGRATION POINTS

```
Streamlit UI
    │
    │  Direct Python calls (same process)
    ├──► service layer (dataset_service, training_service, etc.)
    │
    │  HTTP calls for async operations
    └──► FastAPI backend (port 8000)
              │
              └──► WebSocket /ws/training/{job_id}  (real-time progress)
```

> **Architecture Decision:** Streamlit and FastAPI run as separate processes.
> Streamlit pages call the FastAPI REST API for all operations.
> This keeps the UI stateless and the backend testable independently.
