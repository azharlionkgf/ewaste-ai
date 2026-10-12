"""
🎨 Ultra-Realistic High-Fidelity Three.js 3D E-Waste & Precision Device Architecture Engine
=============================================================================================
Procedural & Asset-Driven 3D WebGL Engine for electronic hardware disassembly & e-waste analysis:
- Photorealistic PBR Material Shaders: Procedural Lychee Vegan Leather bump maps, gold woven seam stitching,
  concentric luxury camera halo dials, sapphire multi-coated optical glass, and gold solder pads.
- Real 3D GLB/glTF Asset Integration: Supports CC-BY-4.0 high-poly models (iPhone 15 Pro, High-Density PCB,
  Li-Po Battery pack) with graceful fallback to the precision procedural digital twin.
- ACES Filmic Tone Mapping & Multi-Point Cinematic Studio Lighting (Key, Rim, Fill, Specular).
- 7-Step Physical Disassembly Manual with micro-component extraction guidance and safety warnings.
- Interactive component inspection HUD with material mass %, scrap value ($), hazard alerts, and recyclability.
"""

import os
import json
import base64
from typing import Dict, Any, Optional

def generate_3d_viewer(device_info: Dict[str, Any], height: int = 620) -> str:
    """
    Generate an interactive ultra-realistic Three.js 3D viewer HTML for electronic devices.
    Includes procedural PBR digital twin, GLB asset loading, 7-layer physical disassembly manual,
    and micro-scale internal component inspection.
    """
    # Extract hardware metadata
    brand = device_info.get("brand", "Electronic Device")
    model_name = device_info.get("model", device_info.get("category", "Device Model"))
    category = device_info.get("category", "Electronics")
    storage = device_info.get("storage", "256 GB UFS Flash")
    ram = device_info.get("ram", "12 GB LPDDR5")
    processor = device_info.get("processor", "SoC Multi-Core Processor")
    camera_specs = device_info.get("camera", "200MP OIS High-Resolution Sensor Array")
    battery_specs = device_info.get("battery", "5000 mAh Li-Po High-Capacity Pack")
    camera_module_type = device_info.get("camera_module_type", "circular_matrix")
    has_racing_stripe = device_info.get("has_racing_stripe", True)
    
    chassis_color = device_info.get("chassis_color", "#E6D7C3")
    accent_color = device_info.get("accent_color", "#FFD700")
    frame_color = device_info.get("frame_color", "#D4AF37")
    screen_color = device_info.get("screen_color", "#080E1A")
    
    # 7-Step Physical Disassembly Manual
    manual_steps = [
        {
            "step": 1,
            "title": "1. Eject Dual-SIM Tray & Heat Rear Vegan Leather Shell",
            "tool": "0.8mm SIM Ejector Pin • Heat Mat (75°C - 80°C) • Suction Clamp",
            "action": "Insert SIM ejector pin into pinhole on lower chassis to pop tray. Place unit on 78°C heating platform for 180s to soften polyurethane hot-melt perimeter adhesive. Affix heavy-duty suction clamp to lower back panel.",
            "safety": "⚠️ Do not heat above 85°C to protect internal lithium pouch battery and AMOLED organic polymers.",
            "layer_idx": 0
        },
        {
            "step": 2,
            "title": "2. Slice Perimeter Adhesive & Remove Gold Bezel Camera Halo",
            "tool": "0.3mm Nylon Guitar Pick • Isopropyl Alcohol (IPA 99%)",
            "action": "Pry 2mm opening at bottom seam; slice around perimeter using nylon guitar pick. Carefully separate the luxury vegan leather back cover with circular gold bezel. Unclip NFC and wireless induction loop.",
            "safety": "⚠️ Insert pick maximum 3mm deep to avoid lacerating internal ribbon cables or battery casing.",
            "layer_idx": 1
        },
        {
            "step": 3,
            "title": "3. Extract 16 Precision Screws & Graphite Thermal Shield",
            "tool": "Phillips #00 Precision Screwdriver (1.4mm) • Magnetic Mat",
            "action": "Remove 16 perimeter Phillips #00 screws. Organize screws on magnetic mat by length. Gently peel back pyrolytic graphite heat dissipation shield and unfasten mid-frame antenna bracket.",
            "safety": "⚠️ Note screw placements: long screws installed into short standoff holes will pierce the logic board traces.",
            "layer_idx": 2
        },
        {
            "step": 4,
            "title": "4. ⚡ MANDATORY: Disconnect Battery Connector FIRST",
            "tool": "ESD Non-Conductive Plastic Spudger • Anti-Static Wrist Strap",
            "action": "CRITICAL FIRST ELECTRICAL PROTOCOL: Pry off the main battery BMU flex connector using a nylon spudger to cut power and prevent motherboard short-circuits. Disconnect display FPC, sub-board interconnect, and coax antennas.",
            "safety": "🚨 NEVER use metal tweezers near battery terminal pins. Static discharge can destroy micro-transistors.",
            "layer_idx": 3
        },
        {
            "step": 5,
            "title": "5. Extract Logic Motherboard & 200MP Triple Camera Module",
            "tool": "ESD Tweezers • Torx T2 Screwdriver • Thermal Paste Spatula",
            "action": "Unscrew logic board standoff screw. Gently lift the 10-layer high-Tg FR4 motherboard containing MediaTek Dimensity 7050 SoC, UFS 3.1 Flash, and Samsung HP3 200MP OIS sensor assembly.",
            "safety": "🟢 Pure gold micro-plating and silver BGA solder pads on motherboard are recovered for high-purity refining.",
            "layer_idx": 4
        },
        {
            "step": 6,
            "title": "6. Extract 5000 mAh Li-Po Battery Using Stretch Pull-Tabs",
            "tool": "Stretch Release Adhesive Tabs • 99% IPA (if tabs tear)",
            "action": "Grasp battery pull-tabs (marked A & B). Pull steadily, slowly, and completely flat along the plane of the battery at a 15° angle. If a pull tab snaps, apply 3 drops of 99% IPA around edge to dissolve adhesive and lift gently.",
            "safety": "🔥 NEVER PRY WITH SHARP TOOLS OR PUNCTURE BATTERY. Punctured lithium oxidizes violently causing thermal runaway fire.",
            "layer_idx": 5
        },
        {
            "step": 7,
            "title": "7. Separate AMOLED Display Assembly & Aerospace Aluminum Frame",
            "tool": "Curved Heated Separator • Plastic Pry Strip • Nitrile Cut Gloves",
            "action": "Unscrew lower loud-speaker box, recover USB-C 100W sub-board and X-axis tactile haptic motor. Heat front assembly and gently slice OCA adhesive to harvest the 120Hz Curved AMOLED panel and 6063 aerospace aluminum unibody frame.",
            "safety": "🧤 Aluminum frame and copper motor coils are 100% recyclable non-hazardous metallurgical scrap.",
            "layer_idx": 6
        }
    ]

    components = device_info.get("components", [])
    if not components:
        components = [
            {"name": "Vegan Leather Shell & Gold Halo Camera Ring", "material": "Polycarbonate + PU Vegan Leather + Titanium Gold Bezel", "specs": camera_specs, "weight_pct": 14.5, "hazardous": False, "recyclable": True, "value_usd": 7.50, "color": chassis_color, "layer": 1},
            {"name": "Graphite Thermal Dissipation & NFC Coil", "material": "Pyrolytic Graphite Sheet + Pure Copper Induction Loop", "specs": "0.12mm Vapor Shield Interface (13.56 MHz)", "weight_pct": 3.2, "hazardous": False, "recyclable": True, "value_usd": 1.20, "color": "#333338", "layer": 2},
            {"name": "16x Precision Screws & Antenna Shield Bracket", "material": "Austenitic Stainless Steel + Polycarbonate-ABS", "specs": "16x Phillips #00 (1.4mm & 1.8mm Torx)", "weight_pct": 2.8, "hazardous": False, "recyclable": True, "value_usd": 0.80, "color": "#7F8C8D", "layer": 3},
            {"name": "Logic Motherboard (SoC + 256GB NAND + Cameras)", "material": "10-Layer FR4 Glass Epoxy + 18k Gold Micro-Plating", "specs": f"{processor} | {ram} | {storage}", "weight_pct": 12.8, "hazardous": False, "recyclable": True, "value_usd": 16.50, "color": "#1B4332", "layer": 4},
            {"name": "5000 mAh Li-Po Battery Pack (100W Fast Charge)", "material": "Lithium Cobalt Oxide (LiCoO2) + Graphite Anode", "specs": battery_specs, "weight_pct": 36.5, "hazardous": True, "recyclable": True, "value_usd": 3.80, "color": "#C0392B", "layer": 5},
            {"name": "Die-Cast Mid-Frame, USB-C & Haptic Engine", "material": "6063 Aerospace Aluminum Alloy + Neodymium Magnet", "specs": "CNC Precision Unibody Core + X-Axis Linear Motor", "weight_pct": 18.0, "hazardous": False, "recyclable": True, "value_usd": 2.80, "color": frame_color, "layer": 6},
            {"name": "120Hz Curved AMOLED Display & Front Glass", "material": "Indium Tin Oxide (ITO) + Aluminosilicate Glass (0.55mm)", "specs": "6.7\" Curved Matrix, 1.07B Colors, 2160Hz PWM", "weight_pct": 12.2, "hazardous": False, "recyclable": True, "value_usd": 7.50, "color": "#1F618D", "layer": 7}
        ]

    comp_data = []
    for i, comp in enumerate(components):
        comp_data.append({
            "name": comp.get("name", f"Component {i+1}"),
            "material": comp.get("material", "Composite"),
            "specs": comp.get("specs", "Standard Hardware Spec"),
            "weight_pct": comp.get("weight_pct", 10.0),
            "hazardous": comp.get("hazardous", False),
            "recyclable": comp.get("recyclable", True),
            "value_usd": comp.get("value_usd", 2.00),
            "color": comp.get("color", "#777777"),
            "layer": comp.get("layer", i + 1),
            "index": i
        })

    comp_json = json.dumps(comp_data)
    manual_steps_json = json.dumps(manual_steps)
    
    total_val = sum(c["value_usd"] for c in comp_data)
    scrap_val_str = f"${total_val:.2f}"
    
    # Public raw CDN links for external CC-BY GLB models (fallback-safe)
    glb_urls = {
        "iphone_15_pro": "https://raw.githubusercontent.com/azharlionkgf/ewaste-ai/main/assets/3d_models/iphone_15_pro.glb",
        "pcb": "https://raw.githubusercontent.com/azharlionkgf/ewaste-ai/main/assets/3d_models/pcb.glb",
        "battery": "https://raw.githubusercontent.com/azharlionkgf/ewaste-ai/main/assets/3d_models/battery.glb"
    }
    glb_urls_json = json.dumps(glb_urls)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    background: #08080a;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    color: #fff;
    overflow: hidden;
    user-select: none;
}}
#viewer-container {{
    width: 100%;
    height: {height}px;
    position: relative;
    background: radial-gradient(circle at 50% 35%, #181d2a 0%, #09090e 85%);
}}
canvas {{ display: block; width: 100%; height: 100%; }}

