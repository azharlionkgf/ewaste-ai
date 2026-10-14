"""
🎨 Ultra-Realistic High-Fidelity Three.js Universal 3D E-Waste & Architecture Engine
=====================================================================================
Multi-Device Procedural & Asset-Driven 3D WebGL Engine for ALL 15 E-Waste Categories:
- Mobile Phones: Curved OLED unibody, vegan leather bump map, gold racing stripe, halo camera, Dimensity SoC, battery, aluminum chassis
- Laptops: Clamshell base, opening hinged display lid with 16:9 LCD & webcam, keyboard deck with keys, trackpad, motherboard, dual copper fans, battery
- Desktop Computers: ATX PC tower cabinet, side glass panel, motherboard with CPU tower heatsink & spinning fan, dedicated GPU with dual fans, PSU, RAM, mesh
- Tablets: Thin unibody chassis, front glass digitizer, dual battery slabs, logic board, rear aluminum housing
- Displays & Televisions: Widescreen panel, micro-bezel, desktop stand & pedestal, internal backlight diffuser layer, controller board
- Batteries & Packs: 18650 / 21700 cylindrical cells array, spot-welded nickel busbars, BMS circuit board, silicone lead wires, heat-shrink wrap
- PCBs & Circuit Boards: High-density FR4 board, PCIe/RAM gold edge fingers, central BGA processors, micro SMD passives, quartz crystal
- Printers & Scanners: Paper feed cassette tray, scanner glass flatbed, liftable scanner lid, toner drum / ink carriage, stepper motor, drive rollers
- Cables & Wires: Stripped PVC protective sleeve, braided shielding, 4x color-coded copper conductor cores, gold-plated USB/RJ45 connector pins
- Networking & Routers: Router chassis with ventilation slots, 4x external adjustable dipole antennas, Ethernet RJ45 ports, internal Wi-Fi SoC & heatsink
- Servers & Data Centers: 2U rackmount server chassis, redundant hot-swap PSUs, 6x high-RPM blower fan wall, dual-CPU sockets, SAS hot-swap drive bays
- Gaming Consoles: Custom console housing, disc drive slot, ventilation cooling ribs, internal APU processor & vapor chamber
- Large Appliances: Heavy steel cabinet, hermetic rotary compressor pump motor, serpentine copper condenser tubing coils, control module
- Small Appliances: Appliance metal enclosure, control knobs/timer dial, high-voltage magnetron / motor coil, 3-pin grounded power cord

Full Features:
- Assembled 🔒 vs Exploded 💥 mode with interactive 0-100% slider
- Step-by-Step Physical Teardown Manual customized to each specific device
- Interactive Component Inspection HUD (Name, Specs, Material, Mass %, Scrap Value $, Hazard alerts)
- Real 3D GLB/glTF Asset loading with graceful CORS and offline fallback
"""

import os
import json
from typing import Dict, Any, Optional

