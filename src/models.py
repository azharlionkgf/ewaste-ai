import os
import time
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, confusion_matrix, classification_report)
from sklearn.model_selection import cross_validate

class ModelTrainer:
    """Trainer class for multiple ML/DL models for E-Waste Classification."""
    def __init__(self, random_seed=42):
        self.random_seed = random_seed
        self.models = self.get_models()
        self.results = {}
    
    def get_models(self) -> dict:
        return {
            'Random Forest': RandomForestClassifier(
                n_estimators=300, max_depth=20, min_samples_split=5,
                class_weight='balanced', random_state=self.random_seed, n_jobs=-1
            ),
            'XGBoost': XGBClassifier(
                n_estimators=300, max_depth=6, learning_rate=0.15,
                use_label_encoder=False, eval_metric='mlogloss',
                random_state=self.random_seed, n_jobs=-1, tree_method='hist'
            ),
            'LightGBM': LGBMClassifier(
                n_estimators=300, max_depth=6, learning_rate=0.15,
                num_leaves=31, random_state=self.random_seed, verbose=-1, n_jobs=-1
            ),
            'CatBoost': CatBoostClassifier(
                iterations=300, depth=6, learning_rate=0.15,
                verbose=0, random_seed=self.random_seed, thread_count=-1
            ),
            'DNN': MLPClassifier(
                hidden_layer_sizes=(256, 128, 64), max_iter=300,
                early_stopping=True, activation='relu',
                random_state=self.random_seed, learning_rate='adaptive'
            )
        }
    
    def train_model(self, name, model, X_train, y_train):
        print(f"  🔄 Training {name}...", end="", flush=True)
        start_time = time.time()
        model.fit(X_train, y_train)
        elapsed = time.time() - start_time
        print(f" ✅ ({elapsed:.1f}s)")
        return elapsed
    
    def evaluate_model(self, name, model, X_test, y_test):
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        self.results[name] = {
            'Accuracy': acc, 'Precision': prec, 'Recall': rec, 'F1-Score': f1,
            'Confusion Matrix': confusion_matrix(y_test, y_pred).tolist(),
            'Classification Report': classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        }
        return self.results[name]
    
    def cross_validate(self, name, model, X, y, cv=10):
        scoring = ['accuracy', 'f1_macro', 'f1_weighted']
        scores = cross_validate(model, X, y, cv=cv, scoring=scoring, n_jobs=-1)
        return {
            'Accuracy Mean': np.mean(scores['test_accuracy']),
            'Accuracy Std': np.std(scores['test_accuracy']),
            'F1 Macro Mean': np.mean(scores['test_f1_macro']),
            'F1 Weighted Mean': np.mean(scores['test_f1_weighted'])
        }
    
    def train_all(self, X_train, y_train, X_test, y_test):
        for name, model in self.models.items():
            train_time = self.train_model(name, model, X_train, y_train)
            eval_metrics = self.evaluate_model(name, model, X_test, y_test)
            self.results[name]['Train Time (s)'] = train_time
        return self.get_comparison_df()
    
    def get_comparison_df(self):
        records = []
        for name, res in self.results.items():
            records.append({
                'Model': name,
                'Accuracy': res['Accuracy'],
                'Precision': res['Precision'],
                'Recall': res['Recall'],
                'F1-Score': res['F1-Score'],
                'Train Time (s)': res.get('Train Time (s)', 0)
            })
        return pd.DataFrame(records).sort_values(by='F1-Score', ascending=False)
    
    def save_results(self, path):
        os.makedirs(path, exist_ok=True)
        self.get_comparison_df().to_csv(os.path.join(path, 'model_comparison.csv'), index=False)
        for name, model in self.models.items():
            with open(os.path.join(path, f"{name.replace(' ', '_')}.pkl"), 'wb') as f:
                pickle.dump(model, f)
        print(f"  💾 Models saved to {path}")
