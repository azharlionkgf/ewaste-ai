# Hologram 3D Engine Builder for three_d_viewer.py
import os

target_path = r"C:\Users\HP\.gemini\antigravity\scratch\e_waste_project\app\three_d_viewer.py"

py_script = r'''"""
✨ Futuristic Hologram Hardware Anatomy & 3D Disassembly Engine
================================================================
Photorealistic 3D hardware breakdown with Hologram Sci-Fi Mode:
- Holographic cyan/gold particle aura and rotating concentric cyber-rings
- Vertical scanning laser beam sweeping up and down the device
- 360° continuous auto-spin with full OrbitControls touch/mouse rotation
- Interactive peeling slider from 0% (solid intact device) to 100% (exploded holographic teardown)
- 16 precision micro-screws, 200MP triple camera halo, 5000mAh battery, Dimensity SoC, and AMOLED display
"""

import os
import json
from typing import Dict, Any, Optional

def generate_3d_viewer(device_info: Dict[str, Any], height: int = 740) -> str:
    """
    Generate a futuristic Hologram 3D hardware anatomy viewer with scanning laser,
    glowing cyber pedestal, particle aura, 360° auto-spin, and disassembly slider.
    """
    brand = device_info.get("brand", "Electronic Device")
    model_name = device_info.get("model", device_info.get("category", "Device Model"))
    category = device_info.get("category", "Mobile Phones")
    storage = device_info.get("storage", "256 GB UFS Flash")
    ram = device_info.get("ram", "12 GB RAM")
    processor = device_info.get("processor", "High-Performance SoC")
    camera_specs = device_info.get("camera", "High-Resolution Sensor Array")
    battery_specs = device_info.get("battery", "Li-ion High-Capacity Pack")
    
    chassis_color = device_info.get("chassis_color", "#E6D7C3")
    accent_color = device_info.get("accent_color", "#FFD700")
    frame_color = device_info.get("frame_color", "#D4AF37")
    screen_color = device_info.get("screen_color", "#080E1A")
    
    cat_lower = str(category).lower()
    if "laptop" in cat_lower: shape_type = "laptop"
    elif "desktop" in cat_lower or "computer" in cat_lower: shape_type = "desktop"
    elif "tablet" in cat_lower or "ipad" in cat_lower: shape_type = "tablet"
    elif "monitor" in cat_lower or "television" in cat_lower or "display" in cat_lower or "tv" in cat_lower: shape_type = "display"
    elif "batter" in cat_lower: shape_type = "battery"
    elif "pcb" in cat_lower or "circuit" in cat_lower or "board" in cat_lower: shape_type = "pcb"
    else: shape_type = "phone"

    teardown_manuals = {
        "phone": [
            {"step": 1, "title": "1. Unscrew 16 Holographic Screws", "tool": "Phillips #00 (1.4mm) Screwdriver", "action": "Extract 16 structural screws securing chassis and back shield.", "safety": "⚠️ Keep screws organized on magnetic pad by thread size.", "slider_pct": 12},
            {"step": 2, "title": "2. Heat & Lift Vegan Leather Rear Cover", "tool": "Heat Mat (78°C) • Suction Cup", "action": "Heat perimeter adhesive 180s; pry gently with nylon pick.", "safety": "⚠️ Do not heat past 85°C to avoid battery degradation.", "slider_pct": 28},
            {"step": 3, "title": "3. Unclip 200MP Camera Module & NFC", "tool": "ESD Plastic Spudger", "action": "Disconnect camera FPC flex ribbon and lift out halo camera island.", "safety": "⚠️ Do not touch optical lenses with bare fingers.", "slider_pct": 44},
            {"step": 4, "title": "4. Separate Structural Magnesium Midframe", "tool": "Precision Tweezers • Spatula", "action": "Unclip side frame rails; isolate USB-C and speaker modules.", "safety": "🧤 Aluminum/magnesium midframe is 100% recyclable.", "slider_pct": 60},
            {"step": 5, "title": "5. ⚡ Pull Battery Stretch Tabs A & B", "tool": "Stretch Release Adhesive Strips", "action": "Pull stretch tabs horizontally at 15° to cleanly release 5000mAh cell.", "safety": "🔥 NEVER BEND OR PUNCTURE LI-ION CELLS.", "slider_pct": 76},
            {"step": 6, "title": "6. Lift 10-Layer Logic Board & Heatpipe", "tool": "Torx T2 • Grounded ESD Strap", "action": "Disconnect RF coaxial cables; lift motherboard with Dimensity SoC.", "safety": "🟢 Pure gold micro-contacts recovered for refining.", "slider_pct": 90},
            {"step": 7, "title": "7. Harvest 120Hz Curved AMOLED Screen", "tool": "Curved Heated Glass Separator", "action": "Separate AMOLED panel and Gorilla Glass Victus front assembly.", "safety": "🧤 Wear safety glasses for fragile display glass.", "slider_pct": 100}
        ],
        "default": [
            {"step": 1, "title": "1. Safety Isolation & Disconnect", "tool": "ESD Kit • Multimeter", "action": "Verify zero residual electrical charge.", "safety": "⚠️ Verify zero voltage before proceeding.", "slider_pct": 20},
            {"step": 2, "title": "2. Remove Outer Housing Fasteners", "tool": "Precision Screwdriver Set", "action": "Extract fasteners and unclip perimeter casing.", "safety": "⚠️ Sort screws by size.", "slider_pct": 40},
            {"step": 3, "title": "3. Isolate Power & Battery Modules", "tool": "Non-Conductive Spudger", "action": "Disconnect power supply or battery pack first.", "safety": "🔥 Prevent sparks and short circuits.", "slider_pct": 60},
            {"step": 4, "title": "4. Extract Electronic Logic PCBs", "tool": "ESD Tweezers • Spatula", "action": "Harvest high-grade printed circuit boards.", "safety": "🟢 High recovery value: Gold, Silver, Copper.", "slider_pct": 80},
            {"step": 5, "title": "5. Material Segregation & Storage", "tool": "Sorting Bins • Cut Gloves", "action": "Segregate metals and hazardous substances.", "safety": "♻️ Deliver to CPCB/R2 certified facilities.", "slider_pct": 100}
        ]
    }

    manual_steps = teardown_manuals.get(shape_type, teardown_manuals["default"])
    manual_steps_json = json.dumps(manual_steps)

    components = [
        {"id": "c1", "num": 1, "name": "Back Cover", "sub": "Plastic / Glass Finish", "material": "Lychee Vegan Leather / Gorilla Glass", "specs": "Sunrise Beige PBR Cover with Halo Camera Island", "weight_pct": 11.5, "hazardous": False, "recyclable": True, "value_usd": 2.50, "color": "#E6D7C3"},
        {"id": "c2", "num": 2, "name": "Camera Module", "sub": "Multiple Lenses + Flash", "material": "Optical Glass + CNC Gold Bezel + CMOS", "specs": "200MP OIS Main + 8MP Ultra-Wide + 2MP Macro", "weight_pct": 5.2, "hazardous": False, "recyclable": True, "value_usd": 7.80, "color": "#D4AF37"},
        {"id": "c3", "num": 3, "name": "Frame / Middle Chassis", "sub": "Metal / Plastic", "material": "Anodized 6000-series Aluminum Alloy", "specs": "Unibody Structural Midframe with Button Rails", "weight_pct": 14.8, "hazardous": False, "recyclable": True, "value_usd": 3.20, "color": "#BDC3C7"},
        {"id": "c4", "num": 4, "name": "Battery", "sub": "Li-ion Polymer Battery", "material": "Lithium Cobalt Oxide + Copper Foil", "specs": "5000mAh 19.25Wh 3.85V Pouch Cell (Tabs A&B)", "weight_pct": 23.4, "hazardous": True, "recyclable": True, "value_usd": 4.80, "color": "#C0392B"},
        {"id": "c5", "num": 5, "name": "Mainboard (PCB)", "sub": "Processor + Memory + ICs", "material": "10-Layer High-Tg FR4 + 18k Gold Plating", "specs": "Dimensity 7050 5G SoC + 256GB UFS + PMIC", "weight_pct": 16.5, "hazardous": True, "recyclable": True, "value_usd": 15.50, "color": "#1B4332"},
        {"id": "c6", "num": 6, "name": "Display Assembly", "sub": "AMOLED / LCD with Touch", "material": "Flexible OLED Substrate + Polarizer", "specs": "6.7\" 120Hz Curved AMOLED 2412x1080 Panel", "weight_pct": 9.8, "hazardous": False, "recyclable": True, "value_usd": 9.00, "color": "#2980B9"},
        {"id": "c7", "num": 7, "name": "Front Frame", "sub": "Plastic / Metal", "material": "Die-Cast Polycarbonate & Magnesium Alloy", "specs": "Precision Bezel Support Frame & Gasket", "weight_pct": 5.0, "hazardous": False, "recyclable": True, "value_usd": 1.20, "color": "#7F8C8D"},
        {"id": "c8", "num": 8, "name": "Front Screen (Display)", "sub": "Gorilla Glass Cover", "material": "Corning Gorilla Glass Victus", "specs": "Double-Reinforced Curved Scratch-Resistant Glass", "weight_pct": 6.8, "hazardous": False, "recyclable": True, "value_usd": 4.50, "color": "#34495E"},
        {"id": "c9", "num": 9, "name": "SIM Tray", "sub": "Metal", "material": "Die-Cast Zinc Alloy + Rubber Gasket", "specs": "Dual Nano-SIM Slot with Ejector Pin Hole", "weight_pct": 0.4, "hazardous": False, "recyclable": True, "value_usd": 0.30, "color": "#F1C40F"},
        {"id": "c10", "num": 10, "name": "Side Buttons", "sub": "Power / Volume", "material": "Anodized Aluminum Alloy", "specs": "Milled Tactile Volume & Power Rocker Switches", "weight_pct": 0.3, "hazardous": False, "recyclable": True, "value_usd": 0.20, "color": "#D4AF37"},
        {"id": "c11", "num": 11, "name": "Speaker", "sub": "Top / Bottom Speaker", "material": "Neodymium Magnet + Copper Voice Coil", "specs": "Dual Stereo Acoustic Chamber Speakers", "weight_pct": 1.6, "hazardous": False, "recyclable": True, "value_usd": 0.80, "color": "#34495E"},
        {"id": "c12", "num": 12, "name": "Vibration Motor", "sub": "Haptic Feedback", "material": "Rare-Earth Neodymium + Copper Windings", "specs": "X-axis Linear Resonant Actuator (LRA)", "weight_pct": 0.9, "hazardous": False, "recyclable": True, "value_usd": 0.60, "color": "#7F8C8D"},
        {"id": "c13", "num": 13, "name": "Charging Port", "sub": "USB Type-C", "material": "Stainless Steel Shell + Gold Pins", "specs": "24-Pin Reversible 67W SuperVOOC Daughterboard", "weight_pct": 1.1, "hazardous": False, "recyclable": True, "value_usd": 0.90, "color": "#D35400"},
        {"id": "c14", "num": 14, "name": "Antenna Modules", "sub": "5G / Wi-Fi / Bluetooth", "material": "Polyimide Copper Flex Strips", "specs": "Sub-6GHz 5G & Dual-Band Wi-Fi 6 MIMO Antennas", "weight_pct": 0.7, "hazardous": False, "recyclable": True, "value_usd": 0.70, "color": "#27AE60"},
        {"id": "c15", "num": 15, "name": "Flex Cables", "sub": "Connectors / Ribbon Cables", "material": "Polyimide + Pure Gold Micro-Contacts", "specs": "Main Display, Sub-board & Battery BMU Ribbons", "weight_pct": 0.8, "hazardous": False, "recyclable": True, "value_usd": 1.10, "color": "#E67E22"},
        {"id": "c16", "num": 16, "name": "Screws & Small Parts", "sub": "16x Micro-Screws & Brackets", "material": "Tempered Steel & Beryllium Copper Clips", "specs": "16x Phillips #00 Screws + Grounding Brackets", "weight_pct": 1.0, "hazardous": False, "recyclable": True, "value_usd": 0.40, "color": "#BDC3C7"}
    ]

    comp_data = []
    for i, c in enumerate(components):
        comp_data.append({
            "id": c.get("id", f"comp_{i+1}"),
            "num": c.get("num", i + 1),
            "name": c.get("name", f"Component {i+1}"),
            "sub": c.get("sub", "Sub-Assembly"),
            "material": c.get("material", "Industrial Composite"),
            "specs": c.get("specs", "Standard Spec"),
            "weight_pct": float(c.get("weight_pct", 10.0)),
            "hazardous": bool(c.get("hazardous", False)),
            "recyclable": bool(c.get("recyclable", True)),
            "value_usd": float(c.get("value_usd", 2.00)),
            "color": c.get("color", "#7F8C8D")
        })

    comp_json = json.dumps(comp_data)
    total_val = sum(c["value_usd"] for c in comp_data)
    total_parts = len(comp_data)
    haz_count = sum(1 for c in comp_data if c["hazardous"])
    rec_count = sum(1 for c in comp_data if c["recyclable"])

    grid_cards_html = ""
    for p in comp_data:
        haz_tag = '<span class="status-tag haz">⚠️ HAZARD</span>' if p["hazardous"] else '<span class="status-tag safe">♻️ SAFE</span>'
        grid_cards_html += f"""
        <div class="comp-tile" id="tile-{p['id']}" onclick="inspectPart('{p['id']}')">
            <div class="comp-tile-top">
                <div class="tile-num">{p['num']}</div>
                <div class="tile-titles">
                    <div class="tile-name">{p['name']}</div>
                    <div class="tile-sub">({p['sub']})</div>
                </div>
            </div>
            <div class="comp-tile-preview" style="background:linear-gradient(135deg, {p['color']}22, {p['color']}55);border-color:{p['color']}66;">
                <div class="preview-icon">{"⚠️" if p['hazardous'] else "🔩"}</div>
                <div class="preview-material">{p['material']}</div>
            </div>
            <div class="comp-tile-bottom">
                <div class="tile-spec-line">⚙️ {p['specs']}</div>
                <div class="tile-metrics">
                    <span class="metric-val">💰 ${p['value_usd']:.2f}</span>
                    <span class="metric-pct">⚖️ {p['weight_pct']}%</span>
                    {haz_tag}
                </div>
            </div>
        </div>
        """

    steps_html = ""
    for s in manual_steps:
        steps_html += f"""
        <div class="step-card" onclick="setSliderPercent({s.get('slider_pct', 50)})">
            <div class="step-header">
                <span class="step-title">{s['title']}</span>
                <span class="step-tool">🧰 {s['tool']}</span>
            </div>
            <div class="step-action">{s['action']}</div>
            <div class="step-safety">{s['safety']}</div>
            <div class="step-btn-cue">👆 Click to view in Hologram 3D (Slider -> {s.get('slider_pct', 50)}%)</div>
        </div>
        """
'''