/* Top Device HUD Bar */
#device-hud {{
    position: absolute;
    top: 10px;
    left: 12px;
    right: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    z-index: 10;
    pointer-events: none;
}}
.hud-brand {{
    background: #DC143C;
    color: #fff;
    font-size: 10.5px;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 6px;
    letter-spacing: 1px;
    font-family: 'Orbitron', sans-serif;
    box-shadow: 0 0 10px rgba(220, 20, 60, 0.5);
}}
.hud-title {{
    color: #f1f1f1;
    font-size: 13px;
    font-weight: 700;
    text-shadow: 0 2px 4px rgba(0,0,0,0.8);
}}
.hud-pill {{
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(8px);
    color: #ccc;
    font-size: 10px;
    padding: 3px 8px;
    border-radius: 12px;
}}
.hud-pill-gold {{
    background: rgba(255, 215, 0, 0.15);
    border-color: #FFD700;
    color: #FFD700;
    font-weight: 700;
}}

/* Asset Switcher Bar */
#model-switcher {{
    position: absolute;
    top: 42px;
    left: 12px;
    display: flex;
    gap: 6px;
    z-index: 12;
    flex-wrap: wrap;
}}
.btn-asset {{
    background: rgba(18, 22, 32, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.18);
    color: #ccc;
    font-size: 9.5px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 8px;
    cursor: pointer;
    backdrop-filter: blur(6px);
    transition: all 0.2s;
}}
.btn-asset:hover {{
    background: rgba(220, 20, 60, 0.3);
    color: #fff;
    border-color: #DC143C;
}}
.btn-asset.active {{
    background: #DC143C;
    color: #fff;
    border-color: #ff3355;
    box-shadow: 0 0 10px rgba(220, 20, 60, 0.6);
}}

/* Left Component Legend */
#legend-panel {{
    position: absolute;
    top: 75px;
    left: 12px;
    background: rgba(12, 14, 20, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 8px 10px;
    max-width: 230px;
    max-height: {height - 150}px;
    overflow-y: auto;
    z-index: 10;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
    scrollbar-width: thin;
    scrollbar-color: #DC143C #12141a;
}}
#legend-panel::-webkit-scrollbar {{ width: 8px; }}
#legend-panel::-webkit-scrollbar-track {{ background: #0d0f14; border-radius: 4px; }}
#legend-panel::-webkit-scrollbar-thumb {{ background: #DC143C; border-radius: 4px; }}
#legend-panel h4 {{
    font-size: 10px;
    color: #DC143C;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
    text-transform: uppercase;
    font-family: 'Orbitron', sans-serif;
}}
.legend-item {{
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 4px 6px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 10px;
    color: #bbb;
    transition: all 0.2s;
    margin-bottom: 2px;
}}
.legend-item:hover, .legend-item.active {{
    background: rgba(220, 20, 60, 0.25);
    color: #fff;
    border-left: 2px solid #DC143C;
    transform: translateX(2px);
}}
.legend-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}}

