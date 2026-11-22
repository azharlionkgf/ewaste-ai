# 🛠️ E-WASTE AI — TECHNOLOGY STACK
## Complete Technology Selection with Justifications

**Version:** 2.0.0 | **Date:** 2026-11-22

---

## ENVIRONMENT BASELINE (Detected)

| Component | Version | Status |
|-----------|---------|--------|
| Python | 3.13.7 | ✅ Ready |
| pip | 26.2.1 | ✅ Ready |
| Node.js | v24.21.0 | ✅ Ready (for static assets) |
| CPU | Intel Core i5-1340P (13th Gen, 12 cores) | ✅ Capable |
| RAM | 16 GB | ✅ Sufficient |
| GPU | None detected | ⚠️ CPU mode activated |
| OS | Windows 11 64-bit | ✅ Supported |

---

## 1. FRONTEND

| Technology | Version | Purpose | Why Selected |
|-----------|---------|---------|-------------|
| **Streamlit** | 1.64.0 | Main UI framework | Python-native, rapid development, pre-installed |
| **Custom CSS** | — | Deep charcoal/gold theme injection | Full control over design |
| **Plotly Express** | Pre-installed | Interactive charts, confusion matrices | Best Python charting library |
| **Matplotlib** | Pre-installed | Static plots, training history | Standard academic visualization |
| **Seaborn** | Pre-installed | Heatmaps, correlation plots | Statistical visualization |

### Design System
```
Colors:
  Background:    #0A0A0A  (Near Black)
  Surface:       #141414  (Dark Surface)
  Card:          #1C1C1C  (Card Background)
  Border:        #2D2D2D  (Subtle Border)
  Gold Primary:  #C9A84C  (Primary Accent)
  Gold Light:    #E8C97A  (Hover State)
  Bronze:        #8B6914  (Secondary Accent)
  Text Primary:  #F2F2F2  (Primary Text)
  Text Muted:    #9A9A9A  (Secondary Text)
  Success:       #27AE60
  Warning:       #E67E22
  Error:         #E74C3C
  Info:          #2980B9

Typography:
  Headings:  'Poppins', sans-serif (Google Fonts)
  Body:      'Inter', sans-serif (Google Fonts)
  Code:      'JetBrains Mono', monospace

Spacing Unit: 8px grid
Border Radius: 8px (cards), 4px (buttons)
```

---

## 2. BACKEND

| Technology | Version | Purpose | Why Selected |
|-----------|---------|---------|-------------|
| **FastAPI** | 0.136.1 | REST API framework | Async, auto-docs, WebSocket, pre-installed |
| **Uvicorn** | 0.47.0 | ASGI server | Production-grade, pre-installed |
| **Pydantic** | Pre-installed | Request/response validation | Built into FastAPI |
| **SQLAlchemy** | 2.0.49 | ORM | Async-capable, pre-installed |
| **aiosqlite** | 0.21.0 | Async SQLite | Non-blocking DB operations, pre-installed |
| **Python-multipart** | Pre-installed | File upload handling | Required by FastAPI |
| **Starlette** | 1.0.0 | WebSocket support | Bundled with FastAPI |

### API Architecture Pattern
```
Router Layer      →  Route definitions, request parsing
Service Layer     →  Business logic, orchestration  
Repository Layer  →  Database CRUD operations
Domain Layer      →  E-waste knowledge, rules, calculations
ML Layer          →  Training, inference, evaluation
```

---

## 3. DATABASE

| Technology | Version | Purpose | Why Selected |
|-----------|---------|---------|-------------|
| **SQLite** | Built-in | Primary database | Zero-config, file-based, perfect for local apps |
| **SQLAlchemy ORM** | 2.0.49 | Database abstraction | Prevents SQL injection, clean models |
| **Alembic** | To install | Database migrations | Schema version control |

### Why SQLite (Not PostgreSQL/MySQL)?
- ✅ No separate server process to manage
- ✅ Single `.db` file, easy to backup and share
- ✅ Sufficient for dataset sizes up to ~10GB
- ✅ Perfect for academic demonstrations
- ✅ Upgrade path: swap SQLAlchemy connection string to PostgreSQL later

---

## 4. MACHINE LEARNING

### 4.1 Deep Learning (Image Classification)

| Technology | Version | Purpose |
|-----------|---------|---------|
| **PyTorch** | 2.12.0 | Primary deep learning framework |
| **TorchVision** | 0.27.0 | Pre-trained models (MobileNetV3, EfficientNet, ResNet) |
| **TensorFlow/Keras** | 2.21.0 | Alternative training backend |
| **HuggingFace Transformers** | 5.8.1 | Vision transformers (ViT) |

**Selected Image Model Architectures:**
```
Primary:   MobileNetV3-Small   → Fast, accurate, CPU-friendly (~1.5MB)
Alt 1:     EfficientNet-B0     → Better accuracy, slightly heavier
Alt 2:     ResNet-18            → Classic benchmark baseline
Research:  ViT-Base/16          → Transformer-based (optional)
```

