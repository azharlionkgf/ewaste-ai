"""
Utility functions for E-Waste classification project.
"""
import os
import logging
import joblib
import time
from functools import wraps
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Setup plot styling
plt.style.use('dark_background')
sns.set_palette(sns.color_palette([config.COLOR_SCHEME['primary'], config.COLOR_SCHEME['accent_1'], 
                                   config.COLOR_SCHEME['accent_2'], config.COLOR_SCHEME['accent_3']]))

def setup_directories():
    """Create all required project directories."""
    for dir_path in config.DIRS.values():
        os.makedirs(dir_path, exist_ok=True)

def get_logger(name):
    """Setup and return a configured logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def timer(func):
    """Decorator to measure execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        get_logger(__name__).info(f"Function {func.__name__} took {end_time - start_time:.4f} seconds to execute.")
        return result
    return wrapper

def save_model(model, filename):
    """Save model to models directory."""
    setup_directories()
    path = os.path.join(config.DIRS['models'], filename)
    joblib.dump(model, path)
    get_logger(__name__).info(f"Model saved to {path}")

def load_model(filename):
    """Load model from models directory."""
    path = os.path.join(config.DIRS['models'], filename)
    if os.path.exists(path):
        return joblib.load(path)
    else:
        get_logger(__name__).error(f"Model file {path} not found.")
        return None

def plot_confusion_matrix(cm, class_names, title='Confusion Matrix', save_name='cm.png'):
    """Plot and save a styled confusion matrix."""
    setup_directories()
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='mako', 
                xticklabels=class_names, yticklabels=class_names,
                cbar=False, linewidths=.5, linecolor='gray')
    plt.title(title, fontsize=16, color=config.COLOR_SCHEME['text'])
    plt.ylabel('True Label', fontsize=14, color=config.COLOR_SCHEME['text'])
    plt.xlabel('Predicted Label', fontsize=14, color=config.COLOR_SCHEME['text'])
    plt.xticks(rotation=45, ha='right', color=config.COLOR_SCHEME['text'])
    plt.yticks(rotation=0, color=config.COLOR_SCHEME['text'])
    plt.tight_layout()
    plt.savefig(os.path.join(config.DIRS['figures'], save_name), dpi=300, facecolor=config.COLOR_SCHEME['background'])
    plt.close()

def plot_feature_importance(importances, features, title='Feature Importance', top_n=20, save_name='feat_imp.png'):
    """Plot and save feature importance bar chart."""
    setup_directories()
    df = pd.DataFrame({'Feature': features, 'Importance': importances})
    df = df.sort_values('Importance', ascending=False).head(top_n)
    
    plt.figure(figsize=(10, 8))
    sns.barplot(x='Importance', y='Feature', data=df, palette='viridis')
    plt.title(title, fontsize=16, color=config.COLOR_SCHEME['text'])
    plt.xlabel('Importance Score', fontsize=14, color=config.COLOR_SCHEME['text'])
    plt.ylabel('Features', fontsize=14, color=config.COLOR_SCHEME['text'])
    plt.tight_layout()
    plt.savefig(os.path.join(config.DIRS['figures'], save_name), dpi=300, facecolor=config.COLOR_SCHEME['background'])
    plt.close()

def plot_roc_curves():
    """Placeholder for ROC curve plotting"""
    pass

def plot_learning_curves():
    """Placeholder for learning curve plotting"""
    pass

def classification_report_to_df(y_true, y_pred, target_names):
    """Convert sklearn classification report to pandas DataFrame."""
    report = classification_report(y_true, y_pred, target_names=target_names, output_dict=True)
    df = pd.DataFrame(report).transpose()
    return df
