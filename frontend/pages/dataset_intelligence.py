"""
Dataset Intelligence Page — Phase 2 UI
Main Streamlit page for the full dataset intelligence pipeline.
"""

import io
import json
import os
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from frontend.theme import COLORS, apply_custom_css


def render():
    apply_custom_css()
    st.markdown(
        f"<h1 style='color:{COLORS[\"gold\"]};font-family:Poppins,sans-serif;'>📊 Dataset Intelligence</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "Upload, inspect, clean, preprocess and export e-waste datasets. "
        "Raw data is **never modified** — all operations create new copies.",
        unsafe_allow_html=True,
    )

    tabs = st.tabs([
        "⬆️ Upload",
        "🔍 Inspection",
        "🧹 Cleaning",
        "⚙️ Preprocessing",
        "♻️ Domain Analysis",
        "📐 Preparation",
        "💾 Export & History",
    ])

    # ------------------------------------------------------------------ #
    # Shared session-state helpers                                         #
    # ------------------------------------------------------------------ #
    if "di_df_raw" not in st.session_state:
        st.session_state["di_df_raw"] = None
    if "di_df_cleaned" not in st.session_state:
        st.session_state["di_df_cleaned"] = None
    if "di_inspection" not in st.session_state:
        st.session_state["di_inspection"] = None
    if "di_cleaning_report" not in st.session_state:
        st.session_state["di_cleaning_report"] = None
    if "di_quality_report" not in st.session_state:
        st.session_state["di_quality_report"] = None
    if "di_dataset_name" not in st.session_state:
        st.session_state["di_dataset_name"] = "dataset"

    # ================================================================== #
    # TAB 1 — UPLOAD                                                       #
    # ================================================================== #
    with tabs[0]:
        _tab_upload()

    # ================================================================== #
    # TAB 2 — INSPECTION                                                   #
    # ================================================================== #
    with tabs[1]:
        _tab_inspection()

    # ================================================================== #
    # TAB 3 — CLEANING                                                     #
    # ================================================================== #
    with tabs[2]:
        _tab_cleaning()

    # ================================================================== #
    # TAB 4 — PREPROCESSING                                                #
    # ================================================================== #
    with tabs[3]:
        _tab_preprocessing()

    # ================================================================== #
    # TAB 5 — DOMAIN ANALYSIS                                              #
    # ================================================================== #
    with tabs[4]:
        _tab_domain_analysis()

    # ================================================================== #
    # TAB 6 — PREPARATION                                                  #
    # ================================================================== #
    with tabs[5]:
        _tab_preparation()

    # ================================================================== #
    # TAB 7 — EXPORT & HISTORY                                             #
    # ================================================================== #
    with tabs[6]:
        _tab_export()


# ======================================================================== #
# TAB IMPLEMENTATIONS                                                        #
# ======================================================================== #

def _tab_upload():
    st.subheader("Upload Dataset")
    uploaded = st.file_uploader(
        "Upload CSV, Excel, JSON or ZIP (image dataset)",
        type=["csv", "xlsx", "xls", "json", "zip"],
        accept_multiple_files=False,
    )

    if uploaded is not None:
        name = Path(uploaded.name).stem
        ext = Path(uploaded.name).suffix.lower()
        st.session_state["di_dataset_name"] = name

        try:
            if ext == ".csv":
                df = pd.read_csv(uploaded)
            elif ext in (".xlsx", ".xls"):
                df = pd.read_excel(uploaded)
            elif ext == ".json":
                df = pd.read_json(uploaded)
            else:
                st.warning("ZIP image datasets: place in `data/raw/` and use the image path in Domain Analysis.")
                return

            st.session_state["di_df_raw"] = df
            st.session_state["di_df_cleaned"] = None   # reset on new upload
            st.session_state["di_inspection"] = None
            st.session_state["di_cleaning_report"] = None
            st.session_state["di_quality_report"] = None

            st.success(f"✅ Loaded **{name}** — {len(df):,} rows × {len(df.columns)} columns")
            st.dataframe(df.head(10), use_container_width=True)

            # Save raw copy
            raw_dir = Path("data/raw")
            raw_dir.mkdir(parents=True, exist_ok=True)
            raw_path = raw_dir / uploaded.name
            df.to_csv(raw_path, index=False) if ext == ".csv" else None
            st.caption(f"Raw copy preserved at `{raw_path}`")

        except Exception as exc:
            st.error(f"Failed to load file: {exc}")

    elif st.session_state["di_df_raw"] is not None:
        df = st.session_state["di_df_raw"]
        st.info(f"Currently loaded: **{st.session_state['di_dataset_name']}** — {len(df):,} rows × {len(df.columns)} columns")
        st.dataframe(df.head(5), use_container_width=True)
    else:
        st.info("No dataset loaded. Upload a file above or place it in `data/raw/`.")


