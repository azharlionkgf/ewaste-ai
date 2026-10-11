"""
🎨 High-Fidelity Three.js 3D E-Waste & Device Architecture Viewer
==================================================================
Procedural 3D WebGL generator for electronic devices with exploded anatomy,
real-time animation, interactive component inspection, deep hardware specs,
and interactive step-by-step physical manual disassembly guidance.
"""

import json
from typing import Dict, Any

def generate_3d_viewer(device_info: Dict[str, Any], height: int = 600) -> str:
    """
    Generate an interactive high-fidelity Three.js 3D viewer HTML for any electronic device.
    Supports granular hardware specs and physical step-by-step disassembly guidance.
    """
    # Extract hardware metadata
    brand = device_info.get("brand", "Electronic Device")
    model_name = device_info.get("model", device_info.get("category", "Device Model"))
    category = device_info.get("category", "Electronics")
    storage = device_info.get("storage", "128 GB Flash")
    ram = device_info.get("ram", "8 GB RAM")
    processor = device_info.get("processor", "SoC Multi-Core Processor")
    camera_specs = device_info.get("camera", "High-Resolution Sensor Array")
    battery_specs = device_info.get("battery", "Li-Ion High-Capacity Pack")
    camera_module_type = device_info.get("camera_module_type", "circular_matrix")
    has_racing_stripe = device_info.get("has_racing_stripe", True)
    
    chassis_color = device_info.get("chassis_color", "#E6D7C3")
    accent_color = device_info.get("accent_color", "#FFD700")
    frame_color = device_info.get("frame_color", "#D4AF37")
    screen_color = device_info.get("screen_color", "#080E1A")
    
    # Precise Physical Disassembly Manual Steps
    manual_steps = [
        {
            "step": 1,
            "title": "1. Detach Vegan Leather Back Cover & Camera Halo Ring",
            "tool": "Heat Mat / Heat Gun (75°C) • Suction Cup • 0.3mm Guitar Pick",
            "action": "Warm device perimeter at 75°C for 180s to soften polyurethane adhesive. Attach suction clamp to lower rear panel, insert guitar pick 3mm deep, and slice adhesive clips. Carefully pivot open rightward to prevent tearing NFC ribbon.",
            "safety": "⚠️ Do not use metal blades to prevent gouging battery or cutting internal flex ribbons.",
            "layer_idx": 0
        },
        {
            "step": 2,
            "title": "2. Remove Graphite Thermal Dissipation Sheet & NFC Antenna",
            "tool": "Phillips #00 Precision Screwdriver • Anti-Static ESD Tweezers",
            "action": "Extract 16 Phillips #00 screws (1.4mm) securing the perimeter shield bracket. Using ESD nylon tweezers, peel back the pyrolytic graphite heat transfer sheet and unhook NFC coil connector from motherboard.",
            "safety": "⚠️ Keep track of screw lengths; overtightening longer screws into logic board can pierce traces.",
            "layer_idx": 1
        },
        {
            "step": 3,
            "title": "3. ⚡ CRITICAL: Disconnect Battery FIRST & Unseat Logic Motherboard",
            "tool": "Non-Conductive ESD Plastic Spudger • Torx T2 Driver",
            "action": "MANDATORY FIRST ELECTRICAL STEP: Disconnect battery ribbon connector immediately to eliminate short-circuit hazard. Unplug rear & front camera ribbon cables, display flex, and antenna coax cables. Unscrew logic board standoffs to safely lift motherboard with MediaTek Dimensity 7050 & 256GB Flash NAND.",
            "safety": "🚨 NEVER use metal tweezers near battery terminal. Ground yourself with ESD wristband.",
            "layer_idx": 2
        },
        {
            "step": 4,
            "title": "4. Extract 5000 mAh Li-Po High-Capacity Battery Pack",
            "tool": "Adhesive Pull-Tabs • Isopropyl Alcohol (IPA 99%)",
            "action": "Locate the two green/orange stretch-release adhesive pull-tabs. Pull slowly, steadily, and flat at a 15-degree low angle along battery face. If a tab tears, apply 2 drops of 99% IPA at edges to dissolve adhesive. Lift battery gently.",
            "safety": "🔥 NEVER PRY OR PUNCTURE BATTERY. Punctured lithium cells react exothermically causing chemical fire.",
            "layer_idx": 3
        },
        {
            "step": 5,
            "title": "5. Separate Aluminum Mid-Frame, USB-C Port & Haptic Motor",
            "tool": "Phillips #00 Driver • Curved Tweezers",
            "action": "Unscrew lower loud-speaker acoustic chamber (6 screws). Extract sub-board with USB-C 100W connector port and X-axis linear haptic vibration motor. Recover 6063 aerospace aluminum mid-frame chassis for high-grade alloy recycling.",
            "safety": "🟢 Aluminum frame and copper motor coils are 100% recyclable non-hazardous scrap.",
            "layer_idx": 4
        },
        {
            "step": 6,
            "title": "6. Release 120Hz Curved AMOLED Display Matrix",
            "tool": "Display Separator Hot Plate (80°C) • Flexible Plastic Film",
            "action": "Place front chassis face-down on 80°C heating plate for 3 minutes. Insert ultra-thin plastic separator film between display glass and aluminum chassis rail. Slide smoothly to release factory OCA display adhesive.",
            "safety": "⚠️ AMOLED display substrate is 0.2mm fragile glass. Apply gentle, zero-force levering.",
            "layer_idx": 5
        },
        {
            "step": 7,
            "title": "7. Harvest Front Aluminosilicate Double-Reinforced Glass",
            "tool": "Heat Mat • Citrus-Based Adhesive Remover",
            "action": "Separate exterior toughened aluminosilicate glass cover. Clean off residual adhesive layers using citrus solvent. Sort glass into specialized display cullet recycling bin.",
            "safety": "🧤 Wear cut-resistant nitrile gloves to prevent injury from micro-glass shards.",
            "layer_idx": 6
        }
    ]

    components = device_info.get("components", [])
    if not components:
        components = [
            {"name": "Circular Halo Camera Ring & Vegan Leather Back", "material": "Polycarbonate + PU Vegan Leather + Gold Bezel", "specs": camera_specs, "weight_pct": 14.5, "hazardous": False, "recyclable": True, "value_usd": 7.50, "color": chassis_color, "layer": 1},
            {"name": "Graphite Thermal Dissipation Sheet & NFC Loop", "material": "Pyrolytic Graphite + Pure Copper Induction Coil", "specs": "Thermal Dissipation Interface (13.56 MHz)", "weight_pct": 3.2, "hazardous": False, "recyclable": True, "value_usd": 1.20, "color": "#4A4A4A", "layer": 2},
            {"name": "Logic Motherboard (SoC & 256GB Flash NAND)", "material": "High-Tg 10-Layer FR4 Glass Epoxy + 18k Gold Micro-Plating", "specs": f"{processor} | {ram} | {storage}", "weight_pct": 12.8, "hazardous": False, "recyclable": True, "value_usd": 16.50, "color": "#1B4332", "layer": 3},
            {"name": "5000 mAh Li-Po Battery Pack", "material": "Lithium Cobalt Oxide (LiCoO2) + Graphite Anode", "specs": battery_specs, "weight_pct": 36.5, "hazardous": True, "recyclable": True, "value_usd": 3.80, "color": "#C0392B", "layer": 4},
            {"name": "Die-Cast Aluminum Mid-Frame & Haptic Motor", "material": "6063 Aerospace Aluminum Alloy + Neodymium Magnet", "specs": "CNC Precision Core + Linear Tactile Engine", "weight_pct": 18.0, "hazardous": False, "recyclable": True, "value_usd": 2.80, "color": frame_color, "layer": 5},
            {"name": "120Hz Curved AMOLED Display Substrate", "material": "Indium Tin Oxide (ITO) + Organic Light Emitting Polymers", "specs": "6.7\" Curved Matrix, 1.07 Billion Colors", "weight_pct": 9.0, "hazardous": False, "recyclable": True, "value_usd": 7.20, "color": "#1F618D", "layer": 6},
            {"name": "Front Double-Reinforced Curved Cover Glass", "material": "Aluminosilicate Strengthened Glass (0.55mm)", "specs": "61° Curvature, Oleophobic Smudge-Proof Coating", "weight_pct": 6.0, "hazardous": False, "recyclable": True, "value_usd": 1.20, "color": "#2C3E50", "layer": 7}
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
    background: radial-gradient(circle at 50% 40%, #151821 0%, #08080a 85%);
}}
canvas {{ display: block; width: 100%; height: 100%; }}

