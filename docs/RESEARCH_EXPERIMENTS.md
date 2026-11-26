# Research Experiments Documentation
## E-WASTE AI — Phase 3: Experiment Management

> [!IMPORTANT]
> All experiment results use **actual training** on the specified dataset.
> Synthetic data experiments are clearly labeled as synthetic.
> Real dataset results are never mixed with synthetic test results.

---

## 1. Experiment Tracker

```python
from research.experiments.experiment_tracker import ExperimentTracker

tracker = ExperimentTracker()

# Start an experiment
exp_id = tracker.start_experiment(
    name="E-Waste Category Classification — Random Forest Baseline",
    objective="Establish baseline accuracy for 5-class e-waste category classification",
    dataset_info={
        "source": "ewaste_classification_data.csv",
        "n_rows": 5000,
        "n_features": 12,
        "n_classes": 5,
        "split": "80/10/10 train/val/test",
    },
    config={
        "algorithm": "random_forest",
        "n_estimators": 100,
        "seed": 42,
        "imbalance_strategy": "class_weight",
    },
)

# Log metrics after training
tracker.log_metrics(exp_id, {
    "val_accuracy": 0.8742,
    "val_f1_macro": 0.8615,
    "test_accuracy": 0.8690,
    "test_f1_macro": 0.8578,
    "training_time_sec": 12.4,
})

# Log an artifact
tracker.log_artifact(exp_id, "models/saved/rf_baseline.pkl", artifact_type="model")

# Close experiment
tracker.end_experiment(exp_id, status="completed")
```

---

## 2. Experiment Index

Experiments are stored in-memory during the session. The `ExperimentTracker` also supports a low-level `create_experiment` / `start_run` / `finish_run` API for fine-grained tracking:

```python
# Low-level API (for detailed per-epoch tracking)
exp = tracker.create_experiment(
    name="CNN Image Classifier",
    description="MobileNetV3 on e-waste image dataset",
    hypothesis="Transfer learning will outperform training from scratch",
)
run_id = tracker.start_run(exp["id"], config={"lr": 0.001, "epochs": 20}, model_name="mobilenetv3")
tracker.log_metric(run_id, "accuracy", 0.72, epoch=1)
tracker.log_metric(run_id, "accuracy", 0.81, epoch=10)
tracker.finish_run(run_id, status="completed")
```

---

## 3. Comparison Table

```python
table = tracker.generate_comparison_table([exp_id_1, exp_id_2, exp_id_3])
# Returns a pandas DataFrame with columns: experiment_id, name, status, duration_sec, + metrics
print(table.to_string())
```

---

## 4. Reproducibility Requirements

For research papers using this platform, record:

| Element | Where to find it |
|---------|-----------------|
| Random seed | `config["seed"]` in experiment |
| Dataset version | `dataset_info["source"]` + file hash |
| Split ratios | `dataset_info["split"]` |
| Algorithm + hyperparameters | `config` in experiment |
| Library versions | `library_versions` field (auto-captured) |
| Training hardware | Add manually: CPU model, RAM |
| Evaluation protocol | Record in `objective` field |

---

## 5. Phase 3 Baseline Experiments (Synthetic Data)

> [!NOTE]
> The following experiments were run on **synthetic datasets** for validation only.
> They are NOT research results. Real results require the actual e-waste datasets.

Synthetic experiment baselines (200 samples, 8 features, 3 classes, seed=42):

| Algorithm | Val Accuracy | Val F1 (macro) | Duration (s) |
|-----------|-------------|----------------|--------------|
| Random Forest | _run to verify_ | _run to verify_ | _run to verify_ |
| Logistic Regression | _run to verify_ | _run to verify_ | _run to verify_ |
| Hist Gradient Boosting | _run to verify_ | _run to verify_ | _run to verify_ |

> Run `python scripts/run_synthetic_baselines.py` to generate actual values.

---

## 6. Research Notes

- **Quality scores** are diagnostic indicators, NOT ISO or scientific standards
- **Model comparisons** use `f1_macro` for classification, `r2` for regression — not accuracy alone
- **Test set metrics** are reported once per final model, never used for tuning
- **Data provenance** must be recorded before claiming generalizable results

> [!CAUTION]
> Do NOT mix synthetic test experiment results with real dataset results in publications.
> Always state clearly whether results are from real or synthetic data.
