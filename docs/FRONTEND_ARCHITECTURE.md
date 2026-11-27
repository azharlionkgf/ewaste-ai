# Phase 5 Frontend Architecture

## Overview

Phase 5 delivers a complete, professional frontend for the E-Waste AI platform built with Streamlit. All 16 pages connect to real backend APIs and database records — no fake data, dummy results or simulated analytics anywhere.

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend Framework | Streamlit | 1.32.2 |
| Charting | Plotly | 5.18.0 |
| Data Tables | Pandas + Streamlit DataFrame | 2.2.2 |
| Styling | Custom CSS (injected via theme.py) | — |
| State Management | Streamlit Session State | — |
| Backend Connection | Direct Python imports + SQLAlchemy | 2.0.30 |

## Application Entry Point

`app.py` (project root) is the Streamlit entry point:

1. Calls `st.set_page_config()` once at startup
2. Injects the global CSS theme via `frontend.theme.inject_theme()`
3. Calls `frontend.components.sidebar.render_sidebar()` → returns current page key
4. Routes to the correct page module via `if/elif` chain

## Directory Structure

```
frontend/
├── theme.py                   # Global CSS design system + helper functions
├── components/
│   └── sidebar.py             # Collapsible navigation sidebar
└── pages/
    ├── __init__.py
    ├── dashboard.py           # Task 3 — Industrial Intelligence Dashboard
    ├── dataset_intelligence.py # Task 4a — AI-powered dataset analysis
    ├── dataset_management.py  # Task 4b — Upload, preview, manage datasets
    ├── data_cleaning.py       # Task 4c — Data cleaning pipeline UI
    ├── preprocessing.py       # Task 4d — Feature engineering / preprocessing
    ├── model_training.py      # Task 5 — Model Training Workspace (44 KB)
    ├── model_evaluation.py    # Task 6 — Evaluation, registry, comparison
    ├── image_analysis.py      # Task 7a — E-waste image classification
    ├── video_analysis.py      # Task 7b — Frame-by-frame video analysis
    ├── industrial_inventory.py # Task 8 — Batches, devices, recovery, inventory
    ├── recovery_intelligence.py # Task 9a — Recovery estimation + recommendations
    ├── economic_analysis.py   # Task 9b — Value estimation + cost analysis
    ├── environmental_impact.py # Task 10a — Environmental metrics + compliance
    ├── report_generator.py    # Task 10b — Downloadable reports (CSV/PDF/MD)
    ├── research_experiments.py # Task 11 — ML experiments, comparison, reproducibility
    └── settings.py            # Task 12 — System status, DB health, model registry
```

## Page Routing

Each page module exports a single `render_*()` function. The router in `app.py` calls it on navigation. Pages are imported lazily (inside the `elif` block) so a broken page does not crash the entire app.

## State Management

Navigation state is stored in `st.session_state.current_page`. On button click the sidebar calls `st.rerun()` to trigger a re-render with the new page key.

Form state within pages uses Streamlit's built-in widget state via unique `key=` arguments.

## Backend Connection

Pages connect to the backend in two ways:

1. **Direct DB access** — `SessionLocal()` from `backend.database` for CRUD operations
2. **Service layer** — Importing service classes (e.g. `AIModelService`, `BatchManagementService`) for business logic

All imports are wrapped in try/except blocks. If a backend service is unavailable, the page shows a clear error and falls back to whatever it can display (empty state, reference data, guide text).

## Error Handling Strategy

| Situation | Behaviour |
|-----------|-----------|
| Database unavailable | Red `st.error()` with error message, page continues with graceful fallback |
| Service unavailable | Orange `st.warning()` + info about what's missing |
| No data yet | Blue `st.info()` with instructions on how to populate |
| Import error (page) | App shows page not found — does NOT crash other pages |
| AI model unavailable | Clear message: "Feature not available until a model is deployed" |

## Loading States

All database queries and AI inference calls that may take time are wrapped with `st.spinner()`. Progress bars (`st.progress()`) are used for multi-step operations like video analysis.
