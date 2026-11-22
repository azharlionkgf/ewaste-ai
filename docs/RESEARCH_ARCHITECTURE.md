# 🔬 E-WASTE AI — RESEARCH ARCHITECTURE
## Experiment Design, Reproducibility, and Academic Documentation

**Version:** 2.0.0 | **Date:** 2026-11-22  
**Purpose:** Academic research workflow, experiment tracking, paper preparation

---

## 1. RESEARCH PHILOSOPHY

This platform is designed so that every experiment is:

| Principle | Implementation |
|-----------|---------------|
| **Reproducible** | Fixed random seeds, versioned datasets, logged hyperparameters |
| **Traceable** | Every result links to: dataset version → preprocessing config → model config → evaluation |
| **Honest** | All estimates clearly labeled; no fabricated results |
| **Comparable** | Baseline comparisons against published benchmarks |
| **Documented** | Auto-generated experiment reports for academic submission |

---

## 2. RESEARCH WORKFLOW

```
1. RESEARCH QUESTION FORMULATION
   └─► Register experiment with hypothesis in research_experiments table

2. DATASET SELECTION & DOCUMENTATION
   └─► Record: dataset name, version, source, license, size, class distribution

3. BASELINE ESTABLISHMENT
   └─► Train simplest model first (Logistic Regression / basic CNN)
   └─► Record as "Baseline Run" in experiment_runs

4. EXPERIMENTAL ITERATIONS
   └─► Vary ONE factor at a time (learning rate OR architecture OR augmentation)
   └─► Record each as separate experiment_run with identical seed

5. EVALUATION
   └─► Evaluate all runs on the SAME held-out test set
   └─► Never tune on test set

6. ANALYSIS
   └─► Statistical significance testing (where applicable)
   └─► Ablation studies

7. REPORTING
   └─► Auto-generate LaTeX-ready tables
   └─► Auto-generate comparison charts
   └─► Export full experiment log
```

---

## 3. EXPERIMENT STRUCTURE

### 3.1 Experiment Hierarchy

```
Research Experiment
    │
    ├── Experiment Run 1 (Baseline: LogReg, seed=42)
    │       ├── Hyperparameters logged
    │       ├── Training metrics per epoch
    │       └── Evaluation metrics (acc, f1, cm, roc)
    │
    ├── Experiment Run 2 (Variant: RF, seed=42)
    │       ├── Same dataset, same seed
    │       └── Evaluation metrics
    │
    ├── Experiment Run 3 (Variant: XGBoost, seed=42)
    │
    └── Experiment Run 4 (Variant: MobileNetV3, seed=42)
              └── Evaluation metrics → BEST MODEL
```

### 3.2 What Gets Logged Per Run

```python
ExperimentRun = {
    # Identity
    "run_id":           "UUID",
    "experiment_name":  "E-Waste Classification Study 1",
    "run_name":         "MobileNetV3-Baseline-Seed42",
    "timestamp":        "2026-11-22T23:48:00",

    # Data provenance
    "dataset_name":     "ewaste_images_v2",
    "dataset_version":  "2.0",
    "dataset_hash":     "sha256:abc123...",
    "train_size":       8400,
    "val_size":         1800,
    "test_size":        1800,
    "class_distribution": {"smartphone": 2100, "laptop": 2100, ...},

    # Preprocessing
    "preprocessing_config": {
        "image_size": [224, 224],
        "normalization": "imagenet_stats",
        "augmentation": ["hflip", "rotation_15", "color_jitter_0.2"]
    },

    # Model config
    "model_type":       "cnn",
    "architecture":     "mobilenetv3_small",
    "pretrained":       True,
    "num_classes":      15,
    "hyperparameters": {
        "optimizer":    "adam",
        "lr":           0.001,
        "batch_size":   16,
        "epochs":       30,
        "weight_decay": 1e-4,
        "scheduler":    "cosine_annealing"
    },
    "random_seed":      42,

    # Results
    "best_val_acc":     0.8921,
    "test_accuracy":    0.8847,
    "test_f1_macro":    0.8812,
    "test_f1_weighted": 0.8863,
    "training_time_s":  1842,

    # Environment
    "python_version":   "3.13.7",
    "torch_version":    "2.12.0",
    "cpu":              "Intel i5-1340P",
    "gpu":              "None"
}
```

---

## 4. DATASET PROVENANCE TRACKING

Every dataset used in research must have:

```yaml
# dataset_metadata.yaml (auto-generated per dataset)
name: "ewaste_images_v2"
version: "2.0"
created_date: "2026-11-22"
source: "Kaggle / UCI / Custom collected"
license: "CC BY 4.0"
collection_method: "web scraping + manual labeling"
annotation_tool: "LabelImg"
annotators: 2
inter_annotator_agreement: 0.91  # Cohen's Kappa
sha256: "abc123..."

class_distribution:
  smartphone: 2100
  laptop: 2100
  tablet: 800
  pcb: 1200
  battery: 900
  monitor: 600
  printer: 450
  cables: 750
  charger: 600
  tv: 450
  desktop: 750
  other: 300

split:
  train: 0.70
  validation: 0.15
  test: 0.15

known_biases:
  - "iPhone over-represented in smartphone class"
  - "Limited industrial PCB samples"

preprocessing_notes:
  - "Images resized to 224x224"
  - "JPEG artifacts present in ~5% of images"
```

