"""
E-Waste AI — CNN Classifier (PyTorch)
=======================================
Builds and fine-tunes CNN models using TorchVision pre-trained backbones.
Supports: MobileNetV3-Small/Large, EfficientNet-B0, ResNet-18/34.

Training happens in Phase 4. This module only defines the model architecture.
"""

import torch
import torch.nn as nn
from torchvision import models
from typing import Optional
import logging

logger = logging.getLogger(__name__)


SUPPORTED_ARCHITECTURES = {
    "mobilenetv3_small": {
        "builder": models.mobilenet_v3_small,
        "weights":  models.MobileNet_V3_Small_Weights.IMAGENET1K_V1,
        "classifier_in_features": 576,
    },
    "mobilenetv3_large": {
        "builder": models.mobilenet_v3_large,
        "weights":  models.MobileNet_V3_Large_Weights.IMAGENET1K_V2,
        "classifier_in_features": 960,
    },
    "efficientnet_b0": {
        "builder": models.efficientnet_b0,
        "weights":  models.EfficientNet_B0_Weights.IMAGENET1K_V1,
        "classifier_in_features": 1280,
    },
    "resnet18": {
        "builder": models.resnet18,
        "weights":  models.ResNet18_Weights.IMAGENET1K_V1,
        "classifier_in_features": 512,
    },
    "resnet34": {
        "builder": models.resnet34,
        "weights":  models.ResNet34_Weights.IMAGENET1K_V1,
        "classifier_in_features": 512,
    },
}


def build_cnn_classifier(
    architecture: str,
    num_classes: int,
    pretrained: bool = True,
    freeze_layers: int = 0,
    dropout: float = 0.2,
) -> nn.Module:
    """
    Build a CNN classifier with the specified architecture.

    Args:
        architecture:  One of SUPPORTED_ARCHITECTURES keys
        num_classes:   Number of output classes
        pretrained:    Use ImageNet pretrained weights (transfer learning)
        freeze_layers: Number of backbone layers to freeze (0 = freeze none)
        dropout:       Dropout rate in classifier head

    Returns:
        torch.nn.Module ready for training
    """
    if architecture not in SUPPORTED_ARCHITECTURES:
        raise ValueError(
            f"Unsupported architecture: '{architecture}'. "
            f"Choose from: {list(SUPPORTED_ARCHITECTURES.keys())}"
        )

    cfg = SUPPORTED_ARCHITECTURES[architecture]
    weights = cfg["weights"] if pretrained else None

    logger.info(f"Building {architecture} | pretrained={pretrained} | classes={num_classes}")

    model = cfg["builder"](weights=weights)

    # ── Replace classifier head ─────────────────────────────────────
    in_features = cfg["classifier_in_features"]

    if "mobilenet" in architecture:
        model.classifier = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.Hardswish(),
            nn.Dropout(p=dropout),
            nn.Linear(256, num_classes),
        )
    elif "efficientnet" in architecture:
        model.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, num_classes),
        )
    elif "resnet" in architecture:
        model.fc = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, num_classes),
        )

    # ── Optionally freeze backbone layers ───────────────────────────
    if freeze_layers > 0 and pretrained:
        frozen = 0
        for name, param in model.named_parameters():
            if frozen >= freeze_layers:
                break
            if "classifier" not in name and "fc" not in name:
                param.requires_grad = False
                frozen += 1
        logger.info(f"Frozen {frozen} backbone parameters")

    total_params = sum(p.numel() for p in model.parameters())
    trainable    = sum(p.numel() for p in model.parameters() if p.requires_grad)
    logger.info(f"Total params: {total_params:,} | Trainable: {trainable:,}")

    return model


def get_imagenet_transforms(image_size: tuple = (224, 224), augment: bool = False):
    """
    Returns torchvision transforms for ImageNet-normalized images.

    Args:
        image_size: Target size (H, W)
        augment:    If True, includes training augmentation

    Returns:
        torchvision.transforms.Compose
    """
    from torchvision import transforms

    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )

    if augment:
        return transforms.Compose([
            transforms.Resize((image_size[0] + 32, image_size[1] + 32)),
            transforms.RandomCrop(image_size),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1),
            transforms.ToTensor(),
            normalize,
        ])
    else:
        return transforms.Compose([
            transforms.Resize(image_size),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            normalize,
        ])