/* Right Floating Inspection HUD */
#inspect-card {{
    position: absolute;
    top: 75px;
    right: 12px;
    background: rgba(12, 14, 20, 0.92);
    border: 1px solid rgba(220, 20, 60, 0.4);
    box-shadow: 0 8px 32px rgba(220, 20, 60, 0.25);
    border-radius: 12px;
    padding: 12px 14px;
    width: 250px;
    z-index: 10;
    display: none;
    backdrop-filter: blur(14px);
    animation: fadeIn 0.2s ease-out;
}}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(-5px); }} to {{ opacity: 1; transform: translateY(0); }} }}
#inspect-card h3 {{
    color: #DC143C;
    font-size: 12px;
    margin-bottom: 6px;
    font-family: 'Orbitron', sans-serif;
}}
.inspect-row {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    font-size: 10px;
}}
.inspect-label {{ color: #888; }}

/* Physical Disassembly Step Action Banner */
#step-banner {{
    position: absolute;
    top: 75px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(15, 18, 25, 0.96);
    border: 1px solid rgba(255, 215, 0, 0.45);
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255, 215, 0, 0.2);
    border-radius: 14px;
    padding: 10px 16px;
    width: 90%;
    max-width: 680px;
    z-index: 10;
    display: none;
    backdrop-filter: blur(14px);
}}
#step-title {{
    color: #FFD700;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 4px;
    display: flex;
    justify-content: space-between;
}}
#step-tools {{
    color: #00FF7F;
    font-size: 10.5px;
    font-weight: 600;
    margin-bottom: 4px;
}}
#step-action {{
    color: #ddd;
    font-size: 10.5px;
    line-height: 1.4;
}}
#step-safety {{
    color: #FF5252;
    font-size: 10px;
    font-weight: 600;
    margin-top: 4px;
}}

/* Bottom Interactive Controls */
#controls-bar {{
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(12, 14, 20, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.65);
    backdrop-filter: blur(12px);
    border-radius: 24px;
    padding: 5px 12px;
    display: flex;
    align-items: center;
    gap: 7px;
    z-index: 10;
    flex-wrap: wrap;
    justify-content: center;
}}
.btn-ctrl {{
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.16);
    color: #f1f1f1;
    padding: 4px 10px;
    border-radius: 14px;
    cursor: pointer;
    font-size: 10.5px;
    font-weight: 600;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 3px;
}}
.btn-ctrl:hover {{
    background: rgba(220, 20, 60, 0.35);
    border-color: #DC143C;
    transform: translateY(-1px);
}}
.btn-ctrl.active {{
    background: #DC143C;
    border-color: #ff3355;
    color: #fff;
    box-shadow: 0 0 12px rgba(220, 20, 60, 0.5);
}}
.btn-ctrl-gold.active {{
    background: #D4AF37;
    border-color: #FFD700;
    color: #000;
    font-weight: 700;
    box-shadow: 0 0 12px rgba(255, 215, 0, 0.6);
}}
.slider-container {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-left: 6px;
    font-size: 11px;
    color: #ccc;
    font-weight: 600;
}}
.slider-container input[type=range] {{
    width: 110px;
    height: 8px;
    accent-color: #DC143C;
    cursor: pointer;
    border-radius: 4px;
}}
#loading-overlay {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #DC143C;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 1px;
    z-index: 20;
    background: rgba(8, 8, 12, 0.85);
    padding: 10px 20px;
    border-radius: 8px;
    border: 1px solid rgba(220, 20, 60, 0.5);
}}
#toast-msg {{
    position: absolute;
    bottom: 52px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(20, 25, 35, 0.95);
    border: 1px solid #FFD700;
    color: #FFD700;
    font-size: 10px;
    padding: 4px 12px;
    border-radius: 12px;
    z-index: 15;
    display: none;
}}
</style>
</head>
<body>
<div id="viewer-container">
    <div id="loading-overlay">⚡ INITIALIZING REALISTIC 3D HARDWARE SIMULATOR...</div>
    <div id="toast-msg"></div>

    <!-- Top Device HUD -->
    <div id="device-hud">
        <span class="hud-brand">{brand.upper()}</span>
        <span class="hud-title">{model_name}</span>
        <span class="hud-pill">💾 {storage}</span>
        <span class="hud-pill">⚡ {ram}</span>
        <span class="hud-pill">🧠 {processor.split('(')[0].strip()}</span>
        <span class="hud-pill hud-pill-gold">💰 Scrap: {scrap_val_str}</span>
    </div>

    <!-- Model Asset Switcher -->
    <div id="model-switcher">
        <button class="btn-asset active" id="btn-mode-twin" onclick="switchModelMode('twin')">📱 Realme 11 Pro Twin</button>
        <button class="btn-asset" id="btn-mode-phone" onclick="switchModelMode('phone')">📐 iPhone 15 Pro (GLB)</button>
        <button class="btn-asset" id="btn-mode-pcb" onclick="switchModelMode('pcb')">⚡ Logic PCB (GLB)</button>
        <button class="btn-asset" id="btn-mode-battery" onclick="switchModelMode('battery')">🔋 Li-Po Battery (GLB)</button>
    </div>

    <!-- Left Component Legend -->
    <div id="legend-panel">
        <h4>🔬 ARCHITECTURE LAYERS</h4>
        <div id="legend-list"></div>
    </div>

    <!-- Right Floating Inspection HUD -->
    <div id="inspect-card">
        <h3 id="card-title">Component Inspector</h3>
        <div class="inspect-row"><span class="inspect-label">Material:</span><span id="card-mat">--</span></div>
        <div class="inspect-row"><span class="inspect-label">Technical Spec:</span><span id="card-spec">--</span></div>
        <div class="inspect-row"><span class="inspect-label">Mass Share:</span><span id="card-weight">--</span></div>
        <div class="inspect-row"><span class="inspect-label">Recovery Value:</span><span id="card-val" style="color:#FFD700;">--</span></div>
        <div class="inspect-row"><span class="inspect-label">Safety Hazard:</span><span id="card-haz">--</span></div>
        <div class="inspect-row"><span class="inspect-label">Recyclability:</span><span id="card-rec">--</span></div>
        <button onclick="closeInspectCard()" style="width:100%;margin-top:6px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;padding:3px;border-radius:6px;cursor:pointer;font-size:9.5px;">Close</button>
    </div>

    <!-- Physical Disassembly Step Action Banner -->
    <div id="step-banner">
        <div id="step-title">
            <span id="step-name">Step 1 of 7</span>
            <span id="step-count" style="color:#aaa;">Physical Teardown Manual</span>
        </div>
        <div id="step-tools">🛠️ Tools: Heat Mat (78°C) • Suction Clamp • SIM Pin</div>
        <div id="step-action">Step Instructions...</div>
        <div id="step-safety">⚠️ Safety Warning...</div>
    </div>

    <!-- Bottom Controls -->
    <div id="controls-bar">
        <button class="btn-ctrl active" id="btn-assembled" onclick="setExplodeMode(false)">🔒 Assembled</button>
        <button class="btn-ctrl" id="btn-exploded" onclick="setExplodeMode(true)">💥 Exploded</button>
        
        <div class="slider-container">
            <span>Explode:</span>
            <input type="range" id="explode-slider" min="0" max="100" value="0" oninput="onSliderExplode(this.value)">
        </div>

        <button class="btn-ctrl btn-ctrl-gold" id="btn-manual" onclick="toggleManualMode()">📖 Manual Teardown</button>
        <button class="btn-ctrl" id="btn-prev-step" onclick="prevStep()" style="display:none;">⏮️ Prev</button>
        <button class="btn-ctrl" id="btn-next-step" onclick="nextStep()" style="display:none;">Next ⏭️</button>

        <button class="btn-ctrl active" id="btn-spin" onclick="toggleAutoSpin()">🔄 Rotate</button>
        <button class="btn-ctrl" id="btn-xray" onclick="toggleXRay()">👁️ X-Ray</button>
        <button class="btn-ctrl" id="btn-reset" onclick="reset3DView()">🎯 Center</button>
    </div>
</div>

<!-- Three.js + GLTFLoader CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>