/* Top Device HUD Bar */
#device-hud {{
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(15, 18, 25, 0.90);
    border: 1px solid rgba(220, 20, 60, 0.45);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7), 0 0 15px rgba(220, 20, 60, 0.2);
    backdrop-filter: blur(12px);
    border-radius: 24px;
    padding: 6px 18px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 11px;
    z-index: 10;
    max-width: 95%;
    white-space: nowrap;
    overflow-x: auto;
}}
.hud-brand {{
    background: #DC143C;
    color: #fff;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 12px;
    letter-spacing: 0.5px;
    font-size: 10px;
}}
.hud-title {{
    font-weight: 700;
    color: #f1f1f1;
    font-size: 12px;
    letter-spacing: 0.3px;
}}
.hud-pill {{
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #d1d5db;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 10px;
}}
.hud-pill-gold {{
    background: rgba(255, 215, 0, 0.15);
    border: 1px solid rgba(255, 215, 0, 0.4);
    color: #FFD700;
}}

/* Left Components Legend */
#legend-panel {{
    position: absolute;
    top: 55px;
    left: 10px;
    background: rgba(12, 14, 20, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    border-radius: 14px;
    padding: 10px;
    font-size: 10px;
    max-height: {height - 180}px;
    width: 210px;
    overflow-y: auto;
    z-index: 9;
}}
#legend-panel h4 {{
    color: #DC143C;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
    padding-bottom: 4px;
    border-bottom: 1px solid rgba(220, 20, 60, 0.2);
}}
.legend-item {{
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 5px 6px;
    margin: 2px 0;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
}}
.legend-item:hover {{
    background: rgba(255, 255, 255, 0.12);
    transform: translateX(2px);
}}
.legend-dot {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow: 0 0 6px rgba(255, 255, 255, 0.3);
}}
.legend-text {{
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 10px;
}}

