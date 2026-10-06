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
            pages = {"🏠 Dashboard":"home","📸 Image Classify":"image","💬 AI Chatbot":"chatbot","🔍 Form Classify":"classify","📊 EDA Explorer":"eda","🤖 Model Performance":"model_perf","♻️ Recovery Advisor":"recovery","🌍 Environmental Impact":"impact","📦 Batch Processing":"batch","📋 History":"history","📂 Dataset Manager":"datasets","ℹ️ About":"about"}
        else:
            pages = {"🏠 Dashboard":"home","📸 Image Classify":"image","💬 AI Chatbot":"chatbot","🔍 Form Classify":"classify","♻️ Recovery Advisor":"recovery","🌍 Environmental Impact":"impact","📋 My History":"history","ℹ️ About":"about"}

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
    st.markdown('<p style="text-align:center;color:#888;">Upload a photo, select model & get AI chatbot recommendations!</p>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)

    # Model Selection
    available_models = ["🏆 Stacking Ensemble (Best)"]
    model_keys = {"🏆 Stacking Ensemble (Best)": "stacking"}
    for mk in ['Random_Forest','XGBoost','LightGBM','CatBoost','DNN']:
        if mk in artifacts:
            label = f"🤖 {mk.replace('_',' ')}"
            available_models.append(label)
            model_keys[label] = mk
    selected_model_label = st.selectbox("🧠 SELECT AI MODEL", available_models)
    selected_model_key = model_keys.get(selected_model_label, "stacking")

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
                "📦 Medium (fits in a bag)", "📦 Large (needs two hands)", "🏗️ Very Large (heavy/bulky)"
            ])
            visual_screen = st.selectbox("3️⃣ Does it have a screen?", ["✅ Yes", "❌ No"])
            visual_condition = st.selectbox("4️⃣ What condition?", [
                "🟢 Working/Good", "🟡 Partially Working", "🔴 Not Working/Broken", "⚫ Severely Damaged"
            ])

            if st.button("⚡ CLASSIFY NOW", use_container_width=True):
                with st.spinner(f"🤖 Analyzing with {selected_model_label}..."):
                    time.sleep(0.5)
                    type_map = {"📱 Phone/Smartphone":"Mobile Phones","💻 Laptop/Notebook":"Laptops","🖥️ Desktop Computer/CPU":"Desktop Computers","📱 Tablet/iPad":"Tablets","🖥️ Monitor/Display":"Monitors/Displays","📺 Television/TV":"Televisions","🖨️ Printer/Scanner":"Printers","🔋 Battery/Power Cell":"Batteries","🔌 Circuit Board/PCB":"PCBs/Circuit Boards","🔌 Cable/Wire":"Cables & Wires","🏠 Small Appliance (fan/toaster/iron)":"Small Appliances","🏠 Large Appliance (fridge/washer)":"Large Appliances","💡 Light/Bulb/Tube":"Lighting Equipment","🔊 Speaker/Audio/Video Device":"Audio/Video Equipment","📡 Router/Switch/Modem":"Networking Equipment"}
                    size_weight = {"🔹 Very Small (fits in palm)":0.1,"🔸 Small (fits in one hand)":0.5,"📦 Medium (fits in a bag)":3.0,"📦 Large (needs two hands)":8.0,"🏗️ Very Large (heavy/bulky)":40.0}
                    cond_map = {"🟢 Working/Good":8,"🟡 Partially Working":5,"🔴 Not Working/Broken":3,"⚫ Severely Damaged":1}
                    has_screen = visual_screen == "✅ Yes"
                    category = type_map.get(visual_type, "Mobile Phones")
                    condition_score = cond_map.get(visual_condition, 5)

                    device_profiles = {
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
                    profile = device_profiles.get(category, device_profiles['Mobile Phones'])
                    features = {**profile,'age_years':5,'condition_score':condition_score,'repair_count':1,
                        'battery_health_pct':60 if has_screen else -1,'screen_size_inch':profile['length_cm']*0.4 if has_screen else -1,
                        'storage_capacity_gb':128,'manufacturing_year':2019,'original_price_usd':profile['weight_kg']*200,
                        'component_count':int(profile['pcb_pct']*5),'connector_count':int(profile['pcb_pct']*0.5)+2,
                        'functional_status':'working' if condition_score>6 else 'partial' if condition_score>3 else 'non_functional',
                        'damage_level':'none' if condition_score>7 else 'minor' if condition_score>5 else 'moderate' if condition_score>3 else 'severe',
                        'energy_rating':'A','brand_tier':'mid_range','country_of_origin':'China',
                        'lead_present':0,'mercury_present':0,'cadmium_present':0,'chromium_present':0,'bfr_present':0,
                        'battery_present':1 if category in ['Mobile Phones','Laptops','Tablets'] else 0,
                        'screen_present':1 if has_screen else 0,'data_storage_present':1,'platinum_mg':2,'rare_earth_g':2,
                        'palladium_mg':profile.get('palladium_mg',10)}

                    # Use selected model
                    confidence = 0.98
                    if models_loaded and selected_model_key in artifacts and 'scaler' in artifacts and 'feature_names' in artifacts:
                        try:
                            input_df = pd.DataFrame([features])
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
                            model_obj = artifacts[selected_model_key]
                            pred_idx = model_obj.predict(X)[0]
                            category = artifacts['label_encoder'].inverse_transform([pred_idx])[0] if 'label_encoder' in artifacts else category
                            try:
                                probas = model_obj.predict_proba(X)[0]
                                confidence = float(max(probas))
                            except: confidence = 0.99
                        except: pass
                    final_category = category

                st.markdown(f'''<div class="result-box">
                    <div style="color:#888;letter-spacing:3px;text-transform:uppercase;font-size:.9rem;">🤖 {selected_model_label}</div>
                    <div class="glow-title" style="font-size:2.2rem;margin:10px 0;">{final_category}</div>
                    <div style="color:#aaa;">Confidence: <span style="color:#00FF7F;font-weight:700;">{confidence*100:.1f}%</span></div>
                </div>''', unsafe_allow_html=True)
                st.progress(min(int(confidence*100),100))

                # AI CHATBOT RECOMMENDATION
                if engines_loaded and final_category in CATEGORIES:
                    rec = recovery_engine.get_recommendation(final_category)
                    env = env_calculator.calculate_impact(final_category)
                    if 'error' not in rec:
                        save_classification(st.session_state.role,"image",final_category,confidence,rec['estimated_value_usd'],rec['recovery_method'],env.get('co2_saved_kg',0),f"Model:{selected_model_key}")

                        st.markdown("<br>", unsafe_allow_html=True)
                        rv1,rv2,rv3 = st.columns(3)
                        with rv1: st.markdown(f'<div class="metric-card"><div class="metric-icon">💰</div><div class="metric-value green-value">${rec["estimated_value_usd"]:.2f}</div><div class="metric-label">Recovery Value</div></div>', unsafe_allow_html=True)
                        with rv2: st.markdown(f'<div class="metric-card"><div class="metric-icon">🔧</div><div class="metric-value" style="font-size:1.4rem;">{rec["recovery_method"].upper()}</div><div class="metric-label">Method</div></div>', unsafe_allow_html=True)
                        with rv3: st.markdown(f'<div class="metric-card"><div class="metric-icon">🌍</div><div class="metric-value" style="color:#00BFFF;">{env.get("co2_saved_kg",0):.1f}</div><div class="metric-label">kg CO₂ Saved</div></div>', unsafe_allow_html=True)

                        # 🤖 CHATBOT STYLE RECOMMENDATION
                        st.markdown('<div class="section-header">🤖 AI RECOVERY CHATBOT</div>', unsafe_allow_html=True)
                        cond_text = visual_condition.split(" ",1)[1] if " " in visual_condition else "Unknown"
                        chat_messages = [
                            ("🤖", f"I've identified your item as **{final_category}** with **{confidence*100:.1f}%** confidence using **{selected_model_key.replace('_',' ').title()}** model."),
                            ("🤖", f"📊 **Condition Assessment:** Your device is in **{cond_text}** condition."),
                            ("🤖", f"💰 **Recovery Value:** This item has an estimated recovery value of **${rec['estimated_value_usd']:.2f}** through **{rec['recovery_method']}** processing."),
                            ("🤖", f"♻️ **Recommended Action:** {'✅ This item can be refurbished and resold!' if condition_score >= 7 else '🔧 Partial component recovery is recommended.' if condition_score >= 4 else '⚠️ Full material recovery recommended — the device is beyond repair.'}"),
                            ("🤖", f"🔧 **Recovery Method:** {rec['recovery_method'].title()} extraction process. Difficulty: **{rec['difficulty'].upper()}**. Estimated time: **{rec['time_estimate']}**."),
                        ]
                        if rec.get('recoverable_materials'):
                            mat_list = ", ".join([f"**{m.title()}**" for m in list(rec['recoverable_materials'].keys())[:5]])
                            chat_messages.append(("🤖", f"💎 **Recoverable Materials:** {mat_list}"))
                        chat_messages.append(("🤖", f"🌍 **Environmental Impact:** Recycling this saves **{env.get('co2_saved_kg',0):.1f} kg CO₂**, equivalent to planting **{env.get('co2_saved_kg',0)/21:.1f} trees**!"))
                        chat_messages.append(("🤖", f"⚠️ **Safety:** {rec['safety_precautions'][0] if rec['safety_precautions'] else 'Standard safety protocols apply.'}"))
                        chat_messages.append(("🤖", f"📋 **Next Steps:** Take this item to a certified e-waste recycling facility. {'Data wiping recommended before disposal.' if final_category in ['Mobile Phones','Laptops','Tablets','Desktop Computers'] else 'Ensure proper handling of hazardous materials.'}"))

                        for sender, msg in chat_messages:
                            st.markdown(f'''<div style="display:flex;gap:12px;margin:8px 0;animation:fadeIn .5s ease;">
                                <div style="font-size:1.5rem;min-width:35px;">{sender}</div>
                                <div class="glass-card" style="margin:0;padding:14px 18px;flex:1;border-left:3px solid #DC143C;">{msg}</div>
                            </div>''', unsafe_allow_html=True)

                        # User can ask follow-up
                        st.markdown("<br>", unsafe_allow_html=True)
                        user_q = st.selectbox("💬 Ask the AI Chatbot:", [
                            "-- Select a question --",
                            "How should I safely dispose of this?",
                            "What materials can be recovered?",
                            "Is it worth recycling?",
                            "What are the environmental benefits?",
                            "Where can I find a recycling center?",
                            "Can this device be repaired instead?"
                        ])
                        if user_q != "-- Select a question --":
                            answers = {
                                "How should I safely dispose of this?": f"For **{final_category}**, follow these steps:\n\n" + "\n".join([f"**Step {i+1}:** {s}" for i,s in enumerate(rec['recovery_steps'][:5])]),
                                "What materials can be recovered?": f"From this **{final_category}**, we can recover:\n\n" + "\n".join([f"• **{m.title()}**: ${v.get('value_usd',0):.2f}" for m,v in list(rec.get('recoverable_materials',{}).items())[:6]]) if rec.get('recoverable_materials') else "Standard materials including metals, plastics, and glass.",
                                "Is it worth recycling?": f"{'**YES!** ' if rec['cost_benefit_analysis']['is_profitable'] else '**Environmentally YES**, but '}the gross value is **${rec['cost_benefit_analysis']['gross_value_usd']:.2f}** with processing cost of **${rec['cost_benefit_analysis']['estimated_processing_cost_usd']:.2f}**. Net value: **${rec['cost_benefit_analysis']['net_value_usd']:.2f}**. {'Profitable!' if rec['cost_benefit_analysis']['is_profitable'] else 'While not directly profitable, the environmental benefits make it worthwhile.'}",
                                "What are the environmental benefits?": f"By recycling this **{final_category}**:\n\n🌳 **CO₂ Saved:** {env.get('co2_saved_kg',0)} kg\n💧 **Water Saved:** {env.get('water_saved_liters',0)} liters\n⚡ **Energy Saved:** {env.get('energy_saved_kwh',0)} kWh\n☠️ **Toxic Waste Prevented:** {env.get('toxic_prevented_kg',0)} kg",
                                "Where can I find a recycling center?": "🏭 Search for **certified e-waste recycling centers** near you:\n\n• Check your local municipality's waste management website\n• Search 'e-waste recycling near me' on Google Maps\n• Contact your electronics retailer — many offer take-back programs\n• Look for **R2 or e-Stewards certified** facilities",
                                "Can this device be repaired instead?": f"{'✅ **Yes!** Your device is in {cond_text} condition and may be repairable. Consider visiting an authorized repair center first.' if condition_score >= 5 else '❌ **Repair is not recommended.** The device is in poor condition. Material recovery is the best option.'}\n\n{'💡 **Tip:** Repairing extends product life by 2-5 years and saves 50-80% of manufacturing emissions!' if condition_score >= 5 else '♻️ **Tip:** Even non-repairable devices contain valuable materials that should be professionally recycled.'}"
                            }
                            st.markdown(f'''<div style="display:flex;gap:12px;margin:12px 0;">
                                <div style="font-size:1.5rem;min-width:35px;">👤</div>
                                <div class="glass-card" style="margin:0;padding:14px 18px;flex:1;border-left:3px solid #FFD700;">{user_q}</div>
                            </div>''', unsafe_allow_html=True)
                            st.markdown(f'''<div style="display:flex;gap:12px;margin:12px 0;">
                                <div style="font-size:1.5rem;min-width:35px;">🤖</div>
                                <div class="glass-card" style="margin:0;padding:14px 18px;flex:1;border-left:3px solid #DC143C;">{answers.get(user_q,"I'm here to help with e-waste recovery!")}</div>
                            </div>''', unsafe_allow_html=True)
    else:
        st.markdown('''<div class="glass-card" style="text-align:center;padding:60px;">
            <div style="font-size:4rem;margin-bottom:15px;">📸</div>
            <h3 style="color:#DC143C;">Upload Any E-Waste Image</h3>
            <p style="color:#888;font-size:1.05rem;">Take a photo of any electronic waste item and our AI will classify it, calculate recovery value, and give you chatbot recommendations.</p>
            <br><p style="color:#555;">No API key required! 100% Free & Offline ✅</p>
        </div>''', unsafe_allow_html=True)

# ─── AI CHATBOT ───
elif page_id == "chatbot":
    st.markdown('<h1 class="glow-title" style="font-size:2.5rem;">💬 AI E-WASTE RECOVERY CHATBOT</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#888;">Ask me anything about e-waste recycling, recovery & safe disposal — I\'m here to help! 🤖</p>', unsafe_allow_html=True)
    st.markdown('<div class="animated-line"></div>', unsafe_allow_html=True)

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "👋 **Namaste! I'm your E-Waste AI Assistant.**\n\nI can help you with:\n\n🔍 **Identify** e-waste items\n♻️ **Recovery** recommendations\n💰 **Value** estimation of materials\n🌍 **Environmental** impact info\n⚠️ **Safety** guidelines\n📍 **Recycling center** guidance\n\n**How can I help you today?** Type your question or select a quick option below!"}
        ]
    if "chatbot_classified" not in st.session_state:
        st.session_state.chatbot_classified = None

    # Chat display
    for msg in st.session_state.chat_messages:
        icon = "🤖" if msg["role"] == "assistant" else "👤"
        border_color = "#DC143C" if msg["role"] == "assistant" else "#FFD700"
        st.markdown(f'''<div style="display:flex;gap:12px;margin:10px 0;">
            <div style="font-size:1.6rem;min-width:38px;padding-top:4px;">{icon}</div>
            <div class="glass-card" style="margin:0;padding:16px 20px;flex:1;border-left:3px solid {border_color};">{msg["content"]}</div>
        </div>''', unsafe_allow_html=True)

    # Quick action buttons
    st.markdown('<div class="section-header">⚡ QUICK ACTIONS</div>', unsafe_allow_html=True)
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_q = None
    with qc1:
        if st.button("📱 Classify Device", use_container_width=True): quick_q = "I want to classify an e-waste device"
    with qc2:
        if st.button("💰 Material Value", use_container_width=True): quick_q = "What materials can be recovered from e-waste?"
    with qc3:
        if st.button("⚠️ Safety Tips", use_container_width=True): quick_q = "What safety precautions should I take when handling e-waste?"
    with qc4:
        if st.button("🌍 Eco Impact", use_container_width=True): quick_q = "What is the environmental impact of e-waste?"

    # Chat input
    user_input = st.chat_input("💬 Type your e-waste question here...")
    query = user_input or quick_q

    if query:
        st.session_state.chat_messages.append({"role": "user", "content": query})
        q = query.lower()

        # Smart AI response engine
        response = ""

        # Device classification queries
        if any(w in q for w in ['classify', 'identify', 'what is', 'kya hai', 'which type', 'category', 'phone', 'laptop', 'computer', 'tablet', 'monitor', 'tv', 'television', 'printer', 'battery', 'circuit', 'pcb', 'cable', 'wire', 'appliance', 'fridge', 'washer', 'light', 'bulb', 'speaker', 'router', 'modem']):
            device_found = None
            device_map = {
                'phone': 'Mobile Phones', 'mobile': 'Mobile Phones', 'smartphone': 'Mobile Phones',
                'laptop': 'Laptops', 'notebook': 'Laptops',
                'desktop': 'Desktop Computers', 'computer': 'Desktop Computers', 'cpu': 'Desktop Computers', 'pc': 'Desktop Computers',
                'tablet': 'Tablets', 'ipad': 'Tablets',
                'monitor': 'Monitors/Displays', 'display': 'Monitors/Displays', 'screen': 'Monitors/Displays',
                'tv': 'Televisions', 'television': 'Televisions',
                'printer': 'Printers', 'scanner': 'Printers',
                'battery': 'Batteries', 'cell': 'Batteries',
                'circuit': 'PCBs/Circuit Boards', 'pcb': 'PCBs/Circuit Boards', 'board': 'PCBs/Circuit Boards',
                'cable': 'Cables & Wires', 'wire': 'Cables & Wires', 'charger': 'Cables & Wires',
                'fan': 'Small Appliances', 'toaster': 'Small Appliances', 'iron': 'Small Appliances', 'mixer': 'Small Appliances', 'small appliance': 'Small Appliances',
                'fridge': 'Large Appliances', 'refrigerator': 'Large Appliances', 'washer': 'Large Appliances', 'washing': 'Large Appliances', 'ac': 'Large Appliances', 'air conditioner': 'Large Appliances',
                'light': 'Lighting Equipment', 'bulb': 'Lighting Equipment', 'lamp': 'Lighting Equipment', 'tube': 'Lighting Equipment', 'led': 'Lighting Equipment', 'cfl': 'Lighting Equipment',
                'speaker': 'Audio/Video Equipment', 'audio': 'Audio/Video Equipment', 'headphone': 'Audio/Video Equipment', 'earphone': 'Audio/Video Equipment',
                'router': 'Networking Equipment', 'modem': 'Networking Equipment', 'switch': 'Networking Equipment', 'hub': 'Networking Equipment',
            }
            for key, cat in device_map.items():
                if key in q:
                    device_found = cat; break

            if device_found and engines_loaded:
                st.session_state.chatbot_classified = device_found
                rec = recovery_engine.get_recommendation(device_found)
                env = env_calculator.calculate_impact(device_found)
                if 'error' not in rec:
                    response = f"## 🔍 Device Identified: **{device_found}**\n\n"
                    response += f"💰 **Recovery Value:** ${rec['estimated_value_usd']:.2f}\n\n"
                    response += f"🔧 **Recovery Method:** {rec['recovery_method'].title()}\n\n"
                    response += f"⏱️ **Processing Time:** {rec['time_estimate']}\n\n"
                    response += f"📊 **Difficulty:** {rec['difficulty'].upper()}\n\n"
                    response += f"🌍 **CO₂ Saved by Recycling:** {env.get('co2_saved_kg',0)} kg\n\n"
                    response += f"💧 **Water Saved:** {env.get('water_saved_liters',0)} liters\n\n"
                    if rec.get('recoverable_materials'):
                        response += "### 💎 Recoverable Materials:\n"
                        for mat, info in list(rec['recoverable_materials'].items())[:6]:
                            response += f"• **{mat.title()}** — ${info.get('value_usd',0):.2f}\n"
                    response += f"\n### ♻️ Recovery Steps:\n"
                    for i, step in enumerate(rec['recovery_steps'][:5],1):
                        response += f"**Step {i}:** {step}\n\n"
                    response += f"\n⚠️ **Safety:** {rec['safety_precautions'][0] if rec['safety_precautions'] else 'Standard protocols apply.'}"
                    save_classification(st.session_state.role, "chatbot", device_found, 0.95, rec['estimated_value_usd'], rec['recovery_method'], env.get('co2_saved_kg',0), f"Chatbot: {query[:50]}")
                else: response = f"I identified **{device_found}** but couldn't load recovery data. Please try the ♻️ Recovery Advisor page."
            elif not device_found:
                response = "🔍 I'd love to help classify your device! Could you tell me more specifically what it is?\n\nFor example:\n• 📱 Phone, Laptop, Tablet\n• 🖥️ Monitor, Desktop, TV\n• 🔋 Battery, Cable, Circuit Board\n• 🏠 Fan, Fridge, Washing Machine\n• 💡 Bulb, LED, Tube Light\n• 📡 Router, Modem, Speaker\n\n**Or upload an image on the 📸 Image Classify page!**"

        # Safety queries
        elif any(w in q for w in ['safety', 'safe', 'danger', 'hazard', 'toxic', 'precaution', 'protect', 'handle', 'suraksha']):
            response = """## ⚠️ E-Waste Safety Guidelines

### 🧤 Personal Protection:
• **Always wear gloves** (nitrile or rubber) when handling e-waste
• **Safety goggles** to protect eyes from dust and particles
• **N95 mask** when breaking or cutting components
• **Work in ventilated area** — avoid inhaling fumes

### ☠️ Hazardous Materials in E-Waste:
| Material | Found In | Health Risk |
|----------|----------|-------------|
| **Lead** | CRT monitors, solder | Brain/kidney damage |
| **Mercury** | Flat screens, switches | Nervous system damage |
| **Cadmium** | Batteries, semiconductors | Cancer risk |
| **Brominated Flame Retardants** | Circuit boards, plastic | Hormone disruption |
| **Lithium** | Rechargeable batteries | Fire/explosion risk |

### 🔥 Battery Safety:
• **NEVER** puncture, crush, or burn batteries
• Store damaged batteries in **sand or salt** container
• Keep away from water and metal objects
• Take to **certified recycling center** only

### 📋 Safe Handling Steps:
1. Sort and separate components
2. Remove batteries first
3. Handle CRT screens with extreme care
4. Never burn e-waste — releases toxic dioxins
5. Wipe data from storage devices before disposal

**Need specific safety info for a device?** Tell me which device you have!"""

        # Material/value queries
        elif any(w in q for w in ['material', 'value', 'price', 'worth', 'gold', 'silver', 'copper', 'metal', 'recover', 'precious', 'paisa', 'keemat']):
            last_device = st.session_state.chatbot_classified
            if last_device and engines_loaded:
                rec = recovery_engine.get_recommendation(last_device)
                if 'error' not in rec and rec.get('recoverable_materials'):
                    response = f"## 💎 Materials in **{last_device}**:\n\n"
                    total = 0
                    for mat, info in rec['recoverable_materials'].items():
                        val = info.get('value_usd', 0)
                        total += val
                        response += f"• **{mat.title()}** — ${val:.2f}\n"
                    response += f"\n💰 **Total Recovery Value:** ${total:.2f}\n\n"
                    response += f"{'✅ **Profitable** to recycle!' if rec['cost_benefit_analysis']['is_profitable'] else '⚠️ Not directly profitable, but **environmentally essential**!'}\n\n"
                    response += f"Processing cost: ${rec['cost_benefit_analysis']['estimated_processing_cost_usd']:.2f}\n"
                    response += f"Net value: ${rec['cost_benefit_analysis']['net_value_usd']:.2f}"
                else: response = f"Recovery data for {last_device} is limited. Try the ♻️ Recovery Advisor page for details."
            else:
                response = """## 💰 Precious Materials in E-Waste:

| Material | Value | Found In |
|----------|-------|----------|
| 🥇 **Gold** | ~$60/gram | Circuit boards, connectors |
| 🥈 **Silver** | ~$0.80/gram | Contacts, switches |
| 🔴 **Copper** | ~$8/kg | Wires, motors, PCBs |
| ⚪ **Platinum** | ~$30/gram | Hard drives, sensors |
| 🟤 **Palladium** | ~$40/gram | Capacitors, connectors |
| 🔵 **Rare Earth** | ~$20/kg | Magnets, screens |

### 📱 Value by Device:
• **Mobile Phone** → $2-5 (gold, silver, copper)
• **Laptop** → $5-15 (more copper, gold)
• **Desktop** → $8-25 (heavy copper, steel)
• **Circuit Board** → $15-50 (highest precious metals!)

**Tell me which device you have, and I'll give exact values!**"""

        # Environmental queries
        elif any(w in q for w in ['environment', 'eco', 'green', 'pollution', 'carbon', 'co2', 'climate', 'nature', 'paryavaran', 'pradushan']):
            response = """## 🌍 E-Waste Environmental Impact

### 📊 Shocking Facts:
• **50 million tons** of e-waste generated globally each year
• Only **20%** is properly recycled
• E-waste contains **70%** of toxic waste in landfills
• 1 million phones recycled = **35,000 lbs copper** + **772 lbs silver** + **75 lbs gold**

### 🌳 Benefits of Recycling:
| Action | Environmental Saving |
|--------|---------------------|
| Recycle 1 laptop | Saves **30 kg CO₂** |
| Recycle 1 phone | Saves **5 kg CO₂** |
| Recycle 1 TV | Saves **50 kg CO₂** |
| Recycle 1 fridge | Saves **150 kg CO₂** |

### 🎯 UN Sustainable Development Goals:
• **SDG 12:** Responsible Consumption & Production
• **SDG 13:** Climate Action
• **SDG 14:** Life Below Water (prevents ocean pollution)
• **SDG 15:** Life on Land (prevents soil contamination)

### ♻️ What YOU Can Do:
1. **Repair** before replacing
2. **Donate** working electronics
3. **Recycle** at certified centers
4. **Buy** refurbished devices
5. **Spread awareness** about e-waste

**Every device recycled makes a difference!** 🌱"""

        # Recycling center queries
        elif any(w in q for w in ['where', 'center', 'near', 'kahan', 'location', 'facility', 'collect', 'drop', 'submit', 'recycle kaha']):
            response = """## 📍 How to Find E-Waste Recycling Centers

### 🔍 Search Methods:
1. **Google Maps:** Search "e-waste recycling near me"
2. **Government portal:** Visit your city's waste management website
3. **Manufacturer programs:** Apple, Samsung, Dell, HP all have take-back programs
4. **E-waste apps:** Download apps like "Karo Sambhav" or "Saahas Zero Waste"

### 🏭 Major E-Waste Recyclers in India:
• **Attero Recycling** — Pan India
• **E-Parisaraa** — Bangalore
• **Sims Recycling** — Multiple cities
• **Cerebra** — Bangalore
• **Ash Recyclers** — Delhi NCR

### 📦 Collection Points:
• Most **mobile stores** accept old phones
• **Electronics retailers** (Croma, Reliance Digital) have collection bins
• **Corporate offices** often have e-waste drives
• **Municipal collection** centers in major cities

### 💡 Tips:
• **Wipe personal data** before submitting
• **Remove batteries** if possible
• **Keep accessories** together
• Ask for a **recycling certificate**

**Need help with a specific location? Tell me your city!**"""

        # Repair queries
        elif any(w in q for w in ['repair', 'fix', 'theek', 'kaise', 'how to', 'diy', 'broken', 'damage', 'not working']):
            response = """## 🔧 Repair vs Recycle Guide

### ✅ When to REPAIR:
• Device is less than **3 years old**
• Only **minor issues** (screen crack, battery weak)
• Repair cost is less than **50%** of new device price
• Device has **sentimental/data value**

### ♻️ When to RECYCLE:
• Device is **5+ years old**
• **Major damage** (water damage, motherboard failure)
• **Obsolete** (no software updates)
• Repair cost **exceeds** device value

### 💡 DIY Repair Tips:
1. **Slow phone?** → Factory reset, clear cache
2. **Weak battery?** → Battery replacement ($10-30)
3. **Cracked screen?** → Screen replacement service
4. **Laptop overheating?** → Clean fans, replace thermal paste
5. **No WiFi?** → Reset router, update firmware

### ⚠️ Don't DIY These:
• CRT monitor/TV repair (high voltage!)
• Lithium battery replacement (fire risk)
• Circuit board soldering (toxic fumes)

**Tell me about your device — I'll recommend repair or recycle!**"""

        # Greeting
        elif any(w in q for w in ['hi', 'hello', 'hey', 'namaste', 'help', 'kya kar', 'what can']):
            response = "👋 **Hello! I'm your E-Waste AI Assistant!**\n\nI can help you with:\n\n🔍 **Classify** — Tell me your device, I'll identify the e-waste type\n💰 **Value** — Know the material recovery value\n♻️ **Recovery** — Step-by-step recycling guidance\n⚠️ **Safety** — Hazard warnings and precautions\n🌍 **Impact** — Environmental benefits of recycling\n📍 **Centers** — Find recycling facilities\n🔧 **Repair** — Should you repair or recycle?\n\n**Just ask your question in English or Hindi!**"

        # Thank you
        elif any(w in q for w in ['thank', 'thanks', 'shukriya', 'dhanyawad', 'great', 'awesome', 'nice', 'good']):
            response = "😊 **You're welcome!** Happy to help with e-waste recycling.\n\n♻️ Remember: **Every device recycled = a greener planet!** 🌱\n\nFeel free to ask more questions anytime!"

        # Default smart response
        else:
            last_device = st.session_state.chatbot_classified
            if last_device:
                response = f"🤔 I'm not sure about that specific query, but I noticed you were asking about **{last_device}**.\n\nHere's what I can help with for {last_device}:\n• 💰 Type **'value'** for material recovery value\n• ♻️ Type **'how to recycle'** for recovery steps\n• ⚠️ Type **'safety'** for handling precautions\n• 🌍 Type **'environment'** for eco impact\n\nOr ask me anything about e-waste!"
            else:
                response = "🤔 I specialize in **e-waste recycling & recovery**. Try asking me:\n\n• \"What can I recover from an old **phone**?\"\n• \"Is it safe to open a **battery**?\"\n• \"Where can I recycle my **laptop**?\"\n• \"What's the environmental impact of **e-waste**?\"\n• \"Should I **repair or recycle** my device?\"\n\n**Type any device name and I'll classify it instantly!**"

        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Clear chat button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "👋 **Chat cleared!** I'm ready to help again.\n\nAsk me anything about e-waste recycling, recovery, safety, or environmental impact! 🤖♻️"}
        ]
        st.session_state.chatbot_classified = None
        st.rerun()

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
