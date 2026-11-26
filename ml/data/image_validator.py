"""
Image Dataset Validator — Phase 2: Dataset Intelligence Engine
Validates image datasets: corrupt images, duplicates, structure, class balance.
"""

from __future__ import annotations

import hashlib
import logging
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

try:
    from PIL import Image, UnidentifiedImageError
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.warning("Pillow not installed — image validation limited")


class ImageDatasetValidator:
    """
    Validates an image dataset stored in a class-per-folder structure.

    Expected layout::

        root_dir/
            class_a/
                img1.jpg
                img2.png
            class_b/
                img3.jpg

    Usage::

        validator = ImageDatasetValidator()
        report = validator.validate(root_dir)
    """

    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}

    def validate(self, root_dir: str | Path) -> dict:
        """
        Validate the image dataset at ``root_dir``.

        Returns a detailed report dict.
        """
        root = Path(root_dir)
        if not root.exists():
            return {"error": f"Directory not found: {root}", "valid": False}

        report: dict[str, Any] = {
            "root_dir": str(root),
            "valid": True,
            "classes": [],
            "class_counts": {},
            "total_images": 0,
            "corrupt_images": [],
            "duplicate_images": [],
            "unsupported_formats": [],
            "empty_classes": [],
            "class_balance": {},
            "issues": [],
        }

        class_dirs = [d for d in root.iterdir() if d.is_dir()]
        if not class_dirs:
            report["issues"].append("No class subdirectories found — expected class-per-folder layout")
            report["valid"] = False
            return report

        hash_map: dict[str, list[str]] = defaultdict(list)

        for class_dir in sorted(class_dirs):
            class_name = class_dir.name
            report["classes"].append(class_name)

            image_files = [
                f for f in class_dir.rglob("*")
                if f.is_file() and f.suffix.lower() in self.SUPPORTED_EXTENSIONS
            ]
            unsupported = [
                f for f in class_dir.rglob("*")
                if f.is_file() and f.suffix.lower() not in self.SUPPORTED_EXTENSIONS
                and not f.name.startswith(".")
            ]

            if not image_files:
                report["empty_classes"].append(class_name)
                report["issues"].append(f"Class '{class_name}' has no valid images")

            valid_count = 0
            for img_path in image_files:
                report["unsupported_formats"].extend(str(f) for f in unsupported)

                # Corrupt check
                if PIL_AVAILABLE:
                    try:
                        with Image.open(img_path) as im:
                            im.verify()
                        valid_count += 1
                    except (UnidentifiedImageError, Exception) as exc:
                        report["corrupt_images"].append(
                            {"path": str(img_path), "error": str(exc)}
                        )
                        continue
                else:
                    valid_count += 1

                # Duplicate detection via MD5
                try:
                    file_hash = self._md5(img_path)
                    hash_map[file_hash].append(str(img_path))
                except Exception:
                    pass

            report["class_counts"][class_name] = valid_count
            report["total_images"] += valid_count

        # Duplicates
        for file_hash, paths in hash_map.items():
            if len(paths) > 1:
                report["duplicate_images"].append({"hash": file_hash, "files": paths})

        # Class balance
        counts = list(report["class_counts"].values())
        if counts:
            total = max(sum(counts), 1)   # guard against all-corrupt datasets
            report["class_balance"] = {
                cls: {"count": cnt, "pct": round(cnt / total * 100, 1)}
                for cls, cnt in report["class_counts"].items()
            }
            if max(counts) / max(min(counts), 1) > 5:
                report["issues"].append(
                    "Severe class imbalance detected (max/min ratio > 5)"
                )

        # Corrupt summary
        if report["corrupt_images"]:
            report["issues"].append(
                f"{len(report['corrupt_images'])} corrupt images found"
            )
            report["valid"] = False

        if report["duplicate_images"]:
            report["issues"].append(
                f"{len(report['duplicate_images'])} duplicate image groups found"
            )

        return report

    def fix_structure(
        self, root_dir: str | Path, output_dir: str | Path
    ) -> dict:
        """
        Copy only valid (non-corrupt) images to ``output_dir`` preserving class structure.

        Returns a summary report.
        """
        root = Path(root_dir)
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        validation = self.validate(root)
        copied = 0
        skipped = 0
        corrupt_paths = {c["path"] for c in validation.get("corrupt_images", [])}

        for class_dir in root.iterdir():
            if not class_dir.is_dir():
                continue
            out_class = out / class_dir.name
            out_class.mkdir(exist_ok=True)
            for img_path in class_dir.rglob("*"):
                if img_path.is_file() and img_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                    if str(img_path) in corrupt_paths:
                        skipped += 1
                        continue
                    shutil.copy2(img_path, out_class / img_path.name)
                    copied += 1

        return {
            "output_dir": str(out),
            "images_copied": copied,
            "images_skipped": skipped,
            "original_validation": validation,
        }

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _md5(path: Path, chunk_size: int = 65536) -> str:
        h = hashlib.md5()
        with open(path, "rb") as f:
            while chunk := f.read(chunk_size):
                h.update(chunk)
        return h.hexdigest()
