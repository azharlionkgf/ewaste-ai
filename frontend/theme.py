"""
E-Waste AI — Obsidian & Champagne Gold Design System
====================================================
Injects the luxury-industrial glassmorphic CSS design system into Streamlit
and provides reusable UI, telemetry card, empty-state, and Plotly chart helpers.
"""

from __future__ import annotations

import html
import streamlit as st


COLORS = {
    "gold":       "#C9A84C",
    "gold_light": "#F2D67B",
    "gold_dark":  "#8C6A23",
    "bronze":     "#6E5116",
    "bg":         "#060709",
    "surface":    "#0E1015",
    "card":       "#141720",
    "text":       "#F4F4F6",
    "muted":      "#9CA3AF",
    "success":    "#10B981",
    "warning":    "#F59E0B",
    "error":      "#EF4444",
    "info":       "#3B82F6",
    # Extended palette for multi-series charts
    "copper":     "#D97745",
    "emerald":    "#10B981",
    "sapphire":   "#3B82F6",
    "violet":     "#8B5CF6",
    "platinum":   "#CBD5E1",
}

CHART_PALETTE = [
    "#C9A84C",  # Champagne gold
    "#10B981",  # Emerald
    "#3B82F6",  # Sapphire
    "#D97745",  # Copper
    "#F2D67B",  # Light gold
    "#8B5CF6",  # Violet
    "#06B6D4",  # Cyan
    "#CBD5E1",  # Platinum
]