/* Floating Hologram Inspection Card */
#inspect-card {{
    position: absolute;
    top: 55px;
    right: 12px;
    background: rgba(10, 12, 18, 0.90);
    border: 1px solid rgba(220, 20, 60, 0.45);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7), 0 0 20px rgba(220, 20, 60, 0.2);
    backdrop-filter: blur(14px);
    border-radius: 14px;
    padding: 14px;
    width: 280px;
    z-index: 10;
    display: none;
    animation: fadeIn 0.3s ease-out;
}}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(-5px); }} to {{ opacity: 1; transform: translateY(0); }} }}
#inspect-card h3 {{
    color: #DC143C;
    font-size: 13px;
    margin-bottom: 6px;
    font-weight: 700;
}}
.inspect-row {{
    display: flex;
    justify-content: space-between;
    margin: 4px 0;
    font-size: 10.5px;
    color: #c9d1d9;
    padding: 2px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}}
.inspect-label {{ color: #8b949e; }}
.badge-danger {{ color: #ff4d4d; font-weight: bold; }}
.badge-safe {{ color: #2ecc71; font-weight: bold; }}

/* Physical Disassembly Step Banner (Bottom center) */
#step-banner {{
    position: absolute;
    bottom: 54px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(10, 12, 18, 0.92);
    border: 1px solid #FFD700;
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.8), 0 0 15px rgba(255, 215, 0, 0.25);
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
    background: rgba(12, 14, 20, 0.90);
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.6);
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
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.15);
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
    gap: 5px;
    margin-left: 4px;
    font-size: 9.5px;
    color: #aaa;
}}
.slider-container input[type=range] {{
    width: 80px;
    accent-color: #DC143C;
    cursor: pointer;
}}
#loading-overlay {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #DC143C;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 1px;
    z-index: 20;
}}
</style>
</head>
<body>
<div id="viewer-container">
    <div id="loading-overlay">⚡ INITIALIZING 3D WEBGL ENGINE...</div>

    <!-- Top Device HUD -->
    <div id="device-hud">
        <span class="hud-brand">{brand.upper()}</span>
        <span class="hud-title">{model_name}</span>
        <span class="hud-pill">💾 {storage}</span>
        <span class="hud-pill">⚡ {ram}</span>
        <span class="hud-pill">🧠 {processor.split('(')[0].strip()}</span>
        <span class="hud-pill hud-pill-gold">💰 Value: {scrap_val_str}</span>
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
        <div id="step-tools">🛠️ Tools: Heat Mat (75°C) • Suction Cup • Nylon Spudger</div>
        <div id="step-action">Step Instructions...</div>
        <div id="step-safety">⚠️ Safety Warning...</div>
    </div>

    <!-- Bottom Controls Bar -->
    <div id="controls-bar">
        <button class="btn-ctrl active" id="btn-assembled" onclick="setExplodeMode(false)">🔧 Assembled</button>
        <button class="btn-ctrl" id="btn-exploded" onclick="setExplodeMode(true)">💥 Exploded</button>
        <button class="btn-ctrl" id="btn-manual" onclick="toggleManualMode()">📖 Manual Teardown</button>
        <button class="btn-ctrl" id="btn-prev-step" onclick="prevStep()" style="display:none;">⏮️ Prev</button>
        <button class="btn-ctrl" id="btn-next-step" onclick="nextStep()" style="display:none;">Next ⏭️</button>
        <button class="btn-ctrl" id="btn-xray" onclick="toggleXRay()">🩻 X-Ray</button>
        <button class="btn-ctrl active" id="btn-spin" onclick="toggleAutoSpin()">🔄 Rotate</button>
        <div class="slider-container">
            <span>Explode:</span>
            <input type="range" id="explode-slider" min="0" max="100" value="0" oninput="onSliderExplode(this.value)">
        </div>
        <button class="btn-ctrl" onclick="reset3DView()">🎯 Reset</button>
    </div>
