# Phase 5 Design System

## Visual Identity

E-Waste AI uses a **premium charcoal and gold** design language — industrial, authoritative, and clean.

### Colour Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#0A0A0A` | Main background |
| `--bg-surface` | `#141414` | Sidebar, panels |
| `--bg-card` | `#1C1C1C` | Cards, inputs |
| `--bg-hover` | `#242424` | Hover states |
| `--border` | `#2D2D2D` | Default borders |
| `--border-light` | `#383838` | Subtle dividers |
| `--gold` | `#C9A84C` | Primary accent, active nav, headings |
| `--gold-light` | `#E8C97A` | Hover gold |
| `--gold-dark` | `#A07830` | Button gradient start, border highlight |
| `--bronze` | `#8B6914` | Secondary accent |
| `--text-primary` | `#F2F2F2` | Body text |
| `--text-secondary` | `#9A9A9A` | Labels, captions |
| `--text-muted` | `#666666` | Placeholder, footnotes |
| `--success` | `#27AE60` | Completed, healthy |
| `--warning` | `#E67E22` | In-progress, caution |
| `--error` | `#E74C3C` | Failed, missing |
| `--info` | `#2980B9` | Informational |

### Typography

| Use | Font | Weight | Size |
|-----|------|--------|------|
| Page titles | Poppins | 700 | 2rem |
| Section headers | Poppins | 600 | 1.05rem |
| Body | Inter | 400 | 0.9rem |
| Labels / Captions | Inter | 500 | 0.75–0.8rem |
| Code / Mono | JetBrains Mono | 400 | 0.85em |

Fonts are loaded from Google Fonts CDN via `@import` in the injected CSS.

### Spacing

- Section gap: `1.5rem`
- Card padding: `1.25rem`
- Border radius: `4px` (sm), `8px` (md), `12px` (lg)

## Component Library (`frontend/theme.py`)

### `inject_theme()` / `apply_theme()`
Injects the full CSS design system into Streamlit. Called at the top of every page render function.

### `page_header(title, subtitle, icon)`
Renders a styled gold page title with optional subtitle and icon emoji.

### `section_header(title, subtitle)`
Renders a left-gold-border section divider — used to separate major content areas within a page.

### `status_badge(text, status)`
Returns an HTML `<span>` badge in one of: `success`, `warning`, `error`, `info`, `gold`, `muted`.

### `metric_card(label, value, delta, color)`
Custom metric card with dark background and gold value text — used as an alternative to `st.metric()` when finer control is needed.

### `badge(text, style)` / `card(content_fn, title)`
HTML helpers for inline badges and card wrappers.

### COLORS dict
Python dict of all colour tokens for use in Plotly chart theming and custom HTML:
```python
from frontend.theme import COLORS
fig.update_layout(paper_bgcolor=COLORS["bg"], font=dict(color=COLORS["text"]))
```

## Plotly Chart Theme

All Plotly charts use:
```python
fig.update_layout(
    paper_bgcolor="#0A0A0A",
    plot_bgcolor="#141414",
    font=dict(color="#F2F2F2", family="Inter"),
    colorway=["#C9A84C", "#2980B9", "#27AE60", "#E74C3C", "#E67E22"],
)
```

## Streamlit Config (`/.streamlit/config.toml`)

```toml
[theme]
primaryColor       = "#C9A84C"
backgroundColor    = "#0A0A0A"
secondaryBackgroundColor = "#141414"
textColor          = "#F2F2F2"
font               = "sans serif"
```

The config.toml provides the base theme; `inject_theme()` enhances it with detailed component-level CSS overrides.

## Status Badges — Usage Guide

```python
from frontend.theme import status_badge
st.markdown(status_badge("Active", "success"), unsafe_allow_html=True)
st.markdown(status_badge("Processing", "warning"), unsafe_allow_html=True)
st.markdown(status_badge("Failed", "error"), unsafe_allow_html=True)
st.markdown(status_badge("v2.0", "gold"), unsafe_allow_html=True)
```

## Responsive Design

Streamlit handles responsive layout via its column system. All pages use `st.columns()` with appropriate ratios. Mobile layout degrades gracefully (columns stack).

The sidebar uses `initial_sidebar_state="expanded"` by default; on mobile Streamlit auto-collapses it.
