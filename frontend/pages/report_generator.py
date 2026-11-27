"""
E-Waste AI — Report Generator
===============================
Task 10 of Phase 5.
Generate downloadable reports: batch, inventory, environmental,
financial, AI prediction and model performance reports.
Connects to backend.services.report_service.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
import io
from datetime import datetime
from frontend.theme import apply_theme, page_header, section_header, COLORS

try:
    from backend.services.report_service import ReportGenerationService
    REPORT_OK = True
except Exception as e:
    REPORT_OK = False
    REPORT_ERR = str(e)

try:
    from backend.database import SessionLocal
    from backend.models.all_models import (
        WasteBatch, RecoveryRecord, Inventory,
        TrainedModel, ModelEvaluation, AIPrediction,
    )
    DB_OK = True
except Exception as e:
    DB_OK = False
    DB_ERR = str(e)

import pandas as pd


def _db():
    if not DB_OK:
        return None
    return SessionLocal()


def render_report_generator():
    apply_theme()
    page_header(
        "Report Generator",
        "Generate downloadable batch, inventory, environmental, financial and AI prediction reports",
        "📄",
    )

    if not DB_OK:
        st.error(f"Database unavailable: {DB_ERR}")
        return

    tabs = st.tabs([
        "📦 Batch Report",
        "⚗️ Material & Inventory",
        "🌱 Environmental",
        "💰 Financial",
        "🤖 AI Predictions",
        "📊 Model Performance",
    ])

    # ── TAB 1: BATCH REPORT ────────────────────────────────────────────
    with tabs[0]:
        section_header("Batch Report")
        db = _db()
        try:
            batches = db.query(WasteBatch).order_by(WasteBatch.created_at.desc()).all()
        except Exception as ex:
            st.error(f"DB error: {ex}")
            batches = []
        finally:
            db.close()

        if not batches:
            st.info("No batches found.")
        else:
            report_type = st.radio("Report Scope", ["All Batches", "Single Batch"], horizontal=True)
            if report_type == "Single Batch":
                batch_map = {b.batch_id: b for b in batches}
                sel = st.selectbox("Select Batch", list(batch_map.keys()))
                report_batches = [batch_map[sel]]
            else:
                report_batches = batches

            if st.button("📄 Generate Batch Report", type="primary"):
                rows = [{
                    "Batch ID": b.batch_id,
                    "Source": b.source,
                    "Category": b.waste_category,
                    "Weight (kg)": b.total_weight_kg,
                    "Status": b.status,
                    "Received": b.received_date,
                    "Notes": b.notes or "",
                } for b in report_batches]
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False).encode()
                st.download_button(
                    "⬇️ Download CSV",
                    csv,
                    file_name=f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                )

                # Try PDF via report service
                if REPORT_OK:
                    try:
                        svc = ReportGenerationService()
                        pdf_bytes = svc.generate_batch_report_pdf(batch_ids=[b.id for b in report_batches])
                        if pdf_bytes:
                            st.download_button(
                                "⬇️ Download PDF",
                                pdf_bytes,
                                file_name=f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                mime="application/pdf",
                            )
                    except Exception as ex:
                        st.caption(f"PDF generation unavailable: {ex}")

    # ── TAB 2: MATERIAL & INVENTORY ────────────────────────────────────
    with tabs[1]:
        section_header("Material Recovery & Inventory Report")

        db2 = _db()
        try:
            records = db2.query(RecoveryRecord).all()
            inventory = db2.query(Inventory).all()
        except Exception as ex:
            st.error(f"DB error: {ex}")
            records, inventory = [], []
        finally:
            db2.close()

        if not records and not inventory:
            st.info("No recovery records or inventory data found.")
        else:
            if st.button("📄 Generate Material Report", type="primary"):
                if records:
                    st.markdown("#### Recovery Records")
                    rec_rows = [{
                        "Batch": r.batch_id,
                        "Material": r.material_name,
                        "Qty (kg)": r.quantity_kg,
                        "Purity %": r.purity_percent,
                        "Method": r.recovery_method,
                        "Source": r.source,
                        "Date": str(r.recorded_at)[:10] if r.recorded_at else "",
                    } for r in records]
                    df_r = pd.DataFrame(rec_rows)
                    st.dataframe(df_r, use_container_width=True)
                    csv_r = df_r.to_csv(index=False).encode()
                    st.download_button(
                        "⬇️ Recovery Records CSV",
                        csv_r,
                        file_name=f"recovery_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                    )

                if inventory:
                    st.markdown("#### Current Inventory")
                    inv_rows = [{
                        "Material": i.material_name,
                        "Qty (kg)": i.quantity_kg,
                        "Location": i.location,
                        "Updated": str(i.updated_at)[:10] if i.updated_at else "",
                    } for i in inventory]
                    df_i = pd.DataFrame(inv_rows)
                    st.dataframe(df_i, use_container_width=True)
                    csv_i = df_i.to_csv(index=False).encode()
                    st.download_button(
                        "⬇️ Inventory CSV",
                        csv_i,
                        file_name=f"inventory_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                    )

    # ── TAB 3: ENVIRONMENTAL ───────────────────────────────────────────
    with tabs[2]:
        section_header("Environmental Summary Report")

        db3 = _db()
        try:
            batches3 = db3.query(WasteBatch).all()
            records3 = db3.query(RecoveryRecord).all()
        except Exception as ex:
            st.error(f"DB error: {ex}")
            batches3, records3 = [], []
        finally:
            db3.close()

        if st.button("📄 Generate Environmental Report", type="primary"):
            total_wt = sum(b.total_weight_kg or 0 for b in batches3)
            total_rec = sum(r.quantity_kg or 0 for r in records3)
            rec_rate = (total_rec / total_wt * 100) if total_wt else 0

            report_md = f"""# Environmental Summary Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Key Metrics