<script>
const COMPONENTS = {comp_json};
const MANUAL_STEPS = {manual_steps_json};
const GLB_URLS = {glb_urls_json};
const CAMERA_TYPE = "{camera_module_type}";
const HAS_RACING_STRIPE = {"true" if has_racing_stripe else "false"};
const COLOR_CHASSIS = "{chassis_color}";
const COLOR_ACCENT = "{accent_color}";
const COLOR_FRAME = "{frame_color}";
const COLOR_SCREEN = "{screen_color}";

let scene, camera, renderer, rootGroup, currentAssetGroup;
let meshLayers = [];
let targetExplodeRatio = 0.0;
let currentExplodeRatio = 0.0;
let isSpinning = true;
let isXRay = false;
let isManualMode = false;
let currentManualStep = 0;
let selectedMesh = null;
let raycaster, mouse;
let currentMode = 'twin';

// Procedural Lychee Vegan Leather Bump Texture
function createLeatherTexture() {{
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 256;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#f4eee4';
    ctx.fillRect(0, 0, 256, 256);
    const imgData = ctx.getImageData(0, 0, 256, 256);
    const data = imgData.data;
    for (let i = 0; i < data.length; i += 4) {{
        const grain = (Math.random() - 0.5) * 32;
        data[i] = Math.min(255, Math.max(0, data[i] + grain));
        data[i+1] = Math.min(255, Math.max(0, data[i+1] + grain * 0.95));
        data[i+2] = Math.min(255, Math.max(0, data[i+2] + grain * 0.85));
    }}
    ctx.putImageData(imgData, 0, 0);
    const texture = new THREE.CanvasTexture(canvas);
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;
    texture.repeat.set(4, 8);
    return texture;
}}

// Procedural Woven Racing Stripe Texture (Matteo Menotto Gucci signature)
function createSeamStripeTexture() {{
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 256;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#1c3d2f'; // Menotto deep green
    ctx.fillRect(0, 0, 64, 256);
    for (let y = 0; y < 256; y += 8) {{
        ctx.fillStyle = (y % 16 === 0) ? '#d4af37' : '#ffd700';
        ctx.fillRect(24, y, 16, 5);
    }}
    const texture = new THREE.CanvasTexture(canvas);
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;
    texture.repeat.set(1, 6);
    return texture;
}}

function showToast(msg) {{
    const t = document.getElementById('toast-msg');
    t.textContent = msg;
    t.style.display = 'block';
    setTimeout(() => {{ t.style.display = 'none'; }}, 3500);
}}

function init3D() {{
    const container = document.getElementById('viewer-container');
    const width = container.clientWidth || window.innerWidth;
    const height = {height};

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 1000);
    camera.position.set(3.8, 2.6, 5.0);
    camera.lookAt(0, 0, 0);

    renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true, powerPreference: "high-performance" }});
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.25;
    container.appendChild(renderer.domElement);

    // Advanced Cinematic Multi-Point Studio Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xfff8ee, 1.25);
    keyLight.position.set(7, 12, 9);
    keyLight.castShadow = true;
    scene.add(keyLight);

    const rimLight = new THREE.DirectionalLight(0x4080ff, 0.65);
    rimLight.position.set(-8, -4, -7);
    scene.add(rimLight);

    const warmUnderLight = new THREE.DirectionalLight(0xffaa44, 0.4);
    warmUnderLight.position.set(0, -8, 2);
    scene.add(warmUnderLight);

    const redAccent = new THREE.SpotLight(0xDC143C, 1.5, 30, Math.PI / 4, 0.5);
    redAccent.position.set(0, 9, 0);
    scene.add(redAccent);

    const grid = new THREE.GridHelper(12, 24, 0x222630, 0x111318);
    grid.position.y = -2.0;
    scene.add(grid);

    rootGroup = new THREE.Group();
    scene.add(rootGroup);

    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    buildUltraRealisticDevice();
    buildLegend();
    setupMouseAndTouch(renderer.domElement);

    document.getElementById('loading-overlay').style.display = 'none';
    animate();
}}

