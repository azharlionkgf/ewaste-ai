"""
🔬 E-Waste 3D Knowledge Engine
==============================
AI-powered device knowledge database + Three.js 3D viewer
By: Azhar Fareed Mulla (2SA25MC002)
"""
import json, sqlite3, os, hashlib
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge.db')

# ═══ DEVICE KNOWLEDGE DATABASE ═══
DEVICE_KNOWLEDGE = {
    "Mobile Phones": {
        "category": "Mobile Phones", "icon": "📱",
        "brands": ["Apple iPhone", "Samsung Galaxy", "Xiaomi Redmi", "OnePlus", "Vivo", "Oppo", "Realme", "Google Pixel", "Motorola", "Nokia"],
        "avg_weight_kg": 0.18, "avg_lifespan_years": 3,
        "components": [
            {"name": "Display (LCD/OLED)", "material": "Glass, Indium, Rare Earth", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#4FC3F7"},
            {"name": "Battery (Li-ion)", "material": "Lithium, Cobalt, Nickel", "weight_pct": 20, "hazardous": True, "recyclable": True, "value_usd": 0.80, "color": "#FF5252"},
            {"name": "Circuit Board (PCB)", "material": "Gold, Silver, Copper, Palladium", "weight_pct": 15, "hazardous": True, "recyclable": True, "value_usd": 1.50, "color": "#66BB6A"},
            {"name": "Camera Module", "material": "Silicon, Glass, Rare Earth", "weight_pct": 3, "hazardous": False, "recyclable": True, "value_usd": 0.30, "color": "#AB47BC"},
            {"name": "Metal Frame", "material": "Aluminum, Stainless Steel", "weight_pct": 18, "hazardous": False, "recyclable": True, "value_usd": 0.20, "color": "#78909C"},
            {"name": "Plastic Casing", "material": "ABS Plastic, Polycarbonate", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 0.05, "color": "#8D6E63"},
            {"name": "Speaker/Mic", "material": "Copper, Neodymium Magnets", "weight_pct": 2, "hazardous": False, "recyclable": True, "value_usd": 0.10, "color": "#FFA726"},
            {"name": "SIM/SD Slot", "material": "Copper, Plastic", "weight_pct": 1, "hazardous": False, "recyclable": True, "value_usd": 0.02, "color": "#26C6DA"},
            {"name": "Cables/Connectors", "material": "Copper, Gold plating", "weight_pct": 3, "hazardous": False, "recyclable": True, "value_usd": 0.15, "color": "#FFEE58"},
            {"name": "Vibration Motor", "material": "Copper, Steel, Magnets", "weight_pct": 1, "hazardous": False, "recyclable": True, "value_usd": 0.05, "color": "#EF5350"}
        ],
        "precious_metals": {"Gold (mg)": 30, "Silver (mg)": 300, "Copper (g)": 15, "Palladium (mg)": 10, "Platinum (mg)": 2},
        "hazardous_materials": ["Lithium (battery)", "Lead (solder)", "Brominated Flame Retardants"],
        "recycling_steps": ["1. Power off & remove SIM/SD cards", "2. Discharge battery to <30%", "3. Remove back cover/screws", "4. Carefully disconnect battery ribbon cable", "5. Remove battery (DO NOT puncture)", "6. Unscrew PCB mounting screws", "7. Disconnect display flex cable", "8. Remove camera module", "9. Separate metal frame from plastic", "10. Sort components by material type"],
        "safety_warnings": ["⚠️ Li-ion battery can EXPLODE if punctured", "⚠️ Lead-free solder still contains trace toxins", "⚠️ OLED screens contain organic compounds", "⚠️ Wear anti-static wristband when handling PCB"],
        "recovery_value_usd": 3.50,
        "environmental_impact": {"co2_saved_kg": 5, "water_saved_liters": 200, "energy_saved_kwh": 10, "toxic_prevented_kg": 0.02},
        "repairability_score": 6, "repair_difficulty": "Medium",
        "3d_shape": "phone"
    },
    "Laptops": {
        "category": "Laptops", "icon": "💻",
        "brands": ["Apple MacBook", "Dell", "HP", "Lenovo ThinkPad", "Asus", "Acer", "MSI", "Samsung", "Microsoft Surface", "Toshiba"],
        "avg_weight_kg": 2.2, "avg_lifespan_years": 5,
        "components": [
            {"name": "Display Panel", "material": "LCD/LED, Glass, Indium", "weight_pct": 20, "hazardous": False, "recyclable": True, "value_usd": 2.00, "color": "#4FC3F7"},
            {"name": "Battery Pack", "material": "Lithium-ion cells, BMS circuit", "weight_pct": 12, "hazardous": True, "recyclable": True, "value_usd": 3.00, "color": "#FF5252"},
            {"name": "Motherboard", "material": "Gold, Silver, Copper, Tin, Palladium", "weight_pct": 10, "hazardous": True, "recyclable": True, "value_usd": 5.00, "color": "#66BB6A"},
            {"name": "CPU/GPU Chips", "material": "Silicon, Gold wire bonds", "weight_pct": 2, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#AB47BC"},
            {"name": "RAM Modules", "material": "Gold contacts, Silicon, PCB", "weight_pct": 1, "hazardous": False, "recyclable": True, "value_usd": 0.80, "color": "#26C6DA"},
            {"name": "Storage (SSD/HDD)", "material": "Aluminum, Rare Earth magnets, PCB", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 1.00, "color": "#FFA726"},
            {"name": "Keyboard", "material": "ABS Plastic, Copper membrane, Rubber", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 0.30, "color": "#8D6E63"},
            {"name": "Metal Chassis", "material": "Aluminum/Magnesium alloy", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#78909C"},
            {"name": "Cooling System", "material": "Copper heatpipe, Aluminum fins, Fan", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 0.40, "color": "#EF5350"},
            {"name": "Speakers", "material": "Neodymium magnets, Copper coil", "weight_pct": 2, "hazardous": False, "recyclable": True, "value_usd": 0.20, "color": "#FFEE58"},
            {"name": "WiFi/BT Card", "material": "PCB, Antenna, Gold contacts", "weight_pct": 1, "hazardous": False, "recyclable": True, "value_usd": 0.30, "color": "#69F0AE"},
            {"name": "Power Port/USB", "material": "Copper, Gold plating, Plastic", "weight_pct": 1, "hazardous": False, "recyclable": True, "value_usd": 0.15, "color": "#CE93D8"}
        ],
        "precious_metals": {"Gold (mg)": 50, "Silver (mg)": 500, "Copper (g)": 80, "Palladium (mg)": 20, "Platinum (mg)": 5},
        "hazardous_materials": ["Lithium (battery cells)", "Lead (solder joints)", "Mercury (older LCD backlights)", "Cadmium (older displays)", "BFRs (plastic casings)"],
        "recycling_steps": ["1. Backup data & factory reset", "2. Remove power adapter", "3. Remove bottom panel screws", "4. Disconnect & remove battery", "5. Remove RAM & storage drives", "6. Disconnect display cable", "7. Remove motherboard screws & lift", "8. Separate keyboard from chassis", "9. Remove cooling assembly", "10. Separate metals from plastics", "11. Sort components for recycling"],
        "safety_warnings": ["⚠️ Battery pack contains multiple Li-ion cells — fire risk", "⚠️ Older laptops may have mercury in LCD backlight", "⚠️ WIPE ALL DATA before recycling (use DBAN)", "⚠️ Capacitors can hold charge — discharge first"],
        "recovery_value_usd": 12.00,
        "environmental_impact": {"co2_saved_kg": 30, "water_saved_liters": 1500, "energy_saved_kwh": 80, "toxic_prevented_kg": 0.15},
        "repairability_score": 5, "repair_difficulty": "Medium-Hard",
        "3d_shape": "laptop"
    },
    "Tablets": {
        "category": "Tablets", "icon": "📟",
        "brands": ["Apple iPad", "Samsung Galaxy Tab", "Amazon Kindle", "Lenovo Tab", "Microsoft Surface", "Huawei MatePad"],
        "avg_weight_kg": 0.5, "avg_lifespan_years": 4,
        "components": [
            {"name": "Touchscreen Display", "material": "Gorilla Glass, ITO, OLED/LCD", "weight_pct": 30, "hazardous": False, "recyclable": True, "value_usd": 1.00, "color": "#4FC3F7"},
            {"name": "Battery", "material": "Li-Polymer cells", "weight_pct": 25, "hazardous": True, "recyclable": True, "value_usd": 1.50, "color": "#FF5252"},
            {"name": "Logic Board", "material": "Gold, Silver, Copper, Silicon", "weight_pct": 10, "hazardous": True, "recyclable": True, "value_usd": 2.50, "color": "#66BB6A"},
            {"name": "Metal Back Panel", "material": "Aluminum alloy", "weight_pct": 20, "hazardous": False, "recyclable": True, "value_usd": 0.80, "color": "#78909C"},
            {"name": "Camera Modules", "material": "Silicon, Glass, Rare Earth", "weight_pct": 3, "hazardous": False, "recyclable": True, "value_usd": 0.40, "color": "#AB47BC"},
            {"name": "Speakers", "material": "Neodymium, Copper", "weight_pct": 3, "hazardous": False, "recyclable": True, "value_usd": 0.15, "color": "#FFA726"},
            {"name": "Cables/Connectors", "material": "Copper, Gold plating", "weight_pct": 4, "hazardous": False, "recyclable": True, "value_usd": 0.20, "color": "#FFEE58"},
            {"name": "Plastic Components", "material": "ABS, Polycarbonate", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 0.05, "color": "#8D6E63"}
        ],
        "precious_metals": {"Gold (mg)": 25, "Silver (mg)": 250, "Copper (g)": 20, "Palladium (mg)": 8},
        "hazardous_materials": ["Lithium-Polymer (battery)", "Lead (solder)", "Indium (display)"],
        "recycling_steps": ["1. Factory reset & sign out", "2. Heat display edges to soften adhesive", "3. Use suction cup to separate screen", "4. Disconnect battery first", "5. Remove logic board", "6. Separate metal back from components", "7. Sort materials for recycling"],
        "safety_warnings": ["⚠️ Li-Po batteries swell & can ignite", "⚠️ Display adhesive requires heat gun — burn risk", "⚠️ Fragile glass — wear cut-resistant gloves"],
        "recovery_value_usd": 6.00,
        "environmental_impact": {"co2_saved_kg": 12, "water_saved_liters": 600, "energy_saved_kwh": 30, "toxic_prevented_kg": 0.05},
        "repairability_score": 3, "repair_difficulty": "Hard",
        "3d_shape": "tablet"
    },
    "Desktop Computers": {
        "category": "Desktop Computers", "icon": "🖥️",
        "brands": ["Dell OptiPlex", "HP ProDesk", "Lenovo ThinkCentre", "Apple iMac", "Custom Built", "Acer", "ASUS"],
        "avg_weight_kg": 8.0, "avg_lifespan_years": 6,
        "components": [
            {"name": "Motherboard", "material": "Gold, Silver, Copper, FR-4 PCB", "weight_pct": 8, "hazardous": True, "recyclable": True, "value_usd": 4.00, "color": "#66BB6A"},
            {"name": "CPU", "material": "Silicon, Gold wire bonds, Copper IHS", "weight_pct": 1, "hazardous": False, "recyclable": True, "value_usd": 2.00, "color": "#AB47BC"},
            {"name": "GPU Card", "material": "PCB, Gold contacts, Copper, Silicon", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 3.00, "color": "#EF5350"},
            {"name": "RAM Sticks", "material": "Gold contacts, Silicon chips, PCB", "weight_pct": 1, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#26C6DA"},
            {"name": "Power Supply", "material": "Copper transformer, Steel case, Capacitors", "weight_pct": 15, "hazardous": True, "recyclable": True, "value_usd": 2.00, "color": "#FFA726"},
            {"name": "Hard Drives", "material": "Aluminum platters, Rare Earth magnets, PCB", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#78909C"},
            {"name": "Steel Case", "material": "Cold-rolled steel, Screws", "weight_pct": 40, "hazardous": False, "recyclable": True, "value_usd": 2.00, "color": "#90A4AE"},
            {"name": "Cooling Fans", "material": "Plastic, Copper motor, Bearings", "weight_pct": 4, "hazardous": False, "recyclable": True, "value_usd": 0.30, "color": "#69F0AE"},
            {"name": "Cables/Wires", "material": "Copper, PVC insulation", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#FFEE58"},
            {"name": "Optical Drive", "material": "Aluminum, Laser diode, PCB, Plastic", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 0.30, "color": "#CE93D8"}
        ],
        "precious_metals": {"Gold (mg)": 100, "Silver (mg)": 800, "Copper (g)": 200, "Palladium (mg)": 30, "Platinum (mg)": 8},
        "hazardous_materials": ["Capacitor electrolyte", "Lead solder (older models)", "Mercury switches (rare)", "BFRs in plastic"],
        "recycling_steps": ["1. Wipe all data (DBAN/Secure Erase)", "2. Unplug & discharge capacitors (wait 5 min)", "3. Open case (thumbscrews/screws)", "4. Remove GPU, RAM, drives", "5. Disconnect PSU cables & remove", "6. Remove motherboard standoffs & lift out", "7. Separate steel case", "8. Sort PCBs, metals, plastics, cables"],
        "safety_warnings": ["⚠️ PSU capacitors hold LETHAL charge", "⚠️ CRT monitors (older) have 25kV — DEADLY", "⚠️ Sharp metal edges — wear gloves", "⚠️ Heavy components — lift carefully"],
        "recovery_value_usd": 20.00,
        "environmental_impact": {"co2_saved_kg": 40, "water_saved_liters": 2000, "energy_saved_kwh": 120, "toxic_prevented_kg": 0.25},
        "repairability_score": 9, "repair_difficulty": "Easy",
        "3d_shape": "desktop"
    },
    "Televisions": {
        "category": "Televisions", "icon": "📺",
        "brands": ["Samsung", "LG", "Sony", "TCL", "Hisense", "Panasonic", "Vizio", "Philips"],
        "avg_weight_kg": 12.0, "avg_lifespan_years": 7,
        "components": [
            {"name": "LED/OLED Panel", "material": "Glass, Indium Tin Oxide, Liquid Crystal/OLED", "weight_pct": 35, "hazardous": True, "recyclable": True, "value_usd": 3.00, "color": "#4FC3F7"},
            {"name": "Main Board", "material": "PCB, Gold, Silver, Copper, ICs", "weight_pct": 5, "hazardous": True, "recyclable": True, "value_usd": 4.00, "color": "#66BB6A"},
            {"name": "Power Supply Board", "material": "Capacitors, Transformer, Copper", "weight_pct": 8, "hazardous": True, "recyclable": True, "value_usd": 2.50, "color": "#FFA726"},
            {"name": "Plastic Frame/Back", "material": "ABS Plastic, Polycarbonate", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#8D6E63"},
            {"name": "Metal Chassis", "material": "Steel, Aluminum", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#78909C"},
            {"name": "Speakers", "material": "Magnets, Copper, Paper cone", "weight_pct": 4, "hazardous": False, "recyclable": True, "value_usd": 0.30, "color": "#AB47BC"},
            {"name": "LED Backlight Strips", "material": "LEDs, Aluminum, Adhesive", "weight_pct": 3, "hazardous": False, "recyclable": True, "value_usd": 0.20, "color": "#FFEE58"},
            {"name": "Cables/Ribbon", "material": "Copper, FPC", "weight_pct": 3, "hazardous": False, "recyclable": True, "value_usd": 0.15, "color": "#69F0AE"},
            {"name": "Stand/Mount", "material": "Steel, Plastic", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#90A4AE"}
        ],
        "precious_metals": {"Gold (mg)": 40, "Silver (mg)": 400, "Copper (g)": 100, "Palladium (mg)": 15, "Indium (mg)": 50},
        "hazardous_materials": ["Mercury (older CCFL backlights)", "Lead (CRT types)", "Cadmium (older displays)", "Capacitor electrolyte"],
        "recycling_steps": ["1. Unplug & wait 30 min for discharge", "2. Remove stand/mount", "3. Remove back cover screws", "4. Photograph cable connections", "5. Disconnect ribbon cables carefully", "6. Remove main board & PSU board", "7. Separate panel from frame", "8. Sort plastics, metals, PCBs, glass"],
        "safety_warnings": ["⚠️ PSU board capacitors — LETHAL VOLTAGE", "⚠️ CRT TVs contain lead glass + 25kV", "⚠️ CCFL tubes contain mercury vapor", "⚠️ Large panels are fragile — handle flat"],
        "recovery_value_usd": 8.00,
        "environmental_impact": {"co2_saved_kg": 50, "water_saved_liters": 3000, "energy_saved_kwh": 150, "toxic_prevented_kg": 0.30},
        "repairability_score": 5, "repair_difficulty": "Medium",
        "3d_shape": "tv"
    },
    "Batteries": {
        "category": "Batteries", "icon": "🔋",
        "brands": ["Panasonic", "Samsung SDI", "LG Chem", "CATL", "BYD", "Sony", "Duracell", "Energizer"],
        "avg_weight_kg": 0.3, "avg_lifespan_years": 3,
        "components": [
            {"name": "Cathode", "material": "Lithium Cobalt Oxide / LFP / NMC", "weight_pct": 30, "hazardous": True, "recyclable": True, "value_usd": 2.00, "color": "#FF5252"},
            {"name": "Anode", "material": "Graphite, Copper foil", "weight_pct": 20, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#424242"},
            {"name": "Electrolyte", "material": "Lithium salt in organic solvent", "weight_pct": 15, "hazardous": True, "recyclable": False, "value_usd": 0.00, "color": "#FFA726"},
            {"name": "Separator", "material": "Polyethylene/Polypropylene membrane", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 0.02, "color": "#E0E0E0"},
            {"name": "Casing", "material": "Aluminum/Steel can", "weight_pct": 20, "hazardous": False, "recyclable": True, "value_usd": 0.10, "color": "#78909C"},
            {"name": "BMS Circuit", "material": "PCB, MOSFET, Thermistor", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 0.30, "color": "#66BB6A"},
            {"name": "Terminals/Tabs", "material": "Nickel, Copper", "weight_pct": 3, "hazardous": False, "recyclable": True, "value_usd": 0.05, "color": "#FFEE58"},
            {"name": "Safety Vent", "material": "Metal disc", "weight_pct": 2, "hazardous": False, "recyclable": True, "value_usd": 0.01, "color": "#90A4AE"}
        ],
        "precious_metals": {"Cobalt (g)": 8, "Lithium (g)": 2, "Nickel (g)": 5, "Copper (g)": 3, "Manganese (g)": 3},
        "hazardous_materials": ["Lithium (water reactive — FIRE)", "Cobalt (toxic dust)", "Electrolyte (flammable, corrosive)", "Hydrofluoric acid (if burned)"],
        "recycling_steps": ["1. ⚠️ DISCHARGE below 1V (use resistor)", "2. Tape all terminals with electrical tape", "3. Store in sand-filled metal container", "4. NEVER open — send to certified recycler", "5. Hydrometallurgical / Pyrometallurgical processing", "6. Cobalt, Lithium, Nickel recovered"],
        "safety_warnings": ["🔥 CAN EXPLODE — never puncture, crush, or short-circuit", "🔥 Thermal runaway at 150°C — chain reaction", "☠️ Electrolyte is TOXIC and FLAMMABLE", "💧 Lithium reacts VIOLENTLY with water", "🚫 NEVER put in regular trash or fire"],
        "recovery_value_usd": 3.00,
        "environmental_impact": {"co2_saved_kg": 3, "water_saved_liters": 100, "energy_saved_kwh": 5, "toxic_prevented_kg": 0.10},
        "repairability_score": 1, "repair_difficulty": "Do Not Attempt",
        "3d_shape": "battery"
    },
    "PCBs/Circuit Boards": {
        "category": "PCBs/Circuit Boards", "icon": "🔌",
        "brands": ["Generic", "Intel", "AMD", "Qualcomm", "MediaTek", "NVIDIA"],
        "avg_weight_kg": 0.15, "avg_lifespan_years": 8,
        "components": [
            {"name": "FR-4 Substrate", "material": "Fiberglass + Epoxy resin", "weight_pct": 40, "hazardous": True, "recyclable": True, "value_usd": 0.50, "color": "#66BB6A"},
            {"name": "Copper Traces", "material": "Copper (multi-layer)", "weight_pct": 20, "hazardous": False, "recyclable": True, "value_usd": 2.00, "color": "#FFA726"},
            {"name": "IC Chips", "material": "Silicon, Gold bond wires", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 5.00, "color": "#424242"},
            {"name": "Solder Joints", "material": "Tin-Lead or Lead-free (SAC)", "weight_pct": 5, "hazardous": True, "recyclable": True, "value_usd": 0.30, "color": "#78909C"},
            {"name": "Gold Contacts/Edge", "material": "Gold plating", "weight_pct": 1, "hazardous": False, "recyclable": True, "value_usd": 3.00, "color": "#FFD700"},
            {"name": "Capacitors", "material": "Ceramic/Aluminum, Electrolyte", "weight_pct": 8, "hazardous": True, "recyclable": True, "value_usd": 0.20, "color": "#26C6DA"},
            {"name": "Resistors", "material": "Carbon, Metal film, Ceramic", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 0.05, "color": "#8D6E63"},
            {"name": "Connectors", "material": "Gold/Nickel plated pins, Plastic", "weight_pct": 6, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#FFEE58"},
            {"name": "Inductors/Coils", "material": "Ferrite core, Copper wire", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 0.15, "color": "#AB47BC"}
        ],
        "precious_metals": {"Gold (g)": 0.3, "Silver (g)": 1.0, "Copper (g)": 30, "Palladium (mg)": 50, "Platinum (mg)": 10},
        "hazardous_materials": ["Lead solder (older boards)", "BFRs (flame retardants in substrate)", "Beryllium (some connectors)", "Cadmium (some components)"],
        "recycling_steps": ["1. Remove heatsinks & fans", "2. Desolder large components (hot air)", "3. Separate IC chips for gold recovery", "4. Shred remaining PCB", "5. Electrolytic/Chemical gold extraction", "6. Copper smelting recovery", "7. Precious metal refining"],
        "safety_warnings": ["⚠️ BFR dust is carcinogenic — use N95 mask", "⚠️ Lead solder fumes — ventilation required", "⚠️ Capacitors may hold charge", "⚠️ Chemical extraction requires proper lab setup"],
        "recovery_value_usd": 12.00,
        "environmental_impact": {"co2_saved_kg": 2, "water_saved_liters": 50, "energy_saved_kwh": 8, "toxic_prevented_kg": 0.05},
        "repairability_score": 7, "repair_difficulty": "Expert",
        "3d_shape": "pcb"
    },
    "Printers": {
        "category": "Printers", "icon": "🖨️",
        "brands": ["HP", "Canon", "Epson", "Brother", "Samsung", "Xerox", "Ricoh"],
        "avg_weight_kg": 8.0, "avg_lifespan_years": 5,
        "components": [
            {"name": "Plastic Housing", "material": "ABS, HIPS Plastic", "weight_pct": 35, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#8D6E63"},
            {"name": "Main PCB", "material": "Gold, Copper, FR-4", "weight_pct": 5, "hazardous": True, "recyclable": True, "value_usd": 2.00, "color": "#66BB6A"},
            {"name": "Stepper Motors", "material": "Copper windings, Steel, Magnets", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 1.00, "color": "#78909C"},
            {"name": "Metal Frame", "material": "Steel chassis", "weight_pct": 20, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#90A4AE"},
            {"name": "Print Head", "material": "Piezoelectric/Thermal, Gold contacts", "weight_pct": 3, "hazardous": False, "recyclable": True, "value_usd": 0.80, "color": "#AB47BC"},
            {"name": "Gears/Rollers", "material": "Nylon, Rubber, Steel shafts", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 0.20, "color": "#FFA726"},
            {"name": "Power Supply", "material": "Transformer, Capacitors, PCB", "weight_pct": 8, "hazardous": True, "recyclable": True, "value_usd": 0.80, "color": "#FFEE58"},
            {"name": "Toner/Ink Cartridge", "material": "Plastic, Toner powder/Ink, PCB chip", "weight_pct": 5, "hazardous": True, "recyclable": True, "value_usd": 0.50, "color": "#424242"},
            {"name": "Cables/Ribbon", "material": "Copper, FPC", "weight_pct": 4, "hazardous": False, "recyclable": True, "value_usd": 0.15, "color": "#69F0AE"}
        ],
        "precious_metals": {"Gold (mg)": 30, "Silver (mg)": 200, "Copper (g)": 60, "Palladium (mg)": 10},
        "hazardous_materials": ["Toner powder (carcinogenic if inhaled)", "Ink chemicals", "Capacitor electrolyte", "Lead solder"],
        "recycling_steps": ["1. Remove toner/ink cartridges (separate recycling)", "2. Unplug & remove all paper", "3. Remove outer plastic housing", "4. Remove metal frame/chassis", "5. Extract motors & gears", "6. Remove PCBs & PSU", "7. Sort plastics, metals, PCBs"],
        "safety_warnings": ["⚠️ Toner powder is FINE particulate — wear N95 mask", "⚠️ Laser printer fuser runs at 200°C — BURN RISK", "⚠️ PSU capacitors hold charge"],
        "recovery_value_usd": 5.00,
        "environmental_impact": {"co2_saved_kg": 15, "water_saved_liters": 500, "energy_saved_kwh": 40, "toxic_prevented_kg": 0.10},
        "repairability_score": 6, "repair_difficulty": "Medium",
        "3d_shape": "printer"
    },
    "Large Appliances": {
        "category": "Large Appliances", "icon": "🏠",
        "brands": ["LG", "Samsung", "Whirlpool", "Bosch", "Haier", "Godrej", "Voltas", "Daikin"],
        "avg_weight_kg": 50.0, "avg_lifespan_years": 10,
        "components": [
            {"name": "Compressor/Motor", "material": "Copper windings, Steel, Refrigerant", "weight_pct": 25, "hazardous": True, "recyclable": True, "value_usd": 15.00, "color": "#78909C"},
            {"name": "Steel Body", "material": "Cold-rolled steel, Paint", "weight_pct": 35, "hazardous": False, "recyclable": True, "value_usd": 10.00, "color": "#90A4AE"},
            {"name": "Copper Tubing", "material": "Copper refrigerant lines", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 5.00, "color": "#FFA726"},
            {"name": "Plastic Parts", "material": "PP, ABS, PS plastic", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 1.00, "color": "#8D6E63"},
            {"name": "Insulation", "material": "Polyurethane foam (may contain CFC/HCFC)", "weight_pct": 8, "hazardous": True, "recyclable": False, "value_usd": 0.00, "color": "#E0E0E0"},
            {"name": "Control Board", "material": "PCB, Microcontroller, Relays", "weight_pct": 2, "hazardous": True, "recyclable": True, "value_usd": 2.00, "color": "#66BB6A"},
            {"name": "Glass Shelves/Door", "material": "Tempered glass", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#4FC3F7"},
            {"name": "Rubber Seals", "material": "PVC, Rubber gaskets", "weight_pct": 3, "hazardous": False, "recyclable": True, "value_usd": 0.10, "color": "#424242"},
            {"name": "Wiring Harness", "material": "Copper wire, PVC insulation", "weight_pct": 2, "hazardous": False, "recyclable": True, "value_usd": 1.00, "color": "#FFEE58"}
        ],
        "precious_metals": {"Copper (g)": 500, "Steel (kg)": 15, "Aluminum (g)": 200},
        "hazardous_materials": ["Refrigerant gas (R-134a/R-410A/R-600a)", "CFC/HCFC (older units — ozone depleting)", "Compressor oil", "PU foam blowing agents", "Mercury (older thermostats)"],
        "recycling_steps": ["1. ⚠️ Recover refrigerant gas FIRST (certified tech)", "2. Remove doors & glass shelves", "3. Remove compressor unit", "4. Drain compressor oil safely", "5. Remove control boards & wiring", "6. Shred steel body", "7. Separate copper from insulation", "8. Treat PU foam for blowing agent recovery"],
        "safety_warnings": ["⚠️ R-600a refrigerant is FLAMMABLE — no sparks", "⚠️ CFC/HCFC release destroys ozone layer", "⚠️ Compressor starts suddenly — lock out power", "⚠️ Very heavy — use proper lifting equipment"],
        "recovery_value_usd": 35.00,
        "environmental_impact": {"co2_saved_kg": 150, "water_saved_liters": 10000, "energy_saved_kwh": 500, "toxic_prevented_kg": 2.00},
        "repairability_score": 7, "repair_difficulty": "Medium",
        "3d_shape": "appliance"
    },
    "Small Appliances": {
        "category": "Small Appliances", "icon": "🔌",
        "brands": ["Philips", "Bajaj", "Havells", "Prestige", "Morphy Richards", "Braun"],
        "avg_weight_kg": 3.0, "avg_lifespan_years": 5,
        "components": [
            {"name": "Electric Motor", "material": "Copper windings, Steel core, Magnets", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#78909C"},
            {"name": "Plastic Housing", "material": "PP, ABS Plastic", "weight_pct": 35, "hazardous": False, "recyclable": True, "value_usd": 0.20, "color": "#8D6E63"},
            {"name": "Heating Element", "material": "Nichrome wire, Ceramic", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 0.30, "color": "#FF5252"},
            {"name": "Power Cord", "material": "Copper wire, PVC, Plug", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 0.20, "color": "#FFEE58"},
            {"name": "Control PCB", "material": "Small PCB, Relay, Triac", "weight_pct": 3, "hazardous": True, "recyclable": True, "value_usd": 0.30, "color": "#66BB6A"},
            {"name": "Metal Parts", "material": "Steel/Aluminum blades, shafts", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#90A4AE"},
            {"name": "Rubber/Silicone", "material": "Gaskets, Feet, Seals", "weight_pct": 4, "hazardous": False, "recyclable": False, "value_usd": 0.00, "color": "#424242"}
        ],
        "precious_metals": {"Copper (g)": 40, "Steel (g)": 100, "Aluminum (g)": 30},
        "hazardous_materials": ["Capacitors (electrolyte)", "Lead solder (older models)", "Asbestos (very old heaters)"],
        "recycling_steps": ["1. Unplug & cut power cord", "2. Remove outer casing screws", "3. Extract motor assembly", "4. Remove heating element", "5. Separate PCB", "6. Sort metals, plastics, copper"],
        "safety_warnings": ["⚠️ Heating elements may have residual heat", "⚠️ Capacitors may hold charge", "⚠️ Sharp blades inside (blenders, grinders)"],
        "recovery_value_usd": 2.00,
        "environmental_impact": {"co2_saved_kg": 8, "water_saved_liters": 300, "energy_saved_kwh": 20, "toxic_prevented_kg": 0.03},
        "repairability_score": 8, "repair_difficulty": "Easy",
        "3d_shape": "small_appliance"
    },
    "Servers & Data Centers": {
        "category": "Servers & Data Centers", "icon": "🗄️",
        "brands": ["Dell PowerEdge", "HPE ProLiant", "Cisco UCS", "Lenovo ThinkSystem", "Supermicro", "IBM"],
        "avg_weight_kg": 22.0, "avg_lifespan_years": 4,
        "components": [
            {"name": "Server Motherboard", "material": "High-grade Multi-layer FR4, Gold, Silver, Palladium", "weight_pct": 12, "hazardous": True, "recyclable": True, "value_usd": 18.00, "color": "#66BB6A"},
            {"name": "Redundant PSUs (2x)", "material": "Copper transformers, Heavy capacitors, Steel", "weight_pct": 18, "hazardous": True, "recyclable": True, "value_usd": 8.00, "color": "#FFA726"},
            {"name": "Xeon / EPYC CPUs", "material": "High-purity Gold pin bonds, Silicon, Copper IHS", "weight_pct": 2, "hazardous": False, "recyclable": True, "value_usd": 15.00, "color": "#AB47BC"},
            {"name": "ECC Registered RAM", "material": "Gold contacts, DRAM chips", "weight_pct": 3, "hazardous": False, "recyclable": True, "value_usd": 12.00, "color": "#26C6DA"},
            {"name": "SAS / NVMe Drive Array", "material": "Aluminum, Rare Earth magnets, PCB", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 10.00, "color": "#78909C"},
            {"name": "High-RPM Blower Fans", "material": "Copper motors, Plastic housings", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 2.00, "color": "#69F0AE"},
            {"name": "Rackmount Steel Chassis", "material": "Galvanized cold-rolled steel", "weight_pct": 42, "hazardous": False, "recyclable": True, "value_usd": 6.00, "color": "#90A4AE"},
            {"name": "RAID / HBA Controller", "material": "Battery-backed cache, Gold contacts, PCB", "weight_pct": 3, "hazardous": True, "recyclable": True, "value_usd": 4.00, "color": "#FFEE58"}
        ],
        "precious_metals": {"Gold (mg)": 250, "Silver (mg)": 1500, "Copper (g)": 450, "Palladium (mg)": 80, "Platinum (mg)": 20},
        "hazardous_materials": ["RAID cache Li-ion battery", "High-capacity electrolytic capacitors", "Lead solder on legacy boards"],
        "recycling_steps": ["1. Department of Defense / NIST 800-88 sanitization on all storage arrays", "2. Extract RAID backup batteries", "3. Pull hot-swap PSUs and discharge", "4. Remove CPU heatsinks and extract gold-rich CPUs", "5. Separate server-grade motherboards for high-yield precious metal refining"],
        "safety_warnings": ["⚠️ Cryptographic data sanitization required prior to physical handling", "⚠️ Heavy rack units (20-30kg) - lift with dual operators", "⚠️ Redundant PSUs hold large residual charges"],
        "recovery_value_usd": 75.00,
        "environmental_impact": {"co2_saved_kg": 180, "water_saved_liters": 4500, "energy_saved_kwh": 350, "toxic_prevented_kg": 0.80},
        "repairability_score": 9, "repair_difficulty": "Modular / Professional",
        "3d_shape": "desktop"
    },
    "Solar Inverters & Renewables": {
        "category": "Solar Inverters & Renewables", "icon": "☀️",
        "brands": ["SMA Solar", "Fronius", "Enphase", "Huawei Solar", "Sungrow", "SolarEdge", "Luminous"],
        "avg_weight_kg": 18.0, "avg_lifespan_years": 12,
        "components": [
            {"name": "High-Power IGBT Modules", "material": "Silicon, Copper baseplate, Aluminum wire bonds", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 10.00, "color": "#AB47BC"},
            {"name": "Toroidal Inductors & Transformers", "material": "Pure Copper windings, Ferrite cores", "weight_pct": 30, "hazardous": False, "recyclable": True, "value_usd": 14.00, "color": "#FFA726"},
            {"name": "DC Bus Film Capacitors", "material": "Polypropylene film, Aluminum, Plastic can", "weight_pct": 12, "hazardous": True, "recyclable": True, "value_usd": 4.00, "color": "#26C6DA"},
            {"name": "Aluminum Heat Sink", "material": "Extruded structural aluminum", "weight_pct": 28, "hazardous": False, "recyclable": True, "value_usd": 8.00, "color": "#78909C"},
            {"name": "Control & DSP Board", "material": "Multi-layer PCB, Gold plating, ICs", "weight_pct": 4, "hazardous": True, "recyclable": True, "value_usd": 5.00, "color": "#66BB6A"},
            {"name": "Weatherproof Enclosure", "material": "Powder-coated die-cast aluminum / NEMA steel", "weight_pct": 18, "hazardous": False, "recyclable": True, "value_usd": 5.00, "color": "#90A4AE"}
        ],
        "precious_metals": {"Copper (g)": 1200, "Aluminum (kg)": 5.5, "Gold (mg)": 25, "Silver (mg)": 150},
        "hazardous_materials": ["High-voltage DC bus (up to 1000V DC)", "Potting resins / Polyurethane sealant"],
        "recycling_steps": ["1. Ensure DC isolator & AC breaker are locked out", "2. Wait 45 minutes for internal bleed resistors to discharge DC bus below 10V", "3. Open enclosure and test with multimeter", "4. Dismantle high-purity copper inductors", "5. Detach aluminum heat sink for scrap smelting"],
        "safety_warnings": ["⚠️ LETHAL DC VOLTAGES up to 1000V from PV string input", "⚠️ Heavy inductive kickback risk if opened live", "⚠️ Hot surfaces on heat sinks post-operation"],
        "recovery_value_usd": 46.00,
        "environmental_impact": {"co2_saved_kg": 95, "water_saved_liters": 2800, "energy_saved_kwh": 220, "toxic_prevented_kg": 0.40},
        "repairability_score": 7, "repair_difficulty": "Certified Electrician Only",
        "3d_shape": "appliance"
    },
    "Industrial PLCs & Automation": {
        "category": "Industrial PLCs & Automation", "icon": "🏭",
        "brands": ["Siemens SIMATIC", "Rockwell Allen-Bradley", "Schneider Electric", "Mitsubishi Electric", "Omron", "ABB"],
        "avg_weight_kg": 2.5, "avg_lifespan_years": 15,
        "components": [
            {"name": "Processor Module (CPU)", "material": "Industrial PCB, High-rel ICs, Gold contacts", "weight_pct": 20, "hazardous": True, "recyclable": True, "value_usd": 8.00, "color": "#66BB6A"},
            {"name": "I/O Relay Terminal Block", "material": "Silver-alloy contacts, Copper bus, PBT plastic", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 6.00, "color": "#FFA726"},
            {"name": "Optocoupler Isolation Subsystem", "material": "Silicon, Gallium arsenide diodes, PCB", "weight_pct": 8, "hazardous": True, "recyclable": True, "value_usd": 2.00, "color": "#AB47BC"},
            {"name": "DIN-Rail Metal Backplate", "material": "Zinc-plated cold rolled steel / Aluminum", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#78909C"},
            {"name": "Flame-Retardant Casing", "material": "UL94-V0 Polycarbonate/ABS blend", "weight_pct": 18, "hazardous": True, "recyclable": False, "value_usd": 0.20, "color": "#8D6E63"},
            {"name": "Lithium RTC Backup Battery", "material": "Lithium thionyl chloride (Li-SOCl2)", "weight_pct": 4, "hazardous": True, "recyclable": True, "value_usd": 1.00, "color": "#FF5252"}
        ],
        "precious_metals": {"Gold (mg)": 60, "Silver (mg)": 400, "Copper (g)": 80, "Palladium (mg)": 15},
        "hazardous_materials": ["Li-SOCl2 battery (highly toxic, water-reactive)", "Brominated flame retardants (UL94-V0)", "Trace Gallium/Arsenic in optocouplers"],
        "recycling_steps": ["1. Unclip from industrial DIN rail", "2. Immediately remove internal Li-SOCl2 coin cell", "3. Separate relay terminal blocks (valuable silver contacts)", "4. Desolder optocoupler and processor boards", "5. Refine precious metal connectors"],
        "safety_warnings": ["⚠️ Li-SOCl2 backup batteries emit toxic SO2 gas if breached", "⚠️ Relay banks may switch 240V/415V - verify isolation", "⚠️ Harsh industrial chemical residues may coat chassis"],
        "recovery_value_usd": 18.50,
        "environmental_impact": {"co2_saved_kg": 25, "water_saved_liters": 900, "energy_saved_kwh": 65, "toxic_prevented_kg": 0.15},
        "repairability_score": 8, "repair_difficulty": "Specialized Industrial",
        "3d_shape": "desktop"
    },
    "Gaming Consoles & Controllers": {
        "category": "Gaming Consoles & Controllers", "icon": "🎮",
        "brands": ["Sony PlayStation", "Microsoft Xbox", "Nintendo Switch", "Valve Steam Deck"],
        "avg_weight_kg": 3.8, "avg_lifespan_years": 7,
        "components": [
            {"name": "High-Performance APU", "material": "Silicon die, Gold interconnects, Copper IHS", "weight_pct": 3, "hazardous": False, "recyclable": True, "value_usd": 6.00, "color": "#AB47BC"},
            {"name": "Vapor Chamber Heat Sink", "material": "Deoxidized high-purity Copper, Sintered wick", "weight_pct": 18, "hazardous": False, "recyclable": True, "value_usd": 5.00, "color": "#FFA726"},
            {"name": "Custom Motherboard", "material": "FR4 multi-layer, GDDR6 memory, Gold plating", "weight_pct": 12, "hazardous": True, "recyclable": True, "value_usd": 7.00, "color": "#66BB6A"},
            {"name": "High-Efficiency Internal PSU", "material": "Copper transformer, Capacitors, Steel shielding", "weight_pct": 14, "hazardous": True, "recyclable": True, "value_usd": 2.50, "color": "#FFEE58"},
            {"name": "Centrifugal Blower Fan", "material": "PBT plastic, Copper winding, Fluid bearings", "weight_pct": 6, "hazardous": False, "recyclable": True, "value_usd": 1.00, "color": "#69F0AE"},
            {"name": "Blu-ray / Optical Drive", "material": "Laser pickup (gallium nitride), Aluminum frame, PCB", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 2.00, "color": "#26C6DA"},
            {"name": "Outer Plastic Casing", "material": "Textured ABS/Polycarbonate", "weight_pct": 30, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#8D6E63"},
            {"name": "Liquid Metal / Thermal Phase Material", "material": "Gallium-Indium-Tin alloy (on newer PS5s)", "weight_pct": 1, "hazardous": True, "recyclable": False, "value_usd": 0.50, "color": "#78909C"}
        ],
        "precious_metals": {"Gold (mg)": 55, "Silver (mg)": 350, "Copper (g)": 280, "Palladium (mg)": 15},
        "hazardous_materials": ["Liquid metal thermal interface (corrosive to aluminum, conductive)", "Capacitor electrolyte", "Laser optical diode"],
        "recycling_steps": ["1. Securely wipe user profile and stored credentials", "2. Pop exterior clip-on plates", "3. Disassemble optical drive & internal PSU", "4. CAUTION: Isolate liquid metal thermal compound on APU without spilling onto contacts", "5. Recover copper vapor chamber"],
        "safety_warnings": ["⚠️ Liquid metal conducts electricity instantly - do NOT smear onto motherboard traces", "⚠️ Laser diodes in optical drive: do not power while disassembled", "⚠️ Internal PSU capacitors hold high DC charge"],
        "recovery_value_usd": 24.50,
        "environmental_impact": {"co2_saved_kg": 35, "water_saved_liters": 1400, "energy_saved_kwh": 90, "toxic_prevented_kg": 0.20},
        "repairability_score": 6, "repair_difficulty": "Medium",
        "3d_shape": "desktop"
    },
    "Medical & Diagnostic Electronics": {
        "category": "Medical & Diagnostic Electronics", "icon": "🏥",
        "brands": ["GE Healthcare", "Philips Medical", "Siemens Healthineers", "Mindray", "Omron Healthcare", "Medtronic"],
        "avg_weight_kg": 6.5, "avg_lifespan_years": 8,
        "components": [
            {"name": "Certified Isolation Power Supply", "material": "Double-insulated Copper transformers, Shielding", "weight_pct": 20, "hazardous": True, "recyclable": True, "value_usd": 6.00, "color": "#FFA726"},
            {"name": "Low-Noise Analog Frontend PCB", "material": "Gold contacts, High-precision Op-Amps, Multi-layer FR4", "weight_pct": 15, "hazardous": True, "recyclable": True, "value_usd": 12.00, "color": "#66BB6A"},
            {"name": "Display / Diagnostic Screen", "material": "Medical-grade LCD, Indium, Tempered glass", "weight_pct": 18, "hazardous": False, "recyclable": True, "value_usd": 4.00, "color": "#4FC3F7"},
            {"name": "Piezoelectric Transducer / Sensor Unit", "material": "Lead Zirconate Titanate (PZT), Gold electrodes", "weight_pct": 7, "hazardous": True, "recyclable": True, "value_usd": 5.00, "color": "#AB47BC"},
            {"name": "Aluminum Shielding Chassis", "material": "Cast aluminum alloy, RFI gaskets", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 4.50, "color": "#78909C"},
            {"name": "Antimicrobial Housing", "material": "Silicone, Treated polymers", "weight_pct": 15, "hazardous": False, "recyclable": False, "value_usd": 0.10, "color": "#8D6E63"}
        ],
        "precious_metals": {"Gold (mg)": 90, "Silver (mg)": 600, "Copper (g)": 180, "Platinum (mg)": 25},
        "hazardous_materials": ["Biohazard potential (clinical exposure)", "Lead Zirconate Titanate in ultrasound probes", "Lithium battery backups", "Beryllium copper RF springs"],
        "recycling_steps": ["1. MANDATORY: Verify certified bio-decontamination certificate before intake", "2. Check for radioactive tracer / sealed sources (if imaging device - do NOT accept if present)", "3. Remove backup batteries and hospital isolation transformers", "4. Recover gold-heavy analog measurement boards"],
        "safety_warnings": ["⛔ CRITICAL STOP-WORK: Never dismantle radioactive or bio-contaminated hardware", "⚠️ Piezoelectric crystals contain Lead Zirconate Titanate", "⚠️ Authorized medical refurbishment facility required for resale"],
        "recovery_value_usd": 32.00,
        "environmental_impact": {"co2_saved_kg": 45, "water_saved_liters": 1800, "energy_saved_kwh": 110, "toxic_prevented_kg": 0.35},
        "repairability_score": 4, "repair_difficulty": "Certified Biomedical Engineer Only",
        "3d_shape": "desktop"
    },
    "Monitors/Displays": {
        "category": "Monitors/Displays", "icon": "🖥️",
        "brands": ["Dell UltraSharp", "LG UltraGear", "Samsung Odyssey", "ASUS ROG", "BenQ", "Acer Predator"],
        "avg_weight_kg": 4.5, "avg_lifespan_years": 6,
        "components": [
            {"name": "LCD/OLED Panel", "material": "Polarizing glass, Liquid crystal, Indium Tin Oxide", "weight_pct": 35, "hazardous": False, "recyclable": True, "value_usd": 3.50, "color": "#4FC3F7"},
            {"name": "LED Backlight Assembly", "material": "Optical diffuser sheets, Light guide plate, PMMA", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 1.20, "color": "#FFEE58"},
            {"name": "Scaler / Controller Board", "material": "FR4 PCB, Video DSP, Gold-plated HDMI/DP ports", "weight_pct": 8, "hazardous": True, "recyclable": True, "value_usd": 2.80, "color": "#66BB6A"},
            {"name": "Power Supply Board (PSU)", "material": "Transformers, Electrolytic capacitors, Aluminum heatsink", "weight_pct": 12, "hazardous": True, "recyclable": True, "value_usd": 2.00, "color": "#FFA726"},
            {"name": "Heavy Metal Stand & Base", "material": "Cast aluminum, Cold-rolled steel, Counterweight", "weight_pct": 22, "hazardous": False, "recyclable": True, "value_usd": 1.80, "color": "#78909C"},
            {"name": "Outer Bezel & Enclosure", "material": "Textured ABS Plastic, Polycarbonate", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 0.30, "color": "#8D6E63"}
        ],
        "precious_metals": {"Gold (mg)": 25, "Silver (mg)": 180, "Copper (g)": 45, "Aluminum (g)": 350},
        "hazardous_materials": ["Capacitor high DC voltage charge", "Mercury in CCFL lamps (older models)", "Lead solder joints"],
        "recycling_steps": ["1. Disconnect AC power and video cables", "2. Unclip or unscrew VESA mount and stand", "3. Pry perimeter bezel clips to separate front frame", "4. CAUTION: Discharge high-voltage power board capacitors", "5. Disconnect LVDS ribbon cable from LCD", "6. Harvest optical diffuser sheets and backplate aluminum"],
        "safety_warnings": ["⚠️ Power supply capacitors hold up to 400V DC — discharge safely", "⚠️ Older CCFL screens contain TOXIC MERCURY vapor tubes", "⚠️ Do not shatter thin polarized glass"],
        "recovery_value_usd": 11.60,
        "environmental_impact": {"co2_saved_kg": 22, "water_saved_liters": 850, "energy_saved_kwh": 65, "toxic_prevented_kg": 0.08},
        "repairability_score": 6, "repair_difficulty": "Medium",
        "3d_shape": "display"
    },
    "Cables & Wires": {
        "category": "Cables & Wires", "icon": "🔌",
        "brands": ["Anker", "Belkin", "Syska", "Finolex", "Polycab", "AmazonBasics"],
        "avg_weight_kg": 0.25, "avg_lifespan_years": 4,
        "components": [
            {"name": "High-Purity Copper Conductors", "material": "Electrolytic Tough Pitch (ETP) Pure Copper", "weight_pct": 55, "hazardous": False, "recyclable": True, "value_usd": 2.20, "color": "#FFA726"},
            {"name": "Braided Metal Shielding", "material": "Tinned Copper / Aluminum wire mesh", "weight_pct": 12, "hazardous": False, "recyclable": True, "value_usd": 0.40, "color": "#78909C"},
            {"name": "PVC Insulation Jacket", "material": "Polyvinyl Chloride (PVC) with plasticizers", "weight_pct": 25, "hazardous": True, "recyclable": True, "value_usd": 0.15, "color": "#424242"},
            {"name": "Gold-Plated Connector Pins", "material": "18k/24k Gold plating over phosphor bronze", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 0.60, "color": "#FFD700"}
        ],
        "precious_metals": {"Copper (g)": 140, "Gold (mg)": 8, "Silver (mg)": 15},
        "hazardous_materials": ["Brominated flame retardants in PVC jacket", "Lead stabilizers in legacy wire insulation"],
        "recycling_steps": ["1. Sort cables by gauge and connector type", "2. Clip terminal connectors (USB/HDMI/RJ45) for pin harvesting", "3. Feed wire through mechanical wire stripper or granulator", "4. Separate granulated PVC from clean copper granules via water table"],
        "safety_warnings": ["⚠️ NEVER BURN CABLES TO STRIP PLASTIC — releases deadly dioxins & furans", "⚠️ Sharp cut strands can puncture skin — wear nitrile cut-gloves"],
        "recovery_value_usd": 3.35,
        "environmental_impact": {"co2_saved_kg": 4, "water_saved_liters": 150, "energy_saved_kwh": 12, "toxic_prevented_kg": 0.05},
        "repairability_score": 9, "repair_difficulty": "Very Easy",
        "3d_shape": "cable"
    },
    "Lighting Equipment": {
        "category": "Lighting Equipment", "icon": "💡",
        "brands": ["Philips Lighting", "Havells", "Osram", "Syska", "Crompton", "Wipro"],
        "avg_weight_kg": 0.15, "avg_lifespan_years": 3,
        "components": [
            {"name": "LED Emitter Array", "material": "Gallium Nitride (GaN) LEDs, Gold wire bonds", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#FFEE58"},
            {"name": "Aluminum Heat Sink Core", "material": "Extruded 6063 Aluminum Alloy", "weight_pct": 45, "hazardous": False, "recyclable": True, "value_usd": 0.40, "color": "#78909C"},
            {"name": "Internal Driver Circuit (SMPS)", "material": "Miniature FR4 PCB, Inductor, Electrolytic capacitor", "weight_pct": 18, "hazardous": True, "recyclable": True, "value_usd": 0.35, "color": "#66BB6A"},
            {"name": "Polycarbonate Diffuser Dome", "material": "Optical-grade Polycarbonate", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 0.05, "color": "#E0E0E0"},
            {"name": "Brass / Nickel Screw Base", "material": "Nickel-plated brass / Copper threaded base", "weight_pct": 14, "hazardous": False, "recyclable": True, "value_usd": 0.20, "color": "#FFA726"}
        ],
        "precious_metals": {"Aluminum (g)": 65, "Copper (g)": 15, "Gold (mg)": 2},
        "hazardous_materials": ["MERCURY VAPOR (in CFLs and Fluorescent tubes)", "Lead solder in older drivers"],
        "recycling_steps": ["1. Inspect bulb type: distinguish LED from toxic CFL tubes", "2. Pop off polycarbonate diffuser cap", "3. Unscrew LED emitter star board from heatsink", "4. Extract driver PCB from base tube", "5. Recycle clean aluminum heatsink"],
        "safety_warnings": ["⚠️ IF HANDLING CFL TUBES: MERCURY HAZARD — if broken, evacuate room for 15 mins", "⚠️ Do not crush tubes manually"],
        "recovery_value_usd": 1.50,
        "environmental_impact": {"co2_saved_kg": 3, "water_saved_liters": 90, "energy_saved_kwh": 8, "toxic_prevented_kg": 0.02},
        "repairability_score": 8, "repair_difficulty": "Easy",
        "3d_shape": "small_appliance"
    },
    "Audio/Video Equipment": {
        "category": "Audio/Video Equipment", "icon": "🔊",
        "brands": ["Sony", "Bose", "JBL / Harman", "Yamaha", "Sennheiser", "Pioneer"],
        "avg_weight_kg": 3.2, "avg_lifespan_years": 7,
        "components": [
            {"name": "Acoustic Speaker Drivers", "material": "Neodymium NdFeB Magnets, Pure Copper Voice Coil", "weight_pct": 32, "hazardous": False, "recyclable": True, "value_usd": 3.80, "color": "#FFA726"},
            {"name": "Audio Amplifier PCB", "material": "FR4 multi-layer, Power MOSFETs, Audio DAC chips", "weight_pct": 18, "hazardous": True, "recyclable": True, "value_usd": 3.20, "color": "#66BB6A"},
            {"name": "Toroidal Power Transformer", "material": "Grain-oriented silicon steel core, Heavy Copper winding", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 2.50, "color": "#FFEE58"},
            {"name": "Aluminum Heat Sink", "material": "Extruded Aluminum Fin Array", "weight_pct": 12, "hazardous": False, "recyclable": True, "value_usd": 1.00, "color": "#78909C"},
            {"name": "Enclosure & Grilles", "material": "MDF wood veneer / Perforated steel / ABS", "weight_pct": 13, "hazardous": False, "recyclable": True, "value_usd": 0.40, "color": "#8D6E63"}
        ],
        "precious_metals": {"Copper (g)": 220, "Neodymium (g)": 35, "Gold (mg)": 15, "Silver (mg)": 80},
        "hazardous_materials": ["High-capacity electrolytic capacitors", "Lead solder traces"],
        "recycling_steps": ["1. Remove exterior acoustic grille and faceplate", "2. Unscrew speaker drivers from baffle board", "3. Extract rare-earth neodymium magnets from voice coils", "4. Remove amplifier power board and transformer", "5. Recover high-grade heavy copper windings"],
        "safety_warnings": ["⚠️ Large audio filter capacitors retain dangerous voltage", "⚠️ Powerful neodymium magnets can pinch fingers severely"],
        "recovery_value_usd": 10.90,
        "environmental_impact": {"co2_saved_kg": 18, "water_saved_liters": 720, "energy_saved_kwh": 55, "toxic_prevented_kg": 0.06},
        "repairability_score": 7, "repair_difficulty": "Medium",
        "3d_shape": "desktop"
    },
    "Networking Equipment": {
        "category": "Networking Equipment", "icon": "📡",
        "brands": ["Cisco", "TP-Link", "Netgear", "D-Link", "Ubiquiti UniFi", "MikroTik", "Huawei"],
        "avg_weight_kg": 0.85, "avg_lifespan_years": 5,
        "components": [
            {"name": "Networking Switch / SoC Motherboard", "material": "FR4 PCB, Gigabit Switch ASIC, Gold PCIe pins", "weight_pct": 35, "hazardous": True, "recyclable": True, "value_usd": 4.50, "color": "#66BB6A"},
            {"name": "Adjustable Dipole Wi-Fi Antennas", "material": "Copper internal wire, Gold U.FL micro-coax, ABS sheath", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 1.20, "color": "#FFA726"},
            {"name": "Aluminum SoC Heat Sink", "material": "Extruded anodized aluminum", "weight_pct": 18, "hazardous": False, "recyclable": True, "value_usd": 0.80, "color": "#78909C"},
            {"name": "Shielded RJ45 Ethernet Ports", "material": "Gold-plated phosphor bronze pins, Stainless steel shield", "weight_pct": 12, "hazardous": False, "recyclable": True, "value_usd": 0.90, "color": "#FFEE58"},
            {"name": "Ventilated Outer Enclosure", "material": "Flame-retardant ABS / Polycarbonate", "weight_pct": 20, "hazardous": False, "recyclable": True, "value_usd": 0.20, "color": "#424242"}
        ],
        "precious_metals": {"Gold (mg)": 28, "Silver (mg)": 120, "Copper (g)": 65},
        "hazardous_materials": ["Brominated Flame Retardants (BFRs)", "Lead solder in legacy routers"],
        "recycling_steps": ["1. Perform hardware factory reset button hold (wipe credentials)", "2. Unclip rubber feet to reveal hidden assembly screws", "3. Separate upper and lower shell casings", "4. Detach U.FL antenna coax connectors from motherboard", "5. Unscrew mainboard and recover gold-bearing network ASIC and RJ45 jacks"],
        "safety_warnings": ["⚠️ WIPE CONFIGURATION: routers store Wi-Fi passwords and IP logs", "⚠️ Use ESD protection when handling flash memory"],
        "recovery_value_usd": 7.60,
        "environmental_impact": {"co2_saved_kg": 12, "water_saved_liters": 450, "energy_saved_kwh": 35, "toxic_prevented_kg": 0.04},
        "repairability_score": 7, "repair_difficulty": "Medium-Easy",
        "3d_shape": "networking"
    }
}

# ═══ 3D SHAPE DEFINITIONS (Three.js parametric) ═══
THREE_JS_SHAPES = {
    "phone": {"width":0.7, "height":1.4, "depth":0.08, "corner":0.05},
    "laptop": {"width":2.5, "height":0.15, "depth":1.7, "corner":0.02},
    "tablet": {"width":1.2, "height":1.8, "depth":0.06, "corner":0.04},
    "desktop": {"width":1.8, "height":4.0, "depth":4.5, "corner":0.02},
    "tv": {"width":5.0, "height":3.0, "depth":0.3, "corner":0.02},
    "battery": {"width":0.5, "height":0.2, "depth":1.0, "corner":0.02},
    "pcb": {"width":2.5, "height":0.05, "depth":2.0, "corner":0.01},
    "printer": {"width":3.5, "height":1.5, "depth":3.0, "corner":0.03},
    "appliance": {"width":3.0, "height":5.0, "depth":3.0, "corner":0.05},
    "small_appliance": {"width":1.5, "height":2.0, "depth":1.5, "corner":0.03},
}

def init_knowledge_db():
    """Initialize the knowledge database"""
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS device_knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT UNIQUE, category TEXT, brand TEXT,
            data_json TEXT, source TEXT, verified INTEGER DEFAULT 0,
            created_at TEXT, updated_at TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS search_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_hash TEXT UNIQUE, query TEXT,
            result_json TEXT, created_at TEXT
        )''')
        conn.commit(); conn.close()
    except: pass

def save_device_knowledge(name, category, brand, data, source="AI Generated", verified=False):
    """Save device knowledge to database"""
    try:
        init_knowledge_db()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        now = datetime.now().isoformat()
        c.execute('''INSERT OR REPLACE INTO device_knowledge 
            (device_name, category, brand, data_json, source, verified, created_at, updated_at) 
            VALUES (?,?,?,?,?,?,?,?)''', (name, category, brand, json.dumps(data), source, 1 if verified else 0, now, now))
        conn.commit(); conn.close()
        return True
    except: return False

def get_device_knowledge(name):
    """Retrieve device knowledge from database"""
    try:
        init_knowledge_db()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT data_json, source, verified FROM device_knowledge WHERE device_name=?', (name,))
        row = c.fetchone(); conn.close()
        if row: return json.loads(row[0]), row[1], bool(row[2])
    except: pass
    return None, None, False

def search_knowledge(query):
    """Search knowledge database"""
    try:
        init_knowledge_db()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT device_name, category, brand FROM device_knowledge WHERE device_name LIKE ? OR category LIKE ?', (f'%{query}%', f'%{query}%'))
        rows = c.fetchall(); conn.close()
        return rows
    except: return []

def get_knowledge_stats():
    """Get database statistics"""
    try:
        init_knowledge_db()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM device_knowledge'); total = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM device_knowledge WHERE verified=1'); verified = c.fetchone()[0]
        c.execute('SELECT COUNT(DISTINCT category) FROM device_knowledge'); categories = c.fetchone()[0]
        conn.close()
        return {'total': total, 'verified': verified, 'categories': categories}
    except: return {'total': 0, 'verified': 0, 'categories': 0}

def get_device_info(category):
    """Get device info from built-in knowledge base"""
    if category in DEVICE_KNOWLEDGE:
        return DEVICE_KNOWLEDGE[category]
    for k,v in DEVICE_KNOWLEDGE.items():
        if category.lower() in k.lower():
            return v
    return None
