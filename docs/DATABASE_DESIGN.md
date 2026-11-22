# 🗄️ E-WASTE AI — DATABASE DESIGN
## Complete Entity Relationship and Schema Documentation

**Version:** 2.0.0 | **Date:** 2026-11-22  
**Engine:** SQLite 3 via SQLAlchemy 2.0 ORM

---

## 1. ENTITY RELATIONSHIP DIAGRAM

```
DATASETS ──────────────┬──────────────── CLEANING_RUNS
    │                  │                      │
    │                  │                      ▼
    │            PREPROCESSING_CONFIGS   CLEANING_REPORTS
    │                  │
    │                  ▼
    │           TRAINING_RUNS ─────────────── MODEL_REGISTRY
    │                                              │
    │                                        ML_EVALUATIONS
    │
    ├──────── WASTE_BATCHES ──────────────── BATCH_ITEMS
    │               │                            │
    │               │                       ITEM_CLASSIFICATIONS
    │               │                            │
    │               │                       ITEM_COMPONENTS
    │               │                            │
    │               │                       MATERIAL_RECOVERY
    │               │
    │               └──────────────────────── ECONOMIC_VALUATIONS
    │                                               │
    │                                         RECOVERY_REPORTS
    │
    └──────── RESEARCH_EXPERIMENTS ─────── EXPERIMENT_RUNS
                                                  │
                                            EXPERIMENT_METRICS
```

---

## 2. TABLE SCHEMAS

### 2.1 DATASETS

Stores metadata for every uploaded dataset (CSV, Excel, JSON, images).

```sql
CREATE TABLE datasets (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    version         TEXT NOT NULL DEFAULT '1.0',
    file_type       TEXT NOT NULL,          -- 'csv', 'excel', 'json', 'images'
    file_path       TEXT NOT NULL,          -- relative path in /data/uploads/
    row_count       INTEGER,
    column_count    INTEGER,
    image_count     INTEGER,                -- for image datasets
    file_size_mb    REAL,
    description     TEXT,
    tags            TEXT,                   -- JSON array: ["ewaste", "phones"]
    source          TEXT,                   -- Where dataset came from
    license         TEXT,                   -- Dataset license info
    checksum        TEXT,                   -- SHA256 for integrity
    status          TEXT DEFAULT 'uploaded', -- 'uploaded'|'cleaned'|'preprocessed'|'trained'
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.2 CLEANING_RUNS

Records every automated data cleaning operation.

```sql
CREATE TABLE cleaning_runs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id          INTEGER NOT NULL REFERENCES datasets(id),
    missing_before      INTEGER DEFAULT 0,
    missing_after       INTEGER DEFAULT 0,
    duplicates_found    INTEGER DEFAULT 0,
    duplicates_removed  INTEGER DEFAULT 0,
    outliers_flagged    INTEGER DEFAULT 0,
    outliers_removed    INTEGER DEFAULT 0,
    type_errors_fixed   INTEGER DEFAULT 0,
    cleaning_config     TEXT,               -- JSON config used
    output_file_path    TEXT,               -- path to cleaned dataset
    summary             TEXT,               -- human-readable summary
    status              TEXT DEFAULT 'pending',
    run_at              DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.3 PREPROCESSING_CONFIGS

Stores preprocessing pipeline configuration for reproducibility.

```sql
CREATE TABLE preprocessing_configs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id          INTEGER NOT NULL REFERENCES datasets(id),
    scaler_type         TEXT,               -- 'standard'|'minmax'|'robust'|'none'
    encoder_type        TEXT,               -- 'onehot'|'label'|'ordinal'|'none'
    feature_columns     TEXT,               -- JSON array of selected features
    target_column       TEXT,
    train_ratio         REAL DEFAULT 0.70,
    val_ratio           REAL DEFAULT 0.15,
    test_ratio          REAL DEFAULT 0.15,
    augmentation_config TEXT,               -- JSON: image augmentation settings
    output_dir          TEXT,               -- path to split datasets
    config_hash         TEXT,               -- hash for reproducibility
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.4 TRAINING_RUNS

Records every model training job with full reproducibility info.

```sql
CREATE TABLE training_runs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id          INTEGER NOT NULL REFERENCES datasets(id),
    preprocessing_id    INTEGER REFERENCES preprocessing_configs(id),
    model_name          TEXT NOT NULL,      -- human-readable name
    model_type          TEXT NOT NULL,      -- 'cnn'|'random_forest'|'xgboost'|'catboost'|'svm'
    architecture        TEXT,               -- e.g., 'mobilenetv3_small'
    hyperparameters     TEXT NOT NULL,      -- JSON: lr, epochs, batch_size, etc.
    random_seed         INTEGER DEFAULT 42,
    num_classes         INTEGER,
    class_names         TEXT,               -- JSON array
    epochs_planned      INTEGER,
    epochs_completed    INTEGER DEFAULT 0,
    best_epoch          INTEGER,
    final_train_loss    REAL,
    final_val_loss      REAL,
    final_train_acc     REAL,
    final_val_acc       REAL,
    training_duration_s REAL,
    model_path          TEXT,               -- path to saved model weights
    status              TEXT DEFAULT 'pending', -- 'pending'|'running'|'completed'|'failed'
    error_message       TEXT,
    started_at          DATETIME,
    completed_at        DATETIME,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.5 ML_EVALUATIONS