/* Construct Ultra-Realistic Multi-Layer Electronic Architecture */
function buildUltraRealisticDevice() {{
    // Clear any existing mesh layers
    while (rootGroup.children.length > 0) {{
        rootGroup.remove(rootGroup.children[0]);
    }}
    meshLayers = [];

    const phoneWidth = 2.05;
    const phoneHeight = 4.3;
    const layerSpacingAssembled = 0.048;
    const layerSpacingExploded = 0.58;
    const nLayers = COMPONENTS.length;

    const leatherTex = createLeatherTexture();
    const seamTex = createSeamStripeTexture();

    COMPONENTS.forEach((comp, idx) => {{
        const layerGroup = new THREE.Group();
        const assembledZ = (idx - nLayers / 2) * layerSpacingAssembled;
        const explodedZ = (idx - nLayers / 2) * layerSpacingExploded;

        let primaryMesh;

        if (comp.layer === 1) {{
            // ═══ LAYER 1: BACK HOUSING & CAMERA MATRIX & VEGAN LEATHER ═══
            const backGeo = new THREE.BoxGeometry(phoneWidth, phoneHeight, 0.055);
            const backMat = new THREE.MeshStandardMaterial({{
                color: parseInt(COLOR_CHASSIS.replace('#', '0x')),
                roughness: 0.76,
                metalness: 0.05,
                bumpMap: leatherTex,
                bumpScale: 0.008
            }});
            primaryMesh = new THREE.Mesh(backGeo, backMat);
            layerGroup.add(primaryMesh);

            // 3D Racing Seam Stripe & Stitching
            if (HAS_RACING_STRIPE) {{
                const stripeGeo = new THREE.BoxGeometry(0.08, phoneHeight + 0.01, 0.062);
                const stripeMat = new THREE.MeshStandardMaterial({{
                    color: 0xffffff,
                    map: seamTex,
                    metalness: 0.7,
                    roughness: 0.3
                }});
                const stripeMesh = new THREE.Mesh(stripeGeo, stripeMat);
                layerGroup.add(stripeMesh);

                const stitchMat = new THREE.MeshBasicMaterial({{ color: 0x9e8354 }});
                const sGeo = new THREE.BoxGeometry(0.012, phoneHeight, 0.063);
                const s1 = new THREE.Mesh(sGeo, stitchMat); s1.position.x = -0.055; layerGroup.add(s1);
                const s2 = new THREE.Mesh(sGeo, stitchMat); s2.position.x = 0.055; layerGroup.add(s2);
            }}

            if (CAMERA_TYPE === "circular_matrix") {{
                // Luxury Gold Bezel Halo Ring
                const haloOuterGeo = new THREE.CylinderGeometry(0.58, 0.58, 0.075, 64);
                const haloOuterMat = new THREE.MeshStandardMaterial({{
                    color: parseInt(COLOR_ACCENT.replace('#', '0x')),
                    metalness: 0.95,
                    roughness: 0.15
                }});
                const haloMesh = new THREE.Mesh(haloOuterGeo, haloOuterMat);
                haloMesh.rotation.x = Math.PI / 2;
                haloMesh.position.set(0, 0.95, 0.055);
                layerGroup.add(haloMesh);

                // Deep Obsidian Camera Glass Disc
                const discGeo = new THREE.CylinderGeometry(0.51, 0.51, 0.085, 64);
                const discMat = new THREE.MeshStandardMaterial({{ color: 0x0a0a0f, roughness: 0.04, metalness: 0.95 }});
                const discMesh = new THREE.Mesh(discGeo, discMat);
                discMesh.rotation.x = Math.PI / 2;
                discMesh.position.set(0, 0.95, 0.06);
                layerGroup.add(discMesh);

                // Primary 200MP OIS Lens with Sapphire Multi-Coating (deep optical blue)
                const lensGeo = new THREE.CylinderGeometry(0.20, 0.20, 0.10, 32);
                const lensMat = new THREE.MeshStandardMaterial({{ color: 0x09203f, metalness: 0.95, roughness: 0.04 }});
                const lensMesh = new THREE.Mesh(lensGeo, lensMat);
                lensMesh.rotation.x = Math.PI / 2;
                lensMesh.position.set(0, 0.95, 0.07);
                layerGroup.add(lensMesh);

                // Secondary 8MP Ultra-Wide & 2MP Macro Lenses
                const subLensGeo = new THREE.CylinderGeometry(0.09, 0.09, 0.095, 24);
                const sub1 = new THREE.Mesh(subLensGeo, lensMat);
                sub1.rotation.x = Math.PI / 2;
                sub1.position.set(-0.27, 0.95, 0.068);
                layerGroup.add(sub1);

                const sub2 = new THREE.Mesh(subLensGeo, lensMat);
                sub2.rotation.x = Math.PI / 2;
                sub2.position.set(0.27, 0.95, 0.068);
                layerGroup.add(sub2);

                // Dual-Tone LED Flash Ring
                const flashGeo = new THREE.CylinderGeometry(0.065, 0.065, 0.092, 20);
                const flashMat = new THREE.MeshStandardMaterial({{ color: 0xFFF5E1, emissive: 0xFFE082, emissiveIntensity: 0.8 }});
                const flashMesh = new THREE.Mesh(flashGeo, flashMat);
                flashMesh.rotation.x = Math.PI / 2;
                flashMesh.position.set(0, 1.28, 0.068);
                layerGroup.add(flashMesh);
            }}

        }} else if (comp.layer === 2) {{
            // ═══ LAYER 2: GRAPHITE THERMAL DISSIPATION & NFC LOOP & COPPER FOIL ═══
            const graphGeo = new THREE.BoxGeometry(phoneWidth * 0.86, phoneHeight * 0.86, 0.018);
            const graphMat = new THREE.MeshStandardMaterial({{ color: 0x222225, roughness: 0.85, metalness: 0.35 }});
            primaryMesh = new THREE.Mesh(graphGeo, graphMat);
            layerGroup.add(primaryMesh);

            const cuFoilGeo = new THREE.BoxGeometry(phoneWidth * 0.65, phoneHeight * 0.38, 0.022);
            const cuFoilMat = new THREE.MeshStandardMaterial({{ color: 0xB87333, metalness: 0.92, roughness: 0.25 }});
            const cuFoil = new THREE.Mesh(cuFoilGeo, cuFoilMat);
            cuFoil.position.set(0, 0.6, 0.005);
            layerGroup.add(cuFoil);

            const coilGeo = new THREE.TorusGeometry(0.48, 0.028, 12, 36);
            const coilMat = new THREE.MeshStandardMaterial({{ color: 0xCD7F32, metalness: 0.95, roughness: 0.2 }});
            const coilMesh = new THREE.Mesh(coilGeo, coilMat);
            coilMesh.position.set(0, -0.15, 0.015);
            layerGroup.add(coilMesh);

        }} else if (comp.layer === 3) {{
            // ═══ LAYER 3: 16x PRECISION SCREWS & MIDFRAME PERIMETER BRACKET ═══
            const bracketGeo = new THREE.BoxGeometry(phoneWidth * 0.95, phoneHeight * 0.95, 0.022);
            const bracketMat = new THREE.MeshStandardMaterial({{ color: 0x424949, metalness: 0.8, roughness: 0.3 }});
            primaryMesh = new THREE.Mesh(bracketGeo, bracketMat);
            layerGroup.add(primaryMesh);

            const screwHeadGeo = new THREE.CylinderGeometry(0.045, 0.035, 0.035, 16);
            const screwDriveGeo = new THREE.BoxGeometry(0.05, 0.012, 0.04);
            const screwMat = new THREE.MeshStandardMaterial({{ color: 0xd5d8dc, metalness: 0.95, roughness: 0.15 }});
            const driveMat = new THREE.MeshBasicMaterial({{ color: 0x1c2833 }});

            const screwCoords = [
                [-0.85, 1.85], [0.85, 1.85], [-0.85, -1.85], [0.85, -1.85],
                [-0.85, 1.2], [0.85, 1.2], [-0.85, -1.2], [0.85, -1.2],
                [-0.85, 0.4], [0.85, 0.4], [-0.85, -0.4], [0.85, -0.4],
                [-0.35, 1.85], [0.35, 1.85], [-0.35, -1.85], [0.35, -1.85]
            ];

            screwCoords.forEach(pos => {{
                const sGroup = new THREE.Group();
                const sh = new THREE.Mesh(screwHeadGeo, screwMat);
                sh.rotation.x = Math.PI / 2;
                const sd = new THREE.Mesh(screwDriveGeo, driveMat);
                sd.position.z = 0.015;
                sGroup.add(sh);
                sGroup.add(sd);
                sGroup.position.set(pos[0], pos[1], 0.02);
                layerGroup.add(sGroup);
            }});

        }} else if (comp.layer === 4) {{
            // ═══ LAYER 4: LOGIC MOTHERBOARD (10-LAYER FR4 PCB + SOC + MEMORY + ICs + FPC) ═══
            const pcbGeo = new THREE.BoxGeometry(phoneWidth * 0.90, phoneHeight * 0.48, 0.028);
            const pcbMat = new THREE.MeshStandardMaterial({{ color: 0x145A32, roughness: 0.35, metalness: 0.25 }});
            primaryMesh = new THREE.Mesh(pcbGeo, pcbMat);
            primaryMesh.position.set(0, 0.95, 0);
            layerGroup.add(primaryMesh);

            // Gold Solder Contact Traces
            const goldTraceMat = new THREE.MeshStandardMaterial({{ color: 0xFFD700, metalness: 0.98, roughness: 0.15 }});
            for (let g = 0; g < 8; g++) {{
                const gt = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.018, 0.032), goldTraceMat);
                gt.position.set(-0.75 + g * 0.22, 0.65, 0.012);
                layerGroup.add(gt);
            }}

            // Dimensity 7050 5G SoC
            const socGeo = new THREE.BoxGeometry(0.44, 0.44, 0.038);
            const socMat = new THREE.MeshStandardMaterial({{ color: 0x0b0e14, metalness: 0.88, roughness: 0.2 }});
            const socMesh = new THREE.Mesh(socGeo, socMat);
            socMesh.position.set(-0.25, 1.0, 0.025);
            layerGroup.add(socMesh);

            // 256GB UFS 3.1 NAND Flash
            const nandGeo = new THREE.BoxGeometry(0.40, 0.34, 0.035);
            const nandMat = new THREE.MeshStandardMaterial({{ color: 0x161c24, metalness: 0.85, roughness: 0.25 }});
            const nandMesh = new THREE.Mesh(nandGeo, nandMat);
            nandMesh.position.set(0.28, 1.0, 0.025);
            layerGroup.add(nandMesh);

            // Nickel-Silver RF EMI Shield
            const shieldGeo = new THREE.BoxGeometry(0.58, 0.38, 0.034);
            const shieldMat = new THREE.MeshStandardMaterial({{ color: 0xEAEDED, metalness: 0.96, roughness: 0.12 }});
            const shieldMesh = new THREE.Mesh(shieldGeo, shieldMat);
            shieldMesh.position.set(0, 0.52, 0.02);
            layerGroup.add(shieldMesh);

            // FPC Flex Ribbon Interconnect
            const fpcGeo = new THREE.BoxGeometry(0.22, 1.8, 0.015);
            const fpcMat = new THREE.MeshStandardMaterial({{ color: 0xB7950B, metalness: 0.6, roughness: 0.35 }});
            const fpcMesh = new THREE.Mesh(fpcGeo, fpcMat);
            fpcMesh.position.set(0.68, -0.15, 0.018);
            layerGroup.add(fpcMesh);

            // Dual SIM Card Slot
            const simSlotGeo = new THREE.BoxGeometry(0.38, 0.45, 0.03);
            const simSlotMat = new THREE.MeshStandardMaterial({{ color: 0x95A5A6, metalness: 0.9 }});
            const simSlot = new THREE.Mesh(simSlotGeo, simSlotMat);
            simSlot.position.set(-0.65, 1.2, 0.02);
            layerGroup.add(simSlot);

        }} else if (comp.layer === 5) {{
            // ═══ LAYER 5: 5000 mAh HIGH-DENSITY LI-PO BATTERY WITH PULL-TABS ═══
            const battGeo = new THREE.BoxGeometry(phoneWidth * 0.82, phoneHeight * 0.46, 0.068);
            const battMat = new THREE.MeshStandardMaterial({{ color: 0x922B21, roughness: 0.65, metalness: 0.15 }});
            primaryMesh = new THREE.Mesh(battGeo, battMat);
            primaryMesh.position.set(0, -0.65, 0);
            layerGroup.add(primaryMesh);

            // Lithium Warning Silkscreen
            const warnGeo = new THREE.BoxGeometry(0.65, 0.25, 0.072);
            const warnMat = new THREE.MeshStandardMaterial({{ color: 0xF39C12, roughness: 0.7 }});
            const warnMesh = new THREE.Mesh(warnGeo, warnMat);
            warnMesh.position.set(0, -0.65, 0.005);
            layerGroup.add(warnMesh);

            // Pull Tabs A & B
            const tabGeo = new THREE.BoxGeometry(0.18, 0.09, 0.075);
            const tabMat = new THREE.MeshStandardMaterial({{ color: 0x27AE60, roughness: 0.4 }});
            const tab1 = new THREE.Mesh(tabGeo, tabMat); tab1.position.set(-0.35, -0.38, 0.01); layerGroup.add(tab1);
            const tab2 = new THREE.Mesh(tabGeo, tabMat); tab2.position.set(0.35, -0.38, 0.01); layerGroup.add(tab2);

            // BMU Flex
            const bmuGeo = new THREE.BoxGeometry(0.45, 0.06, 0.04);
            const bmuMat = new THREE.MeshStandardMaterial({{ color: 0x1B4F72, metalness: 0.8 }});
            const bmu = new THREE.Mesh(bmuGeo, bmuMat);
            bmu.position.set(0, -0.39, 0.02);
            layerGroup.add(bmu);

        }} else if (comp.layer === 6) {{
            // ═══ LAYER 6: 6063 AEROSPACE ALUMINUM MID-FRAME & HAPTIC MOTOR & USB-C ═══
            const frameGeo = new THREE.BoxGeometry(phoneWidth * 0.98, phoneHeight * 0.98, 0.058);
            const frameMat = new THREE.MeshStandardMaterial({{
                color: parseInt(COLOR_FRAME.replace('#', '0x')),
                metalness: 0.88,
                roughness: 0.22
            }});
            primaryMesh = new THREE.Mesh(frameGeo, frameMat);
            layerGroup.add(primaryMesh);

            // Antenna Bands
            const bandMat = new THREE.MeshBasicMaterial({{ color: 0x2C3E50 }});
            const bGeo = new THREE.BoxGeometry(0.04, 0.08, 0.065);
            const b1 = new THREE.Mesh(bGeo, bandMat); b1.position.set(-phoneWidth*0.49, 1.4, 0); layerGroup.add(b1);
            const b2 = new THREE.Mesh(bGeo, bandMat); b2.position.set(phoneWidth*0.49, 1.4, 0); layerGroup.add(b2);
            const b3 = new THREE.Mesh(bGeo, bandMat); b3.position.set(-phoneWidth*0.49, -1.4, 0); layerGroup.add(b3);
            const b4 = new THREE.Mesh(bGeo, bandMat); b4.position.set(phoneWidth*0.49, -1.4, 0); layerGroup.add(b4);

            // USB-C Port
            const usbcGeo = new THREE.BoxGeometry(0.32, 0.08, 0.075);
            const usbcMat = new THREE.MeshStandardMaterial({{ color: 0x17202A, metalness: 0.95 }});
            const usbcMesh = new THREE.Mesh(usbcGeo, usbcMat);
            usbcMesh.position.set(0, -phoneHeight * 0.485, 0);
            layerGroup.add(usbcMesh);

            // X-Axis Linear Tactile Engine
            const motorGeo = new THREE.CylinderGeometry(0.14, 0.14, 0.06, 24);
            const motorMat = new THREE.MeshStandardMaterial({{ color: 0xBDC3C7, metalness: 0.92, roughness: 0.2 }});
            const motorMesh = new THREE.Mesh(motorGeo, motorMat);
            motorMesh.rotation.x = Math.PI / 2;
            motorMesh.position.set(-0.55, -1.65, 0.02);
            layerGroup.add(motorMesh);

            // Speaker Acoustic Resonator
            const spkGeo = new THREE.BoxGeometry(0.65, 0.28, 0.045);
            const spkMat = new THREE.MeshStandardMaterial({{ color: 0x2C3E50, roughness: 0.8 }});
            const spk = new THREE.Mesh(spkGeo, spkMat);
            spk.position.set(0.35, -1.65, 0.015);
            layerGroup.add(spk);

        }} else {{
            // ═══ LAYER 7: 120Hz CURVED AMOLED DISPLAY & FRONT ALUMINOSILICATE GLASS ═══
            const dispGeo = new THREE.BoxGeometry(phoneWidth * 0.96, phoneHeight * 0.96, 0.026);
            const dispMat = new THREE.MeshStandardMaterial({{
                color: parseInt(COLOR_SCREEN.replace('#', '0x')),
                roughness: 0.08,
                metalness: 0.7,
                emissive: 0x051329,
                emissiveIntensity: 0.35
            }});
            primaryMesh = new THREE.Mesh(dispGeo, dispMat);
            layerGroup.add(primaryMesh);

            // Front Glass Cover (Ultra-glossy transparent)
            const glassGeo = new THREE.BoxGeometry(phoneWidth * 0.98, phoneHeight * 0.98, 0.02);
            const glassMat = new THREE.MeshStandardMaterial({{
                color: 0x000000,
                roughness: 0.03,
                metalness: 0.95,
                transparent: true,
                opacity: 0.65
            }});
            const glassMesh = new THREE.Mesh(glassGeo, glassMat);
            glassMesh.position.set(0, 0, 0.012);
            layerGroup.add(glassMesh);

            // Punch-Hole Selfie Camera
            const holeGeo = new THREE.CylinderGeometry(0.045, 0.045, 0.032, 20);
            const holeMat = new THREE.MeshStandardMaterial({{ color: 0x071120, metalness: 0.95, roughness: 0.05 }});
            const holeMesh = new THREE.Mesh(holeGeo, holeMat);
            holeMesh.rotation.x = Math.PI / 2;
            holeMesh.position.set(0, 1.85, 0.022);
            layerGroup.add(holeMesh);

            // Earpiece Speaker Grille Slot
            const earGeo = new THREE.BoxGeometry(0.35, 0.02, 0.03);
            const earMat = new THREE.MeshBasicMaterial({{ color: 0x111115 }});
            const ear = new THREE.Mesh(earGeo, earMat);
            ear.position.set(0, 2.05, 0.022);
            layerGroup.add(ear);
        }}

        if (primaryMesh) {{
            primaryMesh.userData = {{
                ...comp,
                assembledZ: assembledZ,
                explodedZ: explodedZ,
                group: layerGroup
            }};
            meshLayers.push(primaryMesh);
        }}

        layerGroup.position.z = assembledZ;
        rootGroup.add(layerGroup);
    }});
}}