</div>

<!-- Three.js CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const COMPONENTS = {comp_json};
const MANUAL_STEPS = {manual_steps_json};
const CAMERA_TYPE = "{camera_module_type}";
const HAS_RACING_STRIPE = {"true" if has_racing_stripe else "false"};
const COLOR_CHASSIS = "{chassis_color}";
const COLOR_ACCENT = "{accent_color}";
const COLOR_FRAME = "{frame_color}";
const COLOR_SCREEN = "{screen_color}";

let scene, camera, renderer, rootGroup;
let meshLayers = [];
let isSpinning = true;
let isXRay = false;
let isManualMode = false;
let currentManualStep = 0;
let currentExplodeRatio = 0.0;
let targetExplodeRatio = 0.0;
let selectedMesh = null;
let raycaster, mouse;

function init3D() {{
    const container = document.getElementById('viewer-container');
    const width = container.clientWidth || window.innerWidth;
    const height = {height};

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x08080a);

    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(3.8, 2.6, 5.0);
    camera.lookAt(0, 0, 0);

    renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // Dynamic Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.95);
    dirLight1.position.set(6, 10, 8);
    dirLight1.castShadow = true;
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x406080, 0.5);
    dirLight2.position.set(-6, -4, -6);
    scene.add(dirLight2);

    const spotAccent = new THREE.SpotLight(0xDC143C, 1.2, 20, Math.PI / 4, 0.5);
    spotAccent.position.set(0, 7, 0);
    scene.add(spotAccent);

    const grid = new THREE.GridHelper(12, 24, 0x222630, 0x111318);
    grid.position.y = -1.8;
    scene.add(grid);

    rootGroup = new THREE.Group();
    scene.add(rootGroup);

    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    buildRealisticDevice();
    buildLegend();
    setupMouseAndTouch(renderer.domElement);

    document.getElementById('loading-overlay').style.display = 'none';
    animate();
}}

