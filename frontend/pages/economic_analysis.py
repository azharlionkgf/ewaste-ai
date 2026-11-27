"""
E-Waste AI — Economic Analysis (fixed + Phase 6 enhanced)
Uses actual DB column names. All estimates clearly labelled.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from frontend.theme import apply_theme, page_header, section_header, COLORS

try:
    from backend.services.advanced_intelligence import (
        get_engine, MATERIAL_PRICES_USD_PER_G, PRICE_SOURCE, PRICE_DATE
    )
    AI6_OK = True
except Exception as e:
    AI6_OK = False; AI6_ERR = str(e)

try:
    from backend.database import SessionLocal
    from backend.models.all_models import WasteBatch, RecoveryRecord, Inventory
    DB_OK = True
except Exception as e:
    DB_OK = False


def _db():
    return SessionLocal() if DB_OK else None


def render_economic_analysis():
    apply_theme()
    page_header("Economic Intelligence",
                "Recovery value estimation, processing cost analysis and profitability overview", "💰")
    st.info("⚠️ **All financial figures are estimates only.** Not financial advice or certified valuations.")

    tabs = st.tabs(["📊 Value Estimation", "💸 Processing Costs", "📈 Profitability", "🏷️ Price Reference"])

    # ── TAB 1: VALUE ESTIMATION ────────────────────────────────────────
    with tabs[0]:
        section_header("Estimate Recovery Value", "Enter material quantities to estimate market value")

        if not AI6_OK:
            st.warning(f"Advanced Intelligence Engine unavailable: {AI6_ERR}")
            _show_price_ref()
            return

        engine = get_engine()
        st.markdown("**Enter recovered quantities:**")
        MATERIALS = [
            ("gold_traces","Gold (grams)"), ("silver_traces","Silver (grams)"),
            ("copper","Copper (grams)"), ("aluminum","Aluminum (grams)"),
            ("steel_iron","Steel / Iron (grams)"), ("palladium_traces","Palladium (grams)"),
            ("lithium","Lithium (grams)"), ("cobalt","Cobalt (grams)"),
            ("circuit_boards","Circuit Boards (grams)"),
        ]
        qtys = {}
        cols = st.columns(2)
        for idx, (key, label) in enumerate(MATERIALS):
            with cols[idx % 2]:
                qtys[key] = st.number_input(label, min_value=0.0, step=0.01, key=f"qty_{key}")

        if st.button("💰 Estimate Value", type="primary"):
            total = 0.0
            rows = []
            for mat, qty_g in qtys.items():
                if qty_g <= 0:
                    continue
                price = MATERIAL_PRICES_USD_PER_G.get(mat, 0.0)
                val = qty_g * price
                total += val
                rows.append({"Material": mat.replace("_"," ").title(),
                              "Qty (g)": qty_g, "Price ($/g)": price,
                              "Est. Value ($)": f"${val:,.4f}"})
            if rows:
                import pandas as pd
                st.success(f"**Estimated Total Value: ${total:,.4f} USD**")
                st.caption(f"Price source: {PRICE_SOURCE} — as of {PRICE_DATE}")
                st.warning("⚠️ ESTIMATE ONLY — reference prices, not live market rates.")
                st.dataframe(pd.DataFrame(rows), use_container_width=True)
            else:
                st.warning("Enter at least one non-zero quantity.")

    # ── TAB 2: PROCESSING COSTS ────────────────────────────────────────
    with tabs[1]:
        section_header("Processing Cost Analysis")
        if not AI6_OK:
            st.warning("Cost estimation unavailable."); return

        engine = get_engine()
        with st.form("cost_form"):
            c1, c2 = st.columns(2)
            weight_kg     = c1.number_input("Batch Weight (kg)", min_value=0.0, step=1.0, value=100.0)
            device_count  = c2.number_input("Number of Devices", min_value=0, step=1, value=10)
            labour_hours  = c1.number_input("Labour Hours", min_value=0.0, step=0.5)
            equip_hours   = c2.number_input("Equipment Hours", min_value=0.0, step=0.5)
            transport_km  = c1.number_input("Transport Distance (km)", min_value=0.0, step=1.0)
            hazard_kg     = c2.number_input("Hazardous Disposal (kg)", min_value=0.0, step=0.1)
            sub_cost = st.form_submit_button("Calculate Costs", type="primary")

        if sub_cost:
            result = engine.estimate_processing_cost(
                weight_kg=weight_kg, device_count=int(device_count),
                labour_hours=labour_hours, equipment_hours=equip_hours,
                transport_km=transport_km, hazardous_disposal_kg=hazard_kg,
            )
            st.success(f"**Estimated Processing Cost: ${result['total_cost_usd']:,.2f} USD**")
            st.warning(result.get("disclaimer","Estimates only."))
            import pandas as pd
            bk = result.get("breakdown", {})
            rows = [{"Cost Item": k.replace("_"," ").title(), "Amount ($)": f"${v:,.2f}"}
                    for k, v in bk.items()]
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True)
            with st.expander("Rates Used"):
                for k, v in result.get("rates_used", {}).items():
                    st.write(f"**{k.replace('_',' ')}:** ${v}")

    # ── TAB 3: PROFITABILITY ───────────────────────────────────────────
    with tabs[2]:
        section_header("Profitability Overview")
        if not DB_OK:
            st.warning("Database unavailable."); return

        db = _db()
        try:
            recs = db.query(RecoveryRecord).all()
        except Exception as ex:
            st.error(str(ex)); recs = []
        finally:
            db.close()

        if not recs:
            st.info("No recovery records. Log materials in Industrial Operations to see profitability.")
        else:
            total_g = sum(r.recovered_quantity_g or 0 for r in recs)
            # Estimate value from recorded est_value or price table
            total_val = 0.0
            for r in recs:
                if r.estimated_value_usd:
                    total_val += r.estimated_value_usd
                else:
                    price = MATERIAL_PRICES_USD_PER_G.get(r.material_name, 0.001) if AI6_OK else 0.0
                    total_val += (r.recovered_quantity_g or 0) * price

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Recovered", f"{total_g:.1f} g")
            c2.metric("Est. Material Value", f"${total_val:,.2f}")
            c3.metric("Recovery Records", len(recs))
            st.warning("⚠️ Processing costs not deducted automatically. Use **Processing Costs** tab for full P&L.")
            st.caption(f"Value source: {PRICE_SOURCE if AI6_OK else 'Price data unavailable'} — {PRICE_DATE if AI6_OK else ''}")

    # ── TAB 4: PRICE REFERENCE ─────────────────────────────────────────
    with tabs[3]:
        _show_price_ref()


def _show_price_ref():
    section_header("Reference Material Prices", "Approximate prices for estimation only")
    import pandas as pd
    rows = [
        {"Material":"Gold","Unit":"per gram","Est. Price (USD)":"$60–70","Notes":"LME spot — varies daily"},
        {"Material":"Silver","Unit":"per gram","Est. Price (USD)":"$0.70–0.90","Notes":"LME spot"},
        {"Material":"Palladium","Unit":"per gram","Est. Price (USD)":"$30–50","Notes":"High volatility"},
        {"Material":"Platinum","Unit":"per gram","Est. Price (USD)":"$28–35","Notes":"LME spot"},
        {"Material":"Copper","Unit":"per gram","Est. Price (USD)":"$0.008–0.010","Notes":"LME spot"},
        {"Material":"Aluminum","Unit":"per gram","Est. Price (USD)":"$0.002–0.003","Notes":"LME spot"},
        {"Material":"Cobalt","Unit":"per gram","Est. Price (USD)":"$0.025–0.035","Notes":"Battery-grade"},
        {"Material":"Lithium","Unit":"per gram","Est. Price (USD)":"$0.010–0.020","Notes":"Carbonate equiv."},
        {"Material":"Steel/Iron","Unit":"per gram","Est. Price (USD)":"$0.0001–0.0002","Notes":"Scrap price"},
        {"Material":"Circuit Boards","Unit":"per gram","Est. Price (USD)":"$0.005–0.015","Notes":"Varies by grade"},
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    st.caption(f"Sources: {PRICE_SOURCE if AI6_OK else 'LME / USGS Mineral Commodity Summaries'}. "
               f"Reference date: {PRICE_DATE if AI6_OK else '2024-01-15'}. For planning only.")