/* Switch Between Procedural Precision Model and Downloaded GLB Assets */
function switchModelMode(mode) {{
    currentMode = mode;
    document.querySelectorAll('.btn-asset').forEach(b => b.classList.remove('active'));
    const btn = document.getElementById(`btn-mode-${{mode}}`);
    if (btn) btn.classList.add('active');

    closeInspectCard();

    if (mode === 'twin') {{
        buildUltraRealisticDevice();
        document.getElementById('legend-panel').style.display = 'block';
        showToast('📱 Loaded: Realme 11 Pro 5G Precision Twin (7-Layer Teardown)');
    }} else {{
        loadGLBAsset(mode);
    }}
}}

/* Asynchronous GLTF/GLB Asset Loader with CORS & Offline Fallback */
function loadGLBAsset(assetKey) {{
    const url = GLB_URLS[assetKey];
    if (!url || typeof THREE.GLTFLoader === 'undefined') {{
        showToast('⚠️ GLTF loader not ready. Displaying procedural twin.');
        return;
    }}

    showToast(`⏳ Loading ${{assetKey.toUpperCase()}} 3D mesh...`);

    const loader = new THREE.GLTFLoader();
    loader.load(
        url,
        function(gltf) {{
            while (rootGroup.children.length > 0) {{
                rootGroup.remove(rootGroup.children[0]);
            }}
            meshLayers = [];

            const model = gltf.scene;
            // Center & normalize scale
            const box = new THREE.Box3().setFromObject(model);
            const size = box.getSize(new THREE.Vector3());
            const center = box.getCenter(new THREE.Vector3());
            
            const maxDim = Math.max(size.x, size.y, size.z);
            const scale = 3.8 / (maxDim || 1);
            model.scale.set(scale, scale, scale);
            model.position.sub(center.multiplyScalar(scale));

            model.traverse(child => {{
                if (child.isMesh) {{
                    child.castShadow = true;
                    child.receiveShadow = true;
                    child.userData = {{
                        name: child.name || `${{assetKey.toUpperCase()}} Sub-Mesh`,
                        material: "Solid PBR Alloy / Silicon",
                        specs: `GLB Asset Mesh (${{child.geometry ? child.geometry.attributes.position.count : 0}} vertices)`,
                        weight_pct: 100,
                        value_usd: 15.00,
                        hazardous: assetKey === 'battery',
                        recyclable: true
                    }};
                    meshLayers.push(child);
                }}
            }});

            rootGroup.add(model);
            document.getElementById('legend-panel').style.display = 'none';
            showToast(`✅ Loaded CC-BY 3D Asset: ${{assetKey.toUpperCase()}}`);
        }},
        undefined,
        function(error) {{
            console.warn('GLB asset fetch failed (likely browser CORS on raw file). Falling back to procedural model:', error);
            showToast('ℹ️ Notice: External CDN asset restricted by iframe CORS. Reverting to verified procedural twin.');
            buildUltraRealisticDevice();
            document.getElementById('legend-panel').style.display = 'block';
            document.querySelectorAll('.btn-asset').forEach(b => b.classList.remove('active'));
            document.getElementById('btn-mode-twin').classList.add('active');
        }}
    );
}}

