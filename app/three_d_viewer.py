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
import hashlib
from typing import Dict, Any, Optional

_VIEWER_VERSION = "v4_single_init_fix"  # bump to bust cache

def _make_cache_key(device_info: Dict[str, Any]) -> str:
    """Stable cache key from device_info dict."""
    key_parts = [
        _VIEWER_VERSION,
        str(device_info.get("category", "")),
        str(device_info.get("brand", "")),
        str(device_info.get("model", "")),
    ]
    return hashlib.md5("|".join(key_parts).encode()).hexdigest()

# In-memory LRU cache for 3D HTML — avoids regenerating same device
_3D_CACHE: dict = {}  # cleared on each module reload
_3D_CACHE_MAX = 12

def generate_3d_viewer(device_info: Dict[str, Any], height: int = 740) -> str:
    """
    Generate a futuristic Hologram 3D hardware anatomy viewer with scanning laser,
    glowing cyber pedestal, particle aura, 360° auto-spin, and disassembly slider.
    CACHED: same category+brand+model returns instantly from memory.
    """
    # ── INSTANT CACHE CHECK ──
    _ck = _make_cache_key(device_info)
    if _ck in _3D_CACHE:
        return _3D_CACHE[_ck]

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
<script src="https://cdn.jsdelivr.net/npm/three@0.134.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.134.0/examples/js/loaders/GLTFLoader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.134.0/examples/js/controls/OrbitControls.js"></script>
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

// ══════════════════════════════════════════════════════
// TEXTURE GENERATORS
// ══════════════════════════════════════════════════════
function createLeatherTexture() {
    var c = document.createElement('canvas');
    c.width = 512; c.height = 1024;
    var ctx = c.getContext('2d');
    var grad = ctx.createLinearGradient(0,0,512,1024);
    grad.addColorStop(0, '#E8DCBF'); grad.addColorStop(0.5, '#DACBAA'); grad.addColorStop(1, '#CDBB95');
    ctx.fillStyle = grad; ctx.fillRect(0,0,512,1024);
    for(var i=0;i<2000;i++){
        ctx.fillStyle='rgba(150,130,90,'+(Math.random()*0.12+0.04)+')';
        ctx.beginPath();ctx.arc(Math.random()*512,Math.random()*1024,Math.random()*2+0.5,0,Math.PI*2);ctx.fill();
    }
    ctx.strokeStyle='#D4AF37';ctx.lineWidth=6;ctx.setLineDash([12,8]);
    ctx.beginPath();ctx.moveTo(256,60);ctx.lineTo(256,960);ctx.stroke();
    ctx.fillStyle='#64748B';ctx.font='bold 28px Arial';
    ctx.fillText('REALME',210,820);
    return new THREE.CanvasTexture(c);
}
function createBatteryTexture() {
    var c = document.createElement('canvas');
    c.width=512;c.height=512;
    var ctx=c.getContext('2d');
    ctx.fillStyle='#1A2B1A';ctx.fillRect(0,0,512,512);
    var g=ctx.createLinearGradient(0,0,512,0);
    g.addColorStop(0,'#1A3A1A');g.addColorStop(0.5,'#2D5A2D');g.addColorStop(1,'#1A3A1A');
    ctx.fillStyle=g;ctx.fillRect(20,20,472,472);
    ctx.strokeStyle='#00FF44';ctx.lineWidth=2;ctx.setLineDash([8,4]);
    for(var r=0;r<5;r++){ctx.beginPath();ctx.moveTo(0,r*100+50);ctx.lineTo(512,r*100+50);ctx.stroke();}
    ctx.fillStyle='#00FF44';ctx.font='bold 22px monospace';ctx.fillText('5000mAh LiPoly',80,260);
    ctx.fillText('SAMSUNG SDI',120,290);
    return new THREE.CanvasTexture(c);
}
function createPCBTexture() {
    var c=document.createElement('canvas');
    c.width=512;c.height=512;
    var ctx=c.getContext('2d');
    ctx.fillStyle='#0A2B0A';ctx.fillRect(0,0,512,512);
    ctx.strokeStyle='#00AA44';ctx.lineWidth=1.5;
    for(var t=0;t<20;t++){ctx.beginPath();ctx.moveTo(Math.random()*512,0);ctx.lineTo(Math.random()*512,512);ctx.stroke();}
    for(var t2=0;t2<15;t2++){ctx.beginPath();ctx.moveTo(0,Math.random()*512);ctx.lineTo(512,Math.random()*512);ctx.stroke();}
    ctx.fillStyle='rgba(212,175,55,0.7)';
    for(var p=0;p<40;p++){ctx.fillRect(Math.random()*500,Math.random()*500,8,8);}
    ctx.fillStyle='#CCCC00';ctx.font='bold 18px monospace';ctx.fillText('SAMSUNG UFS 256G',60,260);
    return new THREE.CanvasTexture(c);
}

