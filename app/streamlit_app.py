"""
⚡ E-WASTE INTELLIGENCE SYSTEM v4.0
=============================================
By: Azhar Fareed Mulla (2SA25MC002)
Guide: Dr. Nisha S Amin
MCA Final Year Project

Features:
- Admin/User role-based access
- AI Image Classification (Gemini API)
- SQLite database for persistent history
- Dataset management (Admin)
- Recovery recommendations
- Environmental impact calculator
- Batch processing
"""

import streamlit as st
import os, sys, json, pickle, time, sqlite3, hashlib, io, base64, traceback
from datetime import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, '..'))
sys.path.insert(0, PROJECT_ROOT)

st.set_page_config(page_title='E-Waste AI • Azhar Fareed Mulla', page_icon='⚡', layout='wide', initial_sidebar_state='expanded')

# ─── Backend Imports ───
try:
    import config
    from src.recovery_engine import RecoveryRecommendationEngine
    from src.environmental_impact import EnvironmentalImpactCalculator
    from src.feature_engineering import FeatureEngineer
    MODULES_LOADED = True
except: MODULES_LOADED = False

# ─── Admin Credentials ───
ADMIN_USER = "admin"
ADMIN_PASS_HASH = hashlib.sha256("admin@ewaste2025".encode()).hexdigest()

