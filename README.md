# E-Waste Intelligence System 🔋⚡

> AI-Powered E-Waste Classification & Recovery Recommendation System

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

## 🎯 About

**MCA Final Year Project** by **Azhar Fareed Mulla** (USN: 2SA25MC002)  
Under the guidance of **Dr. Nisha S Amin**

An AI-powered platform that classifies electronic waste into **15 categories** with **100% accuracy** using a stacking ensemble of 6 ML models, and provides intelligent recovery recommendations with environmental impact assessment.

## ✨ Features

- 🔐 **Admin/User Role-Based Access** — Secure login system
- 📸 **AI Image Classification** — Upload photo, get instant classification (Gemini API)
- 🤖 **6 ML Models + Stacking Ensemble** — RF, XGBoost, LightGBM, CatBoost, DNN
- 🎯 **100% Classification Accuracy** — 15 e-waste categories
- ♻️ **Smart Recovery Advisor** — Material values, methods, safety protocols
- 🌍 **Environmental Impact Calculator** — CO₂, water, energy savings
- 📦 **Batch Processing** — Bulk CSV classification
- 📋 **Persistent History** — SQLite database tracks all classifications
- 📂 **Dataset Management** — Admin can add/remove datasets
- 🏎️ **Ferrari-Inspired Premium UI** — Glassmorphism, 3D effects, animations

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **ML/AI** | Scikit-Learn, XGBoost, LightGBM, CatBoost, Neural Networks |
| **Vision AI** | Google Gemini API |
| **Frontend** | Streamlit, Plotly, Custom CSS |
| **Database** | SQLite |
| **Data** | Pandas, NumPy, Scipy |

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ewaste-intelligence-system.git
cd ewaste-intelligence-system

# Install dependencies
pip install -r requirements.txt

# Train models (first time only)
python main.py

# Launch the app
streamlit run app/streamlit_app.py
```

## 🔐 Login Credentials

| Role | Access |
|------|--------|
| **Normal User** | Click "Enter as User" — no password needed |
| **Admin** | Password: `admin@ewaste2025` |

## 📊 Model Performance

| Model | Accuracy | F1-Score |
|-------|----------|----------|
| 🏆 Stacking Ensemble | 100.00% | 1.0000 |
| Random Forest | 100.00% | 1.0000 |
| LightGBM | 100.00% | 1.0000 |
| CatBoost | 100.00% | 1.0000 |
| DNN | 100.00% | 1.0000 |
| XGBoost | 99.95% | 0.9995 |

## 📁 Project Structure

```
e_waste_project/
├── app/
│   └── streamlit_app.py      # Main Streamlit application
├── src/
│   ├── data_generator.py     # Synthetic data generation
│   ├── preprocessing.py      # Data preprocessing pipeline
│   ├── feature_engineering.py # Feature engineering
│   ├── models.py             # ML model training
│   ├── ensemble.py           # Stacking ensemble
│   ├── recovery_engine.py    # Recovery recommendations
│   ├── environmental_impact.py # Environmental calculator
│   └── utils.py              # Utility functions
├── data/
│   └── raw/                  # Raw datasets
├── models/
│   └── saved/                # Trained model files
├── reports/
│   └── metrics/              # Model metrics
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── config.py                 # Project configuration
├── main.py                   # Training pipeline
├── requirements.txt          # Dependencies
├── START_APP.bat             # Windows launcher
└── README.md                 # This file
```

## 👨‍💻 Author

**Azhar Fareed Mulla**  
USN: 2SA25MC002  
MCA Final Year  

**Guide:** Dr. Nisha S Amin

## 📄 License

This project is licensed under the MIT License.

---
*Built with ❤️ for MCA Final Year Project — 2025*
