"""
frontend/pages/dataset_management.py
E-WASTE AI - Dataset Management Page
Upload, inspect, clean and prepare datasets for ML training.
"""

import streamlit as st
import pandas as pd
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from frontend.theme import apply_theme, card, metric_card, section_header, status_badge


def render():
    apply_theme()
    st.markdown('<h1 class="page-title">📊 Dataset Management</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Upload, inspect, clean and prepare datasets for AI model training.</p>',
        unsafe_allow_html=True
    )

    tabs = st.tabs(["📤 Upload Dataset", "🔍 Inspect", "🧹 Clean", "⚙️ Preprocess", "📁 Manage Datasets"])

    # ------------------------------------------------------------------ #
    #  TAB 1 — Upload                                                     #
    # ------------------------------------------------------------------ #
    with tabs[0]:
        _tab_upload()

    # ------------------------------------------------------------------ #
    #  TAB 2 — Inspect                                                    #
    # ------------------------------------------------------------------ #
    with tabs[1]:
        _tab_inspect()

    # ------------------------------------------------------------------ #
    #  TAB 3 — Clean                                                      #
    # ------------------------------------------------------------------ #
    with tabs[2]:
        _tab_clean()

    # ------------------------------------------------------------------ #
    #  TAB 4 — Preprocess                                                 #
    # ------------------------------------------------------------------ #
    with tabs[3]:
        _tab_preprocess()

    # ------------------------------------------------------------------ #
    #  TAB 5 — Manage                                                     #
    # ------------------------------------------------------------------ #
    with tabs[4]:
        _tab_manage()


# ============================================================
# TAB 1 — UPLOAD
# ============================================================
def _tab_upload():
    section_header("Upload Your Dataset", "Choose a tabular dataset (CSV / Excel / JSON) or an image folder.")

    col1, col2 = st.columns([2, 1])
    with col1:
        dataset_type = st.radio(
            "Dataset Type",
            ["Tabular (CSV / Excel / JSON)", "Image Dataset (folder upload)"],
            horizontal=True,
            key="ds_upload_type"
        )

    if "Tabular" in dataset_type:
        _upload_tabular()
    else:
        _upload_image_info()


