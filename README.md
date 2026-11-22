# ♻️ E-WASTE AI
### Combined Industrial Intelligence, Academic Research & Recycling Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13.7-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.12.0-orange?style=for-the-badge&logo=pytorch)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136.1-green?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-gold?style=for-the-badge)

**An industry-grade, academically rigorous, research-ready AI platform for electronic waste classification, material recovery analysis, and recycling intelligence.**

</div>

---

## 🎯 WHAT IS E-WASTE AI?

E-Waste AI is a full-stack AI platform serving three simultaneous roles:

| Role | Audience | Purpose |
|------|----------|---------|
| 🎓 **Academic Platform** | Students & Professors | Full dataset→training→evaluation workflow |
| 🏭 **Industrial Tool** | E-Waste Recycling Companies | Batch tracking, AI classification, recovery valuation |
| 🔬 **Research Platform** | Researchers | Reproducible experiments, provenance, paper generation |

---

## ✨ KEY FEATURES

### 🤖 AI & Machine Learning
- **Multi-model training**: MobileNetV3, EfficientNet-B0, ResNet-18 (CNN) + Random Forest, XGBoost, CatBoost, SVM (Tabular)
- **Transfer Learning**: Fine-tune pre-trained ImageNet models on e-waste data
- **Real-time training progress**: WebSocket live updates (loss, accuracy, ETA)
- **Model comparison**: Compare all trained models side-by-side
- **100% local inference**: No cloud, no paid APIs, CPU-compatible

### 📊 Data Pipeline
- **Multi-format ingestion**: CSV, Excel, JSON, Image datasets (zip/folder)
- **Automated cleaning**: Missing values, duplicates, outliers, type errors
- **Reproducible preprocessing**: Saved configs, versioned datasets
- **Stratified splitting**: Train/Validation/Test with configurable ratios

### 🏭 Industrial Workflow
- **Waste batch registration**: Track incoming e-waste by source, weight, date
- **AI classification**: Automatically identify device type, condition, hazard level
- **Material recovery estimation**: Gold, silver, copper, lithium extraction estimates
- **Economic valuation**: Market-price-based recovery value calculation
- **Full workflow**: Intake → Classification → Sorting → Processing → Report

### 🔬 Research Tools
- **Experiment tracking**: Hyperparameters, datasets, metrics per run
- **Dataset provenance**: SHA256 checksums, source, license, annotation metadata
- **Baseline comparisons**: Compare against published benchmarks
- **Reproducibility**: Fixed seeds, versioned configs, full environment logging
- **Academic reports**: Auto-generated research report PDFs

### 🌍 Environmental & Economic Analysis
- **CO₂ savings estimation**: Based on diversion from landfill
- **Toxicity reduction**: Hazardous material containment tracking
- **Economic ROI**: Processing cost vs. recovery value analysis

---

## 🗂️ PROJECT STRUCTURE

```
ewaste-ai/
├── app.py                      ← Streamlit entry point
├── README.md
├── TASK_STATUS.md              ← Development tracker
├── requirements.txt
├── .env.example
├── config.yaml
│
├── docs/                       ← Architecture documentation
│   ├── PROJECT_ARCHITECTURE.md
│   ├── TECHNOLOGY_STACK.md
│   ├── DATABASE_DESIGN.md
│   ├── RESEARCH_ARCHITECTURE.md
│   └── DEVELOPMENT_ROADMAP.md
│
├── backend/                    ← FastAPI backend
│   ├── main.py
│   ├── database.py
│   ├── models/                 ← SQLAlchemy ORM models
│   ├── schemas/                ← Pydantic schemas
│   ├── routers/                ← API route handlers
│   └── services/               ← Business logic
│
├── ml/                         ← Machine Learning engine
│   ├── models/                 ← CNN + Traditional ML
│   ├── training/               ← Training pipeline
│   ├── evaluation/             ← Metrics, visualization
│   ├── inference/              ← Prediction engine
│   └── data/                   ← Data pipeline
│
├── intelligence/               ← E-waste domain knowledge
│   ├── device_database.py
│   ├── material_database.py
│   ├── recovery_engine.py
│   ├── environmental_engine.py
│   └── economic_engine.py
│
├── frontend/                   ← Streamlit pages
│   ├── theme.py
│   ├── components/
│   └── pages/
│
├── data/                       ← Data storage (git-ignored)
│   ├── uploads/
│   ├── processed/
│   ├── images/
│   └── videos/
│
├── database/                   ← SQLite database
│   └── ewaste_ai.db
│
├── saved_models/               ← Trained model artifacts
├── reports/                    ← Generated PDF reports
├── tests/                      ← Test suite
└── logs/                       ← Application logs
```

