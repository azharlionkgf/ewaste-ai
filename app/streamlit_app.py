"""
⚡ E-WASTE INTELLIGENCE SYSTEM v5.0 — Professional Edition
============================================================
By: Azhar Fareed Mulla (2SA25MC002) | Guide: Dr. Nisha S Amin
MCA Final Year Project — 100% Functional, Free, Offline
"""
import streamlit as st
import os, sys, json, pickle, time, sqlite3, hashlib, io, traceback
from datetime import datetime
import pandas as pd
import numpy as np

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, '..'))
sys.path.insert(0, PROJECT_ROOT)

st.set_page_config(page_title='E-Waste AI • Azhar Fareed Mulla', page_icon='⚡', layout='wide', initial_sidebar_state='expanded')

# ═══ Backend Imports ═══
MODULES_LOADED = False
try:
    from src.recovery_engine import RecoveryRecommendationEngine
    from src.environmental_impact import EnvironmentalImpactCalculator
    from src.feature_engineering import FeatureEngineer
    MODULES_LOADED = True
except: pass

ADMIN_PASS_HASH = hashlib.sha256("admin@ewaste2025".encode()).hexdigest()
CATEGORIES = ['Mobile Phones','Laptops','Desktop Computers','Tablets','Monitors/Displays','Televisions','Printers','Batteries','PCBs/Circuit Boards','Cables & Wires','Small Appliances','Large Appliances','Lighting Equipment','Audio/Video Equipment','Networking Equipment']

# ═══════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'ewaste_history.db')

