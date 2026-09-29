"""
Data preprocessing pipeline for E-Waste classification.
"""
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from src.utils import get_logger, setup_directories

logger = get_logger(__name__)

class DataPreprocessor:
    def __init__(self):
        self.num_features = config.NUMERICAL_FEATURES
        self.cat_features = config.CATEGORICAL_FEATURES
        self.bin_features = config.BINARY_FEATURES
        self.target = config.TARGET_COLUMN
        
        self.target_encoder = LabelEncoder()
        
        self.num_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        self.cat_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        self.bin_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent'))
        ])
        
        self.preprocessor = ColumnTransformer([
            ('num', self.num_pipeline, self.num_features),
            ('cat', self.cat_pipeline, self.cat_features),
            ('bin', self.bin_pipeline, self.bin_features)
        ])
        self.feature_names_out = None
        
    def fit_transform(self, df):
        logger.info("Fitting and transforming data...")
        X = df.drop(columns=[self.target])
        y = df[self.target]
        
        # Handle conditional missing values
        for col, indicator in zip(['battery_health_pct', 'screen_size_inch', 'storage_capacity_gb'], 
                                 ['battery_present', 'screen_present', 'data_storage_present']):
            if col in X.columns and indicator in X.columns:
                X.loc[X[indicator] == False, col] = -1
                
        y_encoded = self.target_encoder.fit_transform(y)
        X_processed = self.preprocessor.fit_transform(X)
        
        cat_names = self.preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(self.cat_features)
        self.feature_names_out = self.num_features + list(cat_names) + self.bin_features
        
        X_df = pd.DataFrame(X_processed, columns=self.feature_names_out, index=X.index)
        self.save_processors()
        return X_df, pd.Series(y_encoded, name=self.target, index=y.index)
        
    def transform(self, df):
        logger.info("Transforming data...")
        X = df.copy()
        if self.target in X.columns:
            X = X.drop(columns=[self.target])
            
        for col, indicator in zip(['battery_health_pct', 'screen_size_inch', 'storage_capacity_gb'], 
                                 ['battery_present', 'screen_present', 'data_storage_present']):
            if col in X.columns and indicator in X.columns:
                X.loc[X[indicator] == False, col] = -1
                
        X_processed = self.preprocessor.transform(X)
        return pd.DataFrame(X_processed, columns=self.feature_names_out, index=X.index)
        
    def save_processors(self):
        setup_directories()
        models_dir = config.DIRS['models']
        joblib.dump(self.target_encoder, os.path.join(models_dir, 'label_encoder.joblib'))
        joblib.dump(self.preprocessor, os.path.join(models_dir, 'preprocessor.joblib'))
        logger.info("Saved preprocessors to models directory.")

def preprocess_and_split():
    raw_path = os.path.join(config.DIRS['raw_data'], 'e_waste_data.csv')
    if not os.path.exists(raw_path):
        logger.error("Raw data not found. Run data_generator.py first.")
        return
        
    df = pd.read_csv(raw_path)
    processor = DataPreprocessor()
    X, y = processor.fit_transform(df)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_SEED, stratify=y
    )
    
    proc_dir = config.DIRS['processed_data']
    X_train.to_parquet(os.path.join(proc_dir, 'X_train.parquet'))
    X_test.to_parquet(os.path.join(proc_dir, 'X_test.parquet'))
    y_train.to_frame().to_parquet(os.path.join(proc_dir, 'y_train.parquet'))
    y_test.to_frame().to_parquet(os.path.join(proc_dir, 'y_test.parquet'))
    logger.info("Saved train/test splits to processed directory.")

if __name__ == '__main__':
    preprocess_and_split()
