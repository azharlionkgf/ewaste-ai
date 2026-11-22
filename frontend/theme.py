"""
E-Waste AI — Streamlit Theme Injector
======================================
Injects the premium charcoal/gold design system into Streamlit.
"""

import streamlit as st


THEME_CSS = """
<style>
/* ═══════════════════════════════════════════════════════════
   E-WASTE AI — PREMIUM CHARCOAL & GOLD DESIGN SYSTEM
   ═══════════════════════════════════════════════════════════ */

/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── CSS Variables ──────────────────────────────────────── */
:root {
  --bg-primary:    #0A0A0A;
  --bg-surface:    #141414;
  --bg-card:       #1C1C1C;
  --bg-hover:      #242424;
  --border:        #2D2D2D;
  --border-light:  #383838;

  --gold:          #C9A84C;
  --gold-light:    #E8C97A;
  --gold-dark:     #A07830;
  --bronze:        #8B6914;

  --text-primary:  #F2F2F2;
  --text-secondary:#9A9A9A;
  --text-muted:    #666666;

  --success:       #27AE60;
  --warning:       #E67E22;
  --error:         #E74C3C;
  --info:          #2980B9;

  --font-heading:  'Poppins', sans-serif;
  --font-body:     'Inter', sans-serif;
  --font-code:     'JetBrains Mono', monospace;

  --radius-sm:     4px;
  --radius-md:     8px;
  --radius-lg:     12px;
  --radius-xl:     16px;

  --shadow-gold:   0 0 20px rgba(201, 168, 76, 0.15);
  --shadow-card:   0 4px 24px rgba(0, 0, 0, 0.4);
}

/* ── Global Reset ───────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: var(--font-body) !important;
  background-color: var(--bg-primary) !important;
  color: var(--text-primary) !important;
}

/* ── Main App Container ─────────────────────────────────── */
.main .block-container {
  background-color: var(--bg-primary);
  padding-top: 1.5rem;
  max-width: 1400px;
}

/* ── Sidebar ────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0D0D0D 0%, #111111 100%) !important;
  border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] .block-container {
  padding: 1rem 0.75rem !important;
}

/* ── Headings ───────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading) !important;
  color: var(--text-primary) !important;
}

h1 { font-size: 2rem !important; font-weight: 600 !important; }
h2 { font-size: 1.5rem !important; font-weight: 600 !important; }
h3 { font-size: 1.2rem !important; font-weight: 500 !important; }

/* ── Gold Accent for Page Titles ────────────────────────── */
.page-title {
  font-family: var(--font-heading) !important;
  font-size: 1.8rem !important;
  font-weight: 700 !important;
  color: var(--gold) !important;
  border-bottom: 2px solid var(--gold-dark);
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

/* ── Metric Cards ───────────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  padding: 1rem !important;
  box-shadow: var(--shadow-card) !important;
  transition: border-color 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
  border-color: var(--gold-dark) !important;
}

[data-testid="stMetricLabel"] {
  color: var(--text-secondary) !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
}

[data-testid="stMetricValue"] {
  color: var(--gold) !important;
  font-family: var(--font-heading) !important;
  font-size: 2rem !important;
  font-weight: 700 !important;
}

/* ── Buttons ────────────────────────────────────────────── */
.stButton > button {
  background: linear-gradient(135deg, var(--gold-dark), var(--gold)) !important;
  color: #0A0A0A !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-body) !important;
  font-weight: 600 !important;
  font-size: 0.875rem !important;
  padding: 0.5rem 1.5rem !important;
  transition: all 0.2s ease !important;
  letter-spacing: 0.03em !important;
}

.stButton > button:hover {
  background: linear-gradient(135deg, var(--gold), var(--gold-light)) !important;
  box-shadow: var(--shadow-gold) !important;
  transform: translateY(-1px) !important;
}

.stButton > button:active {
  transform: translateY(0) !important;
}

/* ── Secondary Button ───────────────────────────────────── */
.stButton > button[kind="secondary"] {
  background: transparent !important;
  color: var(--gold) !important;
  border: 1px solid var(--gold-dark) !important;
}

.stButton > button[kind="secondary"]:hover {
  background: rgba(201, 168, 76, 0.1) !important;
}

/* ── Input Fields ───────────────────────────────────────── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 1px var(--gold) !important;
}

/* ── Selectboxes ────────────────────────────────────────── */
.stSelectbox > div > div > div {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
}

/* ── Sliders ────────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] > div > div {
  background: var(--gold) !important;
}

/* ── Progress Bar ───────────────────────────────────────── */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--gold-dark), var(--gold)) !important;
}

/* ── Expander ───────────────────────────────────────────── */
.streamlit-expanderHeader {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
  font-weight: 500 !important;
}

.streamlit-expanderContent {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
}

/* ── Tabs ───────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-surface) !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text-secondary) !important;
  font-family: var(--font-body) !important;
  font-weight: 500 !important;
  border-bottom: 2px solid transparent !important;
  padding: 0.75rem 1.25rem !important;
}

.stTabs [aria-selected="true"] {
  color: var(--gold) !important;
  border-bottom-color: var(--gold) !important;
}

/* ── DataFrames / Tables ────────────────────────────────── */
[data-testid="stDataFrame"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
}

/* ── File Uploader ──────────────────────────────────────── */
[data-testid="stFileUploader"] {
  background: var(--bg-card) !important;
  border: 2px dashed var(--border) !important;
  border-radius: var(--radius-md) !important;
  padding: 1rem !important;
  transition: border-color 0.2s ease !important;
}

[data-testid="stFileUploader"]:hover {
  border-color: var(--gold-dark) !important;
}

/* ── Success / Warning / Error Boxes ───────────────────── */
.stSuccess {
  background: rgba(39, 174, 96, 0.1) !important;
  border: 1px solid rgba(39, 174, 96, 0.3) !important;
  border-radius: var(--radius-sm) !important;
}

.stWarning {
  background: rgba(230, 126, 34, 0.1) !important;
  border: 1px solid rgba(230, 126, 34, 0.3) !important;
  border-radius: var(--radius-sm) !important;
}

.stError {
  background: rgba(231, 76, 60, 0.1) !important;
  border: 1px solid rgba(231, 76, 60, 0.3) !important;
  border-radius: var(--radius-sm) !important;
}

.stInfo {
  background: rgba(41, 128, 185, 0.1) !important;
  border: 1px solid rgba(41, 128, 185, 0.3) !important;
  border-radius: var(--radius-sm) !important;
}

/* ── Divider ────────────────────────────────────────────── */
hr {
  border-color: var(--border) !important;
  margin: 1.5rem 0 !important;
}

/* ── Code blocks ────────────────────────────────────────── */
code {
  font-family: var(--font-code) !important;
  background: var(--bg-card) !important;
  color: var(--gold-light) !important;
  padding: 2px 6px !important;
  border-radius: 3px !important;
  font-size: 0.85em !important;
}

pre code {
  background: transparent !important;
  padding: 0 !important;
}

/* ── Scrollbar ──────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold-dark); }

/* ── Custom Card Component ──────────────────────────────── */
.ewaste-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow-card);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.ewaste-card:hover {
  border-color: var(--gold-dark);
  box-shadow: var(--shadow-gold);
}

.ewaste-card-title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 600;
  color: var(--gold);
  margin-bottom: 0.5rem;
}

/* ── Status Badge ───────────────────────────────────────── */
.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-success { background: rgba(39,174,96,0.2); color: #27AE60; }
.badge-warning { background: rgba(230,126,34,0.2); color: #E67E22; }
.badge-error   { background: rgba(231,76,60,0.2);  color: #E74C3C; }
.badge-info    { background: rgba(41,128,185,0.2);  color: #2980B9; }
.badge-gold    { background: rgba(201,168,76,0.2);  color: #C9A84C; }

/* ── Hide Streamlit Branding ────────────────────────────── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
"""


def inject_theme():
    """Inject the premium charcoal/gold CSS theme into Streamlit."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = ""):
    """Render a styled page header with gold accent."""
    if icon:
        st.markdown(f'<h1 class="page-title">{icon} {title}</h1>', unsafe_allow_html=True)
    else:
        st.markdown(f'<h1 class="page-title">{title}</h1>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p style="color: var(--text-secondary); margin-top: -1rem; margin-bottom: 1.5rem;">{subtitle}</p>',
                    unsafe_allow_html=True)


def card(content_fn, title: str = "", key: str = ""):
    """Render content inside a styled card."""
    if title:
        st.markdown(f'<div class="ewaste-card"><div class="ewaste-card-title">{title}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ewaste-card">', unsafe_allow_html=True)
    content_fn()
    st.markdown('</div>', unsafe_allow_html=True)


def badge(text: str, style: str = "gold") -> str:
    """Return HTML for a status badge."""
    return f'<span class="badge badge-{style}">{text}</span>'
