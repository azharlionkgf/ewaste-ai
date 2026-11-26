"""
frontend/pages/recovery_intelligence.py
E-WASTE AI - Recovery Intelligence & Economic Analysis Page
Estimate material recovery, economic value, environmental impact.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from frontend.theme import apply_theme, section_header


def render():
    apply_theme()
    st.markdown('<h1 class="page-title">♻️ Recovery Intelligence</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Material recovery estimates, economic valuation, environmental impact and recycling recommendations.</p>',
        unsafe_allow_html=True
    )

    tabs = st.tabs([
        "🔩 Recovery Estimator",
        "💰 Economic Valuation",
        "🌱 Environmental Impact",
        "⚠️ Hazmat Checker",
        "📋 Recycling Recommendations",
    ])

    with tabs[0]: _tab_recovery()
    with tabs[1]: _tab_economic()
    with tabs[2]: _tab_environmental()
    with tabs[3]: _tab_hazmat()
    with tabs[4]: _tab_recommendations()


# ============================================================
# TAB 1 — RECOVERY ESTIMATOR
# ============================================================
def _tab_recovery():
    section_header("Material Recovery Estimator",
                   "Estimate recoverable materials from e-waste devices. All values are research-based estimates.")

    st.info("⚠️ **All estimates are research averages labeled `is_estimate=True`. Actual recovery depends on equipment, purity and market conditions.**")

    col1, col2 = st.columns(2)
    with col1:
        device_type = st.selectbox("Device Type", [
            "smartphone", "laptop", "desktop_computer", "tablet",
            "circuit_board", "battery_li_ion", "monitor_lcd", "printer",
            "charger", "cable", "default"
        ], key="recovery_device_type")
        quantity = st.number_input("Quantity (units)", 1, 100000, 10, key="recovery_qty")
        weight_kg = st.number_input("Weight per unit (kg)", 0.01, 100.0, 0.2, step=0.01, key="recovery_weight")

    with col2:
        st.markdown("#### Current Material Prices (Editable)")
        st.caption("These are reference estimates. Update with current market prices.")
        gold_price = st.number_input("Gold (USD/gram)", 0.0, 200.0, 60.0, step=0.5, key="price_gold")
        silver_price = st.number_input("Silver (USD/gram)", 0.0, 10.0, 0.80, step=0.01, key="price_silver")
        copper_price = st.number_input("Copper (USD/gram)", 0.0, 0.1, 0.009, step=0.001, format="%.4f", key="price_copper")
        cobalt_price = st.number_input("Cobalt (USD/gram)", 0.0, 0.5, 0.035, step=0.001, format="%.3f", key="price_cobalt")

    if st.button("🔩 Calculate Recovery", type="primary", key="btn_calc_recovery"):
        _run_recovery_estimate(device_type, quantity, weight_kg, gold_price, silver_price, copper_price, cobalt_price)

    if "recovery_result" in st.session_state:
        _show_recovery_result(st.session_state["recovery_result"])


def _run_recovery_estimate(device_type, quantity, weight_kg, gold_price, silver_price, copper_price, cobalt_price):
    try:
        from industrial.valuation.cost_calculator import CostCalculator

        prices = {
            "gold": gold_price, "silver": silver_price, "copper": copper_price,
            "cobalt": cobalt_price, "lithium": 0.025, "nickel": 0.014,
            "aluminum": 0.002, "iron_steel": 0.0005, "palladium": 45.0,
        }
        calc = CostCalculator(material_prices=prices)
        result = calc.estimate_recovery_value(device_type, quantity=quantity, weight_kg=weight_kg)
        st.session_state["recovery_result"] = result

    except Exception as e:
        st.error(f"Calculation failed: {e}")


def _show_recovery_result(result: dict):
    st.markdown("---")
    st.markdown("### 🔩 Recovery Estimate Results")
    st.caption(f"Source: {result.get('data_source', 'Research averages')} | is_estimate={result.get('is_estimate')}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Recovery Value", f"${result.get('total_value_usd', 0):,.2f} USD")
        st.metric("Scale", result.get("scale", "—"))
    with col2:
        st.metric("Device Type", result.get("device_type", "—").replace("_", " ").title())
        st.metric("Quantity", result.get("quantity", 1))

    breakdown = result.get("material_breakdown", {})
    if breakdown:
        st.markdown("#### Material Breakdown")
        rows = []
        for mat, data in breakdown.items():
            rows.append({
                "Material": mat.replace("_", " ").title(),
                "Total (g)": f"{data.get('total_grams', 0):.4f}",
                "Price (USD/g)": f"{data.get('price_usd_per_gram', 0):.4f}",
                "Value (USD)": f"${data.get('value_usd', 0):.4f}",
            })
        df = pd.DataFrame(rows)
        df = df.sort_values("Value (USD)", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Pie chart of values
        import json
        values = {r["Material"]: float(r["Value (USD)"].replace("$", "")) for r in rows}
        values = {k: v for k, v in values.items() if v > 0}
        if values:
            chart_df = pd.DataFrame(list(values.items()), columns=["Material", "Value USD"])
            chart_df = chart_df[chart_df["Value USD"] > 0].set_index("Material")
            st.bar_chart(chart_df)


# ============================================================
# TAB 2 — ECONOMIC VALUATION
# ============================================================
def _tab_economic():
    section_header("Economic Valuation", "Net value = gross material recovery − processing costs.")

    col1, col2 = st.columns(2)
    with col1:
        device_type = st.selectbox("Device Type", [
            "smartphone", "laptop", "desktop_computer", "tablet",
            "circuit_board", "battery_li_ion", "monitor_lcd", "default"
        ], key="econ_device_type")
        quantity = st.number_input("Quantity", 1, 100000, 100, key="econ_qty")
        weight_kg = st.number_input("Weight per unit (kg)", 0.01, 100.0, 0.5, step=0.01, key="econ_weight")

    with col2:
        st.markdown("#### Processing Cost Override")
        st.caption("Leave 0 to use research-average rates.")
        override_cost = st.number_input("Custom processing cost per kg (USD)", 0.0, 50.0, 0.0, step=0.1, key="econ_cost_override")

    if st.button("💰 Calculate Net Value", type="primary", key="btn_calc_net"):
        _run_net_value(device_type, quantity, weight_kg, override_cost)

    if "econ_result" in st.session_state:
        _show_econ_result(st.session_state["econ_result"])


def _run_net_value(device_type, quantity, weight_kg, override_cost):
    try:
        from industrial.valuation.cost_calculator import CostCalculator
        calc = CostCalculator()
        result = calc.calculate_net_value(device_type, quantity, weight_kg)
        if override_cost > 0:
            result["processing_cost_usd"] = round(override_cost * weight_kg * quantity, 2)
            result["net_value_usd"] = round(result["gross_recovery_value_usd"] - result["processing_cost_usd"], 2)
            result["is_profitable"] = result["net_value_usd"] > 0
        st.session_state["econ_result"] = result

    except Exception as e:
        st.error(f"Calculation failed: {e}")


def _show_econ_result(result: dict):
    st.markdown("---")
    st.markdown("### 💰 Economic Valuation")
    st.caption(f"Source: {result.get('data_source', 'Research averages')} | is_estimate=True")

    cols = st.columns(4)
    with cols[0]: st.metric("Gross Recovery Value", f"${result.get('gross_recovery_value_usd', 0):,.2f}")
    with cols[1]: st.metric("Processing Cost", f"${result.get('processing_cost_usd', 0):,.2f}")
    with cols[2]: st.metric("Net Value", f"${result.get('net_value_usd', 0):,.2f}")
    with cols[3]:
        profitable = result.get("is_profitable", False)
        st.metric("Profitable?", "✅ Yes" if profitable else "❌ No")

    st.caption(result.get("note", ""))

    # Download
    csv = pd.DataFrame([result]).to_csv(index=False)
    st.download_button("⬇️ Download Report CSV", csv, "economic_valuation.csv", "text/csv", key="dl_econ_csv")


# ============================================================
# TAB 3 — ENVIRONMENTAL IMPACT
# ============================================================
def _tab_environmental():
    section_header("Environmental Impact", "Estimate CO₂ avoided, landfill diversion and resource savings.")

    col1, col2 = st.columns(2)
    with col1:
        device_type = st.selectbox("Device Type", [
            "smartphone", "laptop", "desktop_computer", "circuit_board",
            "battery_li_ion", "monitor_lcd", "tablet", "default"
        ], key="env_device_type")
        quantity = st.number_input("Quantity", 1, 1000000, 1000, key="env_qty")
        weight_kg = st.number_input("Weight per unit (kg)", 0.01, 100.0, 0.2, step=0.01, key="env_weight")

    with col2:
        st.markdown("#### Reference Figures (Research Estimates)")
        st.caption("All CO₂ figures are research averages labeled is_estimate=True")
        co2_per_kg = st.number_input("CO₂ avoided per kg recycled (kg CO₂e)", 0.1, 50.0, 2.5, step=0.1, key="env_co2")
        energy_per_kg = st.number_input("Energy saved per kg (MJ)", 1.0, 100.0, 15.0, step=0.5, key="env_energy")

    if st.button("🌱 Calculate Environmental Impact", type="primary", key="btn_env_calc"):
        _run_env_impact(device_type, quantity, weight_kg, co2_per_kg, energy_per_kg)

    if "env_result" in st.session_state:
        _show_env_result(st.session_state["env_result"])


def _run_env_impact(device_type, quantity, weight_kg, co2_per_kg, energy_per_kg):
    try:
        total_weight = quantity * weight_kg
        co2_avoided = round(total_weight * co2_per_kg, 2)
        energy_saved = round(total_weight * energy_per_kg, 2)
        landfill_diverted = round(total_weight, 2)
        trees_equiv = round(co2_avoided / 21.77, 1)  # 1 tree ≈ 21.77 kg CO₂/year

        result = {
            "device_type": device_type,
            "quantity": quantity,
            "total_weight_kg": total_weight,
            "co2_avoided_kg": co2_avoided,
            "energy_saved_mj": energy_saved,
            "landfill_diverted_kg": landfill_diverted,
            "trees_equivalent": trees_equiv,
            "is_estimate": True,
            "data_source": "Research averages — UNEP / EPA e-waste guidelines",
        }
        st.session_state["env_result"] = result

    except Exception as e:
        st.error(f"Calculation failed: {e}")


def _show_env_result(result: dict):
    st.markdown("---")
    st.markdown("### 🌱 Environmental Impact Estimate")
    st.caption("⚠️ Research-based estimates — is_estimate=True")

    cols = st.columns(4)
    with cols[0]: st.metric("CO₂ Avoided", f"{result['co2_avoided_kg']:,.1f} kg")
    with cols[1]: st.metric("Energy Saved", f"{result['energy_saved_mj']:,.0f} MJ")
    with cols[2]: st.metric("Landfill Diverted", f"{result['landfill_diverted_kg']:,.1f} kg")
    with cols[3]: st.metric("Trees Equivalent", f"{result['trees_equivalent']:,.0f}")

    st.info(f"Source: {result.get('data_source')}")


# ============================================================
# TAB 4 — HAZMAT CHECKER
# ============================================================
def _tab_hazmat():
    section_header("Hazmat Checker", "Check hazardous materials and RoHS/WEEE compliance for any device.")

    device_input = st.text_input("Device Type (e.g. laptop, smartphone, monitor_crt)", key="hazmat_device_input")
    if device_input and st.button("⚠️ Check Hazmat", type="primary", key="btn_hazmat_check"):
        _run_hazmat_check(device_input)

    if "hazmat_result" in st.session_state:
        _show_hazmat_result(st.session_state["hazmat_result"])

    st.markdown("---")
    st.markdown("#### Known Hazardous Materials in E-Waste")
    st.markdown("""
    | Material | CAS | Max (ppm) | Health Risk | Key Source |
    |----------|-----|-----------|-------------|------------|
    | Mercury | 7439-97-6 | 1000 | HIGH — neurotoxin | LCD backlights, switches |
    | Lead | 7439-92-1 | 1000 | HIGH — neurotoxin | Pre-RoHS solder, CRT glass |
    | Cadmium | 7440-43-9 | 100 | HIGH — carcinogen | NiCd batteries |
    | Chromium VI | 18540-29-9 | 1000 | HIGH — carcinogen | Metal coatings |
    | PBB | Various | 1000 | MEDIUM — endocrine disruptor | Flame retardants |
    | PBDE | Various | 1000 | MEDIUM — endocrine disruptor | PCBs, plastics |
    
    *Limits per RoHS Directive 2011/65/EU — Annex II*
    """)


def _run_hazmat_check(device_type: str):
    try:
        from industrial.compliance.hazmat_rules import HazmatChecker
        checker = HazmatChecker()
        result = checker.check_device(device_type)
        st.session_state["hazmat_result"] = result
    except Exception as e:
        st.error(f"Hazmat check failed: {e}")


def _show_hazmat_result(result: dict):
    st.markdown(f"### ⚠️ Hazmat Report — {result.get('device_type', '').replace('_', ' ').title()}")

    mats = result.get("hazmat_materials_present", [])
    risk = "🔴 HIGH" if any(m in mats for m in ["mercury", "cadmium"]) else "🟡 MEDIUM" if mats else "🟢 LOW"
    st.metric("Risk Level", risk)

    if mats:
        st.warning(f"**Hazardous materials detected:** {', '.join(mats)}")
    else:
        st.success("No critical hazmat materials detected for this device type.")

    if result.get("combined_handling_instructions"):
        st.markdown("#### Handling Instructions")
        for inst in result["combined_handling_instructions"]:
            st.markdown(f"- {inst}")

    if result.get("compliance_notes"):
        st.markdown("#### Compliance Notes")
        for note in result["compliance_notes"]:
            st.markdown(f"- {note}")


# ============================================================
# TAB 5 — RECYCLING RECOMMENDATIONS
# ============================================================
def _tab_recommendations():
    section_header("Recycling Recommendations", "Get step-by-step recycling guidance for any e-waste device.")

    device_type = st.selectbox("Select Device", [
        "smartphone", "laptop", "desktop_computer", "tablet", "circuit_board",
        "battery_li_ion", "battery_lead_acid", "monitor_crt", "monitor_lcd",
        "printer", "charger", "cable", "television", "household_appliance",
    ], key="rec_device_type")

    if st.button("📋 Get Recommendations", type="primary", key="btn_get_rec"):
        _show_recommendations(device_type)


def _show_recommendations(device_type: str):
    # Built-in recommendations by category
    recs = {
        "smartphone": {
            "steps": [
                "1. Data wipe — perform factory reset and verify data destruction",
                "2. Battery removal — discharge to <30% and carefully detach Li-ion battery",
                "3. Screen separation — remove LCD/OLED display assembly",
                "4. PCB extraction — remove motherboard and sub-boards",
                "5. Camera/sensor disassembly — recover camera modules",
                "6. Metal/plastic sorting — separate aluminum frame, plastic casing",
                "7. PCB to smelter — send to certified precious metal refinery",
                "8. Battery to certified Li-ion recycler",
            ],
            "key_materials": "Gold (PCB), Cobalt/Lithium (battery), Rare Earth (speakers/vibrator)",
            "certified_process": "Pyrometallurgical smelting for PCBs; Hydrometallurgical for batteries",
        },
        "circuit_board": {
            "steps": [
                "1. Visual inspection — identify board type and approximate age",
                "2. Component removal — remove capacitors, ICs, connectors",
                "3. Tin/lead solder collection — if pre-RoHS board",
                "4. Shredding — mechanical shredding for high-volume processing",
                "5. Gravity separation — separate metals from fiberglass",
                "6. Send to certified pyrometallurgical smelter for Au/Ag/Pd/Cu recovery",
            ],
            "key_materials": "Gold, Silver, Palladium, Copper (highest concentration of all e-waste categories)",
            "certified_process": "Pyrometallurgical smelting (e.g. Umicore, Aurubis)",
        },
        "battery_li_ion": {
            "steps": [
                "1. ⚠️ SAFETY FIRST — check for swelling, damage or leakage before handling",
                "2. Discharge — bring to <0% SOC in controlled environment",
                "3. Sealed transport — package in fireproof battery bags",
                "4. Send to certified Li-ion recycler — DO NOT shred undischarged",
                "5. Hydrometallurgical processing recovers Li, Co, Ni, Mn",
            ],
            "key_materials": "Lithium, Cobalt, Nickel, Manganese, Copper, Aluminum",
            "certified_process": "Hydrometallurgical leaching at certified battery recycler",
        },
        "monitor_crt": {
            "steps": [
                "1. ⚠️ HIGH HAZMAT — CRT contains lead glass (4–8 kg of lead per unit)",
                "2. Evacuate CRT in controlled environment — implosion risk",
                "3. Separate leaded funnel glass from relatively pure screen glass",
                "4. Send leaded glass to CRT glass recycler or lead smelter",
                "5. Recover copper yoke, metal frame, plastic casing separately",
            ],
            "key_materials": "Lead (glass), Copper (yoke), Iron/Steel (frame)",
            "certified_process": "CRT glass processor required — standard shredding prohibited",
        },
    }

    rec = recs.get(device_type, {
        "steps": [
            "1. Visual inspection and hazmat assessment",
            "2. Manual disassembly by trained technician",
            "3. Sort components by material type",
            "4. Send to certified WEEE recycler",
        ],
        "key_materials": "Varies by device — refer to hazmat checker",
        "certified_process": "Certified WEEE-compliant recycler",
    })

    st.markdown(f"### ♻️ Recycling Guide — {device_type.replace('_', ' ').title()}")

    st.markdown("#### Step-by-Step Process")
    for step in rec["steps"]:
        if "⚠️" in step or "SAFETY" in step or "HIGH HAZMAT" in step:
            st.warning(step)
        else:
            st.markdown(f"- {step}")

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Key Materials to Recover:** {rec['key_materials']}")
    with col2:
        st.info(f"**Recommended Process:** {rec['certified_process']}")

    # Hazmat check
    try:
        from industrial.compliance.hazmat_rules import HazmatChecker
        checker = HazmatChecker()
        hazmat = checker.check_device(device_type)
        if hazmat["hazmat_materials_present"]:
            st.warning(f"⚠️ **Hazmat Materials:** {', '.join(hazmat['hazmat_materials_present'])} — special handling required.")
    except Exception:
        pass