---

## 5. EVALUATION FRAMEWORK

### 5.1 Standard Metrics (All Models)

| Metric | Formula | Use Case |
|--------|---------|---------|
| Accuracy | TP+TN / Total | Overall performance |
| Precision (Macro) | Mean precision per class | Per-class performance |
| Precision (Weighted) | Weighted by class size | Imbalanced datasets |
| Recall (Macro) | Mean recall per class | Miss rate per class |
| F1 (Macro) | Harmonic mean of P and R per class | Balanced assessment |
| F1 (Weighted) | F1 weighted by class size | Primary metric |
| Cohen's Kappa | Agreement beyond chance | Multi-class quality |
| ROC-AUC (OvR) | One-vs-Rest AUC | Probabilistic ranking |
| Confusion Matrix | Full NxN matrix | Error analysis |

### 5.2 Additional Research Metrics

| Metric | Purpose |
|--------|---------|
| Inference Time (ms/sample) | Practical deployment viability |
| Model Size (MB) | Edge deployment feasibility |
| Training Time (s) | Computational cost reporting |
| Convergence Epoch | Learning efficiency |
| Per-class F1 | Identify underperforming categories |

### 5.3 Test Set Discipline

> [!IMPORTANT]  
> The test set is used ONLY ONCE per experiment — after all hyperparameter tuning  
> is complete using the validation set. This is non-negotiable for academic integrity.

---

## 6. BASELINE COMPARISONS

For academic credibility, we establish baselines against:

| Baseline | Description | Source |
|---------|-------------|--------|
| **Random Classifier** | Uniform random predictions | — |
| **Majority Class** | Always predict most common class | — |
| **Logistic Regression** | Standard ML baseline | sklearn |
| **Random Forest (100 trees)** | Standard ensemble baseline | sklearn |
| **ResNet-18** | Published image classification benchmark | torchvision |
| **MobileNetV2** | Prior lightweight model | torchvision |

All baselines trained on the same dataset with the same train/val/test split.

---

## 7. STATISTICAL RIGOR

### 7.1 Seeds and Determinism
```python
# Every experiment must set these at startup
import random, numpy, torch
random.seed(42)
numpy.random.seed(42)
torch.manual_seed(42)
# For DataLoader:
torch.Generator().manual_seed(42)
```

### 7.2 Multiple Runs (Where Feasible)
For final models, run with 3 different seeds (42, 123, 456) and report:
- Mean ± Standard Deviation for each metric

### 7.3 Cross-Validation
For tabular/smaller datasets, use 5-fold stratified cross-validation.

---

## 8. RESEARCH REPORT STRUCTURE

Auto-generated research report sections:

```
1. Abstract
2. Introduction & Motivation
3. Dataset Description
   3.1 Data Collection
   3.2 Class Distribution (chart)
   3.3 Preprocessing Steps
4. Methodology
   4.1 System Architecture
   4.2 Model Architectures
   4.3 Training Configuration
5. Experimental Results
   5.1 Training Curves (chart)
   5.2 Comparative Table (all models)
   5.3 Best Model Metrics
   5.4 Confusion Matrix (chart)
   5.5 Per-Class Performance (chart)
6. Discussion
   6.1 Analysis of Results
   6.2 Error Analysis
   6.3 Limitations
7. Conclusion
8. References
Appendix A: Full Hyperparameter Logs
Appendix B: Dataset Provenance
```

---

## 9. E-WASTE DOMAIN KNOWLEDGE BASE

Scientific references for material composition data:

| Source | Data Provided |
|--------|--------------|
| Baldé et al. (2017) Global E-waste Monitor | Weight fractions per device type |
| Graedel et al. - Criticality of Metals | Critical material recovery data |
| European Environment Agency | Hazardous substance profiles |
| UNEP (2013) Metal Recycling Report | Recovery efficiency benchmarks |
| Cucchiella et al. (2015) | Economic value estimation methodology |

All material estimates in the platform reference at least one of these sources and are clearly labeled as **estimates** in the UI.

---

## 10. REPRODUCIBILITY CHECKLIST

Before publishing or presenting results, verify:

- [ ] Random seed logged for all runs
- [ ] Dataset version and hash recorded
- [ ] Preprocessing config saved
- [ ] Hyperparameters fully logged
- [ ] Test set used only once
- [ ] All estimates labeled as estimates
- [ ] Data sources cited for material composition
- [ ] Model weights saved with training metadata
- [ ] Environment (Python/library versions) recorded
- [ ] Multiple seed runs completed (for final results)
