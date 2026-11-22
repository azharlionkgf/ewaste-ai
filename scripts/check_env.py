"""
E-Waste AI — Project Health Check Script
==========================================
Verifies environment, imports, and project structure.

Usage:
    python scripts/check_env.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def check(label: str, fn):
    try:
        result = fn()
        print(f"  ✅ {label}" + (f": {result}" if result else ""))
        return True
    except Exception as e:
        print(f"  ❌ {label}: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("  E-WASTE AI — ENVIRONMENT HEALTH CHECK")
    print("=" * 60)

    failures = 0

    print("\n📦 Python Environment:")
    failures += not check("Python version", lambda: f"{sys.version.split()[0]}")

    print("\n📚 Core Libraries:")
    failures += not check("FastAPI", lambda: __import__("fastapi").__version__)
    failures += not check("Streamlit", lambda: __import__("streamlit").__version__)
    failures += not check("SQLAlchemy", lambda: __import__("sqlalchemy").__version__)
    failures += not check("Pandas", lambda: __import__("pandas").__version__)
    failures += not check("NumPy", lambda: __import__("numpy").__version__)

    print("\n🤖 Machine Learning Libraries:")
    failures += not check("PyTorch", lambda: __import__("torch").__version__)
    failures += not check("TorchVision", lambda: __import__("torchvision").__version__)
    failures += not check("scikit-learn", lambda: __import__("sklearn").__version__)
    failures += not check("XGBoost", lambda: __import__("xgboost").__version__)
    failures += not check("CatBoost", lambda: __import__("catboost").__version__)
    failures += not check("Transformers", lambda: __import__("transformers").__version__)

    print("\n🖼️  Image & Video:")
    failures += not check("OpenCV", lambda: __import__("cv2").__version__)
    failures += not check("Pillow", lambda: __import__("PIL").__version__)

    print("\n📊 Visualization & Reporting:")
    failures += not check("Plotly", lambda: __import__("plotly").__version__)
    failures += not check("Matplotlib", lambda: __import__("matplotlib").__version__)
    failures += not check("Seaborn", lambda: __import__("seaborn").__version__)
    failures += not check("ReportLab", lambda: __import__("reportlab").__version__)

    print("\n📁 Project Structure:")
    required_dirs = [
        "backend", "ml", "intelligence", "frontend",
        "data/uploads", "data/processed", "data/images",
        "saved_models", "reports", "tests", "docs", "logs"
    ]
    for d in required_dirs:
        failures += not check(f"Directory: {d}", lambda d=d: os.path.isdir(d) or (_ for _ in ()).throw(Exception("Missing")))

    required_files = [
        "app.py", "backend/main.py", "backend/config.py",
        "backend/database.py", "config.yaml", "requirements.txt",
        "README.md", ".gitignore", "TASK_STATUS.md"
    ]
    for f in required_files:
        failures += not check(f"File: {f}", lambda f=f: os.path.isfile(f) or (_ for _ in ()).throw(Exception("Missing")))

    print("\n" + "=" * 60)
    if failures == 0:
        print("  🎉 ALL CHECKS PASSED — Ready to build!")
    else:
        print(f"  ⚠️  {failures} check(s) failed — review above")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
