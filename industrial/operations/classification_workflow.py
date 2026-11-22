"""
industrial/operations/classification_workflow.py
E-WASTE AI - Classification Workflow Orchestrator
Orchestrates AI classification of e-waste batch items.
"""

import logging
import datetime
import json

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Material composition estimates per device type
# Source: Research averages — always labeled is_estimate=True
# ------------------------------------------------------------------

DEVICE_MATERIAL_ESTIMATES = {
    "smartphone": {
        "gold_pct": 0.034, "silver_pct": 0.35, "copper_pct": 15.0,
        "aluminum_pct": 10.0, "lithium_pct": 1.5, "rare_earth_pct": 0.5,
        "plastic_pct": 40.0, "glass_pct": 30.0,
        "is_estimate": True, "source": "UNEP 2019 / research averages",
    },
    "laptop": {
        "gold_pct": 0.015, "silver_pct": 0.1, "copper_pct": 12.0,
        "aluminum_pct": 25.0, "lithium_pct": 2.0, "rare_earth_pct": 0.3,
        "plastic_pct": 35.0, "iron_steel_pct": 20.0,
        "is_estimate": True, "source": "UNEP 2019 / research averages",
    },
    "desktop_computer": {
        "gold_pct": 0.010, "silver_pct": 0.08, "copper_pct": 14.0,
        "aluminum_pct": 15.0, "iron_steel_pct": 40.0,
        "plastic_pct": 25.0,
        "is_estimate": True, "source": "UNEP 2019 / research averages",
    },
    "tablet": {
        "gold_pct": 0.025, "silver_pct": 0.2, "copper_pct": 12.0,
        "aluminum_pct": 20.0, "lithium_pct": 1.8, "rare_earth_pct": 0.4,
        "plastic_pct": 35.0, "glass_pct": 25.0,
        "is_estimate": True, "source": "Research averages",
    },
    "circuit_board": {
        "gold_pct": 0.1, "silver_pct": 0.5, "copper_pct": 25.0,
        "palladium_pct": 0.015, "platinum_pct": 0.005,
        "iron_steel_pct": 10.0, "plastic_pct": 30.0, "fiberglass_pct": 30.0,
        "is_estimate": True, "source": "Hagelüken 2006 / research averages",
    },
    "battery_li_ion": {
        "lithium_pct": 1.5, "cobalt_pct": 15.0, "nickel_pct": 10.0,
        "manganese_pct": 8.0, "copper_pct": 5.0, "aluminum_pct": 5.0,
        "plastic_pct": 20.0, "steel_pct": 25.0,
        "is_estimate": True, "source": "Research averages",
    },
    "monitor_lcd": {
        "copper_pct": 5.0, "aluminum_pct": 15.0, "iron_steel_pct": 20.0,
        "plastic_pct": 40.0, "glass_pct": 15.0, "mercury_mg_per_unit": 3.5,
        "is_estimate": True, "source": "Research averages",
    },
    "printer": {
        "copper_pct": 6.0, "aluminum_pct": 10.0, "iron_steel_pct": 25.0,
        "plastic_pct": 55.0,
        "is_estimate": True, "source": "Research averages",
    },
    "charger": {
        "copper_pct": 20.0, "iron_steel_pct": 10.0,
        "plastic_pct": 65.0, "aluminum_pct": 5.0,
        "is_estimate": True, "source": "Research averages",
    },
    "cable": {
        "copper_pct": 55.0, "plastic_pct": 40.0, "aluminum_pct": 5.0,
        "is_estimate": True, "source": "Research averages",
    },
    "default": {
        "copper_pct": 10.0, "aluminum_pct": 10.0, "iron_steel_pct": 20.0,
        "plastic_pct": 55.0,
        "is_estimate": True, "source": "Generic research averages",
    },
}