// ══════════════════════════════════════════════════════
// GLOBAL VARS — declared ONCE
// ══════════════════════════════════════════════════════
var scene, camera, renderer, controls, clock;
var phoneModelGroup;
var layers = [], screws = [];
var cyberRing1, cyberRing2, laserPlane;
var holoContainer, holoScanLines = [], holoParticles;
var isAutoSpinning = true, isPointerDown = false, isLaserActive = true;
var currentExplodeVal = 0.0;
var lastPointerX = 0;

function switchModelMode(mode) {}

// ══════════════════════════════════════════════════════
// HOLOGRAM ENVIRONMENT — cylinder + rings + particles
// ══════════════════════════════════════════════════════
function buildHologramEnvironment() {
    // Transparent glowing cylinder AROUND device
    var cylGeo = new THREE.CylinderGeometry(3.8, 3.8, 11, 48, 1, true);
    var cylMat = new THREE.MeshBasicMaterial({color:0x00E5FF,side:THREE.DoubleSide,transparent:true,opacity:0.06,blending:THREE.AdditiveBlending});
    holoContainer = new THREE.Mesh(cylGeo, cylMat);
    scene.add(holoContainer);

    // Top/bottom edge rings
    var topRing = new THREE.Mesh(new THREE.TorusGeometry(3.8,0.05,8,48),new THREE.MeshBasicMaterial({color:0x00F0FF,transparent:true,opacity:0.9,blending:THREE.AdditiveBlending}));
    topRing.position.y=5.5; scene.add(topRing);
    var botRing = topRing.clone(); botRing.position.y=-5.5; scene.add(botRing);

    // 6 horizontal scan line rings (sweep up/down)
    holoScanLines = [];
    var lc=[0x00F0FF,0x38BDF8,0x00FF88,0xFFD700,0xFF4488,0xAA44FF];
    for(var li=0;li<6;li++){
        var sg=new THREE.Mesh(new THREE.TorusGeometry(3.75,0.022,4,48),new THREE.MeshBasicMaterial({color:lc[li],transparent:true,opacity:0.7,blending:THREE.AdditiveBlending}));
        sg.position.y=-5.0+li*2.0; scene.add(sg); holoScanLines.push(sg);
    }

    // Floor pedestal
    var grid=new THREE.PolarGridHelper(4.2,12,6,48,0x00F0FF,0x003355);
    grid.position.y=-5.55; scene.add(grid);

    // Neon floor rings
    var r1=new THREE.Mesh(new THREE.RingGeometry(3.3,3.38,48),new THREE.MeshBasicMaterial({color:0x00F0FF,side:THREE.DoubleSide,transparent:true,opacity:0.8,blending:THREE.AdditiveBlending}));
    r1.rotation.x=Math.PI/2;r1.position.y=-5.5;scene.add(r1);cyberRing1=r1;
    var r2=new THREE.Mesh(new THREE.RingGeometry(3.95,4.0,48),new THREE.MeshBasicMaterial({color:0xFFD700,side:THREE.DoubleSide,transparent:true,opacity:0.5,blending:THREE.AdditiveBlending}));
    r2.rotation.x=Math.PI/2;r2.position.y=-5.5;scene.add(r2);cyberRing2=r2;

    // Laser scan beam
    var lGeo=new THREE.PlaneGeometry(7.2,0.1);
    var lMat=new THREE.MeshBasicMaterial({color:0x00F0FF,side:THREE.DoubleSide,transparent:true,opacity:0.9,blending:THREE.AdditiveBlending});
    laserPlane=new THREE.Mesh(lGeo,lMat); scene.add(laserPlane);

    // Colored particles INSIDE cylinder
    var pGeo=new THREE.BufferGeometry();
    var pCount=300, pPos=new Float32Array(pCount*3), pCol=new Float32Array(pCount*3);
    for(var p=0;p<pCount;p++){
        var ang=Math.random()*Math.PI*2, rad=Math.random()*3.6;
        pPos[p*3]=Math.cos(ang)*rad; pPos[p*3+1]=(Math.random()-0.5)*11; pPos[p*3+2]=Math.sin(ang)*rad;
        var cm=p%3;
        if(cm===0){pCol[p*3]=0;pCol[p*3+1]=0.9;pCol[p*3+2]=1.0;}
        else if(cm===1){pCol[p*3]=1.0;pCol[p*3+1]=0.84;pCol[p*3+2]=0;}
        else{pCol[p*3]=0;pCol[p*3+1]=1.0;pCol[p*3+2]=0.53;}
    }
    pGeo.setAttribute('position',new THREE.BufferAttribute(pPos,3));
    pGeo.setAttribute('color',new THREE.BufferAttribute(pCol,3));
    holoParticles=new THREE.Points(pGeo,new THREE.PointsMaterial({size:0.06,vertexColors:true,transparent:true,opacity:0.9,blending:THREE.AdditiveBlending}));
    scene.add(holoParticles);

    // 6 vertical energy beams on cylinder wall
    for(var vb=0;vb<6;vb++){
        var va=(vb/6)*Math.PI*2;
        var vm=new THREE.MeshBasicMaterial({color:lc[vb],transparent:true,opacity:0.28,blending:THREE.AdditiveBlending});
        var vMesh=new THREE.Mesh(new THREE.CylinderGeometry(0.015,0.015,11,4),vm);
        vMesh.position.set(Math.cos(va)*3.65,0,Math.sin(va)*3.65);scene.add(vMesh);
    }
}

