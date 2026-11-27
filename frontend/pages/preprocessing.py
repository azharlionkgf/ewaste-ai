"""E-Waste AI — Preprocessing Page"""
import streamlit as st
from frontend.theme import apply_theme

def render_preprocessing():
    apply_theme()
    st.title("⚙️ Data Preprocessing")
    st.info("Prepare your cleaned datasets for machine learning training.")
    
    st.markdown("### Preprocessing Steps")
    
    tab1, tab2, tab3 = st.tabs(["Feature Engineering", "Encoding", "Scaling"])
    
    with tab1:
        st.markdown("**Feature Engineering**")
        st.checkbox("Auto-detect numeric features")
        st.checkbox("Auto-detect categorical features")
        st.checkbox("Create interaction features")
    
    with tab2:
        st.markdown("**Categorical Encoding**")
        encoding = st.selectbox("Encoding Method", ["Label Encoding", "One-Hot Encoding", "Ordinal Encoding"])
        st.info(f"Selected: {encoding}")
    
    with tab3:
        st.markdown("**Feature Scaling**")
        scaler = st.selectbox("Scaler", ["StandardScaler", "MinMaxScaler", "RobustScaler", "None"])
        st.info(f"Selected: {scaler}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Train Split %", min_value=50, max_value=90, value=80)
    with col2:
        st.number_input("Validation Split %", min_value=5, max_value=25, value=10)
    
    st.button("⚙️ Run Preprocessing")
    st.warning("Select a dataset from Dataset Management first.")
