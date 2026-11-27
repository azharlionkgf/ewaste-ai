# E-Waste AI — Backend Architecture (Phase 4)

## Overview

Phase 4 implements a complete industrial-grade Python backend for the E-Waste AI platform.

## Architecture

```
backend/
├── main.py                    # FastAPI application, lifespan, router registration
├── config.py                  # Environment-based configuration
├── database.py                # SQLAlchemy engine, sessions, init_db
├── models/
│   ├── all_models.py          # All 17 ORM tables
│   └── __init__.py
├── schemas/
│   ├── all_schemas.py         # Pydantic request/response models
│   └── __init__.py
├── services/
│   ├── auth_service.py        # JWT auth, password hashing, rate limiting
│   ├── ai_model_service.py    # AI model loading, inference, registry integration
│   ├── recovery_service.py    # Material recovery intelligence (rule-based)
│   ├── economic_service.py    # Economic analysis engine
│   ├── batch_service.py       # Batch + inventory management
│   ├── decision_service.py    # Recycling decision support
│   ├── environmental_service.py  # Environmental reporting
│   ├── report_service.py      # Report generation (JSON/CSV)
│   └── training_service.py    # ML training (Phase 3)
├── routers/
│   ├── auth.py                # /api/v1/auth — login, register, me
│   ├── batches.py             # /api/v1/batches, /api/v1/recovery, /api/v1/inventory
│   ├── ai_inference.py        # /api/v1/ai — predictions, image classification
│   └── intelligence.py        # Recovery, economics, decisions, environmental, reports
└── middleware/                # (extensible)
```

## Database Tables (17 total)

| Table | Purpose |
|-------|---------|
| `users` | Authentication and role management |
| `audit_logs` | Security audit trail |
| `datasets` | Dataset versions and metadata |
| `ml_models` | Trained model registry |
| `model_evaluations` | Per-split evaluation metrics |
| `waste_batches` | Incoming e-waste batch records |
| `devices` | Individual device records within batches |
| `components` | Device components |
| `materials` | Material composition records |
| `inventory` | Material inventory |
| `recovery_records` | Recovered material records |
| `processing_operations` | Operational step records |
| `operational_costs` | Cost tracking |
| `ai_predictions` | Prediction history with provenance |
| `environmental_reports` | Environmental impact reports |
| `generated_reports` | Report file metadata |
| `research_experiments` | Research experiment records |

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` — Register user
- `POST /api/v1/auth/login` — Login, receive JWT
- `GET /api/v1/auth/me` — Current user

### Batch Management
- `POST /api/v1/batches` — Register incoming batch
- `GET /api/v1/batches` — List batches
- `GET /api/v1/batches/{id}` — Get batch
- `PATCH /api/v1/batches/{id}/status` — Update status
- `GET /api/v1/batches/{id}/history` — Audit history
- `POST /api/v1/batches/{id}/devices` — Add device

### Recovery & Inventory
- `POST /api/v1/recovery` — Record recovered material
- `GET /api/v1/inventory` — List inventory
- `GET /api/v1/inventory/summary` — Aggregated inventory
- `POST /api/v1/inventory` — Add inventory item

### AI Inference
- `GET /api/v1/ai/status` — Model availability
- `GET /api/v1/ai/models` — List trained models
- `POST /api/v1/ai/predict/tabular` — Tabular prediction
- `POST /api/v1/ai/predict/batch` — Batch prediction
- `POST /api/v1/ai/classify/image` — Image classification
- `GET /api/v1/ai/predictions` — Prediction history

### Intelligence
- `POST /api/v1/intelligence/recovery/estimate` — Recovery estimation
- `GET /api/v1/intelligence/recovery/device-types` — Supported types
- `POST /api/v1/intelligence/economics/analyze` — Economic analysis
- `GET /api/v1/intelligence/economics/prices` — Price references
- `POST /api/v1/intelligence/decisions/recommend` — Recycling recommendations
- `POST /api/v1/environmental/report/{batch_id}` — Environmental report
- `GET /api/v1/environmental/summary` — Period summary

### Reports
- `POST /api/v1/reports/batch/{id}` — Batch report
- `POST /api/v1/reports/inventory` — Inventory report
- `POST /api/v1/reports/ai-predictions` — AI prediction report

## Security

- JWT authentication (python-jose)
- bcrypt password hashing (passlib)
- Role-based authorization (admin/manager/operator/researcher)
- File upload validation (type + size)
- Input sanitization
- Rate limiting (in-memory, Redis in production)
- Global exception handler (never exposes internals in production)
- Audit logging

## Running the Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Start API server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# API docs
open http://localhost:8000/docs
```