def generate_3d_viewer(device_info: Dict[str, Any], height: int = 620) -> str:
    """
    Generate an interactive ultra-realistic Three.js 3D viewer HTML for ANY electronic device.
    Dynamically routes to authentic 3D geometry based on category.
    """
    brand = device_info.get("brand", "Electronic Device")
    model_name = device_info.get("model", device_info.get("category", "Device Model"))
    category = device_info.get("category", "Mobile Phones")
    storage = device_info.get("storage", "256 GB UFS Flash")
    ram = device_info.get("ram", "12 GB RAM")
    processor = device_info.get("processor", "High-Performance SoC")
    camera_specs = device_info.get("camera", "High-Resolution Sensor Array")
    battery_specs = device_info.get("battery", "Li-ion High-Capacity Pack")
    camera_module_type = device_info.get("camera_module_type", "circular_matrix")
    has_racing_stripe = device_info.get("has_racing_stripe", True)
    
    chassis_color = device_info.get("chassis_color", "#E6D7C3")
    accent_color = device_info.get("accent_color", "#FFD700")
    frame_color = device_info.get("frame_color", "#D4AF37")
    screen_color = device_info.get("screen_color", "#080E1A")
    
    # Determine device 3D architecture shape
    cat_lower = str(category).lower()
    if "laptop" in cat_lower:
        shape_type = "laptop"
    elif "desktop" in cat_lower or "computer" in cat_lower:
        shape_type = "desktop"
    elif "tablet" in cat_lower or "ipad" in cat_lower:
        shape_type = "tablet"
    elif "monitor" in cat_lower or "television" in cat_lower or "display" in cat_lower or "tv" in cat_lower:
        shape_type = "display"
    elif "batter" in cat_lower:
        shape_type = "battery"
    elif "pcb" in cat_lower or "circuit" in cat_lower or "board" in cat_lower:
        shape_type = "pcb"
    elif "printer" in cat_lower or "scanner" in cat_lower:
        shape_type = "printer"
    elif "cable" in cat_lower or "wire" in cat_lower:
        shape_type = "cable"
    elif "network" in cat_lower or "router" in cat_lower or "modem" in cat_lower:
        shape_type = "networking"
    elif "server" in cat_lower or "data center" in cat_lower:
        shape_type = "server"
    elif "console" in cat_lower or "game" in cat_lower or "gaming" in cat_lower:
        shape_type = "console"
    elif "large appliance" in cat_lower or "refriger" in cat_lower or "wash" in cat_lower or "ac" in cat_lower:
        shape_type = "large_appliance"
    elif "small appliance" in cat_lower or "microwave" in cat_lower or "mixer" in cat_lower or "light" in cat_lower:
        shape_type = "small_appliance"
    else:
        shape_type = "phone"

    # Category-specific teardown steps
    teardown_manuals = {
        "phone": [
            {"step": 1, "title": "1. Eject SIM Tray & Heat Rear Cover", "tool": "0.8mm SIM Pin • Heat Mat (78°C)", "action": "Eject SIM tray; heat rear adhesive at 78°C for 180s.", "safety": "⚠️ Do not heat above 85°C to protect battery.", "layer_idx": 0},
            {"step": 2, "title": "2. Remove Rear Shell & Camera Halo", "tool": "Nylon Guitar Pick • 99% IPA", "action": "Slice perimeter adhesive; unclip NFC loop.", "safety": "⚠️ Insert pick max 3mm deep.", "layer_idx": 1},
            {"step": 3, "title": "3. Extract Screws & Thermal Shield", "tool": "Phillips #00 Screwdriver (1.4mm)", "action": "Remove 16 perimeter screws and graphite heat shield.", "safety": "⚠️ Separate screws by length.", "layer_idx": 2},
            {"step": 4, "title": "4. ⚡ Disconnect Battery FIRST", "tool": "ESD Plastic Spudger", "action": "Pry off battery BMU flex connector to isolate power.", "safety": "🚨 NEVER use metal tweezers near battery pins.", "layer_idx": 3},
            {"step": 5, "title": "5. Remove Motherboard & Cameras", "tool": "ESD Tweezers • Torx T2", "action": "Lift 10-layer FR4 motherboard with Dimensity SoC and cameras.", "safety": "🟢 Pure gold micro-plating recovered for refining.", "layer_idx": 4},
            {"step": 6, "title": "6. Extract 5000mAh Battery Cell", "tool": "Stretch Release Adhesive Tabs", "action": "Pull stretch-release tabs A & B slowly along the battery plane.", "safety": "🔥 NEVER PUNCTURE OR BEND BATTERY.", "layer_idx": 5},
            {"step": 7, "title": "7. Separate AMOLED Display & Frame", "tool": "Curved Heated Separator", "action": "Harvest 120Hz Curved AMOLED panel and aluminum chassis.", "safety": "🧤 Aluminum frame is 100% recyclable non-toxic scrap.", "layer_idx": 6}
        ],
        "laptop": [
            {"step": 1, "title": "1. Remove Bottom Case Screws", "tool": "Torx T5 / Phillips #0 Screwdriver", "action": "Remove 10 perimeter screws; unclip bottom magnesium cover.", "safety": "⚠️ Ensure laptop is shut down and unplugged.", "layer_idx": 0},
            {"step": 2, "title": "2. ⚡ Disconnect Internal Battery Pack", "tool": "Plastic Pry Spudger", "action": "Unplug the multi-pin battery connector from the motherboard.", "safety": "🚨 Crucial step to prevent motherboard short-circuit.", "layer_idx": 1},
            {"step": 3, "title": "3. Extract M.2 SSD & RAM Modules", "tool": "Phillips #00 Screwdriver", "action": "Remove NVMe SSD hold-down screw; unclip DDR4/DDR5 SO-DIMMs.", "safety": "🔒 WIPE SSD STORAGE SECURELY TO PREVENT DATA THEFT.", "layer_idx": 2},
            {"step": 4, "title": "4. Remove Dual Cooling Fans & Heatpipes", "tool": "Phillips #0 Screwdriver • Thermal Paste Cleaner", "action": "Unscrew copper heatpipe assembly and disconnect fan cables.", "safety": "🟢 Pure copper heatpipe has high metallurgical scrap value.", "layer_idx": 3},
            {"step": 5, "title": "5. Unscrew Motherboard & I/O Boards", "tool": "Phillips #00 • ESD Tweezers", "action": "Disconnect keyboard ribbon, display eDP cable, lift mainboard.", "safety": "🟢 High gold yield from CPU/GPU BGA solder balls.", "layer_idx": 4},
            {"step": 6, "title": "6. Extract 4-Cell Li-Po Battery Pack", "tool": "Plastic Pry Tool", "action": "Unscrew or release battery adhesive strips.", "safety": "🔥 Do not bend flexible battery cells.", "layer_idx": 5},
            {"step": 7, "title": "7. Separate Display Assembly & Hinges", "tool": "Torx T8 • Display Bezel Tool", "action": "Unscrew dual zinc hinges; separate 15.6\" IPS panel.", "safety": "⚠️ Handle glass panel with care; avoid cracked glass shards.", "layer_idx": 6}
        ],
        "desktop": [
            {"step": 1, "title": "1. Remove Side Tempered Glass Panel", "tool": "Captive Thumbscrews • Clean Mat", "action": "Unscrew captive thumb-screws; lift off tempered glass side panel.", "safety": "⚠️ Rest glass on soft surface; never place on tile/stone.", "layer_idx": 0},
            {"step": 2, "title": "2. Disconnect AC Power & Switch Off PSU", "tool": "Manual Isolation", "action": "Unplug AC cord; switch off PSU rocker; press power button to discharge.", "safety": "🚨 High-voltage PSU capacitors retain lethal charge.", "layer_idx": 1},
            {"step": 3, "title": "3. Extract Dedicated PCIe GPU Card", "tool": "Phillips #2 Screwdriver", "action": "Unplug PCIe 8-pin power; unscrew bracket; release PCIe slot latch.", "safety": "💰 High resale and precious metal recovery value.", "layer_idx": 2},
            {"step": 4, "title": "4. Remove RAM DIMMs & M.2 Storage", "tool": "ESD Grounded Hand", "action": "Push RAM retention latches; pull modules straight out.", "safety": "🟢 Gold-plated contact fingers recovered for refining.", "layer_idx": 3},
            {"step": 5, "title": "5. Remove CPU Tower Cooler & Heatsink", "tool": "Long Phillips Screwdriver", "action": "Unscrew cross-bracket; gently twist cooler to break thermal paste seal.", "safety": "🟢 Pure copper heatpipes & aluminum fins.", "layer_idx": 4},
            {"step": 6, "title": "6. Extract ATX Motherboard", "tool": "Magnetic Phillips #1 Screwdriver", "action": "Remove 9 ATX standoff screws; disconnect 24-pin and 8-pin power cables.", "safety": "🟢 Richest e-waste source: Gold, Silver, Palladium.", "layer_idx": 5},
            {"step": 7, "title": "7. Remove Power Supply Unit & Chassis", "tool": "Phillips #2 Screwdriver", "action": "Unscrew 4 rear PSU screws; slide out modular ATX power supply.", "safety": "⚠️ Never open the metal PSU casing.", "layer_idx": 6}
        ],
        "default": [
            {"step": 1, "title": "1. Safety Isolation & Disconnect", "tool": "ESD Safety Kit • Multimeter", "action": "Disconnect all power inputs and verify zero residual electrical charge.", "safety": "⚠️ Verify zero voltage before proceeding.", "layer_idx": 0},
            {"step": 2, "title": "2. Remove Outer Housing / Casing", "tool": "Precision Screwdriver Set", "action": "Extract external fasteners and unclip perimeter casing.", "safety": "⚠️ Sort screws by size.", "layer_idx": 1},
            {"step": 3, "title": "3. Isolate Power & Battery Modules", "tool": "Non-Conductive Spudger", "action": "Disconnect internal power supply or battery pack first.", "safety": "🔥 Prevent sparks and short circuits.", "layer_idx": 2},
            {"step": 4, "title": "4. Extract Electronic Logic PCBs", "tool": "ESD Tweezers • Spatula", "action": "Unscrew and harvest high-grade printed circuit boards.", "safety": "🟢 High recovery value: Gold, Silver, Copper.", "layer_idx": 3},
            {"step": 5, "title": "5. Recover Motors, Coils & Transformers", "tool": "Socket Wrench", "action": "Remove electric motors, copper coils, and electromagnetic units.", "safety": "🟢 Heavy metallurgical scrap value.", "layer_idx": 4},
            {"step": 6, "title": "6. Material Sorting & Hazardous Isolation", "tool": "Sorting Bins • Cut Gloves", "action": "Segregate metals, engineered plastics, and hazardous substances.", "safety": "♻️ Deliver to CPCB/R2 certified e-waste facilities.", "layer_idx": 5}
        ]
    }

    manual_steps = teardown_manuals.get(shape_type, teardown_manuals["default"])
    manual_steps_json = json.dumps(manual_steps)

    # Components list based on category
    if shape_type == "phone":
        components = [
            {"name": "1. Vegan Leather Back Cover & Halo Ring", "material": "Lychee Vegan Leather + Gold Stitched Seam", "specs": "Sunrise Beige PBR Cover with Halo Camera Island", "weight_pct": 12, "hazardous": False, "recyclable": True, "value_usd": 2.50, "color": "#D4AF37", "layer": 1},
            {"name": "2. NFC Coil & Graphite Heat Spreader", "material": "High-Conductivity Graphite + Copper NFC", "specs": "Thermal Dissipation Layer & Wireless Coil", "weight_pct": 6, "hazardous": False, "recyclable": True, "value_usd": 1.20, "color": "#2C3E50", "layer": 2},
            {"name": "3. Magnesium Shield & 16 Assembly Screws", "material": "Die-Cast Magnesium Alloy + Steel Screws", "specs": "Structural Frame Shield (Phillips #00)", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 1.80, "color": "#7F8C8D", "layer": 3},
            {"name": "4. 10-Layer Logic Board & Dimensity SoC", "material": "High-Tg Multi-layer FR4 + 18k Gold Plating", "specs": "Dimensity 7050 5G SoC + RF Cans", "weight_pct": 18, "hazardous": True, "recyclable": True, "value_usd": 14.50, "color": "#1B4332", "layer": 4},
            {"name": "5. 5000mAh High-Density Battery Cell", "material": "Lithium Cobalt Oxide + BMU Circuit", "specs": "Dual Stretch-Release Adhesive Tabs A&B", "weight_pct": 24, "hazardous": True, "recyclable": True, "value_usd": 4.80, "color": "#C0392B", "layer": 5},
            {"name": "6. Aerospace CNC Gold Aluminum Midframe", "material": "Anodized 6000-series Aluminum Alloy", "specs": "Unibody Frame + Volume/Power Rails", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 3.20, "color": "#F39C12", "layer": 6},
            {"name": "7. 120Hz Curved AMOLED & Gorilla Glass", "material": "Flexible OLED Substrate + Corning Glass", "specs": "1080x2412 Curved 120Hz AMOLED Panel", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 8.00, "color": "#2980B9", "layer": 7}
        ]
    else:
        components = device_info.get("components", [])
    if not components:
        # Fallback category components
        cat_components = {
            "laptop": [
                {"name": "Bottom Magnesium/Alloy Chassis", "material": "Magnesium-Aluminum Alloy", "specs": "CNC Precision Sub-Chassis", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 2.50, "color": "#7F8C8D", "layer": 1},
                {"name": "4-Cell Li-Po Battery Pack (54Wh)", "material": "Lithium Cobalt Oxide + BMS", "specs": "15.2V, 54Wh Pack", "weight_pct": 18, "hazardous": True, "recyclable": True, "value_usd": 4.50, "color": "#C0392B", "layer": 2},
                {"name": "Laptop Motherboard (CPU + RAM)", "material": "High-Tg Multi-layer FR4 + Gold", "specs": "Intel/AMD SoC + DDR4/DDR5", "weight_pct": 15, "hazardous": True, "recyclable": True, "value_usd": 12.00, "color": "#1B4332", "layer": 3},
                {"name": "Dual Copper Cooling Fans & Pipes", "material": "Pure Copper Sintered Heatpipe", "specs": "Dual Blower Radial Fans", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 1.80, "color": "#D35400", "layer": 4},
                {"name": "Keyboard Deck & Touchpad", "material": "ABS Plastic + Copper Membrane", "specs": "Backlit Scissor-Switch Deck", "weight_pct": 12, "hazardous": False, "recyclable": True, "value_usd": 1.20, "color": "#2C3E50", "layer": 5},
                {"name": "15.6\" IPS LCD Display Panel", "material": "Indium Tin Oxide + Polarizer Glass", "specs": "1920x1080 144Hz IPS Screen", "weight_pct": 22, "hazardous": False, "recyclable": True, "value_usd": 6.50, "color": "#2980B9", "layer": 6}
            ],
            "desktop": [
                {"name": "ATX Steel Tower Case Chassis", "material": "SPCC Cold Rolled Steel + Mesh", "specs": "Mid-Tower Steel Case", "weight_pct": 40, "hazardous": False, "recyclable": True, "value_usd": 4.00, "color": "#34495E", "layer": 1},
                {"name": "Modular ATX Power Supply (650W)", "material": "Steel + Copper Transformer + Capacitors", "specs": "80-Plus Gold 650W PSU", "weight_pct": 18, "hazardous": True, "recyclable": True, "value_usd": 5.50, "color": "#2C3E50", "layer": 2},
                {"name": "ATX Motherboard (Socket AM4/LGA)", "material": "FR4 Epoxy + 18k Gold Micro-Plating", "specs": "Chipset, PCIe slots, VRM", "weight_pct": 14, "hazardous": True, "recyclable": True, "value_usd": 14.00, "color": "#1E8449", "layer": 3},
                {"name": "CPU Tower Cooler with Fan", "material": "Pure Copper Base + Aluminum Fins", "specs": "120mm PWM Fan + 4 Heatpipes", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 2.20, "color": "#E67E22", "layer": 4},
                {"name": "Dedicated GPU Graphics Card", "material": "Silicon Die + GDDR6 + Dual Fans", "specs": "PCIe x16 Dedicated GPU", "weight_pct": 12, "hazardous": True, "recyclable": True, "value_usd": 22.00, "color": "#8E44AD", "layer": 5},
                {"name": "Tempered Glass Side Panel", "material": "4mm Tempered Glass", "specs": "UV-coated Scratch-Resistant Glass", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#5D6D7E", "layer": 6}
            ],
            "battery": [
                {"name": "Outer Heat-Shrink Sleeve", "material": "PVC / PET Thermal Shrink", "specs": "Dielectric Insulation Wrap", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 0.20, "color": "#2980B9", "layer": 1},
                {"name": "Heavy Copper Terminal Leads", "material": "High-Strand Silicone Copper Wires", "specs": "12 AWG Pure Copper + XT60", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 0.80, "color": "#E74C3C", "layer": 2},
                {"name": "Battery Management System (BMS)", "material": "FR4 PCB + Power MOSFETs + Shunt", "specs": "Over-charge & Balance Protection", "weight_pct": 12, "hazardous": True, "recyclable": True, "value_usd": 2.50, "color": "#27AE60", "layer": 3},
                {"name": "Nickel Spot-Welded Busbars", "material": "Pure Nickel 99.6% Strip", "specs": "0.15mm Low-Resistance Busbars", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#BDC3C7", "layer": 4},
                {"name": "18650 Lithium-Ion Cell Array", "material": "Lithium Nickel Manganese Cobalt (NMC)", "specs": "Rechargeable Pouch/Cylinder Cells", "weight_pct": 65, "hazardous": True, "recyclable": True, "value_usd": 8.00, "color": "#C0392B", "layer": 5}
            ],
            "pcb": [
                {"name": "10-Layer FR4 Glass Epoxy Substrate", "material": "Woven Fiberglass + Epoxy Resin", "specs": "10-Layer High-Tg Core", "weight_pct": 45, "hazardous": False, "recyclable": True, "value_usd": 3.00, "color": "#1B4F72", "layer": 1},
                {"name": "Gold-Plated Contact Fingers", "material": "18k/24k Pure Gold Electroplating", "specs": "PCIe & Memory Gold Edge Traces", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 8.50, "color": "#F1C40F", "layer": 2},
                {"name": "BGA Microprocessors & Silicon Dies", "material": "Silicon + Gold Wire Bonds + Solder", "specs": "Main Processing Unit", "weight_pct": 18, "hazardous": False, "recyclable": True, "value_usd": 9.00, "color": "#17202A", "layer": 3},
                {"name": "Surface Mount Devices (SMD Array)", "material": "Ceramic Capacitors + Resistors", "specs": "SMD 0402 / 0603 High-Density Array", "weight_pct": 18, "hazardous": True, "recyclable": True, "value_usd": 2.50, "color": "#7F8C8D", "layer": 4},
                {"name": "Aluminum Heat Sink & EMI Shields", "material": "Extruded Aluminum + Nickel Cans", "specs": "Thermal Dissipation Block", "weight_pct": 14, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#95A5A6", "layer": 5}
            ],
            "display": [
                {"name": "Rear Plastic Housing & VESA Mount", "material": "ABS Plastic + Steel VESA Bracket", "specs": "Rear Enclosure with Ventilation", "weight_pct": 30, "hazardous": False, "recyclable": True, "value_usd": 2.00, "color": "#34495E", "layer": 1},
                {"name": "LED Backlight Diffuser Panel", "material": "Acrylic Light Guide + LED Strip", "specs": "Edge-Lit LED Backlight Assembly", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 3.50, "color": "#ECF0F1", "layer": 2},
                {"name": "T-CON Controller & Power Board", "material": "FR4 PCB + Capacitors + Transformer", "specs": "Timing Controller + SMPS PSU", "weight_pct": 12, "hazardous": True, "recyclable": True, "value_usd": 6.00, "color": "#27AE60", "layer": 3},
                {"name": "Desktop Stand & Pedestal Base", "material": "Die-Cast Aluminum + Steel", "specs": "Height-Adjustable VESA Stand", "weight_pct": 18, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#7F8C8D", "layer": 4},
                {"name": "IPS/VA LCD Panel & Micro-Bezel", "material": "Indium Tin Oxide + Polarizer Glass", "specs": "2560x1440 165Hz Display Panel", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 8.00, "color": "#2980B9", "layer": 5}
            ],
            "tablet": [
                {"name": "Aluminum Rear Unibody Shell", "material": "Anodized 6000-series Aluminum", "specs": "CNC Machined Unibody Enclosure", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 3.00, "color": "#7F8C8D", "layer": 1},
                {"name": "Front Glass Digitizer & Touch Panel", "material": "Gorilla Glass + Capacitive Sensor", "specs": "Multi-Touch Digitizer Assembly", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 5.00, "color": "#2C3E50", "layer": 2},
                {"name": "Dual Battery Slab Cells", "material": "Lithium Polymer + BMS Circuit", "specs": "8000mAh Dual-Cell Li-Po Pack", "weight_pct": 22, "hazardous": True, "recyclable": True, "value_usd": 4.50, "color": "#C0392B", "layer": 3},
                {"name": "Logic Board & SoC Processor", "material": "High-Tg FR4 + Gold Micro-Plating", "specs": "Apple/Qualcomm SoC + RAM", "weight_pct": 18, "hazardous": True, "recyclable": True, "value_usd": 14.00, "color": "#1B4332", "layer": 4},
                {"name": "10.9\" IPS Retina Display Panel", "material": "IPS LCD + LED Backlight", "specs": "2360x1640 ProMotion Display", "weight_pct": 20, "hazardous": False, "recyclable": True, "value_usd": 7.50, "color": "#2980B9", "layer": 5}
            ],
            "printer": [
                {"name": "ABS Plastic Body Housing", "material": "High-Impact ABS Plastic", "specs": "Main Printer Enclosure", "weight_pct": 35, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#2C3E50", "layer": 1},
                {"name": "Paper Feed Cassette & Tray", "material": "HIPS Plastic + Steel Guides", "specs": "250-Sheet Auto-Feed Cassette", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 0.80, "color": "#ECF0F1", "layer": 2},
                {"name": "Scanner Glass Flatbed & CIS Sensor", "material": "Tempered Glass + Contact Image Sensor", "specs": "1200x2400 DPI Optical Scanner", "weight_pct": 12, "hazardous": False, "recyclable": True, "value_usd": 3.00, "color": "#85C1E9", "layer": 3},
                {"name": "Ink/Toner Cartridge Assembly", "material": "Polycarbonate + Toner Powder/Ink", "specs": "CMYK 4-Color Cartridge Set", "weight_pct": 18, "hazardous": True, "recyclable": True, "value_usd": 12.00, "color": "#1B4332", "layer": 4},
                {"name": "Drive Rollers & Stepper Motors", "material": "Steel Shafts + Copper Coil Motors", "specs": "Precision Paper Transport Assembly", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 2.50, "color": "#7F8C8D", "layer": 5}
            ],
            "cable": [
                {"name": "PVC Protective Outer Sleeve", "material": "Polyvinyl Chloride Jacket", "specs": "Flame-Retardant Insulation", "weight_pct": 25, "hazardous": False, "recyclable": True, "value_usd": 0.20, "color": "#2C3E50", "layer": 1},
                {"name": "Braided EMI Shield Layer", "material": "Tinned Copper Braid", "specs": "95% Coverage Shielding", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 0.80, "color": "#BDC3C7", "layer": 2},
                {"name": "Color-Coded Conductor Cores", "material": "THHN Insulated Copper Wire", "specs": "4x 22AWG Conductor Pairs", "weight_pct": 20, "hazardous": False, "recyclable": True, "value_usd": 1.20, "color": "#E74C3C", "layer": 3},
                {"name": "Bare Copper Core Strands", "material": "Pure Copper 99.9%", "specs": "Multi-Strand Conductor Core", "weight_pct": 30, "hazardous": False, "recyclable": True, "value_usd": 2.50, "color": "#D35400", "layer": 4},
                {"name": "Gold-Plated Connector & Pins", "material": "Zinc Alloy + Gold Electroplate", "specs": "USB-A / RJ45 / HDMI Connector", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#F1C40F", "layer": 5}
            ],
            "networking": [
                {"name": "Router Chassis & Ventilation Slots", "material": "ABS Plastic + Steel Base", "specs": "Slim Form-Factor Enclosure", "weight_pct": 30, "hazardous": False, "recyclable": True, "value_usd": 1.00, "color": "#2C3E50", "layer": 1},
                {"name": "4x External Dipole Antennas", "material": "PCB Antenna + SMA Connectors", "specs": "5dBi Dual-Band MIMO Antennas", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#34495E", "layer": 2},
                {"name": "Ethernet RJ45 & WAN Ports", "material": "Shielded RJ45 Jacks + Gold Contacts", "specs": "4x Gigabit LAN + 1x WAN Port", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 0.80, "color": "#F1C40F", "layer": 3},
                {"name": "Wi-Fi SoC Board & Heatsink", "material": "FR4 PCB + Broadcom/Qualcomm SoC", "specs": "Wi-Fi 6 AX + ARM Processor", "weight_pct": 35, "hazardous": True, "recyclable": True, "value_usd": 8.00, "color": "#27AE60", "layer": 4},
                {"name": "DC Power Jack & Reset Button", "material": "Barrel Connector + Tactile Switch", "specs": "12V/2A DC Input + WPS/Reset", "weight_pct": 7, "hazardous": False, "recyclable": True, "value_usd": 0.30, "color": "#7F8C8D", "layer": 5}
            ],
            "server": [
                {"name": "2U Rackmount Steel Chassis", "material": "Cold-Rolled Steel + Rack Ears", "specs": "2U 19\" Rack-Mountable Server", "weight_pct": 35, "hazardous": False, "recyclable": True, "value_usd": 8.00, "color": "#34495E", "layer": 1},
                {"name": "Hot-Swap SAS/SATA Drive Bays", "material": "Steel Caddies + SAS Backplane", "specs": "6x 3.5\" Hot-Swap Drive Bays", "weight_pct": 12, "hazardous": False, "recyclable": True, "value_usd": 5.00, "color": "#2C3E50", "layer": 2},
                {"name": "High-RPM Blower Fan Wall", "material": "Dual-Ball Bearing + PBT Blades", "specs": "6x 15000RPM Counter-Rotating", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 3.00, "color": "#7F8C8D", "layer": 3},
                {"name": "Dual-CPU Sockets & DIMM Array", "material": "Server FR4 PCB + Xeon/EPYC + ECC RAM", "specs": "Dual Socket + 12x DDR4 ECC", "weight_pct": 25, "hazardous": True, "recyclable": True, "value_usd": 45.00, "color": "#27AE60", "layer": 4},
                {"name": "Redundant Hot-Swap PSUs", "material": "Platinum-Rated SMPS + Gold Connectors", "specs": "2x 800W Redundant PSU Modules", "weight_pct": 20, "hazardous": True, "recyclable": True, "value_usd": 12.00, "color": "#E74C3C", "layer": 5}
            ],
            "console": [
                {"name": "Custom Console Housing Shell", "material": "High-Gloss ABS + Matte Accents", "specs": "Slim-Profile Gaming Console Body", "weight_pct": 30, "hazardous": False, "recyclable": True, "value_usd": 2.00, "color": "#2C3E50", "layer": 1},
                {"name": "Ventilation Cooling Fin Array", "material": "Stamped Aluminum Cooling Ribs", "specs": "Centrifugal Fan + Vent Ribs", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 1.50, "color": "#7F8C8D", "layer": 2},
                {"name": "Custom APU & Vapor Chamber", "material": "Silicon APU + Copper Vapor Chamber", "specs": "AMD Zen 2 APU + RDNA 2 GPU", "weight_pct": 15, "hazardous": True, "recyclable": True, "value_usd": 18.00, "color": "#D35400", "layer": 3},
                {"name": "Blu-Ray / Disc Drive Assembly", "material": "Aluminum Frame + Laser Diode", "specs": "4K UHD Blu-Ray Optical Drive", "weight_pct": 18, "hazardous": False, "recyclable": True, "value_usd": 4.00, "color": "#34495E", "layer": 4},
                {"name": "Internal PSU & Wi-Fi Module", "material": "SMPS Board + Wi-Fi 5 M.2 Card", "specs": "Internal 300W PSU + Wireless", "weight_pct": 22, "hazardous": True, "recyclable": True, "value_usd": 5.00, "color": "#1B4332", "layer": 5}
            ],
            "large_appliance": [
                {"name": "Heavy Steel Cabinet Body", "material": "Powder-Coated SPCC Steel", "specs": "Full-Size Appliance Enclosure", "weight_pct": 40, "hazardous": False, "recyclable": True, "value_usd": 6.00, "color": "#BDC3C7", "layer": 1},
                {"name": "Hermetic Compressor Motor", "material": "Copper Coil + Steel Cylinder", "specs": "R-134a/R-600a Rotary Compressor", "weight_pct": 20, "hazardous": True, "recyclable": True, "value_usd": 8.00, "color": "#34495E", "layer": 2},
                {"name": "Copper Condenser Coil Tubing", "material": "Pure Copper Serpentine Tubes", "specs": "Heat Exchange Condenser Coils", "weight_pct": 12, "hazardous": False, "recyclable": True, "value_usd": 5.50, "color": "#D35400", "layer": 3},
                {"name": "PU Foam Insulation Layer", "material": "Polyurethane Cyclopentane Foam", "specs": "CFC-Free Thermal Insulation", "weight_pct": 15, "hazardous": True, "recyclable": False, "value_usd": 0.50, "color": "#F5E6CC", "layer": 4},
                {"name": "Electronic Control Module", "material": "FR4 PCB + Relay + Thermostat", "specs": "Digital Temperature Controller", "weight_pct": 8, "hazardous": True, "recyclable": True, "value_usd": 3.00, "color": "#27AE60", "layer": 5}
            ],
            "small_appliance": [
                {"name": "Metal/Plastic Enclosure Body", "material": "Stainless Steel + ABS Plastic", "specs": "Appliance Housing with Door", "weight_pct": 35, "hazardous": False, "recyclable": True, "value_usd": 2.00, "color": "#BDC3C7", "layer": 1},
                {"name": "Control Knobs & Timer Dial", "material": "Phenolic Resin + Brass Shaft", "specs": "Mechanical Timer + Selector", "weight_pct": 5, "hazardous": False, "recyclable": True, "value_usd": 0.50, "color": "#ECF0F1", "layer": 2},
                {"name": "Magnetron / Motor Coil Assembly", "material": "Copper Coil + Ceramic + Steel", "specs": "1000W Magnetron / 750W Motor", "weight_pct": 25, "hazardous": True, "recyclable": True, "value_usd": 4.00, "color": "#7F8C8D", "layer": 3},
                {"name": "HV Transformer & Capacitor", "material": "Iron Core + Copper Winding", "specs": "Step-Up Transformer + 1.05µF HV Cap", "weight_pct": 20, "hazardous": True, "recyclable": True, "value_usd": 3.00, "color": "#34495E", "layer": 4},
                {"name": "3-Pin Grounded Power Cord", "material": "PVC Jacket + Copper Conductors", "specs": "16AWG 3-Prong Power Cable", "weight_pct": 8, "hazardous": False, "recyclable": True, "value_usd": 0.30, "color": "#2C3E50", "layer": 5}
            ]
        }
        components = cat_components.get(shape_type, [
            {"name": "Outer Enclosure / Chassis", "material": "Polycarbonate / Aluminum Alloy", "specs": "Exterior Device Shell", "weight_pct": 30, "hazardous": False, "recyclable": True, "value_usd": 2.50, "color": chassis_color, "layer": 1},
            {"name": "Internal Power / Battery Module", "material": "Li-ion / AC Transformer", "specs": "Power Circuit Unit", "weight_pct": 25, "hazardous": True, "recyclable": True, "value_usd": 3.50, "color": "#C0392B", "layer": 2},
            {"name": "Electronic Logic Motherboard", "material": "Multi-layer FR4 + Gold + Copper", "specs": "Central Processing PCB", "weight_pct": 20, "hazardous": True, "recyclable": True, "value_usd": 12.00, "color": "#1B4332", "layer": 3},
            {"name": "Display / Functional Matrix", "material": "Display Glass / Motor Coils", "specs": "Primary Output Subsystem", "weight_pct": 15, "hazardous": False, "recyclable": True, "value_usd": 4.50, "color": "#2980B9", "layer": 4},
            {"name": "Fasteners & Shielding Brackets", "material": "Stainless Steel + Copper Shield", "specs": "Internal Assembly Hardware", "weight_pct": 10, "hazardous": False, "recyclable": True, "value_usd": 1.00, "color": "#7F8C8D", "layer": 5}
        ])

    comp_data = []
    for i, comp in enumerate(components):
        comp_data.append({
            "name": comp.get("name", f"Component {i+1}"),
            "material": comp.get("material", "Composite Material"),
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
    total_val = sum(c["value_usd"] for c in comp_data)
    scrap_val_str = f"${total_val:.2f}"
    
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
    font-size: 10px;
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

/* Model Switcher Bar */
#model-switcher {{
    position: absolute;
    top: 42px;
    left: 12px;
    display: flex;
    gap: 5px;
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
    <div id="loading-overlay">⚡ GENERATING AUTHENTIC 3D HARDWARE MODEL...</div>
    <div id="toast-msg"></div>

    <!-- Top Device HUD -->
    <div id="device-hud">
        <span class="hud-brand">{brand.upper()}</span>
        <span class="hud-title">{model_name}</span>
        <span class="hud-pill">📦 {category}</span>
        <span class="hud-pill">💾 {storage}</span>
        <span class="hud-pill hud-pill-gold">💰 Scrap: {scrap_val_str}</span>
    </div>

    <!-- Model Switcher -->
    <div id="model-switcher">
        <button class="btn-asset active" id="btn-mode-cat" onclick="switchModelMode('cat')">🎯 {category} (Active)</button>
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
            <span id="step-name">Step 1</span>
            <span id="step-count" style="color:#aaa;">Physical Teardown Manual</span>
        </div>
        <div id="step-tools">🛠️ Tools...</div>
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
const SHAPE_TYPE = "{shape_type}";
const COLOR_CHASSIS = "{chassis_color}";
const COLOR_ACCENT = "{accent_color}";
const COLOR_FRAME = "{frame_color}";
const COLOR_SCREEN = "{screen_color}";

let scene, camera, renderer, rootGroup;
let meshLayers = [];
let targetExplodeRatio = 0.0;
let currentExplodeRatio = 0.0;
let isSpinning = true;
let isXRay = false;
let isManualMode = false;
let currentManualStep = 0;
let selectedMesh = null;
let raycaster, mouse;
let currentMode = 'cat';

function showToast(msg) {{
    const t = document.getElementById('toast-msg');
    t.textContent = msg;
    t.style.display = 'block';
    setTimeout(() => {{ t.style.display = 'none'; }}, 3500);
}}

function createLeatherTexture() {{
    const canvas = document.createElement('canvas');
    canvas.width = 1024;
    canvas.height = 2048;
    const ctx = canvas.getContext('2d');

    // 1. Base Pale Cream / Sunrise Beige Lychee Grain Leather
    ctx.fillStyle = '#EBE3D5';
    ctx.fillRect(0, 0, 1024, 2048);

    // Micro-pebble grain noise
    const imgData = ctx.getImageData(0, 0, 1024, 2048);
    const data = imgData.data;
    for (let i = 0; i < data.length; i += 4) {{
        const noise = (Math.random() - 0.5) * 16;
        data[i] = Math.min(255, Math.max(0, data[i] + noise));
        data[i+1] = Math.min(255, Math.max(0, data[i+1] + noise));
        data[i+2] = Math.min(255, Math.max(0, data[i+2] + noise));
    }}
    ctx.putImageData(imgData, 0, 0);

    // 2. Center Gold / Emerald Green Racing Stripe (Reference Match)
    const centerX = 512;
    const stripeWidth = 54;
    
    // Outer stitched groove shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.12)';
    ctx.fillRect(centerX - stripeWidth/2 - 4, 0, stripeWidth + 8, 2048);

    // Gold woven ribbon
    ctx.fillStyle = '#D4AF37';
    ctx.fillRect(centerX - stripeWidth/2, 0, stripeWidth, 2048);

    // Emerald green center runner stripe
    ctx.fillStyle = '#115E39';
    ctx.fillRect(centerX - 8, 0, 16, 2048);

    // Gold accent hairline
    ctx.fillStyle = '#FFD700';
    ctx.fillRect(centerX - 2, 0, 4, 2048);

    // 3. Realistic 3D Double Stitching lines along the stripe borders
    const stitchPitch = 22;
    for (let y = 10; y < 2048; y += stitchPitch) {{
        // Left stitch thread
        ctx.fillStyle = '#F5EE38';
        ctx.fillRect(centerX - stripeWidth/2 + 4, y, 6, 12);
        ctx.fillStyle = 'rgba(0,0,0,0.25)';
        ctx.fillRect(centerX - stripeWidth/2 + 4, y + 12, 6, 3); // Stitch shadow

        // Right stitch thread
        ctx.fillStyle = '#F5EE38';
        ctx.fillRect(centerX + stripeWidth/2 - 10, y, 6, 12);
        ctx.fillStyle = 'rgba(0,0,0,0.25)';
        ctx.fillRect(centerX + stripeWidth/2 - 10, y + 12, 6, 3); // Stitch shadow
    }}

    // 4. Subtle "realme" logo debossing near bottom left
    ctx.fillStyle = '#8C827A';
    ctx.font = 'bold 36px Rajdhani, sans-serif';
    ctx.fillText('realme', 110, 1820);

    const texture = new THREE.CanvasTexture(canvas);
    texture.wrapS = THREE.ClampToEdgeWrapping;
    texture.wrapT = THREE.ClampToEdgeWrapping;
    return texture;
}}

function createScreenTexture() {{
    const canvas = document.createElement('canvas');
    canvas.width = 1080;
    canvas.height = 2400;
    const ctx = canvas.getContext('2d');

    // Deep AMOLED black background with subtle wallpaper gradient
    const grad = ctx.createLinearGradient(0, 0, 1080, 2400);
    grad.addColorStop(0, '#060A12');
    grad.addColorStop(0.4, '#0D1B2A');
    grad.addColorStop(0.8, '#1B263B');
    grad.addColorStop(1, '#0A0E17');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 1080, 2400);

    // Status bar clock & icons
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 64px Rajdhani, sans-serif';
    ctx.fillText('10:24', 90, 140);

    ctx.font = '36px Rajdhani, sans-serif';
    ctx.fillText('5G  100%  ⚡', 820, 140);

    // Clean lockscreen widget
    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    ctx.font = '42px Rajdhani, sans-serif';
    ctx.fillText('E-Waste AI • Circular OS', 90, 220);

    // Punch hole selfie camera cutout at top center
    ctx.fillStyle = '#000000';
    ctx.beginPath();
    ctx.arc(540, 120, 26, 0, Math.PI * 2);
    ctx.fill();

    const texture = new THREE.CanvasTexture(canvas);
    return texture;
}}

// ═══ PROCEDURAL PCB SOLDER MASK + TRACE TEXTURE ═══
function createPCBTexture() {{
    const canvas = document.createElement('canvas');
    canvas.width = 1024;
    canvas.height = 1024;
    const ctx = canvas.getContext('2d');

    // Dark green solder mask base
    ctx.fillStyle = '#0a5c2a';
    ctx.fillRect(0, 0, 1024, 1024);

    // Copper trace grid pattern
    ctx.strokeStyle = '#B87333';
    ctx.lineWidth = 1.5;
    for (let x = 0; x < 1024; x += 32) {{
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, 1024);
        ctx.stroke();
    }}
    for (let y = 0; y < 1024; y += 32) {{
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(1024, y);
        ctx.stroke();
    }}

    // Via pads (small copper circles)
    ctx.fillStyle = '#C49A6C';
    for (let i = 0; i < 60; i++) {{
        const px = Math.random() * 1024;
        const py = Math.random() * 1024;
        ctx.beginPath();
        ctx.arc(px, py, 4, 0, Math.PI * 2);
        ctx.fill();
    }}

    // White silkscreen component outlines
    ctx.strokeStyle = 'rgba(255,255,255,0.6)';
    ctx.lineWidth = 1;
    for (let i = 0; i < 20; i++) {{
        const rx = 50 + Math.random() * 900;
        const ry = 50 + Math.random() * 900;
        ctx.strokeRect(rx, ry, 20 + Math.random() * 40, 10 + Math.random() * 20);
    }}

    return new THREE.CanvasTexture(canvas);
}}

// ═══ PROCEDURAL BRUSHED METAL TEXTURE ═══
function createBrushedMetalTexture(baseColor) {{
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 512;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = baseColor || '#888890';
    ctx.fillRect(0, 0, 512, 512);

    // Horizontal brush strokes
    const imgData = ctx.getImageData(0, 0, 512, 512);
    const data = imgData.data;
    for (let y = 0; y < 512; y++) {{
        const rowNoise = (Math.random() - 0.5) * 30;
        for (let x = 0; x < 512; x++) {{
            const idx = (y * 512 + x) * 4;
            const lineNoise = Math.sin(x * 0.5) * 5 + rowNoise;
            data[idx] = Math.min(255, Math.max(0, data[idx] + lineNoise));
            data[idx+1] = Math.min(255, Math.max(0, data[idx+1] + lineNoise));
            data[idx+2] = Math.min(255, Math.max(0, data[idx+2] + lineNoise));
        }}
    }}
    ctx.putImageData(imgData, 0, 0);

    return new THREE.CanvasTexture(canvas);
}}

// ═══ PROCEDURAL LCD/DISPLAY UI TEXTURE (for monitors, laptops, tablets) ═══
function createDisplayUITexture() {{
    const canvas = document.createElement('canvas');
    canvas.width = 1920;
    canvas.height = 1080;
    const ctx = canvas.getContext('2d');

    // Dark desktop gradient
    const grad = ctx.createLinearGradient(0, 0, 1920, 1080);
    grad.addColorStop(0, '#0a0e1a');
    grad.addColorStop(0.3, '#0d1926');
    grad.addColorStop(0.7, '#12203a');
    grad.addColorStop(1, '#080c14');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 1920, 1080);

    // Taskbar at bottom
    ctx.fillStyle = 'rgba(20, 25, 40, 0.9)';
    ctx.fillRect(0, 1030, 1920, 50);

    // Taskbar icons
    const iconColors = ['#0078D4', '#00CC6A', '#FF4444', '#FFB900', '#7B68EE'];
    iconColors.forEach((c, i) => {{
        ctx.fillStyle = c;
        ctx.beginPath();
        ctx.arc(860 + i * 45, 1055, 12, 0, Math.PI * 2);
        ctx.fill();
    }});

    // Clock in taskbar
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 18px sans-serif';
    ctx.fillText('10:24 PM', 1790, 1058);

    // Window mock
    ctx.fillStyle = 'rgba(30, 40, 60, 0.85)';
    ctx.fillRect(200, 80, 1520, 900);
    ctx.fillStyle = 'rgba(40, 50, 70, 0.95)';
    ctx.fillRect(200, 80, 1520, 36);

    // Window title
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '16px sans-serif';
    ctx.fillText('E-Waste AI Classification System', 220, 105);

    // Window controls
    ctx.fillStyle = '#FF5F56';
    ctx.beginPath(); ctx.arc(1660, 98, 7, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#FFBD2E';
    ctx.beginPath(); ctx.arc(1685, 98, 7, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#27C93F';
    ctx.beginPath(); ctx.arc(1710, 98, 7, 0, Math.PI * 2); ctx.fill();

    return new THREE.CanvasTexture(canvas);
}}

// ═══ HAZARD GLOW OUTLINE SYSTEM ═══
// Adds pulsing red wireframe outline on hazardous component layers
function applyHazardGlow(mesh, isHazardous) {{
    if (!isHazardous || !mesh) return;
    mesh.traverse(function(child) {{
        if (child.isMesh && child.geometry) {{
            const edges = new THREE.EdgesGeometry(child.geometry, 15);
            const lineMat = new THREE.LineBasicMaterial({{
                color: 0xFF2222,
                transparent: true,
                opacity: 0.6,
                linewidth: 2
            }});
            const wireframe = new THREE.LineSegments(edges, lineMat);
            wireframe.userData.isHazardWire = true;
            child.add(wireframe);
        }}
    }});
}}

function init3D() {{
    const container = document.getElementById('viewer-container');
    const width = container.clientWidth || window.innerWidth;
    const height = {height};

    scene = new THREE.Scene();
    // Cinematic depth fog
    scene.fog = new THREE.FogExp2(0x0a0a12, 0.035);

    camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 1000);
    camera.position.set(0.6, 0.4, 5.8);
    camera.lookAt(0, 0, 0);

    renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true, powerPreference: "high-performance" }});
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.3;
    renderer.outputEncoding = THREE.sRGBEncoding;
    container.appendChild(renderer.domElement);

    // ═══ CINEMATIC HDR STUDIO LIGHTING ═══
    const ambientLight = new THREE.AmbientLight(0xdde4ff, 0.55);
    scene.add(ambientLight);

    // Hemisphere sky/ground fill light
    const hemiLight = new THREE.HemisphereLight(0xc8d8ff, 0x3a2218, 0.6);
    hemiLight.position.set(0, 10, 0);
    scene.add(hemiLight);

    // Key light — main directional with sharp shadow
    const keyLight = new THREE.DirectionalLight(0xfff5e8, 1.4);
    keyLight.position.set(5, 10, 8);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.width = 2048;
    keyLight.shadow.mapSize.height = 2048;
    keyLight.shadow.camera.near = 0.5;
    keyLight.shadow.camera.far = 30;
    keyLight.shadow.camera.left = -6;
    keyLight.shadow.camera.right = 6;
    keyLight.shadow.camera.top = 6;
    keyLight.shadow.camera.bottom = -6;
    keyLight.shadow.bias = -0.0003;
    keyLight.shadow.radius = 4;
    scene.add(keyLight);

    // Rim / edge light (cool blue) from behind
    const rimLight = new THREE.DirectionalLight(0x4488ff, 0.7);
    rimLight.position.set(-6, 3, -8);
    scene.add(rimLight);

    // Warm under/bounce fill light
    const warmFill = new THREE.DirectionalLight(0xffaa44, 0.35);
    warmFill.position.set(2, -6, 3);
    scene.add(warmFill);

    // Crimson dramatic accent spot from above
    const redAccent = new THREE.SpotLight(0xDC143C, 1.8, 25, Math.PI / 5, 0.6, 1.5);
    redAccent.position.set(0, 8, 0);
    scene.add(redAccent);

    // Subtle side fill for depth
    const sideFill = new THREE.PointLight(0x66aaff, 0.3, 15);
    sideFill.position.set(-5, 2, 4);
    scene.add(sideFill);

    // ═══ SHADOW-RECEIVING GROUND PLANE ═══
    const groundGeo = new THREE.PlaneGeometry(20, 20);
    const groundMat = new THREE.ShadowMaterial({{ opacity: 0.35 }});
    const groundPlane = new THREE.Mesh(groundGeo, groundMat);
    groundPlane.rotation.x = -Math.PI / 2;
    groundPlane.position.y = -2.2;
    groundPlane.receiveShadow = true;
    scene.add(groundPlane);

    // Subtle grid overlay
    const grid = new THREE.GridHelper(12, 24, 0x222630, 0x111318);
    grid.position.y = -2.19;
    grid.material.opacity = 0.35;
    grid.material.transparent = true;
    scene.add(grid);

    // ═══ FLOATING DUST PARTICLE SYSTEM ═══
    const particleCount = 180;
    const particleGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount; i++) {{
        positions[i * 3]     = (Math.random() - 0.5) * 14;
        positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
        positions[i * 3 + 2] = (Math.random() - 0.5) * 14;
    }}
    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const particleMat = new THREE.PointsMaterial({{
        color: 0xffffff,
        size: 0.025,
        transparent: true,
        opacity: 0.4,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    }});
    const particles = new THREE.Points(particleGeo, particleMat);
    particles.userData.isParticles = true;
    scene.add(particles);

    rootGroup = new THREE.Group();
    rootGroup.rotation.y = -0.35;
    rootGroup.rotation.x = 0.08;
    scene.add(rootGroup);

    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    buildDeviceGeometry(SHAPE_TYPE);
    buildLegend();
    setupMouseAndTouch(renderer.domElement);

    document.getElementById('loading-overlay').style.display = 'none';

    // ═══ CINEMATIC ENTRANCE ANIMATION ═══
    // Start zoomed out and scaled down, then spring in
    camera.position.set(0.6, 0.4, 12.0);
    rootGroup.scale.set(0.01, 0.01, 0.01);
    let entranceProgress = 0;
    function entranceAnimate() {{
        entranceProgress += 0.018;
        if (entranceProgress >= 1.0) {{
            entranceProgress = 1.0;
            camera.position.set(0.6, 0.4, 5.8);
            rootGroup.scale.set(1, 1, 1);
            animate();
            return;
        }}
        // Spring easing
        const t = 1 - Math.pow(1 - entranceProgress, 3.5);
        camera.position.z = 12.0 + (5.8 - 12.0) * t;
        const s = t;
        rootGroup.scale.set(s, s, s);
        renderer.render(scene, camera);
        requestAnimationFrame(entranceAnimate);
    }}
    entranceAnimate();
}}

/* Universal Multi-Device Procedural Architecture Generator */
function buildDeviceGeometry(type) {{
    while (rootGroup.children.length > 0) {{
        rootGroup.remove(rootGroup.children[0]);
    }}
    meshLayers = [];

    const nLayers = COMPONENTS.length;
    const spacing = 0.85; // generous exploded depth spacing

    COMPONENTS.forEach((comp, idx) => {{
        const layerGroup = new THREE.Group();
        const assembledZ = (idx - nLayers / 2) * 0.05;
        // Explode along both Z (depth) and slightly X (lateral cascade) for phone so parts don't occlude each other
        const explodedZ = (idx - nLayers / 2) * spacing;
        const explodedX = (type === 'phone' || type === 'tablet') ? (idx - nLayers / 2) * 0.55 : 0;
        const explodedY = (type === 'phone' || type === 'tablet') ? (idx - nLayers / 2) * 0.08 : 0;
        const matColor = parseInt(comp.color.replace('#', '0x')) || 0x777777;

        let primaryMesh;

        if (type === 'laptop') {{
            // ═══ PRECISION ULTRABOOK / LAPTOP ARCHITECTURE ═══
            if (idx === 0) {{
                // ── 1. ALUMINUM BOTTOM CHASSIS ──
                primaryMesh = new THREE.Group();

                // Anodized aluminum base plate
                const baseGeo = new THREE.BoxGeometry(3.6, 0.06, 2.4);
                const baseMat = new THREE.MeshStandardMaterial({{
                    color: 0x6B6B70,
                    metalness: 0.85,
                    roughness: 0.2
                }});
                const baseMesh = new THREE.Mesh(baseGeo, baseMat);
                primaryMesh.add(baseMesh);

                // Rubber feet (4 small dark cylinders at corners)
                const footGeo = new THREE.CylinderGeometry(0.07, 0.07, 0.02, 16);
                const footMat = new THREE.MeshStandardMaterial({{
                    color: 0x18181a,
                    roughness: 0.9,
                    metalness: 0.1
                }});
                const feetCoords = [
                    [-1.5, -0.035, -0.95],
                    [1.5, -0.035, -0.95],
                    [-1.5, -0.035, 0.95],
                    [1.5, -0.035, 0.95]
                ];
                feetCoords.forEach(pos => {{
                    const foot = new THREE.Mesh(footGeo, footMat);
                    foot.position.set(pos[0], pos[1], pos[2]);
                    primaryMesh.add(foot);
                }});

                // Ventilation grille slots (thin dark rectangles on bottom)
                const ventMat = new THREE.MeshStandardMaterial({{
                    color: 0x18181d,
                    roughness: 0.75,
                    metalness: 0.4
                }});
                const ventSlotGeo = new THREE.BoxGeometry(0.9, 0.005, 0.035);
                for (let s = 0; s < 8; s++) {{
                    const zPos = -0.85 + s * 0.07;
                    const leftSlot = new THREE.Mesh(ventSlotGeo, ventMat);
                    leftSlot.position.set(-0.75, -0.031, zPos);
                    primaryMesh.add(leftSlot);

                    const rightSlot = new THREE.Mesh(ventSlotGeo, ventMat);
                    rightSlot.position.set(0.75, -0.031, zPos);
                    primaryMesh.add(rightSlot);
                }}

                // Product label area
                const labelPlate = new THREE.Mesh(
                    new THREE.BoxGeometry(0.95, 0.004, 0.42),
                    new THREE.MeshStandardMaterial({{ color: 0x242428, roughness: 0.4, metalness: 0.3 }})
                );
                labelPlate.position.set(0, -0.031, 0.15);
                primaryMesh.add(labelPlate);

                const labelBarcode = new THREE.Mesh(
                    new THREE.BoxGeometry(0.7, 0.005, 0.06),
                    new THREE.MeshStandardMaterial({{ color: 0x909098, roughness: 0.2, metalness: 0.8 }})
                );
                labelBarcode.position.set(0, -0.032, 0.15);
                primaryMesh.add(labelBarcode);

                // Side I/O port cutouts
                const portMat = new THREE.MeshStandardMaterial({{ color: 0x111114, metalness: 0.8, roughness: 0.3 }});
                const usbc1 = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.025, 0.07), portMat);
                usbc1.position.set(-1.801, 0, -0.4);
                primaryMesh.add(usbc1);
                const usbc2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.025, 0.07), portMat);
                usbc2.position.set(-1.801, 0, -0.2);
                primaryMesh.add(usbc2);
                const hdmi = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.028, 0.14), portMat);
                hdmi.position.set(1.801, 0, -0.3);
                primaryMesh.add(hdmi);

            }} else if (idx === 1) {{
                // ── 2. BATTERY PACK ──
                primaryMesh = new THREE.Group();

                // Flat Li-Po battery pack with 4 cell segments
                const batWrapMat = new THREE.MeshStandardMaterial({{
                    color: 0x1a1a20,
                    roughness: 0.65,
                    metalness: 0.25
                }});
                const cellGeo = new THREE.BoxGeometry(0.72, 0.045, 0.88);
                const cellOffsets = [-1.14, -0.38, 0.38, 1.14];
                cellOffsets.forEach(cx => {{
                    const cell = new THREE.Mesh(cellGeo, batWrapMat);
                    cell.position.set(cx, 0.025, 0.55);
                    primaryMesh.add(cell);
                }});

                // Cell seam insulation tapes
                const tapeMat = new THREE.MeshStandardMaterial({{ color: 0x111114, roughness: 0.85, metalness: 0.1 }});
                [-0.76, 0.0, 0.76].forEach(tx => {{
                    const tape = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.047, 0.90), tapeMat);
                    tape.position.set(tx, 0.025, 0.55);
                    primaryMesh.add(tape);
                }});

                // BMU flex circuit ribbon at top of battery
                const bmuPlate = new THREE.Mesh(
                    new THREE.BoxGeometry(2.1, 0.02, 0.07),
                    new THREE.MeshStandardMaterial({{ color: 0x0a3d1d, roughness: 0.4 }})
                );
                bmuPlate.position.set(0, 0.025, 0.07);
                primaryMesh.add(bmuPlate);

                // 2 connector pins (small gold cylinders)
                const pinGeo = new THREE.CylinderGeometry(0.022, 0.022, 0.05, 16);
                const pinMat = new THREE.MeshStandardMaterial({{
                    color: 0xFFD700,
                    metalness: 0.98,
                    roughness: 0.15
                }});
                const pin1 = new THREE.Mesh(pinGeo, pinMat);
                pin1.rotation.x = Math.PI / 2;
                pin1.position.set(-0.12, 0.025, 0.03);
                primaryMesh.add(pin1);

                const pin2 = new THREE.Mesh(pinGeo, pinMat);
                pin2.rotation.x = Math.PI / 2;
                pin2.position.set(0.12, 0.025, 0.03);
                primaryMesh.add(pin2);

                // Connector plug housing
                const plug = new THREE.Mesh(
                    new THREE.BoxGeometry(0.38, 0.035, 0.06),
                    new THREE.MeshStandardMaterial({{ color: 0x111111, roughness: 0.7 }})
                );
                plug.position.set(0, 0.025, 0.03);
                primaryMesh.add(plug);

                // Battery warning label (small yellow box)
                const warnLabel = new THREE.Mesh(
                    new THREE.BoxGeometry(0.55, 0.005, 0.32),
                    new THREE.MeshStandardMaterial({{ color: 0xFFD700, roughness: 0.45, metalness: 0.1 }})
                );
                warnLabel.position.set(-0.55, 0.049, 0.55);
                primaryMesh.add(warnLabel);

                // Warning hazard stripe inside label
                const warnStripe = new THREE.Mesh(
                    new THREE.BoxGeometry(0.46, 0.006, 0.04),
                    new THREE.MeshStandardMaterial({{ color: 0x111111, roughness: 0.9 }})
                );
                warnStripe.position.set(-0.55, 0.051, 0.55);
                primaryMesh.add(warnStripe);

                // Spec technical label
                const specLabel = new THREE.Mesh(
                    new THREE.BoxGeometry(0.65, 0.005, 0.30),
                    new THREE.MeshStandardMaterial({{ color: 0x2c2d33, roughness: 0.5, metalness: 0.2 }})
                );
                specLabel.position.set(0.55, 0.049, 0.55);
                primaryMesh.add(specLabel);

            }} else if (idx === 2) {{
                // ── 3. MOTHERBOARD ──
                primaryMesh = new THREE.Group();

                // Green PCB substrate
                const pcbGeo = new THREE.BoxGeometry(3.2, 0.035, 1.25);
                const pcbMat = new THREE.MeshStandardMaterial({{
                    color: 0x0a5c2a,
                    roughness: 0.35,
                    metalness: 0.25
                }});
                const pcb = new THREE.Mesh(pcbGeo, pcbMat);
                pcb.position.set(0, 0.02, -0.45);
                primaryMesh.add(pcb);

                // CPU socket (darker square)
                const cpuSocket = new THREE.Mesh(
                    new THREE.BoxGeometry(0.55, 0.025, 0.55),
                    new THREE.MeshStandardMaterial({{ color: 0x16181b, roughness: 0.4, metalness: 0.6 }})
                );
                cpuSocket.position.set(-0.45, 0.038, -0.45);
                primaryMesh.add(cpuSocket);

                // CPU silicon die
                const cpuDie = new THREE.Mesh(
                    new THREE.BoxGeometry(0.30, 0.015, 0.30),
                    new THREE.MeshStandardMaterial({{ color: 0x28384a, roughness: 0.08, metalness: 0.95 }})
                );
                cpuDie.position.set(-0.45, 0.052, -0.45);
                primaryMesh.add(cpuDie);

                // GPU / Chipset die
                const gpuDie = new THREE.Mesh(
                    new THREE.BoxGeometry(0.45, 0.025, 0.45),
                    new THREE.MeshStandardMaterial({{ color: 0x1a2430, roughness: 0.12, metalness: 0.92 }})
                );
                gpuDie.position.set(0.45, 0.038, -0.45);
                primaryMesh.add(gpuDie);

                // RAM slots (2 thin long rectangles)
                const ramSlotMat = new THREE.MeshStandardMaterial({{ color: 0x18181c, roughness: 0.6, metalness: 0.3 }});
                const ramStickMat = new THREE.MeshStandardMaterial({{ color: 0x0e4720, roughness: 0.4 }});
                const ramGoldMat = new THREE.MeshStandardMaterial({{ color: 0xFFD700, metalness: 0.98, roughness: 0.15 }});

                [-0.88, -0.72].forEach((rz, rIdx) => {{
                    // Slot socket
                    const slot = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.025, 0.12), ramSlotMat);
                    slot.position.set(-0.45, 0.038, rz);
                    primaryMesh.add(slot);

                    // RAM module PCB
                    const stick = new THREE.Mesh(new THREE.BoxGeometry(0.90, 0.02, 0.09), ramStickMat);
                    stick.position.set(-0.45, 0.048, rz);
                    primaryMesh.add(stick);

                    // Gold contact edge
                    const goldContacts = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.005, 0.018), ramGoldMat);
                    goldContacts.position.set(-0.45, 0.055, rz + 0.03);
                    primaryMesh.add(goldContacts);

                    // Memory chips on RAM
                    for (let mc = 0; mc < 4; mc++) {{
                        const mChip = new THREE.Mesh(
                            new THREE.BoxGeometry(0.12, 0.012, 0.06),
                            new THREE.MeshStandardMaterial({{ color: 0x111111, roughness: 0.8 }})
                        );
                        mChip.position.set(-0.75 + mc * 0.20, 0.058, rz);
                        primaryMesh.add(mChip);
                    }}
                }});

                // SSD slot & M.2 NVMe card
                const ssdSlot = new THREE.Mesh(
                    new THREE.BoxGeometry(0.26, 0.025, 0.08),
                    new THREE.MeshStandardMaterial({{ color: 0x202024, roughness: 0.5 }})
                );
                ssdSlot.position.set(1.15, 0.038, -0.88);
                primaryMesh.add(ssdSlot);

                const ssdCard = new THREE.Mesh(
                    new THREE.BoxGeometry(0.24, 0.018, 0.65),
                    new THREE.MeshStandardMaterial({{ color: 0x173b5e, roughness: 0.35, metalness: 0.2 }})
                );
                ssdCard.position.set(1.15, 0.042, -0.52);
                primaryMesh.add(ssdCard);

                // NAND Flash chips on SSD
                [-0.64, -0.44].forEach(cz => {{
                    const flash = new THREE.Mesh(
                        new THREE.BoxGeometry(0.20, 0.015, 0.16),
                        new THREE.MeshStandardMaterial({{ color: 0x111114, roughness: 0.7 }})
                    );
                    flash.position.set(1.15, 0.052, cz);
                    primaryMesh.add(flash);
                }});

                // SSD silver mounting screw
                const ssdScrew = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.02, 0.02, 0.02, 12),
                    new THREE.MeshStandardMaterial({{ color: 0xC0C0C0, metalness: 0.95, roughness: 0.15 }})
                );
                ssdScrew.position.set(1.15, 0.045, -0.18);
                primaryMesh.add(ssdScrew);

                // Wi-Fi chip (small square with RF metal shield)
                const wifiChip = new THREE.Mesh(
                    new THREE.BoxGeometry(0.24, 0.022, 0.24),
                    new THREE.MeshStandardMaterial({{ color: 0xDCDDE1, metalness: 0.92, roughness: 0.15 }})
                );
                wifiChip.position.set(1.22, 0.038, -0.05);
                primaryMesh.add(wifiChip);

                // Wi-Fi antenna U.FL gold micro-connectors
                const uflGeo = new THREE.CylinderGeometry(0.015, 0.015, 0.015, 12);
                const ufl1 = new THREE.Mesh(uflGeo, ramGoldMat);
                ufl1.position.set(1.16, 0.05, -0.12);
                primaryMesh.add(ufl1);
                const ufl2 = new THREE.Mesh(uflGeo, ramGoldMat);
                ufl2.position.set(1.26, 0.05, -0.12);
                primaryMesh.add(ufl2);

                // Copper heat pipe (TorusGeometry arc in copper color)
                const arcPipeGeo = new THREE.TorusGeometry(0.38, 0.028, 16, 32, Math.PI * 0.8);
                const arcPipeMat = new THREE.MeshStandardMaterial({{
                    color: 0xD35400,
                    metalness: 0.96,
                    roughness: 0.15
                }});
                const heatPipeArc = new THREE.Mesh(arcPipeGeo, arcPipeMat);
                heatPipeArc.rotation.x = Math.PI / 2;
                heatPipeArc.rotation.z = -0.4;
                heatPipeArc.position.set(-0.05, 0.05, -0.45);
                primaryMesh.add(heatPipeArc);

                // Multiple small SMD components scattered
                const smdMat = new THREE.MeshStandardMaterial({{ color: 0x8A8E94, metalness: 0.88, roughness: 0.2 }});
                const smdCapMat = new THREE.MeshStandardMaterial({{ color: 0xB8860B, metalness: 0.7, roughness: 0.3 }});
                const smdGeo = new THREE.BoxGeometry(0.045, 0.018, 0.03);

                const smdCoords = [
                    [-0.72, -0.32], [-0.78, -0.36], [-0.72, -0.42], [-0.78, -0.48],
                    [-0.15, -0.32], [-0.15, -0.42], [-0.15, -0.52], [-0.15, -0.62],
                    [0.15, -0.32], [0.15, -0.42], [0.15, -0.52], [0.15, -0.62],
                    [0.72, -0.32], [0.78, -0.36], [0.72, -0.42], [0.78, -0.48],
                    [-1.1, -0.3], [-1.1, -0.4], [-1.1, -0.5],
                    [0.9, -0.75], [0.9, -0.82], [0.9, -0.68],
                    [-0.45, -0.18], [-0.35, -0.18], [-0.55, -0.18]
                ];
                smdCoords.forEach((pt, sIdx) => {{
                    const smd = new THREE.Mesh(smdGeo, sIdx % 3 === 0 ? smdCapMat : smdMat);
                    smd.position.set(pt[0], 0.04, pt[1]);
                    primaryMesh.add(smd);
                }});

                // Power delivery ferrite chokes (VRM square inductors)
                const chokeGeo = new THREE.BoxGeometry(0.08, 0.03, 0.08);
                const chokeMat = new THREE.MeshStandardMaterial({{ color: 0x1f2327, roughness: 0.7, metalness: 0.4 }});
                for (let ck = 0; ck < 5; ck++) {{
                    const choke = new THREE.Mesh(chokeGeo, chokeMat);
                    choke.position.set(-0.75, 0.045, -0.22 - ck * 0.11);
                    primaryMesh.add(choke);
                }}

            }} else if (idx === 3) {{
                // ── 4. DUAL COOLING FANS & HEAT PIPES ──
                primaryMesh = new THREE.Group();

                const fanHousingMat = new THREE.MeshStandardMaterial({{
                    color: 0x222226,
                    metalness: 0.7,
                    roughness: 0.35
                }});
                const bladeMat = new THREE.MeshStandardMaterial({{
                    color: 0x484850,
                    metalness: 0.5,
                    roughness: 0.45
                }});
                const copperMat = new THREE.MeshStandardMaterial({{
                    color: 0xD35400,
                    metalness: 0.96,
                    roughness: 0.18
                }});

                // Two fan centers
                const fanCenters = [-1.15, 1.15];

                fanCenters.forEach(cx => {{
                    // Radial fan housing shroud
                    const shroudRing = new THREE.Mesh(
                        new THREE.TorusGeometry(0.38, 0.04, 16, 48),
                        fanHousingMat
                    );
                    shroudRing.rotation.x = Math.PI / 2;
                    shroudRing.position.set(cx, 0.02, -0.65);
                    primaryMesh.add(shroudRing);

                    // Central hub
                    const hub = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.12, 0.12, 0.05, 24),
                        fanHousingMat
                    );
                    hub.position.set(cx, 0.02, -0.65);
                    primaryMesh.add(hub);

                    // 7 thin BoxGeometry blades arranged in a circle using Math.cos/sin
                    const bladeGeo = new THREE.BoxGeometry(0.025, 0.042, 0.22);
                    for (let b = 0; b < 7; b++) {{
                        const angle = (b / 7) * Math.PI * 2;
                        const blade = new THREE.Mesh(bladeGeo, bladeMat);
                        const radius = 0.22;
                        blade.position.set(
                            cx + Math.cos(angle) * radius,
                            0.02,
                            -0.65 + Math.sin(angle) * radius
                        );
                        blade.rotation.y = -angle + 0.38;
                        primaryMesh.add(blade);
                    }}

                    // Rear exhaust radiator fins
                    const radFins = new THREE.Mesh(
                        new THREE.BoxGeometry(0.68, 0.055, 0.12),
                        new THREE.MeshStandardMaterial({{ color: 0x1f1f22, metalness: 0.85, roughness: 0.3 }})
                    );
                    radFins.position.set(cx, 0.02, -1.02);
                    primaryMesh.add(radFins);
                }});

                // 2 copper heat pipes connecting the cooling system (thin cylinders)
                const pipe1 = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.028, 0.028, 2.3, 16),
                    copperMat
                );
                pipe1.rotation.z = Math.PI / 2;
                pipe1.position.set(0, 0.042, -0.58);
                primaryMesh.add(pipe1);

                const pipe2 = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.028, 0.028, 2.3, 16),
                    copperMat
                );
                pipe2.rotation.z = Math.PI / 2;
                pipe2.position.set(0, 0.042, -0.72);
                primaryMesh.add(pipe2);

                // Thermal cold plates over CPU and GPU contact spots
                const cpuPlate = new THREE.Mesh(
                    new THREE.BoxGeometry(0.55, 0.025, 0.55),
                    copperMat
                );
                cpuPlate.position.set(-0.45, 0.03, -0.55);
                primaryMesh.add(cpuPlate);

                const gpuPlate = new THREE.Mesh(
                    new THREE.BoxGeometry(0.48, 0.025, 0.48),
                    copperMat
                );
                gpuPlate.position.set(0.45, 0.03, -0.55);
                primaryMesh.add(gpuPlate);

            }} else if (idx === 4) {{
                // ── 5. KEYBOARD DECK WITH INDIVIDUAL KEYS ──
                primaryMesh = new THREE.Group();

                // Top unibody palmrest deck plate
                const deckGeo = new THREE.BoxGeometry(3.6, 0.05, 2.4);
                const deckMat = new THREE.MeshStandardMaterial({{
                    color: 0x2A2A2E,
                    metalness: 0.8,
                    roughness: 0.25
                }});
                const deck = new THREE.Mesh(deckGeo, deckMat);
                deck.position.set(0, 0, 0);
                primaryMesh.add(deck);

                // Recessed keyboard tray well
                const well = new THREE.Mesh(
                    new THREE.BoxGeometry(2.92, 0.015, 1.24),
                    new THREE.MeshStandardMaterial({{ color: 0x18181b, roughness: 0.8, metalness: 0.2 }})
                );
                well.position.set(0, 0.02, -0.42);
                primaryMesh.add(well);

                // Grid of small raised keys (6 rows x 14 cols of tiny BoxGeometry 0.16x0.03x0.16 with gaps)
                const keyGeo = new THREE.BoxGeometry(0.16, 0.03, 0.16);
                const keyMat = new THREE.MeshStandardMaterial({{
                    color: 0x141416,
                    roughness: 0.55,
                    metalness: 0.18
                }});

                const colPitch = 0.195;
                const rowPitch = 0.19;
                const startX = -((13 * colPitch) / 2);
                const startZ = -0.42 - ((5 * rowPitch) / 2);

                for (let r = 0; r < 6; r++) {{
                    for (let c = 0; c < 14; c++) {{
                        // Elongated spacebar on row 5 across center keys
                        if (r === 5 && c >= 4 && c <= 8) {{
                            if (c === 6) {{
                                const spacebar = new THREE.Mesh(
                                    new THREE.BoxGeometry(colPitch * 5 - 0.035, 0.03, 0.16),
                                    keyMat
                                );
                                spacebar.position.set(0, 0.038, startZ + r * rowPitch);
                                primaryMesh.add(spacebar);
                            }}
                            continue;
                        }}

                        const kx = startX + c * colPitch;
                        const kz = startZ + r * rowPitch;
                        const key = new THREE.Mesh(keyGeo, keyMat);
                        key.position.set(kx, 0.038, kz);
                        primaryMesh.add(key);
                    }}
                }}

                // Trackpad (smooth rectangle below keys)
                const trackpad = new THREE.Mesh(
                    new THREE.BoxGeometry(1.2, 0.008, 0.78),
                    new THREE.MeshStandardMaterial({{
                        color: 0x38383D,
                        roughness: 0.15,
                        metalness: 0.75
                    }})
                );
                trackpad.position.set(0, 0.026, 0.55);
                primaryMesh.add(trackpad);

                // Subtle chamfered rim around trackpad
                const padRim = new THREE.Mesh(
                    new THREE.BoxGeometry(1.22, 0.005, 0.80),
                    new THREE.MeshStandardMaterial({{ color: 0x55555C, metalness: 0.9, roughness: 0.2 }})
                );
                padRim.position.set(0, 0.024, 0.55);
                primaryMesh.add(padRim);

                // Speaker grilles (tiny dot pattern flanking keyboard)
                const dotMat = new THREE.MeshStandardMaterial({{ color: 0x111113, roughness: 0.9, metalness: 0.3 }});
                const dotGeo = new THREE.CylinderGeometry(0.012, 0.012, 0.006, 8);
                [-1.56, 1.56].forEach(sideX => {{
                    for (let dr = 0; dr < 12; dr++) {{
                        for (let dc = 0; dc < 2; dc++) {{
                            const dot = new THREE.Mesh(dotGeo, dotMat);
                            dot.position.set(sideX + (dc - 0.5) * 0.045, 0.026, -0.8 + dr * 0.07);
                            primaryMesh.add(dot);
                        }}
                    }}
                }});

                // Power button (small circle, accent color)
                const pwrButton = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.065, 0.065, 0.015, 24),
                    new THREE.MeshStandardMaterial({{
                        color: 0x00E5FF,
                        emissive: 0x00A0B0,
                        emissiveIntensity: 0.45,
                        roughness: 0.2,
                        metalness: 0.8
                    }})
                );
                pwrButton.position.set(1.32, 0.03, -0.92);
                primaryMesh.add(pwrButton);

            }} else {{
                // ── 6. DISPLAY LID WITH SCREEN ──
                primaryMesh = new THREE.Group();
                primaryMesh.position.set(0, 0.05, -1.2);
                primaryMesh.rotation.x = -Math.PI / 8;

                // Thin aluminum lid (outer back shell)
                const lidMat = new THREE.MeshStandardMaterial({{
                    color: 0x5a5a60,
                    metalness: 0.88,
                    roughness: 0.22
                }});
                const lid = new THREE.Mesh(new THREE.BoxGeometry(3.6, 2.3, 0.04), lidMat);
                lid.position.set(0, 1.15, -0.015);
                primaryMesh.add(lid);

                // Reflective brand logo on back of lid
                const logo = new THREE.Mesh(
                    new THREE.BoxGeometry(0.32, 0.32, 0.005),
                    new THREE.MeshStandardMaterial({{ color: 0xFFFFFF, metalness: 0.98, roughness: 0.1 }})
                );
                logo.position.set(0, 1.15, -0.038);
                primaryMesh.add(logo);

                // Display bezel (thin frame)
                const bezelMat = new THREE.MeshStandardMaterial({{
                    color: 0x141416,
                    roughness: 0.65,
                    metalness: 0.3
                }});

                // Top bezel bar
                const topBezel = new THREE.Mesh(new THREE.BoxGeometry(3.56, 0.14, 0.02), bezelMat);
                topBezel.position.set(0, 2.22, 0.01);
                primaryMesh.add(topBezel);

                // Bottom chin bezel bar
                const btmBezel = new THREE.Mesh(new THREE.BoxGeometry(3.56, 0.22, 0.02), bezelMat);
                btmBezel.position.set(0, 0.11, 0.01);
                primaryMesh.add(btmBezel);

                // Left and right bezel bars
                const leftBezel = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.98, 0.02), bezelMat);
                leftBezel.position.set(-1.72, 1.16, 0.01);
                primaryMesh.add(leftBezel);

                const rightBezel = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.98, 0.02), bezelMat);
                rightBezel.position.set(1.72, 1.16, 0.01);
                primaryMesh.add(rightBezel);

                // Front screen (dark rectangle with slight blue gradient emissive glow)
                const screenMat = new THREE.MeshStandardMaterial({{
                    color: 0x071426,
                    emissive: 0x0a2540,
                    emissiveIntensity: 0.38,
                    roughness: 0.08,
                    metalness: 0.85
                }});
                const screen = new THREE.Mesh(new THREE.BoxGeometry(3.32, 1.96, 0.015), screenMat);
                screen.position.set(0, 1.16, 0.015);
                primaryMesh.add(screen);

                // Webcam dot (tiny sphere at top center)
                const webcam = new THREE.Mesh(
                    new THREE.SphereGeometry(0.022, 16, 16),
                    new THREE.MeshStandardMaterial({{ color: 0x050508, roughness: 0.1, metalness: 0.9 }})
                );
                webcam.position.set(0, 2.22, 0.022);
                primaryMesh.add(webcam);

                // Webcam green indicator LED dot
                const camLed = new THREE.Mesh(
                    new THREE.SphereGeometry(0.007, 12, 12),
                    new THREE.MeshStandardMaterial({{
                        color: 0x00FF66,
                        emissive: 0x00FF66,
                        emissiveIntensity: 0.7
                    }})
                );
                camLed.position.set(0.06, 2.22, 0.022);
                primaryMesh.add(camLed);

                // Hinge cylinders at bottom
                const hingeMat = new THREE.MeshStandardMaterial({{
                    color: 0x888890,
                    metalness: 0.95,
                    roughness: 0.15
                }});
                const hingeGeo = new THREE.CylinderGeometry(0.045, 0.045, 0.45, 24);

                const leftHinge = new THREE.Mesh(hingeGeo, hingeMat);
                leftHinge.rotation.z = Math.PI / 2;
                leftHinge.position.set(-1.2, 0.0, 0.0);
                primaryMesh.add(leftHinge);

                const rightHinge = new THREE.Mesh(hingeGeo, hingeMat);
                rightHinge.rotation.z = Math.PI / 2;
                rightHinge.position.set(1.2, 0.0, 0.0);
                primaryMesh.add(rightHinge);
            }}

        }} else if (type === 'desktop') {{
            // ═══ FULLY REALISTIC ATX DESKTOP PC TOWER ═══
            if (idx === 0) {{
                // ── LAYER 0: ATX STEEL CASE BODY ──
                primaryMesh = new THREE.Group();

                const caseSteelMat = new THREE.MeshStandardMaterial({{
                    color: 0x1a1c22,
                    metalness: 0.9,
                    roughness: 0.32
                }});
                const darkMetalMat = new THREE.MeshStandardMaterial({{
                    color: 0x0f1115,
                    metalness: 0.92,
                    roughness: 0.45
                }});
                const darkCutoutMat = new THREE.MeshStandardMaterial({{
                    color: 0x08090c,
                    metalness: 0.7,
                    roughness: 0.8
                }});
                const ledEmissiveMat = new THREE.MeshStandardMaterial({{
                    color: 0x00E5FF,
                    emissive: 0x00E5FF,
                    emissiveIntensity: 0.95,
                    roughness: 0.2
                }});

                // Top Panel
                const topPanel = new THREE.Mesh(new THREE.BoxGeometry(1.64, 0.08, 3.24), caseSteelMat);
                topPanel.position.set(0, 1.66, 0);
                primaryMesh.add(topPanel);

                // Bottom Panel
                const botPanel = new THREE.Mesh(new THREE.BoxGeometry(1.64, 0.08, 3.24), caseSteelMat);
                botPanel.position.set(0, -1.66, 0);
                primaryMesh.add(botPanel);

                // Right Steel Side Panel (Motherboard Tray Side)
                const rightPanel = new THREE.Mesh(new THREE.BoxGeometry(0.06, 3.24, 3.08), caseSteelMat);
                rightPanel.position.set(-0.79, 0, 0);
                primaryMesh.add(rightPanel);

                // Motherboard Mounting Tray
                const mbTray = new THREE.Mesh(new THREE.BoxGeometry(0.04, 2.5, 2.5), darkMetalMat);
                mbTray.position.set(-0.62, 0.35, 0);
                primaryMesh.add(mbTray);

                // PSU Chamber Shroud / Basement
                const psuShroud = new THREE.Mesh(new THREE.BoxGeometry(1.58, 0.06, 3.12), darkMetalMat);
                psuShroud.position.set(0, -0.72, 0);
                primaryMesh.add(psuShroud);

                // Rear Chassis Panel
                const rearPanel = new THREE.Mesh(new THREE.BoxGeometry(1.64, 3.24, 0.08), caseSteelMat);
                rearPanel.position.set(0, 0, -1.58);
                primaryMesh.add(rearPanel);

                // Rear I/O Cutout (Rectangle)
                const rearIoCutout = new THREE.Mesh(new THREE.BoxGeometry(0.55, 1.45, 0.09), darkCutoutMat);
                rearIoCutout.position.set(0.22, 0.45, -1.58);
                primaryMesh.add(rearIoCutout);

                // Rear PCIe Expansion Slot Cutout
                const rearPcieCutout = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.78, 0.09), darkCutoutMat);
                rearPcieCutout.position.set(0.22, -0.38, -1.58);
                primaryMesh.add(rearPcieCutout);

                // Rear PSU Cutout Opening
                const rearPsuCutout = new THREE.Mesh(new THREE.BoxGeometry(1.38, 0.88, 0.09), darkCutoutMat);
                rearPsuCutout.position.set(0, -1.16, -1.58);
                primaryMesh.add(rearPsuCutout);

                // Front Panel Frame
                const frontPanel = new THREE.Mesh(new THREE.BoxGeometry(1.64, 3.4, 0.12), caseSteelMat);
                frontPanel.position.set(0, 0, 1.62);
                primaryMesh.add(frontPanel);

                // Front Mesh Ventilation Intake Bay
                const frontVentBay = new THREE.Mesh(new THREE.BoxGeometry(1.24, 2.6, 0.04), darkMetalMat);
                frontVentBay.position.set(0, 0, 1.67);
                primaryMesh.add(frontVentBay);

                // Front Mesh Ventilation (Grid of small holes using BoxGeometry)
                const ventHoleGeo = new THREE.BoxGeometry(0.12, 0.15, 0.05);
                for (let vr = 0; vr < 10; vr++) {{
                    for (let vc = 0; vc < 6; vc++) {{
                        const vHole = new THREE.Mesh(ventHoleGeo, darkCutoutMat);
                        vHole.position.set(-0.45 + vc * 0.18, -0.9 + vr * 0.20, 1.68);
                        primaryMesh.add(vHole);
                    }}
                }}

                // Side Panel Mounting Screw Holes (4 Small Cylinders)
                const screwHoleGeo = new THREE.CylinderGeometry(0.035, 0.035, 0.04, 16);
                screwHoleGeo.rotateZ(Math.PI / 2);
                const screwHoleMat = new THREE.MeshStandardMaterial({{ color: 0x050608, metalness: 0.95, roughness: 0.2 }});
                const shPositions = [
                    [0.80, 1.45, 1.35],
                    [0.80, 1.45, -1.35],
                    [0.80, -1.45, 1.35],
                    [0.80, -1.45, -1.35]
                ];
                shPositions.forEach(pos => {{
                    const sh = new THREE.Mesh(screwHoleGeo, screwHoleMat);
                    sh.position.set(pos[0], pos[1], pos[2]);
                    primaryMesh.add(sh);
                }});

                // Power Button on Top (Small cylinder with LED glow emissive)
                const powerRing = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.09, 0.09, 0.03, 24),
                    new THREE.MeshStandardMaterial({{ color: 0x333742, metalness: 0.9, roughness: 0.2 }})
                );
                powerRing.position.set(0.55, 1.71, 1.25);
                primaryMesh.add(powerRing);

                const powerButton = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.065, 0.065, 0.04, 24),
                    ledEmissiveMat
                );
                powerButton.position.set(0.55, 1.72, 1.25);
                primaryMesh.add(powerButton);

                // Top I/O USB Ports
                const usbMat = new THREE.MeshStandardMaterial({{ color: 0x0077ff, metalness: 0.3, roughness: 0.4 }});
                const usb1 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.03, 0.12), usbMat);
                usb1.position.set(0.55, 1.71, 0.95);
                primaryMesh.add(usb1);
                const usb2 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.03, 0.12), usbMat);
                usb2.position.set(0.55, 1.71, 0.75);
                primaryMesh.add(usb2);

                // 4 Case Feet
                const footGeo = new THREE.CylinderGeometry(0.10, 0.10, 0.12, 16);
                const footMat = new THREE.MeshStandardMaterial({{ color: 0x111215, roughness: 0.6, metalness: 0.5 }});
                [[-0.65, 1.35], [0.65, 1.35], [-0.65, -1.35], [0.65, -1.35]].forEach(coord => {{
                    const foot = new THREE.Mesh(footGeo, footMat);
                    foot.position.set(coord[0], -1.74, coord[1]);
                    primaryMesh.add(foot);
                }});

            }} else if (idx === 1) {{
                // ── LAYER 1: MODULAR PSU ──
                primaryMesh = new THREE.Group();

                const psuMat = new THREE.MeshStandardMaterial({{
                    color: 0x111115,
                    metalness: 0.88,
                    roughness: 0.35
                }});
                const goldLabelMat = new THREE.MeshStandardMaterial({{
                    color: 0xD4AF37,
                    metalness: 0.92,
                    roughness: 0.25,
                    emissive: 0x3d3000,
                    emissiveIntensity: 0.25
                }});
                const powerSwitchMat = new THREE.MeshStandardMaterial({{
                    color: 0xd63031,
                    roughness: 0.35,
                    metalness: 0.15
                }});
                const socketMat = new THREE.MeshStandardMaterial({{
                    color: 0x222630,
                    metalness: 0.4,
                    roughness: 0.5
                }});
                const psuHoleMat = new THREE.MeshStandardMaterial({{
                    color: 0x050608,
                    metalness: 0.9,
                    roughness: 0.8
                }});

                // PSU Main Steel Box
                const psuBox = new THREE.Mesh(new THREE.BoxGeometry(1.38, 0.84, 1.45), psuMat);
                primaryMesh.add(psuBox);

                // Honeycomb Fan Grille (Circle of small holes on top)
                const grilleRim = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.48, 0.48, 0.02, 32),
                    new THREE.MeshStandardMaterial({{ color: 0x222630, metalness: 0.92, roughness: 0.25 }})
                );
                grilleRim.position.set(0, 0.425, 0);
                primaryMesh.add(grilleRim);

                const fanHub = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.14, 0.14, 0.025, 24),
                    new THREE.MeshStandardMaterial({{ color: 0x0d0e12, metalness: 0.95, roughness: 0.2 }})
                );
                fanHub.position.set(0, 0.43, 0);
                primaryMesh.add(fanHub);

                // Inner circle of small holes
                for (let h = 0; h < 8; h++) {{
                    const ang = (h / 8) * Math.PI * 2;
                    const hole = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.025, 0.045), psuHoleMat);
                    hole.position.set(Math.cos(ang) * 0.22, 0.43, Math.sin(ang) * 0.22);
                    primaryMesh.add(hole);
                }}
                // Middle circle of small holes
                for (let h = 0; h < 12; h++) {{
                    const ang = (h / 12) * Math.PI * 2 + 0.26;
                    const hole = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.025, 0.045), psuHoleMat);
                    hole.position.set(Math.cos(ang) * 0.33, 0.43, Math.sin(ang) * 0.33);
                    primaryMesh.add(hole);
                }}
                // Outer circle of small holes
                for (let h = 0; h < 16; h++) {{
                    const ang = (h / 16) * Math.PI * 2;
                    const hole = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.025, 0.045), psuHoleMat);
                    hole.position.set(Math.cos(ang) * 0.43, 0.43, Math.sin(ang) * 0.43);
                    primaryMesh.add(hole);
                }}

                // Modular Cable Connectors (Row of small rectangles on front side)
                const rowConnGeo = new THREE.BoxGeometry(0.16, 0.12, 0.04);
                [-0.42, -0.14, 0.14, 0.42].forEach(cx => {{
                    const conn = new THREE.Mesh(rowConnGeo, socketMat);
                    conn.position.set(cx, 0.16, 0.73);
                    primaryMesh.add(conn);
                }});
                // 24-Pin ATX connector block on modular panel
                const atxConn = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.13, 0.04), socketMat);
                atxConn.position.set(-0.25, -0.12, 0.73);
                primaryMesh.add(atxConn);
                // Peripheral/SATA modular sockets
                [0.15, 0.35].forEach(cx => {{
                    const sataConn = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.10, 0.04), socketMat);
                    sataConn.position.set(cx, -0.12, 0.73);
                    primaryMesh.add(sataConn);
                }});

                // Power Switch (Tiny red rectangle on rear side)
                const switchBezel = new THREE.Mesh(
                    new THREE.BoxGeometry(0.12, 0.16, 0.03),
                    new THREE.MeshStandardMaterial({{ color: 0x1c1e24, roughness: 0.5 }})
                );
                switchBezel.position.set(0.28, 0.12, -0.73);
                primaryMesh.add(switchBezel);

                const powerSwitch = new THREE.Mesh(
                    new THREE.BoxGeometry(0.07, 0.11, 0.04),
                    powerSwitchMat
                );
                powerSwitch.position.set(0.28, 0.12, -0.74);
                primaryMesh.add(powerSwitch);

                // AC Kettle Input Socket
                const acSocket = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.16, 0.04), socketMat);
                acSocket.position.set(-0.26, 0.0, -0.73);
                primaryMesh.add(acSocket);

                // 80 Plus Gold Label (Small gold rectangle on visible side)
                const goldBadge = new THREE.Mesh(
                    new THREE.BoxGeometry(0.02, 0.28, 0.46),
                    goldLabelMat
                );
                goldBadge.position.set(0.695, 0.08, 0.0);
                primaryMesh.add(goldBadge);

                const goldBadgeInner = new THREE.Mesh(
                    new THREE.BoxGeometry(0.025, 0.22, 0.38),
                    new THREE.MeshStandardMaterial({{ color: 0x111115, metalness: 0.8, roughness: 0.4 }})
                );
                goldBadgeInner.position.set(0.698, 0.08, 0.0);
                primaryMesh.add(goldBadgeInner);

                primaryMesh.position.set(0, -1.18, 0.15);

            }} else if (idx === 2) {{
                // ── LAYER 2: ATX MOTHERBOARD ──
                primaryMesh = new THREE.Group();

                const pcbMat = new THREE.MeshStandardMaterial({{
                    color: 0x0a5c2a,
                    roughness: 0.35,
                    metalness: 0.25
                }});
                const socketMat = new THREE.MeshStandardMaterial({{
                    color: 0xc8ccd4,
                    metalness: 0.95,
                    roughness: 0.2
                }});
                const pinGridMat = new THREE.MeshStandardMaterial({{
                    color: 0x121316,
                    metalness: 0.6,
                    roughness: 0.4
                }});
                const goldContactMat = new THREE.MeshStandardMaterial({{
                    color: 0xD4AF37,
                    metalness: 0.98,
                    roughness: 0.15
                }});
                const aluminumMat = new THREE.MeshStandardMaterial({{
                    color: 0x95a5a6,
                    metalness: 0.95,
                    roughness: 0.2
                }});
                const darkPlasticMat = new THREE.MeshStandardMaterial({{
                    color: 0x1a1c22,
                    roughness: 0.5,
                    metalness: 0.3
                }});
                const ioShieldMat = new THREE.MeshStandardMaterial({{
                    color: 0xb4b9c2,
                    metalness: 0.96,
                    roughness: 0.18
                }});

                // Large Main PCB
                const pcb = new THREE.Mesh(new THREE.BoxGeometry(0.04, 2.3, 2.3), pcbMat);
                primaryMesh.add(pcb);

                // Visible CPU Socket (Square with grid of tiny holes)
                const socketFrame = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.72, 0.72), socketMat);
                socketFrame.position.set(0.025, 0.45, -0.22);
                primaryMesh.add(socketFrame);

                const socketBed = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.54, 0.54), pinGridMat);
                socketBed.position.set(0.028, 0.45, -0.22);
                primaryMesh.add(socketBed);

                // Grid of tiny pin holes
                const pinHoleGeo = new THREE.BoxGeometry(0.04, 0.05, 0.05);
                for (let r = 0; r < 5; r++) {{
                    for (let c = 0; c < 5; c++) {{
                        const pinHole = new THREE.Mesh(pinHoleGeo, goldContactMat);
                        pinHole.position.set(0.035, 0.45 - 0.20 + r * 0.10, -0.22 - 0.20 + c * 0.10);
                        primaryMesh.add(pinHole);
                    }}
                }}

                // 4 RAM Slots (Long thin raised rectangles)
                for (let ram = 0; ram < 4; ram++) {{
                    const ramSlot = new THREE.Mesh(
                        new THREE.BoxGeometry(0.05, 0.86, 0.055),
                        darkPlasticMat
                    );
                    ramSlot.position.set(0.03, 0.45, 0.32 + ram * 0.12);
                    primaryMesh.add(ramSlot);

                    const clipTop = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.08, 0.065), socketMat);
                    clipTop.position.set(0.035, 0.88, 0.32 + ram * 0.12);
                    primaryMesh.add(clipTop);
                    const clipBot = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.08, 0.065), socketMat);
                    clipBot.position.set(0.035, 0.02, 0.32 + ram * 0.12);
                    primaryMesh.add(clipBot);
                }}

                // 24-Pin ATX Power Connector
                const atxPower = new THREE.Mesh(
                    new THREE.BoxGeometry(0.06, 0.68, 0.16),
                    darkPlasticMat
                );
                atxPower.position.set(0.04, 0.45, 0.98);
                primaryMesh.add(atxPower);

                // PCIe x16 Slot (Long slot)
                const pcieSlot = new THREE.Mesh(
                    new THREE.BoxGeometry(0.05, 0.08, 1.15),
                    new THREE.MeshStandardMaterial({{ color: 0x222630, metalness: 0.85, roughness: 0.3 }})
                );
                pcieSlot.position.set(0.035, -0.15, -0.15);
                primaryMesh.add(pcieSlot);

                const pcieLock = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.09, 0.10), socketMat);
                pcieLock.position.set(0.04, -0.15, 0.45);
                primaryMesh.add(pcieLock);

                // Chipset Heatsink (Small aluminum block)
                const chipsetBlock = new THREE.Mesh(
                    new THREE.BoxGeometry(0.09, 0.48, 0.48),
                    aluminumMat
                );
                chipsetBlock.position.set(0.05, -0.55, 0.55);
                primaryMesh.add(chipsetBlock);

                // Chipset heatsink cooling ridges
                for (let cr = 0; cr < 3; cr++) {{
                    const ridge = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.04, 0.42), aluminumMat);
                    ridge.position.set(0.05, -0.65 + cr * 0.10, 0.55);
                    primaryMesh.add(ridge);
                }}

                // VRM Heatsink Blocks
                const vrmTop = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.18, 0.68), aluminumMat);
                vrmTop.position.set(0.05, 0.92, -0.22);
                primaryMesh.add(vrmTop);
                const vrmLeft = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.68, 0.18), aluminumMat);
                vrmLeft.position.set(0.05, 0.45, -0.68);
                primaryMesh.add(vrmLeft);

                // Rear I/O Shield with Ports (USB, audio circles)
                const ioShield = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.45, 0.10), ioShieldMat);
                ioShield.position.set(0.03, 0.45, -1.14);
                primaryMesh.add(ioShield);

                // USB Ports
                const usbPortGeo = new THREE.BoxGeometry(0.09, 0.12, 0.07);
                const usbPortMat = new THREE.MeshStandardMaterial({{ color: 0x050608, roughness: 0.5 }});
                [0.85, 0.65, 0.45].forEach(uy => {{
                    const usb = new THREE.Mesh(usbPortGeo, usbPortMat);
                    usb.position.set(0.04, uy, -1.14);
                    primaryMesh.add(usb);
                }});

                // Audio Circles (3.5mm jacks)
                const audioGeo = new THREE.CylinderGeometry(0.035, 0.035, 0.09, 16);
                audioGeo.rotateX(Math.PI / 2);
                const audioColors = [0x00FF7F, 0xFF1493, 0x00BFFF];
                [-0.05, -0.16, -0.27].forEach((ay, aidx) => {{
                    const jack = new THREE.Mesh(
                        audioGeo,
                        new THREE.MeshStandardMaterial({{ color: audioColors[aidx], metalness: 0.8, roughness: 0.3 }})
                    );
                    jack.position.set(0.04, ay, -1.14);
                    primaryMesh.add(jack);
                }});

                primaryMesh.position.set(-0.6, 0.3, 0);

            }} else if (idx === 3) {{
                // ── LAYER 3: CPU TOWER COOLER & FAN ──
                primaryMesh = new THREE.Group();

                const finMat = new THREE.MeshStandardMaterial({{
                    color: 0xC0C0C8,
                    metalness: 0.94,
                    roughness: 0.18
                }});
                const copperMat = new THREE.MeshStandardMaterial({{
                    color: 0xB87333,
                    metalness: 0.96,
                    roughness: 0.22
                }});
                const fanFrameMat = new THREE.MeshStandardMaterial({{
                    color: 0x16181d,
                    metalness: 0.75,
                    roughness: 0.4
                }});
                const bladeMat = new THREE.MeshStandardMaterial({{
                    color: 0x242833,
                    metalness: 0.5,
                    roughness: 0.35
                }});

                // Copper Base Plate
                const copperBase = new THREE.Mesh(
                    new THREE.BoxGeometry(0.58, 0.08, 0.58),
                    copperMat
                );
                copperBase.position.set(0, -0.42, 0);
                primaryMesh.add(copperBase);

                // 4 Copper Heatpipes rising through fins
                const pipeGeo = new THREE.CylinderGeometry(0.026, 0.026, 0.88, 16);
                [[-0.16, -0.16], [-0.16, 0.16], [0.16, -0.16], [0.16, 0.16]].forEach(coord => {{
                    const pipe = new THREE.Mesh(pipeGeo, copperMat);
                    pipe.position.set(coord[0], 0.02, coord[1]);
                    primaryMesh.add(pipe);
                }});

                // Tall Heatsink Tower with Aluminum Fins (Stack of 8 BoxGeometry slabs)
                for (let f = 0; f < 8; f++) {{
                    const finSlab = new THREE.Mesh(
                        new THREE.BoxGeometry(0.68, 0.038, 0.68),
                        finMat
                    );
                    finSlab.position.set(0, -0.32 + f * 0.10, 0);
                    primaryMesh.add(finSlab);
                }}

                // Top Fin Cover Plate
                const topFinPlate = new THREE.Mesh(
                    new THREE.BoxGeometry(0.70, 0.045, 0.70),
                    new THREE.MeshStandardMaterial({{ color: 0x181a20, metalness: 0.95, roughness: 0.2 }})
                );
                topFinPlate.position.set(0, 0.44, 0);
                primaryMesh.add(topFinPlate);

                // Attached 120mm Fan Outer Frame
                const fanFrame = new THREE.Mesh(
                    new THREE.BoxGeometry(0.70, 0.70, 0.08),
                    fanFrameMat
                );
                fanFrame.position.set(0, 0.02, 0.40);
                primaryMesh.add(fanFrame);

                // Fan Motor Center Hub
                const coolerFanHub = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.11, 0.11, 0.09, 24),
                    new THREE.MeshStandardMaterial({{ color: 0x0a0c10, metalness: 0.95, roughness: 0.2 }})
                );
                coolerFanHub.rotation.x = Math.PI / 2;
                coolerFanHub.position.set(0, 0.02, 0.41);
                primaryMesh.add(coolerFanHub);

                // 7 Fan Blades (Using Math.cos/sin rotation)
                const bladeGeo = new THREE.BoxGeometry(0.038, 0.19, 0.015);
                const numCoolerBlades = 7;
                for (let b = 0; b < numCoolerBlades; b++) {{
                    const angle = (b / numCoolerBlades) * Math.PI * 2;
                    const blade = new THREE.Mesh(bladeGeo, bladeMat);
                    const bladeRadius = 0.17;
                    blade.position.set(
                        Math.cos(angle) * bladeRadius,
                        0.02 + Math.sin(angle) * bladeRadius,
                        0.41
                    );
                    blade.rotation.z = angle + 0.45;
                    blade.rotation.x = 0.35;
                    primaryMesh.add(blade);
                }}

                primaryMesh.position.set(-0.25, 0.75, -0.22);

            }} else if (idx === 4) {{
                // ── LAYER 4: DUAL-FAN GPU GRAPHICS CARD ──
                primaryMesh = new THREE.Group();

                const gpuShroudMat = new THREE.MeshStandardMaterial({{
                    color: 0x2c1050,
                    metalness: 0.85,
                    roughness: 0.28
                }});
                const backplateMat = new THREE.MeshStandardMaterial({{
                    color: 0x16181d,
                    metalness: 0.95,
                    roughness: 0.25
                }});
                const gpuPcbMat = new THREE.MeshStandardMaterial({{
                    color: 0x101114,
                    roughness: 0.4,
                    metalness: 0.3
                }});
                const pcieGoldMat = new THREE.MeshStandardMaterial({{
                    color: 0xD4AF37,
                    metalness: 0.98,
                    roughness: 0.15
                }});
                const ringShroudMat = new THREE.MeshStandardMaterial({{
                    color: 0x431c75,
                    metalness: 0.9,
                    roughness: 0.22
                }});
                const gpuFanBladeMat = new THREE.MeshStandardMaterial({{
                    color: 0x1c1e24,
                    metalness: 0.6,
                    roughness: 0.3
                }});
                const rgbStripMat = new THREE.MeshStandardMaterial({{
                    color: 0x9b59b6,
                    emissive: 0x8e44ad,
                    emissiveIntensity: 0.9,
                    roughness: 0.15
                }});
                const portMat = new THREE.MeshStandardMaterial({{
                    color: 0x0a0c10,
                    metalness: 0.9,
                    roughness: 0.3
                }});
                const bracketMat = new THREE.MeshStandardMaterial({{
                    color: 0xd0d4dc,
                    metalness: 0.96,
                    roughness: 0.2
                }});

                // Long PCB
                const gpuPcb = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.72, 2.3), gpuPcbMat);
                primaryMesh.add(gpuPcb);

                // PCIe x16 Gold Contacts
                const pcieContacts = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.11, 0.92), pcieGoldMat);
                pcieContacts.position.set(0, -0.40, -0.32);
                primaryMesh.add(pcieContacts);

                // Backplate (Dark metal plate)
                const backplate = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.72, 2.3), backplateMat);
                backplate.position.set(-0.028, 0, 0);
                primaryMesh.add(backplate);

                // Cooler Heatsink Shroud
                const gpuShroud = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.74, 2.32), gpuShroudMat);
                gpuShroud.position.set(0.15, 0, 0);
                primaryMesh.add(gpuShroud);

                // 2 Visible Fan Shrouds (CylinderGeometry rings)
                [-0.55, 0.55].forEach(fanZ => {{
                    const shroudRing = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.38, 0.38, 0.05, 32),
                        ringShroudMat
                    );
                    shroudRing.rotation.z = Math.PI / 2;
                    shroudRing.position.set(0.29, 0, fanZ);
                    primaryMesh.add(shroudRing);

                    const hub = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.12, 0.12, 0.06, 24),
                        new THREE.MeshStandardMaterial({{ color: 0x121418, metalness: 0.95, roughness: 0.2 }})
                    );
                    hub.rotation.z = Math.PI / 2;
                    hub.position.set(0.30, 0, fanZ);
                    primaryMesh.add(hub);

                    for (let b = 0; b < 9; b++) {{
                        const ang = (b / 9) * Math.PI * 2;
                        const bMesh = new THREE.Mesh(
                            new THREE.BoxGeometry(0.015, 0.17, 0.045),
                            gpuFanBladeMat
                        );
                        bMesh.position.set(0.29, Math.sin(ang) * 0.22, fanZ + Math.cos(ang) * 0.22);
                        bMesh.rotation.x = ang + 0.35;
                        bMesh.rotation.z = 0.3;
                        primaryMesh.add(bMesh);
                    }}
                }});

                // DisplayPort Connectors (Small rectangles at end) & Rear Bracket
                const pcieBracket = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.88, 0.06), bracketMat);
                pcieBracket.position.set(0.05, 0.04, -1.16);
                primaryMesh.add(pcieBracket);

                // 3x DisplayPort connectors
                [0.24, 0.10, -0.04].forEach(py => {{
                    const dp = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.075, 0.035), portMat);
                    dp.position.set(0.05, py, -1.18);
                    primaryMesh.add(dp);
                }});
                // HDMI connector
                const hdmi = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.065, 0.035), portMat);
                hdmi.position.set(0.05, -0.18, -1.18);
                primaryMesh.add(hdmi);

                // RGB Accent Strip (Emissive colored bar)
                const rgbStrip = new THREE.Mesh(
                    new THREE.BoxGeometry(0.05, 0.05, 1.85),
                    rgbStripMat
                );
                rgbStrip.position.set(0.24, 0.38, 0.0);
                primaryMesh.add(rgbStrip);

                primaryMesh.position.set(-0.12, 0.12, 0.0);

            }} else {{
                // ── LAYER 5: TEMPERED GLASS SIDE PANEL ──
                primaryMesh = new THREE.Group();

                const glassMat = new THREE.MeshStandardMaterial({{
                    color: 0x1a2240,
                    transparent: true,
                    opacity: 0.35,
                    roughness: 0.05,
                    metalness: 0.85
                }});
                const thumbscrewMat = new THREE.MeshStandardMaterial({{
                    color: 0x2c2f36,
                    metalness: 0.95,
                    roughness: 0.25
                }});
                const rubberWasherMat = new THREE.MeshStandardMaterial({{
                    color: 0x0c0d10,
                    roughness: 0.8,
                    metalness: 0.2
                }});
                const ceramicBorderMat = new THREE.MeshStandardMaterial({{
                    color: 0x0b0d12,
                    metalness: 0.8,
                    roughness: 0.5
                }});

                // Transparent Tinted Glass Panel
                const glassPanel = new THREE.Mesh(new THREE.BoxGeometry(0.035, 3.32, 3.12), glassMat);
                primaryMesh.add(glassPanel);

                // Silk-Screened Dark Border Trim
                const topBorder = new THREE.Mesh(new THREE.BoxGeometry(0.038, 0.14, 3.12), ceramicBorderMat);
                topBorder.position.set(0, 1.59, 0);
                primaryMesh.add(topBorder);

                const botBorder = new THREE.Mesh(new THREE.BoxGeometry(0.038, 0.14, 3.12), ceramicBorderMat);
                botBorder.position.set(0, -1.59, 0);
                primaryMesh.add(botBorder);

                const frontBorder = new THREE.Mesh(new THREE.BoxGeometry(0.038, 3.32, 0.14), ceramicBorderMat);
                frontBorder.position.set(0, 0, 1.49);
                primaryMesh.add(frontBorder);

                const rearBorder = new THREE.Mesh(new THREE.BoxGeometry(0.038, 3.32, 0.14), ceramicBorderMat);
                rearBorder.position.set(0, 0, -1.49);
                primaryMesh.add(rearBorder);

                // 4 Thumbscrews at Corners (Small cylinders)
                const screwGeo = new THREE.CylinderGeometry(0.065, 0.065, 0.045, 20);
                screwGeo.rotateZ(Math.PI / 2);
                const washerGeo = new THREE.CylinderGeometry(0.075, 0.075, 0.015, 20);
                washerGeo.rotateZ(Math.PI / 2);

                const tsPositions = [
                    [1.45, 1.35],
                    [1.45, -1.35],
                    [-1.45, 1.35],
                    [-1.45, -1.35]
                ];
                tsPositions.forEach(tsp => {{
                    const washer = new THREE.Mesh(washerGeo, rubberWasherMat);
                    washer.position.set(0.022, tsp[0], tsp[1]);
                    primaryMesh.add(washer);

                    const screw = new THREE.Mesh(screwGeo, thumbscrewMat);
                    screw.position.set(0.038, tsp[0], tsp[1]);
                    primaryMesh.add(screw);
                }});

                primaryMesh.position.set(0.82, 0, 0);
            }}

        }} else if (type === 'battery') {{
            // ═══ MULTI-CELL INDUSTRIAL 18650 LI-ION BATTERY PACK (HIGH FIDELITY) ═══
            if (idx === 0) {{
                // ── 1. BLUE HEAT-SHRINK OUTER SLEEVE & REGULATORY LABELS ──
                primaryMesh = new THREE.Group();

                // Main Heat-Shrink Translucent Enclosure
                const wrapGeo = new THREE.BoxGeometry(1.68, 1.72, 1.16);
                const wrapMat = new THREE.MeshStandardMaterial({{
                    color: 0x1B4F72,
                    transparent: true,
                    opacity: 0.6,
                    roughness: 0.25,
                    metalness: 0.12
                }});
                const wrapMesh = new THREE.Mesh(wrapGeo, wrapMat);
                primaryMesh.add(wrapMesh);

                // Rounded Corner Bumpers (Shrink contour edges)
                const cornerGeo = new THREE.CylinderGeometry(0.07, 0.07, 1.72, 16);
                const cornerMat = new THREE.MeshStandardMaterial({{
                    color: 0x154360,
                    transparent: true,
                    opacity: 0.7,
                    roughness: 0.2
                }});
                const cOffsets = [
                    [-0.82, -0.56], [0.82, -0.56],
                    [-0.82, 0.56], [0.82, 0.56]
                ];
                cOffsets.forEach(([cx, cz]) => {{
                    const cm = new THREE.Mesh(cornerGeo, cornerMat);
                    cm.position.set(cx, 0, cz);
                    primaryMesh.add(cm);
                }});

                // Top & Bottom Shrink Aperture Collars (Crimped rims)
                const rimGeo = new THREE.BoxGeometry(1.54, 0.03, 1.02);
                const rimMat = new THREE.MeshStandardMaterial({{ color: 0x0E3A5A, roughness: 0.5 }});
                const topRim = new THREE.Mesh(rimGeo, rimMat);
                topRim.position.set(0, 0.865, 0);
                const btmRim = new THREE.Mesh(rimGeo, rimMat);
                btmRim.position.set(0, -0.865, 0);
                primaryMesh.add(topRim);
                primaryMesh.add(btmRim);

                // Label Backing Materials
                const labelMat = new THREE.MeshStandardMaterial({{ color: 0xFDFEFE, roughness: 0.3 }});
                const darkTextMat = new THREE.MeshStandardMaterial({{ color: 0x1A252F, roughness: 0.5 }});
                const warnYellowMat = new THREE.MeshStandardMaterial({{ color: 0xF1C40F, roughness: 0.35 }});
                const dangerRedMat = new THREE.MeshStandardMaterial({{ color: 0xC0392B, roughness: 0.35 }});

                // Front Surface Z Offset
                const labelZ = 0.585;

                // 1) Printed Voltage & Capacity Specification Plate (White Box)
                const specPlate = new THREE.Mesh(new THREE.BoxGeometry(0.92, 0.46, 0.012), labelMat);
                specPlate.position.set(-0.24, 0.38, labelZ);
                primaryMesh.add(specPlate);

                // Rating Text Line Bars (Simulating "11.1V 5200mAh / 57.7Wh")
                const textLine1 = new THREE.Mesh(new THREE.BoxGeometry(0.74, 0.045, 0.014), darkTextMat);
                textLine1.position.set(-0.24, 0.49, labelZ + 0.002);
                const textLine2 = new THREE.Mesh(new THREE.BoxGeometry(0.60, 0.030, 0.014), darkTextMat);
                textLine2.position.set(-0.31, 0.41, labelZ + 0.002);
                const textLine3 = new THREE.Mesh(new THREE.BoxGeometry(0.70, 0.022, 0.014), new THREE.MeshStandardMaterial({{ color: 0x7F8C8D }}));
                textLine3.position.set(-0.26, 0.33, labelZ + 0.002);
                primaryMesh.add(textLine1);
                primaryMesh.add(textLine2);
                primaryMesh.add(textLine3);

                // Regulatory Certification Logo Stamp (CE/RoHS)
                const certLogo = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.045, 0.045, 0.014, 16),
                    darkTextMat
                );
                certLogo.rotation.x = Math.PI / 2;
                certLogo.position.set(0.12, 0.28, labelZ + 0.002);
                primaryMesh.add(certLogo);

                // 2) Yellow Caution Warning Label
                const warnBox = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.26, 0.012), warnYellowMat);
                warnBox.position.set(0.50, 0.38, labelZ);
                const warnStripe = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.05, 0.014), darkTextMat);
                warnStripe.position.set(0.50, 0.42, labelZ + 0.002);
                const warnDot = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.03, 0.014), darkTextMat);
                warnDot.position.set(0.50, 0.33, labelZ + 0.002);
                primaryMesh.add(warnBox);
                primaryMesh.add(warnStripe);
                primaryMesh.add(warnDot);

                // 3) Red Danger / Fire Hazard Label
                const dangerBox = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.20, 0.012), dangerRedMat);
                dangerBox.position.set(0.48, 0.02, labelZ);
                const dangerText = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.04, 0.014), labelMat);
                dangerText.position.set(0.48, 0.02, labelZ + 0.002);
                primaryMesh.add(dangerBox);
                primaryMesh.add(dangerText);

                // 4) High-Precision Serial Barcode Strip
                const barcodeBack = new THREE.Mesh(new THREE.BoxGeometry(0.82, 0.24, 0.012), labelMat);
                barcodeBack.position.set(-0.28, -0.25, labelZ);
                primaryMesh.add(barcodeBack);

                const barWidths = [0.015, 0.03, 0.012, 0.04, 0.018, 0.035, 0.012, 0.025, 0.04, 0.016, 0.03, 0.015];
                let curBarX = -0.62;
                barWidths.forEach(bw => {{
                    const bar = new THREE.Mesh(new THREE.BoxGeometry(bw, 0.16, 0.014), darkTextMat);
                    bar.position.set(curBarX + bw / 2, -0.25, labelZ + 0.002);
                    primaryMesh.add(bar);
                    curBarX += bw + 0.022;
                }});

            }} else if (idx === 1) {{
                // ── 2. COPPER POWER TERMINALS & SILICONE LEAD WIRES ──
                primaryMesh = new THREE.Group();

                const goldMat = new THREE.MeshStandardMaterial({{
                    color: 0xFFD700,
                    metalness: 0.98,
                    roughness: 0.12
                }});
                const redWireMat = new THREE.MeshStandardMaterial({{
                    color: 0xCC2222,
                    roughness: 0.55,
                    metalness: 0.1
                }});
                const blackWireMat = new THREE.MeshStandardMaterial({{
                    color: 0x222222,
                    roughness: 0.55,
                    metalness: 0.1
                }});
                const copperMat = new THREE.MeshStandardMaterial({{
                    color: 0xB87333,
                    metalness: 0.92,
                    roughness: 0.2
                }});

                // Positive Terminal Post (Red Collar + Gold Tip)
                const redPostBase = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.075, 0.075, 0.26, 24),
                    redWireMat
                );
                redPostBase.position.set(0.46, 0.96, 0.18);
                const redPostGold = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.05, 0.05, 0.12, 24),
                    goldMat
                );
                redPostGold.position.set(0.46, 1.12, 0.18);
                const redNut = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.09, 0.09, 0.06, 6),
                    goldMat
                );
                redNut.position.set(0.46, 0.88, 0.18);
                primaryMesh.add(redPostBase);
                primaryMesh.add(redPostGold);
                primaryMesh.add(redNut);

                // Negative Terminal Post (Black Collar + Gold Tip)
                const blackPostBase = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.075, 0.075, 0.26, 24),
                    blackWireMat
                );
                blackPostBase.position.set(-0.46, 0.96, 0.18);
                const blackPostGold = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.05, 0.05, 0.12, 24),
                    goldMat
                );
                blackPostGold.position.set(-0.46, 1.12, 0.18);
                const blackNut = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.09, 0.09, 0.06, 6),
                    goldMat
                );
                blackNut.position.set(-0.46, 0.88, 0.18);
                primaryMesh.add(blackPostBase);
                primaryMesh.add(blackPostGold);
                primaryMesh.add(blackNut);

                // Flexible Red Silicone Lead Wire (Multi-segment natural smooth curvature)
                const redSegments = [
                    {{ p: [0.46, 1.12, 0.18], r: [0.15, 0, -0.25], l: 0.24 }},
                    {{ p: [0.55, 1.28, 0.24], r: [0.35, 0, -0.55], l: 0.28 }},
                    {{ p: [0.72, 1.40, 0.36], r: [0.55, 0, -0.85], l: 0.28 }},
                    {{ p: [0.90, 1.44, 0.50], r: [0.20, 0, -1.25], l: 0.26 }}
                ];
                redSegments.forEach(s => {{
                    const seg = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.042, 0.042, s.l, 16),
                        redWireMat
                    );
                    seg.position.set(...s.p);
                    seg.rotation.set(...s.r);
                    primaryMesh.add(seg);
                }});

                // Red Ring Terminal Connector (Crimped Collar + Gold Eyelet Torus)
                const redCrimp = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.048, 0.048, 0.10, 16),
                    copperMat
                );
                redCrimp.position.set(1.04, 1.44, 0.56);
                redCrimp.rotation.z = Math.PI / 2;
                const redEyelet = new THREE.Mesh(
                    new THREE.TorusGeometry(0.075, 0.026, 16, 24),
                    goldMat
                );
                redEyelet.position.set(1.16, 1.44, 0.56);
                redEyelet.rotation.y = Math.PI / 4;
                primaryMesh.add(redCrimp);
                primaryMesh.add(redEyelet);

                // Flexible Black Silicone Lead Wire (Curving symmetrically towards left)
                const blackSegments = [
                    {{ p: [-0.46, 1.12, 0.18], r: [0.15, 0, 0.25], l: 0.24 }},
                    {{ p: [-0.55, 1.28, 0.24], r: [0.35, 0, 0.55], l: 0.28 }},
                    {{ p: [-0.72, 1.40, 0.36], r: [0.55, 0, 0.85], l: 0.28 }},
                    {{ p: [-0.90, 1.44, 0.50], r: [0.20, 0, 1.25], l: 0.26 }}
                ];
                blackSegments.forEach(s => {{
                    const seg = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.042, 0.042, s.l, 16),
                        blackWireMat
                    );
                    seg.position.set(...s.p);
                    seg.rotation.set(...s.r);
                    primaryMesh.add(seg);
                }});

                // Black Ring Terminal Connector (Crimped Collar + Gold Eyelet Torus)
                const blackCrimp = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.048, 0.048, 0.10, 16),
                    copperMat
                );
                blackCrimp.position.set(-1.04, 1.44, 0.56);
                blackCrimp.rotation.z = -Math.PI / 2;
                const blackEyelet = new THREE.Mesh(
                    new THREE.TorusGeometry(0.075, 0.026, 16, 24),
                    goldMat
                );
                blackEyelet.position.set(-1.16, 1.44, 0.56);
                blackEyelet.rotation.y = -Math.PI / 4;
                primaryMesh.add(blackCrimp);
                primaryMesh.add(blackEyelet);

            }} else if (idx === 2) {{
                // ── 3. BMS (BATTERY MANAGEMENT SYSTEM) CIRCUIT BOARD ──
                primaryMesh = new THREE.Group();

                // Multi-Layer FR4 Protective Circuit Board
                const pcbGeo = new THREE.BoxGeometry(1.42, 0.035, 0.76);
                const pcbMat = new THREE.MeshStandardMaterial({{
                    color: 0x0a6e2a,
                    roughness: 0.32,
                    metalness: 0.15
                }});
                const pcbBoard = new THREE.Mesh(pcbGeo, pcbMat);
                pcbBoard.position.set(0, 0.78, 0);
                primaryMesh.add(pcbBoard);

                // Gold Surface Trace Pads & Ground Planes
                const goldPadMat = new THREE.MeshStandardMaterial({{
                    color: 0xD4AF37,
                    metalness: 0.95,
                    roughness: 0.15
                }});
                const tracePlane1 = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.005, 0.24), goldPadMat);
                tracePlane1.position.set(-0.35, 0.80, -0.16);
                const tracePlane2 = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.005, 0.20), goldPadMat);
                tracePlane2.position.set(0.35, 0.80, 0.16);
                primaryMesh.add(tracePlane1);
                primaryMesh.add(tracePlane2);

                // 3x High-Current Power N-MOSFETs (with silver thermal sink tabs)
                const mosfetMat = new THREE.MeshStandardMaterial({{ color: 0x111111, roughness: 0.4, metalness: 0.8 }});
                const tabMat = new THREE.MeshStandardMaterial({{ color: 0xC8CED0, metalness: 0.95, roughness: 0.15 }});
                const mosfetXs = [-0.44, -0.24, -0.04];
                mosfetXs.forEach(mx => {{
                    const mBody = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.045, 0.11), mosfetMat);
                    mBody.position.set(mx, 0.815, -0.16);
                    const mTab = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.015, 0.04), tabMat);
                    mTab.position.set(mx, 0.805, -0.225);
                    primaryMesh.add(mBody);
                    primaryMesh.add(mTab);
                }});

                // Microcontroller Protection IC (QFP Chip with Gold Lead Pads)
                const mcuBody = new THREE.Mesh(
                    new THREE.BoxGeometry(0.22, 0.045, 0.22),
                    new THREE.MeshStandardMaterial({{ color: 0x181818, roughness: 0.25, metalness: 0.85 }})
                );
                mcuBody.position.set(0.32, 0.815, -0.12);
                primaryMesh.add(mcuBody);

                // MCU Pin-1 Gold Index Dot
                const mcuDot = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.015, 0.015, 0.006, 12),
                    goldPadMat
                );
                mcuDot.position.set(0.25, 0.84, -0.19);
                primaryMesh.add(mcuDot);

                // Row of Balance Resistors (Precision SMD cylinders)
                const resMat = new THREE.MeshStandardMaterial({{ color: 0x2471A3, roughness: 0.3 }});
                const capEndMat = new THREE.MeshStandardMaterial({{ color: 0xBDC3C7, metalness: 0.9 }});
                for (let r = 0; r < 4; r++) {{
                    const rx = -0.32 + r * 0.18;
                    const res = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.075, 12), resMat);
                    res.rotation.z = Math.PI / 2;
                    res.position.set(rx, 0.815, 0.12);
                    const endL = new THREE.Mesh(new THREE.CylinderGeometry(0.024, 0.024, 0.015, 12), capEndMat);
                    endL.rotation.z = Math.PI / 2;
                    endL.position.set(rx - 0.035, 0.815, 0.12);
                    const endR = new THREE.Mesh(new THREE.CylinderGeometry(0.024, 0.024, 0.015, 12), capEndMat);
                    endR.rotation.z = Math.PI / 2;
                    endR.position.set(rx + 0.035, 0.815, 0.12);
                    primaryMesh.add(res);
                    primaryMesh.add(endL);
                    primaryMesh.add(endR);
                }}

                // Temperature Sensor (NTC Thermistor Bead + Dual Copper Wire Leads)
                const beadMat = new THREE.MeshStandardMaterial({{ color: 0x1A252F, roughness: 0.3 }});
                const bead = new THREE.Mesh(new THREE.SphereGeometry(0.04, 16, 16), beadMat);
                bead.position.set(0.06, 0.825, 0.28);
                const leadGeo = new THREE.CylinderGeometry(0.006, 0.006, 0.14, 8);
                const leadCopperMat = new THREE.MeshStandardMaterial({{ color: 0xD35400, metalness: 0.9 }});
                const lead1 = new THREE.Mesh(leadGeo, leadCopperMat);
                lead1.rotation.x = Math.PI / 2;
                lead1.position.set(0.045, 0.81, 0.21);
                const lead2 = new THREE.Mesh(leadGeo, leadCopperMat);
                lead2.rotation.x = Math.PI / 2;
                lead2.position.set(0.075, 0.81, 0.21);
                primaryMesh.add(bead);
                primaryMesh.add(lead1);
                primaryMesh.add(lead2);

                // Multi-Pin Header Connector (JST Balance Header with Silver Pins)
                const headerHousing = new THREE.Mesh(
                    new THREE.BoxGeometry(0.38, 0.08, 0.11),
                    new THREE.MeshStandardMaterial({{ color: 0xEAEDED, roughness: 0.6 }})
                );
                headerHousing.position.set(0.48, 0.835, 0.24);
                primaryMesh.add(headerHousing);

                const pinMat = new THREE.MeshStandardMaterial({{ color: 0xD5D8DC, metalness: 0.95, roughness: 0.1 }});
                for (let p = 0; p < 5; p++) {{
                    const pin = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, 0.05, 8), pinMat);
                    pin.position.set(0.36 + p * 0.06, 0.88, 0.24);
                    primaryMesh.add(pin);
                }}

            }} else if (idx === 3) {{
                // ── 4. SHINY NICKEL STRIP BUSBARS & SPOT-WELDS ──
                primaryMesh = new THREE.Group();

                const nickelMat = new THREE.MeshStandardMaterial({{
                    color: 0xC8CED0,
                    metalness: 0.98,
                    roughness: 0.08
                }});
                const weldMat = new THREE.MeshStandardMaterial({{
                    color: 0x889296,
                    metalness: 0.95,
                    roughness: 0.25
                }});

                // Top Busbar Assembly (Y = 0.72)
                const topY = 0.72;

                // Function to add spot-weld mark pair
                const addSpotWelds = (wx, wy, wz) => {{
                    [-0.035, 0.035].forEach(dx => {{
                        [-0.035, 0.035].forEach(dz => {{
                            const weld = new THREE.Mesh(
                                new THREE.CylinderGeometry(0.015, 0.015, 0.012, 12),
                                weldMat
                            );
                            weld.position.set(wx + dx, wy + 0.008, wz + dz);
                            primaryMesh.add(weld);
                        }});
                    }});
                }};

                // Connected Zigzag Top Strips
                // Longitudinal link between cell (0,0) and (0,1)
                const topStrip1 = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.014, 0.64), nickelMat);
                topStrip1.position.set(-0.52, topY, 0);
                primaryMesh.add(topStrip1);
                addSpotWelds(-0.52, topY, -0.28);
                addSpotWelds(-0.52, topY, 0.28);

                // Diagonal crossover bridge forming zigzag from (-0.52, 0.28) to (0.0, -0.28)
                const diagBridge1 = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.014, 0.74), nickelMat);
                diagBridge1.rotation.y = 0.72;
                diagBridge1.position.set(-0.26, topY, 0);
                primaryMesh.add(diagBridge1);

                // Longitudinal link between cell (1,0) and (1,1)
                const topStrip2 = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.014, 0.64), nickelMat);
                topStrip2.position.set(0.0, topY, 0);
                primaryMesh.add(topStrip2);
                addSpotWelds(0.0, topY, -0.28);
                addSpotWelds(0.0, topY, 0.28);

                // Diagonal crossover bridge forming zigzag from (0.0, -0.28) to (0.52, 0.28)
                const diagBridge2 = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.014, 0.74), nickelMat);
                diagBridge2.rotation.y = -0.72;
                diagBridge2.position.set(0.26, topY, 0);
                primaryMesh.add(diagBridge2);

                // Longitudinal link between cell (2,0) and (2,1)
                const topStrip3 = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.014, 0.64), nickelMat);
                topStrip3.position.set(0.52, topY, 0);
                primaryMesh.add(topStrip3);
                addSpotWelds(0.52, topY, -0.28);
                addSpotWelds(0.52, topY, 0.28);

                // Bottom Busbar Assembly (Y = -0.72) Completing 3S2P Series Circuits
                const btmY = -0.72;
                const btmStrip1 = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.014, 0.18), nickelMat);
                btmStrip1.position.set(-0.26, btmY, -0.28);
                const btmStrip2 = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.014, 0.18), nickelMat);
                btmStrip2.position.set(0.26, btmY, 0.28);
                primaryMesh.add(btmStrip1);
                primaryMesh.add(btmStrip2);

                // Bottom Spot-welds
                [-0.52, 0.0].forEach(bx => addSpotWelds(bx, btmY - 0.012, -0.28));
                [0.0, 0.52].forEach(bx => addSpotWelds(bx, btmY - 0.012, 0.28));

            }} else {{
                // ── 5. 18650 CYLINDRICAL CELL ARRAY (6 CELLS, 2x3 GRID) ──
                primaryMesh = new THREE.Group();

                const cellRadius = 0.22;
                const cellHeight = 1.36;

                // Materials
                const cellBodyMat = new THREE.MeshStandardMaterial({{
                    color: 0x27AE60,
                    metalness: 0.65,
                    roughness: 0.32
                }});
                const brandBandMat = new THREE.MeshStandardMaterial({{
                    color: 0x1E5631,
                    metalness: 0.40,
                    roughness: 0.40
                }});
                const posButtonMat = new THREE.MeshStandardMaterial({{
                    color: 0xD5D8DC,
                    metalness: 0.96,
                    roughness: 0.12
                }});
                const insulRingMat = new THREE.MeshStandardMaterial({{
                    color: 0xE67E22,
                    roughness: 0.5,
                    metalness: 0.1
                }});
                const negDiscMat = new THREE.MeshStandardMaterial({{
                    color: 0xC0C0C0,
                    metalness: 0.95,
                    roughness: 0.18
                }});

                // Shared Geometries for Peak Rendering Performance
                const bodyGeo = new THREE.CylinderGeometry(cellRadius, cellRadius, cellHeight, 32);
                const brandGeo = new THREE.CylinderGeometry(cellRadius + 0.002, cellRadius + 0.002, 0.46, 32);
                const buttonGeo = new THREE.CylinderGeometry(0.088, 0.088, 0.045, 24);
                const insulGeo = new THREE.TorusGeometry(0.145, 0.024, 16, 32);
                const btmDiscGeo = new THREE.CylinderGeometry(cellRadius - 0.015, cellRadius - 0.015, 0.02, 28);

                // Structural Cell Spacers / Honeycomb Holders (Matte Black Engineering Polymer)
                const holderMat = new THREE.MeshStandardMaterial({{ color: 0x1C1C1C, roughness: 0.7 }});
                const topHolder = new THREE.Mesh(new THREE.BoxGeometry(1.58, 0.09, 1.06), holderMat);
                topHolder.position.set(0, 0.62, 0);
                const btmHolder = new THREE.Mesh(new THREE.BoxGeometry(1.58, 0.09, 1.06), holderMat);
                btmHolder.position.set(0, -0.62, 0);
                primaryMesh.add(topHolder);
                primaryMesh.add(btmHolder);

                // 2 Rows x 3 Columns Cell Lattice
                const colXs = [-0.52, 0.0, 0.52];
                const rowZs = [-0.28, 0.28];

                rowZs.forEach(rz => {{
                    colXs.forEach(cx => {{
                        const singleCell = new THREE.Group();
                        singleCell.position.set(cx, 0, rz);

                        // 1) Main Green Anodized Li-Ion Cell Body
                        const body = new THREE.Mesh(bodyGeo, cellBodyMat);
                        singleCell.add(body);

                        // 2) Darker Green Middle Brand Marking Band
                        const brand = new THREE.Mesh(brandGeo, brandBandMat);
                        brand.position.set(0, 0, 0);
                        singleCell.add(brand);

                        // 3) Raised Positive Terminal Button (+ Top Pole)
                        const button = new THREE.Mesh(buttonGeo, posButtonMat);
                        button.position.set(0, (cellHeight / 2) + 0.022, 0);
                        singleCell.add(button);

                        // 4) High-Visibility Insulation Ring (Orange/Amber)
                        const ring = new THREE.Mesh(insulGeo, insulRingMat);
                        ring.rotation.x = Math.PI / 2;
                        ring.position.set(0, (cellHeight / 2) + 0.006, 0);
                        singleCell.add(ring);

                        // 5) Negative Flat Bottom Plate (- Base Pole)
                        const negDisc = new THREE.Mesh(btmDiscGeo, negDiscMat);
                        negDisc.position.set(0, -(cellHeight / 2) - 0.005, 0);
                        singleCell.add(negDisc);

                        primaryMesh.add(singleCell);
                    }});
                }});
            }}

        }} else if (type === 'pcb') {{
            // ═══ HIGH-DENSITY MULTI-LAYER LOGIC CIRCUIT BOARD ═══
            if (idx === 0) {{
                // ── 1. FR4 SUBSTRATE BOARD & COPPER TRACES ──
                primaryMesh = new THREE.Group();

                // Characteristic Dark Green FR4 Substrate Core
                const pcbWidth = 3.4;
                const pcbHeight = 2.3;
                const pcbThick = 0.055;
                const boardGeo = new THREE.BoxGeometry(pcbWidth, pcbHeight, pcbThick);
                const boardMat = new THREE.MeshStandardMaterial({{
                    color: 0x0a5c2a,
                    roughness: 0.36,
                    metalness: 0.25
                }});
                const mainBoard = new THREE.Mesh(boardGeo, boardMat);
                primaryMesh.add(mainBoard);

                // Beveled Chamfer Edge Perimeter Trims
                const bevelMat = new THREE.MeshStandardMaterial({{
                    color: 0x074620,
                    roughness: 0.45,
                    metalness: 0.30
                }});
                // Left & Right Bevel Borders
                const lrBevelGeo = new THREE.BoxGeometry(0.025, pcbHeight + 0.02, pcbThick + 0.004);
                const leftBevel = new THREE.Mesh(lrBevelGeo, bevelMat);
                leftBevel.position.set(-pcbWidth / 2, 0, 0);
                const rightBevel = new THREE.Mesh(lrBevelGeo, bevelMat);
                rightBevel.position.set(pcbWidth / 2, 0, 0);
                // Top & Bottom Bevel Borders
                const tbBevelGeo = new THREE.BoxGeometry(pcbWidth + 0.02, 0.025, pcbThick + 0.004);
                const topBevel = new THREE.Mesh(tbBevelGeo, bevelMat);
                topBevel.position.set(0, pcbHeight / 2, 0);
                const btmBevel = new THREE.Mesh(tbBevelGeo, bevelMat);
                btmBevel.position.set(0, -pcbHeight / 2, 0);
                primaryMesh.add(leftBevel);
                primaryMesh.add(rightBevel);
                primaryMesh.add(topBevel);
                primaryMesh.add(btmBevel);

                // Sub-surface Copper Ground Plane Flood (visible through translucent solder mask)
                const gndFloodMat = new THREE.MeshStandardMaterial({{
                    color: 0x0e6e33,
                    roughness: 0.30,
                    metalness: 0.40
                }});
                const gndFlood = new THREE.Mesh(
                    new THREE.BoxGeometry(pcbWidth - 0.08, pcbHeight - 0.08, pcbThick + 0.002),
                    gndFloodMat
                );
                primaryMesh.add(gndFlood);

                // ── Surface Copper Trace Patterns (Thin Raised Lines, Color 0xB87333) ──
                const copperMat = new THREE.MeshStandardMaterial({{
                    color: 0xB87333,
                    metalness: 0.90,
                    roughness: 0.20
                }});
                const traceZ = pcbThick / 2 + 0.004;

                // Bus 1: High-Speed PCIe Data Bus (8 parallel horizontal traces)
                for (let t = 0; t < 8; t++) {{
                    const trace = new THREE.Mesh(
                        new THREE.BoxGeometry(1.6, 0.012, 0.006),
                        copperMat
                    );
                    trace.position.set(-0.1, -0.65 - t * 0.035, traceZ);
                    primaryMesh.add(trace);
                }}

                // Bus 2: 45-degree Angled Fanout Traces
                const diagAngles = [Math.PI / 4, -Math.PI / 4, Math.PI / 4, -Math.PI / 4];
                const diagPositions = [
                    [-0.75, -0.50, 0.45],
                    [-0.55, -0.45, 0.35],
                    [0.45, -0.45, 0.35],
                    [0.65, -0.50, 0.45]
                ];
                diagPositions.forEach((dp, i) => {{
                    const diagTrace = new THREE.Mesh(
                        new THREE.BoxGeometry(dp[2], 0.014, 0.006),
                        copperMat
                    );
                    diagTrace.rotation.z = diagAngles[i];
                    diagTrace.position.set(dp[0], dp[1], traceZ);
                    primaryMesh.add(diagTrace);
                }});

                // Bus 3: Memory Routing Vertical Buses
                for (let m = 0; m < 6; m++) {{
                    const memTrace = new THREE.Mesh(
                        new THREE.BoxGeometry(0.012, 0.90, 0.006),
                        copperMat
                    );
                    memTrace.position.set(0.20 + m * 0.045, 0.55, traceZ);
                    primaryMesh.add(memTrace);
                }}

                // Bus 4: Heavy VRM Power Copper Pours / Traces
                const vrmPours = [
                    {{ x: -1.20, y: 0.40, w: 0.45, h: 0.18 }},
                    {{ x: -1.20, y: 0.05, w: 0.45, h: 0.18 }},
                    {{ x: -1.20, y: -0.30, w: 0.45, h: 0.18 }}
                ];
                vrmPours.forEach(p => {{
                    const pour = new THREE.Mesh(
                        new THREE.BoxGeometry(p.w, p.h, 0.006),
                        copperMat
                    );
                    pour.position.set(p.x, p.y, traceZ);
                    primaryMesh.add(pour);
                }});

                // Geometric Test Points & Vias (Circular Copper Annular Rings)
                const viaGeo = new THREE.CylinderGeometry(0.018, 0.018, 0.008, 12);
                viaGeo.rotateX(Math.PI / 2);
                const viaHoleMat = new THREE.MeshStandardMaterial({{ color: 0x050508, roughness: 0.95 }});
                const viaHoleGeo = new THREE.CylinderGeometry(0.009, 0.009, 0.010, 8);
                viaHoleGeo.rotateX(Math.PI / 2);

                const viaCoords = [
                    [-0.95, -0.72], [-0.85, -0.72], [-0.75, -0.72],
                    [0.55, -0.72], [0.65, -0.72], [0.75, -0.72],
                    [-0.30, 0.90], [-0.15, 0.90], [0.0, 0.90],
                    [0.85, 0.20], [0.95, 0.20], [1.05, 0.20]
                ];
                viaCoords.forEach(c => {{
                    const vPad = new THREE.Mesh(viaGeo, copperMat);
                    vPad.position.set(c[0], c[1], traceZ);
                    const vHole = new THREE.Mesh(viaHoleGeo, viaHoleMat);
                    vHole.position.set(c[0], c[1], traceZ + 0.001);
                    primaryMesh.add(vPad);
                    primaryMesh.add(vHole);
                }});

                // ── Mounting Holes (4 Small Dark Cylinders with Copper Grounding Rings at Corners) ──
                const mRingGeo = new THREE.CylinderGeometry(0.13, 0.13, 0.065, 24);
                mRingGeo.rotateX(Math.PI / 2);
                const mHoleGeo = new THREE.CylinderGeometry(0.075, 0.075, 0.070, 24);
                mHoleGeo.rotateX(Math.PI / 2);
                const mHoleMat = new THREE.MeshStandardMaterial({{ color: 0x050508, roughness: 0.95 }});

                const cornerHoles = [
                    [-1.52, 0.98],
                    [1.52, 0.98],
                    [-1.52, -0.98],
                    [1.52, -0.98]
                ];
                cornerHoles.forEach(ch => {{
                    // Exposed copper ground ring pad
                    const ring = new THREE.Mesh(mRingGeo, copperMat);
                    ring.position.set(ch[0], ch[1], 0);
                    primaryMesh.add(ring);
                    // Dark screw hole opening
                    const hole = new THREE.Mesh(mHoleGeo, mHoleMat);
                    hole.position.set(ch[0], ch[1], 0);
                    primaryMesh.add(hole);
                }});

                // ── Silkscreen Markings Area (Tiny White Rectangles, Outlines & Markings) ──
                const silkMat = new THREE.MeshStandardMaterial({{
                    color: 0xF2F4F4,
                    roughness: 0.92,
                    metalness: 0.05
                }});
                const silkZ = traceZ + 0.003;

                // CPU Socket Outline Box (White boundary lines)
                const cpuBoxLines = [
                    {{ x: -0.35, y: 0.72, w: 1.12, h: 0.015 }},
                    {{ x: -0.35, y: -0.36, w: 1.12, h: 0.015 }},
                    {{ x: -0.91, y: 0.18, w: 0.015, h: 1.08 }},
                    {{ x: 0.21, y: 0.18, w: 0.015, h: 1.08 }}
                ];
                cpuBoxLines.forEach(l => {{
                    const line = new THREE.Mesh(new THREE.BoxGeometry(l.w, l.h, 0.004), silkMat);
                    line.position.set(l.x, l.y, silkZ);
                    primaryMesh.add(line);
                }});

                // Chipset Outline Box
                const chipLines = [
                    {{ x: 0.80, y: 0.14, w: 0.72, h: 0.014 }},
                    {{ x: 0.80, y: -0.58, w: 0.72, h: 0.014 }},
                    {{ x: 0.44, y: -0.22, w: 0.014, h: 0.72 }},
                    {{ x: 1.16, y: -0.22, w: 0.014, h: 0.72 }}
                ];
                chipLines.forEach(l => {{
                    const line = new THREE.Mesh(new THREE.BoxGeometry(l.w, l.h, 0.004), silkMat);
                    line.position.set(l.x, l.y, silkZ);
                    primaryMesh.add(line);
                }});

                // Silkscreen Barcode / QR Label Area
                const barcodeLabel = new THREE.Mesh(
                    new THREE.BoxGeometry(0.68, 0.24, 0.005),
                    silkMat
                );
                barcodeLabel.position.set(-0.65, -0.92, silkZ);
                primaryMesh.add(barcodeLabel);

                // Barcode Bars (alternating dark strips)
                const barMat = new THREE.MeshStandardMaterial({{ color: 0x111111, roughness: 0.95 }});
                for (let b = 0; b < 14; b++) {{
                    const barW = (b % 3 === 0) ? 0.022 : 0.010;
                    const bar = new THREE.Mesh(new THREE.BoxGeometry(barW, 0.16, 0.006), barMat);
                    bar.position.set(-0.92 + b * 0.042, -0.92, silkZ + 0.002);
                    primaryMesh.add(bar);
                }}

                // Polarity, Pin-1 & Certification Indicators
                const polarityMark = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.018, 0.004), silkMat);
                polarityMark.position.set(-1.25, 0.84, silkZ);
                const polarityCross = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.08, 0.004), silkMat);
                polarityCross.position.set(-1.25, 0.84, silkZ);
                primaryMesh.add(polarityMark);
                primaryMesh.add(polarityCross);

                // Silkscreen Text Blocks (simulated with micro white rectangles)
                const textBlocks = [
                    {{ x: 0.80, y: 0.95, w: 0.45, h: 0.05 }},
                    {{ x: 0.80, y: 0.86, w: 0.35, h: 0.03 }},
                    {{ x: -1.25, y: -0.70, w: 0.28, h: 0.04 }}
                ];
                textBlocks.forEach(tb => {{
                    const blk = new THREE.Mesh(new THREE.BoxGeometry(tb.w, tb.h, 0.004), silkMat);
                    blk.position.set(tb.x, tb.y, silkZ);
                    primaryMesh.add(blk);
                }});

            }} else if (idx === 1) {{
                // ── 2. GOLD PCIe / RAM EDGE CONNECTOR FINGERS ──
                primaryMesh = new THREE.Group();

                // Ultra-Shiny Gold Material
                const goldMat = new THREE.MeshStandardMaterial({{
                    color: 0xFFD700,
                    metalness: 0.98,
                    roughness: 0.05
                }});

                // Dark FR4 Connector Tongue (Tongue tab that plugs into PCIe / DIMM slot)
                const tongueMat = new THREE.MeshStandardMaterial({{
                    color: 0x074620,
                    roughness: 0.40,
                    metalness: 0.25
                }});
                const tongueY = -1.16;
                const tongueHeight = 0.24;
                const tongueThick = 0.052;

                // Left Tongue Segment (from X = -1.35 to X = -0.26)
                const leftTongueW = 1.09;
                const leftTongue = new THREE.Mesh(
                    new THREE.BoxGeometry(leftTongueW, tongueHeight, tongueThick),
                    tongueMat
                );
                leftTongue.position.set(-0.805, tongueY, 0);
                primaryMesh.add(leftTongue);

                // Right Tongue Segment (from X = -0.10 to X = 1.35)
                const rightTongueW = 1.45;
                const rightTongue = new THREE.Mesh(
                    new THREE.BoxGeometry(rightTongueW, tongueHeight, tongueThick),
                    tongueMat
                );
                rightTongue.position.set(0.625, tongueY, 0);
                primaryMesh.add(rightTongue);

                // Beveled insertion edge along bottom of tongue
                const chamferMat = new THREE.MeshStandardMaterial({{
                    color: 0x0e5a2e,
                    roughness: 0.50
                }});
                const leftChamfer = new THREE.Mesh(
                    new THREE.BoxGeometry(leftTongueW, 0.02, tongueThick * 0.7),
                    chamferMat
                );
                leftChamfer.position.set(-0.805, tongueY - tongueHeight / 2, 0);
                const rightChamfer = new THREE.Mesh(
                    new THREE.BoxGeometry(rightTongueW, 0.02, tongueThick * 0.7),
                    chamferMat
                );
                rightChamfer.position.set(0.625, tongueY - tongueHeight / 2, 0);
                primaryMesh.add(leftChamfer);
                primaryMesh.add(rightChamfer);

                // Gold Contact Fingers (20+ individual fingers with key slot gap)
                const fingerGeo = new THREE.BoxGeometry(0.048, 0.20, 0.008);
                const viaGeo = new THREE.CylinderGeometry(0.012, 0.012, 0.010, 10);
                viaGeo.rotateX(Math.PI / 2);

                // Left Bank (12 individual gold fingers, X: -1.30 to -0.31)
                for (let f = 0; f < 12; f++) {{
                    const fx = -1.30 + f * 0.088;
                    // Front gold contact finger
                    const frontFinger = new THREE.Mesh(fingerGeo, goldMat);
                    frontFinger.position.set(fx, tongueY, tongueThick / 2 + 0.004);
                    primaryMesh.add(frontFinger);

                    // Back gold contact finger
                    const backFinger = new THREE.Mesh(fingerGeo, goldMat);
                    backFinger.position.set(fx, tongueY, -tongueThick / 2 - 0.004);
                    primaryMesh.add(backFinger);

                    // Top contact via pad
                    const viaPad = new THREE.Mesh(viaGeo, goldMat);
                    viaPad.position.set(fx, tongueY + 0.11, tongueThick / 2 + 0.004);
                    primaryMesh.add(viaPad);
                }}

                // Notch / Key Slot Gap: from X = -0.26 to X = -0.10 (width 0.16 slot gap)
                // Mechanical slot edge trim
                const notchEdgeGeo = new THREE.BoxGeometry(0.015, tongueHeight, tongueThick + 0.004);
                const notchLeft = new THREE.Mesh(notchEdgeGeo, tongueMat);
                notchLeft.position.set(-0.26, tongueY, 0);
                const notchRight = new THREE.Mesh(notchEdgeGeo, tongueMat);
                notchRight.position.set(-0.10, tongueY, 0);
                primaryMesh.add(notchLeft);
                primaryMesh.add(notchRight);

                // Right Bank (16 individual gold fingers, X: -0.05 to +1.27)
                for (let f = 0; f < 16; f++) {{
                    const fx = -0.05 + f * 0.088;
                    // Front gold contact finger
                    const frontFinger = new THREE.Mesh(fingerGeo, goldMat);
                    frontFinger.position.set(fx, tongueY, tongueThick / 2 + 0.004);
                    primaryMesh.add(frontFinger);

                    // Back gold contact finger
                    const backFinger = new THREE.Mesh(fingerGeo, goldMat);
                    backFinger.position.set(fx, tongueY, -tongueThick / 2 - 0.004);
                    primaryMesh.add(backFinger);

                    // Top contact via pad
                    const viaPad = new THREE.Mesh(viaGeo, goldMat);
                    viaPad.position.set(fx, tongueY + 0.11, tongueThick / 2 + 0.004);
                    primaryMesh.add(viaPad);
                }}

                // Gold power trace bus rail above contact fingers
                const goldBusGeo = new THREE.BoxGeometry(2.65, 0.015, 0.008);
                const goldBus = new THREE.Mesh(goldBusGeo, goldMat);
                goldBus.position.set(-0.02, tongueY + 0.13, tongueThick / 2 + 0.004);
                primaryMesh.add(goldBus);

            }} else if (idx === 2) {{
                // ── 3. CENTRAL BGA PROCESSOR & CHIPSET ──
                primaryMesh = new THREE.Group();

                // Material definitions
                const ihsMat = new THREE.MeshStandardMaterial({{
                    color: 0x888890,
                    metalness: 0.95,
                    roughness: 0.16
                }});
                const dieMat = new THREE.MeshStandardMaterial({{
                    color: 0x0a0a14,
                    metalness: 0.96,
                    roughness: 0.04
                }});
                const subMat = new THREE.MeshStandardMaterial({{
                    color: 0x0d3c1a,
                    roughness: 0.38,
                    metalness: 0.22
                }});
                const bgaMat = new THREE.MeshStandardMaterial({{
                    color: 0xC8D0D8,
                    metalness: 0.98,
                    roughness: 0.10
                }});
                const markMat = new THREE.MeshStandardMaterial({{
                    color: 0x505058,
                    metalness: 0.85,
                    roughness: 0.40
                }});
                const goldPinMat = new THREE.MeshStandardMaterial({{
                    color: 0xFFD700,
                    metalness: 0.98,
                    roughness: 0.08
                }});

                // ═══ MAIN BGA PROCESSOR ASSEMBLY ═══
                const cpuX = -0.35;
                const cpuY = 0.18;

                // Processor Multi-Layer Organic Package Substrate
                const cpuSub = new THREE.Mesh(
                    new THREE.BoxGeometry(1.06, 1.06, 0.035),
                    subMat
                );
                cpuSub.position.set(cpuX, cpuY, 0);
                primaryMesh.add(cpuSub);

                // Pin-1 Gold Index Marker Triangle
                const pin1Mark = new THREE.Mesh(
                    new THREE.BoxGeometry(0.045, 0.045, 0.006),
                    goldPinMat
                );
                pin1Mark.rotation.z = Math.PI / 4;
                pin1Mark.position.set(cpuX - 0.45, cpuY + 0.45, 0.02);
                primaryMesh.add(pin1Mark);

                // BGA Ball Grid Array Underneath Processor (Visible from Side, 8x8 Grid)
                const bgaGeo = new THREE.SphereGeometry(0.016, 8, 8);
                for (let r = 0; r < 8; r++) {{
                    for (let c = 0; c < 8; c++) {{
                        const ball = new THREE.Mesh(bgaGeo, bgaMat);
                        ball.position.set(
                            cpuX - 0.42 + c * 0.12,
                            cpuY - 0.42 + r * 0.12,
                            -0.026
                        );
                        primaryMesh.add(ball);
                    }}
                }}

                // Integrated Heat Spreader (IHS) Base Flange
                const ihsBase = new THREE.Mesh(
                    new THREE.BoxGeometry(0.94, 0.94, 0.028),
                    ihsMat
                );
                ihsBase.position.set(cpuX, cpuY, 0.026);
                primaryMesh.add(ihsBase);

                // IHS Raised Upper Lid (Direct Thermal Contact Face)
                const ihsLid = new THREE.Mesh(
                    new THREE.BoxGeometry(0.78, 0.78, 0.032),
                    ihsMat
                );
                ihsLid.position.set(cpuX, cpuY, 0.048);
                primaryMesh.add(ihsLid);

                // Die Markings & Laser Engraving (Tiny Embossed Rectangles)
                const logoMark = new THREE.Mesh(
                    new THREE.BoxGeometry(0.44, 0.09, 0.004),
                    markMat
                );
                logoMark.position.set(cpuX, cpuY + 0.14, 0.065);
                primaryMesh.add(logoMark);

                const specMark1 = new THREE.Mesh(
                    new THREE.BoxGeometry(0.38, 0.028, 0.004),
                    markMat
                );
                specMark1.position.set(cpuX, cpuY + 0.04, 0.065);
                primaryMesh.add(specMark1);

                const specMark2 = new THREE.Mesh(
                    new THREE.BoxGeometry(0.32, 0.028, 0.004),
                    markMat
                );
                specMark2.position.set(cpuX, cpuY - 0.04, 0.065);
                primaryMesh.add(specMark2);

                // 2D DataMatrix Security QR Square
                const qrMark = new THREE.Mesh(
                    new THREE.BoxGeometry(0.095, 0.095, 0.004),
                    markMat
                );
                qrMark.position.set(cpuX + 0.24, cpuY - 0.20, 0.065);
                primaryMesh.add(qrMark);

                // Central Silicon Die Core Window (underneath/inside IHS)
                const cpuCore = new THREE.Mesh(
                    new THREE.BoxGeometry(0.38, 0.38, 0.015),
                    dieMat
                );
                cpuCore.position.set(cpuX, cpuY, 0.020);
                primaryMesh.add(cpuCore);

                // ═══ SECOND SMALLER CHIPSET NEARBY (PCH SOUTHBRIDGE) ═══
                const pchX = 0.80;
                const pchY = -0.22;

                // Chipset Package Substrate
                const pchSub = new THREE.Mesh(
                    new THREE.BoxGeometry(0.66, 0.66, 0.028),
                    subMat
                );
                pchSub.position.set(pchX, pchY, 0);
                primaryMesh.add(pchSub);

                // BGA Ball Grid Array Underneath Chipset (6x6 Grid, Visible from Side)
                for (let r = 0; r < 6; r++) {{
                    for (let c = 0; c < 6; c++) {{
                        const ball = new THREE.Mesh(bgaGeo, bgaMat);
                        ball.position.set(
                            pchX - 0.25 + c * 0.10,
                            pchY - 0.25 + r * 0.10,
                            -0.022
                        );
                        primaryMesh.add(ball);
                    }}
                }}

                // Exposed Bare Silicon Chipset Die (High-Gloss Dark Silicon)
                const pchDie = new THREE.Mesh(
                    new THREE.BoxGeometry(0.42, 0.42, 0.028),
                    dieMat
                );
                pchDie.position.set(pchX, pchY, 0.026);
                primaryMesh.add(pchDie);

                // Chipset Die Markings & Pin-1 Dot
                const pchMark1 = new THREE.Mesh(
                    new THREE.BoxGeometry(0.24, 0.04, 0.003),
                    markMat
                );
                pchMark1.position.set(pchX, pchY + 0.05, 0.041);
                const pchMark2 = new THREE.Mesh(
                    new THREE.BoxGeometry(0.18, 0.025, 0.003),
                    markMat
                );
                pchMark2.position.set(pchX, pchY - 0.05, 0.041);
                primaryMesh.add(pchMark1);
                primaryMesh.add(pchMark2);

                const pchDot = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.014, 0.014, 0.004, 12),
                    goldPinMat
                );
                pchDot.rotateX(Math.PI / 2);
                pchDot.position.set(pchX - 0.15, pchY + 0.15, 0.041);
                primaryMesh.add(pchDot);

                // Miniature Decoupling Capacitors Surrounding Chipset Die
                const smdDecoupleMat = new THREE.MeshStandardMaterial({{ color: 0xBA8C52, roughness: 0.4 }});
                const decCoords = [
                    [pchX - 0.26, pchY], [pchX + 0.26, pchY],
                    [pchX, pchY - 0.26], [pchX, pchY + 0.26]
                ];
                decCoords.forEach(dc => {{
                    const cap = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.025, 0.02), smdDecoupleMat);
                    cap.position.set(dc[0], dc[1], 0.022);
                    primaryMesh.add(cap);
                }});

            }} else if (idx === 3) {{
                // ── 4. SURFACE MOUNT COMPONENTS ARRAY (SMD) ──
                primaryMesh = new THREE.Group();

                // Material definitions for SMD components
                const solderMat = new THREE.MeshStandardMaterial({{
                    color: 0xDCDDE1,
                    metalness: 0.95,
                    roughness: 0.12
                }});
                const icBlackMat = new THREE.MeshStandardMaterial({{
                    color: 0x151515,
                    roughness: 0.70,
                    metalness: 0.40
                }});
                const mlccMat = new THREE.MeshStandardMaterial({{
                    color: 0xC89658,
                    roughness: 0.35,
                    metalness: 0.15
                }});
                const resBodyMat = new THREE.MeshStandardMaterial({{
                    color: 0x34495E,
                    roughness: 0.45
                }});
                const goldPinMat = new THREE.MeshStandardMaterial({{
                    color: 0xFFD700,
                    metalness: 0.98,
                    roughness: 0.08
                }});

                // 1) 3x Electrolytic Capacitors (Taller cylinders with polarity stripe)
                const elecBodyMat = new THREE.MeshStandardMaterial({{
                    color: 0x1B2A4A,
                    metalness: 0.60,
                    roughness: 0.25
                }});
                const elecVentMat = new THREE.MeshStandardMaterial({{
                    color: 0xD0D3D4,
                    metalness: 0.95,
                    roughness: 0.15
                }});
                const elecStripeMat = new THREE.MeshStandardMaterial({{
                    color: 0xECF0F1,
                    roughness: 0.85
                }});
                const elecBaseMat = new THREE.MeshStandardMaterial({{
                    color: 0x1C1C1C,
                    roughness: 0.90
                }});

                const elecPositions = [
                    [-1.25, 0.65],
                    [-1.25, 0.25],
                    [-1.25, -0.15]
                ];
                elecPositions.forEach(ep => {{
                    // Square plastic mounting base
                    const base = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.22, 0.03), elecBaseMat);
                    base.position.set(ep[0], ep[1], 0.015);
                    primaryMesh.add(base);

                    // Main cylindrical can
                    const canGeo = new THREE.CylinderGeometry(0.095, 0.095, 0.28, 20);
                    canGeo.rotateX(Math.PI / 2);
                    const can = new THREE.Mesh(canGeo, elecBodyMat);
                    can.position.set(ep[0], ep[1], 0.16);
                    primaryMesh.add(can);

                    // Top aluminum vent cap
                    const ventGeo = new THREE.CylinderGeometry(0.093, 0.093, 0.012, 20);
                    ventGeo.rotateX(Math.PI / 2);
                    const vent = new THREE.Mesh(ventGeo, elecVentMat);
                    vent.position.set(ep[0], ep[1], 0.30);
                    primaryMesh.add(vent);

                    // Negative polarity vertical stripe
                    const stripe = new THREE.Mesh(new THREE.BoxGeometry(0.032, 0.26, 0.01), elecStripeMat);
                    stripe.position.set(ep[0] - 0.088, ep[1], 0.16);
                    primaryMesh.add(stripe);
                }});

                // 2) 4x Solid Polymer Capacitors (Small dark/silver aluminum cans)
                const solidCapMat = new THREE.MeshStandardMaterial({{
                    color: 0xE0E4E8,
                    metalness: 0.92,
                    roughness: 0.14
                }});
                const solidTopMat = new THREE.MeshStandardMaterial({{
                    color: 0x922B21,
                    roughness: 0.45
                }});
                const solidXs = [-0.72, -0.36, 0.0, 0.36];
                solidXs.forEach(sx => {{
                    const scGeo = new THREE.CylinderGeometry(0.065, 0.065, 0.16, 16);
                    scGeo.rotateX(Math.PI / 2);
                    const sc = new THREE.Mesh(scGeo, solidCapMat);
                    sc.position.set(sx, 0.82, 0.09);
                    primaryMesh.add(sc);

                    // Colored crescent marking on top face
                    const topGeo = new THREE.CylinderGeometry(0.063, 0.063, 0.008, 16);
                    topGeo.rotateX(Math.PI / 2);
                    const scTop = new THREE.Mesh(topGeo, solidTopMat);
                    scTop.position.set(sx, 0.82, 0.172);
                    primaryMesh.add(scTop);
                }});

                // 3) 4x Resistors with Color Bands (Color coded materials)
                const band1Mat = new THREE.MeshStandardMaterial({{ color: 0x8B4513 }}); // Brown
                const band2Mat = new THREE.MeshStandardMaterial({{ color: 0x111111 }}); // Black
                const band3Mat = new THREE.MeshStandardMaterial({{ color: 0xC0392B }}); // Red
                const bandGoldMat = new THREE.MeshStandardMaterial({{ color: 0xFFD700, metalness: 0.9 }}); // Gold tolerance

                const resPositions = [
                    [-0.85, -0.58],
                    [-0.58, -0.58],
                    [0.32, -0.58],
                    [0.58, -0.58]
                ];
                resPositions.forEach(rp => {{
                    // Ceramic body
                    const rBody = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.055, 0.045), resBodyMat);
                    rBody.position.set(rp[0], rp[1], 0.024);
                    primaryMesh.add(rBody);

                    // Solder end caps
                    const cap1 = new THREE.Mesh(new THREE.BoxGeometry(0.016, 0.058, 0.048), solderMat);
                    cap1.position.set(rp[0] - 0.065, rp[1], 0.024);
                    const cap2 = new THREE.Mesh(new THREE.BoxGeometry(0.016, 0.058, 0.048), solderMat);
                    cap2.position.set(rp[0] + 0.065, rp[1], 0.024);
                    primaryMesh.add(cap1);
                    primaryMesh.add(cap2);

                    // 4 Color Bands
                    const b1 = new THREE.Mesh(new THREE.BoxGeometry(0.014, 0.057, 0.047), band1Mat);
                    b1.position.set(rp[0] - 0.035, rp[1], 0.024);
                    const b2 = new THREE.Mesh(new THREE.BoxGeometry(0.014, 0.057, 0.047), band2Mat);
                    b2.position.set(rp[0] - 0.012, rp[1], 0.024);
                    const b3 = new THREE.Mesh(new THREE.BoxGeometry(0.014, 0.057, 0.047), band3Mat);
                    b3.position.set(rp[0] + 0.012, rp[1], 0.024);
                    const b4 = new THREE.Mesh(new THREE.BoxGeometry(0.014, 0.057, 0.047), bandGoldMat);
                    b4.position.set(rp[0] + 0.035, rp[1], 0.024);
                    primaryMesh.add(b1);
                    primaryMesh.add(b2);
                    primaryMesh.add(b3);
                    primaryMesh.add(b4);
                }});

                // 4) 8x Ceramic Multi-Layer SMD Capacitors (MLCC 0805)
                const mlccCoords = [
                    [-0.42, -0.42], [-0.22, -0.42], [-0.02, -0.42],
                    [0.82, 0.35], [1.02, 0.35],
                    [0.72, 0.62], [0.92, 0.62], [1.12, 0.62]
                ];
                mlccCoords.forEach(mc => {{
                    const mBody = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.045, 0.035), mlccMat);
                    mBody.position.set(mc[0], mc[1], 0.020);
                    const mEnd1 = new THREE.Mesh(new THREE.BoxGeometry(0.016, 0.048, 0.038), solderMat);
                    mEnd1.position.set(mc[0] - 0.036, mc[1], 0.020);
                    const mEnd2 = new THREE.Mesh(new THREE.BoxGeometry(0.016, 0.048, 0.038), solderMat);
                    mEnd2.position.set(mc[0] + 0.036, mc[1], 0.020);
                    primaryMesh.add(mBody);
                    primaryMesh.add(mEnd1);
                    primaryMesh.add(mEnd2);
                }});

                // 5) 4x High-Efficiency Power MOSFETs (D-PAK)
                const mosfetYs = [0.65, 0.40, 0.15, -0.10];
                mosfetYs.forEach(my => {{
                    const mosBody = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.20, 0.045), icBlackMat);
                    mosBody.position.set(-0.96, my, 0.024);
                    const mosTab = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.06, 0.018), solderMat);
                    mosTab.position.set(-0.96, my + 0.12, 0.015);
                    const mosLeg1 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.05, 0.014), solderMat);
                    mosLeg1.position.set(-1.01, my - 0.12, 0.014);
                    const mosLeg2 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.05, 0.014), solderMat);
                    mosLeg2.position.set(-0.91, my - 0.12, 0.014);
                    primaryMesh.add(mosBody);
                    primaryMesh.add(mosTab);
                    primaryMesh.add(mosLeg1);
                    primaryMesh.add(mosLeg2);
                }});

                // 6) IC 1: 8-Pin SOIC Flash/BIOS Chip (with 8 visible silver gull-wing pins)
                const ic1X = 1.20;
                const ic1Y = -0.55;
                const ic1Body = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.32, 0.06), icBlackMat);
                ic1Body.position.set(ic1X, ic1Y, 0.032);
                primaryMesh.add(ic1Body);

                // Pin-1 Dimple
                const ic1Dimple = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.018, 0.018, 0.005, 12),
                    new THREE.MeshStandardMaterial({{ color: 0x080808 }})
                );
                ic1Dimple.rotateX(Math.PI / 2);
                ic1Dimple.position.set(ic1X - 0.07, ic1Y + 0.11, 0.063);
                primaryMesh.add(ic1Dimple);

                // 8 Gull-Wing Pins (4 along left, 4 along right)
                for (let p = 0; p < 4; p++) {{
                    const py = ic1Y - 0.10 + p * 0.066;
                    const pinL = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.020, 0.015), solderMat);
                    pinL.position.set(ic1X - 0.14, py, 0.015);
                    const pinR = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.020, 0.015), solderMat);
                    pinR.position.set(ic1X + 0.14, py, 0.015);
                    primaryMesh.add(pinL);
                    primaryMesh.add(pinR);
                }}

                // 7) IC 2: QFP 32-Pin High-Definition Audio/LAN Controller
                const qfpX = 1.15;
                const qfpY = 0.05;
                const qfpBody = new THREE.Mesh(new THREE.BoxGeometry(0.40, 0.40, 0.055), icBlackMat);
                qfpBody.position.set(qfpX, qfpY, 0.030);
                primaryMesh.add(qfpBody);

                // Laser text label on top
                const qfpLabel = new THREE.Mesh(
                    new THREE.BoxGeometry(0.22, 0.12, 0.004),
                    new THREE.MeshStandardMaterial({{ color: 0x555555, roughness: 0.6 }})
                );
                qfpLabel.position.set(qfpX, qfpY, 0.059);
                primaryMesh.add(qfpLabel);

                // Quad Pins on all 4 sides
                for (let q = 0; q < 6; q++) {{
                    const qOffset = -0.15 + q * 0.06;
                    // Left and right pin rows
                    const pLeft = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.018, 0.014), solderMat);
                    pLeft.position.set(qfpX - 0.22, qfpY + qOffset, 0.015);
                    const pRight = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.018, 0.014), solderMat);
                    pRight.position.set(qfpX + 0.22, qfpY + qOffset, 0.015);
                    // Top and bottom pin rows
                    const pTop = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.045, 0.014), solderMat);
                    pTop.position.set(qfpX + qOffset, qfpY + 0.22, 0.015);
                    const pBtm = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.045, 0.014), solderMat);
                    pBtm.position.set(qfpX + qOffset, qfpY - 0.22, 0.015);
                    primaryMesh.add(pLeft);
                    primaryMesh.add(pRight);
                    primaryMesh.add(pTop);
                    primaryMesh.add(pBtm);
                }}

                // 8) Quartz Crystal Oscillator (Metallic Can Cylinder)
                const xtalMat = new THREE.MeshStandardMaterial({{
                    color: 0xF0F3F4,
                    metalness: 0.98,
                    roughness: 0.08
                }});
                const xtalGeo = new THREE.CylinderGeometry(0.055, 0.055, 0.22, 20);
                xtalGeo.rotateZ(Math.PI / 2);
                const xtalCan = new THREE.Mesh(xtalGeo, xtalMat);
                xtalCan.position.set(0.48, 0.18, 0.045);
                primaryMesh.add(xtalCan);

                // Crystal insulator base & solder pads
                const xtalBase = new THREE.Mesh(
                    new THREE.BoxGeometry(0.24, 0.09, 0.015),
                    new THREE.MeshStandardMaterial({{ color: 0x222222, roughness: 0.8 }})
                );
                xtalBase.position.set(0.48, 0.18, 0.015);
                primaryMesh.add(xtalBase);

                // 9) Hardware Connectors (Rectangular blocks with pin arrays)
                // ATX 4-Pin Auxiliary Power Header
                const connIvoryMat = new THREE.MeshStandardMaterial({{
                    color: 0xEDEADE,
                    roughness: 0.50
                }});
                const atxShroud = new THREE.Mesh(
                    new THREE.BoxGeometry(0.32, 0.24, 0.18),
                    connIvoryMat
                );
                atxShroud.position.set(-1.28, 0.92, 0.09);
                primaryMesh.add(atxShroud);

                // 4 Gold Square Pins Inside Header
                for (let pr = 0; pr < 2; pr++) {{
                    for (let pc = 0; pc < 2; pc++) {{
                        const pin = new THREE.Mesh(new THREE.BoxGeometry(0.026, 0.026, 0.14), goldPinMat);
                        pin.position.set(-1.33 + pc * 0.10, 0.87 + pr * 0.10, 0.11);
                        primaryMesh.add(pin);
                    }}
                }}

                // Front Panel / USB Header (Black plastic block with 2x5 gold pin array)
                const hdrBlock = new THREE.Mesh(
                    new THREE.BoxGeometry(0.36, 0.16, 0.10),
                    new THREE.MeshStandardMaterial({{ color: 0x202020, roughness: 0.7 }})
                );
                hdrBlock.position.set(1.18, 0.88, 0.05);
                primaryMesh.add(hdrBlock);

                for (let r = 0; r < 2; r++) {{
                    for (let c = 0; c < 5; c++) {{
                        const pin = new THREE.Mesh(new THREE.BoxGeometry(0.020, 0.020, 0.12), goldPinMat);
                        pin.position.set(1.04 + c * 0.07, 0.84 + r * 0.08, 0.09);
                        primaryMesh.add(pin);
                    }}
                }}

                // Right-Angle SATA Storage Connector Block
                const sataBody = new THREE.Mesh(
                    new THREE.BoxGeometry(0.18, 0.38, 0.13),
                    new THREE.MeshStandardMaterial({{ color: 0x1A1A1A, roughness: 0.5 }})
                );
                sataBody.position.set(1.38, -0.85, 0.065);
                const sataClip = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.20, 0.02), solderMat);
                sataClip.position.set(1.29, -0.85, 0.08);
                primaryMesh.add(sataBody);
                primaryMesh.add(sataClip);

            }} else {{
                // ── 5. EXTRUDED ALUMINUM FINNED HEATSINK ──
                primaryMesh = new THREE.Group();

                // Aluminum Heatsink Material
                const aluMat = new THREE.MeshStandardMaterial({{
                    color: 0xB8BCC0,
                    metalness: 0.92,
                    roughness: 0.15
                }});

                // ═══ PRIMARY PROCESSOR EXTRUDED FINNED HEATSINK ═══
                const hsX = -0.35;
                const hsY = 0.18;

                // Solid Extruded Aluminum Base Plate Slab
                const baseWidth = 1.08;
                const baseHeight = 1.08;
                const baseThick = 0.070;
                const hsBase = new THREE.Mesh(
                    new THREE.BoxGeometry(baseWidth, baseHeight, baseThick),
                    aluMat
                );
                hsBase.position.set(hsX, hsY, 0.035);
                primaryMesh.add(hsBase);

                // 9 Parallel Thin Vertical Aluminum Fins (Extruded Cooling Fins)
                const numFins = 9;
                const finThickness = 0.032;
                const finDepth = 0.40;
                const finSpacing = (baseWidth - finThickness) / (numFins - 1);
                const finGeo = new THREE.BoxGeometry(finThickness, baseHeight, finDepth);

                for (let f = 0; f < numFins; f++) {{
                    const fx = hsX - (baseWidth / 2 - finThickness / 2) + f * finSpacing;
                    const fin = new THREE.Mesh(finGeo, aluMat);
                    fin.position.set(fx, hsY, baseThick + finDepth / 2);
                    primaryMesh.add(fin);
                }}

                // Thermal Paste Pad (Visible Gray Rectangle at Underside Base)
                const pasteMat = new THREE.MeshStandardMaterial({{
                    color: 0x7F8C8D,
                    roughness: 0.96,
                    metalness: 0.04
                }});
                const thermalPad = new THREE.Mesh(
                    new THREE.BoxGeometry(0.68, 0.68, 0.014),
                    pasteMat
                );
                thermalPad.position.set(hsX, hsY, -0.007);
                primaryMesh.add(thermalPad);

                // Spring-Loaded Mounting Pushpins at 4 Corners
                const pinShaftGeo = new THREE.CylinderGeometry(0.028, 0.028, 0.32, 16);
                pinShaftGeo.rotateX(Math.PI / 2);
                const pinShaftMat = new THREE.MeshStandardMaterial({{
                    color: 0x222222,
                    roughness: 0.6
                }});

                const springGeo = new THREE.CylinderGeometry(0.055, 0.055, 0.16, 16);
                springGeo.rotateX(Math.PI / 2);
                const springMat = new THREE.MeshStandardMaterial({{
                    color: 0xD5D8DC,
                    metalness: 0.98,
                    roughness: 0.10
                }});

                const capGeo = new THREE.CylinderGeometry(0.075, 0.075, 0.04, 16);
                capGeo.rotateX(Math.PI / 2);
                const capMat = new THREE.MeshStandardMaterial({{
                    color: 0x1A1A1A,
                    roughness: 0.8
                }});

                const cornerPushpinOffsets = [
                    [-0.62, 0.62],
                    [0.62, 0.62],
                    [-0.62, -0.62],
                    [0.62, -0.62]
                ];
                cornerPushpinOffsets.forEach(cpo => {{
                    const px = hsX + cpo[0];
                    const py = hsY + cpo[1];

                    // Aluminum Mounting Flange Ear
                    const ear = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.20, 0.04), aluMat);
                    ear.position.set(px, py, 0.02);
                    primaryMesh.add(ear);

                    // Central Pin Shaft
                    const shaft = new THREE.Mesh(pinShaftGeo, pinShaftMat);
                    shaft.position.set(px, py, 0.12);
                    primaryMesh.add(shaft);

                    // Helical Compression Spring Collar
                    const spring = new THREE.Mesh(springGeo, springMat);
                    spring.position.set(px, py, 0.16);
                    primaryMesh.add(spring);

                    // Pushpin Head / Thumb Cap
                    const pushCap = new THREE.Mesh(capGeo, capMat);
                    pushCap.position.set(px, py, 0.27);
                    primaryMesh.add(pushCap);
                }});

                // ═══ SECONDARY CHIPSET EXTRUDED ALUMINUM HEATSINK ═══
                const pchHsX = 0.80;
                const pchHsY = -0.22;

                // Chipset Heatsink Base Plate
                const pchHsBase = new THREE.Mesh(
                    new THREE.BoxGeometry(0.65, 0.65, 0.045),
                    aluMat
                );
                pchHsBase.position.set(pchHsX, pchHsY, 0.022);
                primaryMesh.add(pchHsBase);

                // 6 Parallel Cooling Fins on Chipset Heatsink
                const pchFinGeo = new THREE.BoxGeometry(0.028, 0.65, 0.22);
                for (let pf = 0; pf < 6; pf++) {{
                    const pfx = pchHsX - 0.26 + pf * 0.104;
                    const pFin = new THREE.Mesh(pchFinGeo, aluMat);
                    pFin.position.set(pfx, pchHsY, 0.045 + 0.11);
                    primaryMesh.add(pFin);
                }}

                // Underside Thermal Interface Pad (Blue Silicone Pad)
                const thermalPadPch = new THREE.Mesh(
                    new THREE.BoxGeometry(0.44, 0.44, 0.012),
                    new THREE.MeshStandardMaterial({{ color: 0x3498DB, roughness: 0.90 }})
                );
                thermalPadPch.position.set(pchHsX, pchHsY, -0.006);
                primaryMesh.add(thermalPadPch);

                // Diagonal Wire Spring Retention Clip
                const clipMat = new THREE.MeshStandardMaterial({{
                    color: 0xCCCCCC,
                    metalness: 0.98,
                    roughness: 0.12
                }});
                const wireClip = new THREE.Mesh(
                    new THREE.BoxGeometry(0.022, 0.88, 0.022),
                    clipMat
                );
                wireClip.rotation.z = Math.PI / 4;
                wireClip.position.set(pchHsX, pchHsY, 0.18);
                primaryMesh.add(wireClip);
            }}

        }} else if (type === 'display') {{
            // ═══ WIDESCREEN DISPLAY / TELEVISION ═══
            if (idx === 0) {{
                // ── REAR HOUSING with PORTS, VENTS, BRAND LOGO ──
                primaryMesh = new THREE.Group();
                const rearShell = new THREE.Mesh(
                    new THREE.BoxGeometry(4.2, 2.6, 0.12),
                    new THREE.MeshStandardMaterial({{ color: 0x1a1a20, roughness: 0.6, metalness: 0.3 }})
                );
                primaryMesh.add(rearShell);

                // Ventilation slot grid (16 slots)
                for (let v = 0; v < 16; v++) {{
                    const slot = new THREE.Mesh(
                        new THREE.BoxGeometry(0.2, 0.025, 0.01),
                        new THREE.MeshStandardMaterial({{ color: 0x060608 }})
                    );
                    slot.position.set(-1.6 + v * 0.2, 0.9, -0.065);
                    primaryMesh.add(slot);
                }}

                // VESA 100x100 mount holes with screw threads
                for (let mx = -1; mx <= 1; mx += 2) {{
                    for (let my = -1; my <= 1; my += 2) {{
                        const ring = new THREE.Mesh(
                            new THREE.CylinderGeometry(0.045, 0.045, 0.13, 16),
                            new THREE.MeshStandardMaterial({{ color: 0x555560, metalness: 0.9 }})
                        );
                        ring.rotation.x = Math.PI / 2;
                        ring.position.set(mx * 0.5, my * 0.5, -0.06);
                        primaryMesh.add(ring);
                        const hole = new THREE.Mesh(
                            new THREE.CylinderGeometry(0.025, 0.025, 0.14, 12),
                            new THREE.MeshStandardMaterial({{ color: 0x080810 }})
                        );
                        hole.rotation.x = Math.PI / 2;
                        hole.position.set(mx * 0.5, my * 0.5, -0.06);
                        primaryMesh.add(hole);
                    }}
                }}

                // I/O Port cluster (HDMI x2, DP, USB, Audio, Power)
                const portY = -0.6;
                const portZ = -0.065;
                // HDMI ports (2x gold-lined trapezoid)
                for (let h = 0; h < 2; h++) {{
                    const hdmi = new THREE.Mesh(
                        new THREE.BoxGeometry(0.22, 0.08, 0.04),
                        new THREE.MeshStandardMaterial({{ color: 0x333340, metalness: 0.7 }})
                    );
                    hdmi.position.set(-1.2 + h * 0.35, portY, portZ);
                    primaryMesh.add(hdmi);
                    // Gold contacts inside
                    const contacts = new THREE.Mesh(
                        new THREE.BoxGeometry(0.18, 0.04, 0.02),
                        new THREE.MeshStandardMaterial({{ color: 0xFFD700, metalness: 0.98, roughness: 0.05 }})
                    );
                    contacts.position.set(-1.2 + h * 0.35, portY, portZ - 0.01);
                    primaryMesh.add(contacts);
                }}
                // DisplayPort
                const dp = new THREE.Mesh(
                    new THREE.BoxGeometry(0.2, 0.08, 0.04),
                    new THREE.MeshStandardMaterial({{ color: 0x444450, metalness: 0.7 }})
                );
                dp.position.set(-0.3, portY, portZ);
                primaryMesh.add(dp);
                // USB-A port
                const usb = new THREE.Mesh(
                    new THREE.BoxGeometry(0.18, 0.06, 0.04),
                    new THREE.MeshStandardMaterial({{ color: 0x1166cc, metalness: 0.5 }})
                );
                usb.position.set(0.1, portY, portZ);
                primaryMesh.add(usb);
                // 3.5mm Audio jack
                const audio = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.025, 0.025, 0.04, 12),
                    new THREE.MeshStandardMaterial({{ color: 0x22cc44, metalness: 0.5 }})
                );
                audio.rotation.x = Math.PI / 2;
                audio.position.set(0.4, portY, portZ);
                primaryMesh.add(audio);
                // DC Power barrel jack
                const power = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.04, 0.04, 0.06, 12),
                    new THREE.MeshStandardMaterial({{ color: 0x222230, metalness: 0.6 }})
                );
                power.rotation.x = Math.PI / 2;
                power.position.set(0.8, portY, portZ);
                primaryMesh.add(power);

                // Brand logo emboss (silver rectangle on back)
                const logo = new THREE.Mesh(
                    new THREE.BoxGeometry(0.6, 0.15, 0.005),
                    new THREE.MeshStandardMaterial({{ color: 0x888895, metalness: 0.85, roughness: 0.15 }})
                );
                logo.position.set(0, 0.2, -0.065);
                primaryMesh.add(logo);

                // Product label sticker
                const label = new THREE.Mesh(
                    new THREE.BoxGeometry(0.8, 0.3, 0.003),
                    new THREE.MeshStandardMaterial({{ color: 0xf0f0f0, roughness: 0.8 }})
                );
                label.position.set(0.8, -0.2, -0.065);
                primaryMesh.add(label);
            }} else if (idx === 1) {{
                // Backlight Diffuser Layer
                primaryMesh = new THREE.Mesh(
                    new THREE.BoxGeometry(3.9, 2.3, 0.03),
                    new THREE.MeshStandardMaterial({{ color: 0xe8e8f0, roughness: 0.1, metalness: 0.05, emissive: 0xffffff, emissiveIntensity: 0.15 }})
                );
            }} else if (idx === 2) {{
                // ── CONTROLLER BOARD & POWER SUPPLY (T-CON + SMPS) ──
                primaryMesh = new THREE.Group();
                const mainPCB = new THREE.Mesh(
                    new THREE.BoxGeometry(1.8, 0.8, 0.04),
                    new THREE.MeshStandardMaterial({{ color: 0x0a5c2a, roughness: 0.35 }})
                );
                primaryMesh.add(mainPCB);
                // Electrolytic capacitors (tall, with stripe)
                for (let c = 0; c < 5; c++) {{
                    const cap = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.06, 0.06, 0.22, 16),
                        new THREE.MeshStandardMaterial({{ color: 0x111118, metalness: 0.6 }})
                    );
                    cap.position.set(-0.6 + c * 0.25, 0.14, 0);
                    primaryMesh.add(cap);
                    // Silver stripe on cap
                    const stripe = new THREE.Mesh(
                        new THREE.BoxGeometry(0.005, 0.22, 0.03),
                        new THREE.MeshStandardMaterial({{ color: 0xcccccc }})
                    );
                    stripe.position.set(-0.6 + c * 0.25 + 0.055, 0.14, 0);
                    primaryMesh.add(stripe);
                }}
                // Main transformer
                const xfm = new THREE.Mesh(
                    new THREE.BoxGeometry(0.4, 0.35, 0.3),
                    new THREE.MeshStandardMaterial({{ color: 0x222230, metalness: 0.5 }})
                );
                xfm.position.set(0.6, 0.2, 0);
                primaryMesh.add(xfm);
                // T-CON timing chip
                const tcon = new THREE.Mesh(
                    new THREE.BoxGeometry(0.25, 0.04, 0.25),
                    new THREE.MeshStandardMaterial({{ color: 0x0a0a14, metalness: 0.7 }})
                );
                tcon.position.set(-0.3, 0.04, -0.2);
                primaryMesh.add(tcon);
                // LVDS flat ribbon connector
                const lvds = new THREE.Mesh(
                    new THREE.BoxGeometry(0.5, 0.06, 0.08),
                    new THREE.MeshStandardMaterial({{ color: 0xdddddd, roughness: 0.4 }})
                );
                lvds.position.set(0, 0.04, 0.35);
                primaryMesh.add(lvds);
                // SMD components scattered
                const smdMat = new THREE.MeshStandardMaterial({{ color: 0x555560, metalness: 0.7 }});
                for (let s = 0; s < 15; s++) {{
                    const smd = new THREE.Mesh(
                        new THREE.BoxGeometry(0.06, 0.025, 0.04),
                        smdMat
                    );
                    smd.position.set(-0.7 + (s % 5) * 0.25, 0.035, -0.3 + Math.floor(s / 5) * 0.2);
                    primaryMesh.add(smd);
                }}
            }} else if (idx === 3) {{
                // ── DESKTOP STAND & PEDESTAL ──
                primaryMesh = new THREE.Group();
                // Adjustable neck arm
                const neck = new THREE.Mesh(
                    new THREE.BoxGeometry(0.25, 1.0, 0.12),
                    new THREE.MeshStandardMaterial({{ color: 0x3a3a42, metalness: 0.8, roughness: 0.25 }})
                );
                neck.position.set(0, -1.8, 0.1);
                primaryMesh.add(neck);
                // Cable management clip on neck
                const clip = new THREE.Mesh(
                    new THREE.TorusGeometry(0.08, 0.015, 8, 16, Math.PI),
                    new THREE.MeshStandardMaterial({{ color: 0x444450, metalness: 0.7 }})
                );
                clip.position.set(0, -1.5, 0.18);
                primaryMesh.add(clip);
                // Heavy round base
                const base = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.7, 0.8, 0.08, 32),
                    new THREE.MeshStandardMaterial({{ color: 0x2a2a30, metalness: 0.85, roughness: 0.2 }})
                );
                base.position.set(0, -2.3, 0.1);
                primaryMesh.add(base);
                // Anti-slip rubber pad on base
                const pad = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.65, 0.65, 0.01, 32),
                    new THREE.MeshStandardMaterial({{ color: 0x222228, roughness: 0.9 }})
                );
                pad.position.set(0, -2.34, 0.1);
                primaryMesh.add(pad);
            }} else {{
                // ── FRONT PANEL (LCD + MICRO-BEZEL + OSD BUTTONS) ──
                primaryMesh = new THREE.Group();
                // Outer bezel frame
                const bezel = new THREE.Mesh(
                    new THREE.BoxGeometry(4.2, 2.6, 0.04),
                    new THREE.MeshStandardMaterial({{ color: 0x111116, roughness: 0.5 }})
                );
                primaryMesh.add(bezel);
                // Main LCD screen panel with display UI texture
                const screenMat = new THREE.MeshStandardMaterial({{
                    color: 0xffffff,
                    roughness: 0.05,
                    metalness: 0.05,
                    emissive: 0x0a1828,
                    emissiveIntensity: 0.35
                }});
                try {{ screenMat.map = createDisplayUITexture(); }} catch(e) {{}}
                const screen = new THREE.Mesh(
                    new THREE.BoxGeometry(4.0, 2.4, 0.02),
                    screenMat
                );
                screen.position.z = 0.03;
                primaryMesh.add(screen);
                // Power LED indicator
                const led = new THREE.Mesh(
                    new THREE.SphereGeometry(0.025, 12, 12),
                    new THREE.MeshStandardMaterial({{ color: 0x00ff66, emissive: 0x00ff66, emissiveIntensity: 1.0 }})
                );
                led.position.set(0, -1.25, 0.03);
                primaryMesh.add(led);
                // OSD navigation joystick/buttons on bottom edge
                for (let ob = 0; ob < 4; ob++) {{
                    const osd = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.02, 0.02, 0.015, 8),
                        new THREE.MeshStandardMaterial({{ color: 0x444450, metalness: 0.6 }})
                    );
                    osd.rotation.x = Math.PI / 2;
                    osd.position.set(0.8 + ob * 0.15, -1.25, 0.03);
                    primaryMesh.add(osd);
                }}
            }}

        }} else if (type === 'printer') {{
            // ═══ PRINTER / SCANNER ═══
            if (idx === 0) {{
                // Main Body Housing
                primaryMesh = new THREE.Group();
                const body = new THREE.Mesh(
                    new THREE.BoxGeometry(3.2, 1.4, 2.4),
                    new THREE.MeshStandardMaterial({{ color: 0x222228, roughness: 0.5, metalness: 0.2 }})
                );
                primaryMesh.add(body);
                // Control panel
                const panel = new THREE.Mesh(
                    new THREE.BoxGeometry(1.2, 0.08, 0.5),
                    new THREE.MeshStandardMaterial({{ color: 0x1a1a22, roughness: 0.3, emissive: 0x113388, emissiveIntensity: 0.15 }})
                );
                panel.position.set(0, 0.74, -0.8);
                primaryMesh.add(panel);
                // Buttons
                for (let b = 0; b < 4; b++) {{
                    const btn = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.04, 0.04, 0.02, 16),
                        new THREE.MeshStandardMaterial({{ color: b === 0 ? 0x00cc44 : 0x888890, metalness: 0.5 }})
                    );
                    btn.rotation.x = Math.PI / 2;
                    btn.position.set(-0.3 + b * 0.2, 0.74, -1.1);
                    primaryMesh.add(btn);
                }}
            }} else if (idx === 1) {{
                // Paper Feed Cassette Tray
                primaryMesh = new THREE.Mesh(
                    new THREE.BoxGeometry(2.8, 0.15, 2.0),
                    new THREE.MeshStandardMaterial({{ color: 0xf0f0f0, roughness: 0.4 }})
                );
                primaryMesh.position.set(0, -0.6, 0);
                // Paper stack
                const paper = new THREE.Mesh(
                    new THREE.BoxGeometry(2.4, 0.08, 1.6),
                    new THREE.MeshStandardMaterial({{ color: 0xffffff, roughness: 0.8 }})
                );
                paper.position.set(0, -0.52, 0);
                const g = new THREE.Group();
                g.add(primaryMesh); g.add(paper);
                primaryMesh = g;
            }} else if (idx === 2) {{
                // Scanner Glass Flatbed + Lid
                primaryMesh = new THREE.Group();
                const glass = new THREE.Mesh(
                    new THREE.BoxGeometry(3.0, 0.03, 2.2),
                    new THREE.MeshStandardMaterial({{ color: 0xaaccdd, transparent: true, opacity: 0.4, roughness: 0.05, metalness: 0.1 }})
                );
                glass.position.y = 0.72;
                primaryMesh.add(glass);
                const lid = new THREE.Mesh(
                    new THREE.BoxGeometry(3.1, 0.06, 2.3),
                    new THREE.MeshStandardMaterial({{ color: 0x1a1a20, roughness: 0.6 }})
                );
                lid.position.y = 0.78;
                primaryMesh.add(lid);
            }} else if (idx === 3) {{
                // Toner/Ink Cartridge Assembly
                primaryMesh = new THREE.Group();
                const colors = [0x111118, 0x00aadd, 0xdd2266, 0xddcc00];
                for (let t = 0; t < 4; t++) {{
                    const cart = new THREE.Mesh(
                        new THREE.BoxGeometry(0.4, 0.6, 1.4),
                        new THREE.MeshStandardMaterial({{ color: colors[t], roughness: 0.5, metalness: 0.3 }})
                    );
                    cart.position.set(-0.75 + t * 0.5, 0.1, 0);
                    primaryMesh.add(cart);
                }}
            }} else {{
                // Internal Drive Rollers & Stepper Motor
                primaryMesh = new THREE.Group();
                for (let r = 0; r < 3; r++) {{
                    const roller = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.08, 0.08, 2.8, 16),
                        new THREE.MeshStandardMaterial({{ color: 0x333340, metalness: 0.7, roughness: 0.3 }})
                    );
                    roller.rotation.z = Math.PI / 2;
                    roller.position.set(0, -0.2 + r * 0.25, -0.3 + r * 0.4);
                    primaryMesh.add(roller);
                }}
                const motor = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.15, 0.15, 0.3, 16),
                    new THREE.MeshStandardMaterial({{ color: 0x555560, metalness: 0.8 }})
                );
                motor.position.set(1.2, -0.1, 0.5);
                primaryMesh.add(motor);
            }}

        }} else if (type === 'cable') {{
            // ═══ CABLES & WIRES ═══
            if (idx === 0) {{
                // PVC Outer Sleeve
                primaryMesh = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.25, 0.25, 4.5, 24),
                    new THREE.MeshStandardMaterial({{ color: 0x1a1a22, roughness: 0.6 }})
                );
                primaryMesh.rotation.z = Math.PI / 2;
            }} else if (idx === 1) {{
                // Braided Shield
                primaryMesh = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.2, 0.2, 4.0, 24),
                    new THREE.MeshStandardMaterial({{ color: 0xC0C0C0, metalness: 0.9, roughness: 0.15 }})
                );
                primaryMesh.rotation.z = Math.PI / 2;
            }} else if (idx === 2) {{
                // Color-Coded Conductor Cores (4 wires)
                primaryMesh = new THREE.Group();
                const wireColors = [0xcc2222, 0x22cc22, 0x2266cc, 0xdddddd];
                for (let w = 0; w < 4; w++) {{
                    const wire = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.045, 0.045, 3.5, 12),
                        new THREE.MeshStandardMaterial({{ color: wireColors[w], roughness: 0.5 }})
                    );
                    wire.rotation.z = Math.PI / 2;
                    const angle = (w / 4) * Math.PI * 2;
                    wire.position.set(0, Math.cos(angle) * 0.1, Math.sin(angle) * 0.1);
                    primaryMesh.add(wire);
                }}
            }} else if (idx === 3) {{
                // Copper Core Strands
                primaryMesh = new THREE.Group();
                for (let s = 0; s < 12; s++) {{
                    const strand = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.012, 0.012, 3.0, 6),
                        new THREE.MeshStandardMaterial({{ color: 0xB87333, metalness: 0.95, roughness: 0.1 }})
                    );
                    strand.rotation.z = Math.PI / 2;
                    const angle = (s / 12) * Math.PI * 2;
                    strand.position.set(0, Math.cos(angle) * 0.06, Math.sin(angle) * 0.06);
                    primaryMesh.add(strand);
                }}
            }} else {{
                // USB/RJ45 Connector with Gold Pins
                primaryMesh = new THREE.Group();
                const housing = new THREE.Mesh(
                    new THREE.BoxGeometry(0.45, 0.2, 0.35),
                    new THREE.MeshStandardMaterial({{ color: 0x888890, metalness: 0.8, roughness: 0.2 }})
                );
                housing.position.x = 2.0;
                primaryMesh.add(housing);
                for (let p = 0; p < 8; p++) {{
                    const pin = new THREE.Mesh(
                        new THREE.BoxGeometry(0.015, 0.008, 0.12),
                        new THREE.MeshStandardMaterial({{ color: 0xFFD700, metalness: 0.98, roughness: 0.05 }})
                    );
                    pin.position.set(2.0, 0.05, -0.12 + p * 0.035);
                    primaryMesh.add(pin);
                }}
                // Second connector
                const h2 = housing.clone();
                h2.position.x = -2.0;
                primaryMesh.add(h2);
            }}

        }} else if (type === 'networking') {{
            // ═══ NETWORKING / ROUTER ═══
            if (idx === 0) {{
                // Router Chassis
                primaryMesh = new THREE.Group();
                const body = new THREE.Mesh(
                    new THREE.BoxGeometry(2.8, 0.35, 1.8),
                    new THREE.MeshStandardMaterial({{ color: 0x111118, roughness: 0.4, metalness: 0.3 }})
                );
                primaryMesh.add(body);
                // Ventilation slots on top
                for (let v = 0; v < 12; v++) {{
                    const slot = new THREE.Mesh(
                        new THREE.BoxGeometry(0.15, 0.005, 1.2),
                        new THREE.MeshStandardMaterial({{ color: 0x080810 }})
                    );
                    slot.position.set(-1.1 + v * 0.2, 0.178, 0);
                    primaryMesh.add(slot);
                }}
                // Status LEDs
                for (let l = 0; l < 5; l++) {{
                    const led = new THREE.Mesh(
                        new THREE.SphereGeometry(0.02, 8, 8),
                        new THREE.MeshStandardMaterial({{ color: 0x00ff44, emissive: 0x00ff44, emissiveIntensity: 0.8 }})
                    );
                    led.position.set(-0.8 + l * 0.25, 0.178, -0.7);
                    primaryMesh.add(led);
                }}
            }} else if (idx === 1) {{
                // External Antennas (4x dipole)
                primaryMesh = new THREE.Group();
                for (let a = 0; a < 4; a++) {{
                    const ant = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.03, 0.025, 1.6, 12),
                        new THREE.MeshStandardMaterial({{ color: 0x1a1a22, roughness: 0.5 }})
                    );
                    ant.position.set(-0.9 + a * 0.6, 0.95, 0.8);
                    ant.rotation.x = -0.15;
                    primaryMesh.add(ant);
                    // Hinge joint
                    const hinge = new THREE.Mesh(
                        new THREE.SphereGeometry(0.04, 8, 8),
                        new THREE.MeshStandardMaterial({{ color: 0x333340, metalness: 0.7 }})
                    );
                    hinge.position.set(-0.9 + a * 0.6, 0.18, 0.8);
                    primaryMesh.add(hinge);
                }}
            }} else if (idx === 2) {{
                // Ethernet RJ45 Ports (4 ports)
                primaryMesh = new THREE.Group();
                for (let e = 0; e < 4; e++) {{
                    const port = new THREE.Mesh(
                        new THREE.BoxGeometry(0.22, 0.18, 0.2),
                        new THREE.MeshStandardMaterial({{ color: 0xddcc00, metalness: 0.4, roughness: 0.5 }})
                    );
                    port.position.set(-0.5 + e * 0.35, 0, -0.9);
                    primaryMesh.add(port);
                    // Gold contacts inside
                    for (let g = 0; g < 8; g++) {{
                        const pin = new THREE.Mesh(
                            new THREE.BoxGeometry(0.008, 0.01, 0.06),
                            new THREE.MeshStandardMaterial({{ color: 0xFFD700, metalness: 0.98 }})
                        );
                        pin.position.set(-0.58 + e * 0.35 + g * 0.02, 0.05, -0.92);
                        primaryMesh.add(pin);
                    }}
                }}
                // WAN port (blue)
                const wan = new THREE.Mesh(
                    new THREE.BoxGeometry(0.22, 0.18, 0.2),
                    new THREE.MeshStandardMaterial({{ color: 0x2266cc, metalness: 0.4 }})
                );
                wan.position.set(1.0, 0, -0.9);
                primaryMesh.add(wan);
            }} else if (idx === 3) {{
                // Internal Wi-Fi SoC Board & Heatsink
                primaryMesh = new THREE.Group();
                const pcb = new THREE.Mesh(
                    new THREE.BoxGeometry(2.4, 0.04, 1.4),
                    new THREE.MeshStandardMaterial({{ color: 0x0a5c2a, roughness: 0.35 }})
                );
                primaryMesh.add(pcb);
                // Main SoC chip
                const soc = new THREE.Mesh(
                    new THREE.BoxGeometry(0.4, 0.06, 0.4),
                    new THREE.MeshStandardMaterial({{ color: 0x111118, metalness: 0.7 }})
                );
                soc.position.set(0, 0.05, 0);
                primaryMesh.add(soc);
                // Heatsink on SoC
                const hs = new THREE.Mesh(
                    new THREE.BoxGeometry(0.5, 0.15, 0.5),
                    new THREE.MeshStandardMaterial({{ color: 0xB8BCC0, metalness: 0.92, roughness: 0.15 }})
                );
                hs.position.set(0, 0.12, 0);
                primaryMesh.add(hs);
                // RAM chip
                const ram = new THREE.Mesh(
                    new THREE.BoxGeometry(0.3, 0.04, 0.15),
                    new THREE.MeshStandardMaterial({{ color: 0x0a0a14, metalness: 0.6 }})
                );
                ram.position.set(-0.7, 0.04, 0.3);
                primaryMesh.add(ram);
                // Flash storage
                const flash = new THREE.Mesh(
                    new THREE.BoxGeometry(0.2, 0.03, 0.2),
                    new THREE.MeshStandardMaterial({{ color: 0x1a1a28, metalness: 0.5 }})
                );
                flash.position.set(0.7, 0.04, -0.3);
                primaryMesh.add(flash);
            }} else {{
                // Power Adapter Port & DC Jack
                primaryMesh = new THREE.Group();
                const jack = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.06, 0.06, 0.15, 16),
                    new THREE.MeshStandardMaterial({{ color: 0x222230, metalness: 0.7 }})
                );
                jack.rotation.x = Math.PI / 2;
                jack.position.set(1.3, 0, -0.9);
                primaryMesh.add(jack);
                const resetBtn = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.015, 0.015, 0.05, 8),
                    new THREE.MeshStandardMaterial({{ color: 0xcc2222 }})
                );
                resetBtn.rotation.x = Math.PI / 2;
                resetBtn.position.set(-1.2, -0.05, -0.9);
                primaryMesh.add(resetBtn);
            }}

        }} else if (type === 'server') {{
            // ═══ 2U RACKMOUNT SERVER ═══
            if (idx === 0) {{
                // Server Chassis
                primaryMesh = new THREE.Group();
                const chassis = new THREE.Mesh(
                    new THREE.BoxGeometry(4.0, 0.7, 2.8),
                    new THREE.MeshStandardMaterial({{ color: 0x222230, metalness: 0.85, roughness: 0.25 }})
                );
                primaryMesh.add(chassis);
                // Rack ears with mounting holes
                for (let side = -1; side <= 1; side += 2) {{
                    const ear = new THREE.Mesh(
                        new THREE.BoxGeometry(0.15, 0.7, 0.06),
                        new THREE.MeshStandardMaterial({{ color: 0x333340, metalness: 0.9 }})
                    );
                    ear.position.set(side * 2.08, 0, -1.4);
                    primaryMesh.add(ear);
                }}
            }} else if (idx === 1) {{
                // Hot-Swap Drive Bays (6 bays)
                primaryMesh = new THREE.Group();
                for (let d = 0; d < 6; d++) {{
                    const bay = new THREE.Mesh(
                        new THREE.BoxGeometry(0.5, 0.18, 0.6),
                        new THREE.MeshStandardMaterial({{ color: 0x1a1a22, metalness: 0.7, roughness: 0.3 }})
                    );
                    bay.position.set(-1.5 + d * 0.55, -0.15, -1.0);
                    primaryMesh.add(bay);
                    // Drive LED
                    const dled = new THREE.Mesh(
                        new THREE.SphereGeometry(0.015, 6, 6),
                        new THREE.MeshStandardMaterial({{ color: 0x00ff44, emissive: 0x00ff44, emissiveIntensity: 0.8 }})
                    );
                    dled.position.set(-1.5 + d * 0.55, -0.04, -1.3);
                    primaryMesh.add(dled);
                }}
            }} else if (idx === 2) {{
                // Blower Fan Wall (6 fans)
                primaryMesh = new THREE.Group();
                for (let f = 0; f < 6; f++) {{
                    const shroud = new THREE.Mesh(
                        new THREE.BoxGeometry(0.45, 0.45, 0.2),
                        new THREE.MeshStandardMaterial({{ color: 0x111118 }})
                    );
                    shroud.position.set(-1.4 + f * 0.5, 0, -0.2);
                    primaryMesh.add(shroud);
                    const fan = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.18, 0.18, 0.05, 24),
                        new THREE.MeshStandardMaterial({{ color: 0x333340, metalness: 0.6 }})
                    );
                    fan.rotation.x = Math.PI / 2;
                    fan.position.set(-1.4 + f * 0.5, 0, -0.2);
                    primaryMesh.add(fan);
                }}
            }} else if (idx === 3) {{
                // Dual CPU Sockets + Heatsinks
                primaryMesh = new THREE.Group();
                for (let cpu = 0; cpu < 2; cpu++) {{
                    const socket = new THREE.Mesh(
                        new THREE.BoxGeometry(0.6, 0.05, 0.6),
                        new THREE.MeshStandardMaterial({{ color: 0x0a5c2a, roughness: 0.4 }})
                    );
                    socket.position.set(-0.8 + cpu * 1.6, 0, 0.5);
                    primaryMesh.add(socket);
                    const heatsink = new THREE.Mesh(
                        new THREE.BoxGeometry(0.55, 0.3, 0.55),
                        new THREE.MeshStandardMaterial({{ color: 0xB8BCC0, metalness: 0.92, roughness: 0.15 }})
                    );
                    heatsink.position.set(-0.8 + cpu * 1.6, 0.18, 0.5);
                    primaryMesh.add(heatsink);
                }}
                // DIMM slots (12)
                for (let dm = 0; dm < 12; dm++) {{
                    const dimm = new THREE.Mesh(
                        new THREE.BoxGeometry(0.04, 0.2, 0.55),
                        new THREE.MeshStandardMaterial({{ color: 0x0a6e2a, metalness: 0.3 }})
                    );
                    dimm.position.set(-1.6 + dm * 0.25, 0.1, -0.4);
                    primaryMesh.add(dimm);
                }}
            }} else {{
                // Redundant Hot-Swap PSUs
                primaryMesh = new THREE.Group();
                for (let ps = 0; ps < 2; ps++) {{
                    const psu = new THREE.Mesh(
                        new THREE.BoxGeometry(0.8, 0.35, 1.4),
                        new THREE.MeshStandardMaterial({{ color: 0x1a1a22, metalness: 0.8, roughness: 0.3 }})
                    );
                    psu.position.set(-0.6 + ps * 1.2, -0.1, 1.0);
                    primaryMesh.add(psu);
                    const handle = new THREE.Mesh(
                        new THREE.BoxGeometry(0.15, 0.08, 0.04),
                        new THREE.MeshStandardMaterial({{ color: ps === 0 ? 0x00cc44 : 0xcc4400, roughness: 0.5 }})
                    );
                    handle.position.set(-0.6 + ps * 1.2, 0.1, 1.7);
                    primaryMesh.add(handle);
                }}
            }}

        }} else if (type === 'console') {{
            // ═══ GAMING CONSOLE ═══
            if (idx === 0) {{
                // Console Housing
                primaryMesh = new THREE.Group();
                const body = new THREE.Mesh(
                    new THREE.BoxGeometry(2.8, 0.6, 2.2),
                    new THREE.MeshStandardMaterial({{ color: 0x111118, roughness: 0.35, metalness: 0.4 }})
                );
                primaryMesh.add(body);
                // Accent stripe
                const stripe = new THREE.Mesh(
                    new THREE.BoxGeometry(2.81, 0.04, 0.08),
                    new THREE.MeshStandardMaterial({{ color: 0x0066ff, emissive: 0x0044cc, emissiveIntensity: 0.6 }})
                );
                stripe.position.set(0, 0, -1.05);
                primaryMesh.add(stripe);
                // Disc drive slot
                const slot = new THREE.Mesh(
                    new THREE.BoxGeometry(1.2, 0.015, 0.01),
                    new THREE.MeshStandardMaterial({{ color: 0x333340 }})
                );
                slot.position.set(-0.5, 0, -1.1);
                primaryMesh.add(slot);
            }} else if (idx === 1) {{
                // Ventilation Cooling Ribs
                primaryMesh = new THREE.Group();
                for (let v = 0; v < 16; v++) {{
                    const rib = new THREE.Mesh(
                        new THREE.BoxGeometry(0.03, 0.5, 2.0),
                        new THREE.MeshStandardMaterial({{ color: 0x0a0a12 }})
                    );
                    rib.position.set(-1.3 + v * 0.16, 0, 0);
                    primaryMesh.add(rib);
                }}
            }} else if (idx === 2) {{
                // APU Processor & Vapor Chamber
                primaryMesh = new THREE.Group();
                const apu = new THREE.Mesh(
                    new THREE.BoxGeometry(0.5, 0.06, 0.5),
                    new THREE.MeshStandardMaterial({{ color: 0x111118, metalness: 0.8 }})
                );
                primaryMesh.add(apu);
                const vapor = new THREE.Mesh(
                    new THREE.BoxGeometry(1.4, 0.08, 1.2),
                    new THREE.MeshStandardMaterial({{ color: 0xB87333, metalness: 0.95, roughness: 0.1 }})
                );
                vapor.position.y = 0.07;
                primaryMesh.add(vapor);
            }} else if (idx === 3) {{
                // Blu-Ray Drive Assembly
                primaryMesh = new THREE.Group();
                const drive = new THREE.Mesh(
                    new THREE.BoxGeometry(1.6, 0.2, 1.4),
                    new THREE.MeshStandardMaterial({{ color: 0x2a2a32, metalness: 0.5, roughness: 0.4 }})
                );
                primaryMesh.add(drive);
                const lens = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.05, 0.05, 0.04, 16),
                    new THREE.MeshStandardMaterial({{ color: 0x4444cc, emissive: 0x2222aa, emissiveIntensity: 0.4, metalness: 0.8 }})
                );
                lens.position.set(0, 0.12, 0);
                primaryMesh.add(lens);
            }} else {{
                // Internal PSU & Wi-Fi Module
                primaryMesh = new THREE.Group();
                const psu = new THREE.Mesh(
                    new THREE.BoxGeometry(1.0, 0.3, 0.8),
                    new THREE.MeshStandardMaterial({{ color: 0x1a1a22, metalness: 0.7 }})
                );
                psu.position.set(0.7, 0, 0.5);
                primaryMesh.add(psu);
                const wifi = new THREE.Mesh(
                    new THREE.BoxGeometry(0.3, 0.04, 0.2),
                    new THREE.MeshStandardMaterial({{ color: 0x0a5c2a, roughness: 0.3 }})
                );
                wifi.position.set(-0.8, 0, 0.6);
                primaryMesh.add(wifi);
            }}

        }} else if (type === 'large_appliance') {{
            // ═══ LARGE APPLIANCE (Refrigerator/Washing Machine) ═══
            if (idx === 0) {{
                // Heavy Steel Cabinet
                primaryMesh = new THREE.Mesh(
                    new THREE.BoxGeometry(2.2, 3.6, 2.4),
                    new THREE.MeshStandardMaterial({{ color: 0xd8d8dc, metalness: 0.6, roughness: 0.3 }})
                );
            }} else if (idx === 1) {{
                // Compressor Motor Pump
                primaryMesh = new THREE.Group();
                const compressor = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.35, 0.35, 0.5, 24),
                    new THREE.MeshStandardMaterial({{ color: 0x222230, metalness: 0.85, roughness: 0.25 }})
                );
                compressor.position.set(0, -1.5, 0.8);
                primaryMesh.add(compressor);
                const mountPlate = new THREE.Mesh(
                    new THREE.BoxGeometry(0.8, 0.04, 0.8),
                    new THREE.MeshStandardMaterial({{ color: 0x333340, metalness: 0.8 }})
                );
                mountPlate.position.set(0, -1.75, 0.8);
                primaryMesh.add(mountPlate);
            }} else if (idx === 2) {{
                // Copper Condenser Coils
                primaryMesh = new THREE.Group();
                for (let coil = 0; coil < 12; coil++) {{
                    const tube = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.02, 0.02, 2.0, 8),
                        new THREE.MeshStandardMaterial({{ color: 0xB87333, metalness: 0.95, roughness: 0.1 }})
                    );
                    tube.rotation.x = Math.PI / 2;
                    tube.position.set(0, -1.4 + coil * 0.12, -1.15);
                    primaryMesh.add(tube);
                }}
            }} else if (idx === 3) {{
                // Insulation Foam Layer
                primaryMesh = new THREE.Mesh(
                    new THREE.BoxGeometry(2.0, 3.4, 2.2),
                    new THREE.MeshStandardMaterial({{ color: 0xf0e8d0, roughness: 0.9, metalness: 0.0, transparent: true, opacity: 0.5 }})
                );
            }} else {{
                // Control Module & Thermostat
                primaryMesh = new THREE.Group();
                const module = new THREE.Mesh(
                    new THREE.BoxGeometry(1.0, 0.3, 0.6),
                    new THREE.MeshStandardMaterial({{ color: 0x0a5c2a, roughness: 0.35 }})
                );
                module.position.set(0, 1.6, -1.0);
                primaryMesh.add(module);
                const display = new THREE.Mesh(
                    new THREE.BoxGeometry(0.6, 0.2, 0.02),
                    new THREE.MeshStandardMaterial({{ color: 0x081020, emissive: 0x1144aa, emissiveIntensity: 0.4 }})
                );
                display.position.set(0, 1.8, -1.2);
                primaryMesh.add(display);
            }}

        }} else if (type === 'small_appliance') {{
            // ═══ SMALL APPLIANCE (Microwave/Mixer/Light) ═══
            if (idx === 0) {{
                // Metal Enclosure
                primaryMesh = new THREE.Group();
                const body = new THREE.Mesh(
                    new THREE.BoxGeometry(2.2, 1.4, 1.6),
                    new THREE.MeshStandardMaterial({{ color: 0xc0c0c8, metalness: 0.65, roughness: 0.3 }})
                );
                primaryMesh.add(body);
                // Door / Front face
                const door = new THREE.Mesh(
                    new THREE.BoxGeometry(1.4, 1.1, 0.04),
                    new THREE.MeshStandardMaterial({{ color: 0x222230, roughness: 0.2, metalness: 0.4 }})
                );
                door.position.set(-0.2, 0, -0.82);
                primaryMesh.add(door);
                // Glass window
                const glass = new THREE.Mesh(
                    new THREE.BoxGeometry(1.0, 0.8, 0.02),
                    new THREE.MeshStandardMaterial({{ color: 0x1a2a3a, transparent: true, opacity: 0.5, roughness: 0.05 }})
                );
                glass.position.set(-0.2, 0.05, -0.84);
                primaryMesh.add(glass);
            }} else if (idx === 1) {{
                // Control Knobs & Timer Dial
                primaryMesh = new THREE.Group();
                for (let k = 0; k < 3; k++) {{
                    const knob = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.08, 0.08, 0.06, 16),
                        new THREE.MeshStandardMaterial({{ color: 0xdddddd, metalness: 0.5, roughness: 0.4 }})
                    );
                    knob.rotation.x = Math.PI / 2;
                    knob.position.set(0.85, 0.3 - k * 0.35, -0.82);
                    primaryMesh.add(knob);
                    // Indicator line
                    const line = new THREE.Mesh(
                        new THREE.BoxGeometry(0.01, 0.06, 0.01),
                        new THREE.MeshStandardMaterial({{ color: 0xcc2222 }})
                    );
                    line.position.set(0.85, 0.36 - k * 0.35, -0.85);
                    primaryMesh.add(line);
                }}
            }} else if (idx === 2) {{
                // Magnetron / Motor Coil
                primaryMesh = new THREE.Group();
                const magnetron = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.25, 0.25, 0.5, 16),
                    new THREE.MeshStandardMaterial({{ color: 0x555560, metalness: 0.8, roughness: 0.25 }})
                );
                magnetron.position.set(0.5, 0.3, 0.3);
                primaryMesh.add(magnetron);
                const coilWire = new THREE.Mesh(
                    new THREE.TorusGeometry(0.15, 0.02, 8, 24),
                    new THREE.MeshStandardMaterial({{ color: 0xB87333, metalness: 0.95, roughness: 0.1 }})
                );
                coilWire.position.set(0.5, 0.3, 0.05);
                primaryMesh.add(coilWire);
            }} else if (idx === 3) {{
                // Transformer & Capacitor
                primaryMesh = new THREE.Group();
                const transformer = new THREE.Mesh(
                    new THREE.BoxGeometry(0.4, 0.35, 0.35),
                    new THREE.MeshStandardMaterial({{ color: 0x222230, metalness: 0.5 }})
                );
                transformer.position.set(-0.5, -0.3, 0.3);
                primaryMesh.add(transformer);
                const cap = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.1, 0.1, 0.35, 16),
                    new THREE.MeshStandardMaterial({{ color: 0x1a1a28, metalness: 0.6 }})
                );
                cap.position.set(-0.1, -0.3, 0.3);
                primaryMesh.add(cap);
            }} else {{
                // 3-Pin Power Cord
                primaryMesh = new THREE.Group();
                const cord = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.06, 0.06, 1.8, 12),
                    new THREE.MeshStandardMaterial({{ color: 0x1a1a22, roughness: 0.6 }})
                );
                cord.rotation.z = Math.PI / 2;
                cord.position.set(0, -0.5, 0.7);
                primaryMesh.add(cord);
                // Plug prongs
                for (let pr = 0; pr < 3; pr++) {{
                    const prong = new THREE.Mesh(
                        new THREE.BoxGeometry(0.02, 0.15, 0.04),
                        new THREE.MeshStandardMaterial({{ color: 0xCCCCCC, metalness: 0.9, roughness: 0.1 }})
                    );
                    prong.position.set(0.95, -0.45 + pr * 0.12, 0.7);
                    primaryMesh.add(prong);
                }}
            }}

        }} else {{
            // ═══ SMARTPHONE / TABLET / REALME REFERENCE ARCHITECTURE ═══
            const phoneWidth = 2.15;
            const phoneHeight = 4.45;
            const phoneThickness = 0.085;

            if (idx === 0) {{
                // ── 1. REALISTIC REAR COVER (Sunrise Beige Vegan Leather + Stitched Center Stripe) ──
                primaryMesh = new THREE.Group();

                // Base Leather Backplate
                const leatherTex = createLeatherTexture();
                const backGeo = new THREE.BoxGeometry(phoneWidth, phoneHeight, 0.035);
                const backMat = new THREE.MeshStandardMaterial({{
                    map: leatherTex,
                    roughness: 0.88,
                    metalness: 0.04
                }});
                const backPlate = new THREE.Mesh(backGeo, backMat);
                primaryMesh.add(backPlate);

                // ── Camera Module Assembly (Raised Circular Halo + Matte Disc + Glass + Triple Lenses) ──
                const camCenterY = 1.05;
                const camBaseZ = 0.025;

                // Step A: Fluted Golden Outer Ring (Halo with metallic luster)
                const haloOuterGeo = new THREE.CylinderGeometry(0.68, 0.70, 0.05, 64);
                const haloOuterMat = new THREE.MeshStandardMaterial({{
                    color: 0xD4AF37,
                    metalness: 0.95,
                    roughness: 0.15
                }});
                const haloOuter = new THREE.Mesh(haloOuterGeo, haloOuterMat);
                haloOuter.rotation.x = Math.PI / 2;
                haloOuter.position.set(0, camCenterY, camBaseZ + 0.025);
                primaryMesh.add(haloOuter);

                // Step B: Deep Obsidian Black Camera Disc
                const discGeo = new THREE.CylinderGeometry(0.64, 0.64, 0.055, 64);
                const discMat = new THREE.MeshStandardMaterial({{
                    color: 0x050505,
                    roughness: 0.25,
                    metalness: 0.85
                }});
                const disc = new THREE.Mesh(discGeo, discMat);
                disc.rotation.x = Math.PI / 2;
                disc.position.set(0, camCenterY, camBaseZ + 0.03);
                primaryMesh.add(disc);

                // Step C: Center Primary SuperZoom Lens (200MP / 100MP OIS Camera)
                // Gold Inner Bezel
                const mainLensRing = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.24, 0.24, 0.065, 48),
                    new THREE.MeshStandardMaterial({{ color: 0xD4AF37, metalness: 0.98, roughness: 0.1 }})
                );
                mainLensRing.rotation.x = Math.PI / 2;
                mainLensRing.position.set(0, camCenterY, camBaseZ + 0.035);
                primaryMesh.add(mainLensRing);

                // Convex Glass Lens Element
                const mainLensGlass = new THREE.Mesh(
                    new THREE.SphereGeometry(0.20, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.4),
                    new THREE.MeshPhysicalMaterial({{
                        color: 0x0a192f,
                        transmission: 0.85,
                        opacity: 0.95,
                        transparent: true,
                        roughness: 0.05,
                        metalness: 0.1,
                        ior: 1.62
                    }})
                );
                mainLensGlass.position.set(0, camCenterY, camBaseZ + 0.068);
                primaryMesh.add(mainLensGlass);

                // Deep Camera Sensor Aperture Pupil
                const mainPupil = new THREE.Mesh(
                    new THREE.CircleGeometry(0.12, 32),
                    new THREE.MeshBasicMaterial({{ color: 0x000814 }})
                );
                mainPupil.position.set(0, camCenterY, camBaseZ + 0.063);
                primaryMesh.add(mainPupil);

                // Step D: Left Ultra-Wide Secondary Lens
                const leftLens = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.12, 0.12, 0.062, 32),
                    new THREE.MeshStandardMaterial({{ color: 0x111111, metalness: 0.9, roughness: 0.1 }})
                );
                leftLens.rotation.x = Math.PI / 2;
                leftLens.position.set(-0.35, camCenterY - 0.20, camBaseZ + 0.035);
                primaryMesh.add(leftLens);

                const leftPupil = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.08, 0.08, 0.066, 24),
                    new THREE.MeshStandardMaterial({{ color: 0x051b2c, roughness: 0.1, metalness: 0.5 }})
                );
                leftPupil.rotation.x = Math.PI / 2;
                leftPupil.position.set(-0.35, camCenterY - 0.20, camBaseZ + 0.036);
                primaryMesh.add(leftPupil);

                // Step E: Right Macro / Depth Lens
                const rightLens = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.12, 0.12, 0.062, 32),
                    new THREE.MeshStandardMaterial({{ color: 0x111111, metalness: 0.9, roughness: 0.1 }})
                );
                rightLens.rotation.x = Math.PI / 2;
                rightLens.position.set(0.35, camCenterY - 0.20, camBaseZ + 0.035);
                primaryMesh.add(rightLens);

                const rightPupil = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.08, 0.08, 0.066, 24),
                    new THREE.MeshStandardMaterial({{ color: 0x051b2c, roughness: 0.1, metalness: 0.5 }})
                );
                rightPupil.rotation.x = Math.PI / 2;
                rightPupil.position.set(0.35, camCenterY - 0.20, camBaseZ + 0.036);
                primaryMesh.add(rightPupil);

                // Step F: Dual-LED TrueTone Flash & Ambient Light Sensor
                const ledFlash = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.065, 0.065, 0.062, 24),
                    new THREE.MeshStandardMaterial({{ color: 0xFFF2B2, emissive: 0x887733, roughness: 0.2 }})
                );
                ledFlash.rotation.x = Math.PI / 2;
                ledFlash.position.set(0, camCenterY + 0.38, camBaseZ + 0.035);
                primaryMesh.add(ledFlash);

                // "200MP OIS" Camera Branding Ring Rim
                const labelRim = new THREE.Mesh(
                    new THREE.TorusGeometry(0.52, 0.008, 16, 64),
                    new THREE.MeshStandardMaterial({{ color: 0xAAAAAA, metalness: 0.8 }})
                );
                labelRim.position.set(0, camCenterY, camBaseZ + 0.06);
                primaryMesh.add(labelRim);

            }} else if (idx === 1) {{
                // ── 2. NFC ANTENNA LOOP & GRAPHITE HEAT SPREADER ──
                primaryMesh = new THREE.Group();
                const sheet = new THREE.Mesh(
                    new THREE.BoxGeometry(phoneWidth * 0.88, phoneHeight * 0.88, 0.015),
                    new THREE.MeshStandardMaterial({{ color: 0x1E1E22, roughness: 0.92, metalness: 0.1 }})
                );
                primaryMesh.add(sheet);

                // Copper NFC coil ring
                const nfcCoil = new THREE.Mesh(
                    new THREE.TorusGeometry(0.48, 0.02, 16, 48),
                    new THREE.MeshStandardMaterial({{ color: 0xD35400, metalness: 0.95, roughness: 0.2 }})
                );
                nfcCoil.position.set(0, 0.3, 0.01);
                primaryMesh.add(nfcCoil);

            }} else if (idx === 2) {{
                // ── 3. INTERNAL MAGNESIUM SHIELD PLATE & 16 FASTENING SCREWS ──
                primaryMesh = new THREE.Group();
                const shieldPlate = new THREE.Mesh(
                    new THREE.BoxGeometry(phoneWidth * 0.95, phoneHeight * 0.95, 0.02),
                    new THREE.MeshStandardMaterial({{ color: 0x3E4444, metalness: 0.85, roughness: 0.3 }})
                );
                primaryMesh.add(shieldPlate);

                // Precision micro-screws along perimeter
                const screwGeo = new THREE.CylinderGeometry(0.028, 0.028, 0.03, 16);
                const screwMat = new THREE.MeshStandardMaterial({{ color: 0xC0C0C0, metalness: 0.98, roughness: 0.1 }});
                const screwPositions = [
                    [-0.9, 2.0], [0.9, 2.0], [-0.9, -2.0], [0.9, -2.0],
                    [-0.9, 0.8], [0.9, 0.8], [-0.9, -0.8], [0.9, -0.8],
                    [-0.4, 1.8], [0.4, 1.8], [-0.4, -1.8], [0.4, -1.8],
                    [-0.9, 0.0], [0.9, 0.0], [0.0, 0.6], [0.0, -0.3]
                ];
                screwPositions.forEach(p => {{
                    const sc = new THREE.Mesh(screwGeo, screwMat);
                    sc.rotation.x = Math.PI / 2;
                    sc.position.set(p[0], p[1], 0.015);
                    primaryMesh.add(sc);
                }});

            }} else if (idx === 3) {{
                // ── 4. MULTI-LAYER FR4 LOGIC BOARD — HYPER-DETAILED PHONE PCB ──
                primaryMesh = new THREE.Group();

                // PCB substrate with copper trace texture
                const pcbMat = new THREE.MeshStandardMaterial({{ color: 0x0E5A33, roughness: 0.35, metalness: 0.3 }});
                try {{ pcbMat.map = createPCBTexture(); }} catch(e) {{}}
                const pcb = new THREE.Mesh(
                    new THREE.BoxGeometry(phoneWidth * 0.92, phoneHeight * 0.44, 0.03),
                    pcbMat
                );
                primaryMesh.add(pcb);

                // ── Main Application Processor (SoC) — Large BGA with IHS ──
                const socBase = new THREE.Mesh(
                    new THREE.BoxGeometry(0.55, 0.5, 0.025),
                    new THREE.MeshStandardMaterial({{ color: 0xDCDDE1, metalness: 0.92, roughness: 0.15 }})
                );
                socBase.position.set(-0.25, 0.15, 0.025);
                primaryMesh.add(socBase);
                // SoC die marking
                const socDie = new THREE.Mesh(
                    new THREE.BoxGeometry(0.28, 0.25, 0.008),
                    new THREE.MeshStandardMaterial({{ color: 0x0a0a18, metalness: 0.7 }})
                );
                socDie.position.set(-0.25, 0.15, 0.04);
                primaryMesh.add(socDie);

                // ── NAND Flash Storage Chip ──
                const nand = new THREE.Mesh(
                    new THREE.BoxGeometry(0.4, 0.35, 0.02),
                    new THREE.MeshStandardMaterial({{ color: 0xC8CED0, metalness: 0.88, roughness: 0.18 }})
                );
                nand.position.set(0.35, 0.2, 0.025);
                primaryMesh.add(nand);
                // NAND label marking
                const nandLabel = new THREE.Mesh(
                    new THREE.BoxGeometry(0.25, 0.08, 0.003),
                    new THREE.MeshStandardMaterial({{ color: 0x222228 }})
                );
                nandLabel.position.set(0.35, 0.2, 0.037);
                primaryMesh.add(nandLabel);

                // ── LPDDR5 RAM Module ──
                const ram = new THREE.Mesh(
                    new THREE.BoxGeometry(0.35, 0.3, 0.018),
                    new THREE.MeshStandardMaterial({{ color: 0x111118, metalness: 0.85, roughness: 0.2 }})
                );
                ram.position.set(-0.25, -0.25, -0.022);
                primaryMesh.add(ram);

                // ── Power Management IC (PMIC) ──
                const pmic = new THREE.Mesh(
                    new THREE.BoxGeometry(0.22, 0.18, 0.015),
                    new THREE.MeshStandardMaterial({{ color: 0x1a1a22, metalness: 0.8 }})
                );
                pmic.position.set(0.5, -0.15, 0.022);
                primaryMesh.add(pmic);

                // ── RF Transceiver (5G/LTE Modem) ──
                const rfChip = new THREE.Mesh(
                    new THREE.BoxGeometry(0.2, 0.15, 0.015),
                    new THREE.MeshStandardMaterial({{ color: 0x2a2a35, metalness: 0.75 }})
                );
                rfChip.position.set(-0.6, -0.1, 0.022);
                primaryMesh.add(rfChip);

                // ── Audio Codec IC ──
                const audioIC = new THREE.Mesh(
                    new THREE.BoxGeometry(0.14, 0.12, 0.012),
                    new THREE.MeshStandardMaterial({{ color: 0x0a0a14, metalness: 0.7 }})
                );
                audioIC.position.set(0.6, 0.35, 0.022);
                primaryMesh.add(audioIC);

                // ── Wi-Fi / Bluetooth Module ──
                const wifiBT = new THREE.Mesh(
                    new THREE.BoxGeometry(0.18, 0.14, 0.012),
                    new THREE.MeshStandardMaterial({{ color: 0x888890, metalness: 0.85, roughness: 0.15 }})
                );
                wifiBT.position.set(0.55, -0.35, 0.022);
                primaryMesh.add(wifiBT);

                // ── SMD Capacitors & Resistors (30+ tiny components) ──
                const smdDarkMat = new THREE.MeshStandardMaterial({{ color: 0x1a1a22, metalness: 0.6 }});
                const smdLightMat = new THREE.MeshStandardMaterial({{ color: 0x888890, metalness: 0.7 }});
                for (let s = 0; s < 30; s++) {{
                    const sx = -0.75 + (s % 10) * 0.16;
                    const sy = -0.35 + Math.floor(s / 10) * 0.22;
                    if (Math.abs(sx + 0.25) < 0.3 && Math.abs(sy - 0.15) < 0.28) continue;
                    const smd = new THREE.Mesh(
                        new THREE.BoxGeometry(0.04 + Math.random() * 0.03, 0.02, 0.015),
                        s % 3 === 0 ? smdLightMat : smdDarkMat
                    );
                    smd.position.set(sx, sy, 0.022);
                    primaryMesh.add(smd);
                }}

                // ── Gold FPC Ribbon Connectors (3 headers) ──
                const fpcMat = new THREE.MeshStandardMaterial({{ color: 0xD4AF37, metalness: 0.98, roughness: 0.08 }});
                for (let fc = 0; fc < 3; fc++) {{
                    const fpc = new THREE.Mesh(
                        new THREE.BoxGeometry(0.25, 0.06, 0.012),
                        fpcMat
                    );
                    fpc.position.set(-0.5 + fc * 0.45, -0.4, 0.022);
                    primaryMesh.add(fpc);
                    // Individual gold pins
                    for (let fp = 0; fp < 8; fp++) {{
                        const pin = new THREE.Mesh(
                            new THREE.BoxGeometry(0.015, 0.008, 0.008),
                            fpcMat
                        );
                        pin.position.set(-0.58 + fc * 0.45 + fp * 0.028, -0.43, 0.022);
                        primaryMesh.add(pin);
                    }}
                }}

                // ── Coaxial Antenna Connectors (2 gold micro-circles) ──
                for (let cx = 0; cx < 2; cx++) {{
                    const coax = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.03, 0.03, 0.015, 12),
                        new THREE.MeshStandardMaterial({{ color: 0xFFD700, metalness: 0.95, roughness: 0.1 }})
                    );
                    coax.rotation.x = Math.PI / 2;
                    coax.position.set(-0.7 + cx * 1.4, 0.35, 0.022);
                    primaryMesh.add(coax);
                }}

                // ── Test Pads (Gold dots for factory QC) ──
                for (let tp = 0; tp < 6; tp++) {{
                    const pad = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.015, 0.015, 0.005, 8),
                        new THREE.MeshStandardMaterial({{ color: 0xFFD700, metalness: 0.95 }})
                    );
                    pad.rotation.x = Math.PI / 2;
                    pad.position.set(-0.6 + tp * 0.24, 0.42, 0.02);
                    primaryMesh.add(pad);
                }}

                primaryMesh.position.set(0, 1.05, 0);

            }} else if (idx === 4) {{
                // ── 5. 5000MAH LI-ION BATTERY — HYPER-DETAILED POUCH CELL ──
                primaryMesh = new THREE.Group();

                // Main pouch cell body (dark blue-black wrapping)
                const cell = new THREE.Mesh(
                    new THREE.BoxGeometry(phoneWidth * 0.86, phoneHeight * 0.46, 0.065),
                    new THREE.MeshStandardMaterial({{ color: 0x0a1020, roughness: 0.5, metalness: 0.1 }})
                );
                primaryMesh.add(cell);

                // "Li-ion" white text label area
                const liLabel = new THREE.Mesh(
                    new THREE.BoxGeometry(0.5, 0.12, 0.003),
                    new THREE.MeshStandardMaterial({{ color: 0xe0e0e0, roughness: 0.8 }})
                );
                liLabel.position.set(0, 0.15, 0.034);
                primaryMesh.add(liLabel);

                // Warning triangle label (yellow)
                const warnLabel = new THREE.Mesh(
                    new THREE.BoxGeometry(0.18, 0.15, 0.003),
                    new THREE.MeshStandardMaterial({{ color: 0xFFCC00, roughness: 0.6 }})
                );
                warnLabel.position.set(-0.55, 0.3, 0.034);
                primaryMesh.add(warnLabel);

                // Voltage/Capacity spec label
                const specLabel = new THREE.Mesh(
                    new THREE.BoxGeometry(0.6, 0.08, 0.003),
                    new THREE.MeshStandardMaterial({{ color: 0xcccccc, roughness: 0.8 }})
                );
                specLabel.position.set(0, -0.05, 0.034);
                primaryMesh.add(specLabel);

                // QR code area
                const qr = new THREE.Mesh(
                    new THREE.BoxGeometry(0.15, 0.15, 0.003),
                    new THREE.MeshStandardMaterial({{ color: 0xffffff, roughness: 0.9 }})
                );
                qr.position.set(0.55, -0.25, 0.034);
                primaryMesh.add(qr);
                // QR pattern dots
                for (let qx = 0; qx < 5; qx++) {{
                    for (let qy = 0; qy < 5; qy++) {{
                        if (Math.random() > 0.4) {{
                            const dot = new THREE.Mesh(
                                new THREE.BoxGeometry(0.02, 0.02, 0.002),
                                new THREE.MeshStandardMaterial({{ color: 0x111111 }})
                            );
                            dot.position.set(0.49 + qx * 0.028, -0.31 + qy * 0.028, 0.036);
                            primaryMesh.add(dot);
                        }}
                    }}
                }}

                // Battery connector (gold tabs + FPC)
                const battConn = new THREE.Mesh(
                    new THREE.BoxGeometry(0.3, 0.06, 0.02),
                    new THREE.MeshStandardMaterial({{ color: 0x222228, metalness: 0.5 }})
                );
                battConn.position.set(0, phoneHeight * 0.22, 0.025);
                primaryMesh.add(battConn);
                // Gold contact pads
                for (let bp = 0; bp < 4; bp++) {{
                    const bpin = new THREE.Mesh(
                        new THREE.BoxGeometry(0.04, 0.015, 0.015),
                        new THREE.MeshStandardMaterial({{ color: 0xFFD700, metalness: 0.98, roughness: 0.05 }})
                    );
                    bpin.position.set(-0.08 + bp * 0.055, phoneHeight * 0.22, 0.035);
                    primaryMesh.add(bpin);
                }}

                // Thermistor (tiny component on connector)
                const therm = new THREE.Mesh(
                    new THREE.BoxGeometry(0.04, 0.03, 0.01),
                    new THREE.MeshStandardMaterial({{ color: 0x444450, metalness: 0.6 }})
                );
                therm.position.set(0.18, phoneHeight * 0.21, 0.03);
                primaryMesh.add(therm);

                // Stretch release pull tabs (neon orange)
                const tabGeo = new THREE.BoxGeometry(0.25, 0.08, 0.01);
                const tabMat = new THREE.MeshStandardMaterial({{ color: 0xE67E22, roughness: 0.4 }});
                const tabA = new THREE.Mesh(tabGeo, tabMat);
                tabA.position.set(-0.35, -0.24, 0.035);
                const tabB = new THREE.Mesh(tabGeo, tabMat);
                tabB.position.set(0.35, -0.24, 0.035);
                primaryMesh.add(tabA);
                primaryMesh.add(tabB);

                // Manufacturer stamp / CE marking
                const ceStamp = new THREE.Mesh(
                    new THREE.BoxGeometry(0.1, 0.08, 0.002),
                    new THREE.MeshStandardMaterial({{ color: 0x888888, roughness: 0.8 }})
                );
                ceStamp.position.set(-0.55, -0.2, 0.034);
                primaryMesh.add(ceStamp);

                primaryMesh.position.set(0, -0.70, 0);

            }} else if (idx === 5) {{
                // ── 6. MIDFRAME + SPEAKER + VIBRATION MOTOR + USB-C + SIM TRAY + ANTENNA ──
                primaryMesh = new THREE.Group();

                // ─── A. CNC Aluminum Unibody Bezel Frame ───
                const frameMat = new THREE.MeshStandardMaterial({{
                    color: 0xD4AF37,
                    metalness: 0.92,
                    roughness: 0.20
                }});
                const frame = new THREE.Mesh(
                    new THREE.BoxGeometry(phoneWidth * 0.99, phoneHeight * 0.99, 0.06),
                    frameMat
                );
                primaryMesh.add(frame);

                // ─── B. Right Side Power Button (Textured) ───
                const pwrBtn = new THREE.Mesh(
                    new THREE.BoxGeometry(0.035, 0.35, 0.05),
                    new THREE.MeshStandardMaterial({{ color: 0xCCAA22, metalness: 0.95, roughness: 0.12 }})
                );
                pwrBtn.position.set(phoneWidth * 0.50, 0.4, 0);
                primaryMesh.add(pwrBtn);

                // ─── C. Right Side Volume Up + Down (Two Separate Buttons) ───
                const volUp = new THREE.Mesh(
                    new THREE.BoxGeometry(0.035, 0.28, 0.05),
                    new THREE.MeshStandardMaterial({{ color: 0xCCAA22, metalness: 0.95, roughness: 0.12 }})
                );
                volUp.position.set(phoneWidth * 0.50, 1.2, 0);
                primaryMesh.add(volUp);
                const volDn = new THREE.Mesh(
                    new THREE.BoxGeometry(0.035, 0.28, 0.05),
                    new THREE.MeshStandardMaterial({{ color: 0xCCAA22, metalness: 0.95, roughness: 0.12 }})
                );
                volDn.position.set(phoneWidth * 0.50, 0.85, 0);
                primaryMesh.add(volDn);

                // ─── D. LEFT SIDE SIM TRAY with Ejector Hole ───
                const simTray = new THREE.Mesh(
                    new THREE.BoxGeometry(0.04, 0.55, 0.035),
                    new THREE.MeshStandardMaterial({{ color: 0xBBAA33, metalness: 0.9, roughness: 0.15 }})
                );
                simTray.position.set(-phoneWidth * 0.50, 0.6, 0);
                primaryMesh.add(simTray);
                // Ejector pin hole
                const ejHole = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.012, 0.012, 0.05, 8),
                    new THREE.MeshStandardMaterial({{ color: 0x050505 }})
                );
                ejHole.rotation.z = Math.PI / 2;
                ejHole.position.set(-phoneWidth * 0.50, 0.82, 0);
                primaryMesh.add(ejHole);

                // ─── E. BOTTOM USB TYPE-C PORT (Realistic with 24-pin Gold Contacts) ───
                const usbShell = new THREE.Mesh(
                    new THREE.BoxGeometry(0.36, 0.06, 0.04),
                    new THREE.MeshStandardMaterial({{ color: 0x222228, metalness: 0.7, roughness: 0.3 }})
                );
                usbShell.position.set(0, -phoneHeight * 0.50, 0);
                primaryMesh.add(usbShell);
                // 24 gold pins inside USB-C
                for (let pin = 0; pin < 12; pin++) {{
                    const p = new THREE.Mesh(
                        new THREE.BoxGeometry(0.012, 0.008, 0.025),
                        new THREE.MeshStandardMaterial({{ color: 0xFFD700, metalness: 0.98, roughness: 0.05 }})
                    );
                    p.position.set(-0.13 + pin * 0.024, -phoneHeight * 0.50, 0.005);
                    primaryMesh.add(p);
                }}

                // ─── F. BOTTOM SPEAKER GRILLE (Left side, visible cone) ───
                for (let g = 0; g < 6; g++) {{
                    const gr = new THREE.Mesh(
                        new THREE.BoxGeometry(0.04, 0.02, 0.025),
                        new THREE.MeshStandardMaterial({{ color: 0x0a0a0e }})
                    );
                    gr.position.set(0.35 + g * 0.075, -phoneHeight * 0.50, 0);
                    primaryMesh.add(gr);
                }}
                // Speaker driver cone (visible behind grille)
                const spkCone = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.15, 0.1, 0.03, 16),
                    new THREE.MeshStandardMaterial({{ color: 0x333338, metalness: 0.6 }})
                );
                spkCone.rotation.x = Math.PI / 2;
                spkCone.position.set(0.55, -phoneHeight * 0.48, -0.02);
                primaryMesh.add(spkCone);

                // ─── G. TOP EARPIECE SPEAKER ───
                const earpiece = new THREE.Mesh(
                    new THREE.BoxGeometry(0.5, 0.025, 0.025),
                    new THREE.MeshStandardMaterial({{ color: 0x0a0a0e }})
                );
                earpiece.position.set(0, phoneHeight * 0.465, 0);
                primaryMesh.add(earpiece);
                // Earpiece mesh grill
                for (let eg = 0; eg < 8; eg++) {{
                    const egr = new THREE.Mesh(
                        new THREE.BoxGeometry(0.04, 0.006, 0.015),
                        new THREE.MeshStandardMaterial({{ color: 0x050508 }})
                    );
                    egr.position.set(-0.18 + eg * 0.05, phoneHeight * 0.465, 0.01);
                    primaryMesh.add(egr);
                }}

                // ─── H. VIBRATION MOTOR (Linear Haptic Motor with Off-Center Weight) ───
                const vibrBody = new THREE.Mesh(
                    new THREE.BoxGeometry(0.35, 0.18, 0.035),
                    new THREE.MeshStandardMaterial({{ color: 0x444450, metalness: 0.85, roughness: 0.2 }})
                );
                vibrBody.position.set(-0.5, -phoneHeight * 0.42, 0);
                primaryMesh.add(vibrBody);
                // Eccentric rotating mass
                const vibrWeight = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.04, 0.04, 0.03, 12),
                    new THREE.MeshStandardMaterial({{ color: 0xD4AF37, metalness: 0.95 }})
                );
                vibrWeight.rotation.x = Math.PI / 2;
                vibrWeight.position.set(-0.42, -phoneHeight * 0.42, 0.02);
                primaryMesh.add(vibrWeight);

                // ─── I. ANTENNA MODULES (3 Flex Antenna Strips) ───
                const antMat = new THREE.MeshStandardMaterial({{ color: 0x2a5e3a, roughness: 0.4 }});
                // Top 5G antenna
                const ant1 = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.08, 0.01), antMat);
                ant1.position.set(0, phoneHeight * 0.44, -0.025);
                primaryMesh.add(ant1);
                // Bottom WiFi antenna
                const ant2 = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.08, 0.01), antMat);
                ant2.position.set(0, -phoneHeight * 0.44, -0.025);
                primaryMesh.add(ant2);
                // Side Bluetooth antenna strip
                const ant3 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.6, 0.01), antMat);
                ant3.position.set(-phoneWidth * 0.46, -0.3, -0.025);
                primaryMesh.add(ant3);

                // ─── J. FLEX RIBBON CABLES (Display + Battery + Charging Board) ───
                const flexMat = new THREE.MeshStandardMaterial({{ color: 0xCC8833, metalness: 0.5, roughness: 0.4 }});
                // Display FPC flex
                const flex1 = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.5, 0.005), flexMat);
                flex1.position.set(0.3, 0.5, 0.025);
                primaryMesh.add(flex1);
                // Battery flex connector
                const flex2 = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.3, 0.005), flexMat);
                flex2.position.set(-0.4, -0.2, 0.025);
                primaryMesh.add(flex2);
                // Charging board flex
                const flex3 = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.08, 0.005), flexMat);
                flex3.position.set(0, -phoneHeight * 0.38, 0.025);
                primaryMesh.add(flex3);

                // ─── K. BOTTOM MICROPHONE HOLE ───
                const mic = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.015, 0.015, 0.05, 8),
                    new THREE.MeshStandardMaterial({{ color: 0x050505 }})
                );
                mic.rotation.x = Math.PI / 2;
                mic.position.set(-0.4, -phoneHeight * 0.50, 0);
                primaryMesh.add(mic);

            }} else {{
                // ── 7. 120HZ CURVED AMOLED DISPLAY & CORNING GORILLA GLASS ──
                primaryMesh = new THREE.Group();
                const screenTex = createScreenTexture();

                // Ultra-thin curved glass front
                const dispGeo = new THREE.BoxGeometry(phoneWidth * 0.96, phoneHeight * 0.97, 0.025);
                const dispMat = new THREE.MeshStandardMaterial({{
                    map: screenTex,
                    roughness: 0.05,
                    metalness: 0.88
                }});
                const disp = new THREE.Mesh(dispGeo, dispMat);
                primaryMesh.add(disp);

                // Glass coating sheen reflection
                const glassCoating = new THREE.Mesh(
                    new THREE.BoxGeometry(phoneWidth * 0.965, phoneHeight * 0.975, 0.005),
                    new THREE.MeshPhysicalMaterial({{
                        color: 0xffffff,
                        transmission: 0.90,
                        opacity: 0.3,
                        transparent: true,
                        roughness: 0.02,
                        ior: 1.52
                    }})
                );
                glassCoating.position.set(0, 0, 0.015);
                primaryMesh.add(glassCoating);
            }}
        }}

        if (primaryMesh) {{
            layerGroup.add(primaryMesh);
            primaryMesh.userData = {{
                ...comp,
                assembledZ: assembledZ,
                explodedZ: explodedZ,
                assembledX: 0,
                explodedX: explodedX,
                assembledY: 0,
                explodedY: explodedY,
                group: layerGroup
            }};
            meshLayers.push(primaryMesh);

            // Apply hazard glow wireframe on dangerous components
            if (comp.hazardous) {{
                applyHazardGlow(primaryMesh, true);
            }}

            // Enable shadow casting on all sub-meshes
            layerGroup.traverse(function(child) {{
                if (child.isMesh) {{
                    child.castShadow = true;
                    child.receiveShadow = true;
                }}
            }});
        }}

        layerGroup.position.set(0, 0, assembledZ);
        rootGroup.add(layerGroup);
    }});
}}

