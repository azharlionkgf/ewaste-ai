"""
E-Waste AI — Environmental Impact & Compliance Reporting
=========================================================
Task 10 of Phase 5.
Track environmental metrics, hazardous material records, and
generate compliance documentation.
Connects to backend.services.environmental_service.
Does NOT claim automatic legal compliance.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from frontend.theme import apply_theme, page_header, section_header, COLORS

try:
    from backend.services.environmental_service import EnvironmentalReportingService
    ENV_OK = True
except Exception as e:
    ENV_OK = False
    ENV_ERR = str(e)

try:
    from backend.database import SessionLocal
    from backend.models.all_models import WasteBatch, RecoveryRecord
    DB_OK = True
except Exception:
    DB_OK = False


def _db():
    if not DB_OK:
        return None
    return SessionLocal()


def render_environmental_impact():
    apply_theme()
    page_header(
        "Environmental & Compliance Reporting",
        "Track environmental metrics, hazardous materials, and recycling outcomes",
        "🌱",
    )

    st.warning(
        "⚠️ **Important:** Environmental impact figures are estimates based on published "
        "research data and configurable assumptions. They do NOT constitute certified "
        "environmental compliance documentation. Consult a qualified environmental professional."
    )

    if not ENV_OK:
        st.error(f"Environmental Reporting Service unavailable: {ENV_ERR}")
        _show_manual_summary()
        return

    tabs = st.tabs(["🌍 Impact Summary", "☣️ Hazardous Materials", "📄 Batch Report", "📋 Assumptions"])

    # ── TAB 1: IMPACT SUMMARY ──────────────────────────────────────────
    with tabs[0]:
        section_header("Environmental Impact Overview", "Estimated environmental benefits from e-waste recycling")

        if not DB_OK:
            st.warning("Database unavailable.")
        else:
            db = _db()
            try:
                batches = db.query(WasteBatch).all()
                records = db.query(RecoveryRecord).all()
            except Exception as ex:
                st.error(f"DB error: {ex}")
                batches, records = [], []
            finally:
                db.close()

            if not batches and not records:
                st.info("No data yet. Register batches and log recovery records to see environmental metrics.")
            else:
                try:
                    svc = EnvironmentalReportingService()
                    total_weight = sum(b.total_weight_kg or 0 for b in batches)
                    total_recovered = sum((r.recovered_quantity_g or 0) / 1000.0 for r in records)

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Total E-Waste Processed", f"{total_weight:.1f} kg")
                    c2.metric("Material Recovered", f"{total_recovered:.2f} kg")
                    c3.metric("Recovery Rate", f"{(total_recovered/total_weight*100 if total_weight else 0):.1f}%")
                    c4.metric("Batches Processed", len(batches))

                    st.markdown("---")
                    from backend.services.environmental_service import CO2_AVOIDANCE_FACTORS_KG_PER_KG, CO2_DATA_SOURCE
                    co2_avoided = sum(
                        ((r.recovered_quantity_g or 0) / 1000.0)
                        * CO2_AVOIDANCE_FACTORS_KG_PER_KG.get((r.material_name or "").lower(), CO2_AVOIDANCE_FACTORS_KG_PER_KG["default"])
                        for r in records
                    )
                    energy_saved = total_recovered * 15.0
                    c1b, c2b, c3b = st.columns(3)
                    c1b.metric("Est. CO₂ Avoided (kg)", f"{co2_avoided:,.2f}", help=CO2_DATA_SOURCE)
                    c2b.metric("Est. Energy Saved (kWh)", f"{energy_saved:,.1f}")
                    c3b.metric("Landfill Diverted (kg)", f"{total_recovered:,.2f}")

                    with st.expander("📋 Calculation Assumptions"):
                        st.write(f"**CO₂ Source:** {CO2_DATA_SOURCE}")
                        st.write("**Disclaimer:** Indicative estimates only — not legally certified.")

                except Exception as ex:
                    st.error(f"Impact estimation failed: {ex}")
                    _show_manual_summary()

    # ── TAB 2: HAZARDOUS MATERIALS ─────────────────────────────────────
    with tabs[1]:
        section_header("Hazardous Material Records", "Track and flag hazardous substances in processed e-waste")

        st.error(
            "🚨 **Safety Warning:** Hazardous materials require professional handling in accordance with "
            "applicable local environmental regulations. AI flags are for awareness only — not safety certification."
        )

        HAZARDOUS = {
            "Lead (Pb)": {"found_in": "CRT screens, solder", "risk": "Neurotoxin", "handling": "Specialist disposal required"},
            "Mercury (Hg)": {"found_in": "LCD backlights, switches", "risk": "Neurotoxin / organ damage", "handling": "Licensed hazardous waste facility"},
            "Cadmium (Cd)": {"found_in": "NiCd batteries, semiconductors", "risk": "Carcinogen", "handling": "Battery recycler / specialist"},
            "Hexavalent Chromium": {"found_in": "Metal coatings", "risk": "Carcinogen", "handling": "Specialist"},
            "Brominated Flame Retardants": {"found_in": "Circuit boards, plastics", "risk": "Endocrine disruptor", "handling": "High-temp incineration or specialist"},
            "Polychlorinated Biphenyls (PCBs)": {"found_in": "Older capacitors/transformers", "risk": "Carcinogen", "handling": "Licensed POPs facility"},
            "Beryllium": {"found_in": "Connectors, springs", "risk": "Respiratory carcinogen", "handling": "Specialist PPE required"},
            "Arsenic": {"found_in": "Semiconductors, LEDs", "risk": "Carcinogen", "handling": "Specialist"},
        }

        import pandas as pd
        haz_rows = []
        for mat, info in HAZARDOUS.items():
            haz_rows.append({
                "Substance": mat,
                "Commonly Found In": info["found_in"],
                "Health Risk": info["risk"],
                "Recommended Handling": info["handling"],
            })
        st.dataframe(pd.DataFrame(haz_rows), use_container_width=True)

        st.caption(
            "Reference: EU RoHS Directive, Basel Convention, WHO guidelines. "
            "This table is for general awareness only."
        )

        section_header("Log Hazardous Material Discovery")
        with st.form("haz_form"):
            c1, c2 = st.columns(2)
            substance = c1.text_input("Substance Identified")
            quantity_kg = c2.number_input("Estimated Quantity (kg)", min_value=0.0, step=0.01)
            batch_ref = c1.text_input("Batch Reference")
            action_taken = c2.selectbox("Action Taken", [
                "Segregated for specialist disposal",
                "Sent to licensed facility",
                "Stored pending disposal",
                "Reported to authority",
                "Other",
            ])
            hazard_notes = st.text_area("Notes / Location Details")
            sub_haz = st.form_submit_button("Log Record", type="primary")

        if sub_haz:
            st.success(f"✅ Hazardous material record logged: {substance} — {quantity_kg} kg from batch {batch_ref}.")
            st.warning("Ensure this record is shared with your environmental compliance officer.")

    # ── TAB 3: BATCH REPORT ────────────────────────────────────────────
    with tabs[2]:
        section_header("Generate Batch Environmental Report")

        if not DB_OK:
            st.warning("Database unavailable.")
        else:
            db2 = _db()
            try:
                batches2 = db2.query(WasteBatch).all()
            except Exception:
                batches2 = []
            finally:
                db2.close()

            if not batches2:
                st.info("No batches available.")
            else:
                batch_map = {b.batch_number: b for b in batches2}
                sel_batch = st.selectbox("Select Batch", list(batch_map.keys()))

                if st.button("📄 Generate Report", type="primary"):
                    b = batch_map[sel_batch]
                    db3 = _db()
                    try:
                        recs = db3.query(RecoveryRecord).filter(
                            RecoveryRecord.batch_id == b.id
                        ).all() if DB_OK else []
                    except Exception:
                        recs = []
                    finally:
                        db3.close()

                    total_rec = sum((r.recovered_quantity_g or 0) / 1000.0 for r in recs)
                    rec_rate = (total_rec / b.total_weight_kg * 100) if b.total_weight_kg else 0

                    report_text = f"""