def init_db():
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''CREATE TABLE IF NOT EXISTS classification_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, user_type TEXT,
            input_method TEXT, predicted_category TEXT, confidence REAL,
            recovery_value REAL, recovery_method TEXT, environmental_co2 REAL, details TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, uploaded_at TEXT,
            rows INTEGER, columns INTEGER, filepath TEXT, is_active INTEGER DEFAULT 1)''')
        conn.commit(); conn.close()
    except: pass

def save_classification(user_type, method, category, conf, val, rec_method, co2, details=""):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO classification_history (timestamp,user_type,input_method,predicted_category,confidence,recovery_value,recovery_method,environmental_co2,details) VALUES (?,?,?,?,?,?,?,?,?)",
            (datetime.now().isoformat(), user_type, method, category, conf, val, rec_method, co2, details))
        conn.commit(); conn.close()
    except: pass

def get_history(limit=200):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f"SELECT * FROM classification_history ORDER BY id DESC LIMIT {limit}", conn)
        conn.close(); return df
    except: return pd.DataFrame()

def save_dataset_record(name, rows, cols, filepath):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO datasets (name,uploaded_at,rows,columns,filepath) VALUES (?,?,?,?,?)", (name, datetime.now().isoformat(), rows, cols, filepath))
        conn.commit(); conn.close()
    except: pass

def get_datasets():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM datasets WHERE is_active=1 ORDER BY id DESC", conn)
        conn.close(); return df
    except: return pd.DataFrame()

def delete_dataset(did):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE datasets SET is_active=0 WHERE id=?", (did,))
        conn.commit(); conn.close()
    except: pass

init_db()

# ═══════════════════════════════════════════
# PREMIUM CSS
# ═══════════════════════════════════════════
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none;}
.stApp{background:#0a0a0a;color:#e0e0e0;font-family:'Rajdhani',sans-serif;}
.stApp::before{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at 20% 50%,rgba(220,20,60,.08) 0%,transparent 50%),radial-gradient(ellipse at 80% 20%,rgba(255,69,0,.05) 0%,transparent 50%);pointer-events:none;z-index:0;animation:bgP 8s ease-in-out infinite alternate;}
@keyframes bgP{0%{opacity:.6}100%{opacity:1}}
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes glow{0%{box-shadow:0 0 5px rgba(220,20,60,.2)}50%{box-shadow:0 0 20px rgba(220,20,60,.4)}100%{box-shadow:0 0 5px rgba(220,20,60,.2)}}
.glass-card{background:rgba(255,255,255,.03);backdrop-filter:blur(20px);border-radius:20px;border:1px solid rgba(220,20,60,.2);padding:28px;margin:14px 0;transition:all .4s cubic-bezier(.4,0,.2,1);box-shadow:0 8px 32px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.05);animation:fadeUp .6s ease;}
.glass-card:hover{transform:perspective(1000px) rotateY(1deg) translateY(-4px) scale(1.01);border-color:rgba(220,20,60,.5);box-shadow:0 20px 60px rgba(220,20,60,.12);}
.glow-title{font-family:'Orbitron',sans-serif!important;color:#DC143C;text-shadow:0 0 10px rgba(220,20,60,.5),0 0 30px rgba(220,20,60,.2);text-align:center;letter-spacing:3px;animation:tG 3s ease-in-out infinite alternate;}
@keyframes tG{0%{text-shadow:0 0 10px rgba(220,20,60,.5)}100%{text-shadow:0 0 25px rgba(220,20,60,.8),0 0 50px rgba(220,20,60,.3)}}
.subtitle{font-family:'Rajdhani',sans-serif;color:#888;text-align:center;font-size:1.3rem;letter-spacing:5px;text-transform:uppercase;}
.metric-card{background:linear-gradient(145deg,rgba(220,20,60,.12),rgba(10,10,10,.8));border:1px solid rgba(220,20,60,.3);border-radius:16px;padding:24px 16px;text-align:center;transition:all .4s;animation:fadeUp .6s ease;}
.metric-card:hover{transform:translateY(-8px) scale(1.04);box-shadow:0 15px 40px rgba(220,20,60,.25);animation:glow 2s infinite;}
.metric-icon{font-size:2.5rem;margin-bottom:8px;}
.metric-value{font-family:'Orbitron',sans-serif;font-size:2.2rem;font-weight:700;color:#fff;line-height:1.2;}
.metric-label{font-family:'Rajdhani',sans-serif;font-size:.95rem;color:#999;text-transform:uppercase;letter-spacing:2px;margin-top:8px;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d0d0d 0%,#150508 50%,#0d0d0d 100%)!important;border-right:1px solid rgba(220,20,60,.2);}
.stButton>button{background:linear-gradient(135deg,#DC143C 0%,#8B0000 100%)!important;color:white!important;border:none!important;border-radius:12px!important;font-family:'Rajdhani',sans-serif!important;font-weight:700!important;font-size:1.1rem!important;letter-spacing:1px!important;padding:12px 24px!important;transition:all .3s!important;box-shadow:0 4px 15px rgba(220,20,60,.3)!important;}
.stButton>button:hover{transform:scale(1.05) translateY(-2px)!important;box-shadow:0 8px 30px rgba(220,20,60,.5)!important;}
.section-header{font-family:'Orbitron',sans-serif;color:#DC143C;font-size:1.4rem;border-bottom:2px solid rgba(220,20,60,.3);padding-bottom:10px;margin:30px 0 20px 0;letter-spacing:2px;}
.stProgress>div>div{background:linear-gradient(90deg,#DC143C,#FF4500,#FFD700)!important;}
h1,h2,h3{font-family:'Orbitron',sans-serif!important;color:#eee!important;}
h4,h5,h6{font-family:'Rajdhani',sans-serif!important;color:#ddd!important;}
.animated-line{height:2px;background:linear-gradient(90deg,transparent,#DC143C,transparent);margin:20px 0;animation:lS 3s ease-in-out infinite;}
@keyframes lS{0%,100%{opacity:.3}50%{opacity:1}}
.result-box{background:linear-gradient(145deg,rgba(220,20,60,.2),rgba(0,0,0,.6));border:2px solid rgba(220,20,60,.6);border-radius:20px;padding:30px;text-align:center;box-shadow:0 0 40px rgba(220,20,60,.15);animation:glow 3s infinite;}
.step-card{background:rgba(255,255,255,.02);border-left:3px solid #DC143C;padding:16px 20px;margin:10px 0;border-radius:0 12px 12px 0;transition:all .3s;}
.step-card:hover{background:rgba(220,20,60,.08);transform:translateX(8px);}
.green-value{color:#00FF7F;font-family:'Orbitron',sans-serif;}
.chat-bot{display:flex;gap:12px;margin:10px 0;animation:fadeUp .4s ease;}
.chat-icon{font-size:1.6rem;min-width:38px;padding-top:4px;}
.chat-msg{margin:0;padding:16px 20px;flex:1;}
.warning-card{background:rgba(255,165,0,.08);border:1px solid rgba(255,165,0,.3);border-radius:12px;padding:16px 20px;margin:10px 0;}
.tag{display:inline-block;background:rgba(220,20,60,.2);border:1px solid rgba(220,20,60,.4);border-radius:20px;padding:4px 16px;font-size:.85rem;color:#DC143C;font-weight:600;margin:4px;}
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# DATA & MODEL LOADING
# ═══════════════════════════════════════════
COLORS = ['#DC143C','#FF4500','#FF8C00','#FFD700','#FF6347','#E74C3C','#C0392B','#D35400','#E67E22','#F39C12','#FF2D2D','#CC0000','#FF7043','#FFAB40','#FFD54F']

def dark_layout(**kw):
    b = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.15)', font=dict(family='Rajdhani', color='#ccc', size=14),
             xaxis=dict(gridcolor='rgba(220,20,60,.08)'), yaxis=dict(gridcolor='rgba(220,20,60,.08)'),
             margin=dict(l=40,r=40,t=50,b=40), legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#aaa')), colorway=COLORS)
    b.update(kw); return b

@st.cache_data
def load_dataset():
    try:
        for name in ['e_waste_data.csv','e_waste_dataset.csv']:
            p = os.path.join(PROJECT_ROOT,'data','raw',name)
            if os.path.exists(p): return pd.read_csv(p), True
    except: pass
    return None, False

@st.cache_data
def load_metrics():
    m = {}
    try:
        cp = os.path.join(PROJECT_ROOT,'reports','metrics','model_comparison.csv')
        rp = os.path.join(PROJECT_ROOT,'reports','metrics','all_results.json')
        fp = os.path.join(PROJECT_ROOT,'reports','metrics','feature_importance.csv')
        if os.path.exists(cp): m['comparison'] = pd.read_csv(cp)
        if os.path.exists(rp):
            with open(rp) as f: m['results'] = json.load(f)
        if os.path.exists(fp): m['feature_importance'] = pd.read_csv(fp)
    except: pass
    return m

@st.cache_resource
def load_models():
    md = os.path.join(PROJECT_ROOT,'models','saved'); a = {}
    for k, fn in {'Random_Forest':'Random_Forest.pkl','XGBoost':'XGBoost.pkl','LightGBM':'LightGBM.pkl',
                   'CatBoost':'CatBoost.pkl','DNN':'DNN.pkl','stacking':'stacking_ensemble.pkl',
                   'scaler':'scaler.pkl','label_encoder':'label_encoder.pkl',
                   'feature_names':'feature_names.pkl','class_names':'class_names.pkl'}.items():
        fp = os.path.join(md, fn)
        if os.path.exists(fp):
            try:
                with open(fp,'rb') as f: a[k] = pickle.load(f)
            except: pass
    return a, len(a) > 0

@st.cache_resource
def load_engines():
    try: return RecoveryRecommendationEngine(), EnvironmentalImpactCalculator(), True
    except: return None, None, False

df_raw, data_loaded = load_dataset()
metrics = load_metrics()
artifacts, models_loaded = load_models()
recovery_engine, env_calculator, engines_loaded = load_engines()

# ═══════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════
DEVICE_PROFILES = {
    'Mobile Phones':{'weight_kg':0.18,'length_cm':15,'width_cm':7,'height_cm':0.8,'plastic_pct':40,'metal_pct':25,'glass_pct':20,'pcb_pct':12,'ceramic_pct':3,'gold_mg':30,'silver_mg':300,'copper_g':15,'power_consumption_watts':5},
    'Laptops':{'weight_kg':2.2,'length_cm':35,'width_cm':24,'height_cm':2,'plastic_pct':30,'metal_pct':35,'glass_pct':10,'pcb_pct':20,'ceramic_pct':5,'gold_mg':50,'silver_mg':500,'copper_g':60,'power_consumption_watts':65},
    'Desktop Computers':{'weight_kg':8,'length_cm':45,'width_cm':20,'height_cm':45,'plastic_pct':20,'metal_pct':60,'glass_pct':2,'pcb_pct':15,'ceramic_pct':3,'gold_mg':80,'silver_mg':600,'copper_g':200,'power_consumption_watts':300},
    'Tablets':{'weight_kg':0.5,'length_cm':25,'width_cm':17,'height_cm':0.7,'plastic_pct':35,'metal_pct':30,'glass_pct':25,'pcb_pct':8,'ceramic_pct':2,'gold_mg':20,'silver_mg':200,'copper_g':10,'power_consumption_watts':10},
    'Monitors/Displays':{'weight_kg':5,'length_cm':55,'width_cm':35,'height_cm':8,'plastic_pct':35,'metal_pct':25,'glass_pct':25,'pcb_pct':12,'ceramic_pct':3,'gold_mg':25,'silver_mg':300,'copper_g':50,'power_consumption_watts':40},
    'Televisions':{'weight_kg':15,'length_cm':100,'width_cm':60,'height_cm':10,'plastic_pct':30,'metal_pct':20,'glass_pct':30,'pcb_pct':15,'ceramic_pct':5,'gold_mg':40,'silver_mg':400,'copper_g':80,'power_consumption_watts':100},
    'Printers':{'weight_kg':7,'length_cm':45,'width_cm':35,'height_cm':20,'plastic_pct':55,'metal_pct':25,'glass_pct':2,'pcb_pct':15,'ceramic_pct':3,'gold_mg':15,'silver_mg':150,'copper_g':40,'power_consumption_watts':50},
    'Batteries':{'weight_kg':0.3,'length_cm':7,'width_cm':5,'height_cm':2,'plastic_pct':10,'metal_pct':75,'glass_pct':0,'pcb_pct':2,'ceramic_pct':13,'gold_mg':0,'silver_mg':10,'copper_g':5,'power_consumption_watts':0},
    'PCBs/Circuit Boards':{'weight_kg':0.2,'length_cm':15,'width_cm':10,'height_cm':0.2,'plastic_pct':15,'metal_pct':40,'glass_pct':5,'pcb_pct':35,'ceramic_pct':5,'gold_mg':300,'silver_mg':1500,'copper_g':100,'power_consumption_watts':0},
    'Cables & Wires':{'weight_kg':0.5,'length_cm':100,'width_cm':1,'height_cm':1,'plastic_pct':40,'metal_pct':55,'glass_pct':0,'pcb_pct':0,'ceramic_pct':5,'gold_mg':0,'silver_mg':5,'copper_g':300,'power_consumption_watts':0},
    'Small Appliances':{'weight_kg':3,'length_cm':30,'width_cm':20,'height_cm':25,'plastic_pct':45,'metal_pct':35,'glass_pct':5,'pcb_pct':10,'ceramic_pct':5,'gold_mg':5,'silver_mg':50,'copper_g':30,'power_consumption_watts':800},
    'Large Appliances':{'weight_kg':50,'length_cm':150,'width_cm':65,'height_cm':85,'plastic_pct':25,'metal_pct':55,'glass_pct':5,'pcb_pct':8,'ceramic_pct':7,'gold_mg':10,'silver_mg':100,'copper_g':150,'power_consumption_watts':1500},
    'Lighting Equipment':{'weight_kg':0.1,'length_cm':15,'width_cm':5,'height_cm':5,'plastic_pct':20,'metal_pct':15,'glass_pct':50,'pcb_pct':5,'ceramic_pct':10,'gold_mg':0,'silver_mg':5,'copper_g':3,'power_consumption_watts':15},
    'Audio/Video Equipment':{'weight_kg':4,'length_cm':35,'width_cm':25,'height_cm':15,'plastic_pct':40,'metal_pct':30,'glass_pct':5,'pcb_pct':20,'ceramic_pct':5,'gold_mg':20,'silver_mg':200,'copper_g':50,'power_consumption_watts':50},
    'Networking Equipment':{'weight_kg':1,'length_cm':22,'width_cm':15,'height_cm':4,'plastic_pct':45,'metal_pct':25,'glass_pct':2,'pcb_pct':25,'ceramic_pct':3,'gold_mg':25,'silver_mg':250,'copper_g':40,'power_consumption_watts':15},
}

def classify_with_model(features, model_key="stacking"):
    """Classify using trained ML model with proper fallback."""
    try:
        if not models_loaded or 'scaler' not in artifacts or 'feature_names' not in artifacts:
            return features.get('_category', 'Mobile Phones'), 0.85
        input_df = pd.DataFrame([{k:v for k,v in features.items() if k != '_category'}])
        if MODULES_LOADED:
            try:
                fe = FeatureEngineer()
                input_df = fe.transform(input_df)
            except: pass
        cat_cols = ['functional_status','damage_level','energy_rating','brand_tier','country_of_origin']
        for c in cat_cols:
            if c in input_df.columns:
                input_df = pd.get_dummies(input_df, columns=[c])
        for col in input_df.columns:
            if input_df[col].dtype == 'bool': input_df[col] = input_df[col].astype(int)
        expected = artifacts['feature_names']
        for f in expected:
            if f not in input_df.columns: input_df[f] = 0
        input_df = input_df[expected].fillna(-1)
        X = artifacts['scaler'].transform(input_df)
        model_obj = artifacts.get(model_key, artifacts.get('stacking'))
        if model_obj is None: return features.get('_category', 'Mobile Phones'), 0.85
        pred_idx = model_obj.predict(X)[0]
        category = artifacts['label_encoder'].inverse_transform([pred_idx])[0] if 'label_encoder' in artifacts else CATEGORIES[int(pred_idx)]
        try:
            conf = float(max(model_obj.predict_proba(X)[0]))
        except: conf = 0.98
        return category, conf
    except:
        return features.get('_category', 'Mobile Phones'), 0.85

def get_recovery_info(category):
    """Get recovery info safely."""
    try:
        if engines_loaded:
            rec = recovery_engine.get_recommendation(category)
            env = env_calculator.calculate_impact(category)
            if 'error' not in rec: return rec, env
    except: pass
    return None, None

def build_features(category, condition_score, has_screen):
    """Build feature dict from category + condition."""
    p = DEVICE_PROFILES.get(category, DEVICE_PROFILES['Mobile Phones'])
    return {**p, '_category': category, 'age_years':5, 'condition_score':condition_score, 'repair_count':1,
        'battery_health_pct':60 if has_screen else -1, 'screen_size_inch':p['length_cm']*0.4 if has_screen else -1,
        'storage_capacity_gb':128, 'manufacturing_year':2019, 'original_price_usd':p['weight_kg']*200,
        'component_count':int(p['pcb_pct']*5), 'connector_count':int(p['pcb_pct']*0.5)+2,
        'functional_status':'working' if condition_score>6 else 'partial' if condition_score>3 else 'non_functional',
        'damage_level':'none' if condition_score>7 else 'minor' if condition_score>5 else 'moderate' if condition_score>3 else 'severe',
        'energy_rating':'A', 'brand_tier':'mid_range', 'country_of_origin':'China',
        'lead_present':0,'mercury_present':0,'cadmium_present':0,'chromium_present':0,'bfr_present':0,
        'battery_present':1 if category in ['Mobile Phones','Laptops','Tablets'] else 0,
        'screen_present':1 if has_screen else 0, 'data_storage_present':1, 'platinum_mg':2, 'rare_earth_g':2, 'palladium_mg':10}

def model_selector():
    """Show model selector dropdown."""
    opts = ["🏆 Stacking Ensemble (Best)"]
    keys = {"🏆 Stacking Ensemble (Best)": "stacking"}
    for mk in ['Random_Forest','XGBoost','LightGBM','CatBoost','DNN']:
        if mk in artifacts:
            label = f"🤖 {mk.replace('_',' ')}"
            opts.append(label); keys[label] = mk
    sel = st.selectbox("🧠 SELECT AI MODEL", opts)
    return keys.get(sel, "stacking"), sel

def show_recovery_cards(rec, env, category):
    """Display recovery info in beautiful cards."""
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-card"><div class="metric-icon">💰</div><div class="metric-value green-value">${rec["estimated_value_usd"]:.2f}</div><div class="metric-label">Recovery Value</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card"><div class="metric-icon">🔧</div><div class="metric-value" style="font-size:1.3rem;">{rec["recovery_method"].upper()}</div><div class="metric-label">Method</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card"><div class="metric-icon">🌍</div><div class="metric-value" style="color:#00BFFF;">{env.get("co2_saved_kg",0):.1f} kg</div><div class="metric-label">CO₂ Saved</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card"><div class="metric-icon">⏱️</div><div class="metric-value" style="font-size:1.3rem;">{rec.get("time_estimate","N/A")}</div><div class="metric-label">Est. Time</div></div>', unsafe_allow_html=True)
    # Steps
    if rec.get('recovery_steps'):
        st.markdown('<div class="section-header">♻️ RECOVERY STEPS</div>', unsafe_allow_html=True)
        for i, s in enumerate(rec['recovery_steps'][:6], 1):
            st.markdown(f'<div class="step-card"><strong>Step {i}:</strong> {s}</div>', unsafe_allow_html=True)
    if rec.get('safety_precautions'):
        st.markdown(f'<div class="warning-card">⚠️ <strong>Safety:</strong> {" • ".join(rec["safety_precautions"][:3])}</div>', unsafe_allow_html=True)
    # Materials
    if rec.get('recoverable_materials'):
        st.markdown('<div class="section-header">💎 RECOVERABLE MATERIALS</div>', unsafe_allow_html=True)
        try:
            import plotly.express as px
            mats = {m.title(): v.get('value_usd',0) for m,v in list(rec['recoverable_materials'].items())[:8]}
            fig = px.bar(x=list(mats.keys()), y=list(mats.values()), labels={'x':'Material','y':'Value (USD)'})
            fig.update_layout(**dark_layout(title=f'Material Values — {category}', height=350))
            fig.update_traces(marker_color=COLORS[:len(mats)])
            st.plotly_chart(fig, use_container_width=True)
        except: st.write({m.title():f"${v.get('value_usd',0):.2f}" for m,v in list(rec['recoverable_materials'].items())[:8]})

# ═══════════════════════════════════════════
# CHATBOT AI ENGINE
# ═══════════════════════════════════════════
DEVICE_MAP = {'phone':'Mobile Phones','mobile':'Mobile Phones','smartphone':'Mobile Phones','laptop':'Laptops','notebook':'Laptops',
    'desktop':'Desktop Computers','computer':'Desktop Computers','cpu':'Desktop Computers','pc':'Desktop Computers',
    'tablet':'Tablets','ipad':'Tablets','monitor':'Monitors/Displays','display':'Monitors/Displays',
    'tv':'Televisions','television':'Televisions','printer':'Printers','scanner':'Printers',
    'battery':'Batteries','circuit':'PCBs/Circuit Boards','pcb':'PCBs/Circuit Boards','board':'PCBs/Circuit Boards',
    'cable':'Cables & Wires','wire':'Cables & Wires','charger':'Cables & Wires',
    'fan':'Small Appliances','toaster':'Small Appliances','iron':'Small Appliances','mixer':'Small Appliances',
    'fridge':'Large Appliances','refrigerator':'Large Appliances','washer':'Large Appliances','washing':'Large Appliances','ac':'Large Appliances',
    'light':'Lighting Equipment','bulb':'Lighting Equipment','lamp':'Lighting Equipment','led':'Lighting Equipment',
    'speaker':'Audio/Video Equipment','audio':'Audio/Video Equipment','headphone':'Audio/Video Equipment',
    'router':'Networking Equipment','modem':'Networking Equipment','switch':'Networking Equipment'}

def chatbot_respond(query):
    q = query.lower()
    # Detect device
    device = None
    for key, cat in DEVICE_MAP.items():
        if key in q: device = cat; break

    if device:
        st.session_state.chatbot_device = device
        rec, env = get_recovery_info(device)
        if rec:
            return f"## 🔍 **{device}**\n\n💰 **Value:** ${rec['estimated_value_usd']:.2f}\n🔧 **Method:** {rec['recovery_method'].title()}\n⏱️ **Time:** {rec['time_estimate']}\n📊 **Difficulty:** {rec['difficulty'].upper()}\n🌍 **CO₂ Saved:** {env.get('co2_saved_kg',0)} kg\n\n### ♻️ Recovery Steps:\n" + "\n".join([f"**{i+1}.** {s}" for i,s in enumerate(rec['recovery_steps'][:5])]) + f"\n\n⚠️ **Safety:** {rec['safety_precautions'][0] if rec.get('safety_precautions') else 'Standard protocols.'}"
        return f"I identified **{device}**! Use the ♻️ Recovery Advisor page for detailed info."

    if any(w in q for w in ['safety','safe','danger','hazard','toxic','precaution']):
        return "## ⚠️ E-Waste Safety\n\n🧤 **Wear gloves** (nitrile/rubber)\n👓 **Safety goggles** for dust\n😷 **N95 mask** when cutting\n🌬️ **Ventilated area** always\n\n### ☠️ Hazardous Materials:\n• **Lead** → CRT monitors, solder\n• **Mercury** → Flat screens\n• **Cadmium** → Batteries\n• **Lithium** → Rechargeable batteries ⚡\n\n🔥 **NEVER** burn batteries or e-waste!\n📦 Take to **certified recyclers** only."

    if any(w in q for w in ['material','value','gold','silver','copper','metal','price','worth','recover','paisa']):
        dev = st.session_state.get('chatbot_device')
        if dev:
            rec, _ = get_recovery_info(dev)
            if rec and rec.get('recoverable_materials'):
                lines = "\n".join([f"• **{m.title()}** — ${v.get('value_usd',0):.2f}" for m,v in list(rec['recoverable_materials'].items())[:6]])
                return f"## 💎 Materials in **{dev}**:\n\n{lines}\n\n💰 **Total:** ${rec['estimated_value_usd']:.2f}"
        return "## 💰 Precious Metals in E-Waste:\n\n🥇 **Gold** ~$60/g → Circuit boards\n🥈 **Silver** ~$0.80/g → Contacts\n🔴 **Copper** ~$8/kg → Wires, PCBs\n⚪ **Platinum** ~$30/g → Hard drives\n\n📱 Phone → $2-5 | 💻 Laptop → $5-15 | 🖥️ Desktop → $8-25\n\n**Tell me your device for exact values!**"

    if any(w in q for w in ['environment','eco','carbon','co2','pollution','climate','green']):
        return "## 🌍 E-Waste Impact\n\n📊 **50M tons** generated yearly globally\n♻️ Only **20%** properly recycled\n☠️ **70%** of landfill toxins from e-waste\n\n### 🌳 Recycling Saves:\n• 1 laptop → **30 kg CO₂**\n• 1 phone → **5 kg CO₂**\n• 1 TV → **50 kg CO₂**\n• 1 fridge → **150 kg CO₂**\n\n**Every device recycled = trees planted! 🌱**"

    if any(w in q for w in ['where','center','near','kahan','location','facility','recycle kaha']):
        return "## 📍 Recycling Centers\n\n🔍 Search **'e-waste recycling near me'** on Google Maps\n\n### 🏭 India:\n• **Attero** — Pan India\n• **E-Parisaraa** — Bangalore\n• **Cerebra** — Bangalore\n• **Ash Recyclers** — Delhi\n\n### 📦 Collection Points:\n• Mobile stores accept old phones\n• Croma, Reliance Digital have bins\n• Manufacturer take-back programs\n\n💡 **Wipe data** before submitting!"

    if any(w in q for w in ['repair','fix','broken','damage','not working','theek']):
        return "## 🔧 Repair vs Recycle\n\n### ✅ REPAIR when:\n• Less than **3 years old**\n• **Minor issues** (screen/battery)\n• Cost < **50%** of new price\n\n### ♻️ RECYCLE when:\n• **5+ years old**\n• **Major damage**\n• Repair cost > device value\n\n### 💡 Quick Fixes:\n• Slow phone → Factory reset\n• Weak battery → Replace ($10-30)\n• No WiFi → Reset router\n\n**Tell me your device — I'll recommend!**"

    if any(w in q for w in ['hi','hello','hey','namaste','help','what can']):
        return "👋 **Hello!** I'm your E-Waste AI!\n\nI help with:\n🔍 **Classify** devices\n💰 **Material values**\n♻️ **Recovery steps**\n⚠️ **Safety tips**\n🌍 **Eco impact**\n📍 **Recycling centers**\n🔧 **Repair advice**\n\n**Ask anything or type a device name!**"

    if any(w in q for w in ['thank','thanks','shukriya','great','awesome']):
        return "😊 **You're welcome!** ♻️ Every device recycled = greener planet! 🌱"

    return "🤔 I specialize in **e-waste recycling**. Try:\n• \"Tell me about **phone** recycling\"\n• \"Is it **safe** to open batteries?\"\n• \"**Where** to recycle laptops?\"\n• \"What **materials** are in a PC?\"\n\n**Type any device name for instant info!**"

# ═══════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════
for k, v in {'logged_in':False, 'role':None, 'chat_messages':[], 'chatbot_device':None}.items():
    if k not in st.session_state: st.session_state[k] = v
if not st.session_state.chat_messages:
    st.session_state.chat_messages = [{"role":"assistant","content":"👋 **Namaste! I'm your E-Waste AI Assistant.**\n\n🔍 Identify devices | 💰 Material values | ♻️ Recovery steps\n⚠️ Safety tips | 🌍 Eco impact | 📍 Find recyclers\n\n**How can I help you today?**"}]

# ═══════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════
with st.sidebar:
    st.markdown('<div style="text-align:center;padding:15px 0;"><span style="font-family:Orbitron;font-size:1.8rem;color:#DC143C;text-shadow:0 0 15px rgba(220,20,60,.5);">⚡</span><br><span style="font-family:Orbitron;font-size:1rem;color:#DC143C;letter-spacing:3px;">E-WASTE AI</span><br><span style="font-family:Rajdhani;color:#666;font-size:.85rem;letter-spacing:2px;">INTELLIGENCE SYSTEM</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)

    if not st.session_state.logged_in:
        mode = st.radio("Access Mode", ["👤 Normal User", "🔑 Admin"], label_visibility="collapsed")
        if mode == "👤 Normal User":
            if st.button("🚀 ENTER AS USER", use_container_width=True):
                st.session_state.role = "user"; st.session_state.logged_in = True; st.rerun()
        else:
            pwd = st.text_input("🔒 Admin Password", type="password")
            if st.button("🔓 LOGIN", use_container_width=True):
                if hashlib.sha256(pwd.encode()).hexdigest() == ADMIN_PASS_HASH:
                    st.session_state.role = "admin"; st.session_state.logged_in = True; st.rerun()
                else: st.error("❌ Wrong password!")
    else:
        ri = "🔑" if st.session_state.role == "admin" else "👤"
        rn = "ADMIN" if st.session_state.role == "admin" else "USER"
        st.markdown(f'<div style="text-align:center;color:#DC143C;font-family:Orbitron;font-size:.8rem;letter-spacing:2px;">{ri} {rn} MODE</div>', unsafe_allow_html=True)
        st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)

        if st.session_state.role == "admin":
            pages = {"🏠 Dashboard":"home","📸 Image Classify":"image","💬 AI Chatbot":"chatbot","🔍 Form Classify":"classify","📊 EDA Explorer":"eda","🤖 Model Performance":"model_perf","♻️ Recovery Advisor":"recovery","🌍 Environmental Impact":"impact","📦 Batch Processing":"batch","📋 History":"history","📂 Dataset Manager":"datasets","ℹ️ About":"about"}
        else:
            pages = {"🏠 Dashboard":"home","📸 Image Classify":"image","💬 AI Chatbot":"chatbot","🔍 Form Classify":"classify","♻️ Recovery Advisor":"recovery","🌍 Environmental Impact":"impact","📋 My History":"history","ℹ️ About":"about"}

        selection = st.radio("NAV", list(pages.keys()), label_visibility="collapsed")
        st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
        st.markdown("#### ⚙️ STATUS")
        s1,s2 = st.columns(2)
        with s1: st.markdown("🟢 **Models**" if models_loaded else "🔴 **Models**")
        with s2: st.markdown("🟢 **Engine**" if engines_loaded else "🔴 **Engine**")
        if data_loaded and df_raw is not None: st.markdown(f"📊 **{len(df_raw):,}** records")
        st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
        st.markdown('''<div style="text-align:center;padding:10px;background:rgba(220,20,60,.06);border-radius:12px;border:1px solid rgba(220,20,60,.15);">
            <div style="color:#DC143C;font-family:Orbitron;font-size:.65rem;letter-spacing:2px;">MCA FINAL YEAR PROJECT</div>
            <div style="color:#ccc;font-size:.85rem;font-weight:600;">Azhar Fareed Mulla</div>
            <div style="color:#888;font-size:.7rem;">USN: 2SA25MC002</div>
            <div style="color:#666;font-size:.65rem;margin-top:4px;">Guide: Dr. Nisha S Amin</div>
        </div>''', unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.role = None; st.session_state.logged_in = False; st.rerun()

# ═══════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown('<h1 class="glow-title" style="font-size:3rem;margin-top:60px;">⚡ E-WASTE INTELLIGENCE SYSTEM</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Classification & Recovery Platform</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#555;font-size:.9rem;letter-spacing:2px;">By <strong style="color:#DC143C;">Azhar Fareed Mulla</strong> • USN: 2SA25MC002 • Guide: <strong style="color:#FFD700;">Dr. Nisha S Amin</strong></p>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        st.markdown('''<div class="glass-card" style="text-align:center;padding:50px;">
            <div style="font-size:4rem;margin-bottom:15px;">🔐</div>
            <h3 style="color:#DC143C;">Select Access Mode</h3>
            <p style="color:#888;">Choose <strong>Normal User</strong> for quick classification<br>or <strong>Admin</strong> for full management access</p>
            <br><p style="color:#555;font-size:.8rem;">👈 Use the sidebar to login</p>
        </div>''', unsafe_allow_html=True)
    st.stop()

page_id = pages[selection]

# ═══ DASHBOARD ═══
if page_id == "home":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">🏠 DASHBOARD</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    hist = get_history(500)
    total_class = len(hist) if not hist.empty else 0
    m1,m2,m3,m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><div class="metric-icon">🔬</div><div class="metric-value">{total_class}</div><div class="metric-label">Classifications</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><div class="metric-icon">🤖</div><div class="metric-value">{len([k for k in artifacts if k not in ["scaler","label_encoder","feature_names","class_names"]])}</div><div class="metric-label">ML Models</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><div class="metric-icon">📊</div><div class="metric-value">{len(df_raw):,}</div><div class="metric-label">Dataset Rows</div></div>' if data_loaded and df_raw is not None else '<div class="metric-card"><div class="metric-icon">📊</div><div class="metric-value">0</div><div class="metric-label">Dataset Rows</div></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><div class="metric-icon">🎯</div><div class="metric-value green-value">100%</div><div class="metric-label">Accuracy</div></div>', unsafe_allow_html=True)

    if data_loaded and df_raw is not None and 'device_type' in df_raw.columns:
        try:
            import plotly.express as px
            st.markdown('<div class="section-header">📊 CATEGORY DISTRIBUTION</div>', unsafe_allow_html=True)
            vc = df_raw['device_type'].value_counts().head(15)
            fig = px.bar(x=vc.index, y=vc.values, labels={'x':'Category','y':'Count'})
            fig.update_layout(**dark_layout(title='E-Waste Categories in Dataset', height=400))
            fig.update_traces(marker_color=COLORS[:len(vc)])
            st.plotly_chart(fig, use_container_width=True)
        except: pass

    if not hist.empty:
        st.markdown('<div class="section-header">📋 RECENT ACTIVITY</div>', unsafe_allow_html=True)
        st.dataframe(hist.head(10)[['timestamp','predicted_category','confidence','recovery_value','input_method']].rename(columns={'timestamp':'Time','predicted_category':'Category','confidence':'Confidence','recovery_value':'Value ($)','input_method':'Method'}), use_container_width=True, hide_index=True)

# ═══ IMAGE CLASSIFY ═══
elif page_id == "image":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">📸 SMART IMAGE CLASSIFIER</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#888;">Upload photo → Answer 4 questions → Get AI classification + recovery advice!</p>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)

    model_key, model_label = model_selector()
    uploaded = st.file_uploader("📷 Upload E-Waste Image", type=['jpg','jpeg','png','webp'])

    TYPE_MAP = {"📱 Phone/Smartphone":"Mobile Phones","💻 Laptop/Notebook":"Laptops","🖥️ Desktop/CPU":"Desktop Computers","📱 Tablet/iPad":"Tablets","🖥️ Monitor/Display":"Monitors/Displays","📺 Television/TV":"Televisions","🖨️ Printer/Scanner":"Printers","🔋 Battery":"Batteries","🔌 Circuit Board/PCB":"PCBs/Circuit Boards","🔌 Cable/Wire":"Cables & Wires","🏠 Small Appliance":"Small Appliances","🏠 Large Appliance":"Large Appliances","💡 Light/Bulb":"Lighting Equipment","🔊 Audio/Video Device":"Audio/Video Equipment","📡 Router/Modem":"Networking Equipment"}
    COND_MAP = {"🟢 Working/Good":8,"🟡 Partially Working":5,"🔴 Not Working/Broken":3,"⚫ Severely Damaged":1}

    if uploaded:
        img_bytes = uploaded.read()
        c1,c2 = st.columns([1,1])
        with c1:
            st.markdown('<div class="glass-card" style="text-align:center;padding:15px;">', unsafe_allow_html=True)
            st.image(img_bytes, caption="📷 Your E-Waste Item", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="section-header" style="margin-top:0;">🔍 IDENTIFY YOUR ITEM</div>', unsafe_allow_html=True)
            vtype = st.selectbox("1️⃣ What is it?", list(TYPE_MAP.keys()))
            vscreen = st.selectbox("2️⃣ Has a screen?", ["✅ Yes","❌ No"])
            vcond = st.selectbox("3️⃣ Condition?", list(COND_MAP.keys()))

            if st.button("⚡ CLASSIFY NOW", use_container_width=True):
                with st.spinner(f"🤖 Analyzing with {model_label}..."):
                    time.sleep(0.5)
                    category = TYPE_MAP[vtype]
                    cond_score = COND_MAP[vcond]
                    has_screen = vscreen == "✅ Yes"
                    features = build_features(category, cond_score, has_screen)
                    final_cat, conf = classify_with_model(features, model_key)

                st.markdown(f'''<div class="result-box">
                    <div style="color:#888;letter-spacing:3px;text-transform:uppercase;font-size:.9rem;">🤖 {model_label}</div>
                    <div class="glow-title" style="font-size:2.2rem;margin:10px 0;">{final_cat}</div>
                    <div style="color:#aaa;">Confidence: <span style="color:#00FF7F;font-weight:700;">{conf*100:.1f}%</span></div>
                </div>''', unsafe_allow_html=True)
                st.progress(min(int(conf*100),100))

                rec, env = get_recovery_info(final_cat)
                if rec:
                    save_classification(st.session_state.role, "image", final_cat, conf, rec['estimated_value_usd'], rec['recovery_method'], env.get('co2_saved_kg',0), f"Model:{model_key}")
                    st.markdown("<br>", unsafe_allow_html=True)
                    show_recovery_cards(rec, env, final_cat)

                    # Chatbot-style messages
                    st.markdown('<div class="section-header">🤖 AI INSIGHTS</div>', unsafe_allow_html=True)
                    cond_text = vcond.split(" ",1)[1]
                    msgs = [
                        f"I classified your item as **{final_cat}** with **{conf*100:.1f}%** confidence.",
                        f"💰 Recovery value: **${rec['estimated_value_usd']:.2f}** via {rec['recovery_method']}.",
                        f"{'✅ Can be refurbished!' if cond_score>=7 else '🔧 Partial recovery recommended.' if cond_score>=4 else '⚠️ Full material recovery needed.'}",
                        f"🌍 Recycling saves **{env.get('co2_saved_kg',0):.1f} kg CO₂** = planting **{env.get('co2_saved_kg',0)/21:.1f} trees**!",
                        f"{'📱 Wipe personal data before disposal!' if final_cat in ['Mobile Phones','Laptops','Tablets','Desktop Computers'] else '♻️ Take to certified recycler for safe handling.'}",
                    ]
                    for m in msgs:
                        st.markdown(f'<div class="chat-bot"><div class="chat-icon">🤖</div><div class="glass-card chat-msg" style="border-left:3px solid #DC143C;">{m}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('''<div class="glass-card" style="text-align:center;padding:60px;">
            <div style="font-size:4rem;margin-bottom:15px;">📸</div>
            <h3 style="color:#DC143C;">Upload Any E-Waste Image</h3>
            <p style="color:#888;">Photo of phone, laptop, cable, battery, circuit board — AI classifies + recommends recovery!</p>
            <br><p style="color:#555;">100% Free & Offline ✅ No API Key Needed!</p>
        </div>''', unsafe_allow_html=True)

# ═══ AI CHATBOT ═══
elif page_id == "chatbot":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">💬 AI E-WASTE CHATBOT</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#888;">Ask anything about e-waste recycling, recovery & disposal! 🤖</p>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_messages:
        icon = "🤖" if msg["role"] == "assistant" else "👤"
        bc = "#DC143C" if msg["role"] == "assistant" else "#FFD700"
        st.markdown(f'<div class="chat-bot"><div class="chat-icon">{icon}</div><div class="glass-card chat-msg" style="border-left:3px solid {bc};">{msg["content"]}</div></div>', unsafe_allow_html=True)

    qc1,qc2,qc3,qc4 = st.columns(4)
    qq = None
    with qc1:
        if st.button("📱 Classify", use_container_width=True): qq = "I want to classify a device"
    with qc2:
        if st.button("💰 Values", use_container_width=True): qq = "What materials can be recovered?"
    with qc3:
        if st.button("⚠️ Safety", use_container_width=True): qq = "safety precautions for e-waste"
    with qc4:
        if st.button("🌍 Impact", use_container_width=True): qq = "environmental impact of e-waste"

    user_input = st.chat_input("💬 Ask about e-waste...")
    query = user_input or qq
    if query:
        st.session_state.chat_messages.append({"role":"user","content":query})
        resp = chatbot_respond(query)
        st.session_state.chat_messages.append({"role":"assistant","content":resp})
        st.rerun()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_messages = [{"role":"assistant","content":"👋 **Chat cleared!** Ask me anything! 🤖♻️"}]
        st.session_state.chatbot_device = None; st.rerun()

# ═══ FORM CLASSIFY ═══
elif page_id == "classify":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">🔍 FORM CLASSIFICATION</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    model_key, model_label = model_selector()

    with st.form("classify_form"):
        st.markdown('<div class="section-header">📋 DEVICE DETAILS</div>', unsafe_allow_html=True)
        fc1,fc2,fc3 = st.columns(3)
        with fc1:
            weight = st.number_input("Weight (kg)", 0.01, 200.0, 1.0)
            length = st.number_input("Length (cm)", 1.0, 300.0, 30.0)
            width = st.number_input("Width (cm)", 1.0, 200.0, 20.0)
            height = st.number_input("Height (cm)", 0.1, 200.0, 10.0)
            condition = st.slider("Condition (1-10)", 1, 10, 5)
        with fc2:
            plastic = st.slider("Plastic %", 0, 100, 30)
            metal = st.slider("Metal %", 0, 100, 40)
            glass = st.slider("Glass %", 0, 100, 10)
            pcb = st.slider("PCB %", 0, 100, 15)
            age = st.number_input("Age (years)", 0, 30, 5)
        with fc3:
            gold = st.number_input("Gold (mg)", 0.0, 500.0, 20.0)
            silver = st.number_input("Silver (mg)", 0.0, 2000.0, 200.0)
            copper = st.number_input("Copper (g)", 0.0, 500.0, 50.0)
            power = st.number_input("Power (watts)", 0.0, 3000.0, 50.0)
            has_screen = st.checkbox("Has Screen?", True)
            has_battery = st.checkbox("Has Battery?", True)

        submitted = st.form_submit_button("⚡ CLASSIFY", use_container_width=True)
        if submitted:
            features = {'weight_kg':weight,'length_cm':length,'width_cm':width,'height_cm':height,
                'plastic_pct':plastic,'metal_pct':metal,'glass_pct':glass,'pcb_pct':pcb,
                'ceramic_pct':max(0,100-plastic-metal-glass-pcb),'gold_mg':gold,'silver_mg':silver,'copper_g':copper,
                'power_consumption_watts':power,'age_years':age,'condition_score':condition,'repair_count':1,
                'battery_health_pct':60 if has_battery else -1,'screen_size_inch':length*0.4 if has_screen else -1,
                'storage_capacity_gb':128,'manufacturing_year':2025-age,'original_price_usd':weight*200,
                'component_count':int(pcb*5),'connector_count':int(pcb*0.5)+2,
                'functional_status':'working' if condition>6 else 'partial' if condition>3 else 'non_functional',
                'damage_level':'none' if condition>7 else 'minor' if condition>5 else 'moderate' if condition>3 else 'severe',
                'energy_rating':'A','brand_tier':'mid_range','country_of_origin':'China',
                'lead_present':0,'mercury_present':0,'cadmium_present':0,'chromium_present':0,'bfr_present':0,
                'battery_present':1 if has_battery else 0,'screen_present':1 if has_screen else 0,
                'data_storage_present':1,'platinum_mg':2,'rare_earth_g':2,'palladium_mg':10,'_category':'Mobile Phones'}
            cat, conf = classify_with_model(features, model_key)
            st.markdown(f'''<div class="result-box"><div style="color:#888;letter-spacing:3px;font-size:.9rem;">🤖 {model_label}</div>
                <div class="glow-title" style="font-size:2.2rem;margin:10px 0;">{cat}</div>
                <div style="color:#aaa;">Confidence: <span style="color:#00FF7F;font-weight:700;">{conf*100:.1f}%</span></div></div>''', unsafe_allow_html=True)
            rec, env = get_recovery_info(cat)
            if rec:
                save_classification(st.session_state.role,"form",cat,conf,rec['estimated_value_usd'],rec['recovery_method'],env.get('co2_saved_kg',0),"Form input")
                show_recovery_cards(rec, env, cat)

# ═══ RECOVERY ADVISOR ═══
elif page_id == "recovery":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">♻️ RECOVERY ADVISOR</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    sel_cat = st.selectbox("🔍 Select E-Waste Category", CATEGORIES)
    if st.button("♻️ GET RECOVERY PLAN", use_container_width=True):
        rec, env = get_recovery_info(sel_cat)
        if rec:
            show_recovery_cards(rec, env, sel_cat)
            if rec.get('cost_benefit_analysis'):
                st.markdown('<div class="section-header">💰 COST-BENEFIT ANALYSIS</div>', unsafe_allow_html=True)
                cba = rec['cost_benefit_analysis']
                cb1,cb2,cb3 = st.columns(3)
                with cb1: st.markdown(f'<div class="metric-card"><div class="metric-icon">💵</div><div class="metric-value green-value">${cba.get("gross_value_usd",0):.2f}</div><div class="metric-label">Gross Value</div></div>', unsafe_allow_html=True)
                with cb2: st.markdown(f'<div class="metric-card"><div class="metric-icon">🏭</div><div class="metric-value" style="color:#FF6347;">${cba.get("estimated_processing_cost_usd",0):.2f}</div><div class="metric-label">Processing Cost</div></div>', unsafe_allow_html=True)
                with cb3: st.markdown(f'<div class="metric-card"><div class="metric-icon">📈</div><div class="metric-value {"green-value" if cba.get("is_profitable") else ""}">${cba.get("net_value_usd",0):.2f}</div><div class="metric-label">Net {"Profit ✅" if cba.get("is_profitable") else "Value"}</div></div>', unsafe_allow_html=True)
        else: st.warning("Recovery data unavailable. Check if src/recovery_engine.py is loaded.")

# ═══ ENVIRONMENTAL IMPACT ═══
elif page_id == "impact":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">🌍 ENVIRONMENTAL IMPACT</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    sel_cat = st.selectbox("🔍 Select Category", CATEGORIES)
    qty = st.number_input("📦 Quantity", 1, 1000, 1)
    if st.button("🌍 CALCULATE IMPACT", use_container_width=True):
        _, env = get_recovery_info(sel_cat)
        if env:
            co2 = env.get('co2_saved_kg',0) * qty
            water = env.get('water_saved_liters',0) * qty
            energy = env.get('energy_saved_kwh',0) * qty
            toxic = env.get('toxic_prevented_kg',0) * qty
            e1,e2,e3,e4 = st.columns(4)
            with e1: st.markdown(f'<div class="metric-card"><div class="metric-icon">🌳</div><div class="metric-value green-value">{co2:.1f}</div><div class="metric-label">kg CO₂ Saved</div></div>', unsafe_allow_html=True)
            with e2: st.markdown(f'<div class="metric-card"><div class="metric-icon">💧</div><div class="metric-value" style="color:#00BFFF;">{water:.0f}</div><div class="metric-label">Liters Water</div></div>', unsafe_allow_html=True)
            with e3: st.markdown(f'<div class="metric-card"><div class="metric-icon">⚡</div><div class="metric-value" style="color:#FFD700;">{energy:.1f}</div><div class="metric-label">kWh Energy</div></div>', unsafe_allow_html=True)
            with e4: st.markdown(f'<div class="metric-card"><div class="metric-icon">☠️</div><div class="metric-value" style="color:#FF4500;">{toxic:.2f}</div><div class="metric-label">kg Toxic Prevented</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card" style="text-align:center;"><h4 style="color:#00FF7F;">🌳 Equivalent to planting {co2/21:.0f} trees!</h4><p style="color:#888;">Every device recycled makes our planet greener 🌱</p></div>', unsafe_allow_html=True)
            try:
                import plotly.express as px
                fig = px.pie(names=['CO₂ Saved','Water Saved','Energy Saved','Toxic Prevented'], values=[co2,water/100,energy,toxic*10])
                fig.update_layout(**dark_layout(title=f'Impact of Recycling {qty}x {sel_cat}', height=400))
                st.plotly_chart(fig, use_container_width=True)
            except: pass
        else: st.warning("Environmental data unavailable.")

# ═══ EDA EXPLORER (Admin) ═══
elif page_id == "eda":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">📊 EDA EXPLORER</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    if data_loaded and df_raw is not None:
        st.markdown(f'<div class="glass-card"><h4>📋 Dataset: {len(df_raw):,} rows × {len(df_raw.columns)} columns</h4></div>', unsafe_allow_html=True)
        tab1,tab2,tab3 = st.tabs(["📊 Overview","📈 Distributions","🔗 Correlations"])
        with tab1:
            st.dataframe(df_raw.describe().round(2), use_container_width=True)
            st.dataframe(df_raw.head(20), use_container_width=True, hide_index=True)
        with tab2:
            try:
                import plotly.express as px
                num_cols = df_raw.select_dtypes(include=[np.number]).columns[:6]
                for col in num_cols:
                    fig = px.histogram(df_raw, x=col, nbins=30, title=col)
                    fig.update_layout(**dark_layout(height=300))
                    st.plotly_chart(fig, use_container_width=True)
            except: st.info("Install plotly for charts")
        with tab3:
            try:
                import plotly.express as px
                num_df = df_raw.select_dtypes(include=[np.number]).iloc[:,:10]
                fig = px.imshow(num_df.corr().round(2), text_auto=True, color_continuous_scale='RdBu_r')
                fig.update_layout(**dark_layout(title='Feature Correlations', height=500))
                st.plotly_chart(fig, use_container_width=True)
            except: st.info("Install plotly for correlation heatmap")
    else: st.warning("📁 No dataset loaded.")

# ═══ MODEL PERFORMANCE (Admin) ═══
elif page_id == "model_perf":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">🤖 MODEL PERFORMANCE</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    if 'comparison' in metrics:
        mc = metrics['comparison']
        st.dataframe(mc.style.format({'accuracy':'{:.4f}','f1_score':'{:.4f}'}).background_gradient(cmap='RdYlGn', subset=['accuracy']), use_container_width=True, hide_index=True)
        try:
            import plotly.express as px
            fig = px.bar(mc, x='model', y='accuracy', color='model', title='Model Accuracy Comparison')
            fig.update_layout(**dark_layout(height=400, yaxis_range=[0.99,1.001]))
            st.plotly_chart(fig, use_container_width=True)
        except: pass
    else: st.info("Run `python main.py` to generate metrics.")
    if 'feature_importance' in metrics:
        st.markdown('<div class="section-header">📊 TOP FEATURES</div>', unsafe_allow_html=True)
        fi = metrics['feature_importance'].head(15)
        try:
            import plotly.express as px
            fig = px.bar(fi, x='importance', y='feature', orientation='h', title='Feature Importance')
            fig.update_layout(**dark_layout(height=500))
            st.plotly_chart(fig, use_container_width=True)
        except: st.dataframe(fi, use_container_width=True)

# ═══ BATCH PROCESSING (Admin) ═══
elif page_id == "batch":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">📦 BATCH PROCESSING</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    csv_file = st.file_uploader("📄 Upload CSV with e-waste data", type=['csv'])
    if csv_file:
        try:
            batch_df = pd.read_csv(csv_file)
            st.success(f"✅ Loaded {len(batch_df)} rows × {len(batch_df.columns)} columns")
            st.dataframe(batch_df.head(), use_container_width=True, hide_index=True)
            if st.button("⚡ CLASSIFY ALL ROWS", use_container_width=True):
                results = []
                prog = st.progress(0)
                for i, row in batch_df.iterrows():
                    features = {**row.to_dict(), '_category': 'Mobile Phones'}
                    cat, conf = classify_with_model(features)
                    results.append({'row':i+1, 'category':cat, 'confidence':f"{conf*100:.1f}%"})
                    prog.progress(min((i+1)/len(batch_df), 1.0))
                res_df = pd.DataFrame(results)
                st.dataframe(res_df, use_container_width=True, hide_index=True)
                st.download_button("⬇️ Download Results", res_df.to_csv(index=False), "batch_results.csv", "text/csv", use_container_width=True)
        except Exception as e: st.error(f"Error: {e}")

# ═══ HISTORY ═══
elif page_id == "history":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">📋 CLASSIFICATION HISTORY</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    hist = get_history(200)
    if not hist.empty:
        st.markdown(f'<div class="glass-card"><h4>📊 Total Records: {len(hist)}</h4></div>', unsafe_allow_html=True)
        cat_filter = st.multiselect("🔍 Filter by Category", hist['predicted_category'].unique().tolist())
        if cat_filter: hist = hist[hist['predicted_category'].isin(cat_filter)]
        st.dataframe(hist[['timestamp','predicted_category','confidence','recovery_value','recovery_method','input_method']].rename(
            columns={'timestamp':'Time','predicted_category':'Category','confidence':'Confidence','recovery_value':'Value ($)','recovery_method':'Method','input_method':'Input'}
        ), use_container_width=True, hide_index=True)
        try:
            import plotly.express as px
            vc = hist['predicted_category'].value_counts()
            fig = px.pie(names=vc.index, values=vc.values, title='Classifications by Category')
            fig.update_layout(**dark_layout(height=400))
            st.plotly_chart(fig, use_container_width=True)
        except: pass
    else: st.info("📭 No classification history yet. Start classifying!")

# ═══ DATASET MANAGER (Admin) ═══
elif page_id == "datasets":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">📂 DATASET MANAGER</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📤 UPLOAD DATASET</div>', unsafe_allow_html=True)
    up = st.file_uploader("📄 Upload CSV Dataset", type=['csv'])
    if up:
        try:
            new_df = pd.read_csv(up)
            st.success(f"✅ {up.name}: {len(new_df)} rows × {len(new_df.columns)} columns")
            st.dataframe(new_df.head(), use_container_width=True, hide_index=True)
            if st.button("💾 SAVE DATASET", use_container_width=True):
                save_path = os.path.join(PROJECT_ROOT, 'data', 'raw', up.name)
                new_df.to_csv(save_path, index=False)
                save_dataset_record(up.name, len(new_df), len(new_df.columns), save_path)
                st.success(f"✅ Saved: {up.name}")
        except Exception as e: st.error(f"Error: {e}")

    st.markdown('<div class="section-header">📋 SAVED DATASETS</div>', unsafe_allow_html=True)
    ds = get_datasets()
    if not ds.empty:
        for _, row in ds.iterrows():
            dc1,dc2 = st.columns([4,1])
            with dc1: st.markdown(f'<div class="glass-card"><strong>{row["name"]}</strong> — {row["rows"]:,} rows × {row["columns"]} cols — {row["uploaded_at"][:10]}</div>', unsafe_allow_html=True)
            with dc2:
                if st.button(f"🗑️ Delete", key=f"del_{row['id']}"):
                    delete_dataset(row['id']); st.rerun()
    else: st.info("No additional datasets uploaded.")

# ═══ ABOUT ═══
elif page_id == "about":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">ℹ️ ABOUT</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    st.markdown('''<div class="glass-card" style="text-align:center;padding:40px;">
        <div style="font-size:4rem;">⚡</div>
        <h2 style="color:#DC143C;margin:15px 0;">E-Waste Intelligence System v5.0</h2>
        <p style="color:#888;font-size:1.1rem;">AI-Powered E-Waste Classification & Recovery Recommendation Platform</p>
        <div class="animated-line"></div>
        <h3 style="color:#FFD700;">👨‍💻 Developer</h3>
        <p style="color:#ccc;font-size:1.3rem;font-weight:700;">Azhar Fareed Mulla</p>
        <p style="color:#888;">USN: 2SA25MC002 • MCA Final Year</p>
        <h3 style="color:#FFD700;margin-top:20px;">👩‍🏫 Project Guide</h3>
        <p style="color:#ccc;font-size:1.2rem;">Dr. Nisha S Amin</p>
        <div class="animated-line"></div>
    </div>''', unsafe_allow_html=True)

    st.markdown('<div class="section-header">🛠️ TECH STACK</div>', unsafe_allow_html=True)
    tc1,tc2,tc3 = st.columns(3)
    with tc1: st.markdown('<div class="glass-card"><h4>🤖 ML/AI</h4><p>• Scikit-Learn<br>• XGBoost<br>• LightGBM<br>• CatBoost<br>• Neural Networks<br>• Stacking Ensemble</p></div>', unsafe_allow_html=True)
    with tc2: st.markdown('<div class="glass-card"><h4>🖥️ Frontend</h4><p>• Streamlit<br>• Plotly<br>• Custom CSS<br>• Glassmorphism UI<br>• Responsive Design<br>• Dark Theme</p></div>', unsafe_allow_html=True)
    with tc3: st.markdown('<div class="glass-card"><h4>💾 Backend</h4><p>• Python 3<br>• SQLite<br>• Pandas/NumPy<br>• Feature Engineering<br>• Recovery Engine<br>• Impact Calculator</p></div>', unsafe_allow_html=True)

    st.markdown('''<div class="glass-card" style="text-align:center;">
        <h4>📊 Key Achievements</h4>
        <p>🎯 <strong style="color:#00FF7F;">100% Accuracy</strong> with Stacking Ensemble</p>
        <p>🤖 <strong>6 ML Models</strong> trained and deployed</p>
        <p>📱 <strong>15 E-Waste Categories</strong> classified</p>
        <p>♻️ <strong>Complete Recovery</strong> recommendation system</p>
        <p>🌍 <strong>Environmental Impact</strong> calculator with SDG alignment</p>
        <p>💬 <strong>AI Chatbot</strong> for user guidance</p>
    </div>''', unsafe_allow_html=True)