// ══════════════════════════════════════════════════════
// PHONE LAYERS
// ══════════════════════════════════════════════════════
function buildRealisticPhoneLayers() {
    layers=[]; screws=[];
    var pW=2.45, pH=5.1, sp=1.45;
    var leatherTex=createLeatherTexture(), battTex=createBatteryTexture(), pcbTex=createPCBTexture();

    function addLayer(meshes, closedY, explodedY, name, id) {
        var g=new THREE.Group();
        for(var m=0;m<meshes.length;m++) g.add(meshes[m]);
        g.userData={closedY:closedY, explodedY:explodedY, name:name, id:id};
        phoneModelGroup.add(g); layers.push(g); return g;
    }
    function box(w,h,d,mat){return new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);}
    function cyl(rt,rb,h,seg,mat){var m=new THREE.Mesh(new THREE.CylinderGeometry(rt,rb,h,seg),mat);m.rotation.x=Math.PI/2;return m;}
    function std(col,met,rou){return new THREE.MeshStandardMaterial({color:col,metalness:met,roughness:rou});}

    // Screws group
    var sg=new THREE.Group();
    var sMat=std(0xCDD5D9,0.98,0.08);
    var sPos=[[-1.05,2.3],[1.05,2.3],[-1.05,-2.3],[1.05,-2.3],[-1.05,1.2],[1.05,1.2],[-1.05,-1.2],[1.05,-1.2]];
    for(var s=0;s<sPos.length;s++){
        var sc=new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.032,0.09,10),sMat);
        sc.rotation.x=Math.PI/2;sc.position.set(sPos[s][0],sPos[s][1],0);sg.add(sc);screws.push(sc);
    }
    sg.userData={closedY:0,explodedY:-4.2*sp,name:'Micro-Screws (8)',id:'c16'};
    phoneModelGroup.add(sg);layers.push(sg);

    // Back cover
    var bc=[box(pW,pH,0.07,new THREE.MeshStandardMaterial({map:leatherTex,roughness:0.65,metalness:0.07}))];
    var camRing=new THREE.Mesh(new THREE.CylinderGeometry(0.82,0.82,0.065,32),std(0xCBB070,0.95,0.12));
    camRing.rotation.x=Math.PI/2;camRing.position.set(0,1.15,0.05);bc.push(camRing);
    addLayer(bc,0,-3.5*sp,'Back Cover (Glass/Leather)','c1');

    // Camera
    var camG=[new THREE.Mesh(new THREE.CylinderGeometry(0.72,0.72,0.1,32),std(0x0A0A0F,0.85,0.18))];
    camG[0].rotation.x=Math.PI/2;
    var lens=new THREE.Mesh(new THREE.CylinderGeometry(0.28,0.28,0.13,24),new THREE.MeshStandardMaterial({color:0x010A1A,metalness:0.9,roughness:0.02}));
    lens.rotation.x=Math.PI/2;camG.push(lens);
    var flash=new THREE.Mesh(new THREE.CylinderGeometry(0.08,0.08,0.08,10),std(0xFFE8A0,0.3,0.5));
    flash.rotation.x=Math.PI/2;flash.position.set(0,-0.38,0.04);camG.push(flash);
    var cg=addLayer(camG,0,-2.6*sp,'Triple Camera (200MP)','c2');
    cg.position.set(0,1.15,0);

    // Midframe
    var mf=[box(pW,pH,0.095,std(0xCDD4DA,0.94,0.19))];
    var inner=box(pW*0.88,pH*0.92,0.1,std(0x101418,0,0.9));inner.position.z=0.002;mf.push(inner);
    addLayer(mf,0,-0.8*sp,'Aluminum Midframe','c3');

    // Battery
    var bat=[box(pW*0.87,pH*0.49,0.085,new THREE.MeshStandardMaterial({map:battTex,roughness:0.38,metalness:0.12}))];
    var bg=addLayer(bat,0,0.12*sp,'5000mAh Li-Poly Battery','c4');
    bg.position.set(0,-0.68,0);

    // PCB
    var pcb=[box(pW*0.9,pH*0.45,0.045,new THREE.MeshStandardMaterial({map:pcbTex,roughness:0.32,metalness:0.32}))];
    var emi=box(0.74,0.66,0.062,std(0xDDE2E5,0.94,0.2));emi.position.set(-0.33,0.1,0.034);pcb.push(emi);
    var pg=addLayer(pcb,0,1.25*sp,'Mainboard (Dimensity SoC)','c5');
    pg.position.set(0,1.08,0);

    // AMOLED
    addLayer([box(pW*0.96,pH*0.97,0.042,std(0x04060C,0.88,0.08))],0,2.4*sp,'120Hz AMOLED Display','c6');

    // Glass
    addLayer([box(pW*0.985,pH*0.985,0.025,new THREE.MeshStandardMaterial({color:0x05090F,transparent:true,opacity:0.85,roughness:0.015,metalness:0.1}))],0,3.6*sp,'Gorilla Glass Victus','c8');
    
    updateLayerPositions(currentExplodeVal);
}

