"""
🎨 Three.js 3D E-Waste Viewer Generator
========================================
Generates interactive 3D HTML viewers for e-waste devices
"""

def generate_3d_viewer(device_info, height=550):
    """Generate an interactive Three.js 3D viewer HTML for a device"""
    category = device_info.get('category', 'Unknown')
    components = device_info.get('components', [])
    shape = device_info.get('3d_shape', 'phone')
    
    # Build component data for JS
    comp_data = []
    total_parts = len(components)
    for i, comp in enumerate(components):
        comp_data.append({
            "name": comp["name"],
            "material": comp["material"],
            "weight_pct": comp["weight_pct"],
            "hazardous": comp["hazardous"],
            "recyclable": comp["recyclable"],
            "value_usd": comp.get("value_usd", 0),
            "color": comp.get("color", "#888888"),
            "index": i
        })
    
    comp_json = str(comp_data).replace("'", '"').replace("True", "true").replace("False", "false")
    
    html = f"""<!DOCTYPE html>
<html><head>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#0a0a0a;font-family:'Segoe UI',sans-serif;color:#fff;overflow:hidden;}}
#canvas-container{{width:100%;height:{height}px;position:relative;}}
canvas{{display:block;}}
#info-panel{{position:absolute;top:10px;right:10px;background:rgba(0,0,0,.85);border:1px solid rgba(220,20,60,.3);border-radius:12px;padding:14px;max-width:280px;backdrop-filter:blur(10px);font-size:12px;}}
#info-panel h3{{color:#DC143C;font-size:14px;margin-bottom:8px;}}
#controls{{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:8px;}}
.ctrl-btn{{background:rgba(220,20,60,.2);border:1px solid rgba(220,20,60,.4);color:#fff;padding:8px 16px;border-radius:20px;cursor:pointer;font-size:12px;transition:all .2s;}}
.ctrl-btn:hover,.ctrl-btn.active{{background:#DC143C;}}
#legend{{position:absolute;top:10px;left:10px;background:rgba(0,0,0,.8);border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:10px;font-size:10px;max-height:{height-30}px;overflow-y:auto;}}
.legend-item{{display:flex;align-items:center;gap:6px;margin:3px 0;cursor:pointer;padding:3px 6px;border-radius:4px;transition:background .2s;}}
.legend-item:hover{{background:rgba(255,255,255,.1);}}
.legend-dot{{width:10px;height:10px;border-radius:50%;flex-shrink:0;}}
.haz-badge{{color:#FF5252;font-weight:bold;font-size:9px;}}
#title-bar{{position:absolute;top:10px;left:50%;transform:translateX(-50%);background:rgba(220,20,60,.15);border:1px solid rgba(220,20,60,.3);border-radius:20px;padding:6px 20px;font-size:13px;letter-spacing:1px;white-space:nowrap;}}
#loading{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:16px;color:#DC143C;}}
</style>
</head><body>
<div id="canvas-container">
    <div id="loading">⏳ Loading 3D Model...</div>
    <div id="title-bar">🔬 {category} — 3D Component Explorer</div>
    <div id="legend"></div>
    <div id="info-panel" style="display:none;">
        <h3 id="comp-name">Select a component</h3>
        <div id="comp-details"></div>
    </div>
    <div id="controls">
        <div class="ctrl-btn active" onclick="setView('assembled')">🔧 Assembled</div>
        <div class="ctrl-btn" onclick="setView('exploded')">💥 Exploded</div>
        <div class="ctrl-btn" onclick="toggleSpin()">🔄 Auto Rotate</div>
        <div class="ctrl-btn" onclick="toggleLabels()">🏷️ Labels</div>
        <div class="ctrl-btn" onclick="resetCamera()">🎯 Reset</div>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const COMPONENTS = {comp_json};
const SHAPE = "{shape}";

let scene, camera, renderer, group, raycaster, mouse;
let meshes = [], labels = [], labelSprites = [];
let isExploded = false, isSpinning = true, showLabels = true;
let selectedMesh = null;

function init() {{
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a0a);
    
    camera = new THREE.PerspectiveCamera(50, window.innerWidth/{height}, 0.1, 100);
    camera.position.set(4, 3, 5);
    camera.lookAt(0, 0, 0);
    
    renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
    renderer.setSize(window.innerWidth, {height});
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    document.getElementById('canvas-container').appendChild(renderer.domElement);
    
    // Lights
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 10, 7);
    directionalLight.castShadow = true;
    scene.add(directionalLight);
    const pointLight = new THREE.PointLight(0xDC143C, 0.3, 20);
    pointLight.position.set(-3, 5, -3);
    scene.add(pointLight);
    
    // Grid
    const gridHelper = new THREE.GridHelper(10, 20, 0x222222, 0x111111);
    scene.add(gridHelper);
    
    group = new THREE.Group();
    scene.add(group);
    
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();
    
    createDevice();
    buildLegend();
    setupInteraction();
    
    document.getElementById('loading').style.display = 'none';
    animate();
}}

function createDevice() {{
    const n = COMPONENTS.length;
    const spacing = 0.15;
    
    COMPONENTS.forEach((comp, i) => {{
        let geometry;
        const sizeFactor = Math.sqrt(comp.weight_pct / 100) * 2;
        const yOffset = (i - n/2) * spacing;
        
        // Create varied shapes based on component type
        const name = comp.name.toLowerCase();
        if (name.includes('display') || name.includes('panel') || name.includes('screen')) {{
            geometry = new THREE.BoxGeometry(2.0 * sizeFactor + 0.5, 0.03, 1.4 * sizeFactor + 0.3);
        }} else if (name.includes('battery') || name.includes('cell')) {{
            geometry = new THREE.BoxGeometry(1.2 * sizeFactor + 0.3, 0.06, 0.8 * sizeFactor + 0.2);
        }} else if (name.includes('board') || name.includes('pcb') || name.includes('logic')) {{
            geometry = new THREE.BoxGeometry(1.5 * sizeFactor + 0.3, 0.02, 1.2 * sizeFactor + 0.2);
        }} else if (name.includes('cpu') || name.includes('chip') || name.includes('gpu') || name.includes('ic')) {{
            geometry = new THREE.BoxGeometry(0.3, 0.05, 0.3);
        }} else if (name.includes('motor') || name.includes('compressor') || name.includes('fan')) {{
            geometry = new THREE.CylinderGeometry(0.3 * sizeFactor + 0.1, 0.3 * sizeFactor + 0.1, 0.4 * sizeFactor + 0.1, 16);
        }} else if (name.includes('cable') || name.includes('wire') || name.includes('cord')) {{
            geometry = new THREE.TorusGeometry(0.2 * sizeFactor + 0.1, 0.02, 8, 32);
        }} else if (name.includes('case') || name.includes('chassis') || name.includes('frame') || name.includes('housing')) {{
            geometry = new THREE.BoxGeometry(2.2 * sizeFactor + 0.4, 0.1, 1.5 * sizeFactor + 0.3);
        }} else if (name.includes('speaker') || name.includes('camera') || name.includes('lens')) {{
            geometry = new THREE.CylinderGeometry(0.1, 0.15, 0.08, 16);
        }} else if (name.includes('ram') || name.includes('memory')) {{
            geometry = new THREE.BoxGeometry(0.8, 0.02, 0.15);
        }} else if (name.includes('capacitor') || name.includes('resistor') || name.includes('inductor')) {{
            geometry = new THREE.CylinderGeometry(0.04, 0.04, 0.12, 8);
        }} else if (name.includes('connector') || name.includes('port') || name.includes('slot')) {{
            geometry = new THREE.BoxGeometry(0.3, 0.05, 0.08);
        }} else {{
            geometry = new THREE.BoxGeometry(
                0.8 * sizeFactor + 0.2, 
                0.05 + Math.random() * 0.05, 
                0.6 * sizeFactor + 0.15
            );
        }}
        
        const material = new THREE.MeshPhongMaterial({{
            color: parseInt(comp.color.replace('#','0x')),
            transparent: true,
            opacity: 0.85,
            shininess: 80,
            side: THREE.DoubleSide
        }});
        
        if (comp.hazardous) {{
            material.emissive = new THREE.Color(0x330000);
            material.emissiveIntensity = 0.3;
        }}
        
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.y = yOffset;
        mesh.userData = {{ ...comp, assembledY: yOffset, explodedY: yOffset * 4 }};
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        
        // Edge wireframe
        const edges = new THREE.EdgesGeometry(geometry);
        const lineMat = new THREE.LineBasicMaterial({{ color: 0x444444, transparent: true, opacity: 0.3 }});
        const wireframe = new THREE.LineSegments(edges, lineMat);
        mesh.add(wireframe);
        
        group.add(mesh);
        meshes.push(mesh);
    }});
}}

function buildLegend() {{
    const legend = document.getElementById('legend');
    let html = '<div style="color:#DC143C;font-weight:bold;margin-bottom:6px;font-size:11px;">📦 COMPONENTS</div>';
    COMPONENTS.forEach((comp, i) => {{
        const haz = comp.hazardous ? ' <span class="haz-badge">⚠️</span>' : '';
        html += '<div class="legend-item" onclick="highlightComponent(' + i + ')">' +
            '<div class="legend-dot" style="background:' + comp.color + ';"></div>' +
            '<span>' + comp.name + haz + '</span></div>';
    }});
    legend.innerHTML = html;
}}

function highlightComponent(index) {{
    meshes.forEach((m, i) => {{
        if (i === index) {{
            m.material.opacity = 1.0;
            m.material.emissive = new THREE.Color(0x333333);
            m.material.emissiveIntensity = 0.5;
            m.scale.set(1.1, 1.1, 1.1);
            selectedMesh = m;
            showInfoPanel(m.userData);
        }} else {{
            m.material.opacity = 0.3;
            m.material.emissive = new THREE.Color(0x000000);
            m.material.emissiveIntensity = 0;
            m.scale.set(1, 1, 1);
        }}
    }});
}}

function showInfoPanel(data) {{
    const panel = document.getElementById('info-panel');
    panel.style.display = 'block';
    document.getElementById('comp-name').textContent = data.name;
    
    const haz = data.hazardous ? '🔴 HAZARDOUS' : '🟢 Safe';
    const rec = data.recyclable ? '♻️ Recyclable' : '❌ Not Recyclable';
    
    document.getElementById('comp-details').innerHTML = 
        '<div style="margin:4px 0;">📦 <b>Material:</b> ' + data.material + '</div>' +
        '<div style="margin:4px 0;">⚖️ <b>Weight:</b> ' + data.weight_pct + '% of device</div>' +
        '<div style="margin:4px 0;">💰 <b>Recovery Value:</b> $' + data.value_usd.toFixed(2) + '</div>' +
        '<div style="margin:4px 0;">' + haz + '</div>' +
        '<div style="margin:4px 0;">' + rec + '</div>';
}}

function setView(view) {{
    document.querySelectorAll('.ctrl-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    
    if (view === 'exploded') {{
        isExploded = true;
        meshes.forEach(m => {{
            m.material.opacity = 0.85;
            m.material.emissive = new THREE.Color(0x000000);
            m.scale.set(1, 1, 1);
        }});
    }} else {{
        isExploded = false;
        meshes.forEach(m => {{
            m.material.opacity = 0.85;
            m.material.emissive = new THREE.Color(0x000000);
            m.scale.set(1, 1, 1);
        }});
    }}
}}

function toggleSpin() {{ isSpinning = !isSpinning; event.target.classList.toggle('active'); }}
function toggleLabels() {{ showLabels = !showLabels; event.target.classList.toggle('active'); }}

function resetCamera() {{
    camera.position.set(4, 3, 5);
    camera.lookAt(0, 0, 0);
    meshes.forEach(m => {{
        m.material.opacity = 0.85;
        m.material.emissive = new THREE.Color(0x000000);
        m.scale.set(1, 1, 1);
    }});
    document.getElementById('info-panel').style.display = 'none';
    selectedMesh = null;
}}

function setupInteraction() {{
    let isDragging = false, prevX = 0, prevY = 0;
    const canvas = renderer.domElement;
    
    canvas.addEventListener('mousedown', e => {{ isDragging = true; prevX = e.clientX; prevY = e.clientY; }});
    canvas.addEventListener('mousemove', e => {{
        if (isDragging) {{
            const dx = (e.clientX - prevX) * 0.01;
            const dy = (e.clientY - prevY) * 0.01;
            group.rotation.y += dx;
            group.rotation.x = Math.max(-1, Math.min(1, group.rotation.x + dy));
            prevX = e.clientX; prevY = e.clientY;
        }}
    }});
    canvas.addEventListener('mouseup', () => isDragging = false);
    canvas.addEventListener('mouseleave', () => isDragging = false);
    
    canvas.addEventListener('wheel', e => {{
        camera.position.multiplyScalar(e.deltaY > 0 ? 1.05 : 0.95);
        e.preventDefault();
    }}, {{ passive: false }});
    
    canvas.addEventListener('click', e => {{
        const rect = canvas.getBoundingClientRect();
        mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(meshes);
        if (intersects.length > 0) {{
            const idx = meshes.indexOf(intersects[0].object);
            if (idx >= 0) highlightComponent(idx);
        }}
    }});
    
    // Touch support
    let touchStartX, touchStartY;
    canvas.addEventListener('touchstart', e => {{
        const t = e.touches[0];
        touchStartX = t.clientX; touchStartY = t.clientY;
        e.preventDefault();
    }}, {{ passive: false }});
    canvas.addEventListener('touchmove', e => {{
        const t = e.touches[0];
        const dx = (t.clientX - touchStartX) * 0.01;
        const dy = (t.clientY - touchStartY) * 0.01;
        group.rotation.y += dx;
        group.rotation.x = Math.max(-1, Math.min(1, group.rotation.x + dy));
        touchStartX = t.clientX; touchStartY = t.clientY;
        e.preventDefault();
    }}, {{ passive: false }});
}}

function animate() {{
    requestAnimationFrame(animate);
    
    if (isSpinning && !selectedMesh) {{
        group.rotation.y += 0.005;
    }}
    
    // Smooth explode/assemble animation
    meshes.forEach(m => {{
        const targetY = isExploded ? m.userData.explodedY : m.userData.assembledY;
        m.position.y += (targetY - m.position.y) * 0.08;
    }});
    
    renderer.render(scene, camera);
}}

window.addEventListener('resize', () => {{
    camera.aspect = window.innerWidth / {height};
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, {height});
}});

init();
</script>
</body></html>"""
    return html
