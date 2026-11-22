"""
E-Waste AI — Application Configuration Loader
Reads from config.yaml and environment variables.
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

_config_path = Path(__file__).parent.parent / "config.yaml"

def load_config() -> dict:
    """Load YAML config file."""
    if _config_path.exists():
        with open(_config_path, "r") as f:
            return yaml.safe_load(f)
    return {}

_cfg = load_config()


class Settings:
    """Central application settings."""

    # App
    APP_NAME: str = _cfg.get("app", {}).get("name", "E-Waste AI")
    APP_VERSION: str = _cfg.get("app", {}).get("version", "2.0.0")
    DEBUG: bool = os.getenv("APP_DEBUG", "false").lower() == "true"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        _cfg.get("database", {}).get("url", "sqlite:///./database/ewaste_ai.db")
    )

    # Storage
    UPLOADS_DIR: Path = Path(_cfg.get("storage", {}).get("uploads_dir", "data/uploads"))
    PROCESSED_DIR: Path = Path(_cfg.get("storage", {}).get("processed_dir", "data/processed"))
    IMAGES_DIR: Path = Path(_cfg.get("storage", {}).get("images_dir", "data/images"))
    VIDEOS_DIR: Path = Path(_cfg.get("storage", {}).get("videos_dir", "data/videos"))
    EXPORTS_DIR: Path = Path(_cfg.get("storage", {}).get("exports_dir", "data/exports"))
    MODELS_DIR: Path = Path(_cfg.get("storage", {}).get("models_dir", "saved_models"))
    REPORTS_DIR: Path = Path(_cfg.get("storage", {}).get("reports_dir", "reports"))
    LOGS_DIR: Path = Path(_cfg.get("storage", {}).get("logs_dir", "logs"))

    # ML
    DEFAULT_SEED: int = _cfg.get("ml", {}).get("default_seed", 42)
    BATCH_SIZE: int = _cfg.get("ml", {}).get("batch_size", 16)
    NUM_WORKERS: int = _cfg.get("ml", {}).get("num_workers", 0)
    IMAGE_SIZE: tuple = tuple(_cfg.get("ml", {}).get("image_size", [224, 224]))
    MAX_EPOCHS: int = _cfg.get("ml", {}).get("max_epochs", 50)
    TRAIN_SPLIT: float = _cfg.get("ml", {}).get("train_split", 0.70)
    VAL_SPLIT: float = _cfg.get("ml", {}).get("val_split", 0.15)
    TEST_SPLIT: float = _cfg.get("ml", {}).get("test_split", 0.15)

    # Uploads
    MAX_FILE_SIZE_MB: int = _cfg.get("uploads", {}).get("max_file_size_mb", 500)
    ALLOWED_TABULAR_TYPES: list = _cfg.get("uploads", {}).get(
        "allowed_tabular_types", [".csv", ".xlsx", ".xls", ".json"]
    )
    ALLOWED_IMAGE_TYPES: list = _cfg.get("uploads", {}).get(
        "allowed_image_types", [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
    )
    ALLOWED_VIDEO_TYPES: list = _cfg.get("uploads", {}).get(
        "allowed_video_types", [".mp4", ".avi", ".mov", ".mkv"]
    )

    # Economic (approximate market prices — clearly labeled as estimates)
    GOLD_PRICE_USD_OZ: float = _cfg.get("economic", {}).get("gold_price_usd_per_troy_oz", 2650.0)
    SILVER_PRICE_USD_OZ: float = _cfg.get("economic", {}).get("silver_price_usd_per_troy_oz", 30.0)
    COPPER_PRICE_USD_KG: float = _cfg.get("economic", {}).get("copper_price_usd_per_kg", 9.50)
    LITHIUM_PRICE_USD_KG: float = _cfg.get("economic", {}).get("lithium_price_usd_per_kg", 12.0)

    def ensure_directories(self):
        """Create all required directories if they don't exist."""
        dirs = [
            self.UPLOADS_DIR, self.PROCESSED_DIR, self.IMAGES_DIR,
            self.VIDEOS_DIR, self.EXPORTS_DIR, self.MODELS_DIR,
            self.REPORTS_DIR, self.LOGS_DIR,
            self.MODELS_DIR / "checkpoints",
            self.MODELS_DIR / "sklearn",
            self.MODELS_DIR / "metadata",
            Path("database"),
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)


settings = Settings()