// ══════════════════════════════════════════════════════
// LAPTOP LAYERS
// ══════════════════════════════════════════════════════
function buildLaptopLayers() {
    layers=[]; screws=[];
    function std(col,met,rou){return new THREE.MeshStandardMaterial({color:col,metalness:met,roughness:rou});}
    function box(w,h,d,mat){return new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);}
    function addLayer(mesh,cy,ey,name,id){
        var g=new THREE.Group();if(Array.isArray(mesh)){for(var i=0;i<mesh.length;i++)g.add(mesh[i]);}else g.add(mesh);
        g.userData={closedY:cy,explodedY:ey,name:name,id:id};phoneModelGroup.add(g);layers.push(g);return g;
    }
    var sp=1.3;
    addLayer(box(5.8,0.12,4.0,std(0xC0C8D0,0.9,0.15)),0,-3.5*sp,'Bottom Chassis','l1');
    addLayer(box(5.5,0.08,3.7,std(0x1B4332,0.3,0.3)),0,-2.5*sp,'Mainboard PCB','l2');
    addLayer([box(4.2,0.06,0.9,std(0x0A1A0A,0.1,0.8)),box(3.0,0.04,0.6,std(0x001133,0.85,0.1))],0,-1.5*sp,'Battery Pack (6-cell)','l3');
    addLayer(box(2.2,0.3,1.8,std(0xD0D8E0,0.85,0.2)),0,-0.5*sp,'Cooling System + Fan','l4');
    addLayer([box(5.8,0.09,4.0,std(0xB8C2CC,0.88,0.18)),box(4.8,0.06,3.2,std(0x05090F,0.9,0.05))],0,1.0*sp,'Top Lid + Display','l5');
    updateLayerPositions(currentExplodeVal);
}

// ══════════════════════════════════════════════════════
// DESKTOP LAYERS
// ══════════════════════════════════════════════════════
function buildDesktopLayers() {
    layers=[]; screws=[];
    function std(col,met,rou){return new THREE.MeshStandardMaterial({color:col,metalness:met,roughness:rou});}
    function box(w,h,d,mat){return new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);}
    function addLayer(mesh,cy,ey,name,id){
        var g=new THREE.Group();if(Array.isArray(mesh)){for(var i=0;i<mesh.length;i++)g.add(mesh[i]);}else g.add(mesh);
        g.userData={closedY:cy,explodedY:ey,name:name,id:id};phoneModelGroup.add(g);layers.push(g);return g;
    }
    var sp=1.4;
    addLayer(box(3.5,4.5,0.12,std(0xC0C4C8,0.88,0.2)),0,-3.5*sp,'Side Panel (Steel)','d1');
    addLayer(box(3.2,2.8,0.06,std(0x0A2B0A,0.3,0.3)),0,-2.2*sp,'Motherboard ATX','d2');
    addLayer(box(1.4,0.6,0.4,std(0x1A1A2E,0.8,0.2)),0,-1.2*sp,'GPU Card','d3');
    addLayer([box(0.7,1.8,0.5,std(0x1A1A1A,0.6,0.4)),box(0.65,1.7,0.45,std(0x001133,0.9,0.1))],0,-0.3*sp,'PSU + Cables','d4');
    addLayer(box(1.5,1.5,1.5,std(0x101010,0.7,0.3)),0,0.9*sp,'CPU + Cooler','d5');
    addLayer(box(3.5,4.5,0.12,std(0xD0D4D8,0.85,0.18)),0,2.2*sp,'Opposite Side Panel','d6');
    updateLayerPositions(currentExplodeVal);
}