/* Construct High-Fidelity Multi-Layer Smartphone Architecture */
function buildRealisticDevice() {{
    const phoneWidth = 2.0;
    const phoneHeight = 4.2;
    const layerSpacingAssembled = 0.045;
    const layerSpacingExploded = 0.55;

    const nLayers = COMPONENTS.length;

    COMPONENTS.forEach((comp, idx) => {{
        const layerGroup = new THREE.Group();
        const assembledZ = (idx - nLayers / 2) * layerSpacingAssembled;
        const explodedZ = (idx - nLayers / 2) * layerSpacingExploded;

        let primaryMesh;
        const matColor = parseInt(comp.color.replace('#', '0x')) || 0x777777;

        if (comp.layer === 1) {{
            // LAYER 1: BACK HOUSING & CAMERA MODULE
            const backGeo = new THREE.BoxGeometry(phoneWidth, phoneHeight, 0.06);
            const backMat = new THREE.MeshStandardMaterial({{
                color: parseInt(COLOR_CHASSIS.replace('#', '0x')),
                roughness: 0.65,
                metalness: 0.1
            }});
            primaryMesh = new THREE.Mesh(backGeo, backMat);
            layerGroup.add(primaryMesh);

            // 3D Racing Seam Stripe (Realme 11 Pro Signature)
            if (HAS_RACING_STRIPE) {{
                const stripeGeo = new THREE.BoxGeometry(0.08, phoneHeight + 0.01, 0.065);
                const stripeMat = new THREE.MeshStandardMaterial({{
                    color: parseInt(COLOR_ACCENT.replace('#', '0x')),
                    metalness: 0.8,
                    roughness: 0.3
                }});
                const stripeMesh = new THREE.Mesh(stripeGeo, stripeMat);
                layerGroup.add(stripeMesh);
            }}

            if (CAMERA_TYPE === "circular_matrix") {{
                // Iconic Circular Halo Ring (Realme / Oppo style)
                const haloOuterGeo = new THREE.CylinderGeometry(0.55, 0.55, 0.08, 36);
                const haloOuterMat = new THREE.MeshStandardMaterial({{
                    color: parseInt(COLOR_ACCENT.replace('#', '0x')),
                    metalness: 0.9,
                    roughness: 0.2
                }});
                const haloMesh = new THREE.Mesh(haloOuterGeo, haloOuterMat);
                haloMesh.rotation.x = Math.PI / 2;
                haloMesh.position.set(0, 0.95, 0.06);
                layerGroup.add(haloMesh);

                const discGeo = new THREE.CylinderGeometry(0.48, 0.48, 0.09, 36);
                const discMat = new THREE.MeshStandardMaterial({{ color: 0x111115, roughness: 0.1, metalness: 0.9 }});
                const discMesh = new THREE.Mesh(discGeo, discMat);
                discMesh.rotation.x = Math.PI / 2;
                discMesh.position.set(0, 0.95, 0.065);
                layerGroup.add(discMesh);

                const lensGeo = new THREE.CylinderGeometry(0.18, 0.18, 0.11, 24);
                const lensMat = new THREE.MeshStandardMaterial({{ color: 0x0f3460, metalness: 0.8, roughness: 0.1 }});
                const lensMesh = new THREE.Mesh(lensGeo, lensMat);
                lensMesh.rotation.x = Math.PI / 2;
                lensMesh.position.set(0, 0.95, 0.07);
                layerGroup.add(lensMesh);

                const subLensGeo = new THREE.CylinderGeometry(0.08, 0.08, 0.10, 16);
                const sub1 = new THREE.Mesh(subLensGeo, lensMat);
                sub1.rotation.x = Math.PI / 2;
                sub1.position.set(-0.25, 0.95, 0.07);
                layerGroup.add(sub1);

                const sub2 = new THREE.Mesh(subLensGeo, lensMat);
                sub2.rotation.x = Math.PI / 2;
                sub2.position.set(0.25, 0.95, 0.07);
                layerGroup.add(sub2);

                const flashGeo = new THREE.CylinderGeometry(0.06, 0.06, 0.10, 16);
                const flashMat = new THREE.MeshStandardMaterial({{ color: 0xFFF8DC, emissive: 0xFFE4B5, emissiveIntensity: 0.4 }});
                const flashMesh = new THREE.Mesh(flashGeo, flashMat);
                flashMesh.rotation.x = Math.PI / 2;
                flashMesh.position.set(0, 1.25, 0.07);
                layerGroup.add(flashMesh);
            }}

        }} else if (comp.layer === 2) {{
            // LAYER 2: GRAPHITE THERMAL SHEET & NFC INDUCTION LOOP
            const graphGeo = new THREE.BoxGeometry(phoneWidth * 0.85, phoneHeight * 0.85, 0.02);
            const graphMat = new THREE.MeshStandardMaterial({{ color: 0x2b2b2b, roughness: 0.8, metalness: 0.3 }});
            primaryMesh = new THREE.Mesh(graphGeo, graphMat);
            layerGroup.add(primaryMesh);

            const coilGeo = new THREE.TorusGeometry(0.45, 0.03, 8, 32);
            const coilMat = new THREE.MeshStandardMaterial({{ color: 0xB87333, metalness: 0.9, roughness: 0.2 }});
            const coilMesh = new THREE.Mesh(coilGeo, coilMat);
            coilMesh.position.set(0, 0, 0.015);
            layerGroup.add(coilMesh);

        }} else if (comp.layer === 3) {{
            // LAYER 3: LOGIC MOTHERBOARD (PCB) WITH SOC & NAND FLASH CHIPS
            const pcbGeo = new THREE.BoxGeometry(phoneWidth * 0.88, phoneHeight * 0.48, 0.03);
            const pcbMat = new THREE.MeshStandardMaterial({{ color: 0x1B4332, roughness: 0.4, metalness: 0.2 }});
            primaryMesh = new THREE.Mesh(pcbGeo, pcbMat);
            primaryMesh.position.set(0, 0.95, 0);
            layerGroup.add(primaryMesh);

            const socGeo = new THREE.BoxGeometry(0.42, 0.42, 0.04);
            const socMat = new THREE.MeshStandardMaterial({{ color: 0x0d1117, metalness: 0.8, roughness: 0.3 }});
            const socMesh = new THREE.Mesh(socGeo, socMat);
            socMesh.position.set(-0.25, 0.95, 0.025);
            layerGroup.add(socMesh);

            const nandGeo = new THREE.BoxGeometry(0.38, 0.32, 0.035);
            const nandMat = new THREE.MeshStandardMaterial({{ color: 0x161b22, metalness: 0.7, roughness: 0.4 }});
            const nandMesh = new THREE.Mesh(nandGeo, nandMat);
            nandMesh.position.set(0.28, 0.95, 0.025);
            layerGroup.add(nandMesh);

            const shieldGeo = new THREE.BoxGeometry(0.55, 0.35, 0.03);
            const shieldMat = new THREE.MeshStandardMaterial({{ color: 0xd0d7de, metalness: 0.95, roughness: 0.2 }});
            const shieldMesh = new THREE.Mesh(shieldGeo, shieldMat);
            shieldMesh.position.set(0, 0.5, 0.02);
            layerGroup.add(shieldMesh);

        }} else if (comp.layer === 4) {{
            // LAYER 4: 5000 mAh HIGH-DENSITY LI-PO BATTERY
            const battGeo = new THREE.BoxGeometry(phoneWidth * 0.82, phoneHeight * 0.45, 0.07);
            const battMat = new THREE.MeshStandardMaterial({{ color: 0xC0392B, roughness: 0.5, metalness: 0.2 }});
            primaryMesh = new THREE.Mesh(battGeo, battMat);
            primaryMesh.position.set(0, -0.65, 0);
            layerGroup.add(primaryMesh);

            const warnGeo = new THREE.BoxGeometry(0.5, 0.2, 0.075);
            const warnMat = new THREE.MeshStandardMaterial({{ color: 0xF39C12, roughness: 0.8 }});
            const warnMesh = new THREE.Mesh(warnGeo, warnMat);
            warnMesh.position.set(0, -0.65, 0.005);
            layerGroup.add(warnMesh);

        }} else if (comp.layer === 5) {{
            // LAYER 5: ALUMINUM MID-FRAME CHASSIS
            const frameGeo = new THREE.BoxGeometry(phoneWidth * 0.98, phoneHeight * 0.98, 0.06);
            const frameMat = new THREE.MeshStandardMaterial({{
                color: parseInt(COLOR_FRAME.replace('#', '0x')),
                metalness: 0.85,
                roughness: 0.25
            }});
            primaryMesh = new THREE.Mesh(frameGeo, frameMat);
            layerGroup.add(primaryMesh);

            const usbcGeo = new THREE.BoxGeometry(0.3, 0.06, 0.08);
            const usbcMat = new THREE.MeshStandardMaterial({{ color: 0x111111, metalness: 0.9 }});
            const usbcMesh = new THREE.Mesh(usbcGeo, usbcMat);
            usbcMesh.position.set(0, -phoneHeight * 0.48, 0);
            layerGroup.add(usbcMesh);

        }} else if (comp.layer === 6) {{
            // LAYER 6: 120Hz CURVED AMOLED DISPLAY SUBSTRATE
            const dispGeo = new THREE.BoxGeometry(phoneWidth * 0.94, phoneHeight * 0.94, 0.03);
            const dispMat = new THREE.MeshStandardMaterial({{
                color: parseInt(COLOR_SCREEN.replace('#', '0x')),
                roughness: 0.1,
                metalness: 0.6,
                emissive: 0x051329,
                emissiveIntensity: 0.3
            }});
            primaryMesh = new THREE.Mesh(dispGeo, dispMat);
            layerGroup.add(primaryMesh);

        }} else {{
            // LAYER 7: FRONT CURVED TOUGHENED GLASS WITH PUNCH HOLE
            const glassGeo = new THREE.BoxGeometry(phoneWidth * 0.98, phoneHeight * 0.98, 0.025);
            const glassMat = new THREE.MeshStandardMaterial({{
                color: 0x000000,
                roughness: 0.05,
                metalness: 0.9,
                transparent: true,
                opacity: 0.75
            }});
            primaryMesh = new THREE.Mesh(glassGeo, glassMat);
            layerGroup.add(primaryMesh);

            const holeGeo = new THREE.CylinderGeometry(0.04, 0.04, 0.03, 16);
            const holeMat = new THREE.MeshStandardMaterial({{ color: 0x0a1128, metalness: 0.9, roughness: 0.1 }});
            const holeMesh = new THREE.Mesh(holeGeo, holeMat);
            holeMesh.rotation.x = Math.PI / 2;
            holeMesh.position.set(0, 1.8, 0.015);
            layerGroup.add(holeMesh);
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

/* Construct Left Component Legend */
function buildLegend() {{
    const list = document.getElementById('legend-list');
    let html = '';
    COMPONENTS.forEach((comp, idx) => {{
        const hazIcon = comp.hazardous ? ' ⚠️' : '';
        html += `<div class="legend-item" onclick="selectComponentByIndex(${{idx}})">
            <div class="legend-dot" style="background:${{comp.color}};"></div>
            <span class="legend-text">${{comp.name}}${{hazIcon}}</span>
        </div>`;
    }});
    list.innerHTML = html;
}}

/* Interactive Raycast Selection */
function selectComponent(mesh) {{
    if (!mesh || !mesh.userData) return;
    selectedMesh = mesh;
    const data = mesh.userData;

    meshLayers.forEach(m => {{
        if (m === mesh) {{
            m.material.emissive = new THREE.Color(0xDC143C);
            m.material.emissiveIntensity = 0.5;
            m.scale.set(1.06, 1.06, 1.06);
        }} else {{
            m.material.emissive = new THREE.Color(0x000000);
            m.material.emissiveIntensity = 0;
            m.scale.set(1, 1, 1);
        }}
    }});

    document.getElementById('card-title').textContent = data.name;
    document.getElementById('card-mat').textContent = data.material;
    document.getElementById('card-spec').textContent = data.specs || 'Standard Spec';
    document.getElementById('card-weight').textContent = data.weight_pct + '% of device';
    document.getElementById('card-val').textContent = '$' + data.value_usd.toFixed(2);
    
    const hazEl = document.getElementById('card-haz');
    hazEl.textContent = data.hazardous ? '🔴 HAZARDOUS (Requires PPE)' : '🟢 Safe Component';
    hazEl.className = data.hazardous ? 'badge-danger' : 'badge-safe';

    const recEl = document.getElementById('card-rec');
    recEl.textContent = data.recyclable ? '♻️ 100% Recyclable' : '❌ Non-Recyclable';
    recEl.className = data.recyclable ? 'badge-safe' : 'badge-danger';

    document.getElementById('inspect-card').style.display = 'block';
}}

function selectComponentByIndex(idx) {{
    if (idx >= 0 && idx < meshLayers.length) {{
        selectComponent(meshLayers[idx]);
    }}
}}

function closeInspectCard() {{
    document.getElementById('inspect-card').style.display = 'none';
    meshLayers.forEach(m => {{
        m.material.emissive = new THREE.Color(0x000000);
        m.material.emissiveIntensity = 0;
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
        m.material.wireframe = isXRay;
        m.material.transparent = true;
        m.material.opacity = isXRay ? 0.35 : (m.userData.layer === 7 ? 0.75 : 1.0);
    }});
}}

/* Manual Step-by-Step Disassembly Engine */
function toggleManualMode() {{
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

    // Animate target layer forward to show manual removal
    meshLayers.forEach((m, idx) => {{
        if (idx === stepData.layer_idx) {{
            m.userData.targetManualZ = m.userData.assembledZ + 1.4;
            m.material.emissive = new THREE.Color(0xFFD700);
            m.material.emissiveIntensity = 0.6;
        }} else if (idx < stepData.layer_idx) {{
            // Already disassembled parts float away
            m.userData.targetManualZ = m.userData.assembledZ + 2.2;
            m.material.emissive = new THREE.Color(0x000000);
            m.material.emissiveIntensity = 0;
        }} else {{
            // Remaining assembled parts stay in place
            m.userData.targetManualZ = m.userData.assembledZ;
            m.material.emissive = new THREE.Color(0x000000);
            m.material.emissiveIntensity = 0;
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

        const intersects = raycaster.intersectObjects(meshLayers);
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