THEME_CSS = """
<style>
/* Google Fonts: Display + UI + Monospace telemetry */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --bg-primary:     #060709;
  --bg-surface:     #0E1015;
  --bg-card:        rgba(20, 23, 32, 0.84);
  --bg-card-solid:  #141720;
  --bg-hover:       rgba(32, 37, 50, 0.92);
  --border:         rgba(255, 255, 255, 0.08);
  --border-gold:    rgba(201, 168, 76, 0.28);

  --gold:           #C9A84C;
  --gold-light:     #F2D67B;
  --gold-dark:      #8C6A23;

  --text-primary:   #F4F4F6;
  --text-secondary: #9CA3AF;
  --text-muted:     #6B7280;

  --success:        #10B981;
  --warning:        #F59E0B;
  --error:          #EF4444;
  --info:           #3B82F6;

  --font-heading:   'Space Grotesk', sans-serif;
  --font-body:      'Plus Jakarta Sans', sans-serif;
  --font-code:      'JetBrains Mono', monospace;

  --radius-sm:      6px;
  --radius-md:      10px;
  --radius-lg:      14px;
  --radius-xl:      18px;

  --shadow-gold:    0 8px 30px rgba(201, 168, 76, 0.14);
  --shadow-card:    0 8px 32px rgba(0, 0, 0, 0.45);
}

@keyframes ewaste-fade-up {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes ewaste-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.55); }
  50%      { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* ── App Canvas + Ambient Obsidian Backdrop ─────────────── */
html, body, .stApp, [data-testid="stAppViewContainer"] {
  font-family: var(--font-body) !important;
  background-color: var(--bg-primary) !important;
  color: var(--text-primary) !important;
}

[data-testid="stAppViewContainer"] {
  background-image:
    radial-gradient(ellipse 75% 45% at 88% -8%, rgba(201, 168, 76, 0.10), transparent 65%),
    radial-gradient(ellipse 55% 40% at 12% 105%, rgba(59, 130, 246, 0.05), transparent 60%),
    radial-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px) !important;
  background-size: 100% 100%, 100% 100%, 26px 26px !important;
  background-attachment: fixed !important;
}

.main .block-container {
  padding-top: 1.5rem !important;
  padding-bottom: 3rem !important;
  max-width: 1440px !important;
  animation: ewaste-fade-up 0.35s ease-out;
}

/* ── Sidebar Shell ──────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #090B0F 0%, #0D1016 60%, #090B0F 100%) !important;
  border-right: 1px solid rgba(201, 168, 76, 0.16) !important;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
  gap: 0.25rem !important;
}

[data-testid="stSidebar"] .stButton > button {
  width: 100% !important;
  justify-content: flex-start !important;
  text-align: left !important;
  padding: 0.52rem 0.85rem !important;
  border-radius: 9px !important;
  font-family: var(--font-body) !important;
  font-size: 0.84rem !important;
  letter-spacing: 0.01em !important;
  transition: all 0.18s cubic-bezier(0.22, 1, 0.36, 1) !important;
}

[data-testid="stSidebar"] .stButton > button[kind="secondary"],
[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"] {
  background: rgba(255, 255, 255, 0.02) !important;
  color: #A7B0BF !important;
  border: 1px solid rgba(255, 255, 255, 0.04) !important;
  font-weight: 500 !important;
}

[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover,
[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"]:hover {
  background: rgba(201, 168, 76, 0.09) !important;
  color: #F4F4F6 !important;
  border-color: rgba(201, 168, 76, 0.35) !important;
  transform: translateX(3px) !important;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"],
[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {
  background: linear-gradient(90deg, rgba(201, 168, 76, 0.22), rgba(201, 168, 76, 0.09)) !important;
  color: var(--gold-light) !important;
  border: 1px solid rgba(201, 168, 76, 0.55) !important;
  border-left: 3px solid var(--gold-light) !important;
  font-weight: 600 !important;
  box-shadow: 0 4px 18px rgba(201, 168, 76, 0.16) !important;
}

/* ── Typography ─────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading) !important;
  color: var(--text-primary) !important;
  letter-spacing: -0.02em;
}

.page-title {
  font-family: var(--font-heading) !important;
  font-size: 2rem !important;
  font-weight: 700 !important;
  background: linear-gradient(95deg, #F4F4F6 0%, #F2D67B 58%, #C9A84C 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.25rem !important;
}

.page-subtitle {
  color: var(--text-secondary) !important;
  font-size: 0.94rem !important;
  margin-bottom: 1.25rem !important;
}

/* ── Hero Header Component ──────────────────────────────── */
.ew-hero {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, rgba(20, 23, 32, 0.92) 0%, rgba(12, 14, 20, 0.95) 60%, rgba(28, 24, 14, 0.88) 100%);
  border: 1px solid rgba(201, 168, 76, 0.26);
  border-radius: var(--radius-xl);
  padding: 1.5rem 1.85rem;
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow-card), inset 0 1px 0 rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(14px);
}

.ew-hero::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #F2D67B, #C9A84C, transparent);
}

.ew-hero-top {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.45rem;
}

.ew-eyebrow {
  font-family: var(--font-code);
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--gold);
}

.ew-hero-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  align-items: center;
}

.ew-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: var(--font-code);
  font-size: 0.7rem;
  font-weight: 500;
  padding: 3px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.10);
  color: #CBD5E1;
}

.ew-pill-gold {
  background: rgba(201, 168, 76, 0.12);
  border-color: rgba(201, 168, 76, 0.35);
  color: #F2D67B;
}

.ew-pill-live {
  background: rgba(16, 185, 129, 0.12);
  border-color: rgba(16, 185, 129, 0.35);
  color: #34D399;
}

.ew-dot-live {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10B981;
  animation: ewaste-pulse 2s infinite;
}

.ew-hero-title {
  font-family: var(--font-heading);
  font-size: 1.85rem;
  font-weight: 700;
  line-height: 1.2;
  background: linear-gradient(95deg, #FFFFFF 0%, #F2D67B 65%, #C9A84C 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0.15rem 0 0.35rem 0;
}

.ew-hero-sub {
  font-family: var(--font-body);
  font-size: 0.92rem;
  color: #9CA3AF;
  max-width: 820px;
  line-height: 1.5;
}

/* ── Metric & KPI Cards ─────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-top: 2px solid rgba(201, 168, 76, 0.45) !important;
  border-radius: var(--radius-lg) !important;
  padding: 1rem 1.15rem !important;
  box-shadow: var(--shadow-card) !important;
  backdrop-filter: blur(12px) !important;
  transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
  transform: translateY(-2px) !important;
  border-color: rgba(201, 168, 76, 0.55) !important;
  box-shadow: var(--shadow-gold) !important;
}

[data-testid="stMetricLabel"] {
  color: var(--text-secondary) !important;
  font-size: 0.72rem !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
}

[data-testid="stMetricValue"] {
  color: var(--gold-light) !important;
  font-family: var(--font-heading) !important;
  font-variant-numeric: tabular-nums !important;
  font-size: 1.75rem !important;
  font-weight: 700 !important;
}

.ew-kpi {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.05rem 1.2rem;
  margin-bottom: 0.75rem;
  box-shadow: var(--shadow-card);
  backdrop-filter: blur(12px);
  transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  position: relative;
  overflow: hidden;
}

.ew-kpi:hover {
  transform: translateY(-2px);
  border-color: rgba(201, 168, 76, 0.5);
  box-shadow: var(--shadow-gold);
}

.ew-kpi-label {
  font-family: var(--font-code);
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-secondary);
}

.ew-kpi-value {
  font-family: var(--font-heading);
  font-variant-numeric: tabular-nums;
  font-size: 1.65rem;
  font-weight: 700;
  margin-top: 0.3rem;
  line-height: 1.15;
}

.ew-kpi-meta {
  font-size: 0.76rem;
  color: var(--text-muted);
  margin-top: 0.35rem;
}

/* ── Main Content Buttons ───────────────────────────────── */
.main .stButton > button[kind="primary"],
.main .stButton > button[data-testid="baseButton-primary"],
.main .stFormSubmitButton > button {
  background: linear-gradient(135deg, #B38B30 0%, #DFBE64 50%, #C9A84C 100%) !important;
  color: #07080B !important;
  border: 1px solid rgba(242, 214, 123, 0.55) !important;
  border-radius: 9px !important;
  font-family: var(--font-body) !important;
  font-weight: 700 !important;
  font-size: 0.86rem !important;
  padding: 0.55rem 1.35rem !important;
  letter-spacing: 0.02em !important;
  box-shadow: 0 4px 16px rgba(201, 168, 76, 0.24) !important;
  transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
}

.main .stButton > button[kind="primary"]:hover,
.main .stButton > button[data-testid="baseButton-primary"]:hover,
.main .stFormSubmitButton > button:hover {
  background: linear-gradient(135deg, #C9A84C 0%, #F7DF8D 100%) !important;
  box-shadow: 0 8px 24px rgba(201, 168, 76, 0.38) !important;
  transform: translateY(-1px) !important;
}

.main .stButton > button[kind="secondary"],
.main .stButton > button[data-testid="baseButton-secondary"],
.main .stDownloadButton > button {
  background: rgba(20, 23, 32, 0.85) !important;
  color: var(--gold-light) !important;
  border: 1px solid rgba(201, 168, 76, 0.35) !important;
  border-radius: 9px !important;
  font-family: var(--font-body) !important;
  font-weight: 600 !important;
  font-size: 0.85rem !important;
  padding: 0.52rem 1.2rem !important;
  transition: all 0.2s ease !important;
}

.main .stButton > button[kind="secondary"]:hover,
.main .stButton > button[data-testid="baseButton-secondary"]:hover,
.main .stDownloadButton > button:hover {
  background: rgba(201, 168, 76, 0.14) !important;
  border-color: var(--gold-light) !important;
  transform: translateY(-1px) !important;
}

/* ── Form Inputs & Selectboxes ──────────────────────────── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
  background: rgba(16, 18, 25, 0.92) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 8px !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
  transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 2px rgba(201, 168, 76, 0.22) !important;
}

.stSelectbox [data-baseweb="select"] > div,
.stMultiSelect [data-baseweb="select"] > div {
  background: rgba(16, 18, 25, 0.92) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 8px !important;
}

/* ── Segmented Pill Tabs ────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(14, 16, 22, 0.88) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  padding: 5px !important;
  gap: 6px !important;
  margin-bottom: 1rem !important;
  overflow-x: auto !important;
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text-secondary) !important;
  font-family: var(--font-body) !important;
  font-weight: 500 !important;
  font-size: 0.86rem !important;
  border-radius: 8px !important;
  border: none !important;
  padding: 0.55rem 1.05rem !important;
  transition: all 0.18s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
  color: var(--text-primary) !important;
  background: rgba(255, 255, 255, 0.04) !important;
}

.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(201, 168, 76, 0.22), rgba(201, 168, 76, 0.08)) !important;
  color: var(--gold-light) !important;
  border: 1px solid rgba(201, 168, 76, 0.45) !important;
  font-weight: 600 !important;
}

.stTabs [data-baseweb="tab-highlight"] {
  display: none !important;
}

/* ── Expanders, DataFrames, File Uploader ───────────────── */
[data-testid="stExpander"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  overflow: hidden !important;
}

[data-testid="stDataFrame"] {
  border: 1px solid rgba(201, 168, 76, 0.18) !important;
  border-radius: var(--radius-md) !important;
  overflow: hidden !important;
  box-shadow: var(--shadow-card) !important;
}

[data-testid="stFileUploader"] {
  background: rgba(18, 21, 29, 0.78) !important;
  border: 1.5px dashed rgba(201, 168, 76, 0.35) !important;
  border-radius: var(--radius-lg) !important;
  padding: 1.15rem !important;
  transition: all 0.2s ease !important;
}

[data-testid="stFileUploader"]:hover {
  border-color: var(--gold-light) !important;
  background: rgba(201, 168, 76, 0.05) !important;
}

/* ── Progress Bar & Slider ──────────────────────────────── */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--gold-dark), var(--gold), var(--gold-light)) !important;
}

/* ── Reusable Cards & Empty States ──────────────────────── */
.ewaste-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.2rem 1.35rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow-card);
  backdrop-filter: blur(12px);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.ewaste-card:hover {
  border-color: var(--border-gold);
  box-shadow: var(--shadow-gold);
}

.ewaste-card-title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 600;
  color: var(--gold-light);
  margin-bottom: 0.45rem;
}

.ew-empty {
  background: rgba(16, 19, 27, 0.72);
  border: 1.5px dashed rgba(201, 168, 76, 0.28);
  border-radius: var(--radius-lg);
  padding: 2rem 1.5rem;
  text-align: center;
  margin: 0.5rem 0 1rem 0;
}

.ew-empty-icon {
  font-size: 2.2rem;
  margin-bottom: 0.55rem;
}

.ew-empty-title {
  font-family: var(--font-heading);
  font-size: 1.05rem;
  font-weight: 600;
  color: #F4F4F6;
  margin-bottom: 0.3rem;
}

.ew-empty-msg {
  font-size: 0.86rem;
  color: #9CA3AF;
  max-width: 520px;
  margin: 0 auto;
  line-height: 1.5;
}

.ew-empty-hint {
  display: inline-block;
  margin-top: 0.75rem;
  font-family: var(--font-code);
  font-size: 0.74rem;
  color: #F2D67B;
  background: rgba(201, 168, 76, 0.12);
  border: 1px solid rgba(201, 168, 76, 0.3);
  padding: 4px 12px;
  border-radius: 999px;
}

/* ── Badges ─────────────────────────────────────────────── */
.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  font-family: var(--font-code);
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.badge-success { background: rgba(16,185,129,0.16); color: #34D399; border: 1px solid rgba(16,185,129,0.35); }
.badge-warning { background: rgba(245,158,11,0.16); color: #FBBF24; border: 1px solid rgba(245,158,11,0.35); }
.badge-error   { background: rgba(239,68,68,0.16);  color: #F87171; border: 1px solid rgba(239,68,68,0.35); }
.badge-info    { background: rgba(59,130,246,0.16); color: #60A5FA; border: 1px solid rgba(59,130,246,0.35); }
.badge-gold    { background: rgba(201,168,76,0.16); color: #F2D67B; border: 1px solid rgba(201,168,76,0.38); }

/* ── Code, Scrollbar, Divider ───────────────────────────── */
hr { border-color: rgba(255, 255, 255, 0.08) !important; margin: 1.4rem 0 !important; }
code {
  font-family: var(--font-code) !important;
  background: rgba(20, 23, 32, 0.9) !important;
  color: var(--gold-light) !important;
  padding: 2px 6px !important;
  border-radius: 4px !important;
  font-size: 0.84em !important;
}
pre code { background: transparent !important; padding: 0 !important; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #060709; }
::-webkit-scrollbar-thumb { background: #2D323E; border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold-dark); }

/* ── Hide Streamlit Chrome cleanly ──────────────────────── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
[data-testid="stToolbar"] { right: 1rem !important; }

/* ── Mobile Polish (<768px) ─────────────────────────────── */
@media (max-width: 768px) {
  .ew-hero { padding: 1.1rem 1.15rem; border-radius: 14px; }
  .ew-hero-title { font-size: 1.38rem; }
  .main .block-container { padding-left: 0.85rem !important; padding-right: 0.85rem !important; }
}
</style>
"""


