"""
E-Waste AI — Data Cleaning Workspace
======================================
Task 4 of Phase 5. Connects to Phase 2 data cleaning pipeline.
Shows cleaning results, issues found and allows cleaned export.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from frontend.theme import apply_theme, page_header, section_header, COLORS

try:
    from ewaste.data_pipeline.data_cleaner import DataCleaner
    CLEANER_OK = True
except Exception as e:
    CLEANER_OK = False
    CLEANER_ERR = str(e)


def render_data_cleaning():
    apply_theme()
    page_header(
        "Data Cleaning",
        "Inspect, clean and validate datasets using the Phase 2 cleaning pipeline",
        "🧹",
    )

    if not CLEANER_OK:
        st.warning(f"Data Cleaner module unavailable: {CLEANER_ERR}")
        st.info("The data cleaning pipeline will be available once the ewaste package is installed.")
        _show_cleaning_guide()
        return

    section_header("Upload Dataset for Cleaning")
    uploaded = st.file_uploader("Upload CSV / Excel dataset", type=["csv", "xlsx", "xls"])

    if not uploaded:
        st.markdown(
            "<div style='background:#1C1C1C;border:2px dashed #2D2D2D;border-radius:12px;"
            "padding:3rem;text-align:center;color:#666'>"
            "<div style='font-size:3rem'>🧹</div>"
            "<div style='font-size:1rem;margin-top:1rem'>Upload a dataset to begin cleaning</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        _show_cleaning_guide()
        return

    import pandas as pd, io

    try:
        if uploaded.name.endswith(".csv"):
            df_raw = pd.read_csv(uploaded)
        else:
            df_raw = pd.read_excel(uploaded)
    except Exception as ex:
        st.error(f"Could not read file: {ex}")
        return

    st.success(f"✅ Loaded: **{uploaded.name}** — {len(df_raw):,} rows × {len(df_raw.columns)} columns")

    tabs = st.tabs(["👁️ Preview", "🔍 Issues", "🧹 Clean", "📊 Quality Score"])

    with tabs[0]:
        section_header("Raw Data Preview")
        st.dataframe(df_raw.head(50), use_container_width=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", f"{len(df_raw):,}")
        c2.metric("Columns", len(df_raw.columns))
        c3.metric("Missing Values", int(df_raw.isnull().sum().sum()))

    with tabs[1]:
        section_header("Data Issues Found")
        issues = []
        for col in df_raw.columns:
            null_pct = df_raw[col].isnull().mean() * 100
            if null_pct > 0:
                issues.append({"Column": col, "Issue": "Missing values", "Severity": "High" if null_pct > 50 else "Medium", "Details": f"{null_pct:.1f}% null"})
            if df_raw[col].dtype == object:
                dupe_pct = df_raw[col].duplicated().mean() * 100
                if dupe_pct > 90:
                    issues.append({"Column": col, "Issue": "High duplication", "Severity": "Low", "Details": f"{dupe_pct:.1f}% duplicated"})

        dup_rows = df_raw.duplicated().sum()
        if dup_rows > 0:
            issues.append({"Column": "— (rows)", "Issue": "Duplicate rows", "Severity": "Medium", "Details": f"{dup_rows} duplicate rows"})

        if issues:
            issues_df = pd.DataFrame(issues)
            st.dataframe(issues_df, use_container_width=True)
        else:
            st.success("✅ No obvious issues detected in this dataset.")

    with tabs[2]:
        section_header("Cleaning Options")
        col1, col2 = st.columns(2)
        drop_dupes   = col1.checkbox("Drop duplicate rows", value=True)
        fill_numeric = col2.checkbox("Fill missing numeric with median", value=True)
        fill_cat     = col1.checkbox("Fill missing categorical with 'Unknown'", value=True)
        strip_spaces = col2.checkbox("Strip whitespace from text columns", value=True)

        if st.button("🧹 Apply Cleaning", type="primary"):
            df_clean = df_raw.copy()
            if drop_dupes:
                before = len(df_clean)
                df_clean = df_clean.drop_duplicates()
                st.info(f"Removed {before - len(df_clean)} duplicate rows.")
            if fill_numeric:
                for col in df_clean.select_dtypes(include="number").columns:
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
            if fill_cat:
                for col in df_clean.select_dtypes(include="object").columns:
                    df_clean[col].fillna("Unknown", inplace=True)
            if strip_spaces:
                for col in df_clean.select_dtypes(include="object").columns:
                    df_clean[col] = df_clean[col].str.strip()

            st.success(f"✅ Cleaned: {len(df_clean):,} rows × {len(df_clean.columns)} columns")
            st.dataframe(df_clean.head(50), use_container_width=True)

            csv_clean = df_clean.to_csv(index=False).encode()
            st.download_button("⬇️ Download Cleaned CSV", csv_clean,
                               file_name=f"cleaned_{uploaded.name.replace('.xlsx','.csv')}",
                               mime="text/csv")

    with tabs[3]:
        section_header("Dataset Quality Score")
        total_cells = df_raw.size
        missing_cells = df_raw.isnull().sum().sum()
        completeness = (1 - missing_cells / total_cells) * 100 if total_cells else 0
        uniqueness = (1 - df_raw.duplicated().mean()) * 100
        quality_score = (completeness * 0.6 + uniqueness * 0.4)

        c1, c2, c3 = st.columns(3)
        c1.metric("Completeness", f"{completeness:.1f}%")
        c2.metric("Uniqueness", f"{uniqueness:.1f}%")
        c3.metric("Overall Quality Score", f"{quality_score:.1f}/100")

        if quality_score >= 80:
            st.success("✅ Good quality dataset — suitable for training.")
        elif quality_score >= 60:
            st.warning("⚠️ Fair quality — cleaning recommended before training.")
        else:
            st.error("❌ Poor quality — significant cleaning required.")


def _show_cleaning_guide():
    section_header("Data Cleaning Guide")
    st.markdown("""
**What Data Cleaning Does**
1. **Removes duplicates** — identical rows that skew training
2. **Handles missing values** — fill or drop based on column type
3. **Normalises text** — strips whitespace, standardises categories
4. **Validates data types** — catches columns stored as wrong type
5. **Flags outliers** — extreme values that may indicate errors

**When to Clean**
- Before any preprocessing or feature engineering
- After uploading new raw data
- When model performance degrades unexpectedly

**Output**
- Cleaned CSV/Excel file for download
- Cleaning report with issues and actions taken
- Quality score to assess readiness for training
    """)