/* Switch Between Procedural Model and Downloaded GLB Assets */
function switchModelMode(mode) {{
    currentMode = mode;
    document.querySelectorAll('.btn-asset').forEach(b => b.classList.remove('active'));
    const btn = document.getElementById(`btn-mode-${{mode}}`);
    if (btn) btn.classList.add('active');

    closeInspectCard();

    if (mode === 'cat') {{
        buildDeviceGeometry(SHAPE_TYPE);
        document.getElementById('legend-panel').style.display = 'block';
        showToast(`🎯 Loaded Authentic 3D Model: ${{SHAPE_TYPE.toUpperCase()}}`);
    }} else {{
        loadGLBAsset(mode);
    }}
}}

/* Asynchronous GLTF/GLB Asset Loader with CORS & Offline Fallback */
function loadGLBAsset(assetKey) {{
    const url = GLB_URLS[assetKey];
    if (!url || typeof THREE.GLTFLoader === 'undefined') {{
        showToast('⚠️ GLTF loader not ready. Displaying procedural model.');
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
                        name: child.name || `${{assetKey.toUpperCase()}} Component`,
                        material: "Solid Alloy / Silicon PBR",
                        specs: `External GLB Mesh (${{child.geometry ? child.geometry.attributes.position.count : 0}} vertices)`,
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
            console.warn('GLB asset fetch failed (CORS/offline). Reverting to procedural twin:', error);
            showToast('ℹ️ Notice: External CDN asset restricted by iframe CORS. Reverting to procedural twin.');
            buildDeviceGeometry(SHAPE_TYPE);
            document.getElementById('legend-panel').style.display = 'block';
            document.querySelectorAll('.btn-asset').forEach(b => b.classList.remove('active'));
            document.getElementById('btn-mode-cat').classList.add('active');
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
            m.material.opacity = isXRay ? 0.35 : 1.0;
        }}
    }});
}}

