# E-WASTE AI — AI/ML Architecture

## Overview

The E-WASTE AI platform implements a complete, end-to-end machine learning pipeline that follows the academic workflow required for research and industry deployment. The pipeline is designed to work entirely on CPU (no GPU required), making it accessible for academic environments and small-to-medium recycling facilities.

> **[!IMPORTANT]**
> No pre-trained e-waste-specific models are shipped with this platform. All models must be trained by the user on their own datasets. This ensures scientific integrity and allows the platform to adapt to specific local e-waste compositions.

---

## Pipeline Stages

The complete AI/ML pipeline consists of **9 sequential stages**:

```
Stage 1: Dataset Upload
       │
       ▼
Stage 2: Dataset Inspection
       │
       ▼
Stage 3: Data Cleaning
       │
       ▼
Stage 4: Preprocessing & Feature Engineering
       │
       ▼
Stage 5: Model Selection
       │
       ▼
Stage 6: Model Training
       │
       ▼
Stage 7: Model Evaluation
       │
       ▼
Stage 8: Model Saving & Registry
       │
       ▼
Stage 9: Prediction / Inference
```

---

## Stage 1: Dataset Upload

**Supported Formats:**
- **Tabular:** CSV (`.csv`), Excel (`.xlsx`, `.xls`), JSON (`.json`)
- **Image:** JPEG, PNG, BMP (organized in class subdirectories)

**Upload Handler:** `ml/data/loaders/dataset_loader.py`

Functions:
- `load_tabular_dataset(file_path)` — Reads CSV/Excel/JSON into a pandas DataFrame
- `inspect_tabular_dataset(df)` — Returns shape, dtypes, missing counts, sample rows
- `load_image_dataset(root_dir)` — Builds image path list from directory structure
- `inspect_image_dataset(root_dir)` — Returns class names, counts, total images

---

## Stage 2: Dataset Inspection

**Purpose:** Automatically analyse the uploaded dataset for quality and completeness.

**Tabular Inspection Reports:**
| Metric | Description |
|--------|-------------|
| Shape | Rows × Columns |
| Column Types | Numeric, Categorical, Boolean, DateTime |
| Missing Values | Count and percentage per column |
| Duplicate Rows | Count and percentage |
| Class Distribution | Target variable value counts |
| Statistical Summary | Mean, std, min, max, quartiles |

**Image Inspection Reports:**
| Metric | Description |
|--------|-------------|
| Total Images | Count |
| Classes Found | Directory names as class labels |
| Class Distribution | Images per class |
| Resolution Stats | Min, max, median image dimensions |
| Format Distribution | JPEG vs PNG vs BMP counts |

---

## Stage 3: Data Cleaning

**Handler:** `ml/data/loaders/cleaner.py` — `DataCleaner` class

**Operations Performed:**
1. **Missing Value Imputation**
   - Numeric: median imputation
   - Categorical: mode imputation
   - Columns with >50% missing: flagged for removal
2. **Duplicate Removal** — Exact duplicate rows removed
3. **Outlier Detection** — IQR-based detection; flagged, not auto-removed
4. **Text Normalization** — Lowercase, strip whitespace, standardise categories
5. **Type Coercion** — String-to-numeric where appropriate
6. **Cleaning Report** — Before/after statistics, changes logged

---

## Stage 4: Preprocessing and Feature Engineering

**Handler:** `ml/data/loaders/preprocessor.py` — `DataPreprocessor` class

**Operations:**
| Operation | Description |
|-----------|-------------|
| Label Encoding | Ordinal categoricals → integer codes |
| One-Hot Encoding | Nominal categoricals → binary columns |
| Standard Scaling | Numeric features → zero mean, unit variance |
| Train/Val/Test Split | Stratified split (70% / 15% / 15%) |
| Config Serialisation | Preprocessing config saved as JSON for reproducibility |

**Output:**
- `X_train`, `X_val`, `X_test` — Feature arrays
- `y_train`, `y_val`, `y_test` — Label arrays
- `preprocessor_config.json` — Saved for use at inference time

**Image Preprocessing:**
- Resize to 224×224 (model input requirement)
- Normalize with ImageNet mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
- Data augmentation: horizontal flip, rotation, colour jitter (training only)

---

## Stage 5: Model Selection

**Supported Model Types:**

### Image Classification (CNN)
| Model | Architecture | Parameters | Notes |
|-------|-------------|------------|-------|
| `mobilenet_v3_small` | MobileNetV3-Small | ~2.5M | Fastest, best for edge/CPU |
| `mobilenet_v3_large` | MobileNetV3-Large | ~5.4M | Good accuracy/speed trade-off |
| `efficientnet_b0` | EfficientNet-B0 | ~5.3M | Excellent accuracy, moderate speed |
| `resnet50` | ResNet-50 | ~25M | Strong baseline, slower on CPU |

**Strategy:** Transfer learning from ImageNet weights. Only the classification head is trained by default; full fine-tuning optional.

### Tabular Classification
| Model | Library | Notes |
|-------|---------|-------|
| `random_forest` | scikit-learn | Fast, interpretable, feature importance |
| `xgboost` | XGBoost | High accuracy on tabular data |
| `catboost` | CatBoost | Handles categoricals natively |
| `svm` | scikit-learn | Effective for small datasets |
| `logistic_regression` | scikit-learn | Linear baseline |

---

## Stage 6: Model Training

**Handler:** `ml/training/trainer.py` — `ModelTrainer` class