/* Construct Left Component Legend */
function buildLegend() {{
    const list = document.getElementById('legend-list');
    list.innerHTML = '';
    COMPONENTS.forEach((comp, idx) => {{
        const item = document.createElement('div');
        item.className = 'legend-item';
        item.innerHTML = `
            <div class="legend-dot" style="background:${{comp.color}};"></div>
            <span>${{comp.name}}</span>
        `;
        item.onclick = () => selectComponentByIndex(idx);
        list.appendChild(item);
    }});
}}

/* Interactive Raycasting Selection */
function selectComponent(mesh) {{
    if (!mesh || !mesh.userData) return;
    selectedMesh = mesh;

    meshLayers.forEach(m => {{
        if (m === mesh) {{
            if (m.material && m.material.emissive) {{
                m.material.emissive = new THREE.Color(0xDC143C);
                m.material.emissiveIntensity = 0.55;
            }}
            m.scale.set(1.04, 1.04, 1.04);
        }} else {{
            if (m.material && m.material.emissive) {{
                m.material.emissive = new THREE.Color(0x000000);
                m.material.emissiveIntensity = 0;
            }}
            m.scale.set(1, 1, 1);
        }}
    }});

    const data = mesh.userData;
    document.getElementById('card-title').textContent = data.name || 'Hardware Part';
    document.getElementById('card-mat').textContent = data.material || 'Alloy';
    document.getElementById('card-spec').textContent = data.specs || 'Standard Part';
    document.getElementById('card-weight').textContent = data.weight_pct ? `${{data.weight_pct}}% of total` : 'N/A';
    document.getElementById('card-val').textContent = data.value_usd ? `$${{data.value_usd.toFixed(2)}} USD` : '--';
    document.getElementById('card-haz').innerHTML = data.hazardous ? '<span style="color:#FF4500;">⚠️ HAZARDOUS</span>' : '<span style="color:#00FF7F;">Safe</span>';
    document.getElementById('card-rec').innerHTML = data.recyclable ? '<span style="color:#00FF7F;">✅ 100% Recyclable</span>' : 'Non-Recyclable';
    document.getElementById('inspect-card').style.display = 'block';

    const items = document.querySelectorAll('.legend-item');
    items.forEach((it, i) => it.classList.toggle('active', i === data.index));
}}

function selectComponentByIndex(idx) {{
    if (idx >= 0 && idx < meshLayers.length) {{
        selectComponent(meshLayers[idx]);
    }}
}}

function closeInspectCard() {{
    document.getElementById('inspect-card').style.display = 'none';
    meshLayers.forEach(m => {{
        if (m.material && m.material.emissive) {{
            m.material.emissive = new THREE.Color(0x000000);
            m.material.emissiveIntensity = 0;
        }}
        m.scale.set(1, 1, 1);
    }});
    selectedMesh = null;
}}

/* Explode and Camera Controls */
function setExplodeMode(exploded) {{
    isManualMode = false;
    document.getElementById('btn-manual').classList.remove('active');
    document.getElementById('step-banner').style.display = 'none';
    document.getElementById('btn-prev-step').style.display = 'none';
    document.getElementById('btn-next-step').style.display = 'none';

    targetExplodeRatio = exploded ? 1.0 : 0.0;
    document.getElementById('explode-slider').value = Math.round(targetExplodeRatio * 100);
    document.getElementById('btn-assembled').classList.toggle('active', !exploded);
    document.getElementById('btn-exploded').classList.toggle('active', exploded);
}}