---

## 🚀 QUICK START

### Prerequisites
- Python 3.10+
- pip
- 8GB+ RAM recommended
- CPU: Any modern x86-64 processor (GPU optional)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/azharlionkgf/ewaste-ai.git
cd ewaste-ai

# 2. Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# Edit .env with your settings

# 5. Initialize database
python scripts/init_db.py

# 6. Start the backend API
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 7. Start the frontend (in a new terminal)
streamlit run app.py
```

### Access Points
- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

---

## 📈 SUPPORTED E-WASTE CATEGORIES

| Category | Examples |
|---------|---------|
| 📱 Mobile Devices | Smartphones, Tablets, Feature Phones |
| 💻 Computing | Laptops, Desktops, Servers |
| 🖥️ Displays | Monitors, TVs (LCD, LED, OLED, Plasma) |
| 🔋 Power | Batteries (Li-ion, Lead-acid, NiMH), Chargers |
| 🔌 Peripherals | Cables, Printers, Keyboards, Mice |
| 🔧 Components | PCBs, Motherboards, CPUs, RAM, GPUs, HDDs |
| 🏠 Household | Small appliances, Audio equipment |
| 🏭 Industrial | Industrial PCBs, Control systems |

---

## 🛠️ TECHNOLOGY STACK

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit 1.64 + Custom CSS (Charcoal/Gold) |
| **Backend** | FastAPI 0.136 + Uvicorn |
| **Database** | SQLite + SQLAlchemy 2.0 ORM |
| **Deep Learning** | PyTorch 2.12 + TorchVision |
| **Traditional ML** | scikit-learn 1.8 + XGBoost + CatBoost |
| **NLP/Vision** | HuggingFace Transformers 5.8 |
| **Data** | Pandas + NumPy + OpenCV + Pillow |
| **Charts** | Plotly + Matplotlib + Seaborn |
| **Reports** | ReportLab 5.0 |
| **Experiments** | MLflow |

---

## 🗺️ DEVELOPMENT PHASES

| Phase | Status | Description |
|-------|--------|-------------|
| P0 — Architecture | ✅ Done | Foundation, design, documentation |
| P1 — Dataset Management | 🔲 Next | Upload, inspect, version datasets |
| P2 — Data Pipeline | 🔲 Pending | Cleaning, preprocessing, splitting |
| P3 — Dataset Prep | 🔲 Pending | PyTorch datasets, augmentation |
| P4 — ML Training | 🔲 Pending | CNN + traditional ML training |
| P5 — Evaluation | 🔲 Pending | Metrics, comparison, research |
| P6 — Backend API | 🔲 Pending | Full REST API + WebSocket |
| P7 — Frontend UI | 🔲 Pending | All pages with premium design |
| P8 — Integration | 🔲 Pending | Testing, documentation, launch |

---

## 📚 DOCUMENTATION

| Document | Description |
|---------|-------------|
| [Project Architecture](docs/PROJECT_ARCHITECTURE.md) | System design and module overview |
| [Technology Stack](docs/TECHNOLOGY_STACK.md) | Full technology selection with justifications |
| [Database Design](docs/DATABASE_DESIGN.md) | Schema, ERD, and data integrity rules |
| [Research Architecture](docs/RESEARCH_ARCHITECTURE.md) | Experiment tracking and reproducibility |
| [Development Roadmap](docs/DEVELOPMENT_ROADMAP.md) | Detailed phase-by-phase task breakdown |
| [Task Status](TASK_STATUS.md) | Live development tracker |

---

## ⚠️ IMPORTANT NOTES

> All **material recovery estimates** are based on published scientific literature and are clearly labeled as **estimates** in the UI. No fabricated or fake AI predictions are generated anywhere in this platform.

> All **economic valuations** are estimates based on current market prices and published recovery efficiency data. They should be treated as indicative values only.

---

## 👨‍💻 AUTHOR

**Adil** | GitHub: [@azharlionkgf](https://github.com/azharlionkgf)  
**Project Type:** Academic Final Year Project + Industrial Tool + Research Platform  
**Institution:** [Your College/University Name]

---

## 📄 LICENSE

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
<strong>Built with ❤️ for E-Waste Awareness, Research, and Industry</strong><br>
<em>Using 100% open-source technologies. No mandatory paid APIs.</em>
</div>
