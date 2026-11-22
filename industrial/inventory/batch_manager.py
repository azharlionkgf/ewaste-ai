"""
industrial/inventory/batch_manager.py
E-WASTE AI - Industrial Batch Manager
Handles incoming e-waste batch registration and tracking.
"""

import logging
import datetime
import json
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

VALID_STATUSES = [
    "registered",
    "assessed",
    "classified",
    "sorted",
    "dismantled",
    "recovered",
    "completed",
]


class BatchManager:
    """
    Manages incoming e-waste batches in an industrial processing workflow.
    If db_session is None, uses in-memory storage.
    """

    def __init__(self, db_session=None):
        self.db_session = db_session
        self._batches = {}
        self._items = {}
        self._next_batch_id = 1
        self._next_item_id = 1

    # ------------------------------------------------------------------
    # Batch Operations
    # ------------------------------------------------------------------

    def register_batch(
        self,
        source: str,
        weight_kg: float,
        item_count: int,
        notes: str = "",
        collection_point: str = "",
    ) -> dict:
        """Register a new incoming e-waste batch."""
        batch_id = self._next_batch_id
        batch_ref = f"BATCH-{datetime.datetime.utcnow().strftime('%Y%m%d')}-{batch_id:04d}"

        batch = {
            "id": batch_id,
            "batch_ref": batch_ref,
            "source": source,
            "weight_kg": float(weight_kg),
            "item_count": item_count,
            "notes": notes,
            "collection_point": collection_point,
            "status": "registered",
            "registered_at": datetime.datetime.utcnow().isoformat(),
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "items": [],
            "closed_at": None,
            "close_notes": "",
        }

        self._batches[batch_id] = batch
        self._next_batch_id += 1
        logger.info(f"Registered batch #{batch_id} ({batch_ref}) from '{source}', {weight_kg}kg, {item_count} items")
        return batch.copy()

    def add_item_to_batch(
        self,
        batch_id: int,
        device_type: str,
        brand: str = "",
        model: str = "",
        condition: str = "",
        weight_kg: float = 0.0,
        serial_number: str = "",
    ) -> dict:
        """Add an individual item to a batch."""
        if batch_id not in self._batches:
            raise ValueError(f"Batch {batch_id} not found")

        item_id = self._next_item_id
        item = {
            "id": item_id,
            "batch_id": batch_id,
            "device_type": device_type,
            "brand": brand,
            "model": model,
            "condition": condition,
            "weight_kg": float(weight_kg),
            "serial_number": serial_number or str(uuid.uuid4())[:8].upper(),
            "classification_status": "pending",
            "classified_as": None,
            "confidence": None,
            "added_at": datetime.datetime.utcnow().isoformat(),
        }

        self._items[item_id] = item
        self._batches[batch_id]["items"].append(item_id)
        self._batches[batch_id]["last_updated"] = datetime.datetime.utcnow().isoformat()
        self._next_item_id += 1

        logger.info(f"Added item #{item_id} ({device_type}) to batch #{batch_id}")
        return item.copy()

    def update_batch_status(self, batch_id: int, new_status: str) -> bool:
        """Update batch status through the workflow pipeline."""
        if batch_id not in self._batches:
            raise ValueError(f"Batch {batch_id} not found")
        if new_status not in VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Valid: {VALID_STATUSES}")

        old_status = self._batches[batch_id]["status"]
        self._batches[batch_id]["status"] = new_status
        self._batches[batch_id]["last_updated"] = datetime.datetime.utcnow().isoformat()
        logger.info(f"Batch #{batch_id} status: {old_status} → {new_status}")
        return True

    def get_batch_summary(self, batch_id: int) -> dict:
        """Get full summary of a batch including item details."""
        batch = self._batches.get(batch_id)
        if not batch:
            raise ValueError(f"Batch {batch_id} not found")

        items = [self._items[iid].copy() for iid in batch["items"] if iid in self._items]
        classified = sum(1 for i in items if i["classification_status"] == "completed")
        total_weight = sum(i["weight_kg"] for i in items if i["weight_kg"])

        return {
            **batch.copy(),
            "item_details": items,
            "total_items_registered": len(items),
            "items_classified": classified,
            "items_pending": len(items) - classified,
            "total_items_weight_kg": round(total_weight, 3),
        }

    def list_batches(self, status: str = None, limit: int = 50) -> list:
        """List batches, optionally filtered by status."""
        batches = list(self._batches.values())
        if status:
            batches = [b for b in batches if b["status"] == status]
        batches.sort(key=lambda b: b["registered_at"], reverse=True)
        return [b.copy() for b in batches[:limit]]

    def close_batch(self, batch_id: int, notes: str = "") -> dict:
        """Close a completed batch."""
        if batch_id not in self._batches:
            raise ValueError(f"Batch {batch_id} not found")
        self._batches[batch_id]["status"] = "completed"
        self._batches[batch_id]["closed_at"] = datetime.datetime.utcnow().isoformat()
        self._batches[batch_id]["close_notes"] = notes
        self._batches[batch_id]["last_updated"] = datetime.datetime.utcnow().isoformat()
        logger.info(f"Closed batch #{batch_id}")
        return self.get_batch_summary(batch_id)

    def update_item_classification(
        self,
        item_id: int,
        classified_as: str,
        confidence: float,
    ) -> bool:
        """Mark an item's classification result."""
        if item_id not in self._items:
            raise ValueError(f"Item {item_id} not found")
        self._items[item_id]["classified_as"] = classified_as
        self._items[item_id]["confidence"] = confidence
        self._items[item_id]["classification_status"] = "completed"
        return True
