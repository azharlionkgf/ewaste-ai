"""
E-Waste AI — ML Model Registry (Stub)
=======================================
Central registry for all supported model architectures.
Full training implementation in Phase 4.
"""

# Supported CNN architectures (via torchvision)
CNN_MODELS = {
    "mobilenetv3_small": {
        "description": "MobileNetV3-Small — fast, lightweight, CPU-friendly",
        "params_millions": 1.5,
        "input_size": (224, 224),
        "pretrained": True,
        "recommended": True,
    },
    "mobilenetv3_large": {
        "description": "MobileNetV3-Large — better accuracy than small",
        "params_millions": 3.0,
        "input_size": (224, 224),
        "pretrained": True,
    },
    "efficientnet_b0": {
        "description": "EfficientNet-B0 — excellent accuracy/size tradeoff",
        "params_millions": 5.3,
        "input_size": (224, 224),
        "pretrained": True,
    },
    "resnet18": {
        "description": "ResNet-18 — classic benchmark baseline",
        "params_millions": 11.7,
        "input_size": (224, 224),
        "pretrained": True,
    },
    "resnet34": {
        "description": "ResNet-34 — deeper ResNet baseline",
        "params_millions": 21.8,
        "input_size": (224, 224),
        "pretrained": True,
    },
}

# Supported traditional ML algorithms
TABULAR_MODELS = {
    "random_forest": {
        "description": "Random Forest — ensemble, good baseline, interpretable",
        "library": "sklearn",
        "recommended": True,
    },
    "xgboost": {
        "description": "XGBoost — high-performance gradient boosting",
        "library": "xgboost",
        "recommended": True,
    },
    "catboost": {
        "description": "CatBoost — excellent with categorical features",
        "library": "catboost",
    },
    "svm": {
        "description": "Support Vector Machine — effective for small datasets",
        "library": "sklearn",
    },
    "logistic_regression": {
        "description": "Logistic Regression — interpretable, fast baseline",
        "library": "sklearn",
    },
}


def get_cnn_architectures() -> dict:
    return CNN_MODELS


def get_tabular_algorithms() -> dict:
    return TABULAR_MODELS


def get_all_models() -> dict:
    return {"cnn": CNN_MODELS, "tabular": TABULAR_MODELS}
