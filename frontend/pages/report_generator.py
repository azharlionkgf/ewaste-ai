"""
E-Waste AI — Report Generator (fixed column names)
"""
import os, sys, json as _json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from datetime import datetime
import pandas as pd
from frontend.theme import apply_theme, page_header, section_header

try:
    from backend.database import SessionLocal
    from backend.models.all_models import (
        WasteBatch, RecoveryRecord, Inventory,
        TrainedModel, ModelEvaluation, AIPrediction,
    )
    DB_OK = True
except Exception as e:
    DB_OK = False; DB_ERR = str(e)


def _db():
    return SessionLocal() if DB_OK else None


def _get_metric(ev, key):
    if not ev or not ev.metrics:
        return None
    try:
        m = _json.loads(ev.metrics) if isinstance(ev.metrics, str) else ev.metrics
        return m.get(key) or m.get(f"val_{key}") or m.get(f"test_{key}")
    except Exception:
        return None


def render_report_generator():
    apply_theme()
    page_header("Report Generator",
                "Generate downloadable batch, inventory, environmental, financial and AI reports", "📄")

    if not DB_OK:
        st.error(f"Database unavailable: {DB_ERR}"); return

    tabs = st.tabs(["📦 Batch", "⚗️ Material & Inventory",
                    "🌱 Environmental", "💰 Financial",
                    "🤖 AI Predictions", "📊 Model Performance"])

    # ── TAB 1: BATCH ──────────────────────────────────────────────────
    with tabs[0]:
        section_header("Batch Report")
        db = _db()
        try:
            batches = db.query(WasteBatch).order_by(WasteBatch.created_at.desc()).all()
        except Exception as ex:
            st.error(str(ex)); batches = []
        finally:
            db.close()

        if not batches:
            st.info("No batches found.")
        else:
            scope = st.radio("Scope", ["All Batches","Single Batch"], horizontal=True)
            if scope == "Single Batch":
                bmap = {b.batch_number: b for b in batches}
                sel = st.selectbox("Batch", list(bmap.keys()))
                report_batches = [bmap[sel]]
            else:
                report_batches = batches

            if st.button("📄 Generate Batch Report", type="primary"):
                rows = [{"Batch Number": b.batch_number, "Source": b.source,
                         "Category": b.waste_category, "Weight (kg)": b.total_weight_kg,
                         "Status": b.status, "Received": b.received_date,
                         "Location": b.location or "—", "Notes": b.notes or ""}
                        for b in report_batches]
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True)
                st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode(),
                                   f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", "text/csv")

    # ── TAB 2: MATERIAL & INVENTORY ───────────────────────────────────
    with tabs[1]:
        section_header("Material Recovery & Inventory Report")
        db2 = _db()
        try:
            records = db2.query(RecoveryRecord).all()
            inventory = db2.query(Inventory).all()
        except Exception as ex:
            st.error(str(ex)); records, inventory = [], []
        finally:
            db2.close()

        if not records and not inventory:
            st.info("No recovery or inventory data yet.")
        else:
            if st.button("📄 Generate Material Report", type="primary"):
                if records:
                    st.markdown("#### Recovery Records")
                    rec_rows = [{"Batch": r.batch_id, "Material": r.material_name,
                                 "Qty (g)": r.recovered_quantity_g, "Rate %": r.recovery_rate_percent,
                                 "Method": r.recovery_method, "Est Value $": r.estimated_value_usd,
                                 "Source": r.value_source,
                                 "Date": str(r.recorded_at)[:10] if r.recorded_at else ""}
                                for r in records]
                    df_r = pd.DataFrame(rec_rows)
                    st.dataframe(df_r, use_container_width=True)
                    st.download_button("⬇️ Recovery CSV", df_r.to_csv(index=False).encode(),
                                       f"recovery_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", "text/csv")

                if inventory:
                    st.markdown("#### Current Inventory")
                    inv_rows = [{"Material": i.material_name,
                                 "Qty (g)": i.quantity_g,
                                 "Qty (kg)": round((i.quantity_g or 0)/1000, 4),
                                 "Location": i.location or "—",
                                 "Source": i.source or "—",
                                 "Updated": str(i.updated_at)[:10] if i.updated_at else "—"}
                                for i in inventory]
                    df_i = pd.DataFrame(inv_rows)
                    st.dataframe(df_i, use_container_width=True)
                    st.download_button("⬇️ Inventory CSV", df_i.to_csv(index=False).encode(),
                                       f"inventory_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", "text/csv")

    # ── TAB 3: ENVIRONMENTAL ──────────────────────────────────────────
    with tabs[2]:
        section_header("Environmental Summary Report")
        db3 = _db()
        try:
            batches3 = db3.query(WasteBatch).all()
            records3 = db3.query(RecoveryRecord).all()
        except Exception as ex:
            st.error(str(ex)); batches3, records3 = [], []
        finally:
            db3.close()

        if st.button("📄 Generate Environmental Report", type="primary"):
            total_wt = sum(b.total_weight_kg or 0 for b in batches3)
            total_rec_g = sum(r.recovered_quantity_g or 0 for r in records3)
            total_rec_kg = total_rec_g / 1000.0
            rec_rate = (total_rec_kg / total_wt * 100) if total_wt else 0
            report = f"""# Environmental Summary Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Key Metrics
| Metric | Value |
|--------|-------|
| Total E-Waste Registered | {total_wt:.2f} kg |
| Total Material Recovered | {total_rec_kg:.4f} kg ({total_rec_g:.1f} g) |
| Recovery Rate | {rec_rate:.1f}% |
| Total Batches | {len(batches3)} |
| Recovery Records | {len(records3)} |

## Estimated Environmental Benefits (Approximate)
| Benefit | Estimate |
|---------|----------|
| CO₂ Avoided | ~{total_rec_kg * 2.5:.2f} kg (avg 2.5 kg/kg recovered) |
| Landfill Diverted | ~{total_rec_kg:.4f} kg |

---
*DISCLAIMER: Estimates based on published averages. NOT certified compliance documentation.*
*Source: UNEP, EEA reference data.*"""
            st.markdown(report)
            st.download_button("⬇️ Download Report", report.encode(),
                               f"env_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md", "text/markdown")

    # ── TAB 4: FINANCIAL ──────────────────────────────────────────────
    with tabs[3]:
        section_header("Financial Estimates Report")
        st.warning("⚠️ ESTIMATES ONLY — not official financial statements.")
        db4 = _db()
        try:
            recs4 = db4.query(RecoveryRecord).all()
        except Exception:
            recs4 = []
        finally:
            db4.close()

        if not recs4:
            st.info("No recovery records. Financial estimates require logged material data.")
        else:
            if st.button("📄 Generate Financial Report", type="primary"):
                PRICES = {
                    "gold": 65.0, "gold_traces": 65.0, "silver": 0.80, "silver_traces": 0.80,
                    "copper": 0.009, "aluminum": 0.002, "steel": 0.00015, "steel_iron": 0.00015,
                    "iron": 0.00015, "palladium": 42.0, "palladium_traces": 42.0,
                    "platinum": 31.0, "lithium": 0.012, "cobalt": 0.028,
                    "circuit_boards": 0.010, "other": 0.001,
                }
                fin_rows = []
                total_val = 0.0
                for r in recs4:
                    # quantity is in grams
                    qty_g = r.recovered_quantity_g or 0
                    price = PRICES.get(r.material_name, 0.001)  # USD/g
                    # Use recorded estimated_value if available, else calculate
                    val = r.estimated_value_usd if r.estimated_value_usd else qty_g * price
                    total_val += val
                    fin_rows.append({
                        "Material": r.material_name, "Qty (g)": qty_g,
                        "Price ($/g)": price, "Est. Value ($)": round(val, 4),
                        "Batch": r.batch_id,
                    })
                df_fin = pd.DataFrame(fin_rows)
                st.dataframe(df_fin, use_container_width=True)
                st.metric("Total Estimated Value", f"${total_val:,.4f} USD")
                st.caption("Prices: LME approximate reference (2024-01). Not real-time.")
                st.download_button("⬇️ Financial CSV", df_fin.to_csv(index=False).encode(),
                                   f"financial_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", "text/csv")

    # ── TAB 5: AI PREDICTIONS ─────────────────────────────────────────
    with tabs[4]:
        section_header("AI Prediction History")
        db5 = _db()
        try:
            preds = db5.query(AIPrediction).order_by(AIPrediction.created_at.desc()).limit(500).all()
        except Exception as ex:
            st.error(str(ex)); preds = []
        finally:
            db5.close()

        if not preds:
            st.info("No AI predictions recorded yet. Use E-Waste Analysis or AI Intelligence to run predictions.")
        else:
            if st.button("📄 Generate Prediction Report", type="primary"):
                pred_rows = [{"ID": p.id, "Model": p.model_name or p.model_id,
                              "Version": p.model_version or "—",
                              "Task": p.task_type or "—",
                              "Input Type": p.input_type or "—",
                              "Confidence": f"{p.confidence:.4f}" if p.confidence else "—",
                              "Type": p.prediction_type or "—",
                              "Date": str(p.created_at)[:16] if p.created_at else "—"}
                             for p in preds]
                df_pred = pd.DataFrame(pred_rows)
                st.dataframe(df_pred, use_container_width=True)
                st.download_button("⬇️ Predictions CSV", df_pred.to_csv(index=False).encode(),
                                   f"predictions_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", "text/csv")

    # ── TAB 6: MODEL PERFORMANCE ──────────────────────────────────────
    with tabs[5]:
        section_header("Model Performance Report")
        db6 = _db()
        try:
            models = db6.query(TrainedModel).all()
            evals = {e.model_id: e for e in db6.query(ModelEvaluation).all()}
        except Exception as ex:
            st.error(str(ex)); models, evals = [], {}
        finally:
            db6.close()

        if not models:
            st.info("No trained models found.")
        else:
            if st.button("📄 Generate Model Report", type="primary"):
                mod_rows = [{"Name": m.name, "Version": m.version, "Task": m.task_type,
                             "Algorithm": m.algorithm, "Status": m.status,
                             "Accuracy": _get_metric(evals.get(m.id),"accuracy"),
                             "F1": _get_metric(evals.get(m.id),"f1"),
                             "Train Time (s)": m.training_duration_sec,
                             "File": os.path.basename(m.file_path) if m.file_path else "—",
                             "File OK": os.path.exists(m.file_path) if m.file_path else False,
                             "Created": str(m.created_at)[:10] if m.created_at else "—"}
                            for m in models]
                df_mod = pd.DataFrame(mod_rows)
                st.dataframe(df_mod, use_container_width=True)
                st.download_button("⬇️ Model Report CSV", df_mod.to_csv(index=False).encode(),
                                   f"model_perf_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", "text/csv")
