"""
EwasteImageDataset: PyTorch Dataset for e-waste image classification.
Supports loading from lists of paths or auto-discovery from a directory tree.
"""

import logging
import pathlib
from typing import List, Optional

import numpy as np
import torch
import torchvision.transforms as T
from PIL import Image
from torch.utils.data import Dataset

logger = logging.getLogger(__name__)


class EwasteImageDataset(Dataset):
    """
    A PyTorch Dataset for e-waste images.

    Parameters
    ----------
    image_paths : list[str | Path]
        Absolute or relative paths to image files.
    labels : list[int], optional
        Integer class labels aligned with *image_paths*.
        If None the dataset operates in inference mode (no labels returned).
    transform : callable, optional
        torchvision transform applied to each PIL image before returning.
    class_names : list[str], optional
        Human-readable class names; index i → class_names[i].
    """

    def __init__(
        self,
        image_paths: List,
        labels: Optional[List[int]] = None,
        transform=None,
        class_names: Optional[List[str]] = None,
    ):
        self.image_paths: List[pathlib.Path] = [
            pathlib.Path(p) for p in image_paths
        ]
        self.labels: Optional[List[int]] = labels
        self.transform = transform
        self._class_names: List[str] = class_names or []

        if labels is not None and len(image_paths) != len(labels):
            raise ValueError(
                f"image_paths ({len(image_paths)}) and labels ({len(labels)}) "
                "must have the same length."
            )

        logger.debug(
            "EwasteImageDataset: %d images, %d classes, labels=%s",
            len(self.image_paths),
            len(self._class_names),
            labels is not None,
        )

    # ------------------------------------------------------------------
    # Dataset protocol
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int):
        """
        Returns
        -------
        (image_tensor, label_int)  when labels are available, else
        image_tensor               in inference mode.
        """
        img_path = self.image_paths[idx]

        try:
            image = Image.open(img_path).convert("RGB")
        except Exception as exc:
            logger.warning("Failed to open image %s: %s", img_path, exc)
            # Return a black placeholder so a DataLoader batch doesn't crash
            image = Image.new("RGB", (224, 224), color=0)

        if self.transform is not None:
            image = self.transform(image)
        else:
            image = T.ToTensor()(image)

        if self.labels is not None:
            return image, int(self.labels[idx])
        return image

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def get_class_names(self) -> List[str]:
        """Return the list of human-readable class names."""
        return list(self._class_names)

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @staticmethod
    def from_directory(
        root_dir,
        transform=None,
        extensions: tuple = (".jpg", ".jpeg", ".png", ".bmp"),
    ) -> "EwasteImageDataset":
        """
        Build an EwasteImageDataset by walking *root_dir*.

        Each immediate subdirectory is treated as one class.
        Files with matching *extensions* inside those subdirectories are
        collected; files in root_dir itself are skipped.

        Parameters
        ----------
        root_dir : str | Path
            Root directory containing one subdirectory per class.
        transform : callable, optional
            torchvision transform applied to each image.
        extensions : tuple[str]
            Lowercase file extensions to include.

        Returns
        -------
        EwasteImageDataset
        """
        root = pathlib.Path(root_dir)
        if not root.is_dir():
            raise NotADirectoryError(f"root_dir is not a directory: {root}")

        # Collect class names from immediate subdirectories (sorted for stability)
        class_dirs = sorted(
            d for d in root.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        )
        if not class_dirs:
            raise ValueError(f"No class subdirectories found under: {root}")

        class_names = [d.name for d in class_dirs]
        class_to_idx = {name: idx for idx, name in enumerate(class_names)}

        image_paths: List[pathlib.Path] = []
        labels: List[int] = []
        ext_lower = {e.lower() for e in extensions}

        for class_dir in class_dirs:
            class_idx = class_to_idx[class_dir.name]
            for file_path in sorted(class_dir.rglob("*")):
                if file_path.is_file() and file_path.suffix.lower() in ext_lower:
                    image_paths.append(file_path)
                    labels.append(class_idx)

        logger.info(
            "from_directory: found %d images across %d classes in '%s'",
            len(image_paths),
            len(class_names),
            root,
        )

        return EwasteImageDataset(
            image_paths=image_paths,
            labels=labels,
            transform=transform,
            class_names=class_names,
        )
