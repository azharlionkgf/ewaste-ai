# Model Registry Documentation
## E-WASTE AI — Phase 3: Model Version Management

> [!NOTE]
> The Model Registry provides persistent versioning, activation, and comparison of trained models.
> It is backed by a JSON file at `models/registry/registry.json`.

---

## 1. Architecture

```
models/
├── saved/           # Serialized model files (.pkl, .pt)
├── history/         # Per-run training history JSON files
└── registry/
    └── registry.json   # Persistent registry index
```

---

## 2. Usage

### Register a Model
```python
from ml.models.model_version_registry import ModelRegistry

registry = ModelRegistry()

entry_id = registry.register(
    run_name="ewaste_rf_v1",
    model_path="models/saved/ewaste_rf_v1.pkl",
    metadata={
        "algorithm": "random_forest",
        "task": "classification",
        "train_metrics": {"accuracy": 0.92, "f1_macro": 0.90},
        "val_metrics":   {"accuracy": 0.87, "f1_macro": 0.85},
        "test_metrics":  {"accuracy": 0.86, "f1_macro": 0.84},
        "class_names": ["Laptop", "Mobile", "Monitor"],
        "seed": 42,
        "dataset_name": "ewaste_classification_data.csv",
    }
)
print(entry_id)  # e.g. "ewaste_rf_v1_20261126_120000"
```

### Activate a Model
```python
registry.activate(entry_id)
# Sets status = "active"; archives previous active model for the same algorithm
```

### List All Models
```python
entries = registry.list_all()
for e in entries:
    print(e["run_name"], e["algorithm"], e["status"], e["val_metrics"].get("accuracy"))
```

### Compare Versions
```python
comparison = registry.compare_versions([entry_id_1, entry_id_2, entry_id_3])
for row in comparison:
    print(row["algorithm"], row["val_acc"], row["test_acc"], row["status"])
```

### Load a Model
```python
model = registry.load_model(entry_id)
predictions = model.predict(X_new)
```

---

## 3. Registry Entry Schema

| Field | Type | Description |
|-------|------|-------------|
| `entry_id` | str | Unique identifier (`{run_name}_{timestamp}`) |
| `run_name` | str | Human-readable name for the training run |
| `algorithm` | str | Algorithm identifier (e.g. `random_forest`) |
| `task` | str | `classification` or `regression` |
| `status` | str | `registered` → `active` → `archived` |
| `train_metrics` | dict | Metrics on training set |
| `val_metrics` | dict | Metrics on validation set |
| `test_metrics` | dict | Metrics on test set |
| `model_path` | str | Absolute path to saved model file |
| `model_size_kb` | float | Size of model file in KB |
| `random_seed` | int | Seed used during training |
| `registered_at` | str | ISO 8601 timestamp |
| `library_versions` | dict | sklearn, numpy, pandas versions at training time |

---

## 4. Status Lifecycle

```
registered  →  active    (via activate())
active      →  archived  (automatically when a newer model is activated)
registered  →  archived  (via archive())
```

> [!TIP]
> Only one model per algorithm can be `active` at a time.
> All previous versions are retained in `archived` status.

---

## 5. Export Metadata

```python
registry.export_metadata(entry_id, output_path="exports/model_meta.json")
```

---

## 6. Training Service (DB Integration)

For applications that need database persistence alongside the file registry:

```python
from backend.services.training_service import TrainingService

service = TrainingService(db_session=db)   # or db_session=None for memory mode

run_id = service.create_run(
    config={"algorithm": "random_forest", "task": "classification", "seed": 42},
    dataset_id=1,
)
service.update_status(run_id, "running")
service.save_metrics(run_id, train_metrics, val_metrics, test_metrics)
service.update_status(run_id, "completed", model_path="models/saved/my_run.pkl")

runs = service.list_runs(status="completed")
```

> [!IMPORTANT]
> `TrainingService` falls back to in-memory mode automatically when the database is unavailable.
> This ensures the training pipeline works even without a running database.
