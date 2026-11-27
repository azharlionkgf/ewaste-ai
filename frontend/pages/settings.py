"""E-Waste AI — Settings & System Status (fixed column names)"""
import os, sys, platform, json as _json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from datetime import datetime
from frontend.theme import apply_theme, page_header, section_header, status_badge


def render_settings():
    apply_theme()
    page_header("Settings & System Status",
                "Database health, AI model registry, environment info and configuration", "⚙️")

    tabs = st.tabs(["🗄️ Database", "🤖 AI Models", "🖥️ System Info", "🔧 Configuration"])

    with tabs[0]:
        section_header("Database Status")
        try:
            from backend.database import SessionLocal, DATABASE_URL
            db = SessionLocal()
            try:
                from sqlalchemy import text
                db.execute(text("SELECT 1"))
                db_ok = True
            except Exception:
                db_ok = False
            finally:
                db.close()

            sb = status_badge("Healthy ✅","success") if db_ok else status_badge("Error ❌","error")
            st.markdown(f"**Status:** {sb}", unsafe_allow_html=True)
            st.markdown(f"**URL:** `{DATABASE_URL}`")
        except Exception as ex:
            st.error(f"Database module unavailable: {ex}"); return

        section_header("Table Row Counts")
        try:
            from backend.database import SessionLocal as SL
            from backend.models.all_models import (
                WasteBatch, Device, RecoveryRecord, Inventory,
                TrainedModel, ModelEvaluation, AIPrediction, ResearchExperiment,
                OperationalCost, EnvironmentalReport, Dataset, AuditLog,
            )
            db2 = SL()
            tbl = {"Waste Batches": WasteBatch, "Devices": Device, "Recovery Records": RecoveryRecord,
                   "Inventory Items": Inventory, "Trained Models": TrainedModel,
                   "Model Evaluations": ModelEvaluation, "AI Predictions": AIPrediction,
                   "Research Experiments": ResearchExperiment, "Operational Costs": OperationalCost,
                   "Env. Reports": EnvironmentalReport, "Datasets": Dataset, "Audit Logs": AuditLog}
            cols = st.columns(3)
            for idx, (name, model) in enumerate(tbl.items()):
                try: cnt = db2.query(model).count()
                except: cnt = "N/A"
                cols[idx % 3].metric(name, cnt)
            db2.close()
        except Exception as ex:
            st.warning(f"Table counts unavailable: {ex}")

        try:
            db_path = DATABASE_URL.replace("sqlite:///","").replace("sqlite+aiosqlite:///","")
            if os.path.exists(db_path):
                size_mb = os.path.getsize(db_path)/1024/1024
                mtime = datetime.fromtimestamp(os.path.getmtime(db_path))
                st.markdown(f"**DB Size:** {size_mb:.2f} MB · **Modified:** {mtime.strftime('%Y-%m-%d %H:%M')}")
        except Exception:
            pass

    with tabs[1]:
        section_header("AI Model Registry")
        try:
            from backend.database import SessionLocal as SL
            from backend.models.all_models import TrainedModel, ModelEvaluation
            db3 = SL()
            models = db3.query(TrainedModel).all()
            evals  = {e.model_id: e for e in db3.query(ModelEvaluation).all()}
            db3.close()
            if not models:
                st.info("No trained models. Use **Model Training** to train your first model.")
            else:
                for m in models:
                    sb = status_badge(m.status or "unknown",
                                      "success" if m.status == "active" else "warning")
                    with st.expander(f"🤖 {m.name} v{m.version}  {sb}"):
                        c1, c2 = st.columns(2)
                        c1.markdown(f"**Task:** {m.task_type or '—'}")
                        c1.markdown(f"**Algorithm:** {m.algorithm or '—'}")
                        c1.markdown(f"**Status:** {m.status or '—'}")
                        c2.markdown(f"**Train time:** {m.training_duration_sec or '—'} s")
                        c2.markdown(f"**Created:** {str(m.created_at)[:10] if m.created_at else '—'}")
                        if m.file_path:
                            exists = os.path.exists(m.file_path)
                            c2.markdown(f"**File:** {'✅' if exists else '❌'} `{m.file_path}`")
        except Exception as ex:
            st.error(f"Model service unavailable: {ex}")

        section_header("Saved Models Directory")
        saved_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','saved_models'))
        if os.path.exists(saved_dir):
            files = []
            for root, dirs, fnames in os.walk(saved_dir):
                for f in fnames:
                    fp = os.path.join(root, f)
                    files.append({"File": os.path.relpath(fp, saved_dir),
                                  "Size (KB)": round(os.path.getsize(fp)/1024, 1)})
            if files:
                import pandas as pd
                st.dataframe(pd.DataFrame(files), use_container_width=True)
            else:
                st.info("No model files in saved_models/")
        else:
            st.warning(f"saved_models/ not found at: {saved_dir}")

    with tabs[2]:
        section_header("System Information")
        c1, c2 = st.columns(2)
        c1.markdown(f"**Python:** {sys.version.split()[0]}")
        c1.markdown(f"**Platform:** {platform.system()} {platform.release()}")
        c1.markdown(f"**Architecture:** {platform.machine()}")
        libs = ["streamlit","sqlalchemy","scikit-learn","xgboost","pandas","numpy","pydantic"]
        c2.markdown("**Key Libraries:**")
        for lib in libs:
            try:
                mod = __import__(lib.replace("-","_").replace("scikit_learn","sklearn"))
                ver = getattr(mod,"__version__","?")
            except Exception:
                ver = "not installed"
            c2.markdown(f"- `{lib}`: {ver}")

        section_header("ML Library Availability")
        for name, mod_name in [("scikit-learn","sklearn"),("xgboost","xgboost"),
                                ("PyTorch","torch"),("OpenCV","cv2"),("Pillow","PIL")]:
            try:
                __import__(mod_name)
                st.markdown(f"✅ **{name}** — available")
            except ImportError:
                st.markdown(f"❌ **{name}** — not installed")

    with tabs[3]:
        section_header("Application Configuration")
        try:
            from backend.config import settings
            for k, v in [("App Name", settings.APP_NAME),
                          ("Debug", str(getattr(settings,"DEBUG",False))),
                          ("Database URL", getattr(settings,"DATABASE_URL","—")),
                          ("Log Level", str(getattr(settings,"LOG_LEVEL","INFO")))]:
                st.markdown(f"**{k}:** `{v}`")
        except Exception as ex:
            st.warning(f"Config unavailable: {ex}")

        section_header("Environment Variables")
        for var in ["DATABASE_URL","SECRET_KEY","DEBUG","LOG_LEVEL"]:
            val = os.environ.get(var)
            if val:
                display = "***hidden***" if var == "SECRET_KEY" else val
                st.markdown(f"**{var}:** `{display}`")
            else:
                st.markdown(f"**{var}:** *(not set — using default)*")
