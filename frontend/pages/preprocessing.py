"""E-Waste AI — Preprocessing Page"""
import streamlit as st
from frontend.theme import apply_theme


def render_preprocessing():
    apply_theme()
    st.title("⚙️ Data Preprocessing")
    st.info("Prepare your cleaned datasets for machine learning training.")

    df = st.session_state.get("current_dataset_df")
    if df is None:
        st.warning("No active dataset loaded in session. Upload or clean a dataset in **Dataset Management** or **Data Cleaning** first.")
        return

    st.success(f"Active dataset loaded: **{len(df):,} rows × {len(df.columns)} columns**")
    st.markdown("### Preprocessing Configuration")

    tab1, tab2, tab3 = st.tabs(["Target & Splits", "Encoding", "Scaling"])

    with tab1:
        target_col = st.selectbox("Target Column", options=list(df.columns), index=len(df.columns) - 1)
        col1, col2 = st.columns(2)
        with col1:
            train_pct = st.number_input("Train Split %", min_value=50, max_value=85, value=70, step=5)
        with col2:
            val_pct = st.number_input("Validation Split %", min_value=5, max_value=30, value=15, step=5)
        test_pct = max(0, 100 - train_pct - val_pct)
        st.caption(f"Split ratios: Train {train_pct}% / Val {val_pct}% / Test {test_pct}%")

    with tab2:
        encoding_map = {
            "One-Hot Encoding": "onehot",
            "Ordinal Encoding": "ordinal",
            "None": "none",
        }
        encoding_label = st.selectbox("Encoding Method", list(encoding_map.keys()))
        encoding = encoding_map[encoding_label]

    with tab3:
        scaler_map = {
            "StandardScaler": "standard",
            "MinMaxScaler": "minmax",
            "RobustScaler": "robust",
            "None": "none",
        }
        scaler_label = st.selectbox("Scaler", list(scaler_map.keys()))
        scaler = scaler_map[scaler_label]

    if st.button("⚙️ Run Preprocessing", type="primary"):
        if train_pct + val_pct >= 100 or test_pct <= 0:
            st.error("Train + Validation splits must be less than 100% so a non-empty test split remains.")
            return
        try:
            from ml.data.preprocessor_advanced import AdvancedPreprocessor

            prep = AdvancedPreprocessor()
            result = prep.fit_transform(
                df,
                target_col=target_col,
                config={
                    "scaler": scaler,
                    "encoder": encoding,
                    "train_ratio": round(train_pct / 100.0, 2),
                    "val_ratio": round(val_pct / 100.0, 2),
                    "test_ratio": round(test_pct / 100.0, 2),
                },
            )
            st.session_state["preprocessed_result"] = result
            c1, c2, c3 = st.columns(3)
            c1.metric("Train Samples", len(result["X_train"]))
            c2.metric("Val Samples", len(result["X_val"]))
            c3.metric("Test Samples", len(result["X_test"]))
            st.success(f"✅ Preprocessing complete ({len(result['feature_names'])} features generated).")
        except Exception as exc:
            st.error(f"Preprocessing failed: {exc}")
