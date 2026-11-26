# Model Training Documentation
## E-WASTE AI — Phase 3: AI/ML Training Laboratory

> [!NOTE]
> This document describes the AI/ML Training Laboratory implemented in Phase 3.
> All training metrics in this documentation are from actual experiments on synthetic datasets
> clearly labeled as synthetic. No fabricated results are presented.

---

## 1. Architecture Overview

```
ml/
├── training/
│   ├── training_engine.py      # Unified training engine (tabular + CNN)
│   ├── optimizer.py            # Hyperparameter tuning + imbalance handling
│   └── callbacks.py            # Training callbacks (Phase 1 baseline)
├── models/
│   ├── tabular/
│   │   └── sklearn_models.py   # Full sklearn model factory + registries
│   ├── cnn/
│   │   └── classifier.py       # CNN architecture builder (MobileNetV3, etc.)
│   └── model_version_registry.py  # File-based model registry
├── evaluation/
│   └── evaluator.py            # Classification + regression metrics
└── inference/
    └── model_exporter.py       # Model package + report export
```

---

## 2. Supported Algorithms

### Classification
| Algorithm | ID | Speed | Interpretable |
|-----------|-----|-------|---------------|
| Logistic Regression | `logistic_regression` | Fast | Yes |
| Decision Tree | `decision_tree` | Fast | Yes |
| Random Forest | `random_forest` | Medium | Partial |
| Extra Trees | `extra_trees` | Medium | Partial |
| Support Vector Machine | `svm` | Slow | No |
| K-Nearest Neighbors | `knn` | Medium | No |
| Gradient Boosting | `gradient_boosting` | Slow | No |
| Hist Gradient Boosting | `hist_gradient_boosting` | Fast | No |
| XGBoost | `xgboost` | Fast | No |
| CatBoost | `catboost` | Medium | No |

### Regression
| Algorithm | ID |
|-----------|----|
| Linear Regression | `linear_regression` |
| Decision Tree | `decision_tree` |
| Random Forest | `random_forest` |
| Extra Trees | `extra_trees` |
| Gradient Boosting | `gradient_boosting` |
| Hist Gradient Boosting | `hist_gradient_boosting` |
| XGBoost | `xgboost` |
| SVR | `svr` |

---

## 3. Training Engine

### Usage — Tabular Training
```python
from ml.training.training_engine import TrainingEngine

engine = TrainingEngine(seed=42)
result = engine.train_tabular(
    X_train, y_train, X_val, y_val,
    algorithm="random_forest",
    task="classification",   # or "regression"
    run_name="my_experiment",
    config={"class_names": ["Laptop", "Mobile", "Monitor"]},
)

print(result["val_metrics"]["accuracy"])  # e.g. 0.8750
print(result["model_path"])              # saved model path
```

### Result Dictionary Keys
| Key | Description |
|-----|-------------|
| `algorithm` | Algorithm name |
| `task` | classification or regression |
| `train_metrics` | Metrics on training set |
| `val_metrics` | Metrics on validation set |
| `model_path` | Path to saved .pkl file |
| `duration_sec` | Training wall-clock time |
| `model` | The fitted model object |

### Usage — Image Training (CNN)
```python
result = engine.train_image(
    train_loader, val_loader,
    num_classes=5,
    architecture="mobilenetv3_small",
    config={"epochs": 10, "lr": 0.001},
    run_name="ewaste_cnn_v1",
)
```

---

## 4. Model Optimization

### Hyperparameter Tuning
```python
from ml.training.optimizer import ModelOptimizer

optimizer = ModelOptimizer()
best_model, best_params = optimizer.tune(
    algorithm="random_forest",
    X_train=X_train, y_train=y_train,
    task="classification",
    method="random",   # "random" or "grid"
    n_iter=20,
    cv=5,
    seed=42,
)
```

### Class Imbalance Handling
```python
X_res, y_res = optimizer.handle_class_imbalance(
    X_train, y_train,
    strategy="smote",   # "smote", "oversample", "none", "class_weight"
    seed=42,
)
```

| Strategy | Description |
|----------|-------------|
| `none` | No resampling |
| `oversample` | Random oversampling of minority class |
| `smote` | SMOTE synthetic oversampling (requires imbalanced-learn) |
| `class_weight` | Use `class_weight="balanced"` in model |

---

## 5. Evaluation Engine

### Classification Metrics
```python
from ml.evaluation.evaluator import evaluate_tabular

metrics = evaluate_tabular(model, X_test, y_test, task="classification", split="test")
# Returns: accuracy, precision, recall, f1_macro, f1_weighted, kappa,
#          roc_auc, pr_auc, confusion_matrix, per_class_report
```

### Regression Metrics
```python
metrics = evaluate_tabular(model, X_test, y_test, task="regression", split="test")
# Returns: mae, mse, rmse, r2, mape
```

### Model Comparison
```python
from ml.evaluation.evaluator import compare_models

comparison = compare_models({
    "rf": rf_metrics,
    "xgb": xgb_metrics,
    "lr": lr_metrics,
})
# Returns: {"ranked": [...sorted by primary metric...], "recommendation": "rf"}
```

---

## 6. CPU Performance Guidance

This system is optimized for CPU-only environments (Intel i5-1340P, 16GB RAM):

| Algorithm | 200 rows / 10 features | 10,000 rows / 50 features |
|-----------|------------------------|---------------------------|
| Logistic Regression | < 1 sec | 2–5 sec |
| Random Forest (100 trees) | 1–3 sec | 10–30 sec |
| XGBoost | 2–5 sec | 15–60 sec |
| SVM | 2–8 sec | 60–300 sec |
| CNN (MobileNetV3, 10 epochs) | 5–15 min | Varies by dataset |

> [!TIP]
> For large datasets, prefer `hist_gradient_boosting` over `gradient_boosting` —
> it is 10–100× faster with similar accuracy.

> [!IMPORTANT]
> All DataLoader calls use `num_workers=0` for Windows CPU compatibility.

---

## 7. E-Waste Specific Pipelines

Seven domain-specific pipelines are available:

| Pipeline | Task | Target Column Examples |
|----------|------|------------------------|
| E-Waste Category Classification | Classification | `category`, `ewaste_category` |
| Device Identification | Classification | `device`, `device_type` |
| Component Classification | Classification | `component`, `component_type` |
| Material Classification | Classification | `material`, `material_type` |
| Recovery Quantity Prediction | Regression | `recovery_quantity`, `recovery_kg` |
| Economic Value Prediction | Regression | `economic_value`, `value_usd` |
| Recycling Outcome Prediction | Classification | `recycling_outcome`, `outcome` |

```python
from ewaste.ai_pipelines import EwastePipelineManager

manager = EwastePipelineManager()

# Check if your dataset is compatible
result = manager.validate_dataset(df, "ewaste_category_classification")
print(result["compatible"])        # True/False
print(result["detected_target"])   # e.g. "category"
print(result["issues"])            # list of blocking problems
print(result["warnings"])          # list of non-blocking warnings

# Prepare X, y for training
prep = manager.prepare(df, "ewaste_category_classification", target_col="category")
X, y = prep["X"], prep["y"]
```

> [!CAUTION]
> Pipelines **honestly report** when required columns are missing.
> No data is invented or silently imputed.

---

## 8. Design Constraints

- **No fake training metrics** — all results from actual model fitting
- **CPU-only** — no CUDA, no GPU required anywhere
- **Synthetic test data** clearly labeled — never mixed with real research results
- **Raw datasets never modified** — only copies are processed
- **Quality scores** are diagnostic indicators, NOT scientific standards