Stores comprehensive evaluation metrics for each trained model.

```sql
CREATE TABLE ml_evaluations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    training_run_id     INTEGER NOT NULL REFERENCES training_runs(id),
    dataset_split       TEXT DEFAULT 'test',  -- 'val'|'test'
    accuracy            REAL,
    precision_macro     REAL,
    precision_weighted  REAL,
    recall_macro        REAL,
    recall_weighted     REAL,
    f1_macro            REAL,
    f1_weighted         REAL,
    roc_auc             REAL,
    cohen_kappa         REAL,
    confusion_matrix    TEXT,               -- JSON 2D array
    classification_report TEXT,            -- JSON full sklearn report
    per_class_metrics   TEXT,              -- JSON per-class breakdown
    training_history    TEXT,              -- JSON loss/acc per epoch
    evaluated_at        DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.6 WASTE_BATCHES

Industrial module: tracks physical incoming e-waste batches.

```sql
CREATE TABLE waste_batches (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_code          TEXT UNIQUE NOT NULL,  -- e.g., 'BATCH-2026-001'
    source_name         TEXT,                  -- company/individual name
    source_type         TEXT,                  -- 'corporate'|'household'|'municipal'|'retail'
    received_date       DATE NOT NULL,
    total_weight_kg     REAL,
    item_count          INTEGER,
    location            TEXT,                  -- storage location code
    status              TEXT DEFAULT 'received', 
                        -- 'received'|'sorting'|'classified'|'processing'|'completed'
    notes               TEXT,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.7 BATCH_ITEMS

Individual items within a waste batch.

```sql
CREATE TABLE batch_items (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id            INTEGER NOT NULL REFERENCES waste_batches(id),
    item_code           TEXT UNIQUE NOT NULL,  -- e.g., 'ITEM-2026-001-001'
    image_path          TEXT,                  -- uploaded image path
    weight_kg           REAL,
    condition           TEXT,                  -- 'working'|'damaged'|'broken'|'scrap'
    status              TEXT DEFAULT 'pending',
    notes               TEXT,
    registered_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.8 ITEM_CLASSIFICATIONS

AI classification result for each batch item.

```sql
CREATE TABLE item_classifications (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id             INTEGER NOT NULL REFERENCES batch_items(id),
    model_id            INTEGER REFERENCES training_runs(id),
    device_category     TEXT,               -- 'smartphone'|'laptop'|'pcb'|etc.
    device_subcategory  TEXT,               -- 'android_phone'|'gaming_laptop'|etc.
    brand_estimate      TEXT,               -- best-guess brand (not guaranteed)
    confidence_score    REAL,               -- 0.0 - 1.0
    hazard_level        TEXT,               -- 'low'|'medium'|'high'|'critical'
    hazardous_materials TEXT,               -- JSON: ['lead','mercury','cadmium']
    top_predictions     TEXT,               -- JSON: [{label, confidence}...]
    classified_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.9 ITEM_COMPONENTS

Components identified within each classified item.

```sql
CREATE TABLE item_components (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id             INTEGER NOT NULL REFERENCES batch_items(id),
    classification_id   INTEGER REFERENCES item_classifications(id),
    component_name      TEXT NOT NULL,      -- 'motherboard'|'battery'|'screen'|etc.
    component_category  TEXT,               -- 'electronic'|'mechanical'|'chemical'
    quantity            INTEGER DEFAULT 1,
    weight_estimate_g   REAL,
    condition           TEXT,
    is_recoverable      BOOLEAN DEFAULT TRUE,
    recovery_difficulty TEXT,               -- 'easy'|'medium'|'hard'
    notes               TEXT
);
```

### 2.10 MATERIAL_RECOVERY

Estimated recoverable materials per item.

```sql
CREATE TABLE material_recovery (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id             INTEGER NOT NULL REFERENCES batch_items(id),
    material_name       TEXT NOT NULL,      -- 'gold'|'silver'|'copper'|'lithium'|etc.
    material_category   TEXT,               -- 'precious_metal'|'base_metal'|'polymer'|'rare_earth'
    estimated_weight_g  REAL,               -- estimated weight to recover
    purity_percent      REAL,               -- estimated purity
    recovery_method     TEXT,               -- 'hydrometallurgy'|'pyrometallurgy'|'mechanical'
    recovery_efficiency REAL,               -- expected yield efficiency (0-1)
    is_estimate         BOOLEAN DEFAULT TRUE, -- always flag estimates
    data_source         TEXT,               -- source of composition data
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.11 ECONOMIC_VALUATIONS

Economic value estimates per batch or item.

```sql
CREATE TABLE economic_valuations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id            INTEGER REFERENCES waste_batches(id),
    item_id             INTEGER REFERENCES batch_items(id),
    valuation_date      DATE NOT NULL,
    total_estimated_value_usd REAL,
    gold_value_usd      REAL,
    silver_value_usd    REAL,
    copper_value_usd    REAL,
    lithium_value_usd   REAL,
    other_metals_usd    REAL,
    processing_cost_usd REAL,
    net_value_usd       REAL,               -- total_estimated - processing_cost
    price_data_source   TEXT,               -- 'manual'|'lme'|'kitco'
    price_date          DATE,               -- date of market prices used
    is_estimate         BOOLEAN DEFAULT TRUE,
    notes               TEXT,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.12 RESEARCH_EXPERIMENTS

Academic research experiment registry.

```sql
CREATE TABLE research_experiments (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_name     TEXT NOT NULL,
    research_question   TEXT,
    hypothesis          TEXT,
    dataset_ids         TEXT,               -- JSON array of dataset IDs used
    methodology         TEXT,
    baseline_reference  TEXT,               -- paper or model being compared against
    expected_outcome    TEXT,
    tags                TEXT,               -- JSON: ['classification','transfer_learning']
    status              TEXT DEFAULT 'planning', -- 'planning'|'running'|'completed'
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at        DATETIME
);
```

### 2.13 EXPERIMENT_RUNS

Individual runs within a research experiment.

```sql
CREATE TABLE experiment_runs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id       INTEGER NOT NULL REFERENCES research_experiments(id),
    training_run_id     INTEGER REFERENCES training_runs(id),
    run_name            TEXT,
    run_description     TEXT,
    hyperparameters     TEXT,               -- JSON
    dataset_version     TEXT,
    preprocessing_version TEXT,
    random_seed         INTEGER,
    result_summary      TEXT,               -- JSON: key metrics
    notes               TEXT,
    run_at              DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.14 EXPERIMENT_METRICS

Detailed metrics per experiment run (supports custom metrics).

```sql
CREATE TABLE experiment_metrics (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_run_id   INTEGER NOT NULL REFERENCES experiment_runs(id),
    metric_name         TEXT NOT NULL,      -- 'accuracy'|'f1_macro'|'inference_time_ms'
    metric_value        REAL NOT NULL,
    metric_type         TEXT,               -- 'primary'|'secondary'|'custom'
    split              TEXT,               -- 'train'|'val'|'test'
    recorded_at         DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 3. INDEXES

```sql
-- Performance indexes
CREATE INDEX idx_datasets_status ON datasets(status);
CREATE INDEX idx_training_runs_status ON training_runs(status);
CREATE INDEX idx_training_runs_dataset ON training_runs(dataset_id);
CREATE INDEX idx_batch_items_batch ON batch_items(batch_id);
CREATE INDEX idx_item_classifications_item ON item_classifications(item_id);
CREATE INDEX idx_material_recovery_item ON material_recovery(item_id);
CREATE INDEX idx_experiment_runs_experiment ON experiment_runs(experiment_id);
CREATE INDEX idx_experiment_metrics_run ON experiment_metrics(experiment_run_id);
```

---

## 4. DATABASE VIEWS

```sql
-- Batch summary view
CREATE VIEW v_batch_summary AS
SELECT 
    wb.id, wb.batch_code, wb.source_name, wb.received_date,
    wb.total_weight_kg, wb.status,
    COUNT(bi.id) as item_count,
    COUNT(ic.id) as classified_count,
    AVG(ic.confidence_score) as avg_confidence,
    SUM(ev.net_value_usd) as total_net_value
FROM waste_batches wb
LEFT JOIN batch_items bi ON bi.batch_id = wb.id
LEFT JOIN item_classifications ic ON ic.item_id = bi.id
LEFT JOIN economic_valuations ev ON ev.batch_id = wb.id
GROUP BY wb.id;

-- Model performance comparison view
CREATE VIEW v_model_comparison AS
SELECT 
    tr.id, tr.model_name, tr.model_type, tr.architecture,
    tr.final_val_acc, tr.training_duration_s,
    me.accuracy as test_accuracy,
    me.f1_weighted as test_f1,
    me.precision_weighted as test_precision,
    me.recall_weighted as test_recall
FROM training_runs tr
LEFT JOIN ml_evaluations me ON me.training_run_id = tr.id
WHERE tr.status = 'completed';
```

---

## 5. DATA INTEGRITY RULES

| Rule | Implementation |
|------|---------------|
| All foreign keys enforced | SQLAlchemy relationships + `PRAGMA foreign_keys = ON` |
| `is_estimate` required on valuations | Default TRUE; must be consciously set FALSE for verified data |
| `data_source` required on material estimates | Tracks provenance |
| `random_seed` required on training runs | Ensures reproducibility |
| `checksum` on uploaded datasets | SHA256 to detect corruption |
| Soft deletes | `status = 'deleted'` instead of physical deletion |

---

## 6. BACKUP STRATEGY

```
Daily: Copy ewaste_ai.db → backups/ewaste_ai_YYYYMMDD.db
On Training: Checkpoint model files to saved_models/checkpoints/
On Report: Save PDF to reports/archive/ with timestamp
```