class ClassificationWorkflow:
    """
    Orchestrates AI-powered classification of e-waste items in industrial batches.
    Uses a predictor (from ml.inference.predictor) if provided, else rule-based fallback.
    """

    def __init__(self, predictor=None, batch_manager=None):
        self.predictor = predictor
        self.batch_manager = batch_manager

    def classify_item(
        self,
        item_id: int,
        image_path: str = None,
        feature_dict: dict = None,
    ) -> dict:
        """
        Classify a single e-waste item.
        Uses predictor if available, otherwise returns a placeholder pending manual classification.
        Always sets is_estimate=True when no trained model is used.
        """
        result = {
            "item_id": item_id,
            "device_type": "unknown",
            "confidence": 0.0,
            "top_predictions": [],
            "material_hints": {},
            "recommended_action": "expert_assessment",
            "is_estimate": True,
            "classification_method": "rule_based",
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }

        # Try AI predictor
        if self.predictor is not None:
            try:
                if image_path:
                    preds = self.predictor.predict_image(image_path, top_k=5)
                    if preds and not preds[0].get("error"):
                        top = preds[0]
                        result["device_type"] = top.get("class_name", "unknown")
                        result["confidence"] = top.get("confidence", 0.0)
                        result["top_predictions"] = preds
                        result["classification_method"] = "ai_cnn"
                        result["is_estimate"] = False
                elif feature_dict:
                    pred = self.predictor.predict_tabular(
                        feature_dict,
                        list(feature_dict.keys()),
                    )
                    if pred and not pred.get("error"):
                        result["device_type"] = pred.get("predicted_class", "unknown")
                        result["confidence"] = pred.get("confidence", 0.0)
                        result["classification_method"] = "ai_tabular"
                        result["is_estimate"] = False
            except Exception as e:
                logger.warning(f"Predictor failed for item {item_id}: {e}")
                result["classification_method"] = "rule_based_fallback"
                result["is_estimate"] = True

        # Enrich with material hints
        result["material_hints"] = self._estimate_materials(result["device_type"])
        result["recommended_action"] = self.get_recommended_action(
            result["device_type"], result["confidence"]
        )

        # Update batch manager if available
        if self.batch_manager is not None and result["confidence"] > 0:
            try:
                self.batch_manager.update_item_classification(
                    item_id,
                    result["device_type"],
                    result["confidence"],
                )
            except Exception as e:
                logger.warning(f"Could not update batch manager for item {item_id}: {e}")

        return result

    def classify_batch(self, batch_id: int, items: list) -> dict:
        """
        Classify all items in a batch.
        items: list of dicts with keys: item_id, image_path (optional), feature_dict (optional)
        """
        results = []
        errors = []

        for item in items:
            try:
                r = self.classify_item(
                    item_id=item.get("item_id", 0),
                    image_path=item.get("image_path"),
                    feature_dict=item.get("feature_dict"),
                )
                results.append(r)
            except Exception as e:
                errors.append({"item_id": item.get("item_id"), "error": str(e)})
                logger.error(f"Failed to classify item {item.get('item_id')}: {e}")

        # Aggregate stats
        actions = {}
        for r in results:
            a = r.get("recommended_action", "unknown")
            actions[a] = actions.get(a, 0) + 1

        avg_confidence = (
            sum(r.get("confidence", 0) for r in results) / len(results) if results else 0
        )

        return {
            "batch_id": batch_id,
            "total_items": len(items),
            "classified": len(results),
            "errors": len(errors),
            "error_details": errors,
            "average_confidence": round(avg_confidence, 4),
            "action_summary": actions,
            "results": results,
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }

    def get_recommended_action(self, device_type: str, confidence: float) -> str:
        """
        Determine recommended processing action based on confidence level.
        """
        if confidence >= 0.80:
            return "auto_process"
        elif confidence >= 0.50:
            return "manual_review"
        else:
            return "expert_assessment"

    def _estimate_materials(self, device_type: str) -> dict:
        """
        Return material composition estimates for a device type.
        Always labeled is_estimate=True.
        """
        normalized = device_type.lower().replace(" ", "_").replace("-", "_")
        # Fuzzy match
        for key in DEVICE_MATERIAL_ESTIMATES:
            if key in normalized or normalized in key:
                return DEVICE_MATERIAL_ESTIMATES[key].copy()
        return DEVICE_MATERIAL_ESTIMATES["default"].copy()
