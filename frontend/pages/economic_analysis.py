"""
E-Waste AI — Economic Intelligence Page
========================================
Task 9 of Phase 5.
Estimate material value, processing costs, and recovery profitability.
Connects to backend.services.economic_service.
All figures are labelled as ESTIMATES.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from frontend.theme import apply_theme, page_header, section_header, status_badge, COLORS

# ── backend imports ────────────────────────────────────────────────────
try:
    from backend.services.economic_service import EconomicIntelligenceService
    ECON_OK = True
except Exception as e:
    ECON_OK = False
    ECON_ERR = str(e)

try:
    from backend.database import SessionLocal
    from backend.models.all_models import WasteBatch, RecoveryRecord, Inventory
    DB_OK = True
except Exception as e:
    DB_OK = False


def _db():
    if not DB_OK:
        return None
    return SessionLocal()


def render_economic_analysis():
    apply_theme()
    page_header(
        "Economic Intelligence",
        "Recovery value estimation, processing cost analysis and profitability overview",
        "💰",
    )

    st.info(
        "⚠️ **All financial figures are estimates only.** "
        "Actual market prices fluctuate. Never use these estimates as official valuations or financial advice."
    )

    if not ECON_OK:
        st.warning(f"Economic Intelligence Service unavailable: {ECON_ERR}")
        st.info("Showing reference price table only.")
        _show_price_reference()
        return

    tabs = st.tabs(["📊 Value Estimation", "💸 Cost Analysis", "📈 Profitability", "🏷️ Price Reference"])

    # ── TAB 1: VALUE ESTIMATION ────────────────────────────────────────
    with tabs[0]:
        section_header("Estimate Recovery Value", "Enter material quantities to calculate estimated market value")

        st.markdown("Enter the quantities of recovered materials:")

        materials = [
            ("gold_g", "Gold (grams)"),
            ("silver_g", "Silver (grams)"),
            ("copper_kg", "Copper (kg)"),
            ("aluminum_kg", "Aluminum (kg)"),
            ("steel_kg", "Steel / Iron (kg)"),
            ("palladium_g", "Palladium (grams)"),
            ("platinum_g", "Platinum (grams)"),
            ("lithium_kg", "Lithium (kg)"),
            ("cobalt_kg", "Cobalt (kg)"),
            ("circuit_boards_kg", "Circuit Boards (kg)"),
        ]

        qtys = {}
        cols = st.columns(2)
        for idx, (key, label) in enumerate(materials):
            with cols[idx % 2]:
                qtys[key] = st.number_input(label, min_value=0.0, step=0.01, key=f"qty_{key}")

        if st.button("💰 Estimate Value", type="primary"):
            try:
                svc = EconomicIntelligenceService()
                result = svc.estimate_material_value(material_quantities=qtys)
                _display_value_result(result)
            except Exception as ex:
                st.error(f"Estimation failed: {ex}")

    # ── TAB 2: COST ANALYSIS ───────────────────────────────────────────
    with tabs[1]:
        section_header("Processing Cost Analysis", "Estimate operational costs for a batch")

        with st.form("cost_form"):
            c1, c2 = st.columns(2)
            weight_kg = c1.number_input("Batch Weight (kg)", min_value=0.0, step=1.0, value=100.0)
            device_count = c2.number_input("Number of Devices", min_value=0, step=1, value=10)
            manual_hours = c1.number_input("Manual Labour Hours", min_value=0.0, step=0.5)
            equipment_hours = c2.number_input("Equipment/Machine Hours", min_value=0.0, step=0.5)
            transport_km = c1.number_input("Transport Distance (km)", min_value=0.0, step=1.0)
            disposal_kg = c2.number_input("Hazardous Waste Disposal (kg)", min_value=0.0, step=0.1)
            sub_cost = st.form_submit_button("Calculate Costs", type="primary")

        if sub_cost:
            try:
                svc = EconomicIntelligenceService()
                result = svc.estimate_processing_cost(
                    weight_kg=weight_kg,
                    device_count=int(device_count),
                    labour_hours=manual_hours,
                    equipment_hours=equipment_hours,
                    transport_km=transport_km,
                    hazardous_disposal_kg=disposal_kg,
                )
                _display_cost_result(result)
            except Exception as ex:
                st.error(f"Cost calculation failed: {ex}")

    # ── TAB 3: PROFITABILITY ───────────────────────────────────────────
    with tabs[2]:
        section_header("Profitability Overview", "Compare estimated revenue vs. processing costs")

        if not DB_OK:
            st.warning("Database unavailable — cannot load batch data.")
        else:
            db = _db()
            try:
                batches = db.query(WasteBatch).all()
                records = db.query(RecoveryRecord).all()
            except Exception as ex:
                st.error(f"Database error: {ex}")
                batches, records = [], []
            finally:
                db.close()

            if not records:
                st.info("No recovery records yet. Log materials in Industrial Operations to see profitability data.")
            else:
                try:
                    svc = EconomicIntelligenceService()
                    agg = {}
                    for r in records:
                        # convert to common unit for estimation
                        mat = r.material_name or "other"
                        qty = r.quantity_kg or 0
                        key = f"{mat}_kg"
                        agg[key] = agg.get(key, 0) + qty

                    value_result = svc.estimate_material_value(material_quantities=agg)
                    total_value = value_result.get("total_estimated_value_usd", 0)
                    total_recovered = sum(r.quantity_kg or 0 for r in records)

                    c1, c2, c3 = st.columns(3)
                    c1.metric("Total Recovered", f"{total_recovered:.2f} kg")
                    c2.metric("Est. Material Value", f"${total_value:,.2f}")
                    c3.metric("Recovery Records", len(records))

                    st.warning(
                        "⚠️ Processing costs are not automatically deducted here. "
                        "Enter costs in the **Cost Analysis** tab for a complete picture."
                    )
                    _display_value_result(value_result)
                except Exception as ex:
                    st.error(f"Profitability analysis failed: {ex}")

    # ── TAB 4: PRICE REFERENCE ─────────────────────────────────────────
    with tabs[3]:
        _show_price_reference()


def _display_value_result(result: dict):
    if not result:
        st.warning("No result returned.")
        return

    total = result.get("total_estimated_value_usd", 0)
    breakdown = result.get("breakdown", {})
    source = result.get("price_source", "Internal reference prices")
    timestamp = result.get("price_timestamp", "N/A")

    st.success(f"**Estimated Total Value: ${total:,.2f} USD**")
    st.caption(f"Price source: {source} — as of {timestamp}")
    st.warning("⚠️ ESTIMATE ONLY — not a certified valuation.")

    if breakdown:
        import pandas as pd
        rows = []
        for mat, info in breakdown.items():
            rows.append({
                "Material": mat,
                "Quantity": info.get("quantity", ""),
                "Unit Price (USD)": info.get("unit_price_usd", ""),
                "Est. Value (USD)": f"${info.get('value_usd', 0):,.2f}",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)


def _display_cost_result(result: dict):
    if not result:
        st.warning("No result returned.")
        return

    total = result.get("total_cost_usd", 0)
    breakdown = result.get("breakdown", {})
    assumptions = result.get("assumptions", {})

    st.success(f"**Estimated Processing Cost: ${total:,.2f} USD**")
    st.warning("⚠️ ESTIMATE ONLY — based on configurable default rates.")

    if breakdown:
        import pandas as pd
        rows = [{"Cost Item": k, "Amount (USD)": f"${v:,.2f}"} for k, v in breakdown.items()]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    if assumptions:
        with st.expander("📋 Assumptions"):
            for k, v in assumptions.items():
                st.write(f"**{k}:** {v}")


def _show_price_reference():
    section_header("Reference Material Prices", "Approximate market prices (for estimation purposes only)")

    import pandas as pd
    ref_data = [
        {"Material": "Gold", "Unit": "per gram", "Est. Price (USD)": "$60–70", "Notes": "LME spot — varies daily"},
        {"Material": "Silver", "Unit": "per gram", "Est. Price (USD)": "$0.70–0.90", "Notes": "LME spot"},
        {"Material": "Palladium", "Unit": "per gram", "Est. Price (USD)": "$30–50", "Notes": "High volatility"},
        {"Material": "Platinum", "Unit": "per gram", "Est. Price (USD)": "$28–35", "Notes": "LME spot"},
        {"Material": "Copper", "Unit": "per kg", "Est. Price (USD)": "$8–10", "Notes": "LME spot"},
        {"Material": "Aluminum", "Unit": "per kg", "Est. Price (USD)": "$1.80–2.20", "Notes": "LME spot"},
        {"Material": "Cobalt", "Unit": "per kg", "Est. Price (USD)": "$25–35", "Notes": "Battery-grade"},
        {"Material": "Lithium", "Unit": "per kg", "Est. Price (USD)": "$10–20", "Notes": "Carbonate equiv."},
        {"Material": "Steel/Iron", "Unit": "per kg", "Est. Price (USD)": "$0.10–0.20", "Notes": "Scrap price"},
        {"Material": "Circuit Boards", "Unit": "per kg", "Est. Price (USD)": "$5–15", "Notes": "Varies by grade"},
    ]
    st.dataframe(pd.DataFrame(ref_data), use_container_width=True)
    st.caption(
        "Sources: LME (London Metal Exchange) spot prices, industry recycling benchmarks. "
        "Prices are approximate and for planning purposes only. Last reviewed: 2024."
    )