### 4.2 Traditional ML (Tabular Data)

| Technology | Version | Purpose |
|-----------|---------|---------|
| **scikit-learn** | 1.8.0 | Random Forest, SVM, Logistic Regression, preprocessing |
| **XGBoost** | 3.4.1 | Gradient boosting (tabular data) |
| **CatBoost** | 1.2.10 | Categorical feature handling |
| **imbalanced-learn** | To install | SMOTE for class imbalance |

**Algorithm Selection Matrix:**

| Algorithm | Best For | CPU Performance |
|-----------|---------|----------------|
| Random Forest | Baseline, feature importance | ✅ Fast |
| XGBoost | High accuracy tabular | ✅ Fast |
| CatBoost | Categorical-heavy data | ✅ Fast |
| SVM | Small-medium datasets | ⚠️ Slow on large |
| Logistic Regression | Interpretable baseline | ✅ Very fast |
| MobileNetV3 | Image classification | ✅ Acceptable on CPU |
| EfficientNet-B0 | Accurate image classification | ✅ Reasonable |

### 4.3 Experiment Tracking

| Technology | Version | Purpose |
|-----------|---------|---------|
| **MLflow** | To install | Experiment tracking, model registry |
| **Custom DB** | SQLite | Fallback experiment storage |

---

## 5. DATA PROCESSING

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Pandas** | Pre-installed | Tabular data manipulation |
| **NumPy** | Pre-installed | Numerical operations |
| **OpenCV** | Pre-installed | Image processing, video frames |
| **Pillow** | Pre-installed | Image I/O, augmentation |
| **openpyxl** | Pre-installed | Excel file reading/writing |
| **scipy** | Pre-installed | Statistical analysis |

### Data Pipeline
```
Raw Upload (CSV/Excel/JSON/Images)
    │
    ▼ Validation (format, size, type checks)
    │
    ▼ Inspection (shape, dtypes, nulls, uniques)
    │
    ▼ Cleaning (missing values, duplicates, outliers)
    │
    ▼ Preprocessing (encoding, scaling, feature engineering)
    │
    ▼ Splitting (train 70% / val 15% / test 15%)
    │
    ▼ Dataset Export (ready for ML training)
```

---

## 6. VISUALIZATION & REPORTING

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Plotly** | Pre-installed | Interactive charts in Streamlit |
| **Matplotlib** | Pre-installed | Static plot generation for PDFs |
| **Seaborn** | Pre-installed | Heatmaps, distribution plots |
| **ReportLab** | 5.0.1 | PDF report generation |
| **fpdf2** | 2.8.8 | Alternative PDF (lighter weight) |

---

## 7. TESTING

| Technology | Version | Purpose |
|-----------|---------|---------|
| **pytest** | Pre-installed | Unit and integration tests |
| **pytest-asyncio** | To install | Async test support |
| **httpx** | Pre-installed | FastAPI test client |
| **coverage** | To install | Code coverage reports |

---

## 8. DEVOPS & UTILITIES

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Git** | 2.56.0 | Version control |
| **python-dotenv** | Pre-installed | Environment variable management |
| **PyYAML** | Pre-installed | Configuration files |
| **Rich** | Pre-installed | Colorized terminal logging |
| **Loguru / logging** | Built-in | Structured application logging |
| **joblib** | Pre-installed | Model serialization (sklearn models) |
| **pathlib** | Built-in | Cross-platform file paths |

---

## 9. PACKAGES TO INSTALL

The following packages are NOT pre-installed and will be installed during setup:

```bash
pip install alembic mlflow imbalanced-learn pytest-asyncio coverage
```

---

## 10. WHAT WE ARE NOT USING (AND WHY)

| Technology | Reason Excluded |
|-----------|----------------|
| Docker | Not needed for local deployment; adds complexity |
| PostgreSQL | SQLite sufficient; easier for academic environment |
| Redis | No need for distributed caching at this scale |
| Celery | FastAPI BackgroundTasks handles async training adequately |
| React/Next.js | Streamlit is faster to develop and Python-native |
| Paid AI APIs | All inference runs locally |
| Three.js / 3D | Explicitly excluded per project requirements |
| Cloud Storage | All storage is local; filesystem-based |

---

## 11. REQUIREMENTS.TXT PREVIEW

```text
# Web Framework
fastapi==0.136.1
uvicorn==0.47.0
python-multipart

# Database
sqlalchemy==2.0.49
aiosqlite==0.21.0
alembic

# Frontend
streamlit==1.64.0

# Machine Learning
torch==2.12.0
torchvision==0.27.0
scikit-learn==1.8.0
xgboost==3.4.1
catboost==1.2.10
transformers==5.8.1
mlflow
imbalanced-learn

# Data Processing
pandas
numpy
opencv-python
Pillow
openpyxl
scipy

# Visualization & Reporting
plotly
matplotlib
seaborn
reportlab==5.0.1
fpdf2==2.8.8

# Testing
pytest
pytest-asyncio
httpx
coverage

# Utilities
python-dotenv
pyyaml
rich
joblib
```
