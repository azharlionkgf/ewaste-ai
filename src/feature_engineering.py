"""
Advanced feature engineering for E-Waste classification.
"""
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import get_logger

logger = get_logger(__name__)

class FeatureEngineer:
    def __init__(self):
        self.precious_metal_prices = {
            'gold': 60.0,
            'silver': 0.8,
            'palladium': 30.0,
            'platinum': 30.0,
            'copper': 0.008
        }
        
    def fit_transform(self, df):
        return self.transform(df)
        
    def transform(self, df):
        logger.info("Applying feature engineering...")
        df_eng = df.copy()
        
        # Volume & Densities
        if all(c in df_eng.columns for c in ['length_cm', 'width_cm', 'height_cm']):
            df_eng['volume_cm3'] = df_eng['length_cm'] * df_eng['width_cm'] * df_eng['height_cm']
            
        if 'original_price_usd' in df_eng.columns and 'weight_kg' in df_eng.columns:
            df_eng['value_density'] = df_eng['original_price_usd'] / (df_eng['weight_kg'] + 1e-5)
            
        if all(c in df_eng.columns for c in ['gold_mg', 'silver_mg', 'palladium_mg', 'platinum_mg', 'weight_kg']):
            total_precious_mg = (df_eng['gold_mg'] + df_eng['silver_mg'] + 
                                 df_eng['palladium_mg'] + df_eng['platinum_mg'])
            df_eng['metal_richness'] = total_precious_mg / (df_eng['weight_kg'] * 1e6 + 1e-5)
            
        # Hazard Score
        hazard_cols = ['lead_present', 'mercury_present', 'cadmium_present', 'chromium_present', 'bfr_present']
        if all(col in df_eng.columns for col in hazard_cols):
            df_eng['hazard_score'] = df_eng[hazard_cols].sum(axis=1) / len(hazard_cols)
            
        # Interactions
        if 'age_years' in df_eng.columns and 'condition_score' in df_eng.columns:
            df_eng['age_condition_interaction'] = df_eng['age_years'] * (10 - df_eng['condition_score'])
            
        # Material Entropy
        pct_cols = ['plastic_pct', 'metal_pct', 'glass_pct', 'pcb_pct', 'ceramic_pct']
        if all(col in df_eng.columns for col in pct_cols):
            pcts = df_eng[pct_cols].div(df_eng[pct_cols].sum(axis=1), axis=0) + 1e-5
            df_eng['material_complexity'] = - (pcts * np.log2(pcts)).sum(axis=1)
            
        # Precious Metal Value
        if all(c in df_eng.columns for c in ['gold_mg', 'silver_mg', 'palladium_mg', 'platinum_mg', 'copper_g']):
            df_eng['total_precious_metal_value_usd'] = (
                (df_eng['gold_mg'] / 1000) * self.precious_metal_prices['gold'] +
                (df_eng['silver_mg'] / 1000) * self.precious_metal_prices['silver'] +
                (df_eng['palladium_mg'] / 1000) * self.precious_metal_prices['palladium'] +
                (df_eng['platinum_mg'] / 1000) * self.precious_metal_prices['platinum'] +
                df_eng['copper_g'] * self.precious_metal_prices['copper']
            )
            
        # Recovery Potential
        if 'total_precious_metal_value_usd' in df_eng.columns and 'age_years' in df_eng.columns and 'condition_score' in df_eng.columns:
            df_eng['recovery_potential'] = df_eng['total_precious_metal_value_usd'] / (df_eng['age_years'] * (11 - df_eng['condition_score']) + 1)
            
        # Size Category
        if 'volume_cm3' in df_eng.columns:
            df_eng['size_category'] = pd.qcut(df_eng['volume_cm3'], q=5, labels=False, duplicates='drop')
            
        # Price per Component
        if 'original_price_usd' in df_eng.columns and 'component_count' in df_eng.columns:
            df_eng['price_per_component'] = df_eng['original_price_usd'] / (df_eng['component_count'] + 1)
            
        # Is High Value
        if 'original_price_usd' in df_eng.columns:
            threshold = df_eng['original_price_usd'].median()
            df_eng['is_high_value'] = (df_eng['original_price_usd'] > threshold).astype(int)
            
        # Power Density
        if 'power_consumption_watts' in df_eng.columns and 'volume_cm3' in df_eng.columns:
            df_eng['power_density'] = df_eng['power_consumption_watts'] / (df_eng['volume_cm3'] + 1e-5)
            
        # Degradation Rate
        if 'condition_score' in df_eng.columns and 'age_years' in df_eng.columns:
            df_eng['degradation_rate'] = (10 - df_eng['condition_score']) / (df_eng['age_years'] + 1e-5)
            
        # Recyclability Index (Heuristic)
        if 'metal_richness' in df_eng.columns and 'hazard_score' in df_eng.columns:
            df_eng['recyclability_index'] = df_eng['metal_richness'] / (df_eng['hazard_score'] + 0.1)

        logger.info(f"Engineered {len(df_eng.columns) - len(df.columns)} new features.")
        return df_eng