def _tab_inspection():
    st.subheader("Automatic Dataset Inspection")
    df = st.session_state.get("di_df_raw")
    if df is None:
        st.warning("Upload a dataset first (Tab 1).")
        return

    if st.button("🔍 Run Inspection", type="primary"):
        try:
            from ml.data.inspector import DatasetInspector
            from ml.data.quality_scorer import DatasetQualityScorer

            inspector = DatasetInspector()
            report = inspector.inspect_tabular(df)
            st.session_state["di_inspection"] = report

            scorer = DatasetQualityScorer()
            quality = scorer.score(df, report)
            st.session_state["di_quality_report"] = quality

            st.success("Inspection complete!")
        except Exception as exc:
            st.error(f"Inspection failed: {exc}")

    report = st.session_state.get("di_inspection")
    quality = st.session_state.get("di_quality_report")

    if report:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", f"{report.get('row_count', 0):,}")
        col2.metric("Columns", report.get("column_count", 0))
        col3.metric("Missing Values", report.get("total_missing", 0))
        col4.metric("Duplicates", report.get("duplicate_rows", 0))

        if quality:
            score = quality.get("overall_score", 0)
            grade = quality.get("grade", "?")
            color = "#4CAF50" if score >= 70 else "#FF9800" if score >= 50 else "#F44336"
            st.markdown(
                f"<h3 style='color:{color}'>Quality Score: {score}/100 (Grade {grade})</h3>"
                "<p style='font-size:0.8em;color:#888'>Diagnostic indicator — not a scientific standard</p>",
                unsafe_allow_html=True,
            )
            dims = quality.get("dimension_scores", {})
            if dims:
                dim_df = pd.DataFrame(
                    {"Dimension": list(dims.keys()), "Score": list(dims.values())}
                )
                st.bar_chart(dim_df.set_index("Dimension"))

        with st.expander("Column Details"):
            col_info = report.get("columns", {})
            if col_info:
                rows = []
                for col_name, info in col_info.items():
                    rows.append({
                        "Column": col_name,
                        "Type": info.get("inferred_type", "?"),
                        "Missing": info.get("missing_count", 0),
                        "Missing %": f"{info.get('missing_pct', 0):.1f}%",
                        "Unique": info.get("unique_count", 0),
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True)

        if quality and quality.get("issues"):
            with st.expander("⚠️ Issues Found"):
                for issue in quality["issues"]:
                    st.markdown(f"- {issue}")

        if quality and quality.get("recommendations"):
            with st.expander("💡 Recommendations"):
                for rec in quality["recommendations"]:
                    st.markdown(f"- {rec}")


def _tab_cleaning():
    st.subheader("Automated Data Cleaning")
    df = st.session_state.get("di_df_raw")
    if df is None:
        st.warning("Upload a dataset first (Tab 1).")
        return

    with st.form("cleaning_form"):
        col1, col2 = st.columns(2)
        with col1:
            fill_strategy = st.selectbox(
                "Missing value strategy",
                ["median", "mean", "mode", "constant", "drop_row"],
            )
            fill_constant = st.number_input("Fill constant (if strategy=constant)", value=0.0)
        with col2:
            drop_empty = st.checkbox("Drop fully empty columns", value=True)
            remove_dupes = st.checkbox("Remove duplicates", value=True)
            normalize_text = st.checkbox("Normalize text (lowercase + strip)", value=True)
            fix_types = st.checkbox("Fix data types", value=True)
            flag_outliers = st.checkbox("Flag outliers (IQR)", value=True)

        submitted = st.form_submit_button("🧹 Run Cleaning", type="primary")

    if submitted:
        try:
            from ml.data.cleaner_advanced import AdvancedDataCleaner
            cleaner = AdvancedDataCleaner()
            config = {
                "fill_strategy": fill_strategy,
                "fill_constant": fill_constant,
                "drop_empty_cols": drop_empty,
                "remove_duplicates": remove_dupes,
                "normalize_text": normalize_text,
                "fix_types": fix_types,
                "flag_outliers": flag_outliers,
            }
            cleaned_df, report = cleaner.clean(df, config)
            st.session_state["di_df_cleaned"] = cleaned_df
            st.session_state["di_cleaning_report"] = report

            # Save cleaned copy
            cleaned_dir = Path("data/cleaned")
            cleaned_dir.mkdir(parents=True, exist_ok=True)
            cleaned_path = cleaned_dir / f"{st.session_state['di_dataset_name']}_cleaned.csv"
            cleaned_df.to_csv(cleaned_path, index=False)

            st.success(f"✅ Cleaning complete! Cleaned copy saved to `{cleaned_path}`")
        except Exception as exc:
            st.error(f"Cleaning failed: {exc}")

    report = st.session_state.get("di_cleaning_report")
    cleaned_df = st.session_state.get("di_df_cleaned")

    if report and cleaned_df is not None:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows Before", report["rows_before"])
        col2.metric("Rows After", report["rows_after"])
        col3.metric("Missing Filled", report["missing_filled"])
        col4.metric("Duplicates Removed", report["duplicates_removed"])

        with st.expander("Operations Log"):
            for op in report.get("operations_log", []):
                st.markdown(f"**{op.get('operation')}** — {op.get('detail', '')}")

        st.subheader("Cleaned Data Preview")
        st.dataframe(cleaned_df.head(10), use_container_width=True)


def _tab_preprocessing():
    st.subheader("Advanced Preprocessing")
    df = st.session_state.get("di_df_cleaned") or st.session_state.get("di_df_raw")
    if df is None:
        st.warning("Upload and optionally clean a dataset first.")
        return

    cols = list(df.columns)
    target_col = st.selectbox("Target / Label column", cols)
    feature_cols = st.multiselect(
        "Feature columns (leave empty = all except target)",
        [c for c in cols if c != target_col],
    )

    with st.form("prep_form"):
        col1, col2 = st.columns(2)
        with col1:
            scaler = st.selectbox("Scaler", ["standard", "minmax", "robust", "none"])
            encoder = st.selectbox("Categorical Encoder", ["onehot", "label", "none"])
        with col2:
            train_r = st.slider("Train ratio", 0.5, 0.9, 0.7, 0.05)
            val_r   = st.slider("Validation ratio", 0.05, 0.3, 0.15, 0.05)
            seed    = st.number_input("Random seed", value=42, step=1)
            stratify = st.checkbox("Stratified split", value=True)

        test_r = round(1.0 - train_r - val_r, 2)
        st.caption(f"Test ratio will be: **{test_r}**")

        submitted = st.form_submit_button("⚙️ Run Preprocessing", type="primary")

    if submitted:
        if abs(train_r + val_r + test_r - 1.0) > 0.01:
            st.error("Ratios must sum to 1.0")
            return
        try:
            from ml.data.preprocessor_advanced import AdvancedPreprocessor
            prep = AdvancedPreprocessor()
            result = prep.fit_transform(
                df=df,
                target_col=target_col,
                feature_cols=feature_cols or None,
                config={
                    "scaler": scaler,
                    "encoder": encoder,
                    "train_ratio": train_r,
                    "val_ratio": val_r,
                    "test_ratio": test_r,
                    "random_seed": int(seed),
                    "stratify": stratify,
                },
            )
            r = result["preprocessing_report"]
            st.success("✅ Preprocessing complete!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Train samples", r["split"]["train"])
            col2.metric("Val samples", r["split"]["val"])
            col3.metric("Test samples", r["split"]["test"])
            st.json(r)
        except Exception as exc:
            st.error(f"Preprocessing failed: {exc}")


def _tab_domain_analysis():
    st.subheader("E-Waste Domain Analysis")
    df = st.session_state.get("di_df_cleaned") or st.session_state.get("di_df_raw")
    if df is None:
        st.warning("Upload a dataset first (Tab 1).")
        return

    if st.button("♻️ Run Domain Analysis", type="primary"):
        try:
            from ewaste.domain_intelligence import EwasteDomainAnalyzer
            analyzer = EwasteDomainAnalyzer()
            inspection = st.session_state.get("di_inspection")
            report = analyzer.analyze(df, inspection)

            st.info(report.get("summary", ""))

            is_ewaste = report.get("is_ewaste_dataset", False)
            confidence = int(report.get("confidence", 0) * 100)
            st.metric("E-Waste Dataset?", "YES ✅" if is_ewaste else "NO ❌", f"Confidence: {confidence}%")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Detected Column Roles**")
                role_map = report.get("detected_columns_by_role", {})
                for role, cols in role_map.items():
                    if cols:
                        st.markdown(f"- **{role}**: {', '.join(cols)}")

            with col2:
                st.markdown("**Suspicious Records**")
                suspicious = report.get("suspicious_records", [])
                if suspicious:
                    for s in suspicious:
                        st.warning(f"Column `{s['column']}`: {s['issue']} ({s['count']} records)")
                else:
                    st.success("No suspicious records found")

            hazmat = report.get("hazardous_material_flags", [])
            if hazmat:
                st.warning(f"⚠️ {len(hazmat)} hazardous material flag(s) detected")
                for h in hazmat:
                    st.markdown(f"- **{h['material']}** in column `{h['column']}` ({h['count']} records) — {h['note']}")

            issues = report.get("domain_issues", [])
            if issues:
                with st.expander("Domain Issues"):
                    for issue in issues:
                        st.markdown(f"- {issue}")

            suggestions = report.get("suggestions", [])
            if suggestions:
                with st.expander("💡 Suggestions"):
                    for s in suggestions:
                        st.markdown(f"- {s}")

        except Exception as exc:
            st.error(f"Domain analysis failed: {exc}")


def _tab_preparation():
    st.subheader("Dataset Preparation (Train / Val / Test Split)")
    df = st.session_state.get("di_df_cleaned") or st.session_state.get("di_df_raw")
    if df is None:
        st.warning("Upload a dataset first (Tab 1).")
        return

    cols = list(df.columns)
    target_col = st.selectbox("Target column", cols, key="prep_target")
    dataset_name = st.text_input("Dataset name (for output folder)", st.session_state["di_dataset_name"])

    with st.form("prepare_form"):
        col1, col2 = st.columns(2)
        with col1:
            train_r = st.slider("Train ratio", 0.5, 0.9, 0.7, 0.05, key="p_train")
            val_r   = st.slider("Val ratio", 0.05, 0.3, 0.15, 0.05, key="p_val")
        with col2:
            seed = st.number_input("Random seed", value=42, step=1, key="p_seed")
            stratify = st.checkbox("Stratified split", value=True, key="p_strat")

        test_r = round(1.0 - train_r - val_r, 2)
        st.caption(f"Test ratio: **{test_r}**")
        submitted = st.form_submit_button("📐 Prepare Dataset", type="primary")

    if submitted:
        try:
            from ml.data.dataset_preparer import DatasetPreparer
            preparer = DatasetPreparer()
            result = preparer.prepare_tabular(
                df=df,
                target_col=target_col,
                config={
                    "train_ratio": train_r,
                    "val_ratio": val_r,
                    "test_ratio": test_r,
                    "random_seed": int(seed),
                    "stratify": stratify,
                },
                dataset_name=dataset_name,
            )
            st.success("✅ Dataset prepared!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Train", result.stats["train_samples"])
            col2.metric("Val",   result.stats["val_samples"])
            col3.metric("Test",  result.stats["test_samples"])

            with st.expander("Split Paths"):
                for split, path in result.split_paths.items():
                    st.markdown(f"- **{split}**: `{path}`")

            with st.expander("Provenance"):
                st.json(result.provenance)

        except Exception as exc:
            st.error(f"Preparation failed: {exc}")


def _tab_export():
    st.subheader("Export & History")
    df = st.session_state.get("di_df_cleaned") or st.session_state.get("di_df_raw")
    cleaning_report = st.session_state.get("di_cleaning_report")
    quality_report = st.session_state.get("di_quality_report")
    dataset_name = st.session_state.get("di_dataset_name", "dataset")

    if df is None:
        st.warning("No dataset loaded.")
        return

    col1, col2, col3 = st.columns(3)

    with col1:
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download CSV",
            data=csv_data,
            file_name=f"{dataset_name}_processed.csv",
            mime="text/csv",
        )

    with col2:
        json_data = df.to_json(orient="records", indent=2).encode("utf-8")
        st.download_button(
            "⬇️ Download JSON",
            data=json_data,
            file_name=f"{dataset_name}_processed.json",
            mime="application/json",
        )

    with col3:
        if quality_report:
            report_json = json.dumps(quality_report, indent=2, default=str).encode("utf-8")
            st.download_button(
                "⬇️ Download Quality Report",
                data=report_json,
                file_name=f"{dataset_name}_quality_report.json",
                mime="application/json",
            )
        else:
            st.info("Run inspection first to download quality report")

    st.divider()
    st.subheader("Research Documentation")
    if st.button("📄 Generate Research Doc"):
        try:
            from ml.data.dataset_exporter import DatasetExporter
            exporter = DatasetExporter()
            inspection = st.session_state.get("di_inspection")
            md = exporter.generate_research_documentation(
                dataset_name=dataset_name,
                inspection_report=inspection,
                cleaning_report=cleaning_report,
                quality_report=quality_report,
            )
            st.download_button(
                "⬇️ Download Research Doc (Markdown)",
                data=md.encode("utf-8"),
                file_name=f"{dataset_name}_research_doc.md",
                mime="text/markdown",
            )
            with st.expander("Preview"):
                st.markdown(md)
        except Exception as exc:
            st.error(f"Documentation generation failed: {exc}")

    st.divider()
    st.subheader("Dataset Registry")
    try:
        from backend.services.dataset_service import DatasetService
        svc = DatasetService()
        datasets = svc.list_all_datasets()
        if datasets:
            st.dataframe(pd.DataFrame(datasets), use_container_width=True)
        else:
            st.info("No datasets registered in database yet.")
    except Exception as exc:
        st.caption(f"Database registry unavailable: {exc}")
