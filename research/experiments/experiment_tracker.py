"""
research/experiments/experiment_tracker.py
E-WASTE AI - Research Experiment Tracker
Tracks experiments, runs, metrics for reproducible research.
"""

import logging
import datetime
import json
import csv
import io
from pathlib import Path

logger = logging.getLogger(__name__)


class ExperimentTracker:
    """
    Tracks ML experiments, runs, and metrics for research reproducibility.
    If db_session is None, uses in-memory storage.
    """

    def __init__(self, db_session=None, experiment_name: str = "", researcher: str = ""):
        self.db_session = db_session
        self.experiment_name = experiment_name
        self.researcher = researcher
        # In-memory store when no DB session
        self._memory_store = {
            "experiments": {},
            "runs": {},
            "metrics": {},
            "next_experiment_id": 1,
            "next_run_id": 1,
        }

    # ------------------------------------------------------------------
    # Experiment Management
    # ------------------------------------------------------------------

    def create_experiment(
        self,
        name: str,
        description: str = "",
        hypothesis: str = "",
        methodology: str = "",
        dataset_id: int = None,
    ) -> dict:
        """Create a new research experiment."""
        exp_id = self._memory_store["next_experiment_id"]
        experiment = {
            "id": exp_id,
            "name": name,
            "description": description,
            "hypothesis": hypothesis,
            "methodology": methodology,
            "dataset_id": dataset_id,
            "researcher": self.researcher,
            "status": "planned",
            "created_at": datetime.datetime.utcnow().isoformat(),
            "runs": [],
        }
        self._memory_store["experiments"][exp_id] = experiment
        self._memory_store["next_experiment_id"] += 1
        logger.info(f"Created experiment #{exp_id}: {name}")
        return experiment.copy()

    def get_experiment(self, experiment_id: int) -> dict:
        """Retrieve experiment by ID."""
        exp = self._memory_store["experiments"].get(experiment_id)
        if not exp:
            raise ValueError(f"Experiment {experiment_id} not found")
        return exp.copy()

    # ------------------------------------------------------------------
    # Run Management
    # ------------------------------------------------------------------

    def start_run(self, experiment_id: int, config: dict, model_name: str) -> int:
        """Start a new experiment run. Returns run_id."""
        if experiment_id not in self._memory_store["experiments"]:
            raise ValueError(f"Experiment {experiment_id} not found")

        run_id = self._memory_store["next_run_id"]
        run = {
            "id": run_id,
            "experiment_id": experiment_id,
            "model_name": model_name,
            "config": config,
            "status": "running",
            "started_at": datetime.datetime.utcnow().isoformat(),
            "finished_at": None,
            "notes": "",
            "metrics_summary": {},
        }
        self._memory_store["runs"][run_id] = run
        self._memory_store["metrics"][run_id] = []
        self._memory_store["next_run_id"] += 1

        # Register run with experiment
        self._memory_store["experiments"][experiment_id]["runs"].append(run_id)
        # Mark experiment active
        self._memory_store["experiments"][experiment_id]["status"] = "active"

        logger.info(f"Started run #{run_id} for experiment #{experiment_id} — model: {model_name}")
        return run_id

    def finish_run(self, run_id: int, status: str = "completed", notes: str = "") -> None:
        """Mark a run as finished."""
        run = self._memory_store["runs"].get(run_id)
        if not run:
            raise ValueError(f"Run {run_id} not found")
        run["status"] = status
        run["finished_at"] = datetime.datetime.utcnow().isoformat()
        run["notes"] = notes

        # Summarise metrics
        metrics = self._memory_store["metrics"].get(run_id, [])
        summary = {}
        for m in metrics:
            name = m["metric_name"]
            if name not in summary:
                summary[name] = []
            summary[name].append(m["metric_value"])
        run["metrics_summary"] = {
            k: {
                "best": max(v) if v else None,
                "last": v[-1] if v else None,
                "count": len(v),
            }
            for k, v in summary.items()
        }
        logger.info(f"Finished run #{run_id} — status: {status}")

    # ------------------------------------------------------------------
    # Metric Logging
    # ------------------------------------------------------------------

    def log_metric(
        self,
        run_id: int,
        metric_name: str,
        metric_value: float,
        epoch: int = None,
        phase: str = "training",
    ) -> None:
        """Log a single metric value."""
        if run_id not in self._memory_store["metrics"]:
            self._memory_store["metrics"][run_id] = []
        entry = {
            "run_id": run_id,
            "metric_name": metric_name,
            "metric_value": float(metric_value),
            "epoch": epoch,
            "phase": phase,
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }
        self._memory_store["metrics"][run_id].append(entry)

    def log_metrics_batch(
        self,
        run_id: int,
        metrics: dict,
        epoch: int = None,
        phase: str = "training",
    ) -> None:
        """Log multiple metrics at once."""
        for name, value in metrics.items():
            self.log_metric(run_id, name, value, epoch=epoch, phase=phase)

    # ------------------------------------------------------------------
    # Analysis
    # ------------------------------------------------------------------

    def compare_runs(self, experiment_id: int) -> dict:
        """Return a summary comparison table for all runs in an experiment."""
        exp = self._memory_store["experiments"].get(experiment_id)
        if not exp:
            raise ValueError(f"Experiment {experiment_id} not found")

        rows = []
        for run_id in exp.get("runs", []):
            run = self._memory_store["runs"].get(run_id, {})
            metrics = self._memory_store["metrics"].get(run_id, [])

            acc_vals = [m["metric_value"] for m in metrics if m["metric_name"] == "accuracy"]
            f1_vals = [m["metric_value"] for m in metrics if m["metric_name"] == "f1"]

            started = run.get("started_at", "")
            finished = run.get("finished_at", "")
            duration = None
            if started and finished:
                try:
                    d = datetime.datetime.fromisoformat(finished) - datetime.datetime.fromisoformat(started)
                    duration = round(d.total_seconds(), 1)
                except Exception:
                    pass

            rows.append({
                "run_id": run_id,
                "model": run.get("model_name", ""),
                "status": run.get("status", ""),
                "best_accuracy": max(acc_vals) if acc_vals else None,
                "best_f1": max(f1_vals) if f1_vals else None,
                "epochs": len({m["epoch"] for m in metrics if m["epoch"] is not None}),
                "duration_sec": duration,
            })

        return {
            "experiment_id": experiment_id,
            "experiment_name": exp.get("name", ""),
            "runs": rows,
            "total_runs": len(rows),
        }

    def get_best_run(self, experiment_id: int, metric: str = "accuracy") -> dict:
        """Return the run with the best value for the given metric."""
        comparison = self.compare_runs(experiment_id)
        runs = comparison.get("runs", [])
        if not runs:
            return {}
        key = f"best_{metric}"
        valid = [r for r in runs if r.get(key) is not None]
        if not valid:
            return {}
        return max(valid, key=lambda r: r[key])

    # ------------------------------------------------------------------
    # High-level API (Phase 3 compatibility layer)
    # ------------------------------------------------------------------

    def start_experiment(
        self,
        name: str,
        objective: str = "",
        dataset_info: dict | None = None,
        config: dict | None = None,
    ) -> str:
        """
        High-level API: create + activate an experiment in one call.
        Returns a string experiment_id.
        """
        import uuid
        import sys
        exp_id = str(uuid.uuid4())
        now = datetime.datetime.utcnow().isoformat()
        entry = {
            "experiment_id": exp_id,
            "name": name,
            "objective": objective,
            "dataset_info": dataset_info or {},
            "config": config or {},
            "metrics": {},
            "artifacts": [],
            "status": "running",
            "start_time": now,
            "end_time": None,
            "duration_sec": None,
            "library_versions": {
                lib: getattr(__import__(lib, fromlist=[""]), "__version__", "unknown")
                for lib in ["numpy", "pandas", "sklearn"]
                if lib in sys.modules or _try_import(lib)
            },
        }
        self._memory_store.setdefault("_hl_experiments", {})[exp_id] = entry
        return exp_id

    def log_metrics(self, experiment_id: str, metrics: dict) -> None:
        """High-level API: log a dict of metrics to an experiment."""
        exp = self._memory_store.get("_hl_experiments", {}).get(experiment_id)
        if exp is None:
            return
        exp["metrics"].update(metrics)

    def log_artifact(self, experiment_id: str, file_path: str, artifact_type: str = "file") -> None:
        """High-level API: record an artifact path."""
        exp = self._memory_store.get("_hl_experiments", {}).get(experiment_id)
        if exp is None:
            return
        exp["artifacts"].append({"path": file_path, "type": artifact_type})

    def end_experiment(self, experiment_id: str, status: str = "completed") -> None:
        """High-level API: mark experiment as finished."""
        exp = self._memory_store.get("_hl_experiments", {}).get(experiment_id)
        if exp is None:
            return
        exp["status"] = status
        now = datetime.datetime.utcnow().isoformat()
        exp["end_time"] = now
        try:
            start = datetime.datetime.fromisoformat(exp["start_time"])
            end = datetime.datetime.fromisoformat(now)
            exp["duration_sec"] = round((end - start).total_seconds(), 2)
        except Exception:
            pass

    def get_experiment(self, experiment_id: str) -> dict | None:
        """High-level API: retrieve experiment by string ID."""
        return self._memory_store.get("_hl_experiments", {}).get(experiment_id)

    def list_experiments(self) -> list:
        """High-level API: list all high-level experiments."""
        return list(self._memory_store.get("_hl_experiments", {}).values())

    def generate_comparison_table(self, experiment_ids: list) -> object:
        """High-level API: build a pandas DataFrame comparing experiments."""
        try:
            import pandas as pd
        except ImportError:
            return None
        rows = []
        store = self._memory_store.get("_hl_experiments", {})
        for eid in experiment_ids:
            exp = store.get(eid)
            if exp is None:
                continue
            row = {
                "experiment_id": eid[:8],
                "name": exp.get("name"),
                "status": exp.get("status"),
                "duration_sec": exp.get("duration_sec"),
            }
            row.update(exp.get("metrics", {}))
            rows.append(row)
        return pd.DataFrame(rows) if rows else pd.DataFrame()

    def export_to_csv(self, experiment_id: int, output_path: str) -> str:
        """Export all run metrics to a CSV file."""
        exp = self._memory_store["experiments"].get(experiment_id)
        if not exp:
            raise ValueError(f"Experiment {experiment_id} not found")

        rows = []
        for run_id in exp.get("runs", []):
            run = self._memory_store["runs"].get(run_id, {})
            for m in self._memory_store["metrics"].get(run_id, []):
                rows.append({
                    "experiment_id": experiment_id,
                    "run_id": run_id,
                    "model_name": run.get("model_name", ""),
                    "epoch": m.get("epoch"),
                    "phase": m.get("phase"),
                    "metric_name": m.get("metric_name"),
                    "metric_value": m.get("metric_value"),
                    "timestamp": m.get("timestamp"),
                })

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", newline="") as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        logger.info(f"Exported {len(rows)} metric rows to {output_path}")
        return str(output)


def _try_import(lib: str) -> bool:
    """Return True if lib can be imported."""
    try:
        __import__(lib)
        return True
    except ImportError:
        return False
