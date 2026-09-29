"""
E-Waste Classification & Recovery Recommendation System
========================================================
Complete End-to-End Training Pipeline
Final Year Data Science Project
"""

import os
import sys
import json
import pickle
import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, f1_score, precision_score, 
                             recall_score, confusion_matrix, classification_report)

warnings.filterwarnings('ignore')

# Setup paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

import config
from src.utils import setup_directories, get_logger, save_model, timer
from src.data_generator import generate_synthetic_data
from src.preprocessing import DataPreprocessor
from src.feature_engineering import FeatureEngineer
from src.models import ModelTrainer
from src.ensemble import StackingEnsembleClassifier
from src.recovery_engine import RecoveryRecommendationEngine
from src.environmental_impact import EnvironmentalImpactCalculator

logger = get_logger(__name__)


def main():
    print("=" * 70)
    print("⚡ E-WASTE CLASSIFICATION & RECOVERY RECOMMENDATION SYSTEM")
    print("=" * 70)
    print()

    # ─── Step 1: Setup Directories ───
    print("📁 [1/8] Setting up directories...")
    setup_directories()
    print("   ✅ Directories created.\n")

    # ─── Step 2: Generate Data ───
    print("📊 [2/8] Generating synthetic dataset...")
    raw_path = os.path.join(config.DIRS['raw_data'], 'e_waste_data.csv')
    if os.path.exists(raw_path):
        print(f"   ℹ️  Dataset already exists at {raw_path}")
        df = pd.read_csv(raw_path)
    else:
        df = generate_synthetic_data(num_samples=config.DATASET_SIZE, random_seed=config.RANDOM_SEED)
    print(f"   ✅ Dataset shape: {df.shape}")
    print(f"   ✅ Categories: {df[config.TARGET_COLUMN].nunique()}")
    print(f"   ✅ Samples per category:\n{df[config.TARGET_COLUMN].value_counts().to_string()}\n")

    # ─── Step 3: Feature Engineering ───
    print("🔧 [3/8] Feature engineering...")
    fe = FeatureEngineer()
    df_eng = fe.fit_transform(df)
    print(f"   ✅ Features after engineering: {len(df_eng.columns)}\n")

    # ─── Step 4: Preprocessing ───
    print("⚙️ [4/8] Preprocessing & splitting data...")
    # Separate target
    y_raw = df_eng[config.TARGET_COLUMN]
    X_raw = df_eng.drop(columns=[config.TARGET_COLUMN])
    
    # Drop non-numeric columns that aren't in our feature lists
    feature_cols = []
    for col in X_raw.columns:
        if X_raw[col].dtype in ['float64', 'float32', 'int64', 'int32', 'bool']:
            feature_cols.append(col)
        elif col in config.CATEGORICAL_FEATURES:
            feature_cols.append(col)
    
    X_selected = X_raw[feature_cols].copy()
    
    # One-hot encode categoricals
    cat_cols = [c for c in config.CATEGORICAL_FEATURES if c in X_selected.columns]
    if cat_cols:
        X_selected = pd.get_dummies(X_selected, columns=cat_cols, drop_first=False)
    
    # Convert booleans to int
    for col in X_selected.columns:
        if X_selected[col].dtype == 'bool':
            X_selected[col] = X_selected[col].astype(int)
    
    # Fill NaN
    X_selected = X_selected.fillna(-1)
    
    # Encode target
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    le = LabelEncoder()
    y_encoded = le.fit_transform(y_raw)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_selected)
    feature_names = list(X_selected.columns)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, 
        test_size=config.TEST_SIZE, 
        random_state=config.RANDOM_SEED, 
        stratify=y_encoded
    )
    print(f"   ✅ Train: {X_train.shape}, Test: {X_test.shape}\n")

    # ─── Step 5: Train Individual Models ───
    print("🤖 [5/8] Training base models...")
    trainer = ModelTrainer(random_seed=config.RANDOM_SEED)
    comparison_df = trainer.train_all(X_train, y_train, X_test, y_test)
    print("\n   📋 Model Comparison:")
    print(comparison_df[['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'Train Time (s)']].to_string(index=False))
    print()

    # ─── Step 6: Stacking Ensemble ───
    print("🏆 [6/8] Training Stacking Ensemble...")
    # Use top models for stacking (skip DNN for speed)
    base_models_for_stack = [
        (name, model) for name, model in trainer.models.items() 
        if name != 'DNN'
    ]
    
    stacking = StackingEnsembleClassifier(
        base_models=base_models_for_stack,
        cv=5,
        use_proba=True
    )
    stacking.fit(X_train, y_train)
    
    y_pred_stack = stacking.predict(X_test)
    stack_acc = accuracy_score(y_test, y_pred_stack)
    stack_prec = precision_score(y_test, y_pred_stack, average='weighted', zero_division=0)
    stack_rec = recall_score(y_test, y_pred_stack, average='weighted', zero_division=0)
    stack_f1 = f1_score(y_test, y_pred_stack, average='weighted', zero_division=0)
    stack_cm = confusion_matrix(y_test, y_pred_stack)
    stack_report = classification_report(y_test, y_pred_stack, target_names=le.classes_, output_dict=True, zero_division=0)
    
    print(f"\n   🏆 STACKING ENSEMBLE RESULTS:")
    print(f"   ┌───────────────────────────────────┐")
    print(f"   │  Accuracy:   {stack_acc:.4f}              │")
    print(f"   │  Precision:  {stack_prec:.4f}              │")
    print(f"   │  Recall:     {stack_rec:.4f}              │")
    print(f"   │  F1-Score:   {stack_f1:.4f}              │")
    print(f"   └───────────────────────────────────┘\n")

    # ─── Step 7: Save Everything ───
    print("💾 [7/8] Saving all artifacts...")
    models_dir = config.DIRS['models']
    metrics_dir = config.DIRS['metrics']
    
    # Save models
    trainer.save_results(models_dir)
    
    with open(os.path.join(models_dir, 'stacking_ensemble.pkl'), 'wb') as f:
        pickle.dump(stacking, f)
    
    with open(os.path.join(models_dir, 'scaler.pkl'), 'wb') as f:
        pickle.dump(scaler, f)
    
    with open(os.path.join(models_dir, 'label_encoder.pkl'), 'wb') as f:
        pickle.dump(le, f)
    
    with open(os.path.join(models_dir, 'feature_names.pkl'), 'wb') as f:
        pickle.dump(feature_names, f)
    
    # Save metrics
    os.makedirs(metrics_dir, exist_ok=True)
    
    # Add stacking to comparison
    stack_row = pd.DataFrame([{
        'Model': 'Stacking Ensemble',
        'Accuracy': stack_acc,
        'Precision': stack_prec,
        'Recall': stack_rec,
        'F1-Score': stack_f1,
        'Train Time (s)': 0
    }])
    full_comparison = pd.concat([comparison_df, stack_row], ignore_index=True)
    full_comparison = full_comparison.sort_values('F1-Score', ascending=False)
    full_comparison.to_csv(os.path.join(metrics_dir, 'model_comparison.csv'), index=False)
    
    # Save confusion matrices
    all_results = trainer.results.copy()
    all_results['Stacking Ensemble'] = {
        'Accuracy': stack_acc,
        'Precision': stack_prec,
        'Recall': stack_rec,
        'F1-Score': stack_f1,
        'Confusion Matrix': stack_cm.tolist(),
        'Classification Report': stack_report
    }
    
    with open(os.path.join(metrics_dir, 'all_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    # Save feature importance (from Random Forest)
    rf_model = trainer.models.get('Random Forest')
    if rf_model and hasattr(rf_model, 'feature_importances_'):
        feat_imp = pd.DataFrame({
            'Feature': feature_names[:len(rf_model.feature_importances_)],
            'Importance': rf_model.feature_importances_
        }).sort_values('Importance', ascending=False)
        feat_imp.to_csv(os.path.join(metrics_dir, 'feature_importance.csv'), index=False)
    
    # Save class names
    with open(os.path.join(models_dir, 'class_names.pkl'), 'wb') as f:
        pickle.dump(list(le.classes_), f)
    
    print("   ✅ All models saved to models/saved/")
    print("   ✅ All metrics saved to reports/metrics/")
    
    # ─── Step 8: Quick Demo ───
    print("\n♻️ [8/8] Demo: Recovery & Environmental Impact...")
    recovery = RecoveryRecommendationEngine()
    env_calc = EnvironmentalImpactCalculator()
    
    for device in ['Mobile Phones', 'Laptops', 'PCBs/Circuit Boards']:
        rec = recovery.get_recommendation(device)
        env = env_calc.calculate_impact(device, quantity=100)
        print(f"\n   📱 {device}:")
        print(f"      Recovery Value: ${rec['estimated_value_usd']:.2f}")
        print(f"      Method: {rec['recovery_method']}")
        print(f"      CO2 Saved (100 units): {env['co2_saved_kg']:.1f} kg")
    
    print("\n" + "=" * 70)
    print("🎉 PIPELINE COMPLETE! All models trained and saved successfully.")
    print(f"🏆 Best Model: {full_comparison.iloc[0]['Model']} (F1: {full_comparison.iloc[0]['F1-Score']:.4f})")
    print("🌐 Run the Streamlit app: streamlit run app/streamlit_app.py")
    print("=" * 70)


if __name__ == '__main__':
    main()