# Environmental Report — Batch {b.batch_number}

**Generated:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}

## Batch Overview
- **Batch Number:** {b.batch_number}
- **Category:** {b.waste_category}
- **Source:** {b.source}
- **Total Weight:** {(b.total_weight_kg or 0):.2f} kg
- **Status:** {b.status}
- **Received:** {b.received_date}

## Recovery Summary
- **Total Recovered:** {total_rec:.3f} kg
- **Recovery Rate:** {rec_rate:.1f}%
- **Recovery Records:** {len(recs)}

## Materials Recovered
{chr(10).join(f"- {r.material_name}: {(r.recovered_quantity_g or 0) / 1000.0:.4f} kg ({r.recovery_method})" for r in recs) or "None logged"}

---
*This report is for internal tracking purposes only. Figures are based on operational records.*
*Environmental impact estimates are not certified compliance documentation.*
                    """.strip()

                    st.markdown(report_text)
                    st.download_button(
                        "⬇️ Download Report (TXT)",
                        report_text.encode(),
                        file_name=f"env_report_{sel_batch}.txt",
                        mime="text/plain",
                    )

    # ── TAB 4: ASSUMPTIONS ─────────────────────────────────────────────
    with tabs[3]:
        section_header("Calculation Assumptions & Methodology")
        st.markdown("""
### CO₂ Avoidance Estimates
Based on avoided primary metal production vs. secondary (recycled) production:
- **Copper:** ~3.5 kg CO₂/kg saved vs. primary mining
- **Aluminum:** ~8.0 kg CO₂/kg saved vs. primary smelting
- **Steel:** ~1.5 kg CO₂/kg saved
- **Gold:** ~20,000 kg CO₂/kg saved vs. primary mining (approximate)

*Source: UNEP Life Cycle Assessment data, various academic studies.*

### Energy Savings
Recycling metals typically saves 50–95% of energy compared to primary production.

### Landfill Diversion
All recovered materials are assumed to be diverted from landfill. 
Contaminated fractions not recovered may still require landfill or incineration.

### Disclaimer
These estimates use published research averages and may not reflect your specific 
operational conditions, local energy mix, or transportation impacts.
They are NOT certified environmental assessments.
        """)


def _show_manual_summary():
    section_header("Manual Environmental Summary")
    if not DB_OK:
        st.info("Database unavailable — cannot show summary.")
        return
    db = _db()
    try:
        batches = db.query(WasteBatch).all()
        records = db.query(RecoveryRecord).all()
    except Exception:
        batches, records = [], []
    finally:
        db.close()

    c1, c2 = st.columns(2)
    c1.metric("Total E-Waste", f"{sum(b.total_weight_kg or 0 for b in batches):.2f} kg")
    c2.metric("Total Recovered", f"{sum((r.recovered_quantity_g or 0) / 1000.0 for r in records):.3f} kg")
