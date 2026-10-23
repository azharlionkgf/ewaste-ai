"""
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

    raw_html = '''<!DOCTYPE html>
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
var phoneModelGroup = null;
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

var isPointerDown = false;
var lastPointerX = 0;
var lastPointerY = 0;

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

    // Master Phone Group for seamless 360° continuous rotation
    phoneModelGroup = new THREE.Group();
    scene.add(phoneModelGroup);

    // OrbitControls for smooth camera zoom
    if (typeof THREE.OrbitControls !== 'undefined') {
        try {
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.08;
            controls.maxDistance = 26;
            controls.minDistance = 3.5;
            controls.enableZoom = true;
            controls.enableRotate = false; // direct pointer rotates phoneModelGroup directly
            controls.enablePan = false;
        } catch (e) {
            console.warn('OrbitControls optional init:', e);
        }
    }

    // Direct touch & mouse drag to rotate the phone in 3D from any angle
    container.addEventListener('pointerdown', function(e) {
        isPointerDown = true;
        lastPointerX = e.clientX;
        lastPointerY = e.clientY;
        container.style.cursor = 'grabbing';
    });

    window.addEventListener('pointermove', function(e) {
        if (!isPointerDown || !phoneModelGroup) return;
        var dx = e.clientX - lastPointerX;
        var dy = e.clientY - lastPointerY;
        lastPointerX = e.clientX;
        lastPointerY = e.clientY;
        phoneModelGroup.rotation.y += dx * 0.012;
        phoneModelGroup.rotation.x += dy * 0.012;
        phoneModelGroup.rotation.x = Math.max(-1.15, Math.min(1.15, phoneModelGroup.rotation.x));
    });

    window.addEventListener('pointerup', function() {
        isPointerDown = false;
        if (container) container.style.cursor = 'grab';
    });

    window.addEventListener('pointercancel', function() {
        isPointerDown = false;
        if (container) container.style.cursor = 'grab';
    });

    container.addEventListener('wheel', function(e) {
        e.preventDefault();
        if (camera) {
            camera.position.z += e.deltaY * 0.005;
            camera.position.z = Math.max(3.8, Math.min(24.0, camera.position.z));
        }
    }, { passive: false });

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
    // --- Build Device-Specific 3D Model Based on Category ---
    var deviceShape = '__SHAPE_TYPE__';
    if      (deviceShape === 'laptop')  buildLaptopLayers();
    else if (deviceShape === 'desktop') buildDesktopLayers();
    else if (deviceShape === 'tablet')  buildTabletLayers();
    else if (deviceShape === 'display') buildTVLayers();
    else if (deviceShape === 'battery') buildBatteryPackLayers();
    else if (deviceShape === 'pcb')     buildPCBLayers();
    else                                buildRealisticPhoneLayers();
    updateLayerPositions(currentExplodeVal);
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
    var pW = 2.45;   // phone width
    var pH = 5.1;    // phone height
    var spread = 1.45;  // explode spacing multiplier

    var leatherTex = createLeatherTexture();
    var batteryTex = createBatteryTexture();
    var pcbTex     = createPCBTexture();

    // Helper: rounded-rectangle Shape
    function roundedBox(w, h, d, r) {
        return new THREE.BoxGeometry(w, h, d);
    }

    // ─── LAYER 0: 16 Micro-Screws ───
    var screwGroup = new THREE.Group();
    var screwGeo   = new THREE.CylinderGeometry(0.038, 0.032, 0.09, 14);
    var screwMat   = new THREE.MeshStandardMaterial({ color: 0xCDD5D9, metalness: 0.98, roughness: 0.08 });
    var headGeo    = new THREE.CylinderGeometry(0.055, 0.055, 0.025, 14);
    var headMat    = new THREE.MeshStandardMaterial({ color: 0xB8BCC0, metalness: 0.99, roughness: 0.06 });
    var screwPos = [
        [-1.05,2.3],[ 1.05,2.3],[-1.05,-2.3],[ 1.05,-2.3],
        [-1.05,1.2],[ 1.05,1.2],[-1.05,-1.2],[ 1.05,-1.2],
        [-0.55,2.35],[0.55,2.35],[-0.55,-2.35],[0.55,-2.35],
        [-1.1,0.0],[1.1,0.0],[-0.45,0.85],[0.45,0.85]
    ];
    for (var s=0; s<screwPos.length; s++) {
        var sg = new THREE.Group();
        var shaft = new THREE.Mesh(screwGeo, screwMat);
        shaft.rotation.x = Math.PI/2;
        sg.add(shaft);
        var head = new THREE.Mesh(headGeo, headMat);
        head.rotation.x = Math.PI/2;
        head.position.z = 0.057;
        sg.add(head);
        // Cross-slot line on head
        var slotGeo = new THREE.BoxGeometry(0.095, 0.012, 0.01);
        var slotMat = new THREE.MeshBasicMaterial({ color: 0x505560 });
        var slot1 = new THREE.Mesh(slotGeo, slotMat); slot1.position.z = 0.066; sg.add(slot1);
        var slot2 = new THREE.Mesh(slotGeo, slotMat); slot2.rotation.z = Math.PI/2; slot2.position.z = 0.066; sg.add(slot2);
        sg.position.set(screwPos[s][0], screwPos[s][1], 0);
        screwGroup.add(sg);
        screws.push(sg);
    }
    screwGroup.userData = { closedY: -4.2*spread, explodedY: -4.2*spread, closedZ: 0, explodedZ: 0.05, name:'16 Micro-Screws', id:'c16' };
    phoneModelGroup.add(screwGroup);
    layers.push(screwGroup);

    // ─── LAYER 1: Back Cover (Glass/Leather, most realistic) ───
    var backGroup = new THREE.Group();
    var backGeo = roundedBox(pW, pH, 0.072, 0.28);
    var backMesh = new THREE.Mesh(backGeo, new THREE.MeshStandardMaterial({ map: leatherTex, roughness: 0.68, metalness: 0.07 }));
    backGroup.add(backMesh);
    // Camera Island — Gold ring
    var cIsland = new THREE.CylinderGeometry(0.82, 0.82, 0.065, 64);
    var cIslandMesh = new THREE.Mesh(cIsland, new THREE.MeshStandardMaterial({ color:0xCBB070, metalness:0.95, roughness:0.12 }));
    cIslandMesh.rotation.x = Math.PI/2; cIslandMesh.position.set(0, 1.15, 0.055);
    backGroup.add(cIslandMesh);
    // Camera island black base
    var cBase = new THREE.Mesh(new THREE.CylinderGeometry(0.74, 0.74, 0.06, 48),
        new THREE.MeshStandardMaterial({ color:0x08080C, roughness:0.25, metalness:0.6 }));
    cBase.rotation.x = Math.PI/2; cBase.position.set(0, 1.15, 0.058); backGroup.add(cBase);
    // Logo text plane
    var logoGeo = new THREE.PlaneGeometry(0.8, 0.18);
    var logoMat = new THREE.MeshStandardMaterial({ color:0xB8C4CC, metalness:0.9, roughness:0.2, transparent:true, opacity:0.7 });
    var logoMesh = new THREE.Mesh(logoGeo, logoMat);
    logoMesh.position.set(0, -0.8, 0.04); backGroup.add(logoMesh);
    backGroup.userData = { closedY:0, explodedY:-3.5*spread, name:'Back Cover (Glass)', id:'c1' };
    phoneModelGroup.add(backGroup); layers.push(backGroup);

    // ─── LAYER 2: Triple Camera Module ───
    var camGroup = new THREE.Group();
    // Outer ring
    var outerRing = new THREE.Mesh(
        new THREE.CylinderGeometry(0.73, 0.73, 0.1, 48),
        new THREE.MeshStandardMaterial({ color:0x0A0A0F, metalness:0.85, roughness:0.18 }));
    outerRing.rotation.x = Math.PI/2; camGroup.add(outerRing);
    // Main lens (200MP)
    var mainLens = new THREE.Mesh(
        new THREE.CylinderGeometry(0.28, 0.28, 0.14, 32),
        new THREE.MeshPhysicalMaterial({ color:0x010A1A, metalness:0.9, roughness:0.02, transmission:0.7, ior:1.72, thickness:0.1 }));
    mainLens.rotation.x = Math.PI/2; mainLens.position.z=0.04; camGroup.add(mainLens);
    // Lens reflection ring
    var lensRing = new THREE.Mesh(
        new THREE.TorusGeometry(0.25, 0.02, 8, 32),
        new THREE.MeshStandardMaterial({ color:0x3060A0, metalness:0.9, roughness:0.1 }));
    lensRing.rotation.x = Math.PI/2; lensRing.position.z=0.07; camGroup.add(lensRing);
    // Ultrawide lens
    var lens2 = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.11, 24),
        new THREE.MeshPhysicalMaterial({ color:0x010812, metalness:0.85, roughness:0.03, transmission:0.65, ior:1.65 }));
    lens2.rotation.x = Math.PI/2; lens2.position.set(-0.38,-0.22,0.04); camGroup.add(lens2);
    // Macro lens
    var lens3 = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.09, 20),
        new THREE.MeshPhysicalMaterial({ color:0x010812, metalness:0.85, roughness:0.03, transmission:0.6, ior:1.6 }));
    lens3.rotation.x = Math.PI/2; lens3.position.set(0.38,-0.22,0.04); camGroup.add(lens3);
    // Flash + IR
    var flash = new THREE.Mesh(new THREE.CylinderGeometry(0.082, 0.082, 0.09, 16),
        new THREE.MeshStandardMaterial({ color:0xFFE8A0, emissive:0xFFD060, emissiveIntensity:0.6 }));
    flash.rotation.x = Math.PI/2; flash.position.set(0.38,0.22,0.04); camGroup.add(flash);
    var ir = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.07, 12),
        new THREE.MeshStandardMaterial({ color:0x3A1A1A }));
    ir.rotation.x = Math.PI/2; ir.position.set(-0.38,0.22,0.04); camGroup.add(ir);
    camGroup.position.set(0, 1.15, 0);
    camGroup.userData = { closedY:0, explodedY:-2.6*spread, name:'Triple Camera Module', id:'c2' };
    phoneModelGroup.add(camGroup); layers.push(camGroup);

    // ─── LAYER 3: NFC Coil + Graphite Thermal Sheet ───
    var nfcGroup = new THREE.Group();
    var nfcBase = new THREE.Mesh(
        roundedBox(pW*0.9, pH*0.72, 0.018, 0.15),
        new THREE.MeshStandardMaterial({ color:0x1A2235, roughness:0.55, metalness:0.12 }));
    nfcGroup.add(nfcBase);
    // NFC coil (flat copper torus)
    var nfcCoil = new THREE.Mesh(
        new THREE.TorusGeometry(0.48, 0.038, 8, 48),
        new THREE.MeshStandardMaterial({ color:0xD06010, metalness:0.97, roughness:0.14 }));
    nfcCoil.rotation.x = Math.PI/2; nfcCoil.position.set(0.05, 0.2, 0.015); nfcGroup.add(nfcCoil);
    // NFC chip
    var nfcChip = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.14, 0.04),
        new THREE.MeshStandardMaterial({ color:0x101820, metalness:0.8 }));
    nfcChip.position.set(0.05, 0.2, 0.03); nfcGroup.add(nfcChip);
    // Graphite stripes
    for (var gx=-1; gx<=1; gx+=0.5) {
        var gStrip = new THREE.Mesh(new THREE.BoxGeometry(0.04, pH*0.65, 0.008),
            new THREE.MeshStandardMaterial({ color:0x22293A, roughness:0.4 }));
        gStrip.position.set(gx, 0, -0.01); nfcGroup.add(gStrip);
    }
    nfcGroup.userData = { closedY:0, explodedY:-1.7*spread, name:'NFC Coil + Graphite Sheet', id:'c14' };
    phoneModelGroup.add(nfcGroup); layers.push(nfcGroup);

    // ─── LAYER 4: Midframe (Aluminum Alloy) ───
    var frameGroup = new THREE.Group();
    var outerFrame = new THREE.Mesh(
        roundedBox(pW, pH, 0.095, 0.28),
        new THREE.MeshStandardMaterial({ color:0xCDD4DA, metalness:0.94, roughness:0.19 }));
    frameGroup.add(outerFrame);
    // Inner cutout (hollow look) — dark recessed area
    var innerCut = new THREE.Mesh(
        roundedBox(pW*0.88, pH*0.92, 0.1, 0.22),
        new THREE.MeshStandardMaterial({ color:0x101418, roughness:0.9 }));
    innerCut.position.z = 0.002; frameGroup.add(innerCut);
    // Volume buttons
    var btn = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.42, 0.07),
        new THREE.MeshStandardMaterial({ color:0xC8AD6A, metalness:0.93 }));
    btn.position.set(pW*0.5+0.022, 0.62, 0); frameGroup.add(btn);
    var btn2 = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.72, 0.07),
        new THREE.MeshStandardMaterial({ color:0xC8AD6A, metalness:0.93 }));
    btn2.position.set(pW*0.5+0.022, 1.35, 0); frameGroup.add(btn2);
    // Power button (opposite side)
    var pwr = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.55, 0.07),
        new THREE.MeshStandardMaterial({ color:0xC8AD6A, metalness:0.93 }));
    pwr.position.set(-pW*0.5-0.022, 0.7, 0); frameGroup.add(pwr);
    // USB port
    var usbc = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.07, 0.08),
        new THREE.MeshStandardMaterial({ color:0x080C10 }));
    usbc.position.set(0, -pH*0.495, 0); frameGroup.add(usbc);
    // SIM tray
    var sim = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.07, 0.06),
        new THREE.MeshStandardMaterial({ color:0xF0D070, metalness:0.9 }));
    sim.position.set(-pW*0.5-0.022, -1.5, 0); frameGroup.add(sim);
    frameGroup.userData = { closedY:0, explodedY:-0.8*spread, name:'Midframe (Aluminum)', id:'c3' };
    phoneModelGroup.add(frameGroup); layers.push(frameGroup);

    // ─── LAYER 5: Battery (Li-Poly Pouch Cell) ───
    var battGroup = new THREE.Group();
    var battBody = new THREE.Mesh(
        roundedBox(pW*0.87, pH*0.49, 0.085, 0.1),
        new THREE.MeshStandardMaterial({ map: batteryTex, roughness:0.38, metalness:0.12 }));
    battGroup.add(battBody);
    // Electrode tabs
    var tabA = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.09, 0.025),
        new THREE.MeshStandardMaterial({ color:0xFF5800, metalness:0.85, roughness:0.3 }));
    tabA.position.set(-0.38, -pH*0.245, 0.045); battGroup.add(tabA);
    var tabB = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.09, 0.025),
        new THREE.MeshStandardMaterial({ color:0xFF5800, metalness:0.85, roughness:0.3 }));
    tabB.position.set(0.38, -pH*0.245, 0.045); battGroup.add(tabB);
    // BMU circuit strip
    var bmu = new THREE.Mesh(new THREE.BoxGeometry(pW*0.82, 0.16, 0.03),
        new THREE.MeshStandardMaterial({ color:0x101C14, roughness:0.6 }));
    bmu.position.set(0, -pH*0.22, 0.06); battGroup.add(bmu);
    // Thermal adhesive stripes
    for (var tx=-0.5; tx<=0.5; tx+=0.5) {
        var tadhesive = new THREE.Mesh(new THREE.BoxGeometry(0.15, pH*0.45, 0.005),
            new THREE.MeshStandardMaterial({ color:0x1E3022, transparent:true, opacity:0.7 }));
        tadhesive.position.set(tx, 0, -0.045); battGroup.add(tadhesive);
    }
    battGroup.position.set(0, -0.68, 0);
    battGroup.userData = { closedY:0, explodedY:0.12*spread, name:'Battery (5000mAh Li-Poly)', id:'c4' };
    phoneModelGroup.add(battGroup); layers.push(battGroup);

    // ─── LAYER 6: Mainboard (10-Layer PCB) ───
    var pcbGroup = new THREE.Group();
    var pcbBody = new THREE.Mesh(
        roundedBox(pW*0.9, pH*0.45, 0.045, 0.08),
        new THREE.MeshStandardMaterial({ map: pcbTex, roughness:0.32, metalness:0.32 }));
    pcbGroup.add(pcbBody);
    // EMI Shield (SoC area) — matte aluminum can
    var emiShield = new THREE.Mesh(new THREE.BoxGeometry(0.74, 0.66, 0.062),
        new THREE.MeshStandardMaterial({ color:0xDDE2E5, metalness:0.94, roughness:0.2 }));
    emiShield.position.set(-0.33, 0.1, 0.034); pcbGroup.add(emiShield);
    // EMI Shield 2 (modem)
    var emi2 = new THREE.Mesh(new THREE.BoxGeometry(0.64, 0.55, 0.062),
        new THREE.MeshStandardMaterial({ color:0xDDE2E5, metalness:0.94, roughness:0.2 }));
    emi2.position.set(0.42, 0.12, 0.034); pcbGroup.add(emi2);
    // RAM chips (visible beside EMI)
    for (var rc=0; rc<2; rc++) {
        var ramChip = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.16, 0.04),
            new THREE.MeshStandardMaterial({ color:0x0A0E12, metalness:0.7, roughness:0.3 }));
        ramChip.position.set(0.1+rc*0.25, -0.3, 0.04); pcbGroup.add(ramChip);
    }
    // Coaxial RF cable connector (small gold dot)
    var rfConn = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.04, 12),
        new THREE.MeshStandardMaterial({ color:0xD4AF37, metalness:0.99, roughness:0.05 }));
    rfConn.rotation.x = Math.PI/2; rfConn.position.set(-0.75, 0.7, 0.04); pcbGroup.add(rfConn);
    // USB-C daughterboard connector
    var usbConn = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.1, 0.05),
        new THREE.MeshStandardMaterial({ color:0x182530, metalness:0.6 }));
    usbConn.position.set(0, -0.85, 0.04); pcbGroup.add(usbConn);
    // Gold bond-wire pattern (emissive)
    var goldTrace = new THREE.Mesh(new THREE.BoxGeometry(pW*0.85, 0.015, 0.002),
        new THREE.MeshStandardMaterial({ color:0xC8A020, emissive:0x8060A0, emissiveIntensity:0.25, metalness:0.99 }));
    goldTrace.position.set(0, 0.5, 0.026); pcbGroup.add(goldTrace);
    var goldTrace2 = goldTrace.clone(); goldTrace2.position.y = -0.15; pcbGroup.add(goldTrace2);
    // Thermal paste blobs on EMI shield
    var paste = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.012, 16),
        new THREE.MeshStandardMaterial({ color:0xA8A0A0, metalness:0.1, roughness:0.95 }));
    paste.rotation.x = Math.PI/2; paste.position.set(-0.33, 0.1, 0.068); pcbGroup.add(paste);
    pcbGroup.position.set(0, 1.08, 0);
    pcbGroup.userData = { closedY:0, explodedY:1.25*spread, name:'Mainboard — Dimensity 7050 SoC', id:'c5' };
    phoneModelGroup.add(pcbGroup); layers.push(pcbGroup);

    // ─── LAYER 7: AMOLED Display Assembly ───
    var dispGroup = new THREE.Group();
    var dispBody = new THREE.Mesh(
        roundedBox(pW*0.96, pH*0.97, 0.042, 0.26),
        new THREE.MeshStandardMaterial({ color:0x04060C, roughness:0.08, metalness:0.88 }));
    dispGroup.add(dispBody);
    // Copper flex back (visible on OLED underside)
    var cuFlex = new THREE.Mesh(
        roundedBox(pW*0.93, pH*0.93, 0.01, 0.22),
        new THREE.MeshStandardMaterial({ color:0xC06015, metalness:0.96, roughness:0.18 }));
    cuFlex.position.z = -0.026; dispGroup.add(cuFlex);
    // Touch IC chip
    var touchIC = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.2, 0.04),
        new THREE.MeshStandardMaterial({ color:0x0A1018, metalness:0.7 }));
    touchIC.position.set(0.6, -1.8, -0.03); dispGroup.add(touchIC);
    // Punchhole camera ring
    var phRing = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.016, 8, 24),
        new THREE.MeshStandardMaterial({ color:0x1A1A1F, metalness:0.7 }));
    phRing.rotation.x = Math.PI/2; phRing.position.set(0, 2.2, 0.022); dispGroup.add(phRing);
    dispGroup.userData = { closedY:0, explodedY:2.4*spread, name:'AMOLED Display (120Hz)', id:'c6' };
    phoneModelGroup.add(dispGroup); layers.push(dispGroup);

    // ─── LAYER 8: Gorilla Glass Front ───
    var glassGroup = new THREE.Group();
    var glassMesh = new THREE.Mesh(
        roundedBox(pW*0.985, pH*0.985, 0.025, 0.28),
        new THREE.MeshPhysicalMaterial({
            color: 0x05090F,
            transmission: 0.92,
            opacity: 0.95,
            transparent: true,
            roughness: 0.015,
            ior: 1.54,
            thickness: 0.15,
            reflectivity: 0.9
        }));
    glassGroup.add(glassMesh);
    // Punchhole camera
    var punchHole = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.065, 0.03, 16),
        new THREE.MeshBasicMaterial({ color: 0x000000 }));
    punchHole.rotation.x = Math.PI/2; punchHole.position.set(0, 2.2, 0.01);
    glassGroup.add(punchHole);
    // Selfie camera black circle
    var selfieLen = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.042, 0.015, 16),
        new THREE.MeshPhysicalMaterial({ color:0x000510, transmission:0.5, roughness:0.05 }));
    selfieLen.rotation.x = Math.PI/2; selfieLen.position.set(0, 2.2, 0.018); glassGroup.add(selfieLen);
    glassGroup.userData = { closedY:0, explodedY:3.6*spread, name:'Gorilla Glass Victus Front', id:'c8' };
    phoneModelGroup.add(glassGroup); layers.push(glassGroup);

    // Flex ribbon cables connecting layers (decorative — emissive orange)
    var ribbonMat = new THREE.MeshStandardMaterial({ color:0xD84C00, metalness:0.7, roughness:0.4, emissive:0x501800, emissiveIntensity:0.3 });
    var ribbon1 = new THREE.Mesh(new THREE.BoxGeometry(0.085, 0.5, 0.012), ribbonMat);
    ribbon1.position.set(0.65, -0.5, 0); phoneModelGroup.add(ribbon1);
    var ribbon2 = new THREE.Mesh(new THREE.BoxGeometry(0.085, 0.4, 0.012), ribbonMat);
    ribbon2.position.set(-0.65, 0.6, 0); phoneModelGroup.add(ribbon2);
}

// CASCADE EXPLODE — dynamic per-layer windows based on actual layer count
function updateLayerPositions(val) {
    var n = layers.length;
    if (n === 0) return;
    for (var i = 0; i < n; i++) {
        var wStart = i / n;
        var wEnd   = (i + 1) / n;
        var t = (val - wStart) / Math.max(0.001, wEnd - wStart);
        t = Math.max(0.0, Math.min(1.0, t));
        // Ease-out cubic
        var te = 1.0 - Math.pow(1.0 - t, 3.0);
        var layer = layers[i];
        var closedY   = (layer.userData.closedY   !== undefined) ? layer.userData.closedY   : 0;
        var explodedY = (layer.userData.explodedY  !== undefined) ? layer.userData.explodedY : (i - n/2) * 1.4;
        layer.position.y = closedY + (explodedY - closedY) * te;
        var zSign = (i % 2 === 0) ? 1.0 : -0.8;
        layer.position.z = te * zSign * (i+1) * 0.3;
        var tiltDir = (i % 2 === 0) ? -1 : 1;
        layer.rotation.x = te * tiltDir * 0.12;
        layer.rotation.y = te * tiltDir * 0.07;
        // Cyan glow on the actively peeling layer
        var isActive = val >= wStart && val <= wEnd;
        layer.traverse(function(obj) {
            if (obj.isMesh && obj.material) {
                var mats = Array.isArray(obj.material) ? obj.material : [obj.material];
                mats.forEach(function(m) {
                    if (m.emissive) {
                        m.emissiveIntensity = isActive ? 0.4 : 0.0;
                        if (isActive) m.emissive.set(0x00C8FF);
                    }
                });
            }
        });
    }
    // Screws: staggered pop-out first 12% of slider
    for (var s2 = 0; s2 < screws.length; s2++) {
        var sm = screws[s2];
        var delay = (s2 / Math.max(1, screws.length)) * 0.08;
        var lt = Math.max(0, Math.min(1, (val - delay) / Math.max(0.001, 0.12 - delay)));
        var lte = 1.0 - Math.pow(1.0 - lt, 2.0);
        sm.position.z = lte * (0.7 + (s2 % 5)*0.14);
        sm.rotation.z = lte * Math.PI * 8;
    }
    // Update badge with active layer name
    var pct = Math.round(val * 100);
    var activeIdx = Math.min(n-1, Math.floor(val * n));
    var activeName = (layers[activeIdx] && layers[activeIdx].userData.name) ? layers[activeIdx].userData.name : '';
    var badge = document.getElementById('sliderBadge');
    if (badge) badge.textContent = 'Disassembly: ' + pct + '%' + (activeName ? ' → ' + activeName : '');
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
    if (camera) camera.position.set(0, 1.2, 11.5);
    if (phoneModelGroup) phoneModelGroup.rotation.set(0, 0, 0);
    if (controls) {
        controls.target.set(0, 0, 0);
        controls.update();
    }
}

function setCameraAngle(view) {
    if (!phoneModelGroup) return;
    if (view === 'front') phoneModelGroup.rotation.set(0, 0, 0);
    else if (view === 'back') phoneModelGroup.rotation.set(0, Math.PI, 0);
    else if (view === 'left') phoneModelGroup.rotation.set(0, Math.PI / 2, 0);
    else if (view === 'right') phoneModelGroup.rotation.set(0, -Math.PI / 2, 0);
    else if (view === 'top') phoneModelGroup.rotation.set(Math.PI / 2, 0, 0);
    else if (view === 'bottom') phoneModelGroup.rotation.set(-Math.PI / 2, 0, 0);
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
var spinVelocity = 0.0;

function animate() {
    requestAnimationFrame(animate);
    var t = clock.getElapsedTime();

    // Rotate Cyber Pedestal Rings with pulse
    if (cyberRing1) cyberRing1.rotation.z = t * 0.32;
    if (cyberRing2) cyberRing2.rotation.z = -t * 0.18;
    if (cyberRing1 && cyberRing1.material) {
        cyberRing1.material.opacity = 0.45 + 0.2 * Math.sin(t * 2.1);
    }

    // Sweeping Scanning Laser with pulsing opacity
    if (laserPlane && isLaserActive) {
        laserPlane.position.y = Math.sin(t * 1.6) * 3.1;
        if (laserPlane.material) laserPlane.material.opacity = 0.5 + 0.28 * Math.sin(t * 3.0);
    }

    // Auto-Spin with inertia coast after drag
    if (phoneModelGroup) {
        if (isAutoSpinning && !isPointerDown) {
            phoneModelGroup.rotation.y += 0.012;
            spinVelocity = 0;
        } else if (!isPointerDown && Math.abs(spinVelocity) > 0.0002) {
            phoneModelGroup.rotation.y += spinVelocity;
            spinVelocity *= 0.92;
        }
    }

    if (isAutoPlaying) {
        currentExplodeVal += 0.004 * autoPlayDir;
        if (currentExplodeVal >= 1.0) { currentExplodeVal = 1.0; autoPlayDir = -1; }
        else if (currentExplodeVal <= 0.0) { currentExplodeVal = 0.0; autoPlayDir = 1; }
        var slider = document.getElementById('explodeSlider');
        if (slider) slider.value = Math.round(currentExplodeVal * 100);
        updateLayerPositions(currentExplodeVal);
    }

    if (controls) controls.update();
    if (renderer && scene && camera) renderer.render(scene, camera);
}
}

var initDone = false;
function safeInit3D() {
    if (initDone) return;
    if (typeof THREE === 'undefined') {
        setTimeout(safeInit3D, 100);
        return;
    }
    initDone = true;
    init3D();
}

window.addEventListener('DOMContentLoaded', safeInit3D);
window.addEventListener('load', safeInit3D);
setTimeout(safeInit3D, 150);

// ═══════════════════════════════════════════════════════
// 🖥️ LAPTOP 3D MODEL
// ═══════════════════════════════════════════════════════
function buildLaptopLayers() {
    layers = []; screws = [];
    var lW=5.8, lH=3.8, spread=1.5;

    function rBox(w,h,d,r){
        return new THREE.BoxGeometry(w, h, d);
    }

    // Layer 0: Bottom Base Chassis
    var baseG=new THREE.Group();
    baseG.add(new THREE.Mesh(rBox(lW,lH,0.18,0.25),new THREE.MeshStandardMaterial({color:0xC8CACF,metalness:0.95,roughness:0.18})));
    // Rubber feet
    [[lW*0.42,lH*0.43],[- lW*0.42,lH*0.43],[lW*0.42,-lH*0.43],[-lW*0.42,-lH*0.43]].forEach(function(p){
        var ft=new THREE.Mesh(new THREE.CylinderGeometry(0.14,0.14,0.06,12),new THREE.MeshStandardMaterial({color:0x111111,roughness:0.95}));
        ft.rotation.x=Math.PI/2; ft.position.set(p[0],p[1],-0.12); baseG.add(ft);
    });
    // Vent slots
    for(var v=-1.2;v<=1.2;v+=0.18){
        var slot=new THREE.Mesh(new THREE.BoxGeometry(1.8,0.06,0.02),new THREE.MeshStandardMaterial({color:0x222226}));
        slot.position.set(1.0,v,-0.1); baseG.add(slot);
    }
    baseG.userData={closedY:0,explodedY:-3.5*spread,name:'Bottom Chassis',id:'c1'};
    phoneModelGroup.add(baseG); layers.push(baseG);

    // Layer 1: Battery (full-width)
    var battG=new THREE.Group();
    battG.add(new THREE.Mesh(new THREE.BoxGeometry(lW*0.88,lH*0.28,0.16),new THREE.MeshStandardMaterial({color:0x101820,roughness:0.4})));
    var battLabel=new THREE.Mesh(new THREE.BoxGeometry(lW*0.7,0.25,0.01),new THREE.MeshStandardMaterial({color:0x0A3A7A,metalness:0.3}));
    battLabel.position.set(0,0,0.09); battG.add(battLabel);
    battG.position.set(0,-lH*0.33,0);
    battG.userData={closedY:0,explodedY:-2.4*spread,name:'72Wh Li-Polymer Battery',id:'c4'};
    phoneModelGroup.add(battG); layers.push(battG);

    // Layer 2: Cooling + Fan
    var fanG=new THREE.Group();
    var fanBase=new THREE.Mesh(new THREE.BoxGeometry(lW*0.85,lH*0.55,0.08),new THREE.MeshStandardMaterial({color:0x181C22,roughness:0.5}));
    fanG.add(fanBase);
    // Fan blades (cylinder + lines)
    var fanHub=new THREE.Mesh(new THREE.CylinderGeometry(0.55,0.55,0.06,32),new THREE.MeshStandardMaterial({color:0x2A2E38,metalness:0.7}));
    fanHub.rotation.x=Math.PI/2; fanHub.position.set(-1.8,0.5,0.05); fanG.add(fanHub);
    for(var b=0;b<7;b++){
        var blade=new THREE.Mesh(new THREE.BoxGeometry(0.42,0.09,0.04),new THREE.MeshStandardMaterial({color:0x333844,metalness:0.8}));
        blade.rotation.z=b*Math.PI/3.5; blade.position.set(-1.8+Math.cos(b*Math.PI/3.5)*0.28, 0.5+Math.sin(b*Math.PI/3.5)*0.28,0.06);
        fanG.add(blade);
    }
    // Heatpipe
    var pipe=new THREE.Mesh(new THREE.CylinderGeometry(0.055,0.055,4.5,12),new THREE.MeshStandardMaterial({color:0xD4A020,metalness:0.95,roughness:0.12}));
    pipe.rotation.z=Math.PI/2; pipe.position.set(0.3,0.5,0.06); fanG.add(pipe);
    fanG.userData={closedY:0,explodedY:-1.5*spread,name:'Cooling Fan + Heatpipe',id:'c3'};
    phoneModelGroup.add(fanG); layers.push(fanG);

    // Layer 3: Mainboard (PCB)
    var pcbTex=createPCBTexture();
    var pcbG=new THREE.Group();
    pcbG.add(new THREE.Mesh(new THREE.BoxGeometry(lW*0.82,lH*0.62,0.05),new THREE.MeshStandardMaterial({map:pcbTex,roughness:0.3,metalness:0.35})));
    // CPU/GPU EMI shields
    [[0.6,0.4,1.1,0.9],[- 0.9,0.2,1.2,1.0]].forEach(function(r){
        var sh=new THREE.Mesh(new THREE.BoxGeometry(r[2],r[3],0.07),new THREE.MeshStandardMaterial({color:0xD8DDE0,metalness:0.95,roughness:0.18}));
        sh.position.set(r[0],r[1],0.04); pcbG.add(sh);
    });
    // RAM slots
    for(var rs=0;rs<2;rs++){
        var ram=new THREE.Mesh(new THREE.BoxGeometry(0.12,1.5,0.06),new THREE.MeshStandardMaterial({color:0x101010,metalness:0.7}));
        ram.position.set(1.5+rs*0.22,-0.1,0.04); pcbG.add(ram);
    }
    pcbG.userData={closedY:0,explodedY:-0.6*spread,name:'Mainboard — Intel/AMD SoC',id:'c5'};
    phoneModelGroup.add(pcbG); layers.push(pcbG);

    // Layer 4: Keyboard Deck
    var kbG=new THREE.Group();
    kbG.add(new THREE.Mesh(rBox(lW,lH,0.09,0.22),new THREE.MeshStandardMaterial({color:0xBFC3C8,metalness:0.92,roughness:0.2})));
    // Key grid
    for(var kr=0;kr<4;kr++){
        for(var kc=0;kc<13;kc++){
            var key=new THREE.Mesh(new THREE.BoxGeometry(0.28,0.27,0.04),new THREE.MeshStandardMaterial({color:0x2A2D34,roughness:0.9}));
            key.position.set(-2.4+kc*0.4, 0.4-kr*0.38, 0.065); kbG.add(key);
        }
    }
    // Trackpad
    var tp=new THREE.Mesh(rBox(1.4,0.88,0.02,0.12),new THREE.MeshPhysicalMaterial({color:0xABAEB4,roughness:0.08,metalness:0.3}));
    tp.position.set(0,-1.3,0.05); kbG.add(tp);
    kbG.userData={closedY:0,explodedY:0.6*spread,name:'Keyboard + Trackpad Deck',id:'c7'};
    phoneModelGroup.add(kbG); layers.push(kbG);

    // Layer 5: Screen Hinge + Lid
    var lidG=new THREE.Group();
    lidG.add(new THREE.Mesh(rBox(lW,lH,0.08,0.22),new THREE.MeshStandardMaterial({color:0xC0C4CA,metalness:0.95,roughness:0.16})));
    // Display panel
    var disp=new THREE.Mesh(rBox(lW*0.94,lH*0.92,0.02,0.18),new THREE.MeshStandardMaterial({color:0x030407,roughness:0.05,metalness:0.9}));
    disp.position.z=0.05; lidG.add(disp);
    // Webcam
    var cam=new THREE.Mesh(new THREE.CylinderGeometry(0.07,0.07,0.05,12),new THREE.MeshStandardMaterial({color:0x080808}));
    cam.rotation.x=Math.PI/2; cam.position.set(0,lH*0.47,0.06); lidG.add(cam);
    // Hinges
    [-1.5,1.5].forEach(function(hx){
        var hinge=new THREE.Mesh(new THREE.CylinderGeometry(0.18,0.18,0.38,16),new THREE.MeshStandardMaterial({color:0x9AA0A6,metalness:0.98,roughness:0.1}));
        hinge.rotation.z=Math.PI/2; hinge.position.set(hx,-lH*0.5,0); lidG.add(hinge);
    });
    lidG.userData={closedY:0,explodedY:2.0*spread,name:'LCD/OLED Lid + Webcam',id:'c6'};
    phoneModelGroup.add(lidG); layers.push(lidG);
}

// ═══════════════════════════════════════════════════════
// 🖥️ DESKTOP / TOWER 3D MODEL
// ═══════════════════════════════════════════════════════
function buildDesktopLayers() {
    layers = []; screws = [];
    var tW=2.2, tH=4.5, spread=1.6;

    // Layer 0: Side Panel (tempered glass / steel)
    var panG=new THREE.Group();
    panG.add(new THREE.Mesh(new THREE.BoxGeometry(tW,tH,0.06),new THREE.MeshPhysicalMaterial({color:0x0A0A10,transmission:0.75,roughness:0.04,ior:1.52,thickness:0.1})));
    panG.userData={closedY:0,explodedY:-3.8*spread,name:'Tempered Glass Side Panel',id:'c1'};
    phoneModelGroup.add(panG); layers.push(panG);

    // Layer 1: Power Supply
    var psuG=new THREE.Group();
    psuG.add(new THREE.Mesh(new THREE.BoxGeometry(tW*0.85,1.0,1.8),new THREE.MeshStandardMaterial({color:0x1A1A20,metalness:0.8})));
    var psuFan=new THREE.Mesh(new THREE.CylinderGeometry(0.36,0.36,0.05,24),new THREE.MeshStandardMaterial({color:0x2A2A30,metalness:0.6}));
    psuFan.rotation.x=Math.PI/2; psuFan.position.set(0,0,0.93); psuG.add(psuFan);
    psuG.position.set(0,-tH*0.36,0);
    psuG.userData={closedY:0,explodedY:-2.8*spread,name:'650W Power Supply Unit',id:'c4'};
    phoneModelGroup.add(psuG); layers.push(psuG);

    // Layer 2: HDD/SSD Cage
    var hddG=new THREE.Group();
    hddG.add(new THREE.Mesh(new THREE.BoxGeometry(tW*0.7,0.4,1.5),new THREE.MeshStandardMaterial({color:0x0A0E14,metalness:0.7})));
    var platLabel=new THREE.Mesh(new THREE.BoxGeometry(0.8,0.3,0.02),new THREE.MeshStandardMaterial({color:0x101838,metalness:0.3}));
    platLabel.position.z=0.76; hddG.add(platLabel);
    hddG.position.set(0,-tH*0.12,0);
    hddG.userData={closedY:0,explodedY:-1.8*spread,name:'NVMe SSD + HDD Drive Bay',id:'c3'};
    phoneModelGroup.add(hddG); layers.push(hddG);

    // Layer 3: Mainboard (ATX)
    var pcbTex=createPCBTexture();
    var mbG=new THREE.Group();
    mbG.add(new THREE.Mesh(new THREE.BoxGeometry(tW*0.95,tH*0.62,0.06),new THREE.MeshStandardMaterial({map:pcbTex,roughness:0.28,metalness:0.4})));
    // CPU + heatsink
    var cpu=new THREE.Mesh(new THREE.BoxGeometry(0.6,0.6,0.08),new THREE.MeshStandardMaterial({color:0xA0A4A8,metalness:0.99,roughness:0.06}));
    cpu.position.set(-0.3,0.8,0.06); mbG.add(cpu);
    var heatsink=new THREE.Mesh(new THREE.CylinderGeometry(0.55,0.55,0.9,8,1,false),new THREE.MeshStandardMaterial({color:0xC8CACE,metalness:0.88,roughness:0.25}));
    heatsink.rotation.x=Math.PI/2; heatsink.position.set(-0.3,0.8,0.5); mbG.add(heatsink);
    // RAM slots × 4
    for(var rm=0;rm<4;rm++){
        var rs=new THREE.Mesh(new THREE.BoxGeometry(0.12,1.4,0.05),new THREE.MeshStandardMaterial({color:0x1A1E24}));
        rs.position.set(0.45+rm*0.2,0.5,0.05); mbG.add(rs);
    }
    // GPU slot indicator
    var gpuSlot=new THREE.Mesh(new THREE.BoxGeometry(tW*0.88,0.12,0.04),new THREE.MeshStandardMaterial({color:0x22293A}));
    gpuSlot.position.set(0,-0.6,0.05); mbG.add(gpuSlot);
    mbG.userData={closedY:0,explodedY:-0.6*spread,name:'ATX Motherboard',id:'c5'};
    phoneModelGroup.add(mbG); layers.push(mbG);

    // Layer 4: GPU (Graphics Card)
    var gpuG=new THREE.Group();
    gpuG.add(new THREE.Mesh(new THREE.BoxGeometry(tW*0.88,0.85,0.5),new THREE.MeshStandardMaterial({color:0x101418,metalness:0.8})));
    // GPU fans × 2
    [-0.6,0.55].forEach(function(gx){
        var gf=new THREE.Mesh(new THREE.CylinderGeometry(0.32,0.32,0.04,20),new THREE.MeshStandardMaterial({color:0x22262E,metalness:0.6}));
        gf.rotation.x=Math.PI/2; gf.position.set(gx,0,0.28); gpuG.add(gf);
    });
    gpuG.position.set(0,-0.6,0.3);
    gpuG.userData={closedY:0,explodedY:0.7*spread,name:'Discrete GPU (Graphics Card)',id:'c6'};
    phoneModelGroup.add(gpuG); layers.push(gpuG);

    // Layer 5: Outer Tower Chassis
    var caseG=new THREE.Group();
    caseG.add(new THREE.Mesh(new THREE.BoxGeometry(tW,tH,0.06),new THREE.MeshStandardMaterial({color:0x1E2025,metalness:0.7,roughness:0.3})));
    caseG.userData={closedY:0,explodedY:2.2*spread,name:'Steel Tower Chassis',id:'c8'};
    phoneModelGroup.add(caseG); layers.push(caseG);
}

// ═══════════════════════════════════════════════════════
// 📱 TABLET 3D MODEL
// ═══════════════════════════════════════════════════════
function buildTabletLayers() {
    layers = []; screws = [];
    var tW=3.8, tH=5.2, spread=1.4;

    function rBox(w,h,d,r){
        return new THREE.BoxGeometry(w, h, d);
    }

    // Back cover (aluminum)
    var backG=new THREE.Group();
    backG.add(new THREE.Mesh(rBox(tW,tH,0.07,0.3),new THREE.MeshStandardMaterial({color:0xC8CBCF,metalness:0.96,roughness:0.15})));
    // Camera bump
    var camBump=new THREE.Mesh(new THREE.CylinderGeometry(0.22,0.22,0.04,24),new THREE.MeshStandardMaterial({color:0x0A0A0F,metalness:0.8}));
    camBump.rotation.x=Math.PI/2; camBump.position.set(tW*0.36,tH*0.42,0.055); backG.add(camBump);
    backG.userData={closedY:0,explodedY:-3.2*spread,name:'Aluminum Back Cover',id:'c1'};
    phoneModelGroup.add(backG); layers.push(backG);

    // Battery (large tablet cell)
    var battG=new THREE.Group();
    battG.add(new THREE.Mesh(rBox(tW*0.86,tH*0.55,0.09,0.15),new THREE.MeshStandardMaterial({color:0x0E1420,roughness:0.4})));
    battG.userData={closedY:0,explodedY:-2.0*spread,name:'10,000mAh Li-Poly Battery',id:'c4'};
    phoneModelGroup.add(battG); layers.push(battG);

    // PCB (tablet SoC)
    var pcbTex=createPCBTexture();
    var pcbG=new THREE.Group();
    pcbG.add(new THREE.Mesh(rBox(tW*0.72,tH*0.35,0.05,0.1),new THREE.MeshStandardMaterial({map:pcbTex,roughness:0.3,metalness:0.35})));
    var emi=new THREE.Mesh(new THREE.BoxGeometry(0.9,0.75,0.06),new THREE.MeshStandardMaterial({color:0xD5D8DC,metalness:0.95,roughness:0.18}));
    emi.position.set(0,0.1,0.04); pcbG.add(emi);
    pcbG.position.set(0,tH*0.28,0);
    pcbG.userData={closedY:0,explodedY:-0.8*spread,name:'SoC Mainboard',id:'c5'};
    phoneModelGroup.add(pcbG); layers.push(pcbG);

    // LCD/OLED Display
    var dispG=new THREE.Group();
    dispG.add(new THREE.Mesh(rBox(tW*0.96,tH*0.97,0.04,0.28),new THREE.MeshStandardMaterial({color:0x030408,roughness:0.06,metalness:0.9})));
    dispG.userData={closedY:0,explodedY:0.8*spread,name:'LCD/OLED Display Panel',id:'c6'};
    phoneModelGroup.add(dispG); layers.push(dispG);

    // Front Glass
    var glassG=new THREE.Group();
    glassG.add(new THREE.Mesh(rBox(tW*0.985,tH*0.985,0.024,0.3),new THREE.MeshPhysicalMaterial({color:0x04070E,transmission:0.9,roughness:0.015,ior:1.52,thickness:0.12})));
    glassG.userData={closedY:0,explodedY:2.0*spread,name:'Gorilla Glass Front',id:'c8'};
    phoneModelGroup.add(glassG); layers.push(glassG);
}

// ═══════════════════════════════════════════════════════
// 📺 TV / MONITOR 3D MODEL
// ═══════════════════════════════════════════════════════
function buildTVLayers() {
    layers = []; screws = [];
    var tW=7.5, tH=4.5, spread=1.8;

    // Back housing
    var backG=new THREE.Group();
    backG.add(new THREE.Mesh(new THREE.BoxGeometry(tW,tH,0.14),new THREE.MeshStandardMaterial({color:0x111318,roughness:0.4,metalness:0.3})));
    // Vents
    for(var v=-1.8;v<=1.8;v+=0.25){
        var vent=new THREE.Mesh(new THREE.BoxGeometry(2.2,0.06,0.02),new THREE.MeshBasicMaterial({color:0x222226}));
        vent.position.set(2.5,v,-0.08); backG.add(vent);
    }
    // Stand
    var stand=new THREE.Mesh(new THREE.BoxGeometry(0.18,1.2,0.16),new THREE.MeshStandardMaterial({color:0x1A1C20,metalness:0.5}));
    stand.position.set(0,-tH*0.6,0); backG.add(stand);
    var base=new THREE.Mesh(new THREE.BoxGeometry(2.2,0.12,0.9),new THREE.MeshStandardMaterial({color:0x1A1C20,metalness:0.5}));
    base.position.set(0,-tH*0.7,0.35); backG.add(base);
    backG.userData={closedY:0,explodedY:-3.8*spread,name:'Back Housing + Stand',id:'c1'};
    phoneModelGroup.add(backG); layers.push(backG);

    // PSU Board
    var psuG=new THREE.Group();
    psuG.add(new THREE.Mesh(new THREE.BoxGeometry(tW*0.4,tH*0.7,0.04),new THREE.MeshStandardMaterial({color:0x0C1218,roughness:0.5})));
    psuG.position.set(-tW*0.28,0,0);
    psuG.userData={closedY:0,explodedY:-2.6*spread,name:'Power Supply Board',id:'c4'};
    phoneModelGroup.add(psuG); layers.push(psuG);

    // Main Logic Board (T-Con + SMPS)
    var pcbTex=createPCBTexture();
    var mbG=new THREE.Group();
    mbG.add(new THREE.Mesh(new THREE.BoxGeometry(tW*0.48,tH*0.55,0.04),new THREE.MeshStandardMaterial({map:pcbTex,roughness:0.3,metalness:0.35})));
    mbG.position.set(tW*0.18,0,0);
    mbG.userData={closedY:0,explodedY:-1.4*spread,name:'Main Logic + T-Con Board',id:'c5'};
    phoneModelGroup.add(mbG); layers.push(mbG);

    // LED Backlight Strip
    var blG=new THREE.Group();
    for(var bl=0;bl<9;bl++){
        var strip=new THREE.Mesh(new THREE.BoxGeometry(tW*0.9,0.08,0.01),new THREE.MeshStandardMaterial({color:0xFFFFE8,emissive:0xFFFFCC,emissiveIntensity:0.7}));
        strip.position.set(0,-tH*0.38+bl*0.46,-0.02); blG.add(strip);
    }
    blG.userData={closedY:0,explodedY:-0.3*spread,name:'LED Backlight Array',id:'c3'};
    phoneModelGroup.add(blG); layers.push(blG);

    // LCD Panel
    var lcdG=new THREE.Group();
    lcdG.add(new THREE.Mesh(new THREE.BoxGeometry(tW*0.97,tH*0.97,0.04),new THREE.MeshStandardMaterial({color:0x020305,roughness:0.04,metalness:0.92})));
    lcdG.userData={closedY:0,explodedY:1.0*spread,name:'IPS/OLED Display Panel',id:'c6'};
    phoneModelGroup.add(lcdG); layers.push(lcdG);

    // Bezel + Front Cover
    var bezG=new THREE.Group();
    var outer=new THREE.Mesh(new THREE.BoxGeometry(tW,tH,0.04),new THREE.MeshStandardMaterial({color:0x0A0C10,roughness:0.3}));
    bezG.add(outer);
    bezG.userData={closedY:0,explodedY:2.5*spread,name:'Front Bezel Frame',id:'c8'};
    phoneModelGroup.add(bezG); layers.push(bezG);
}

// ═══════════════════════════════════════════════════════
// 🔋 BATTERY PACK 3D MODEL
// ═══════════════════════════════════════════════════════
function buildBatteryPackLayers() {
    layers = []; screws = [];
    var spread=1.6;

    // Outer shell
    var shellG=new THREE.Group();
    shellG.add(new THREE.Mesh(new THREE.BoxGeometry(3.0,1.5,4.8),new THREE.MeshStandardMaterial({color:0x101418,roughness:0.35,metalness:0.25})));
    shellG.userData={closedY:0,explodedY:-3.2*spread,name:'ABS Outer Shell',id:'c1'};
    phoneModelGroup.add(shellG); layers.push(shellG);

    // BMS PCB (Battery Management System)
    var pcbTex=createPCBTexture();
    var bmsG=new THREE.Group();
    bmsG.add(new THREE.Mesh(new THREE.BoxGeometry(2.4,0.28,4.4),new THREE.MeshStandardMaterial({map:pcbTex,roughness:0.3,metalness:0.4})));
    var mosfet=new THREE.Mesh(new THREE.BoxGeometry(0.25,0.14,0.2),new THREE.MeshStandardMaterial({color:0x0A0E14,metalness:0.7}));
    mosfet.position.set(0.8,0.22,0.9); bmsG.add(mosfet);
    bmsG.userData={closedY:0,explodedY:-1.6*spread,name:'Battery Management System (BMS)',id:'c5'};
    phoneModelGroup.add(bmsG); layers.push(bmsG);

    // Li-ion cells (cylindrical 18650)
    var cellsG=new THREE.Group();
    var cellMat=new THREE.MeshStandardMaterial({color:0x1A2890,metalness:0.6,roughness:0.3});
    var posArr=[[-0.75,-0.6],[0,-0.6],[0.75,-0.6],[-0.75,0.0],[0,0.0],[0.75,0.0],[-0.75,0.6],[0,0.6],[0.75,0.6]];
    posArr.forEach(function(p){
        var cell=new THREE.Mesh(new THREE.CylinderGeometry(0.3,0.3,4.2,16),new THREE.MeshStandardMaterial({color:0x1A2490,metalness:0.55,roughness:0.32}));
        cell.rotation.x=Math.PI/2; cell.position.set(p[0],p[1],0); cellsG.add(cell);
        var cap=new THREE.Mesh(new THREE.CylinderGeometry(0.12,0.12,0.05,12),new THREE.MeshStandardMaterial({color:0xC0C0C0,metalness:0.99}));
        cap.rotation.x=Math.PI/2; cap.position.set(p[0],p[1],2.13); cellsG.add(cap);
    });
    cellsG.userData={closedY:0,explodedY:0.4*spread,name:'18650 Li-Ion Cells (×9)',id:'c4'};
    phoneModelGroup.add(cellsG); layers.push(cellsG);

    // Nickel strips / interconnects
    var nickelG=new THREE.Group();
    for(var ns=-0.75;ns<=0.75;ns+=0.75){
        var strip=new THREE.Mesh(new THREE.BoxGeometry(2.2,0.07,0.08),new THREE.MeshStandardMaterial({color:0xC8D0D4,metalness:0.98,roughness:0.08}));
        strip.position.set(0,ns,2.15); nickelG.add(strip);
    }
    nickelG.userData={closedY:0,explodedY:2.0*spread,name:'Nickel Cell Interconnects',id:'c3'};
    phoneModelGroup.add(nickelG); layers.push(nickelG);
}

// ═══════════════════════════════════════════════════════
// 🔌 PCB / CIRCUIT BOARD 3D MODEL
// ═══════════════════════════════════════════════════════
function buildPCBLayers() {
    layers = []; screws = [];
    var pW=5.0, pH=3.8, spread=1.5;
    var pcbTex=createPCBTexture();

    // Base PCB board (green FR4)
    var boardG=new THREE.Group();
    boardG.add(new THREE.Mesh(new THREE.BoxGeometry(pW,pH,0.07),new THREE.MeshStandardMaterial({map:pcbTex,roughness:0.28,metalness:0.38})));
    // Gold fingers (edge connector)
    for(var gf=0;gf<18;gf++){
        var finger=new THREE.Mesh(new THREE.BoxGeometry(0.06,0.28,0.01),new THREE.MeshStandardMaterial({color:0xD4AF37,metalness:0.99,roughness:0.04}));
        finger.position.set(-pW*0.44+gf*0.26,-pH*0.49,0.04); boardG.add(finger);
    }
    boardG.userData={closedY:0,explodedY:-3.0*spread,name:'FR4 PCB Substrate',id:'c1'};
    phoneModelGroup.add(boardG); layers.push(boardG);

    // SMD components layer
    var smdG=new THREE.Group();
    // IC chips
    [[0.8,0.6,0.9,0.75],[- 1.2,0.2,0.7,0.55],[-0.2,-0.8,0.55,0.45],[1.5,-0.5,0.4,0.35]].forEach(function(c){
        var chip=new THREE.Mesh(new THREE.BoxGeometry(c[2],c[3],0.06),new THREE.MeshStandardMaterial({color:0x0A0C10,metalness:0.7,roughness:0.4}));
        chip.position.set(c[0],c[1],0.075); smdG.add(chip);
        // Gold leads
        for(var l=0;l<8;l++){
            var lead=new THREE.Mesh(new THREE.BoxGeometry(0.04,0.04,0.01),new THREE.MeshStandardMaterial({color:0xD4AF37,metalness:0.99}));
            lead.position.set(c[0]-c[2]/2+l*(c[2]/7),c[1]-c[3]/2-0.025,0.075); smdG.add(lead);
        }
    });
    // Capacitors (cylindrical)
    [[0.2,1.1],[- 0.6,0.8],[1.8,0.3],[-2.0,0.6]].forEach(function(cp){
        var cap=new THREE.Mesh(new THREE.CylinderGeometry(0.1,0.1,0.22,12),new THREE.MeshStandardMaterial({color:0x181A60,roughness:0.5}));
        cap.rotation.x=Math.PI/2; cap.position.set(cp[0],cp[1],0.16); smdG.add(cap);
    });
    // Resistors
    for(var r=0;r<12;r++){
        var res=new THREE.Mesh(new THREE.BoxGeometry(0.12,0.06,0.04),new THREE.MeshStandardMaterial({color:0x4A3820,roughness:0.8}));
        res.position.set(-pW*0.3+r*0.35,pH*0.3+Math.random()*0.3,0.075); smdG.add(res);
    }
    smdG.userData={closedY:0,explodedY:-1.5*spread,name:'SMD ICs, Capacitors & Resistors',id:'c5'};
    phoneModelGroup.add(smdG); layers.push(smdG);

    // Copper trace layer (visible underside)
    var traceG=new THREE.Group();
    for(var t=0;t<8;t++){
        var trace=new THREE.Mesh(new THREE.BoxGeometry(0.04,pH*0.85,0.01),new THREE.MeshStandardMaterial({color:0xC06010,metalness:0.96,roughness:0.15}));
        trace.position.set(-pW*0.35+t*0.55,0,-0.04); traceG.add(trace);
    }
    for(var th=0;th<6;th++){
        var htrace=new THREE.Mesh(new THREE.BoxGeometry(pW*0.85,0.04,0.01),new THREE.MeshStandardMaterial({color:0xC06010,metalness:0.96,roughness:0.15}));
        htrace.position.set(0,-pH*0.32+th*0.45,-0.04); traceG.add(htrace);
    }
    traceG.userData={closedY:0,explodedY:0.5*spread,name:'Copper Trace Network',id:'c3'};
    phoneModelGroup.add(traceG); layers.push(traceG);

    // Solder mask + silkscreen top
    var maskG=new THREE.Group();
    maskG.add(new THREE.Mesh(new THREE.BoxGeometry(pW,pH,0.008),new THREE.MeshStandardMaterial({color:0x1A6620,roughness:0.5,transparent:true,opacity:0.85})));
    maskG.userData={closedY:0,explodedY:2.0*spread,name:'Solder Mask + Silkscreen',id:'c6'};
    phoneModelGroup.add(maskG); layers.push(maskG);
}
</script>
</body>
</html>'''
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
    html = html.replace("__SHAPE_TYPE__", shape_type)
    return html