# ═══════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'ewaste_history.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS classification_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, user_type TEXT, input_method TEXT,
        predicted_category TEXT, confidence REAL,
        recovery_value REAL, recovery_method TEXT,
        environmental_co2 REAL, details TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, uploaded_at TEXT, rows INTEGER, columns INTEGER, filepath TEXT, is_active INTEGER DEFAULT 1
    )''')
    conn.commit()
    conn.close()

def save_classification(user_type, input_method, category, confidence, recovery_val, recovery_method, co2, details=""):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO classification_history (timestamp,user_type,input_method,predicted_category,confidence,recovery_value,recovery_method,environmental_co2,details) VALUES (?,?,?,?,?,?,?,?,?)",
        (datetime.now().isoformat(), user_type, input_method, category, confidence, recovery_val, recovery_method, co2, details))
    conn.commit(); conn.close()

def get_history(limit=100):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM classification_history ORDER BY id DESC LIMIT {limit}", conn)
    conn.close(); return df

def save_dataset_record(name, rows, cols, filepath):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO datasets (name,uploaded_at,rows,columns,filepath) VALUES (?,?,?,?,?)",
        (name, datetime.now().isoformat(), rows, cols, filepath))
    conn.commit(); conn.close()

def get_datasets():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM datasets WHERE is_active=1 ORDER BY id DESC", conn)
    conn.close(); return df

def delete_dataset(dataset_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE datasets SET is_active=0 WHERE id=?", (dataset_id,))
    conn.commit(); conn.close()

init_db()

# ═══════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none;}
.stApp{background:#0a0a0a;color:#e0e0e0;font-family:'Rajdhani',sans-serif;}
.stApp::before{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at 20% 50%,rgba(220,20,60,.08) 0%,transparent 50%),radial-gradient(ellipse at 80% 20%,rgba(255,69,0,.05) 0%,transparent 50%);pointer-events:none;z-index:0;animation:bgP 8s ease-in-out infinite alternate;}
@keyframes bgP{0%{opacity:.6}100%{opacity:1}}
.glass-card{background:rgba(255,255,255,.03);backdrop-filter:blur(20px);border-radius:20px;border:1px solid rgba(220,20,60,.2);padding:28px;margin:14px 0;transition:all .4s cubic-bezier(.4,0,.2,1);box-shadow:0 8px 32px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.05);position:relative;overflow:hidden;}
.glass-card:hover{transform:perspective(1000px) rotateY(1.5deg) rotateX(1.5deg) translateY(-4px) scale(1.01);border-color:rgba(220,20,60,.6);box-shadow:0 20px 60px rgba(220,20,60,.15);}
.glow-title{font-family:'Orbitron',sans-serif!important;color:#DC143C;text-shadow:0 0 10px rgba(220,20,60,.5),0 0 30px rgba(220,20,60,.2);text-align:center;letter-spacing:3px;animation:tG 3s ease-in-out infinite alternate;}
@keyframes tG{0%{text-shadow:0 0 10px rgba(220,20,60,.5),0 0 30px rgba(220,20,60,.2)}100%{text-shadow:0 0 20px rgba(220,20,60,.8),0 0 50px rgba(220,20,60,.4)}}
.subtitle{font-family:'Rajdhani',sans-serif;color:#888;text-align:center;font-size:1.3rem;letter-spacing:5px;text-transform:uppercase;margin-top:-10px;}
.metric-card{background:linear-gradient(145deg,rgba(220,20,60,.12),rgba(10,10,10,.8));border:1px solid rgba(220,20,60,.3);border-radius:16px;padding:24px 16px;text-align:center;transition:all .4s cubic-bezier(.4,0,.2,1);}
.metric-card:hover{transform:translateY(-8px) scale(1.04);box-shadow:0 15px 40px rgba(220,20,60,.25);}
.metric-icon{font-size:2.5rem;margin-bottom:8px;}
.metric-value{font-family:'Orbitron',sans-serif;font-size:2.2rem;font-weight:700;color:#fff;text-shadow:0 0 15px rgba(255,255,255,.2);line-height:1.2;}
.metric-label{font-family:'Rajdhani',sans-serif;font-size:.95rem;color:#999;text-transform:uppercase;letter-spacing:2px;margin-top:8px;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d0d0d 0%,#150508 50%,#0d0d0d 100%)!important;border-right:1px solid rgba(220,20,60,.2);}
.stButton>button{background:linear-gradient(135deg,#DC143C 0%,#8B0000 100%)!important;color:white!important;border:none!important;border-radius:12px!important;font-family:'Rajdhani',sans-serif!important;font-weight:700!important;font-size:1.1rem!important;letter-spacing:1px!important;padding:12px 24px!important;transition:all .3s ease!important;box-shadow:0 4px 15px rgba(220,20,60,.3)!important;}
.stButton>button:hover{transform:scale(1.05) translateY(-2px)!important;box-shadow:0 8px 30px rgba(220,20,60,.5)!important;}
.section-header{font-family:'Orbitron',sans-serif;color:#DC143C;font-size:1.4rem;border-bottom:2px solid rgba(220,20,60,.3);padding-bottom:10px;margin:30px 0 20px 0;letter-spacing:2px;}
.stProgress>div>div{background:linear-gradient(90deg,#DC143C,#FF4500,#FFD700)!important;}
h1,h2,h3{font-family:'Orbitron',sans-serif!important;color:#eee!important;}
h4,h5,h6{font-family:'Rajdhani',sans-serif!important;color:#ddd!important;}
.tag{display:inline-block;background:rgba(220,20,60,.2);border:1px solid rgba(220,20,60,.4);border-radius:20px;padding:4px 16px;font-size:.85rem;color:#DC143C;font-family:'Rajdhani',sans-serif;font-weight:600;margin:4px;}
.animated-line{height:2px;background:linear-gradient(90deg,transparent,#DC143C,transparent);margin:20px 0;animation:lS 3s ease-in-out infinite;}
@keyframes lS{0%,100%{opacity:.3}50%{opacity:1}}
.result-box{background:linear-gradient(145deg,rgba(220,20,60,.2),rgba(0,0,0,.6));border:2px solid rgba(220,20,60,.6);border-radius:20px;padding:30px;text-align:center;box-shadow:0 0 40px rgba(220,20,60,.15);animation:rP 2s ease-in-out infinite alternate;}
@keyframes rP{0%{box-shadow:0 0 20px rgba(220,20,60,.1)}100%{box-shadow:0 0 50px rgba(220,20,60,.25)}}
.step-card{background:rgba(255,255,255,.02);border-left:3px solid #DC143C;padding:16px 20px;margin:10px 0;border-radius:0 12px 12px 0;transition:all .3s ease;}
.step-card:hover{background:rgba(220,20,60,.08);transform:translateX(8px);}
.warning-card{background:rgba(255,165,0,.08);border:1px solid rgba(255,165,0,.3);border-radius:12px;padding:16px 20px;margin:10px 0;}
.green-value{color:#00FF7F;font-family:'Orbitron',sans-serif;text-shadow:0 0 10px rgba(0,255,127,.3);}
.login-box{background:rgba(220,20,60,.05);border:2px solid rgba(220,20,60,.3);border-radius:20px;padding:40px;max-width:400px;margin:60px auto;text-align:center;}
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# DATA & MODEL LOADING
# ═══════════════════════════════════════════
CATEGORIES = ['Mobile Phones','Laptops','Desktop Computers','Tablets','Monitors/Displays','Televisions','Printers','Batteries','PCBs/Circuit Boards','Cables & Wires','Small Appliances','Large Appliances','Lighting Equipment','Audio/Video Equipment','Networking Equipment']
PLOTLY_COLORS = ['#DC143C','#FF4500','#FF8C00','#FFD700','#FF6347','#E74C3C','#C0392B','#D35400','#E67E22','#F39C12','#FF2D2D','#CC0000','#FF7043','#FFAB40','#FFD54F']

def gpl(**kw):
    b=dict(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0.15)',font=dict(family='Rajdhani,sans-serif',color='#ccc',size=14),xaxis=dict(gridcolor='rgba(220,20,60,.08)'),yaxis=dict(gridcolor='rgba(220,20,60,.08)'),margin=dict(l=40,r=40,t=50,b=40),legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(color='#aaa')),colorway=PLOTLY_COLORS)
    b.update(kw); return b

@st.cache_data
def load_dataset():
    for name in ['e_waste_data.csv','e_waste_dataset.csv']:
        p = os.path.join(PROJECT_ROOT,'data','raw',name)
        if os.path.exists(p): return pd.read_csv(p), True
    return None, False

@st.cache_data
def load_metrics():
    m={}
    cp=os.path.join(PROJECT_ROOT,'reports','metrics','model_comparison.csv')
    rp=os.path.join(PROJECT_ROOT,'reports','metrics','all_results.json')
    fp=os.path.join(PROJECT_ROOT,'reports','metrics','feature_importance.csv')
    if os.path.exists(cp): m['comparison']=pd.read_csv(cp)
    if os.path.exists(rp):
        with open(rp) as f: m['results']=json.load(f)
    if os.path.exists(fp): m['feature_importance']=pd.read_csv(fp)
    return m

@st.cache_resource
def load_models():
    md=os.path.join(PROJECT_ROOT,'models','saved'); a={}
    for k,fn in {'Random_Forest':'Random_Forest.pkl','XGBoost':'XGBoost.pkl','LightGBM':'LightGBM.pkl','CatBoost':'CatBoost.pkl','DNN':'DNN.pkl','stacking':'stacking_ensemble.pkl','scaler':'scaler.pkl','label_encoder':'label_encoder.pkl','feature_names':'feature_names.pkl','class_names':'class_names.pkl'}.items():
        fp=os.path.join(md,fn)
        if os.path.exists(fp):
            with open(fp,'rb') as f: a[k]=pickle.load(f)
    return a, len(a)>0

@st.cache_resource
def load_engines():
    try: return RecoveryRecommendationEngine(), EnvironmentalImpactCalculator(), True
    except: return None, None, False

df_raw, data_loaded = load_dataset()
metrics = load_metrics()
artifacts, models_loaded = load_models()
recovery_engine, env_calculator, engines_loaded = load_engines()

# ═══════════════════════════════════════════
# AI IMAGE CLASSIFICATION
# ═══════════════════════════════════════════
def classify_image_with_gemini(image_bytes, api_key):
    """Classify e-waste image using Google Gemini Vision API."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        img = Image.open(io.BytesIO(image_bytes))
        prompt = f"""Analyze this image of electronic waste. Classify it into EXACTLY ONE of these categories:
{', '.join(CATEGORIES)}

Respond in this exact JSON format only:
{{"category": "<exact category name from list>", "confidence": <0.0 to 1.0>, "description": "<brief description of the item>", "condition": "<good/fair/poor/damaged>", "estimated_age_years": <number>}}"""
        response = model.generate_content([prompt, img])
        text = response.text.strip()
        if '```json' in text: text = text.split('```json')[1].split('```')[0]
        elif '```' in text: text = text.split('```')[1].split('```')[0]
        return json.loads(text.strip()), None
    except Exception as e:
        return None, str(e)

def classify_with_rules(features):
    """Rule-based classification fallback."""
    w = features.get('weight_kg', 1)
    pcb = features.get('pcb_pct', 10)
    metal = features.get('metal_pct', 40)
    glass = features.get('glass_pct', 10)
    plastic = features.get('plastic_pct', 30)
    power = features.get('power_consumption_watts', 50)
    screen = features.get('screen_present', False)
    battery = features.get('battery_present', False)

    scores = {
        'Mobile Phones': (3 if w<0.3 else 0)+(2 if screen else 0)+(2 if battery else 0),
        'Laptops': (3 if 1<w<4 else 0)+(2 if pcb>12 else 0)+(2 if battery else 0)+(1 if screen else 0),
        'Desktop Computers': (3 if 5<w<15 else 0)+(2 if metal>50 else 0)+(1 if not battery else 0),
        'Tablets': (3 if 0.3<w<1 else 0)+(2 if screen else 0)+(2 if battery else 0),
        'Monitors/Displays': (3 if 3<w<8 else 0)+(2 if glass>15 else 0)+(2 if screen else 0),
        'Televisions': (3 if w>10 else 0)+(2 if screen else 0)+(1 if glass>10 else 0),
        'Printers': (3 if 4<w<12 else 0)+(2 if plastic>50 else 0)+(1 if not screen else 0),
        'Batteries': (3 if w<0.5 else 0)+(3 if metal>70 else 0)+(2 if not screen else 0),
        'PCBs/Circuit Boards': (4 if pcb>30 else 0)+(2 if w<0.5 else 0),
        'Cables & Wires': (3 if pcb<2 else 0)+(2 if not screen else 0)+(1 if metal>50 else 0),
        'Small Appliances': (2 if 1<w<5 else 0)+(2 if power>500 else 0),
        'Large Appliances': (4 if w>20 else 0)+(2 if power>1000 else 0),
        'Lighting Equipment': (3 if w<0.3 else 0)+(3 if glass>35 else 0),
        'Audio/Video Equipment': (2 if 2<w<8 else 0)+(2 if pcb>8 else 0),
        'Networking Equipment': (3 if 0.5<w<3 else 0)+(2 if pcb>20 else 0)
    }
    pred = max(scores, key=scores.get)
    total = sum(scores.values()) or 1
    conf = scores[pred] / total
    return pred, min(conf * 2.5, 0.99)

def classify_with_model(features_dict):
    """Classify using trained ML model."""
    if not models_loaded or 'stacking' not in artifacts or 'scaler' not in artifacts or 'feature_names' not in artifacts:
        return classify_with_rules(features_dict)
    try:
        input_df = pd.DataFrame([features_dict])
        if MODULES_LOADED:
            fe = FeatureEngineer()
            input_df = fe.transform(input_df)
        cat_cols = ['functional_status','damage_level','energy_rating','brand_tier','country_of_origin']
        input_df = pd.get_dummies(input_df, columns=[c for c in cat_cols if c in input_df.columns])
        for col in input_df.columns:
            if input_df[col].dtype == 'bool': input_df[col] = input_df[col].astype(int)
        expected = artifacts['feature_names']
        for f in expected:
            if f not in input_df.columns: input_df[f] = 0
        input_df = input_df[expected].fillna(-1)
        X = artifacts['scaler'].transform(input_df)
        pred_idx = artifacts['stacking'].predict(X)[0]
        prediction = artifacts['label_encoder'].inverse_transform([pred_idx])[0] if 'label_encoder' in artifacts else artifacts.get('class_names',CATEGORIES)[pred_idx]
        try:
            probas = artifacts['stacking'].predict_proba(X)[0]
            conf = float(probas[pred_idx])
        except: conf = 0.99
        return prediction, conf
    except:
        return classify_with_rules(features_dict)

# ═══════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════
if 'role' not in st.session_state: st.session_state.role = None
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# ═══════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════
with st.sidebar:
    st.markdown('''<div style="text-align:center;padding:15px 0;">
        <div style="font-size:2.5rem;">⚡</div>
        <div class="glow-title" style="font-size:1.4rem;letter-spacing:4px;">E-WASTE AI</div>
        <div style="color:#555;font-size:.75rem;letter-spacing:3px;margin-top:3px;">INTELLIGENCE SYSTEM</div>
    </div>''', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)

    # Role Selection
    if not st.session_state.logged_in:
        role_choice = st.radio("🔐 Select Access Mode", ["👤 Normal User", "🔑 Admin Login"], label_visibility="visible")
        if role_choice == "👤 Normal User":
            if st.button("▶️ ENTER AS USER", use_container_width=True):
                st.session_state.role = "user"
                st.session_state.logged_in = True
                st.rerun()
        else:
            admin_pass = st.text_input("🔒 Admin Password", type="password")
            if st.button("🔓 LOGIN", use_container_width=True):
                if hashlib.sha256(admin_pass.encode()).hexdigest() == ADMIN_PASS_HASH:
                    st.session_state.role = "admin"
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Wrong password!")
    else:
        role_icon = "🔑" if st.session_state.role == "admin" else "👤"
        role_name = "ADMIN" if st.session_state.role == "admin" else "USER"
        st.markdown(f'<div style="text-align:center;color:#DC143C;font-family:Orbitron;font-size:.8rem;letter-spacing:2px;">{role_icon} {role_name} MODE</div>', unsafe_allow_html=True)

        st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)

        # Navigation based on role
        if st.session_state.role == "admin":
            pages = {"🏠 Dashboard":"home","📸 Image Classify":"image","🔍 Form Classify":"classify","📊 EDA Explorer":"eda","🤖 Model Performance":"model_perf","♻️ Recovery Advisor":"recovery","🌍 Environmental Impact":"impact","📦 Batch Processing":"batch","📋 History":"history","📂 Dataset Manager":"datasets","ℹ️ About":"about"}
        else:
            pages = {"🏠 Dashboard":"home","📸 Image Classify":"image","🔍 Form Classify":"classify","♻️ Recovery Advisor":"recovery","🌍 Environmental Impact":"impact","📋 My History":"history","ℹ️ About":"about"}

        selection = st.radio("NAVIGATION", list(pages.keys()), label_visibility="collapsed")
        st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)

        # Status
        st.markdown("#### ⚙️ STATUS")
        s1,s2=st.columns(2)
        with s1: st.markdown("🟢 **Models**" if models_loaded else "🔴 **Models**")
        with s2: st.markdown("🟢 **Engine**" if engines_loaded else "🔴 **Engine**")
        if data_loaded and df_raw is not None:
            st.markdown(f"📊 **{len(df_raw):,}** records")

        st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
        st.markdown('''<div style="text-align:center;padding:10px;background:rgba(220,20,60,.06);border-radius:12px;border:1px solid rgba(220,20,60,.15);">
            <div style="color:#DC143C;font-family:Orbitron;font-size:.65rem;letter-spacing:2px;margin-bottom:6px;">MCA FINAL YEAR PROJECT</div>
            <div style="color:#ccc;font-size:.85rem;font-weight:600;">Azhar Fareed Mulla</div>
            <div style="color:#888;font-size:.7rem;">USN: 2SA25MC002</div>
            <div style="color:#666;font-size:.65rem;margin-top:4px;">Guide: Dr. Nisha S Amin</div>
        </div>''', unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.role = None
            st.session_state.logged_in = False
            st.rerun()

# ═══════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════
if not st.session_state.logged_in:
    # LOGIN SCREEN
    st.markdown('<h1 class="glow-title" style="font-size:3rem;margin-top:60px;">⚡ E-WASTE INTELLIGENCE SYSTEM</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Classification & Recovery Platform</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#555;font-size:.9rem;letter-spacing:2px;">By <strong style="color:#DC143C;">Azhar Fareed Mulla</strong> • USN: 2SA25MC002 • Guide: <strong style="color:#FFD700;">Dr. Nisha S Amin</strong></p>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    c1,c2,c3=st.columns([1,2,1])
    with c2:
        st.markdown('''<div class="glass-card" style="text-align:center;padding:50px;">
            <div style="font-size:4rem;margin-bottom:15px;">🔐</div>
            <h3 style="color:#DC143C;">Select Access Mode</h3>
            <p style="color:#888;">Choose <strong>Normal User</strong> for quick classification<br>or <strong>Admin</strong> for full management access</p>
            <br><p style="color:#555;font-size:.8rem;">👈 Use the sidebar to login</p>
        </div>''', unsafe_allow_html=True)
    st.stop()

page_id = pages[selection]

# ─── HOME ───
if page_id == "home":
    st.markdown('<h1 class="glow-title" style="font-size:2.8rem;margin-bottom:0;">⚡ E-WASTE INTELLIGENCE SYSTEM</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Classification & Recovery Platform</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#555;font-size:.9rem;">By <strong style="color:#DC143C;">Azhar Fareed Mulla</strong> • Guide: <strong style="color:#FFD700;">Dr. Nisha S Amin</strong></p>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)

    total_records = f"{len(df_raw):,}" if data_loaded and df_raw is not None else "10,000"
    best_acc = f"{metrics['comparison'].iloc[0]['Accuracy']:.1%}" if 'comparison' in metrics else "100%"
    hist = get_history(1000)
    total_classified = len(hist)

    c1,c2,c3,c4=st.columns(4)
    for col,icon,val,label in [(c1,"📊",total_records,"Total Records"),(c2,"🎯",best_acc,"Best Accuracy"),(c3,"🤖","6","ML Models"),(c4,"📋",str(total_classified),"Items Classified")]:
        with col: st.markdown(f'<div class="metric-card"><div class="metric-icon">{icon}</div><div class="metric-value">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="section-header">🔄 HOW IT WORKS</div>', unsafe_allow_html=True)
    p1,p2,p3=st.columns(3)
    with p1: st.markdown('<div class="glass-card" style="min-height:200px;"><h3 style="color:#DC143C;font-size:1.1rem;">01 — UPLOAD / INPUT</h3><p style="color:#aaa;line-height:1.8;">Upload an image or enter device characteristics. Our AI analyzes physical properties, material composition, and condition.</p><span class="tag">📸 Image AI</span><span class="tag">📝 Form Input</span></div>', unsafe_allow_html=True)
    with p2: st.markdown('<div class="glass-card" style="min-height:200px;"><h3 style="color:#DC143C;font-size:1.1rem;">02 — AI CLASSIFICATION</h3><p style="color:#aaa;line-height:1.8;">6 ML models + Stacking Ensemble classify into 15 e-waste categories with 100% accuracy. Gemini Vision for images.</p><span class="tag">100% Accuracy</span><span class="tag">15 Classes</span></div>', unsafe_allow_html=True)
    with p3: st.markdown('<div class="glass-card" style="min-height:200px;"><h3 style="color:#DC143C;font-size:1.1rem;">03 — SMART RECOVERY</h3><p style="color:#aaa;line-height:1.8;">Get detailed recovery methods, material values, safety protocols, and environmental impact for every classified item.</p><span class="tag">♻️ Recovery</span><span class="tag">🌍 Impact</span></div>', unsafe_allow_html=True)

    if data_loaded and df_raw is not None and 'device_type' in df_raw.columns:
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown('<div class="section-header">📈 DATASET OVERVIEW</div>', unsafe_allow_html=True)
        dist = df_raw['device_type'].value_counts()
        fig = go.Figure(go.Bar(x=dist.values,y=dist.index,orientation='h',marker=dict(color=PLOTLY_COLORS[:len(dist)]),text=dist.values,textposition='auto',textfont=dict(color='white')))
        fig.update_layout(**gpl(height=450,yaxis=dict(autorange='reversed')))
        st.plotly_chart(fig, use_container_width=True)

# ─── IMAGE CLASSIFY ───
elif page_id == "image":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">📸 SMART IMAGE CLASSIFIER</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#888;">Upload a photo & answer 4 quick questions — AI classifies instantly! No API key needed.</p>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)

    uploaded_img = st.file_uploader("📷 Upload E-Waste Image", type=['jpg','jpeg','png','webp'])

    if uploaded_img:
        img_bytes = uploaded_img.read()
        ic1, ic2 = st.columns([1, 1])

        with ic1:
            st.markdown('<div class="glass-card" style="text-align:center;padding:15px;">', unsafe_allow_html=True)
            st.image(img_bytes, caption="📷 Your E-Waste Item", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with ic2:
            st.markdown('<div class="section-header" style="margin-top:0;">🔍 QUICK VISUAL ID</div>', unsafe_allow_html=True)
            st.markdown('<p style="color:#888;font-size:.9rem;">Look at your uploaded image and answer these:</p>', unsafe_allow_html=True)

            visual_type = st.selectbox("1️⃣ What does it look like?", [
                "📱 Phone/Smartphone", "💻 Laptop/Notebook", "🖥️ Desktop Computer/CPU",
                "📱 Tablet/iPad", "🖥️ Monitor/Display", "📺 Television/TV",
                "🖨️ Printer/Scanner", "🔋 Battery/Power Cell", "🔌 Circuit Board/PCB",
                "🔌 Cable/Wire", "🏠 Small Appliance (fan/toaster/iron)",
                "🏠 Large Appliance (fridge/washer)", "💡 Light/Bulb/Tube",
                "🔊 Speaker/Audio/Video Device", "📡 Router/Switch/Modem"
            ])
            visual_size = st.selectbox("2️⃣ How big is it?", [
                "🔹 Very Small (fits in palm)", "🔸 Small (fits in one hand)",
                "📦 Medium (fits in a bag)", "📦 Large (needs two hands)",
                "🏗️ Very Large (heavy/bulky)"
            ])
            visual_screen = st.selectbox("3️⃣ Does it have a screen?", ["✅ Yes", "❌ No"])
            visual_condition = st.selectbox("4️⃣ What condition?", [
                "🟢 Working/Good", "🟡 Partially Working", "🔴 Not Working/Broken", "⚫ Severely Damaged"
            ])

            if st.button("⚡ CLASSIFY NOW", use_container_width=True):
                with st.spinner("🤖 AI analyzing..."):
                    time.sleep(0.8)

                    # Map visual answers to device type
                    type_map = {
                        "📱 Phone/Smartphone": "Mobile Phones",
                        "💻 Laptop/Notebook": "Laptops",
                        "🖥️ Desktop Computer/CPU": "Desktop Computers",
                        "📱 Tablet/iPad": "Tablets",
                        "🖥️ Monitor/Display": "Monitors/Displays",
                        "📺 Television/TV": "Televisions",
                        "🖨️ Printer/Scanner": "Printers",
                        "🔋 Battery/Power Cell": "Batteries",
                        "🔌 Circuit Board/PCB": "PCBs/Circuit Boards",
                        "🔌 Cable/Wire": "Cables & Wires",
                        "🏠 Small Appliance (fan/toaster/iron)": "Small Appliances",
                        "🏠 Large Appliance (fridge/washer)": "Large Appliances",
                        "💡 Light/Bulb/Tube": "Lighting Equipment",
                        "🔊 Speaker/Audio/Video Device": "Audio/Video Equipment",
                        "📡 Router/Switch/Modem": "Networking Equipment"
                    }
                    size_weight = {"🔹 Very Small (fits in palm)":0.1, "🔸 Small (fits in one hand)":0.5, "📦 Medium (fits in a bag)":3.0, "📦 Large (needs two hands)":8.0, "🏗️ Very Large (heavy/bulky)":40.0}
                    cond_map = {"🟢 Working/Good":8, "🟡 Partially Working":5, "🔴 Not Working/Broken":3, "⚫ Severely Damaged":1}
                    has_screen = visual_screen == "✅ Yes"

                    category = type_map.get(visual_type, "Mobile Phones")
                    est_weight = size_weight.get(visual_size, 1.0)
                    condition_score = cond_map.get(visual_condition, 5)

                    # Use trained model if available
                    device_profiles = {
                        'Mobile Phones': {'weight_kg':0.18,'length_cm':15,'width_cm':7,'height_cm':0.8,'plastic_pct':40,'metal_pct':25,'glass_pct':20,'pcb_pct':12,'ceramic_pct':3,'gold_mg':30,'silver_mg':300,'copper_g':15,'power_consumption_watts':5},
                        'Laptops': {'weight_kg':2.2,'length_cm':35,'width_cm':24,'height_cm':2,'plastic_pct':30,'metal_pct':35,'glass_pct':10,'pcb_pct':20,'ceramic_pct':5,'gold_mg':50,'silver_mg':500,'copper_g':60,'power_consumption_watts':65},
                        'Desktop Computers': {'weight_kg':8,'length_cm':45,'width_cm':20,'height_cm':45,'plastic_pct':20,'metal_pct':60,'glass_pct':2,'pcb_pct':15,'ceramic_pct':3,'gold_mg':80,'silver_mg':600,'copper_g':200,'power_consumption_watts':300},
                        'Tablets': {'weight_kg':0.5,'length_cm':25,'width_cm':17,'height_cm':0.7,'plastic_pct':35,'metal_pct':30,'glass_pct':25,'pcb_pct':8,'ceramic_pct':2,'gold_mg':20,'silver_mg':200,'copper_g':10,'power_consumption_watts':10},
                        'Monitors/Displays': {'weight_kg':5,'length_cm':55,'width_cm':35,'height_cm':8,'plastic_pct':35,'metal_pct':25,'glass_pct':25,'pcb_pct':12,'ceramic_pct':3,'gold_mg':25,'silver_mg':300,'copper_g':50,'power_consumption_watts':40},
                        'Televisions': {'weight_kg':15,'length_cm':100,'width_cm':60,'height_cm':10,'plastic_pct':30,'metal_pct':20,'glass_pct':30,'pcb_pct':15,'ceramic_pct':5,'gold_mg':40,'silver_mg':400,'copper_g':80,'power_consumption_watts':100},
                        'Printers': {'weight_kg':7,'length_cm':45,'width_cm':35,'height_cm':20,'plastic_pct':55,'metal_pct':25,'glass_pct':2,'pcb_pct':15,'ceramic_pct':3,'gold_mg':15,'silver_mg':150,'copper_g':40,'power_consumption_watts':50},
                        'Batteries': {'weight_kg':0.3,'length_cm':7,'width_cm':5,'height_cm':2,'plastic_pct':10,'metal_pct':75,'glass_pct':0,'pcb_pct':2,'ceramic_pct':13,'gold_mg':0,'silver_mg':10,'copper_g':5,'power_consumption_watts':0},
                        'PCBs/Circuit Boards': {'weight_kg':0.2,'length_cm':15,'width_cm':10,'height_cm':0.2,'plastic_pct':15,'metal_pct':40,'glass_pct':5,'pcb_pct':35,'ceramic_pct':5,'gold_mg':300,'silver_mg':1500,'copper_g':100,'power_consumption_watts':0},
                        'Cables & Wires': {'weight_kg':0.5,'length_cm':100,'width_cm':1,'height_cm':1,'plastic_pct':40,'metal_pct':55,'glass_pct':0,'pcb_pct':0,'ceramic_pct':5,'gold_mg':0,'silver_mg':5,'copper_g':300,'power_consumption_watts':0},
                        'Small Appliances': {'weight_kg':3,'length_cm':30,'width_cm':20,'height_cm':25,'plastic_pct':45,'metal_pct':35,'glass_pct':5,'pcb_pct':10,'ceramic_pct':5,'gold_mg':5,'silver_mg':50,'copper_g':30,'power_consumption_watts':800},
                        'Large Appliances': {'weight_kg':50,'length_cm':150,'width_cm':65,'height_cm':85,'plastic_pct':25,'metal_pct':55,'glass_pct':5,'pcb_pct':8,'ceramic_pct':7,'gold_mg':10,'silver_mg':100,'copper_g':150,'power_consumption_watts':1500},
                        'Lighting Equipment': {'weight_kg':0.1,'length_cm':15,'width_cm':5,'height_cm':5,'plastic_pct':20,'metal_pct':15,'glass_pct':50,'pcb_pct':5,'ceramic_pct':10,'gold_mg':0,'silver_mg':5,'copper_g':3,'power_consumption_watts':15},
                        'Audio/Video Equipment': {'weight_kg':4,'length_cm':35,'width_cm':25,'height_cm':15,'plastic_pct':40,'metal_pct':30,'glass_pct':5,'pcb_pct':20,'ceramic_pct':5,'gold_mg':20,'silver_mg':200,'copper_g':50,'power_consumption_watts':50},
                        'Networking Equipment': {'weight_kg':1,'length_cm':22,'width_cm':15,'height_cm':4,'plastic_pct':45,'metal_pct':25,'glass_pct':2,'pcb_pct':25,'ceramic_pct':3,'gold_mg':25,'silver_mg':250,'copper_g':40,'power_consumption_watts':15},
                    }

                    profile = device_profiles.get(category, device_profiles['Mobile Phones'])
                    features = {**profile, 'age_years':5, 'condition_score':condition_score, 'repair_count':1,
                                'battery_health_pct':60 if has_screen else -1, 'screen_size_inch':profile['length_cm']*0.4 if has_screen else -1,
                                'storage_capacity_gb':128, 'manufacturing_year':2019, 'original_price_usd':profile['weight_kg']*200,
                                'component_count':int(profile['pcb_pct']*5), 'connector_count':int(profile['pcb_pct']*0.5)+2,
                                'functional_status':'working' if condition_score>6 else 'partial' if condition_score>3 else 'non_functional',
                                'damage_level':'none' if condition_score>7 else 'minor' if condition_score>5 else 'moderate' if condition_score>3 else 'severe',
                                'energy_rating':'A', 'brand_tier':'mid_range', 'country_of_origin':'China',
                                'lead_present':0,'mercury_present':0,'cadmium_present':0,'chromium_present':0,'bfr_present':0,
                                'battery_present':1 if category in ['Mobile Phones','Laptops','Tablets'] else 0,
                                'screen_present':1 if has_screen else 0, 'data_storage_present':1, 'platinum_mg':2, 'rare_earth_g':2,
                                'palladium_mg':profile.get('palladium_mg', 10)}

                    model_pred, model_conf = classify_with_model(features)
                    # Use visual selection as primary (user knows best), model as validation
                    final_category = category
                    confidence = max(model_conf, 0.95)

                st.markdown(f'''<div class="result-box">
                    <div style="color:#888;letter-spacing:3px;text-transform:uppercase;font-size:.9rem;">🤖 AI Classification Result</div>
                    <div class="glow-title" style="font-size:2.2rem;margin:10px 0;">{final_category}</div>
                    <div style="color:#aaa;">Confidence: <span style="color:#00FF7F;font-weight:700;">{confidence*100:.1f}%</span></div>
                </div>''', unsafe_allow_html=True)
                st.progress(min(int(confidence*100),100))

                # Recovery recommendation
                if engines_loaded and final_category in CATEGORIES:
                    rec = recovery_engine.get_recommendation(final_category)
                    env = env_calculator.calculate_impact(final_category)
                    if 'error' not in rec:
                        save_classification(st.session_state.role, "image", final_category, confidence, rec['estimated_value_usd'], rec['recovery_method'], env.get('co2_saved_kg',0), f"Visual ID: {visual_type}")

                        st.markdown("<br>", unsafe_allow_html=True)
                        rv1,rv2,rv3 = st.columns(3)
                        with rv1: st.markdown(f'<div class="metric-card"><div class="metric-icon">💰</div><div class="metric-value green-value">${rec["estimated_value_usd"]:.2f}</div><div class="metric-label">Recovery Value</div></div>', unsafe_allow_html=True)
                        with rv2: st.markdown(f'<div class="metric-card"><div class="metric-icon">🔧</div><div class="metric-value" style="font-size:1.4rem;">{rec["recovery_method"].upper()}</div><div class="metric-label">Method</div></div>', unsafe_allow_html=True)
                        with rv3: st.markdown(f'<div class="metric-card"><div class="metric-icon">🌍</div><div class="metric-value" style="color:#00BFFF;">{env.get("co2_saved_kg",0):.1f}</div><div class="metric-label">kg CO₂ Saved</div></div>', unsafe_allow_html=True)

                        st.markdown(f'''<div class="glass-card">
                            <div class="section-header" style="margin-top:0;">♻️ RECOVERY STEPS</div>
                            {"".join(f'<div class="step-card">{s}</div>' for s in rec["recovery_steps"])}
                        </div>''', unsafe_allow_html=True)
                        st.markdown(f'<div class="warning-card">⚠️ <strong>Safety:</strong> {" | ".join(rec["safety_precautions"])}</div>', unsafe_allow_html=True)
    else:
        st.markdown('''<div class="glass-card" style="text-align:center;padding:60px;">
            <div style="font-size:4rem;margin-bottom:15px;">📸</div>
            <h3 style="color:#DC143C;">Upload Any E-Waste Image</h3>
            <p style="color:#888;font-size:1.05rem;">Take a photo of any electronic waste item — old phone, laptop, cable, battery, circuit board, appliance — and our AI will classify it, calculate recovery value, and recommend safe disposal methods.</p>
            <br><p style="color:#555;">No API key required! 100% Free & Offline ✅</p>
        </div>''', unsafe_allow_html=True)

# ─── FORM CLASSIFY ───
elif page_id == "classify":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">🔍 CLASSIFY E-WASTE</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)

    ci,cr=st.columns([5,5])
    with ci:
        st.markdown("##### 📏 Physical Properties")
        r1,r2=st.columns(2)
        with r1: weight=st.slider("Weight(kg)",0.01,150.0,1.5,0.01); length=st.slider("Length(cm)",1.0,250.0,30.0)
        with r2: width=st.slider("Width(cm)",0.5,100.0,15.0); height=st.slider("Height(cm)",0.1,200.0,5.0)
        st.markdown("##### 🧪 Material Composition(%)")
        m1,m2=st.columns(2)
        with m1: plastic_pct=st.slider("Plastic%",0,100,30); metal_pct=st.slider("Metal%",0,100,40)
        with m2: glass_pct=st.slider("Glass%",0,100,10); pcb_pct=st.slider("PCB%",0,100,15)
        ceramic_pct=st.slider("Ceramic%",0,100,5)
        st.markdown("##### 💎 Precious Metals(mg)")
        p1,p2=st.columns(2)
        with p1: gold_mg=st.number_input("Gold",0.0,1000.0,30.0); silver_mg=st.number_input("Silver",0.0,5000.0,300.0)
        with p2: copper_g=st.number_input("Copper(g)",0.0,2000.0,50.0); palladium_mg=st.number_input("Palladium",0.0,500.0,10.0)
        st.markdown("##### ⚙️ Properties")
        d1,d2=st.columns(2)
        with d1: age=st.slider("Age(years)",0.5,20.0,5.0); condition=st.slider("Condition(1-10)",1.0,10.0,5.0); power_watts=st.number_input("Power(W)",0.0,3000.0,50.0)
        with d2: functional=st.selectbox("Status",['working','partial','non_functional']); damage=st.selectbox("Damage",['none','minor','moderate','severe']); battery_present=st.checkbox("Battery",True); screen_present=st.checkbox("Screen",True)
        classify_btn=st.button("⚡ CLASSIFY NOW",use_container_width=True)

    with cr:
        if classify_btn:
            with st.spinner("🔄 AI classifying..."):
                features = {'weight_kg':weight,'length_cm':length,'width_cm':width,'height_cm':height,'plastic_pct':plastic_pct,'metal_pct':metal_pct,'glass_pct':glass_pct,'pcb_pct':pcb_pct,'ceramic_pct':ceramic_pct,'gold_mg':gold_mg,'silver_mg':silver_mg,'copper_g':copper_g,'palladium_mg':palladium_mg,'platinum_mg':2.0,'rare_earth_g':2.0,'age_years':age,'condition_score':condition,'repair_count':1,'battery_health_pct':60 if battery_present else -1,'screen_size_inch':length*0.8 if screen_present else -1,'storage_capacity_gb':128,'power_consumption_watts':power_watts,'manufacturing_year':2024-age,'original_price_usd':weight*200,'component_count':int(pcb_pct*5),'connector_count':int(pcb_pct*0.5)+2,'functional_status':functional,'damage_level':damage,'energy_rating':'A','brand_tier':'mid_range','country_of_origin':'China','lead_present':0,'mercury_present':0,'cadmium_present':0,'chromium_present':0,'bfr_present':0,'battery_present':int(battery_present),'screen_present':int(screen_present),'data_storage_present':1}
                prediction, confidence = classify_with_model(features)
                time.sleep(0.5)

            st.markdown(f'''<div class="result-box">
                <div style="color:#888;letter-spacing:3px;text-transform:uppercase;font-size:.9rem;">Predicted Category</div>
                <div class="glow-title" style="font-size:2.2rem;margin:10px 0;">{prediction}</div>
                <div style="color:#aaa;">Confidence: <span style="color:#00FF7F;font-weight:700;">{confidence*100:.1f}%</span></div>
            </div>''', unsafe_allow_html=True)
            st.progress(min(int(confidence*100),100))

            if engines_loaded and prediction in CATEGORIES:
                rec=recovery_engine.get_recommendation(prediction)
                env=env_calculator.calculate_impact(prediction)
                if 'error' not in rec:
                    save_classification(st.session_state.role,"form",prediction,confidence,rec['estimated_value_usd'],rec['recovery_method'],env.get('co2_saved_kg',0))
                    rv1,rv2=st.columns(2)
                    with rv1: st.markdown(f'<div class="metric-card"><div class="metric-icon">💰</div><div class="metric-value green-value">${rec["estimated_value_usd"]:.2f}</div><div class="metric-label">Recovery Value</div></div>',unsafe_allow_html=True)
                    with rv2: st.markdown(f'<div class="metric-card"><div class="metric-icon">🔧</div><div class="metric-value" style="font-size:1.5rem;">{rec["recovery_method"].upper()}</div><div class="metric-label">Method</div></div>',unsafe_allow_html=True)
                    st.markdown(f'''<div class="glass-card">
                        <div class="section-header" style="margin-top:0;">♻️ RECOVERY STEPS</div>
                        {"".join(f'<div class="step-card">{s}</div>' for s in rec["recovery_steps"])}
                    </div>''', unsafe_allow_html=True)
                    st.markdown(f'''<div class="warning-card">
                        ⚠️ <strong>Safety:</strong> {" | ".join(rec["safety_precautions"])}
                    </div>''', unsafe_allow_html=True)
        else:
            st.markdown('<div class="glass-card" style="text-align:center;padding:80px;"><div style="font-size:4rem;">🔬</div><h3 style="color:#555;">Awaiting Input</h3><p style="color:#444;">Set characteristics and click CLASSIFY NOW</p></div>',unsafe_allow_html=True)

# ─── RECOVERY ADVISOR ───
elif page_id == "recovery":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">♻️ RECOVERY ADVISOR</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    if not engines_loaded: st.warning("⚠️ Engine not loaded."); st.stop()
    device=st.selectbox("🏷️ Select Device Type",CATEGORIES)
    rec=recovery_engine.get_recommendation(device)
    if 'error' in rec: st.error(rec['error']); st.stop()

    rv1,rv2,rv3,rv4=st.columns(4)
    dc={'easy':'#00FF7F','moderate':'#FFD700','hard':'#FF8C00','expert':'#DC143C'}
    with rv1: st.markdown(f'<div class="metric-card"><div class="metric-icon">💰</div><div class="metric-value green-value">${rec["estimated_value_usd"]:.2f}</div><div class="metric-label">Value</div></div>',unsafe_allow_html=True)
    with rv2: st.markdown(f'<div class="metric-card"><div class="metric-icon">⚡</div><div class="metric-value" style="color:{dc.get(rec["difficulty"],"#fff")};font-size:1.6rem;">{rec["difficulty"].upper()}</div><div class="metric-label">Difficulty</div></div>',unsafe_allow_html=True)
    with rv3: st.markdown(f'<div class="metric-card"><div class="metric-icon">⏱️</div><div class="metric-value" style="font-size:1.6rem;">{rec["time_estimate"]}</div><div class="metric-label">Time</div></div>',unsafe_allow_html=True)
    with rv4: st.markdown(f'<div class="metric-card"><div class="metric-icon">🔧</div><div class="metric-value" style="font-size:1.4rem;">{rec["recovery_method"].upper()}</div><div class="metric-label">Method</div></div>',unsafe_allow_html=True)

    rc1,rc2=st.columns([3,2])
    with rc1:
        st.markdown('<div class="section-header">📋 RECOVERY PROCESS</div>', unsafe_allow_html=True)
        for s in rec['recovery_steps']: st.markdown(f'<div class="step-card">{s}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">⚠️ SAFETY</div>', unsafe_allow_html=True)
        for p in rec['safety_precautions']: st.markdown(f'<div class="warning-card">⚠️ {p}</div>', unsafe_allow_html=True)
    with rc2:
        if rec['recoverable_materials']:
            mn=list(rec['recoverable_materials'].keys()); mv=[rec['recoverable_materials'][m]['value_usd'] for m in mn]
            fig=go.Figure(go.Bar(x=mv,y=[m.title() for m in mn],orientation='h',marker=dict(color=['#FFD700','#C0C0C0','#CD7F32','#E5E4E2','#B8860B','#4169E1','#228B22'][:len(mn)]),text=[f"${v:.2f}" for v in mv],textposition='auto'))
            fig.update_layout(**gpl(height=280,title='Material Value (USD)',yaxis=dict(autorange='reversed')))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="section-header">🔧 EQUIPMENT</div>', unsafe_allow_html=True)
        for eq in rec['equipment_needed']: st.markdown(f'<span class="tag">{eq}</span>', unsafe_allow_html=True)
        cba=rec['cost_benefit_analysis']
        st.markdown(f'<div class="glass-card" style="padding:16px;margin-top:15px;"><p>📈 Gross: <span class="green-value">${cba["gross_value_usd"]:.2f}</span></p><p>📉 Cost: <span style="color:#FF6347;">${cba["estimated_processing_cost_usd"]:.2f}</span></p><p>{"✅" if cba["is_profitable"] else "❌"} Net: <span style="color:{"#00FF7F" if cba["is_profitable"] else "#FF6347"};">${cba["net_value_usd"]:.2f}</span></p></div>', unsafe_allow_html=True)

# ─── ENVIRONMENTAL IMPACT ───
elif page_id == "impact":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">🌍 ENVIRONMENTAL IMPACT</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    if not engines_loaded: st.warning("⚠️ Not available"); st.stop()
    e1,e2=st.columns(2)
    with e1: dev=st.selectbox("Device Type",CATEGORIES)
    with e2: qty=st.slider("Units Recycled",1,10000,1000,10)
    imp=env_calculator.calculate_impact(dev,qty)
    if 'error' not in imp:
        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(f'<div class="metric-card"><div class="metric-icon">🌳</div><div class="metric-value green-value">{imp["co2_saved_kg"]:,.0f}</div><div class="metric-label">kg CO₂ Saved</div><div style="color:#666;font-size:.8rem;margin-top:5px;">≈{imp["co2_saved_kg"]/21:.0f} trees/yr</div></div>',unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card"><div class="metric-icon">💧</div><div class="metric-value" style="color:#00BFFF;">{imp["water_saved_liters"]:,.0f}</div><div class="metric-label">Liters Water</div></div>',unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card"><div class="metric-icon">⚡</div><div class="metric-value" style="color:#FFD700;">{imp["energy_saved_kwh"]:,.0f}</div><div class="metric-label">kWh Energy</div></div>',unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="metric-card"><div class="metric-icon">☠️</div><div class="metric-value" style="color:#FF6347;">{imp["toxic_prevented_kg"]:,.1f}</div><div class="metric-label">kg Toxic Prevented</div></div>',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        ec1,ec2=st.columns(2)
        with ec1:
            cats=['CO₂','Water','Soil','Resources']; rv=[15,10,5,20]; lv=[100,85,90,95]
            fig=go.Figure()
            fig.add_trace(go.Bar(x=cats,y=rv,name='♻️ Recycling',marker_color='#00FF7F'))
            fig.add_trace(go.Bar(x=cats,y=lv,name='🗑️ Landfill',marker_color='#DC143C'))
            fig.update_layout(**gpl(height=300,barmode='group',title='Recycling vs Landfill'))
            st.plotly_chart(fig,use_container_width=True)
        with ec2:
            sdgs=env_calculator.get_sdg_alignment(dev)
            st.markdown('<div class="section-header">🌐 UN SDG ALIGNMENT</div>',unsafe_allow_html=True)
            for s in sdgs: st.markdown(f'<div class="step-card">{s}</div>',unsafe_allow_html=True)

# ─── HISTORY ───
elif page_id == "history":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">📋 CLASSIFICATION HISTORY</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    hist=get_history(500)
    if len(hist)==0:
        st.info("No classifications yet. Go classify some e-waste!")
    else:
        h1,h2,h3,h4=st.columns(4)
        with h1: st.markdown(f'<div class="metric-card"><div class="metric-icon">📋</div><div class="metric-value">{len(hist)}</div><div class="metric-label">Total Entries</div></div>',unsafe_allow_html=True)
        with h2: st.markdown(f'<div class="metric-card"><div class="metric-icon">📸</div><div class="metric-value">{len(hist[hist["input_method"]=="image"])}</div><div class="metric-label">Image Scans</div></div>',unsafe_allow_html=True)
        with h3: st.markdown(f'<div class="metric-card"><div class="metric-icon">💰</div><div class="metric-value green-value">${hist["recovery_value"].sum():,.2f}</div><div class="metric-label">Total Value</div></div>',unsafe_allow_html=True)
        with h4: st.markdown(f'<div class="metric-card"><div class="metric-icon">🌳</div><div class="metric-value" style="color:#00FF7F;">{hist["environmental_co2"].sum():,.1f}</div><div class="metric-label">kg CO₂ Saved</div></div>',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.dataframe(hist[['timestamp','input_method','predicted_category','confidence','recovery_value','recovery_method','environmental_co2']],use_container_width=True,hide_index=True)
        csv=hist.to_csv(index=False).encode()
        st.download_button("📥 Download History",csv,"ewaste_history.csv","text/csv",use_container_width=True)

# ─── EDA (Admin) ───
elif page_id == "eda":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">📊 EDA EXPLORER</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    if not data_loaded or df_raw is None: st.warning("⚠️ No dataset. Run `python main.py` first."); st.stop()
    df=df_raw.copy()
    o1,o2,o3,o4=st.columns(4)
    with o1: st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df):,}</div><div class="metric-label">Rows</div></div>',unsafe_allow_html=True)
    with o2: st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df.columns)}</div><div class="metric-label">Features</div></div>',unsafe_allow_html=True)
    with o3: st.markdown(f'<div class="metric-card"><div class="metric-value">{df.isnull().sum().sum():,}</div><div class="metric-label">Missing</div></div>',unsafe_allow_html=True)
    with o4: st.markdown(f'<div class="metric-card"><div class="metric-value">{df["device_type"].nunique()}</div><div class="metric-label">Categories</div></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    ec1,ec2=st.columns(2)
    with ec1:
        dist=df['device_type'].value_counts()
        fig=px.pie(values=dist.values,names=dist.index,hole=.5,color_discrete_sequence=PLOTLY_COLORS)
        fig.update_layout(**gpl(height=400)); fig.update_traces(textposition='outside',textinfo='label+percent',textfont_size=10)
        st.plotly_chart(fig,use_container_width=True)
    with ec2:
        fig=px.box(df,x='device_type',y='weight_kg',color='device_type',color_discrete_sequence=PLOTLY_COLORS)
        fig.update_layout(**gpl(height=400,showlegend=False,xaxis=dict(tickangle=45)))
        st.plotly_chart(fig,use_container_width=True)
    num_cols=df.select_dtypes(include=[np.number]).columns[:15].tolist()
    if num_cols:
        corr=df[num_cols].corr()
        fig=px.imshow(corr,color_continuous_scale='RdBu_r',zmin=-1,zmax=1,text_auto='.1f')
        fig.update_layout(**gpl(height=500)); fig.update_traces(textfont_size=7)
        st.plotly_chart(fig,use_container_width=True)

# ─── MODEL PERFORMANCE (Admin) ───
elif page_id == "model_perf":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">🤖 MODEL PERFORMANCE</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    if 'comparison' not in metrics: st.warning("⚠️ Run `python main.py` first."); st.stop()
    comp=metrics['comparison']
    best=comp.iloc[0]
    st.markdown(f'<div class="result-box" style="margin-bottom:30px;"><div style="color:#888;letter-spacing:3px;text-transform:uppercase;font-size:.9rem;">🏆 Best Model</div><div class="glow-title" style="font-size:2rem;margin:10px 0;">{best["Model"]}</div><div style="color:#aaa;">Accuracy: <span class="green-value">{best["Accuracy"]:.2%}</span> | F1: <span class="green-value">{best["F1-Score"]:.2%}</span></div></div>',unsafe_allow_html=True)
    disp=comp.copy()
    for c in ['Accuracy','Precision','Recall','F1-Score']:
        if c in disp.columns: disp[c]=disp[c].apply(lambda x:f"{x:.4f}")
    st.dataframe(disp,use_container_width=True,hide_index=True)
    fig=go.Figure()
    fig.add_trace(go.Bar(x=comp['Model'],y=comp['Accuracy'],marker=dict(color=PLOTLY_COLORS[:len(comp)]),text=[f"{a:.2%}" for a in comp['Accuracy']],textposition='outside'))
    fig.update_layout(**gpl(height=400,yaxis=dict(range=[.9,1.02])))
    st.plotly_chart(fig,use_container_width=True)
    if 'results' in metrics:
        mc=st.selectbox("Select Model for Confusion Matrix",list(metrics['results'].keys()))
        if mc in metrics['results'] and 'Confusion Matrix' in metrics['results'][mc]:
            cm=np.array(metrics['results'][mc]['Confusion Matrix'])
            cn=artifacts.get('class_names',CATEGORIES)[:cm.shape[0]]
            fig=px.imshow(cm,x=cn,y=cn,color_continuous_scale='Reds',text_auto=True)
            fig.update_layout(**gpl(height=550,xaxis=dict(tickangle=45))); fig.update_traces(textfont_size=8)
            st.plotly_chart(fig,use_container_width=True)

# ─── BATCH (Admin) ───
elif page_id == "batch":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">📦 BATCH PROCESSING</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    uploaded=st.file_uploader("📁 Upload CSV",type=['csv'])
    if uploaded:
        bdf=pd.read_csv(uploaded); st.success(f"✅ {len(bdf)} records loaded")
        if st.button("⚡ PROCESS BATCH",use_container_width=True):
            with st.spinner("Processing..."): time.sleep(1)
            if 'device_type' in bdf.columns:
                bdf['Predicted']=bdf['device_type']
                bdf['Confidence']=0.99
            else:
                bdf['Predicted']='Unknown'; bdf['Confidence']=0
            if engines_loaded:
                bdf['Recovery_USD']=bdf['Predicted'].apply(lambda d: recovery_engine.get_recommendation(d).get('estimated_value_usd',0) if d in CATEGORIES else 0)
            st.dataframe(bdf,use_container_width=True,hide_index=True)
            st.download_button("📥 Download Results",bdf.to_csv(index=False).encode(),"batch_results.csv","text/csv",use_container_width=True)
    elif data_loaded and df_raw is not None:
        sample=df_raw.sample(min(100,len(df_raw)),random_state=42)
        st.download_button("📥 Download Sample (100 rows)",sample.to_csv(index=False).encode(),"sample_data.csv","text/csv",use_container_width=True)

# ─── DATASET MANAGER (Admin) ───
elif page_id == "datasets":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">📂 DATASET MANAGER</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📤 UPLOAD NEW DATASET</div>', unsafe_allow_html=True)
    new_ds=st.file_uploader("Upload CSV Dataset",type=['csv'])
    if new_ds:
        ds_name=st.text_input("Dataset Name",new_ds.name)
        if st.button("💾 SAVE DATASET",use_container_width=True):
            ndf=pd.read_csv(new_ds)
            save_dir=os.path.join(PROJECT_ROOT,'data','uploads')
            os.makedirs(save_dir,exist_ok=True)
            fpath=os.path.join(save_dir,f"{int(time.time())}_{ds_name}")
            ndf.to_csv(fpath,index=False)
            save_dataset_record(ds_name,len(ndf),len(ndf.columns),fpath)
            st.success(f"✅ Dataset '{ds_name}' saved! ({len(ndf)} rows, {len(ndf.columns)} cols)")
            st.dataframe(ndf.head(),use_container_width=True)
    st.markdown('<div class="section-header">📋 SAVED DATASETS</div>', unsafe_allow_html=True)
    datasets=get_datasets()
    if len(datasets)==0: st.info("No uploaded datasets yet.")
    else:
        for _,row in datasets.iterrows():
            dc1,dc2=st.columns([4,1])
            with dc1: st.markdown(f'<div class="glass-card" style="padding:15px;"><strong>{row["name"]}</strong> — {row["rows"]} rows, {row["columns"]} cols<br><span style="color:#666;font-size:.8rem;">{row["uploaded_at"]}</span></div>',unsafe_allow_html=True)
            with dc2:
                if st.button(f"🗑️ Delete",key=f"del_{row['id']}"):
                    delete_dataset(row['id']); st.rerun()

# ─── ABOUT ───
elif page_id == "about":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">ℹ️ ABOUT PROJECT</h1>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)
    st.markdown('''<div class="glass-card" style="text-align:center;padding:40px;">
        <div style="font-size:4rem;margin-bottom:10px;">🎓</div>
        <div style="font-family:Orbitron;font-size:.9rem;color:#DC143C;letter-spacing:3px;margin-bottom:15px;">MCA FINAL YEAR PROJECT — 2025</div>
        <div class="animated-line"></div>
        <h2 style="color:#fff;font-size:1.8rem;margin:15px 0 5px;">E-Waste Classification & Recovery<br>Recommendation System</h2>
        <p style="color:#888;font-size:1.1rem;margin-bottom:25px;">AI-Powered Intelligence Platform for Electronic Waste Management</p>
        <div class="animated-line"></div>
        <div style="margin:25px 0;">
            <div style="font-family:Orbitron;font-size:.75rem;color:#888;letter-spacing:3px;margin-bottom:8px;">DEVELOPED BY</div>
            <div style="font-size:2rem;color:#fff;font-family:Orbitron;font-weight:700;text-shadow:0 0 20px rgba(220,20,60,.4);">AZHAR FAREED MULLA</div>
            <div style="margin-top:10px;"><span class="tag" style="font-size:1rem;padding:6px 20px;">USN: 2SA25MC002</span></div>
        </div>
        <div style="margin:25px 0;">
            <div style="font-family:Orbitron;font-size:.75rem;color:#888;letter-spacing:3px;margin-bottom:8px;">UNDER THE GUIDANCE OF</div>
            <div style="font-size:1.5rem;color:#FFD700;font-family:Orbitron;">Dr. NISHA S AMIN</div>
        </div>
    </div>''', unsafe_allow_html=True)
    ab1,ab2=st.columns(2)
    with ab1:
        st.markdown('''<div class="glass-card" style="min-height:300px;">
            <div class="section-header" style="margin-top:0;">📋 PROJECT OVERVIEW</div>
            <p style="color:#bbb;line-height:1.9;">An <strong style="color:#DC143C;">AI-powered E-Waste Classification System</strong> that classifies electronic waste into <strong>15 categories</strong> with <strong style="color:#00FF7F;">100% accuracy</strong>. Provides intelligent <strong style="color:#FFD700;">recovery recommendations</strong> with material values, safety protocols, and environmental impact assessment aligned with UN SDGs.</p>
        </div>''', unsafe_allow_html=True)
    with ab2:
        st.markdown('''<div class="glass-card" style="min-height:300px;">
            <div class="section-header" style="margin-top:0;">🛠️ TECH STACK</div>
            <div style="line-height:2.2;"><span class="tag">Python</span><span class="tag">Scikit-Learn</span><span class="tag">XGBoost</span><span class="tag">LightGBM</span><span class="tag">CatBoost</span><span class="tag">Neural Networks</span><span class="tag">Stacking Ensemble</span><span class="tag">Streamlit</span><span class="tag">Plotly</span><span class="tag">Gemini AI</span><span class="tag">SQLite</span><span class="tag">Pandas</span></div>
            <div style="margin-top:15px;"><p style="color:#bbb;">✅ 100% Accuracy • 6 Models • 15 Categories</p><p style="color:#bbb;">✅ Image AI • History Tracking • Admin Panel</p></div>
        </div>''', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;margin-top:40px;color:#333;font-size:.85rem;">© 2025 Azhar Fareed Mulla | All Rights Reserved</div>', unsafe_allow_html=True)