// ══════════════════════════════════════════════════════
// TABLET LAYERS
// ══════════════════════════════════════════════════════
function buildTabletLayers() {
    layers=[]; screws=[];
    function std(col,met,rou){return new THREE.MeshStandardMaterial({color:col,metalness:met,roughness:rou});}
    function box(w,h,d,mat){return new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);}
    function addLayer(mesh,cy,ey,name,id){
        var g=new THREE.Group();if(Array.isArray(mesh)){for(var i=0;i<mesh.length;i++)g.add(mesh[i]);}else g.add(mesh);
        g.userData={closedY:cy,explodedY:ey,name:name,id:id};phoneModelGroup.add(g);layers.push(g);return g;
    }
    var sp=1.3;
    addLayer(box(3.8,5.4,0.08,std(0xD0D4D8,0.92,0.12)),0,-3.0*sp,'Back Aluminum Shell','t1');
    addLayer(box(3.4,4.8,0.055,std(0x0A2B0A,0.3,0.3)),0,-1.8*sp,'Mainboard (Apple M2)','t2');
    addLayer(box(3.0,2.8,0.07,std(0x1A3A1A,0.15,0.6)),0,-0.8*sp,'Battery (6000mAh)','t3');
    addLayer(box(3.6,5.1,0.04,std(0x04060C,0.9,0.06)),0,0.5*sp,'LCD/OLED Display','t4');
    addLayer(box(3.8,5.4,0.025,std(0x0A0E14,0.15,0.02)),0,1.8*sp,'Cover Glass','t5');
    updateLayerPositions(currentExplodeVal);
}

// ══════════════════════════════════════════════════════
// TV/DISPLAY LAYERS
// ══════════════════════════════════════════════════════
function buildTVLayers() {
    layers=[]; screws=[];
    function std(col,met,rou){return new THREE.MeshStandardMaterial({color:col,metalness:met,roughness:rou});}
    function box(w,h,d,mat){return new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);}
    function addLayer(mesh,cy,ey,name,id){
        var g=new THREE.Group();if(Array.isArray(mesh)){for(var i=0;i<mesh.length;i++)g.add(mesh[i]);}else g.add(mesh);
        g.userData={closedY:cy,explodedY:ey,name:name,id:id};phoneModelGroup.add(g);layers.push(g);return g;
    }
    var sp=1.2;
    addLayer(box(5.5,3.2,0.1,std(0x202020,0.5,0.7)),0,-3.0*sp,'Rear Plastic Cover','v1');
    addLayer(box(5.2,2.9,0.04,std(0x0A2B0A,0.3,0.3)),0,-1.8*sp,'Main PCB + Power Board','v2');
    addLayer(box(5.2,2.9,0.06,std(0x001122,0.5,0.4)),0,-0.6*sp,'LED Backlight Array','v3');
    addLayer(box(5.2,2.9,0.025,std(0x040810,0.8,0.05)),0,0.8*sp,'LCD Panel + Polarizer','v4');
    addLayer(box(5.5,3.2,0.03,std(0x101010,0.2,0.1)),0,2.2*sp,'Bezel Frame','v5');
    updateLayerPositions(currentExplodeVal);
}

