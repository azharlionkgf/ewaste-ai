import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier

class StackingEnsembleClassifier:
    """Stacking ensemble to combine predictions of multiple base models."""
    def __init__(self, base_models=None, meta_model=None, use_proba=True, cv=5):
        self.base_models = base_models if base_models else []
        self.meta_model = meta_model if meta_model else LogisticRegression(max_iter=1000)
        self.use_proba = use_proba
        self.cv = cv
        self.classes_ = None
        
    def fit(self, X, y):
        X_arr = np.array(X)
        y_arr = np.array(y)
        self.classes_ = np.unique(y_arr)
        
        kf = StratifiedKFold(n_splits=self.cv, shuffle=True, random_state=42)
        meta_features = []
        
        print("Training base models to generate meta-features...")
        
        # Out-of-fold predictions
        for name, model in self.base_models:
            print(f"OOF predictions for {name}...")
            if self.use_proba:
                oof_preds = np.zeros((len(X_arr), len(self.classes_)))
            else:
                oof_preds = np.zeros((len(X_arr), 1))
                
            for train_idx, val_idx in kf.split(X_arr, y_arr):
                X_train_fold, y_train_fold = X_arr[train_idx], y_arr[train_idx]
                X_val_fold = X_arr[val_idx]
                
                model.fit(X_train_fold, y_train_fold)
                if self.use_proba:
                    oof_preds[val_idx] = model.predict_proba(X_val_fold)
                else:
                    oof_preds[val_idx, 0] = model.predict(X_val_fold)
            
            meta_features.append(oof_preds)
            
        meta_features = np.hstack(meta_features)
        
        print("Training meta model...")
        self.meta_model.fit(meta_features, y_arr)
        
        print("Retraining base models on full data...")
        for name, model in self.base_models:
            model.fit(X_arr, y_arr)
            
        return self
        
    def _get_meta_features(self, X):
        meta_features = []
        for name, model in self.base_models:
            if self.use_proba:
                meta_features.append(model.predict_proba(X))
            else:
                meta_features.append(model.predict(X).reshape(-1, 1))
        return np.hstack(meta_features)
        
    def predict(self, X):
        meta_features = self._get_meta_features(X)
        return self.meta_model.predict(meta_features)
        
    def predict_proba(self, X):
        meta_features = self._get_meta_features(X)
        return self.meta_model.predict_proba(meta_features)
        
    def get_feature_importance(self):
        if hasattr(self.meta_model, 'coef_'):
            return self.meta_model.coef_
        elif hasattr(self.meta_model, 'feature_importances_'):
            return self.meta_model.feature_importances_
        return None

class VotingEnsemble:
    """Soft voting ensemble to average out probabilities of base models."""
    def __init__(self, estimators, voting='soft'):
        self.voting = voting
        self.ensemble = VotingClassifier(estimators=estimators, voting=self.voting)
        
    def fit(self, X, y):
        self.ensemble.fit(X, y)
        return self
        
    def predict(self, X):
        return self.ensemble.predict(X)
        
    def predict_proba(self, X):
        if self.voting == 'soft':
            return self.ensemble.predict_proba(X)
        raise NotImplementedError("predict_proba is only available for soft voting")
