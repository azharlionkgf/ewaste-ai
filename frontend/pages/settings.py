"""
E-Waste AI — Application Settings
====================================
Task 12 of Phase 5.
System information, database health, AI model status and configuration.
"""

import os, sys, platform
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from datetime import datetime
from frontend.theme import apply_theme, page_header, section_header, status_badge, COLORS


def render_settings():
    apply_theme()
    page_header(
        "Settings & System Status",
        "Database health, AI model registry, environment info and configuration",
        "⚙️",
    )

    tabs = st.tabs(["🗄️ Database", "🤖 AI Models", "🖥️ System Info", "🔧 Configuration"])

    # ── TAB 1: DATABASE ────────────────────────────────────────────────
    with tabs[0]:
        section_header("Database Status")

        try:
            from backend.database import SessionLocal, engine, DATABASE_URL
            db = SessionLocal()

            # Health check
            try:
                db.execute(__import__('sqlalchemy').text("SELECT 1"))
                db_healthy = True
            except Exception:
                db_healthy = False
            finally:
                db.close()

            sb = status_badge("Healthy ✅", "success") if db_healthy else status_badge("Error ❌", "error")
            st.markdown(f"**Connection Status:** {sb}", unsafe_allow_html=True)
            st.markdown(f"**URL:** `{DATABASE_URL}`")

        except Exception as ex:
            st.error(f"Database module unavailable: {ex}")
            st.stop()

        # Table row counts
        section_header("Table Row Counts")
        try:
            from backend.models.all_models import (
                WasteBatch, Device, Component, Material,
                RecoveryRecord, Inventory, TrainedModel,
                ModelEvaluation, AIPrediction, ResearchExperiment,
                OperationalCost, EnvironmentalReport,
            )
            db2 = SessionLocal()
            tables = {
                "Waste Batches": WasteBatch,
                "Devices": Device,
                "Components": Component,
                "Materials": Material,
                "Recovery Records": RecoveryRecord,
                "Inventory": Inventory,
                "Trained Models": TrainedModel,
                "Model Evaluations": ModelEvaluation,
                "AI Predictions": AIPrediction,
                "Research Experiments": ResearchExperiment,
                "Operational Costs": OperationalCost,
                "Environmental Reports": EnvironmentalReport,
            }
            cols = st.columns(3)
            for idx, (name, model) in enumerate(tables.items()):
                try:
                    count = db2.query(model).count()
                    cols[idx % 3].metric(name, count)
                except Exception:
                    cols[idx % 3].metric(name, "N/A")
            db2.close()
        except Exception as ex:
            st.warning(f"Could not load table counts: {ex}")

        # Database file info
        try:
            db_path = DATABASE_URL.replace("sqlite:///", "").replace("sqlite+aiosqlite:///", "")
            if os.path.exists(db_path):
                size_mb = os.path.getsize(db_path) / 1024 / 1024
                mtime = datetime.fromtimestamp(os.path.getmtime(db_path))
                st.markdown(f"**DB File Size:** {size_mb:.2f} MB")
                st.markdown(f"**Last Modified:** {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception:
            pass

    # ── TAB 2: AI MODELS ──────────────────────────────────────────────
    with tabs[1]:
        section_header("AI Model Registry")

        try:
            from backend.services.ai_model_service import AIModelService
            svc = AIModelService()
            models = svc.list_available_models()

            if not models:
                st.info(
                    "No models currently deployed. "
                    "Train and register models in the **Model Training** workspace."
                )
            else:
                for m in models:
                    sb = status_badge(m.get("status", "unknown"), "success" if m.get("status") == "active" else "warning")
                    with st.expander(
                        f"🤖 {m.get('name', 'Unknown')} v{m.get('version', '?')}  {sb}",
                        expanded=False,
                    ):
                        c1, c2 = st.columns(2)
                        c1.markdown(f"**Model ID:** `{m.get('model_id', '—')}`")
                        c1.markdown(f"**Task Type:** {m.get('task_type', '—')}")
                        c1.markdown(f"**Algorithm:** {m.get('algorithm', '—')}")
                        c2.markdown(f"**Status:** {m.get('status', '—')}")
                        c2.markdown(f"**Created:** {str(m.get('created_at', '—'))[:10]}")
                        if m.get("model_path"):
                            exists = os.path.exists(m["model_path"])
                            file_ok = status_badge("File Found ✅", "success") if exists else status_badge("File Missing ❌", "error")
                            st.markdown(f"**Model File:** {file_ok}", unsafe_allow_html=True)
                            st.markdown(f"`{m.get('model_path')}`")

        except Exception as ex:
            st.error(f"AI Model Service unavailable: {ex}")

        # Saved models directory
        section_header("Saved Models Directory")
        saved_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'saved_models')
        saved_dir = os.path.abspath(saved_dir)
        if os.path.exists(saved_dir):
            files = []
            for root, dirs, fnames in os.walk(saved_dir):
                for f in fnames:
                    fp = os.path.join(root, f)
                    size_kb = os.path.getsize(fp) / 1024
                    rel = os.path.relpath(fp, saved_dir)
                    files.append({"File": rel, "Size (KB)": round(size_kb, 1)})
            if files:
                import pandas as pd
                st.dataframe(pd.DataFrame(files), use_container_width=True)
            else:
                st.info("No model files found in saved_models/")
        else:
            st.warning(f"saved_models/ directory not found at: {saved_dir}")

    # ── TAB 3: SYSTEM INFO ─────────────────────────────────────────────
    with tabs[2]:
        section_header("Environment & System Information")

        c1, c2 = st.columns(2)
        c1.markdown(f"**Python Version:** {sys.version.split()[0]}")
        c1.markdown(f"**Platform:** {platform.system()} {platform.release()}")
        c1.markdown(f"**Architecture:** {platform.machine()}")

        # Key library versions
        libs = ["streamlit", "fastapi", "sqlalchemy", "scikit-learn", "xgboost",
                "pandas", "numpy", "pydantic"]
        versions = {}
        for lib in libs:
            try:
                mod = __import__(lib.replace("-", "_").replace("scikit_learn", "sklearn"))
                versions[lib] = getattr(mod, "__version__", "?")
            except Exception:
                versions[lib] = "not installed"

        c2.markdown("**Library Versions:**")
        for lib, ver in versions.items():
            c2.markdown(f"- `{lib}`: {ver}")

        # Disk usage
        section_header("Disk Usage")
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        dirs_to_check = ["data", "saved_models", "database", "reports", "logs"]
        for d in dirs_to_check:
            dp = os.path.join(project_root, d)
            if os.path.exists(dp):
                total = sum(
                    os.path.getsize(os.path.join(root, f))
                    for root, dirs, files in os.walk(dp)
                    for f in files
                ) / 1024 / 1024
                st.markdown(f"**{d}/:** {total:.2f} MB")

        # ML availability
        section_header("ML Library Availability")
        ml_libs = {
            "scikit-learn": "sklearn",
            "xgboost": "xgboost",
            "PyTorch": "torch",
            "OpenCV": "cv2",
            "Pillow": "PIL",
        }
        for name, mod_name in ml_libs.items():
            try:
                __import__(mod_name)
                st.markdown(f"✅ **{name}** — available")
            except ImportError:
                st.markdown(f"❌ **{name}** — not installed")

    # ── TAB 4: CONFIGURATION ──────────────────────────────────────────
    with tabs[3]:
        section_header("Application Configuration")

        try:
            from backend.config import settings
            config_items = {
                "App Name": settings.APP_NAME,
                "Debug Mode": str(getattr(settings, "DEBUG", False)),
                "Database URL": getattr(settings, "DATABASE_URL", "—"),
                "Max Upload Size (MB)": str(getattr(settings, "MAX_UPLOAD_SIZE_MB", "—")),
                "Models Directory": str(getattr(settings, "MODELS_DIR", "—")),
                "Log Level": str(getattr(settings, "LOG_LEVEL", "INFO")),
            }
            for k, v in config_items.items():
                st.markdown(f"**{k}:** `{v}`")
        except Exception as ex:
            st.warning(f"Could not load settings: {ex}")

        section_header("Environment Variables")
        env_vars = ["DATABASE_URL", "SECRET_KEY", "DEBUG", "LOG_LEVEL", "MODELS_DIR"]
        for var in env_vars:
            val = os.environ.get(var, None)
            if val:
                display = val if var not in ("SECRET_KEY",) else "***hidden***"
                st.markdown(f"**{var}:** `{display}`")
            else:
                st.markdown(f"**{var}:** *(not set — using default)*")

        st.markdown("---")
        st.caption(
            "⚙️ To change configuration, edit `.env` in the project root or set environment variables. "
            "Settings are loaded at startup."
        )