### CNN Training Loop
```
for epoch in range(epochs):
    - Forward pass through CNN
    - Compute CrossEntropyLoss
    - Backpropagation + Adam optimizer
    - Validation accuracy check
    - EarlyStopping check (patience=5)
    - ProgressCallback emit (for UI progress bar)
    - Save best checkpoint
```

**Hyperparameters (defaults):**
| Parameter | Default | Description |
|-----------|---------|-------------|
| `epochs` | 20 | Maximum training epochs |
| `lr` | 0.001 | Learning rate (Adam) |
| `batch_size` | 32 | Images per batch |
| `patience` | 5 | Early stopping patience |
| `num_workers` | 0 | Windows DataLoader compatibility |

### Tabular Training
- Fit `sklearn` or `xgboost` model on `X_train`, `y_train`
- Evaluate on `X_val` immediately after fit
- Save model using `joblib`

**Callbacks:** `ml/training/callbacks.py`
- `EarlyStopping` — Stops training when val_accuracy plateaus
- `ProgressCallback` — Emits epoch progress dict for UI streaming

---

## Stage 7: Model Evaluation

**Handler:** `ml/evaluation/metrics.py`

**Metrics Computed:**
| Metric | Description |
|--------|-------------|
| Accuracy | Overall correct classifications / total |
| Precision (macro) | Average precision across all classes |
| Recall (macro) | Average recall across all classes |
| F1-Score (macro) | Harmonic mean of precision and recall |
| Confusion Matrix | NxN matrix of predicted vs actual classes |
| Per-Class Report | Precision, recall, F1 for each individual class |
| Training History | Loss and accuracy curves per epoch (CNN) |

**Visualisations Generated:**
- Confusion matrix heatmap (matplotlib)
- Training history curves (loss/accuracy vs epoch)
- Per-class bar chart

---

## Stage 8: Model Saving and Registry

**Registry:** `ml/models/model_registry.py`

**Storage Structure:**
```
saved_models/
├── {model_name}_{timestamp}/
│   ├── model.pth          (CNN PyTorch state dict)
│   ├── model.joblib       (tabular sklearn model)
│   ├── metadata.json      (model_type, classes, training config, metrics)
│   └── preprocessor_config.json
```

**Registry Operations:**
- `register_model(name, path, metadata)` — Add model to registry
- `list_models()` — List all saved models with metrics
- `load_model(name)` — Load model by name
- `compare_models()` — Side-by-side metric comparison

---

## Stage 9: Prediction / Inference

**Handler:** `ml/inference/predictor.py` — `ModelPredictor` class

**Image Prediction:**
1. Load model from `saved_models/`
2. Apply ImageNet transforms to input image
3. Forward pass → logits → softmax probabilities
4. Return top-k predictions with class names and confidence scores

**Tabular Prediction:**
1. Load `joblib` model and preprocessor config
2. Encode input features using saved preprocessor
3. `predict_proba()` → class probabilities
4. Return predicted class + confidence

**Output Schema:**
```json
{
  "predicted_class": "Circuit Board",
  "confidence": 0.924,
  "top_predictions": [
    {"rank": 1, "class_name": "Circuit Board", "confidence": 0.924},
    {"rank": 2, "class_name": "Laptop", "confidence": 0.051}
  ],
  "is_estimate": false,
  "model_name": "mobilenet_v3_small_20240115",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## CPU Optimization Strategy

Since this platform targets CPU-only environments (no GPU):

| Strategy | Implementation |
|----------|---------------|
| Lightweight CNNs | MobileNetV3-Small preferred over ResNet-50 |
| Frozen backbone | Only train classification head by default |
| Small batch sizes | 16–32 images to fit in RAM |
| `num_workers=0` | Avoids Windows multiprocessing issues |
| `torch.no_grad()` | Used during validation and inference |
| Tabular first | Encourage tabular models for initial experiments |
| Quantisation | Optional INT8 quantisation for inference speedup |

**Hardware target:** Intel Core i5 (1340P or equivalent), 16GB RAM, no dedicated GPU.

---

## Model Storage and Versioning

- Each trained model is saved with a **timestamp-based directory name**
- `metadata.json` records: model_name, model_type, num_classes, class_names, training_date, epochs_run, best_val_accuracy, dataset_id
- Multiple versions of the same model type can coexist in `saved_models/`
- The model registry lists all saved models and their metrics for comparison
- Future versions may integrate MLflow for experiment tracking

---

## Supported E-Waste Classification Categories

The platform supports classification into these 15 e-waste categories (defined in `config/ewaste_categories.json`):

1. Smartphone  
2. Laptop / Notebook  
3. Desktop Computer  
4. Tablet  
5. Battery (Li-Ion)  
6. Battery (Lead-Acid)  
7. Circuit Board / PCB  
8. CRT Monitor / TV  
9. LCD / LED Monitor  
10. Printer / Scanner  
11. Television (LCD/LED/OLED)  
12. Charger / Power Adapter  
13. Cable / Wire  
14. Household Electronics  
15. Industrial Electronics  

---

## Important Notes

> **[!NOTE]**
> No pre-trained e-waste models are included. Users must collect their own dataset, train models through the platform's training pipeline, and evaluate results before using predictions in industrial or research contexts.

> **[!TIP]**
> Start with tabular models (Random Forest, XGBoost) for initial experiments. They train in seconds on CPU and provide solid baselines for comparison with deep learning models.

> **[!WARNING]**
> Never report AI prediction results as ground truth without human verification, especially for high-hazmat devices (CRTs, NiCd batteries). The platform enforces `is_estimate=True` flags on all predictions until validated.