def _upload_tabular():
    st.markdown("#### Upload Tabular Dataset")
    uploaded = st.file_uploader(
        "Drop your CSV, Excel or JSON file here",
        type=["csv", "xlsx", "xls", "json"],
        help="Max 200 MB. Must contain column headers.",
        key="tabular_uploader"
    )

    if uploaded:
        ds_name = st.text_input("Dataset Name", value=uploaded.name.split(".")[0].replace("_", " ").title(), key="ds_name_input")
        ds_desc = st.text_area("Description (optional)", height=80, key="ds_desc_input")
        ds_source = st.text_input("Data Source / Citation (optional)", key="ds_source_input")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save & Inspect Dataset", type="primary", key="btn_save_tabular"):
                _save_tabular_dataset(uploaded, ds_name, ds_desc, ds_source)
    else:
        st.info("👆 Upload a file to get started. The system will automatically inspect and profile your dataset.")

        st.markdown("#### Supported Formats")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            **CSV** `.csv`
            - Comma or semicolon separated
            - UTF-8 or Latin-1 encoding
            - Header row required
            """)
        with c2:
            st.markdown("""
            **Excel** `.xlsx / .xls`
            - First sheet used
            - Header row required
            - Merged cells not supported
            """)
        with c3:
            st.markdown("""
            **JSON** `.json`
            - Array of objects format
            - Keys become column names
            - Nested objects flattened
            """)


def _save_tabular_dataset(uploaded_file, name: str, desc: str, source: str):
    """Save uploaded file and run initial inspection."""
    try:
        from ml.data.loaders.dataset_loader import load_tabular_dataset, inspect_tabular_dataset

        upload_dir = PROJECT_ROOT / "data" / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Inspecting dataset..."):
            df = load_tabular_dataset(str(file_path))
            info = inspect_tabular_dataset(df)

        st.session_state["current_dataset_path"] = str(file_path)
        st.session_state["current_dataset_df"] = df
        st.session_state["current_dataset_info"] = info
        st.session_state["current_dataset_name"] = name

        st.success(f"✅ Dataset '{name}' loaded! **{info['shape'][0]:,} rows × {info['shape'][1]} columns**")
        st.info("👉 Switch to the **Inspect** tab to review quality and statistics.")

    except Exception as e:
        st.error(f"❌ Failed to load dataset: {e}")


def _upload_image_info():
    st.markdown("#### Image Dataset Upload")
    st.info("""
    **Image datasets** should be organized as one folder per class:
    ```
    my_dataset/
    ├── smartphone/
    │   ├── img001.jpg
    │   └── img002.jpg
    ├── laptop/
    │   └── img003.png
    └── circuit_board/
        └── img004.jpg
    ```
    Zip your dataset folder and upload it below.
    """)

    uploaded_zip = st.file_uploader(
        "Upload dataset ZIP file",
        type=["zip"],
        help="Max 500 MB. Organize as one subfolder per class.",
        key="image_zip_uploader"
    )

    if uploaded_zip:
        import zipfile
        ds_name = st.text_input("Dataset Name", value=uploaded_zip.name.replace(".zip", ""), key="img_ds_name")
        if st.button("📦 Extract & Inspect Images", type="primary", key="btn_extract_zip"):
            _extract_image_dataset(uploaded_zip, ds_name)


def _extract_image_dataset(uploaded_zip, name: str):
    import zipfile
    try:
        extract_dir = PROJECT_ROOT / "data" / "images" / name
        extract_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(uploaded_zip, "r") as z:
            z.extractall(extract_dir)

        from ml.data.loaders.dataset_loader import inspect_image_dataset
        info = inspect_image_dataset(str(extract_dir))

        st.session_state["current_image_dataset_path"] = str(extract_dir)
        st.session_state["current_image_dataset_info"] = info

        st.success(f"✅ Extracted! **{info['total_images']} images** across **{info['num_classes']} classes**")
        st.json(info)

    except Exception as e:
        st.error(f"❌ Extraction failed: {e}")


# ============================================================
# TAB 2 — INSPECT
# ============================================================
def _tab_inspect():
    section_header("Dataset Inspection", "Automatic quality profiling and statistics.")

    df = st.session_state.get("current_dataset_df")
    info = st.session_state.get("current_dataset_info")
    name = st.session_state.get("current_dataset_name", "Dataset")
    image_info = st.session_state.get("current_image_dataset_info")

    if df is None and image_info is None:
        st.warning("No dataset loaded. Please upload a dataset in the **Upload Dataset** tab first.")
        return

    if df is not None and info is not None:
        _show_tabular_inspection(df, info, name)

    if image_info is not None:
        _show_image_inspection(image_info)


def _show_tabular_inspection(df: pd.DataFrame, info: dict, name: str):
    st.markdown(f"### 📊 {name}")

    # Key metrics row
    cols = st.columns(5)
    metrics = [
        ("Rows", f"{info['shape'][0]:,}"),
        ("Columns", f"{info['shape'][1]}"),
        ("Missing Values", f"{info.get('total_missing', 0):,}"),
        ("Duplicate Rows", f"{info.get('duplicates', 0)}"),
        ("Memory", f"{info.get('memory_mb', 0):.1f} MB"),
    ]
    for col, (label, value) in zip(cols, metrics):
        with col:
            st.metric(label, value)

    st.markdown("---")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("#### Column Summary")
        if "columns_info" in info:
            col_df = pd.DataFrame(info["columns_info"])
            st.dataframe(col_df, use_container_width=True, height=300)
        else:
            # Build from describe
            summary = df.describe(include="all").T
            summary["missing"] = df.isnull().sum()
            summary["missing_%"] = (df.isnull().sum() / len(df) * 100).round(2)
            st.dataframe(summary[["count", "missing", "missing_%"]].astype(str), use_container_width=True, height=300)

    with col2:
        st.markdown("#### Data Types")
        dtype_counts = df.dtypes.astype(str).value_counts().reset_index()
        dtype_counts.columns = ["Type", "Count"]
        st.dataframe(dtype_counts, use_container_width=True, hide_index=True)

        st.markdown("#### Missing Values")
        missing = df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        if len(missing) > 0:
            miss_df = pd.DataFrame({"Column": missing.index, "Missing": missing.values,
                                     "%": (missing.values / len(df) * 100).round(1)})
            st.dataframe(miss_df, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No missing values!")

    st.markdown("#### Sample Data (first 10 rows)")
    st.dataframe(df.head(10), use_container_width=True)

    # Numeric statistics
    numeric_cols = df.select_dtypes(include="number")
    if not numeric_cols.empty:
        st.markdown("#### Numeric Column Statistics")
        st.dataframe(numeric_cols.describe().T.round(4), use_container_width=True)


def _show_image_inspection(info: dict):
    st.markdown("### 🖼️ Image Dataset")
    cols = st.columns(4)
    with cols[0]: st.metric("Total Images", info.get("total_images", 0))
    with cols[1]: st.metric("Classes", info.get("num_classes", 0))
    with cols[2]: st.metric("Avg per Class", f"{info.get('avg_per_class', 0):.0f}")
    with cols[3]: st.metric("Formats", ", ".join(info.get("formats", [])))

    if "class_counts" in info:
        st.markdown("#### Class Distribution")
        class_df = pd.DataFrame(list(info["class_counts"].items()), columns=["Class", "Images"])
        class_df = class_df.sort_values("Images", ascending=False)
        st.bar_chart(class_df.set_index("Class"))


# ============================================================
# TAB 3 — CLEAN
# ============================================================
def _tab_clean():
    section_header("Data Cleaning", "Remove duplicates, fix missing values, detect outliers.")

    df = st.session_state.get("current_dataset_df")
    if df is None:
        st.warning("No tabular dataset loaded. Upload one in the **Upload** tab first.")
        return

    st.markdown(f"**Current dataset:** {df.shape[0]:,} rows × {df.shape[1]} columns")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Missing Value Strategy")
        num_strategy = st.selectbox("Numeric columns", ["median", "mean", "zero", "drop_rows"], key="num_strategy")
        cat_strategy = st.selectbox("Categorical columns", ["mode", "unknown", "drop_rows"], key="cat_strategy")
        drop_threshold = st.slider("Drop column if missing % >", 0, 100, 50, key="drop_thresh")

    with col2:
        st.markdown("#### Other Options")
        remove_dupes = st.checkbox("Remove duplicate rows", value=True, key="rm_dupes")
        detect_outliers = st.checkbox("Detect outliers (IQR method)", value=True, key="detect_out")
        normalize_text = st.checkbox("Normalize text columns (lowercase, strip)", value=True, key="norm_text")
        fix_types = st.checkbox("Auto-fix column types", value=True, key="fix_types")

    st.markdown("---")
    if st.button("🧹 Run Data Cleaning", type="primary", key="btn_run_cleaning"):
        _run_cleaning(df, num_strategy, cat_strategy, drop_threshold,
                      remove_dupes, detect_outliers, normalize_text, fix_types)

    # Show cleaning results if available
    if "cleaning_report" in st.session_state:
        _show_cleaning_report(st.session_state["cleaning_report"])


def _run_cleaning(df, num_strategy, cat_strategy, drop_thresh,
                  remove_dupes, detect_outliers, normalize_text, fix_types):
    try:
        from ml.data.loaders.cleaner import DataCleaner

        config = {
            "numeric_strategy": num_strategy,
            "categorical_strategy": cat_strategy,
            "drop_col_threshold": drop_thresh / 100,
            "remove_duplicates": remove_dupes,
            "detect_outliers": detect_outliers,
            "normalize_text": normalize_text,
            "fix_types": fix_types,
        }

        with st.spinner("Cleaning dataset... This may take a moment."):
            cleaner = DataCleaner(config)
            cleaned_df, report = cleaner.clean(df)

        st.session_state["cleaned_dataset_df"] = cleaned_df
        st.session_state["cleaning_report"] = report

        st.success(f"✅ Cleaning complete! **{report.get('rows_removed', 0)} rows removed**, "
                   f"**{report.get('missing_filled', 0)} missing values filled**.")

    except Exception as e:
        st.error(f"❌ Cleaning failed: {e}")
        import traceback
        st.code(traceback.format_exc())


def _show_cleaning_report(report: dict):
    st.markdown("### 🧹 Cleaning Report")
    cols = st.columns(4)
    with cols[0]: st.metric("Rows Before", report.get("rows_before", "—"))
    with cols[1]: st.metric("Rows After", report.get("rows_after", "—"))
    with cols[2]: st.metric("Missing Filled", report.get("missing_filled", 0))
    with cols[3]: st.metric("Duplicates Removed", report.get("duplicates_removed", 0))

    if report.get("outliers_detected", 0) > 0:
        st.warning(f"⚠️ {report['outliers_detected']} outlier values detected (not auto-removed — review before training).")

    if "dropped_columns" in report and report["dropped_columns"]:
        st.info(f"Columns dropped (too many missing): {report['dropped_columns']}")

    cleaned_df = st.session_state.get("cleaned_dataset_df")
    if cleaned_df is not None:
        st.markdown("#### Cleaned Dataset Preview")
        st.dataframe(cleaned_df.head(10), use_container_width=True)
        if st.button("✅ Use Cleaned Dataset for Preprocessing", key="btn_use_cleaned"):
            st.session_state["current_dataset_df"] = cleaned_df
            st.success("Cleaned dataset is now the active dataset.")


# ============================================================
# TAB 4 — PREPROCESS
# ============================================================
def _tab_preprocess():
    section_header("Data Preprocessing", "Encode, scale and split your dataset for ML training.")

    df = st.session_state.get("current_dataset_df")
    if df is None:
        st.warning("No dataset loaded. Upload in the **Upload** tab first.")
        return

    st.markdown(f"**Active dataset:** {df.shape[0]:,} rows × {df.shape[1]} columns")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Feature & Target Selection")
        all_cols = list(df.columns)
        target_col = st.selectbox("Target Column (label to predict)", all_cols, key="target_col_select")
        feature_cols = st.multiselect(
            "Feature Columns (inputs)",
            [c for c in all_cols if c != target_col],
            default=[c for c in all_cols if c != target_col],
            key="feature_cols_select"
        )

    with col2:
        st.markdown("#### Encoding & Scaling")
        scaler = st.selectbox("Numeric Scaler", ["standard", "minmax", "robust", "none"], key="scaler_select")
        encoder = st.selectbox("Categorical Encoder", ["label", "onehot", "none"], key="encoder_select")

        st.markdown("#### Train / Val / Test Split")
        train_ratio = st.slider("Train %", 50, 90, 70, key="train_ratio") / 100
        val_ratio = st.slider("Validation %", 5, 30, 15, key="val_ratio") / 100
        test_ratio = round(1 - train_ratio - val_ratio, 2)
        st.info(f"Test = **{test_ratio*100:.0f}%** (auto-calculated)")

    st.markdown("---")

    if not feature_cols:
        st.warning("Select at least one feature column.")
        return

    if st.button("⚙️ Run Preprocessing", type="primary", key="btn_run_preprocess"):
        _run_preprocessing(df, target_col, feature_cols, scaler, encoder, train_ratio, val_ratio)

    if "preprocessing_result" in st.session_state:
        _show_preprocessing_result(st.session_state["preprocessing_result"])


def _run_preprocessing(df, target_col, feature_cols, scaler, encoder, train_ratio, val_ratio):
    try:
        from ml.data.loaders.preprocessor import DataPreprocessor

        config = {
            "scaler": scaler,
            "encoder": encoder,
            "train_ratio": train_ratio,
            "val_ratio": val_ratio,
            "test_ratio": round(1 - train_ratio - val_ratio, 2),
            "feature_columns": feature_cols,
            "target_column": target_col,
        }

        with st.spinner("Preprocessing dataset..."):
            preprocessor = DataPreprocessor(config)
            X_train, X_val, X_test, y_train, y_val, y_test, feature_names = \
                preprocessor.fit_transform(df[feature_cols + [target_col]], target_col)

        result = {
            "X_train_shape": X_train.shape,
            "X_val_shape": X_val.shape,
            "X_test_shape": X_test.shape,
            "y_train_shape": y_train.shape,
            "feature_names": feature_names,
            "num_classes": len(set(y_train)),
            "config": config,
        }

        st.session_state["preprocessing_result"] = result
        st.session_state["preprocessor"] = preprocessor
        st.session_state["X_train"] = X_train
        st.session_state["X_val"] = X_val
        st.session_state["X_test"] = X_test
        st.session_state["y_train"] = y_train
        st.session_state["y_val"] = y_val
        st.session_state["y_test"] = y_test
        st.session_state["feature_names"] = feature_names
        st.session_state["num_classes"] = result["num_classes"]
        st.session_state["target_col"] = target_col

        st.success(f"✅ Preprocessing complete! **{result['num_classes']} classes** detected.")

    except Exception as e:
        st.error(f"❌ Preprocessing failed: {e}")
        import traceback
        st.code(traceback.format_exc())


def _show_preprocessing_result(result: dict):
    st.markdown("### ⚙️ Preprocessing Result")
    cols = st.columns(4)
    with cols[0]: st.metric("Train Samples", result["X_train_shape"][0])
    with cols[1]: st.metric("Val Samples", result["X_val_shape"][0])
    with cols[2]: st.metric("Test Samples", result["X_test_shape"][0])
    with cols[3]: st.metric("Features", result["X_train_shape"][1])

    st.info(f"**{result['num_classes']} classes** detected. Ready for model training!")
    if st.button("▶ Go to Model Training", key="btn_goto_training"):
        st.session_state["nav_page"] = "🤖 Model Training"
        st.rerun()


# ============================================================
# TAB 5 — MANAGE
# ============================================================
def _tab_manage():
    section_header("Manage Datasets", "View saved datasets in the data directory.")

    upload_dir = PROJECT_ROOT / "data" / "uploads"
    image_dir = PROJECT_ROOT / "data" / "images"

    st.markdown("#### Uploaded Tabular Datasets")
    tabular_files = list(upload_dir.glob("*.*")) if upload_dir.exists() else []
    if tabular_files:
        for f in tabular_files:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1: st.markdown(f"📄 **{f.name}**")
            with col2: st.caption(f"{f.stat().st_size / 1024:.1f} KB")
            with col3:
                if st.button("Load", key=f"load_{f.name}"):
                    _load_existing_file(f)
    else:
        st.info("No uploaded datasets yet. Use the **Upload Dataset** tab.")

    st.markdown("#### Image Datasets")
    image_dirs = list(image_dir.iterdir()) if image_dir.exists() else []
    if image_dirs:
        for d in image_dirs:
            if d.is_dir():
                img_count = sum(1 for _ in d.rglob("*") if _.suffix.lower() in (".jpg", ".jpeg", ".png", ".bmp"))
                st.markdown(f"🖼️ **{d.name}** — {img_count} images")
    else:
        st.info("No image datasets yet.")


def _load_existing_file(file_path: Path):
    try:
        from ml.data.loaders.dataset_loader import load_tabular_dataset, inspect_tabular_dataset
        df = load_tabular_dataset(str(file_path))
        info = inspect_tabular_dataset(df)
        st.session_state["current_dataset_df"] = df
        st.session_state["current_dataset_info"] = info
        st.session_state["current_dataset_name"] = file_path.stem
        st.session_state["current_dataset_path"] = str(file_path)
        st.success(f"✅ Loaded {file_path.name} — {df.shape[0]:,} rows × {df.shape[1]} columns")
    except Exception as e:
        st.error(f"Failed to load: {e}")