def inject_theme():
    """Inject the Obsidian & Champagne Gold CSS design system."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def apply_theme():
    """Alias for inject_theme — backwards compatibility."""
    inject_theme()


def apply_custom_css():
    """Alias for inject_theme — backwards compatibility."""
    inject_theme()


def hero_banner(
    eyebrow: str,
    title: str,
    subtitle: str = "",
    icon: str = "",
    badges: list[tuple[str, str]] | None = None,
):
    """Render an executive glassmorphic hero banner. badges: list of (label, tone: live|gold|neutral)."""
    inject_theme()
    badge_html = ""
    for label, tone in (badges or []):
        safe_l = html.escape(str(label))
        if tone == "live":
            badge_html += f'<span class="ew-pill ew-pill-live"><span class="ew-dot-live"></span>{safe_l}</span>'
        elif tone == "gold":
            badge_html += f'<span class="ew-pill ew-pill-gold">{safe_l}</span>'
        else:
            badge_html += f'<span class="ew-pill">{safe_l}</span>'

    icon_html = f"{icon} " if icon else ""
    safe_eyebrow = html.escape(eyebrow)
    safe_title = html.escape(title)
    safe_sub = html.escape(subtitle)
    sub_block = f'<div class="ew-hero-sub">{safe_sub}</div>' if subtitle else ""

    st.markdown(
        f"""<div class="ew-hero">
          <div class="ew-hero-top">
            <span class="ew-eyebrow">{safe_eyebrow}</span>
            <div class="ew-hero-badges">{badge_html}</div>
          </div>
          <div class="ew-hero-title">{icon_html}{safe_title}</div>
          {sub_block}
        </div>""",
        unsafe_allow_html=True,
    )


def page_header(
    title: str,
    subtitle: str = "",
    icon: str = "",
    eyebrow: str = "E-WASTE AI · INTELLIGENCE WORKSPACE",
    badges: list[tuple[str, str]] | None = None,
):
    """Render standardized executive hero header across all 17 workspaces."""
    default_badges = badges if badges is not None else [("CPU Engine", "gold")]
    hero_banner(eyebrow=eyebrow, title=title, subtitle=subtitle, icon=icon, badges=default_badges)


def section_header(title: str, subtitle: str = "", icon: str = ""):
    """Render a crisp gold-accent section divider with optional subtitle."""
    icon_prefix = f"{icon} " if icon else ""
    safe_title = html.escape(title)
    safe_sub = html.escape(subtitle)
    sub_div = f"<div style='color:#9CA3AF;font-size:0.82rem;margin-top:2px'>{safe_sub}</div>" if subtitle else ""
    st.markdown(
        f"<div style='border-left:3px solid #C9A84C;padding:2px 0 2px 13px;"
        f"margin:1.35rem 0 0.85rem 0'>"
        f"<div style='color:#F4F4F6;font-family:Space Grotesk,sans-serif;"
        f"font-weight:600;font-size:1.08rem;letter-spacing:-0.01em'>{icon_prefix}{safe_title}</div>"
        f"{sub_div}</div>",
        unsafe_allow_html=True,
    )


def kpi_card(
    label: str,
    value: str,
    delta: str = "",
    tone: str = "gold",
    badge_text: str = "",
):
    """Render a glassmorphic KPI telemetry card with tabular numeric alignment."""
    tone_colors = {
        "gold":    "#F2D67B",
        "success": "#34D399",
        "warning": "#FBBF24",
        "error":   "#F87171",
        "info":    "#60A5FA",
        "neutral": "#F4F4F6",
    }
    val_color = tone_colors.get(tone, "#F2D67B")
    border_top = f"border-top:2px solid {val_color}88;"
    delta_html = f"<div class='ew-kpi-meta'>{html.escape(delta)}</div>" if delta else ""
    badge_html = (
        f"<span style='float:right'>{status_badge(badge_text, tone if tone in ('success','warning','error','info','gold') else 'gold')}</span>"
        if badge_text else ""
    )
    st.markdown(
        f"""<div class="ew-kpi" style="{border_top}">
          <div class="ew-kpi-label">{html.escape(label)}{badge_html}</div>
          <div class="ew-kpi-value" style="color:{val_color}">{html.escape(str(value))}</div>
          {delta_html}
        </div>""",
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, delta: str = "", color: str = "#C9A84C"):
    """Backwards-compatible metric card."""
    delta_html = f"<div class='ew-kpi-meta'>{html.escape(delta)}</div>" if delta else ""
    st.markdown(
        f"""<div class="ew-kpi" style="border-top:2px solid {color}88">
          <div class="ew-kpi-label">{html.escape(label)}</div>
          <div class="ew-kpi-value" style="color:{color}">{html.escape(str(value))}</div>
          {delta_html}
        </div>""",
        unsafe_allow_html=True,
    )


def empty_state_card(icon: str, title: str, message: str, hint: str = ""):
    """Render an inviting Obsidian empty-state box instead of generic alert banners."""
    hint_html = f'<div class="ew-empty-hint">{html.escape(hint)}</div>' if hint else ""
    st.markdown(
        f"""<div class="ew-empty">
          <div class="ew-empty-icon">{icon}</div>
          <div class="ew-empty-title">{html.escape(title)}</div>
          <div class="ew-empty-msg">{html.escape(message)}</div>
          {hint_html}
        </div>""",
        unsafe_allow_html=True,
    )


def card(content_fn, title: str = "", key: str = ""):
    """Render content inside a styled card."""
    if title:
        st.markdown(f'<div class="ewaste-card"><div class="ewaste-card-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ewaste-card">', unsafe_allow_html=True)
    content_fn()
    st.markdown('</div>', unsafe_allow_html=True)


def badge(text: str, style: str = "gold") -> str:
    """Return HTML for a status pill badge."""
    return f'<span class="badge badge-{style}">{html.escape(text)}</span>'


def status_badge(text: str, status: str = "info") -> str:
    """Return HTML badge string."""
    colors = {
        "success": "#34D399", "warning": "#FBBF24",
        "error":   "#F87171", "info":    "#60A5FA",
        "gold":    "#F2D67B", "muted":   "#9CA3AF",
    }
    fg = colors.get(status, colors["info"])
    return (
        f"<span style='background:{fg}1F;color:{fg};border:1px solid {fg}55;"
        f"border-radius:999px;padding:2px 9px;font-size:0.7rem;"
        f"font-family:JetBrains Mono,monospace;font-weight:600;letter-spacing:0.04em'>"
        f"{html.escape(text)}</span>"
    )


def plotly_dark_layout(fig, title: str = "", height: int = 360, xaxis_title: str = "", yaxis_title: str = ""):
    """Apply consistent Obsidian & Champagne Gold interactive Plotly theme (2D only)."""
    fig.update_layout(
        title=dict(text=title, font=dict(family="Space Grotesk, sans-serif", size=15, color="#F2D67B"), x=0.01) if title else None,
        height=height,
        paper_bgcolor="rgba(14,16,21,0.65)",
        plot_bgcolor="rgba(10,12,16,0.72)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#E5E7EB", size=12),
        margin=dict(l=48, r=24, t=48 if title else 24, b=42),
        hoverlabel=dict(
            bgcolor="#141720",
            bordercolor="#C9A84C",
            font=dict(family="JetBrains Mono, sans-serif", color="#F4F4F6", size=12),
        ),
        legend=dict(
            bgcolor="rgba(14,16,21,0.5)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            font=dict(size=11),
        ),
        xaxis=dict(
            title=xaxis_title or None,
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.10)",
        ),
        yaxis=dict(
            title=yaxis_title or None,
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.10)",
        ),
    )
    return fig