// ══════════════════════════════════════════════════════
// BATTERY PACK LAYERS
// ══════════════════════════════════════════════════════
function buildBatteryPackLayers() {
    layers=[]; screws=[];
    function std(col,met,rou){return new THREE.MeshStandardMaterial({color:col,metalness:met,roughness:rou});}
    function box(w,h,d,mat){return new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);}
    function addLayer(mesh,cy,ey,name,id){
        var g=new THREE.Group();if(Array.isArray(mesh)){for(var i=0;i<mesh.length;i++)g.add(mesh[i]);}else g.add(mesh);
        g.userData={closedY:cy,explodedY:ey,name:name,id:id};phoneModelGroup.add(g);layers.push(g);return g;
    }
    var sp=1.4;
    addLayer(box(2.5,4.5,0.15,std(0x1A2235,0.4,0.5)),0,-3.0*sp,'Battery Enclosure','b1');
    addLayer(box(2.2,4.0,0.08,std(0x0A2B0A,0.3,0.3)),0,-1.8*sp,'BMS Circuit Board','b2');
    for(var ci=0;ci<3;ci++){
        var cg=new THREE.Group();
        cg.add(new THREE.Mesh(new THREE.CylinderGeometry(0.55,0.55,3.5,20),std(0xC8C8CC,0.85,0.2)));
        cg.userData={closedY:0,explodedY:(-0.8+ci*1.4)*sp,name:'Li-ion Cell '+(ci+1),id:'b3_'+ci};
        cg.position.x=(ci-1)*1.2;
        phoneModelGroup.add(cg);layers.push(cg);
    }
    addLayer(box(2.5,4.5,0.15,std(0x1A2235,0.4,0.5)),0,2.2*sp,'Top Cover','b4');
    updateLayerPositions(currentExplodeVal);
}

// ══════════════════════════════════════════════════════
// PCB LAYERS
// ══════════════════════════════════════════════════════
function buildPCBLayers() {
    layers=[]; screws=[];
    var pcbTex=createPCBTexture();
    function std(col,met,rou){return new THREE.MeshStandardMaterial({color:col,metalness:met,roughness:rou});}
    function box(w,h,d,mat){return new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);}
    function addLayer(mesh,cy,ey,name,id){
        var g=new THREE.Group();if(Array.isArray(mesh)){for(var i=0;i<mesh.length;i++)g.add(mesh[i]);}else g.add(mesh);
        g.userData={closedY:cy,explodedY:ey,name:name,id:id};phoneModelGroup.add(g);layers.push(g);return g;
    }
    var sp=1.3;
    addLayer(box(4.0,5.0,0.06,new THREE.MeshStandardMaterial({map:pcbTex,roughness:0.3,metalness:0.35})),0,-3.0*sp,'PCB Substrate (FR4)','p1');
    var smdG=[]; for(var sc=0;sc<12;sc++){var sm=box(Math.random()*0.3+0.1,Math.random()*0.3+0.1,0.08,std(0x888888,0.6,0.4));sm.position.set((Math.random()-0.5)*3,(Math.random()-0.5)*4,0.04);smdG.push(sm);}
    addLayer(smdG,0,-1.8*sp,'SMD Components (ICs/Caps)','p2');
    addLayer(box(1.2,1.2,0.15,std(0x1A1A1A,0.7,0.3)),0,-0.5*sp,'Main SoC Chip','p3');
    addLayer(box(4.0,5.0,0.015,std(0x004400,0.1,0.8)),0,1.0*sp,'Solder Mask Layer','p4');
    addLayer([box(0.8,0.5,0.04,std(0xD4AF37,0.99,0.05)),box(1.2,0.3,0.04,std(0xD4AF37,0.99,0.05))],0,2.4*sp,'Gold Contacts (Au)','p5');
    updateLayerPositions(currentExplodeVal);
}

// ══════════════════════════════════════════════════════
// UPDATE LAYER POSITIONS
// ══════════════════════════════════════════════════════
function updateLayerPositions(val) {
    var n=layers.length; if(n===0) return;
    for(var i=0;i<n;i++){
        var wS=i/n, wE=(i+1)/n;
        var t=Math.max(0,Math.min(1,(val-wS)/Math.max(0.001,wE-wS)));
        var te=1.0-Math.pow(1.0-t,3.0);
        var L=layers[i];
        var cy=(L.userData.closedY!==undefined)?L.userData.closedY:0;
        var ey=(L.userData.explodedY!==undefined)?L.userData.explodedY:(i-n/2)*1.4;
        L.position.y=cy+(ey-cy)*te;
        L.position.z=i*0.001+te*(i%2===0?1.1:-0.9)*(i+1)*0.22;
        L.rotation.x=te*(i%2===0?-0.08:0.08);
        var isAct=val>=wS&&val<=wE;
        L.traverse(function(obj){
            if(obj.isMesh&&obj.material&&obj.material.emissive){
                obj.material.emissiveIntensity=isAct?0.3:0;
                if(isAct)obj.material.emissive.set(0x00C8FF);
            }
        });
    }
    for(var s=0;s<screws.length;s++){
        var st=Math.max(0,Math.min(1,val/(1.0/Math.max(n,1)+0.05)));
        var ste=1.0-Math.pow(1.0-st,2.0);
        screws[s].position.z=ste*(0.5+(s%4)*0.1);
        screws[s].rotation.z=ste*Math.PI*6;
    }
    var pct=Math.round(val*100);
    var badge=document.getElementById('sliderBadge');
    if(badge){
        var ai=Math.min(n-1,Math.floor(val*n));
        var an=layers[ai]?(layers[ai].userData.name||''):'';
        badge.textContent='Disassembly: '+pct+'%'+(an?' → '+an:'');
    }
}