function onSliderExplode(val) {{
    isManualMode = false;
    targetExplodeRatio = parseFloat(val) / 100.0;
    document.getElementById('btn-assembled').classList.toggle('active', targetExplodeRatio === 0);
    document.getElementById('btn-exploded').classList.toggle('active', targetExplodeRatio === 1);
    document.getElementById('btn-manual').classList.remove('active');
    document.getElementById('step-banner').style.display = 'none';
}}

function toggleAutoSpin() {{
    isSpinning = !isSpinning;
    document.getElementById('btn-spin').classList.toggle('active', isSpinning);
}}

function toggleXRay() {{
    isXRay = !isXRay;
    document.getElementById('btn-xray').classList.toggle('active', isXRay);
    meshLayers.forEach(m => {{
        if (m.material) {{
            m.material.wireframe = isXRay;
            m.material.transparent = true;
            m.material.opacity = isXRay ? 0.35 : (m.userData.layer === 7 ? 0.65 : 1.0);
        }}
    }});
}}

/* Manual Step-by-Step Disassembly Engine */
function toggleManualMode() {{
    if (currentMode !== 'twin') {{
        switchModelMode('twin');
    }}

    isManualMode = !isManualMode;
    document.getElementById('btn-manual').classList.toggle('active', isManualMode);
    document.getElementById('btn-assembled').classList.remove('active');
    document.getElementById('btn-exploded').classList.remove('active');
    
    document.getElementById('btn-prev-step').style.display = isManualMode ? 'flex' : 'none';
    document.getElementById('btn-next-step').style.display = isManualMode ? 'flex' : 'none';
    document.getElementById('step-banner').style.display = isManualMode ? 'block' : 'none';

    if (isManualMode) {{
        currentManualStep = 0;
        showManualStep(currentManualStep);
    }} else {{
        reset3DView();
    }}
}}

function showManualStep(stepIdx) {{
    if (stepIdx < 0) stepIdx = 0;
    if (stepIdx >= MANUAL_STEPS.length) stepIdx = MANUAL_STEPS.length - 1;
    currentManualStep = stepIdx;

    const stepData = MANUAL_STEPS[stepIdx];
    document.getElementById('step-name').textContent = stepData.title;
    document.getElementById('step-count').textContent = `Step ${{stepIdx + 1}} of ${{MANUAL_STEPS.length}}`;
    document.getElementById('step-tools').textContent = `🛠️ Tools: ${{stepData.tool}}`;
    document.getElementById('step-action').textContent = stepData.action;
    document.getElementById('step-safety').textContent = stepData.safety;

    meshLayers.forEach((m, idx) => {{
        if (idx === stepData.layer_idx) {{
            m.userData.targetManualZ = m.userData.assembledZ + 1.45;
            if (m.material && m.material.emissive) {{
                m.material.emissive = new THREE.Color(0xFFD700);
                m.material.emissiveIntensity = 0.65;
            }}
        }} else if (idx < stepData.layer_idx) {{
            m.userData.targetManualZ = m.userData.assembledZ + 2.3;
            if (m.material && m.material.emissive) {{
                m.material.emissive = new THREE.Color(0x000000);
                m.material.emissiveIntensity = 0;
            }}
        }} else {{
            m.userData.targetManualZ = m.userData.assembledZ;
            if (m.material && m.material.emissive) {{
                m.material.emissive = new THREE.Color(0x000000);
                m.material.emissiveIntensity = 0;
            }}
        }}
    }});
}}

function nextStep() {{
    if (currentManualStep < MANUAL_STEPS.length - 1) {{
        showManualStep(currentManualStep + 1);
    }}
}}

function prevStep() {{
    if (currentManualStep > 0) {{
        showManualStep(currentManualStep - 1);
    }}
}}

function reset3DView() {{
    camera.position.set(3.8, 2.6, 5.0);
    camera.lookAt(0, 0, 0);
    rootGroup.rotation.set(0, 0, 0);
    targetExplodeRatio = 0.0;
    isManualMode = false;
    document.getElementById('explode-slider').value = 0;
    document.getElementById('btn-assembled').classList.add('active');
    document.getElementById('btn-exploded').classList.remove('active');
    document.getElementById('btn-manual').classList.remove('active');
    document.getElementById('step-banner').style.display = 'none';
    document.getElementById('btn-prev-step').style.display = 'none';
    document.getElementById('btn-next-step').style.display = 'none';
    closeInspectCard();
}}

/* Mouse and Touch Drag Handler */
function setupMouseAndTouch(canvas) {{
    let isDragging = false;
    let prevX = 0, prevY = 0;

    canvas.addEventListener('mousedown', e => {{
        isDragging = true;
        prevX = e.clientX;
        prevY = e.clientY;
    }});

    window.addEventListener('mouseup', () => isDragging = false);

    canvas.addEventListener('mousemove', e => {{
        if (isDragging) {{
            const dx = (e.clientX - prevX) * 0.008;
            const dy = (e.clientY - prevY) * 0.008;
            rootGroup.rotation.y += dx;
            rootGroup.rotation.x = Math.max(-1.2, Math.min(1.2, rootGroup.rotation.x + dy));
            prevX = e.clientX;
            prevY = e.clientY;
        }}
    }});

    canvas.addEventListener('wheel', e => {{
        e.preventDefault();
        const zoomDelta = e.deltaY > 0 ? 1.08 : 0.92;
        camera.position.multiplyScalar(zoomDelta);
        camera.position.clampLength(2.0, 15.0);
    }}, {{ passive: false }});

    canvas.addEventListener('click', e => {{
        const rect = canvas.getBoundingClientRect();
        mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);

        const intersects = raycaster.intersectObjects(meshLayers, true);
        if (intersects.length > 0) {{
            selectComponent(intersects[0].object);
        }}
    }});

    let touchStartX = 0, touchStartY = 0;
    canvas.addEventListener('touchstart', e => {{
        if (e.touches.length === 1) {{
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        }}
    }}, {{ passive: true }});

    canvas.addEventListener('touchmove', e => {{
        if (e.touches.length === 1) {{
            const dx = (e.touches[0].clientX - touchStartX) * 0.01;
            const dy = (e.touches[0].clientY - touchStartY) * 0.01;
            rootGroup.rotation.y += dx;
            rootGroup.rotation.x = Math.max(-1.2, Math.min(1.2, rootGroup.rotation.x + dy));
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        }}
    }}, {{ passive: true }});
}}

/* Render Loop with Smooth Physics Interpolation */
function animate() {{
    requestAnimationFrame(animate);

    if (isSpinning && !selectedMesh && !isManualMode) {{
        rootGroup.rotation.y += 0.004;
    }}

    currentExplodeRatio += (targetExplodeRatio - currentExplodeRatio) * 0.08;

    meshLayers.forEach(m => {{
        if (m.userData && m.userData.group) {{
            let targetZ;
            if (isManualMode && m.userData.targetManualZ !== undefined) {{
                targetZ = m.userData.targetManualZ;
            }} else {{
                const asZ = m.userData.assembledZ;
                const exZ = m.userData.explodedZ;
                targetZ = asZ + (exZ - asZ) * currentExplodeRatio;
            }}
            m.userData.group.position.z += (targetZ - m.userData.group.position.z) * 0.1;
        }}
    }});

    renderer.render(scene, camera);
}}

window.addEventListener('resize', () => {{
    const container = document.getElementById('viewer-container');
    const width = container.clientWidth || window.innerWidth;
    const height = {height};
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
}});

init3D();
</script>
</body>
</html>"""
    return html