html_block = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>E-Waste AI - Hologram Hardware Anatomy & 3D Teardown</title>
<!-- Powered by Three.js 3D WebGL Engine -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
    background: #04060A;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #E2E8F0;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 10px;
    user-select: none;
}
.container {
    max-width: 1400px;
    margin: 0 auto;
}

/* Futuristic Hologram Header */
.header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(90deg, rgba(10,25,45,0.95), rgba(6,12,22,0.95));
    border: 1px solid #00F0FF;
    border-radius: 12px;
    padding: 10px 18px;
    margin-bottom: 10px;
    box-shadow: 0 0 25px rgba(0,240,255,0.25);
}
.header-left { display: flex; align-items: center; gap: 12px; }
.brand-pill {
    background: linear-gradient(135deg, #00F0FF, #00A3FF);
    color: #04060A;
    font-weight: 800;
    font-size: 11px;
    letter-spacing: 1.5px;
    padding: 4px 10px;
    border-radius: 6px;
    text-transform: uppercase;
    box-shadow: 0 0 10px rgba(0,240,255,0.5);
}
.main-title { font-size: 15px; font-weight: 700; color: #F8FAFC; letter-spacing: 0.5px; }
.sub-title { font-size: 11px; color: #38BDF8; }
.header-badges { display: flex; gap: 8px; }
.cert-badge {
    background: rgba(0,240,255,0.08);
    border: 1px solid rgba(0,240,255,0.4);
    color: #38BDF8;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 16px;
    box-shadow: 0 0 8px rgba(0,240,255,0.2);
}
.cert-badge.green { border-color: #00FF7F; color: #00FF7F; background: rgba(0,255,127,0.1); }
.cert-badge.gold { border-color: #FFD700; color: #FFD700; background: rgba(255,215,0,0.1); }

/* Hologram 3D Stage */
.stage-card {
    background: radial-gradient(circle at 50% 40%, #0B192E 0%, #04060A 85%);
    border: 1px solid rgba(0,240,255,0.35);
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 12px;
    position: relative;
    box-shadow: 0 0 35px rgba(0,240,255,0.2);
}
.controls-deck {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    background: rgba(8,16,30,0.92);
    border: 1px solid rgba(0,240,255,0.25);
    backdrop-filter: blur(10px);
    border-radius: 10px;
    padding: 10px 16px;
    margin-bottom: 10px;
    flex-wrap: wrap;
}
.slider-container {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 1;
    min-width: 290px;
}
.slider-lbl {
    font-size: 11px;
    font-weight: 800;
    color: #38BDF8;
    white-space: nowrap;
    letter-spacing: 0.5px;
}
.explode-slider {
    flex: 1;
    -webkit-appearance: none;
    height: 8px;
    border-radius: 5px;
    background: linear-gradient(90deg, #00FF7F 0%, #00F0FF 50%, #FF0055 100%);
    outline: none;
    cursor: pointer;
    box-shadow: 0 0 10px rgba(0,240,255,0.4);
}
.explode-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #FFFFFF;
    border: 3px solid #00F0FF;
    cursor: pointer;
    box-shadow: 0 0 16px rgba(0,240,255,0.9);
}
.btn-action {
    background: rgba(0,240,255,0.12);
    border: 1px solid #00F0FF;
    color: #00F0FF;
    font-weight: 700;
    font-size: 11px;
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
}
.btn-action:hover {
    background: #00F0FF;
    color: #04060A;
    box-shadow: 0 0 16px rgba(0,240,255,0.7);
}
.quick-steps-row {
    display: flex;
    gap: 6px;
    overflow-x: auto;
    padding-bottom: 4px;
}
.step-chip {
    background: rgba(0,240,255,0.06);
    border: 1px solid rgba(0,240,255,0.2);
    color: #BAE6FD;
    font-size: 9.5px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 12px;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.2s;
}
.step-chip:hover, .step-chip.active {
    border-color: #00F0FF;
    color: #00F0FF;
    background: rgba(0,240,255,0.18);
    box-shadow: 0 0 10px rgba(0,240,255,0.4);
}

/* 3D Canvas Box */
#canvas-3d-container {
    width: 100%;
    height: 520px;
    border-radius: 10px;
    overflow: hidden;
    position: relative;
    background: transparent;
    touch-action: none;
}
#canvas-3d-container canvas {
    display: block;
    width: 100%;
    height: 100%;
    cursor: grab;
    touch-action: none;
}
#canvas-3d-container canvas:active { cursor: grabbing; }

/* Hologram Overlay Elements */
.overlay-hint {
    position: absolute;
    bottom: 12px;
    left: 14px;
    font-size: 10.5px;
    font-weight: 600;
    color: #38BDF8;
    background: rgba(6,12,22,0.85);
    border: 1px solid rgba(0,240,255,0.3);
    padding: 4px 12px;
    border-radius: 6px;
    pointer-events: none;
    box-shadow: 0 0 12px rgba(0,240,255,0.2);
}
.overlay-slider-val {
    position: absolute;
    top: 12px;
    right: 14px;
    font-size: 13px;
    font-weight: 800;
    color: #00F0FF;
    background: rgba(6,12,22,0.9);
    border: 1px solid #00F0FF;
    padding: 5px 12px;
    border-radius: 8px;
    box-shadow: 0 0 16px rgba(0,240,255,0.4);
    pointer-events: none;
}
.hologram-scan-grid {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(rgba(0,240,255,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,240,255,0.03) 1px, transparent 1px);
    background-size: 32px 32px;
}

/* Inspector HUD */
.inspector-card {
    background: linear-gradient(135deg, rgba(10,25,45,0.95), rgba(6,14,26,0.95));
    border: 1px solid #00F0FF;
    border-radius: 12px;
    padding: 12px 18px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 0 20px rgba(0,240,255,0.25);
}
.inspector-icon {
    width: 52px;
    height: 52px;
    border-radius: 10px;
    background: rgba(0,240,255,0.12);
    border: 1px solid rgba(0,240,255,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    box-shadow: 0 0 12px rgba(0,240,255,0.3);
}
.inspector-details { flex: 1; }
.inspector-title { font-size: 14px; font-weight: 700; color: #00F0FF; letter-spacing: 0.5px; }
.inspector-sub { font-size: 11px; color: #BAE6FD; margin-top: 2px; }
.inspector-specs { font-size: 9.5px; color: #94A3B8; margin-top: 2px; }
.inspector-stats { display: flex; gap: 14px; margin-top: 6px; font-size: 10.5px; font-weight: 700; }
.stat-item.gold { color: #FFD700; }
.stat-item.green { color: #00FF7F; }
.stat-item.cyan { color: #00F0FF; }

/* 15-Part Grid */
.section-title {
    font-size: 12.5px;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.parts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 8px;
    margin-bottom: 12px;
}
.comp-tile {
    background: rgba(10, 20, 35, 0.88);
    border: 1px solid rgba(0, 240, 255, 0.15);
    border-radius: 8px;
    padding: 8px 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.comp-tile:hover {
    border-color: #00F0FF;
    transform: translateY(-2px);
    box-shadow: 0 0 16px rgba(0, 240, 255, 0.3);
}
.comp-tile.active {
    border-color: #00F0FF;
    background: rgba(0, 240, 255, 0.08);
    box-shadow: 0 0 18px rgba(0, 240, 255, 0.4);
}
.comp-tile-top { display: flex; align-items: flex-start; gap: 6px; margin-bottom: 6px; }
.tile-num {
    background: rgba(0,240,255,0.15);
    color: #00F0FF;
    font-weight: 800;
    font-size: 9.5px;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border: 1px solid rgba(0,240,255,0.3);
}
.tile-titles { flex: 1; min-width: 0; }
.tile-name { font-size: 10.5px; font-weight: 700; color: #F1F5F9; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tile-sub { font-size: 8px; color: #94A3B8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.comp-tile-preview {
    height: 44px;
    border-radius: 5px;
    border: 1px solid;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 4px;
    margin-bottom: 6px;
}
.preview-icon { font-size: 16px; }
.preview-material { font-size: 8px; color: #E2E8F0; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
.tile-spec-line { font-size: 7.5px; color: #64748B; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tile-metrics { display: flex; align-items: center; justify-content: space-between; font-size: 8.5px; padding-top: 3px; border-top: 1px solid rgba(255,255,255,0.05); }
.metric-val { font-weight: 700; color: #00F0FF; }
.metric-pct { color: #94A3B8; }
.status-tag { font-size: 7px; font-weight: 700; padding: 1px 4px; border-radius: 3px; }
.status-tag.haz { background: rgba(255,0,85,0.18); color: #FF0055; border: 1px solid rgba(255,0,85,0.4); }
.status-tag.safe { background: rgba(0,255,127,0.12); color: #00FF7F; border: 1px solid rgba(0,255,127,0.3); }

/* Lower Deck */
.lower-deck {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 12px;
}
.deck-panel {
    background: rgba(10, 20, 35, 0.9);
    border: 1px solid rgba(0, 240, 255, 0.15);
    border-radius: 10px;
    padding: 12px;
}
.views-row {
    display: flex;
    gap: 6px;
    overflow-x: auto;
    padding-bottom: 6px;
    margin-bottom: 10px;
}
.view-tile {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(0,240,255,0.12);
    border-radius: 6px;
    padding: 6px 10px;
    text-align: center;
    min-width: 75px;
    flex: 1;
    cursor: pointer;
    transition: all 0.2s;
}
.view-tile:hover {
    border-color: #00F0FF;
    background: rgba(0,240,255,0.1);
    box-shadow: 0 0 10px rgba(0,240,255,0.3);
}
.view-tile-icon { font-size: 16px; }
.view-tile-lbl { font-size: 8.5px; color: #38BDF8; margin-top: 2px; font-weight: 600; }
.specs-list { font-size: 9.5px; color: #CBD5E1; line-height: 1.8; }
.specs-list strong { color: #00F0FF; }

.steps-scroll { max-height: 240px; overflow-y: auto; padding-right: 4px; }
.step-card {
    background: rgba(0,0,0,0.3);
    border-left: 3px solid #00F0FF;
    border-radius: 4px;
    padding: 8px 10px;
    margin-bottom: 6px;
    cursor: pointer;
    transition: all 0.2s;
}
.step-card:hover {
    background: rgba(0,240,255,0.08);
    border-left-color: #00FF7F;
}
.step-header { display: flex; justify-content: space-between; align-items: center; font-size: 9.5px; font-weight: 700; margin-bottom: 2px; }
.step-title { color: #F1F5F9; }
.step-tool { color: #00FF7F; font-size: 8.5px; }
.step-action { font-size: 8.5px; color: #94A3B8; }
.step-safety { font-size: 8px; color: #FF6347; margin-top: 2px; }
.step-btn-cue { font-size: 8px; color: #00F0FF; margin-top: 3px; font-weight: 600; }

.footer-banner {
    text-align: center;
    padding: 8px;
    border-top: 1px solid rgba(0,240,255,0.15);
    font-size: 9.5px;
    color: #64748B;
}
.footer-banner strong { color: #00F0FF; }
</style>
</head>
<body>
<div class="container">

    <!-- TOP BANNER -->
    <div class="header-bar">
        <div class="header-left">
            <span class="brand-pill">⚡ __BRAND_UPPER__</span>
            <div>
                <div class="main-title">__BRAND__ __MODEL__ — Hologram Hardware Disassembly 3D</div>
                <div class="sub-title">Astra-Style Holographic Anatomy • Sweeping Laser Scan • Real Rotatable 3D Components</div>
            </div>
        </div>
        <div class="header-badges">
            <span class="cert-badge cyan">✨ Hologram Grid</span>
            <span class="cert-badge green">✔ Real Parts</span>
            <span class="cert-badge gold">✔ Educational Use</span>
        </div>
    </div>

    <!-- 3D HOLOGRAM DISASSEMBLY STAGE -->
    <div class="stage-card">
        <div class="controls-deck">
            <div class="slider-container">
                <span class="slider-lbl">🔒 ASSEMBLED (0%)</span>
                <input type="range" id="explodeSlider" class="explode-slider" min="0" max="100" value="55" oninput="onSliderChange(this.value)">
                <span class="slider-lbl">💥 HOLOGRAM EXPLODED (100%)</span>
            </div>
            <button id="btnAutoSpin" class="btn-action" onclick="toggleAutoSpin()">🔄 360° Spin: ON</button>
            <button id="btnLaser" class="btn-action" onclick="toggleLaser()">⚡ Scan Laser: ON</button>
            <button id="btnAutoPlay" class="btn-action" onclick="toggleAutoPlay()">▶ Auto-Teardown</button>
            <button class="btn-action" onclick="reset3DCamera()">🎯 Center View</button>
        </div>

        <div class="quick-steps-row">
            <span class="step-chip" onclick="setSliderPercent(0)">🔒 Solid Device (0%)</span>
            <span class="step-chip" onclick="setSliderPercent(12)">Step 1: 16 Screws Unscrew</span>
            <span class="step-chip" onclick="setSliderPercent(28)">Step 2: Vegan Leather Cover</span>
            <span class="step-chip" onclick="setSliderPercent(44)">Step 3: 200MP Triple Camera Halo</span>
            <span class="step-chip" onclick="setSliderPercent(60)">Step 4: Aluminum Midframe & USB-C</span>
            <span class="step-chip" onclick="setSliderPercent(76)">Step 5: 5000mAh Battery & Pull Tabs ⚡</span>
            <span class="step-chip" onclick="setSliderPercent(90)">Step 6: 10-Layer Logic Board & SoC</span>
            <span class="step-chip" onclick="setSliderPercent(100)">Step 7: Curved AMOLED Display</span>
        </div>

        <!-- 3D Canvas Box -->
        <div id="canvas-3d-container">
            <div class="hologram-scan-grid"></div>
            <div class="overlay-hint">🔄 Drag / Swipe with finger to Rotate 360° • Pinch / Scroll to Zoom • Watch Scanning Laser</div>
            <div id="sliderBadge" class="overlay-slider-val">Disassembly: 55%</div>
        </div>
    </div>

    <!-- INSPECTOR HUD -->
    <div id="inspector-hud" class="inspector-card">
        <div id="insp-icon" class="inspector-icon">📱</div>
        <div class="inspector-details">
            <div id="insp-title" class="inspector-title">1. Back Cover (Plastic / Glass Finish)</div>
            <div id="insp-sub" class="inspector-sub">Material: Lychee Vegan Leather / Gorilla Glass</div>
            <div id="insp-specs" class="inspector-specs">Engineering Spec: Sunrise Beige PBR Cover with Halo Camera Island</div>
            <div class="inspector-stats">
                <span id="insp-val" class="stat-item cyan">💰 Recovery Value: $2.50 USD</span>
                <span id="insp-mass" class="stat-item green">⚖️ Mass: 11.5%</span>
                <span id="insp-status" class="stat-item" style="color:#00FF7F;">♻️ Safe Recyclable Material</span>
            </div>
        </div>
    </div>

    <!-- 15-PART IDENTIFIED HARDWARE GRID -->
    <div class="section-title">
        <span>📋 Identified Components (__TOTAL_PARTS__ Structural Sub-Assemblies)</span>
        <span style="font-size:11px;color:#00F0FF;">Total Salvage Yield: $__TOTAL_VAL__ USD • __HAZ_COUNT__ Hazardous • __REC_COUNT__ Recyclable</span>
    </div>
    <div class="parts-grid">
        __GRID_CARDS_HTML__
    </div>

    <!-- LOWER DECK -->
    <div class="lower-deck">
        <div class="deck-panel">
            <div class="section-title">📷 3D Angles & Hardware Specifications</div>
            <div class="views-row">
                <div class="view-tile" onclick="setCameraAngle('back')"><div class="view-tile-icon">📱</div><div class="view-tile-lbl">Back View</div></div>
                <div class="view-tile" onclick="setCameraAngle('front')"><div class="view-tile-icon">📲</div><div class="view-tile-lbl">Front View</div></div>
                <div class="view-tile" onclick="setCameraAngle('left')"><div class="view-tile-icon">▎</div><div class="view-tile-lbl">Left Rail</div></div>
                <div class="view-tile" onclick="setCameraAngle('right')"><div class="view-tile-icon">▎</div><div class="view-tile-lbl">Right Rail</div></div>
                <div class="view-tile" onclick="setCameraAngle('top')"><div class="view-tile-icon">▔</div><div class="view-tile-lbl">Top View</div></div>
                <div class="view-tile" onclick="setCameraAngle('bottom')"><div class="view-tile-icon"> </div><div class="view-tile-lbl">Bottom USB</div></div>
            </div>
            <div class="specs-list">
                • <strong>Material & Finish:</strong> Vegan Leather, CNC Anodized Aluminum, Corning Glass<br>
                • <strong>SoC Processor:</strong> __PROCESSOR__<br>
                • <strong>Power Reservoir:</strong> __BATTERY__<br>
                • <strong>Storage & RAM:</strong> __STORAGE__ + __RAM__<br>
                • <strong>Optics Package:</strong> __CAMERA__
            </div>
        </div>

        <div class="deck-panel">
            <div class="section-title">🛠️ Step-by-Step Manual Opening Guide</div>
            <div class="steps-scroll">
                __STEPS_HTML__
            </div>
        </div>
    </div>

    <div class="footer-banner">
        <strong>E-Waste AI</strong> | Identify • Analyze • Recover • Certified Scientific E-Waste Intelligence System
    </div>

</div>

<!-- THREE.JS 3D HOLOGRAM DISASSEMBLY ENGINE -->
<script>
var MANUAL_STEPS = __MANUAL_STEPS_JSON__;
var COMPONENT_DATA = __COMP_JSON__;

function createLeatherTexture() {
    var c = document.createElement('canvas');
    c.width = 1024; c.height = 2048;
    var ctx = c.getContext('2d');
    var grad = ctx.createLinearGradient(0,0,1024,2048);
    grad.addColorStop(0, '#E8DCBF');
    grad.addColorStop(0.5, '#DACBAA');
    grad.addColorStop(1, '#CDBB95');
    ctx.fillStyle = grad;
    ctx.fillRect(0,0,1024,2048);
    for(var i=0; i<6000; i++) {
        ctx.fillStyle = 'rgba(150,130,90,' + (Math.random()*0.15 + 0.05) + ')';
        ctx.beginPath();
        ctx.arc(Math.random()*1024, Math.random()*2048, Math.random()*2+1, 0, Math.PI*2);
        ctx.fill();
    }
    ctx.strokeStyle = '#D4AF37';
    ctx.lineWidth = 10;
    ctx.setLineDash([16, 10]);
    ctx.beginPath(); ctx.moveTo(512, 120); ctx.lineTo(512, 1920); ctx.stroke();
    ctx.fillStyle = '#64748B';
    ctx.font = 'bold 36px Arial';
    ctx.fillText('realme', 460, 1650);
    return new THREE.CanvasTexture(c);
}

function createBatteryTexture() {
    var c = document.createElement('canvas');
    c.width = 1024; c.height = 1024;
    var ctx = c.getContext('2d');
    ctx.fillStyle = '#0F131F';
    ctx.fillRect(0,0,1024,1024);
    ctx.strokeStyle = '#5A6275';
    ctx.lineWidth = 14;
    ctx.strokeRect(10,10,1004,1004);
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 56px Arial';
    ctx.fillText('Li-ion RECHARGEABLE BATTERY', 80, 160);
    ctx.font = '36px Arial';
    ctx.fillStyle = '#94A3B8';
    ctx.fillText('Model: BLP951 • 5000mAh / 19.25Wh', 80, 230);
    ctx.fillText('Nominal: 3.85V • Max Charge: 4.45V', 80, 290);
    ctx.fillStyle = '#FFD700';
    ctx.font = 'bold 38px Arial';
    ctx.fillText('⚠ CAUTION / WARNING:', 80, 390);
    ctx.fillStyle = '#EF4444';
    ctx.font = '28px Arial';
    ctx.fillText('Do not puncture, incinerate, or expose over 60°C.', 80, 440);
    ctx.fillText('Danger of chemical fire or explosion.', 80, 480);
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(80, 600, 240, 240);
    ctx.fillStyle = '#000000';
    ctx.fillRect(100, 620, 200, 200);
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(140, 660, 120, 120);
    for(var b=0; b<45; b++) {
        ctx.fillStyle = (b%2===0)?'#FFFFFF':'#0F131F';
        ctx.fillRect(400 + b*10, 680, 8, 120);
    }
    return new THREE.CanvasTexture(c);
}

function createPCBTexture() {
    var c = document.createElement('canvas');
    c.width = 1024; c.height = 1024;
    var ctx = c.getContext('2d');
    ctx.fillStyle = '#093B1F';
    ctx.fillRect(0,0,1024,1024);
    ctx.strokeStyle = 'rgba(212,175,55,0.45)';
    ctx.lineWidth = 3;
    for(var i=0; i<30; i++) {
        ctx.beginPath();
        ctx.moveTo(30 + i*32, 40);
        ctx.lineTo(30 + i*32, 980);
        ctx.stroke();
    }
    ctx.fillStyle = '#111827';
    ctx.fillRect(320, 320, 380, 380);
    ctx.strokeStyle = '#D4AF37';
    ctx.lineWidth = 4;
    ctx.strokeRect(320, 320, 380, 380);
    ctx.fillStyle = '#F8FAFC';
    ctx.font = 'bold 42px monospace';
    ctx.fillText('MEDIATEK', 400, 480);
    ctx.fillText('DIMENSITY', 390, 540);
    ctx.fillStyle = '#FFD700';
    ctx.font = 'bold 36px monospace';
    ctx.fillText('7050 5G', 440, 600);
    ctx.fillStyle = '#1E293B';
    ctx.fillRect(120, 120, 240, 180);
    ctx.fillStyle = '#CBD5E1';
    ctx.font = 'bold 24px monospace';
    ctx.fillText('SAMSUNG UFS', 140, 210);
    ctx.fillText('256GB NAND', 150, 250);
    return new THREE.CanvasTexture(c);
}

function switchModelMode(mode) { return mode; }

// --- 3D Scene Global Variables ---
var scene, camera, renderer, controls;
var layers = [];
var screws = [];
var laserPlane = null;
var cyberRing1, cyberRing2;
var currentExplodeVal = 0.55;
var isAutoPlaying = false;
var autoPlayDir = 1;
var isAutoSpinning = true;
var isLaserActive = true;
var clock = new THREE.Clock();

function init3D() {
    var container = document.getElementById('canvas-3d-container');
    if (!container) return;

    var width = container.clientWidth || 900;
    var height = container.clientHeight || 520;

    scene = new THREE.Scene();
    scene.background = null;

    camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 1000);
    camera.position.set(0, 1.2, 11.5);

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    while (container.firstChild && container.firstChild.tagName === 'CANVAS') {
        container.removeChild(container.firstChild);
    }
    container.appendChild(renderer.domElement);

    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.06;
    controls.maxDistance = 26;
    controls.minDistance = 3.5;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 2.2;
    controls.enableZoom = true;
    controls.enableRotate = true;
    controls.enablePan = true;

    // Lighting
    var amb = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(amb);

    var keyLight = new THREE.DirectionalLight(0xffffff, 1.2);
    keyLight.position.set(8, 12, 10);
    scene.add(keyLight);

    // Cyan & Gold Hologram Rim Lights
    var cyanRim = new THREE.DirectionalLight(0x00F0FF, 1.2);
    cyanRim.position.set(-8, -4, 6);
    scene.add(cyanRim);

    var goldFill = new THREE.PointLight(0xFFD700, 1.0, 20);
    goldFill.position.set(0, 4, 6);
    scene.add(goldFill);

    // --- Build Hologram Scenery ---
    buildHologramEnvironment();

    // --- Build Realistic Hardware Layers ---
    buildRealisticPhoneLayers();
    updateLayerPositions(currentExplodeVal);

    window.addEventListener('resize', onWindowResize, false);
    animate();
}

function buildHologramEnvironment() {
    // 1. Hologram Circular Grid Pedestal
    var gridHelper = new THREE.PolarGridHelper(5.5, 16, 8, 64, 0x00F0FF, 0x004466);
    gridHelper.position.y = -3.2;
    scene.add(gridHelper);

    // 2. Concentric Neon Cyber Rings
    var ringGeo1 = new THREE.RingGeometry(4.2, 4.28, 64);
    var ringMat1 = new THREE.MeshBasicMaterial({ color: 0x00F0FF, side: THREE.DoubleSide, transparent: true, opacity: 0.6 });
    cyberRing1 = new THREE.Mesh(ringGeo1, ringMat1);
    cyberRing1.rotation.x = Math.PI / 2;
    cyberRing1.position.y = -3.15;
    scene.add(cyberRing1);

    var ringGeo2 = new THREE.RingGeometry(5.2, 5.25, 48);
    var ringMat2 = new THREE.MeshBasicMaterial({ color: 0x38BDF8, side: THREE.DoubleSide, transparent: true, opacity: 0.4 });
    cyberRing2 = new THREE.Mesh(ringGeo2, ringMat2);
    cyberRing2.rotation.x = Math.PI / 2;
    cyberRing2.position.y = -3.18;
    scene.add(cyberRing2);

    // 3. Sweeping Holographic Laser Beam
    var laserGeo = new THREE.PlaneGeometry(8.5, 0.12);
    var laserMat = new THREE.MeshBasicMaterial({
        color: 0x00F0FF,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.75,
        blending: THREE.AdditiveBlending
    });
    laserPlane = new THREE.Mesh(laserGeo, laserMat);
    laserPlane.rotation.x = Math.PI / 2;
    scene.add(laserPlane);

    // 4. Floating Holographic Particles
    var partGeo = new THREE.BufferGeometry();
    var partCount = 180;
    var posArray = new Float32Array(partCount * 3);
    for(var p=0; p<partCount*3; p+=3) {
        posArray[p] = (Math.random() - 0.5) * 9;
        posArray[p+1] = (Math.random() - 0.5) * 6;
        posArray[p+2] = (Math.random() - 0.5) * 9;
    }
    partGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    var partMat = new THREE.PointsMaterial({ size: 0.05, color: 0x00F0FF, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending });
    var particles = new THREE.Points(partGeo, partMat);
    scene.add(particles);
}

function buildRealisticPhoneLayers() {
    var pWidth = 2.4;
    var pHeight = 4.8;
    var spread = 1.35;

    var leatherTex = createLeatherTexture();
    var batteryTex = createBatteryTexture();
    var pcbTex = createPCBTexture();

    // 16 Micro Screws
    var screwGroup = new THREE.Group();
    var screwGeo = new THREE.CylinderGeometry(0.035, 0.035, 0.08, 12);
    var screwMat = new THREE.MeshStandardMaterial({ color: 0xDCDDE1, metalness: 0.95, roughness: 0.15 });
    var screwPositions = [
        [-1.0, 2.2], [1.0, 2.2], [-1.0, -2.2], [1.0, -2.2],
        [-1.0, 1.1], [1.0, 1.1], [-1.0, -1.1], [1.0, -1.1],
        [-0.5, 2.25], [0.5, 2.25], [-0.5, -2.25], [0.5, -2.25],
        [-1.1, 0.0], [1.1, 0.0], [-0.4, 0.8], [0.4, 0.8]
    ];
    for(var s=0; s<screwPositions.length; s++) {
        var sm = new THREE.Mesh(screwGeo, screwMat);
        sm.rotation.x = Math.PI / 2;
        sm.position.set(screwPositions[s][0], screwPositions[s][1], 0);
        screwGroup.add(sm);
        screws.push(sm);
    }
    screwGroup.userData = { closedX: -0.09, explodedX: -4.5 * spread, name: '16 Micro-Screws', id: 'c16' };
    scene.add(screwGroup);
    layers.push(screwGroup);

    // Layer 0: Back Cover
    var backGroup = new THREE.Group();
    var backMesh = new THREE.Mesh(
        new THREE.BoxGeometry(pWidth, pHeight, 0.05),
        new THREE.MeshStandardMaterial({ map: leatherTex, roughness: 0.7, metalness: 0.1 })
    );
    backGroup.add(backMesh);
    var haloMesh = new THREE.Mesh(
        new THREE.CylinderGeometry(0.78, 0.78, 0.09, 64),
        new THREE.MeshStandardMaterial({ color: 0xD4AF37, metalness: 0.95, roughness: 0.15 })
    );
    haloMesh.rotation.x = Math.PI / 2;
    haloMesh.position.set(0, 1.1, 0.05);
    backGroup.add(haloMesh);
    backGroup.userData = { closedX: -0.07, explodedX: -3.6 * spread, name: 'Back Cover', id: 'c1' };
    scene.add(backGroup);
    layers.push(backGroup);

    // Layer 1: Camera Module
    var camGroup = new THREE.Group();
    var camDisc = new THREE.Mesh(
        new THREE.CylinderGeometry(0.70, 0.70, 0.08, 36),
        new THREE.MeshStandardMaterial({ color: 0x050508, metalness: 0.85, roughness: 0.2 })
    );
    camDisc.rotation.x = Math.PI / 2;
    camGroup.add(camDisc);
    var lens1 = new THREE.Mesh(
        new THREE.CylinderGeometry(0.26, 0.26, 0.12, 32),
        new THREE.MeshPhysicalMaterial({ color: 0x001B3A, metalness: 0.9, roughness: 0.02, transmission: 0.6, ior: 1.6 })
    );
    lens1.rotation.x = Math.PI / 2;
    lens1.position.set(0, 0, 0.03);
    camGroup.add(lens1);
    var lens2 = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.1, 20), new THREE.MeshStandardMaterial({ color: 0x001122 }));
    lens2.rotation.x = Math.PI / 2; lens2.position.set(-0.36, -0.22, 0.03); camGroup.add(lens2);
    var lens3 = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.1, 20), new THREE.MeshStandardMaterial({ color: 0x001122 }));
    lens3.rotation.x = Math.PI / 2; lens3.position.set(0.36, -0.22, 0.03); camGroup.add(lens3);
    var flashMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.09, 16), new THREE.MeshStandardMaterial({ color: 0xFFEAA7, emissive: 0xFFD700, emissiveIntensity: 0.4 }));
    flashMesh.rotation.x = Math.PI / 2; flashMesh.position.set(0, -0.38, 0.03); camGroup.add(flashMesh);
    camGroup.position.set(0, 1.1, 0);
    camGroup.userData = { closedX: -0.05, explodedX: -2.7 * spread, name: 'Camera Module', id: 'c2' };
    scene.add(camGroup);
    layers.push(camGroup);

    // Layer 2: NFC & Graphite Heat Spreader
    var nfcGroup = new THREE.Group();
    var nfcSheet = new THREE.Mesh(
        new THREE.BoxGeometry(pWidth * 0.88, pHeight * 0.7, 0.02),
        new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.6 })
    );
    nfcGroup.add(nfcSheet);
    var nfcCoil = new THREE.Mesh(
        new THREE.TorusGeometry(0.45, 0.04, 8, 32),
        new THREE.MeshStandardMaterial({ color: 0xD35400, metalness: 0.95, roughness: 0.2 })
    );
    nfcCoil.position.set(0, 0.2, 0.015);
    nfcGroup.add(nfcCoil);
    nfcGroup.userData = { closedX: -0.03, explodedX: -1.8 * spread, name: 'NFC & Graphite Sheet', id: 'c14' };
    scene.add(nfcGroup);
    layers.push(nfcGroup);

    // Layer 3: Middle Chassis / Frame
    var frameGroup = new THREE.Group();
    var frameMesh = new THREE.Mesh(
        new THREE.BoxGeometry(pWidth * 0.98, pHeight * 0.98, 0.08),
        new THREE.MeshStandardMaterial({ color: 0xCBD5E1, metalness: 0.92, roughness: 0.22 })
    );
    frameGroup.add(frameMesh);
    var btn1 = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.45, 0.06), new THREE.MeshStandardMaterial({ color: 0xD4AF37, metalness: 0.9 }));
    btn1.position.set(pWidth*0.49, 0.6, 0); frameGroup.add(btn1);
    var btn2 = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.75, 0.06), new THREE.MeshStandardMaterial({ color: 0xD4AF37, metalness: 0.9 }));
    btn2.position.set(pWidth*0.49, 1.3, 0); frameGroup.add(btn2);
    var usb = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.06, 0.06), new THREE.MeshStandardMaterial({ color: 0x0F172A }));
    usb.position.set(0, -pHeight*0.49, 0); frameGroup.add(usb);
    frameGroup.userData = { closedX: -0.01, explodedX: -0.9 * spread, name: 'Midframe Chassis', id: 'c3' };
    scene.add(frameGroup);
    layers.push(frameGroup);

    // Layer 4: Battery (Li-ion)
    var battGroup = new THREE.Group();
    var battMesh = new THREE.Mesh(
        new THREE.BoxGeometry(pWidth * 0.86, pHeight * 0.48, 0.08),
        new THREE.MeshStandardMaterial({ map: batteryTex, roughness: 0.4, metalness: 0.1 })
    );
    battGroup.add(battMesh);
    var tabA = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.09, 0.02), new THREE.MeshStandardMaterial({ color: 0xFF5500 }));
    tabA.position.set(-0.35, -pHeight*0.24, 0.04); battGroup.add(tabA);
    var tabB = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.09, 0.02), new THREE.MeshStandardMaterial({ color: 0xFF5500 }));
    tabB.position.set(0.35, -pHeight*0.24, 0.04); battGroup.add(tabB);
    battGroup.position.set(0, -0.7, 0);
    battGroup.userData = { closedX: 0.01, explodedX: 0.1 * spread, name: 'Battery (Li-ion)', id: 'c4' };
    scene.add(battGroup);
    layers.push(battGroup);

    // Layer 5: Mainboard (PCB)
    var pcbGroup = new THREE.Group();
    var pcbMesh = new THREE.Mesh(
        new THREE.BoxGeometry(pWidth * 0.92, pHeight * 0.44, 0.04),
        new THREE.MeshStandardMaterial({ map: pcbTex, roughness: 0.35, metalness: 0.3 })
    );
    pcbGroup.add(pcbMesh);
    var emi1 = new THREE.Mesh(new THREE.BoxGeometry(0.70, 0.60, 0.05), new THREE.MeshStandardMaterial({ color: 0xE2E8F0, metalness: 0.92 }));
    emi1.position.set(-0.35, 0.1, 0.03); pcbGroup.add(emi1);
    var emi2 = new THREE.Mesh(new THREE.BoxGeometry(0.60, 0.50, 0.05), new THREE.MeshStandardMaterial({ color: 0xE2E8F0, metalness: 0.92 }));
    emi2.position.set(0.4, 0.12, 0.03); pcbGroup.add(emi2);
    pcbGroup.position.set(0, 1.05, 0);
    pcbGroup.userData = { closedX: 0.03, explodedX: 1.2 * spread, name: 'Mainboard (PCB)', id: 'c5' };
    scene.add(pcbGroup);
    layers.push(pcbGroup);

    // Layer 6: Display Assembly
    var dispGroup = new THREE.Group();
    var dispMesh = new THREE.Mesh(
        new THREE.BoxGeometry(pWidth * 0.96, pHeight * 0.97, 0.04),
        new THREE.MeshStandardMaterial({ color: 0x050810, roughness: 0.1, metalness: 0.85 })
    );
    dispGroup.add(dispMesh);
    var cuBack = new THREE.Mesh(
        new THREE.BoxGeometry(pWidth * 0.92, pHeight * 0.93, 0.01),
        new THREE.MeshStandardMaterial({ color: 0xD35400, metalness: 0.95, roughness: 0.2 })
    );
    cuBack.position.set(0, 0, -0.02); dispGroup.add(cuBack);
    dispGroup.userData = { closedX: 0.05, explodedX: 2.3 * spread, name: 'Display Assembly', id: 'c6' };
    scene.add(dispGroup);
    layers.push(dispGroup);

    // Layer 7: Front Screen (Gorilla Glass)
    var glassGroup = new THREE.Group();
    var glassMesh = new THREE.Mesh(
        new THREE.BoxGeometry(pWidth * 0.98, pHeight * 0.98, 0.02),
        new THREE.MeshPhysicalMaterial({
            color: 0x050C18,
            transmission: 0.88,
            opacity: 0.95,
            transparent: true,
            roughness: 0.02,
            ior: 1.52
        })
    );
    glassGroup.add(glassMesh);
    var punchHole = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.03, 16), new THREE.MeshBasicMaterial({ color: 0x000000 }));
    punchHole.rotation.x = Math.PI / 2;
    punchHole.position.set(0, 2.15, 0.01);
    glassGroup.add(punchHole);
    glassGroup.userData = { closedX: 0.07, explodedX: 3.5 * spread, name: 'Front Screen Glass', id: 'c8' };
    scene.add(glassGroup);
    layers.push(glassGroup);
}

function updateLayerPositions(val) {
    for (var i = 0; i < layers.length; i++) {
        var layer = layers[i];
        var closedX = layer.userData.closedX;
        var explodedX = layer.userData.explodedX;
        layer.position.x = THREE.MathUtils.lerp(closedX, explodedX, val);
        layer.rotation.y = THREE.MathUtils.lerp(0, 0.15, val);
    }
    for (var s = 0; s < screws.length; s++) {
        var sm = screws[s];
        sm.position.z = THREE.MathUtils.lerp(0.05, 0.6 + (s % 3)*0.2, val);
        sm.rotation.z = val * Math.PI * 4;
    }
}

function onSliderChange(val) {
    currentExplodeVal = parseFloat(val) / 100.0;
    document.getElementById('sliderBadge').textContent = 'Disassembly: ' + Math.round(currentExplodeVal * 100) + '%';
    updateLayerPositions(currentExplodeVal);
}

function setSliderPercent(pct) {
    var slider = document.getElementById('explodeSlider');
    if (slider) {
        slider.value = pct;
        onSliderChange(pct);
    }
}

function toggleAutoSpin() {
    isAutoSpinning = !isAutoSpinning;
    if (controls) controls.autoRotate = isAutoSpinning;
    var btn = document.getElementById('btnAutoSpin');
    if (btn) btn.textContent = isAutoSpinning ? '🔄 360° Spin: ON' : '⏸ 360° Spin: OFF';
}

function toggleLaser() {
    isLaserActive = !isLaserActive;
    if (laserPlane) laserPlane.visible = isLaserActive;
    var btn = document.getElementById('btnLaser');
    if (btn) btn.textContent = isLaserActive ? '⚡ Scan Laser: ON' : '⚡ Scan Laser: OFF';
}

function toggleAutoPlay() {
    isAutoPlaying = !isAutoPlaying;
    var btn = document.getElementById('btnAutoPlay');
    if (btn) btn.textContent = isAutoPlaying ? '⏸ Pause' : '▶ Auto-Teardown';
}

function reset3DCamera() {
    if (camera && controls) {
        camera.position.set(0, 1.2, 11.5);
        controls.target.set(0, 0, 0);
        controls.update();
    }
}

function setCameraAngle(view) {
    if (!camera || !controls) return;
    if (view === 'back') camera.position.set(0, 0, -11.5);
    else if (view === 'front') camera.position.set(0, 0, 11.5);
    else if (view === 'left') camera.position.set(-11.5, 0, 0);
    else if (view === 'right') camera.position.set(11.5, 0, 0);
    else if (view === 'top') camera.position.set(0, 11.5, 0.1);
    else if (view === 'bottom') camera.position.set(0, -11.5, 0.1);
    controls.target.set(0, 0, 0);
    controls.update();
}

function inspectPart(partId) {
    var comp = null;
    for (var i = 0; i < COMPONENT_DATA.length; i++) {
        if (COMPONENT_DATA[i].id === partId) { comp = COMPONENT_DATA[i]; break; }
    }
    if (!comp) return;

    var allTiles = document.querySelectorAll('.comp-tile');
    for (var j = 0; j < allTiles.length; j++) allTiles[j].classList.remove('active');
    var activeTile = document.getElementById('tile-' + partId);
    if (activeTile) {
        activeTile.classList.add('active');
        activeTile.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    document.getElementById('insp-icon').textContent = comp.hazardous ? '⚠️' : '⚡';
    document.getElementById('insp-title').textContent = comp.num + '. ' + comp.name + ' (' + comp.sub + ')';
    document.getElementById('insp-sub').textContent = 'Material: ' + comp.material;
    document.getElementById('insp-specs').textContent = 'Engineering Spec: ' + comp.specs;
    document.getElementById('insp-val').textContent = '💰 Recovery Value: $' + comp.value_usd.toFixed(2) + ' USD';
    document.getElementById('insp-mass').textContent = '⚖️ Mass: ' + comp.weight_pct + '%';
    var statusEl = document.getElementById('insp-status');
    if (comp.hazardous) {
        statusEl.textContent = '⚠️ Hazardous Material - Handled under CPCB protocol';
        statusEl.style.color = '#FF4444';
    } else {
        statusEl.textContent = '♻️ Safe Recyclable Material';
        statusEl.style.color = '#00FF7F';
    }
}

function onWindowResize() {
    var container = document.getElementById('canvas-3d-container');
    if (!container || !camera || !renderer) return;
    var w = container.clientWidth;
    var h = container.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
}

function animate() {
    requestAnimationFrame(animate);

    var t = clock.getElapsedTime();

    // Rotate Cyber Pedestal Rings
    if (cyberRing1) cyberRing1.rotation.z = t * 0.3;
    if (cyberRing2) cyberRing2.rotation.z = -t * 0.2;

    // Sweeping Scanning Laser
    if (laserPlane && isLaserActive) {
        laserPlane.position.y = Math.sin(t * 1.8) * 2.8;
    }

    if (isAutoPlaying) {
        currentExplodeVal += 0.005 * autoPlayDir;
        if (currentExplodeVal >= 1.0) { currentExplodeVal = 1.0; autoPlayDir = -1; }
        else if (currentExplodeVal <= 0.0) { currentExplodeVal = 0.0; autoPlayDir = 1; }
        var slider = document.getElementById('explodeSlider');
        if (slider) slider.value = Math.round(currentExplodeVal * 100);
        document.getElementById('sliderBadge').textContent = 'Disassembly: ' + Math.round(currentExplodeVal * 100) + '%';
        updateLayerPositions(currentExplodeVal);
    }

    if (controls) controls.update();
    if (renderer && scene && camera) renderer.render(scene, camera);
}

window.addEventListener('load', init3D);
setTimeout(init3D, 250);
</script>
</body>
</html>'''

python_tail = """
    raw_html = '''""" + html_block + """'''
    html = raw_html.replace("__BRAND_UPPER__", str(brand).upper())
    html = html.replace("__BRAND__", str(brand))
    html = html.replace("__MODEL__", str(model_name))
    html = html.replace("__PROCESSOR__", str(processor))
    html = html.replace("__BATTERY__", str(battery_specs))
    html = html.replace("__STORAGE__", str(storage))
    html = html.replace("__RAM__", str(ram))
    html = html.replace("__CAMERA__", str(camera_specs))
    html = html.replace("__TOTAL_PARTS__", str(total_parts))
    html = html.replace("__TOTAL_VAL__", f"{total_val:.2f}")
    html = html.replace("__HAZ_COUNT__", str(haz_count))
    html = html.replace("__REC_COUNT__", str(rec_count))
    html = html.replace("__GRID_CARDS_HTML__", grid_cards_html)
    html = html.replace("__STEPS_HTML__", steps_html)
    html = html.replace("__MANUAL_STEPS_JSON__", manual_steps_json)
    html = html.replace("__COMP_JSON__", comp_json)
    return html
"""

full_content = py_script + python_tail

with open(target_path, "w", encoding="utf-8") as f:
    f.write(full_content)

print("Hologram three_d_viewer.py assembled successfully!")