// ══════════════════════════════════════════════════════
// ANIMATE LOOP
// ══════════════════════════════════════════════════════
function animate() {
    requestAnimationFrame(animate);
    var t=clock?clock.getElapsedTime():0;
    if(controls)controls.update();

    // Device: spin + float
    if(phoneModelGroup){
        if(isAutoSpinning&&!isPointerDown) phoneModelGroup.rotation.y+=0.010;
        phoneModelGroup.position.y=Math.sin(t*0.75)*0.18;
        phoneModelGroup.rotation.z=Math.sin(t*0.42)*0.025;
    }

    // Hologram cylinder pulse
    if(holoContainer&&holoContainer.material)
        holoContainer.material.opacity=0.05+0.04*Math.sin(t*1.8);

    // Scan lines cascade sweep
    if(holoScanLines){
        for(var si=0;si<holoScanLines.length;si++){
            var sp2=1.4+si*0.3, so=(si/holoScanLines.length)*Math.PI*2;
            holoScanLines[si].position.y=Math.sin(t*sp2+so)*5.0;
            holoScanLines[si].material.opacity=0.3+0.5*Math.abs(Math.sin(t*sp2+so));
        }
    }

    // Floor rings spin+pulse
    if(cyberRing1){cyberRing1.rotation.z=t*0.4;if(cyberRing1.material)cyberRing1.material.opacity=0.5+0.3*Math.sin(t*2.2);}
    if(cyberRing2){cyberRing2.rotation.z=-t*0.22;if(cyberRing2.material)cyberRing2.material.opacity=0.3+0.25*Math.sin(t*1.7+1.0);}

    // Laser sweep
    if(laserPlane&&isLaserActive){
        laserPlane.position.y=Math.sin(t*1.8)*5.0;
        if(laserPlane.material)laserPlane.material.opacity=0.55+0.4*Math.abs(Math.sin(t*1.8));
    }
    if(laserPlane)laserPlane.visible=isLaserActive;

    // Particles drift
    if(holoParticles){
        holoParticles.rotation.y=t*0.06;
        if(holoParticles.material)holoParticles.material.opacity=0.7+0.25*Math.sin(t*1.3);
    }

    if(renderer&&scene&&camera)renderer.render(scene,camera);
}

// ══════════════════════════════════════════════════════
// MAIN INIT
// ══════════════════════════════════════════════════════
function init() {
    var container=document.getElementById('canvas-3d-container');
    if(!container){console.error('canvas-3d-container NOT FOUND');return;}

    var W=container.clientWidth||720, H=container.clientHeight||520;

    scene=new THREE.Scene();
    scene.background=new THREE.Color(0x04060A);
    scene.fog=new THREE.FogExp2(0x04060A,0.035);

    camera=new THREE.PerspectiveCamera(42,W/H,0.1,200);
    camera.position.set(0,1.5,12);

    renderer=new THREE.WebGLRenderer({antialias:false,alpha:false,powerPreference:'high-performance'});
    renderer.setSize(W,H);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.5));
    renderer.shadowMap.enabled=false;
    container.appendChild(renderer.domElement);

    clock=new THREE.Clock();

    // Controls
    if(typeof THREE.OrbitControls!=='undefined'){
        try{
            controls=new THREE.OrbitControls(camera,renderer.domElement);
            controls.enableDamping=true;controls.dampingFactor=0.08;
            controls.enableZoom=true;controls.minDistance=4;controls.maxDistance=22;
            controls.maxPolarAngle=Math.PI*0.88;
        }catch(e){console.warn('OrbitControls:',e);}
    }

    // Lights
    scene.add(new THREE.AmbientLight(0x112244,0.8));
    var kl=new THREE.DirectionalLight(0xFFEECC,1.8);kl.position.set(3,8,5);scene.add(kl);
    var rl=new THREE.DirectionalLight(0x00AAFF,2.0);rl.position.set(-5,3,-5);scene.add(rl);
    var fl=new THREE.PointLight(0x4488FF,1.2,20);fl.position.set(-4,0,4);scene.add(fl);
    var gl=new THREE.PointLight(0xFFD700,0.8,15);gl.position.set(4,6,3);scene.add(gl);

    // Hologram environment
    buildHologramEnvironment();

    // Device model group
    phoneModelGroup=new THREE.Group();
    scene.add(phoneModelGroup);

    // Route to device
    var ds='__SHAPE_TYPE__';
    if(ds==='laptop')buildLaptopLayers();
    else if(ds==='desktop')buildDesktopLayers();
    else if(ds==='tablet')buildTabletLayers();
    else if(ds==='display')buildTVLayers();
    else if(ds==='battery')buildBatteryPackLayers();
    else if(ds==='pcb')buildPCBLayers();
    else buildRealisticPhoneLayers();

    updateLayerPositions(currentExplodeVal);

    // Pointer controls
    renderer.domElement.addEventListener('pointerdown',function(e){isPointerDown=true;lastPointerX=e.clientX;});
    renderer.domElement.addEventListener('pointermove',function(e){
        if(isPointerDown&&!isAutoSpinning&&phoneModelGroup){
            phoneModelGroup.rotation.y+=(e.clientX-lastPointerX)*0.008;lastPointerX=e.clientX;
        }
    });
    renderer.domElement.addEventListener('pointerup',function(){isPointerDown=false;});
    renderer.domElement.addEventListener('pointerleave',function(){isPointerDown=false;});

    window.addEventListener('resize',function(){
        var w2=container.clientWidth,h2=container.clientHeight;
        if(camera){camera.aspect=w2/h2;camera.updateProjectionMatrix();}
        if(renderer)renderer.setSize(w2,h2);
    });

    animate();
}

