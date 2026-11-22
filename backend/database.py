"""
E-Waste AI — Database Setup
============================
SQLAlchemy engine, session factory, and base model.
Full ORM models will be implemented in Phase 1.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/ewaste_ai.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency: yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables. Called at startup."""
    # Import all models so SQLAlchemy knows about them
    # from backend.models import dataset, ml_model, analysis, report  # Phase 1
    Base.metadata.create_all(bind=engine)