| Metric | Value |
|--------|-------|
| Total E-Waste Registered | {total_wt:.2f} kg |
| Total Material Recovered | {total_rec:.2f} kg |
| Recovery Rate | {rec_rate:.1f}% |
| Total Batches | {len(batches3)} |
| Recovery Records | {len(records3)} |

## Estimated Environmental Benefits (Approximate)
| Benefit | Estimate |
|---------|----------|
| CO₂ Avoided | ~{total_rec * 2.5:.1f} kg (avg. 2.5 kg/kg recovered) |
| Landfill Diverted | ~{total_rec:.1f} kg |

---
*DISCLAIMER: These figures are estimates based on published averages.*
*They do NOT constitute certified environmental compliance documentation.*
*Source: UNEP, EEA reference data.*
"""
            st.markdown(report_md)
            st.download_button(
                "⬇️ Download Report (Markdown)",
                report_md.encode(),
                file_name=f"env_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
            )

    # ── TAB 4: FINANCIAL ───────────────────────────────────────────────
    with tabs[3]:
        section_header("Financial Estimates Report")
        st.warning("⚠️ ESTIMATES ONLY — not official financial statements.")

        db4 = _db()
        try:
            records4 = db4.query(RecoveryRecord).all()
        except Exception:
            records4 = []
        finally:
            db4.close()

        if not records4:
            st.info("No recovery records. Financial estimates require logged material recovery data.")
        else:
            if st.button("📄 Generate Financial Report", type="primary"):
                PRICES = {
                    "gold": 65.0, "silver": 0.80, "copper": 9.0, "aluminum": 2.0,
                    "steel": 0.15, "iron": 0.12, "palladium": 40.0, "platinum": 32.0,
                    "lithium": 15.0, "cobalt": 30.0, "circuit_boards": 10.0,
                }
                fin_rows = []
                total_val = 0.0
                for r in records4:
                    price = PRICES.get(r.material_name, 1.0)
                    val = (r.quantity_kg or 0) * price
                    total_val += val
                    fin_rows.append({
                        "Material": r.material_name,
                        "Qty (kg)": r.quantity_kg,
                        "Est. Price ($/kg)": price,
                        "Est. Value ($)": round(val, 2),
                        "Batch": r.batch_id,
                    })

                df_fin = pd.DataFrame(fin_rows)
                st.dataframe(df_fin, use_container_width=True)
                st.metric("Total Estimated Value", f"${total_val:,.2f} USD")
                st.caption("Prices: LME approximate spot prices (2024 reference). Not real-time.")

                csv_fin = df_fin.to_csv(index=False).encode()
                st.download_button(
                    "⬇️ Download Financial CSV",
                    csv_fin,
                    file_name=f"financial_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                )

    # ── TAB 5: AI PREDICTIONS ──────────────────────────────────────────
    with tabs[4]:
        section_header("AI Prediction History Report")

        db5 = _db()
        try:
            predictions = db5.query(AIPrediction).order_by(
                AIPrediction.created_at.desc()
            ).limit(500).all()
        except Exception as ex:
            st.error(f"DB error: {ex}")
            predictions = []
        finally:
            db5.close()

        if not predictions:
            st.info("No AI predictions recorded yet. Use **E-Waste Analysis** to run predictions.")
        else:
            if st.button("📄 Generate Prediction Report", type="primary"):
                pred_rows = [{
                    "Prediction ID": p.id,
                    "Model ID": p.model_id,
                    "Input Type": p.input_type or "—",
                    "Predicted Class": p.predicted_class or "—",
                    "Confidence": f"{p.confidence:.4f}" if p.confidence else "—",
                    "Date": str(p.created_at)[:16] if p.created_at else "—",
                } for p in predictions]
                df_pred = pd.DataFrame(pred_rows)
                st.dataframe(df_pred, use_container_width=True)
                csv_pred = df_pred.to_csv(index=False).encode()
                st.download_button(
                    "⬇️ Download Predictions CSV",
                    csv_pred,
                    file_name=f"predictions_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                )

    # ── TAB 6: MODEL PERFORMANCE ───────────────────────────────────────
    with tabs[5]:
        section_header("Model Performance Report")

        db6 = _db()
        try:
            models = db6.query(TrainedModel).all()
            evals = db6.query(ModelEvaluation).all()
        except Exception as ex:
            st.error(f"DB error: {ex}")
            models, evals = [], []
        finally:
            db6.close()

        if not models:
            st.info("No trained models found.")
        else:
            if st.button("📄 Generate Model Report", type="primary"):
                eval_map = {e.model_id: e for e in evals}
                mod_rows = []
                for m in models:
                    ev = eval_map.get(m.id)
                    mod_rows.append({
                        "Model Name": m.model_name,
                        "Version": m.version,
                        "Task": m.task_type,
                        "Algorithm": m.algorithm,
                        "Status": m.status,
                        "Accuracy": ev.accuracy if ev else "—",
                        "F1 Score": ev.f1_score if ev else "—",
                        "Train Time (s)": m.training_time_seconds,
                        "Created": str(m.created_at)[:10] if m.created_at else "—",
                    })

                df_mod = pd.DataFrame(mod_rows)
                st.dataframe(df_mod, use_container_width=True)
                csv_mod = df_mod.to_csv(index=False).encode()
                st.download_button(
                    "⬇️ Download Model Report CSV",
                    csv_mod,
                    file_name=f"model_performance_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                )