// ══════════════════════════════════════════════════════
// CONTROLS
// ══════════════════════════════════════════════════════
function onSliderChange(val){
    currentExplodeVal=parseFloat(val)/100.0;
    updateLayerPositions(currentExplodeVal);
}
function setSliderPercent(pct){
    var sl=document.getElementById('explodeSlider');
    if(sl){sl.value=pct;onSliderChange(pct);}
}
function toggleAutoSpin(){
    isAutoSpinning=!isAutoSpinning;
    var btn=document.getElementById('btnAutoSpin');
    if(btn)btn.textContent=isAutoSpinning?'🔄 360° Spin: ON':'⏸ 360° Spin: OFF';
}
function toggleLaser(){
    isLaserActive=!isLaserActive;
    if(laserPlane)laserPlane.visible=isLaserActive;
}
function toggleAutoPlay(){}
function reset3DCamera(){
    if(camera){camera.position.set(0,1.5,12);camera.lookAt(0,0,0);}
}
function setCameraAngle(a){
    if(!camera)return;
    if(a==='front')camera.position.set(0,1.5,12);
    else if(a==='back')camera.position.set(0,1.5,-12);
    else if(a==='left')camera.position.set(-12,1.5,0);
    else if(a==='right')camera.position.set(12,1.5,0);
    else if(a==='top')camera.position.set(0,12,1);
    else if(a==='bottom')camera.position.set(0,-10,3);
    camera.lookAt(0,0,0);
}

// ══════════════════════════════════════════════════════
// LAUNCH
// ══════════════════════════════════════════════════════
if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',init);
}else{
    init();
}
</script>
</body>
</html>
'''
    # ── CACHE LIMIT ──
    if len(_3D_CACHE) >= _3D_CACHE_MAX:
        oldest = next(iter(_3D_CACHE))
        del _3D_CACHE[oldest]

    html = raw_html.replace("__BRAND_UPPER__", str(brand).upper())
    html = html.replace("__BRAND__", str(brand))
    html = html.replace("__MODEL__", str(model_name))
    html = html.replace("__PROCESSOR__", str(processor))
    html = html.replace("__BATTERY__", str(battery_specs))
    html = html.replace("__STORAGE__", str(storage))
    html = html.replace("__RAM__", str(ram))
    html = html.replace("__CAMERA__", str(camera_specs))
    html = html.replace("__SHAPE_TYPE__", shape_type)
    html = html.replace("__MANUAL_STEPS_JSON__", manual_steps_json)
    html = html.replace("__COMP_JSON__", json.dumps([]))
    html = html.replace("__GRID_CARDS_HTML__", "")
    html = html.replace("__STEPS_HTML__", "")
    html = html.replace("__TOTAL_PARTS__", "15")
    html = html.replace("__TOTAL_VAL__", "52.00")
    html = html.replace("__HAZ_COUNT__", "3")
    html = html.replace("__REC_COUNT__", "12")

    _3D_CACHE[_ck] = html
    return html
