# Model Evaluation Documentation
## E-WASTE AI — Phase 3: Evaluation Engine

> [!NOTE]
> All evaluation metrics are computed from actual model outputs on specified data splits.
> No metrics are fabricated. Quality scores are diagnostic indicators, NOT scientific standards.

---

## 1. Classification Metrics

| Metric | Key | Description |
|--------|-----|-------------|
| Accuracy | `accuracy` | Fraction of correctly classified samples |
| Precision | `precision` | Positive predictive value (macro/binary) |
| Recall | `recall` | True positive rate (macro/binary) |
| F1 Score (macro) | `f1_macro` | Unweighted mean F1 across classes |
| F1 Score (weighted) | `f1_weighted` | Weighted mean F1 by class support |
| Cohen's Kappa | `kappa` | Agreement corrected for chance |
| ROC-AUC | `roc_auc` | Area under ROC curve (OvR for multiclass) |
| PR-AUC | `pr_auc` | Area under Precision-Recall curve |
| Confusion Matrix | `confusion_matrix` | N×N matrix of predictions vs actuals |
| Per-class Report | `per_class` | Per-class precision, recall, F1, support |

```python
from ml.evaluation.evaluator import evaluate_tabular

metrics = evaluate_tabular(
    model, X_test, y_test,
    task="classification",
    split="test",
    class_names=["Laptop", "Mobile", "Monitor"],
)

print(f"Accuracy: {metrics['accuracy']:.4f}")
print(f"F1 (macro): {metrics['f1_macro']:.4f}")
print(f"ROC-AUC: {metrics.get('roc_auc', 'N/A')}")
```

---

## 2. Regression Metrics

| Metric | Key | Description |
|--------|-----|-------------|
| MAE | `mae` | Mean Absolute Error |
| MSE | `mse` | Mean Squared Error |
| RMSE | `rmse` | Root Mean Squared Error |
| R² | `r2` | Coefficient of determination (1.0 = perfect) |
| MAPE | `mape` | Mean Absolute Percentage Error (%) |

```python
metrics = evaluate_tabular(
    model, X_test, y_test,
    task="regression",
    split="test",
)

print(f"MAE:  {metrics['mae']:.4f}")
print(f"RMSE: {metrics['rmse']:.4f}")
print(f"R²:   {metrics['r2']:.4f}")
```

---

## 3. Cross-Validation

```python
from ml.evaluation.evaluator import cross_validate_model

result = cross_validate_model(
    model, X, y,
    task="classification",
    cv=5,
    seed=42,
)

# Returns: cv_folds, test_accuracy_mean, test_accuracy_std, test_f1_macro_mean, ...
print(f"CV Accuracy: {result['test_accuracy_mean']:.4f} ± {result['test_accuracy_std']:.4f}")
```

---

## 4. Model Comparison

```python
from ml.evaluation.evaluator import compare_models

# Pass a list of full training result dicts from TrainingEngine.train_tabular()
comparison = compare_models([result_rf, result_lr, result_xgb])

print(comparison["recommendation"])
for row in comparison["comparison_table"]:
    print(f"{row['algorithm']}: val_f1={row['val_f1_macro']:.4f}, overfit={row['overfit_gap']:.4f}")
```

> [!IMPORTANT]
> The comparison uses `f1_macro` for classification and `r2` for regression as the primary ranking metric.
> Accuracy alone is not used for model selection.

---

## 5. Evaluation Protocol

### Recommended Split Strategy
```
Full Dataset
    └── Train+Val (80%)  ──→  TrainingEngine.train_tabular()  ──→  Uses internally for train/val
    └── Test (20%)       ──→  engine.evaluate_on_test()       ──→  Final honest evaluation
```

### Data Leakage Prevention
- Test set is **never** used during training or hyperparameter tuning
- Validation set is used for model selection only
- Final test metrics reported once only
- Preprocessing is fitted on train only, applied to val/test

---

## 6. Handling Imbalanced Datasets

When class distribution is uneven:
- Use `f1_macro` (not accuracy) as primary metric
- Examine per-class precision and recall
- Consider `class_weight="balanced"` or SMOTE oversampling
- ROC-AUC gives a robust imbalance-resistant signal

> [!WARNING]
> Accuracy can be misleadingly high on imbalanced datasets.
> A model predicting the majority class 100% achieves high accuracy but zero recall on minority classes.