/* Manual Step-by-Step Disassembly Engine */
function toggleManualMode() {{
    if (currentMode !== 'cat') {{
        switchModelMode('cat');
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
    camera.position.set(0.6, 0.4, 5.8);
    camera.lookAt(0, 0, 0);
    rootGroup.rotation.set(0.08, -0.35, 0);
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

let animTime = 0;

function animate() {{
    requestAnimationFrame(animate);
    animTime += 0.016;

    if (isSpinning && !selectedMesh && !isManualMode) {{
        rootGroup.rotation.y += 0.004;
    }}

    currentExplodeRatio += (targetExplodeRatio - currentExplodeRatio) * 0.08;

    meshLayers.forEach((m, idx) => {{
        if (m.userData && m.userData.group) {{
            let targetZ, targetX = 0, targetY = 0;
            if (isManualMode && m.userData.targetManualZ !== undefined) {{
                targetZ = m.userData.targetManualZ;
                targetX = (m.userData.explodedX || 0) * 0.5;
            }} else {{
                const asZ = m.userData.assembledZ;
                const exZ = m.userData.explodedZ;
                targetZ = asZ + (exZ - asZ) * currentExplodeRatio;
                targetX = (m.userData.explodedX || 0) * currentExplodeRatio;
                targetY = (m.userData.explodedY || 0) * currentExplodeRatio;
            }}

            // Realistic floating hover when exploded
            if (currentExplodeRatio > 0.05) {{
                const floatPhase = animTime * 0.8 + idx * 1.2;
                targetY += Math.sin(floatPhase) * 0.06 * currentExplodeRatio;
                targetX += Math.cos(floatPhase * 0.7) * 0.03 * currentExplodeRatio;
            }}

            m.userData.group.position.z += (targetZ - m.userData.group.position.z) * 0.1;
            m.userData.group.position.x += (targetX - m.userData.group.position.x) * 0.1;
            m.userData.group.position.y += (targetY - m.userData.group.position.y) * 0.1;

            // Enable shadows on all layer meshes
            m.userData.group.traverse(function(child) {{
                if (child.isMesh) {{ child.castShadow = true; child.receiveShadow = true; }}
            }});
        }}

        // Breathing pulse on selected component
        if (m === selectedMesh && m.material && m.material.emissiveIntensity !== undefined) {{
            m.material.emissiveIntensity = 0.4 + Math.sin(animTime * 3.0) * 0.25;
        }}
    }});

    // Drift dust particles slowly
    scene.traverse(function(obj) {{
        if (obj.isPoints && obj.userData.isParticles) {{
            const pos = obj.geometry.attributes.position.array;
            for (let i = 0; i < pos.length; i += 3) {{
                pos[i + 1] += 0.002;
                if (pos[i + 1] > 5) pos[i + 1] = -5;
            }}
            obj.geometry.attributes.position.needsUpdate = true;
            obj.rotation.y += 0.0003;
        }}
        // Pulse hazard wireframe glow
        if (obj.isLineSegments && obj.userData.isHazardWire) {{
            obj.material.opacity = 0.3 + Math.sin(animTime * 2.5) * 0.35;
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
