"""
Unit tests for 3D Viewer & Asset Registry Integration
"""

import unittest
from app.three_d_viewer import generate_3d_viewer
from src.asset_registry import get_asset_record, list_registered_assets, ASSET_REGISTRY

class Test3DViewerAndAssets(unittest.TestCase):
    def test_generate_3d_viewer_html(self):
        sample_device = {
            "brand": "Realme",
            "model": "Realme 11 Pro+ 5G (Sunrise Beige)",
            "category": "Mobile Phones",
            "chassis_color": "#E6D7C3",
            "accent_color": "#FFD700",
            "frame_color": "#D4AF37",
            "camera_module_type": "circular_matrix",
            "has_racing_stripe": True
        }
        html = generate_3d_viewer(sample_device, height=600)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Three.js", html)
        self.assertIn("GLTFLoader", html)
        self.assertIn("createLeatherTexture", html)
        self.assertIn("switchModelMode", html)
        self.assertIn("REALME", html)

    def test_asset_registry_lookup(self):
        record = get_asset_record("realme_11_pro")
        self.assertEqual(record["brand"], "Realme")
        self.assertEqual(record["verification_status"], "VERIFIED_EXACT_MATCH")
        self.assertIn("components", record)
        self.assertGreater(len(record["components"]), 5)

    def test_asset_registry_fuzzy_lookup(self):
        record = get_asset_record("iphone")
        self.assertEqual(record["brand"], "Apple")
        self.assertIn("iphone_15_pro.glb", record["asset_file"])

    def test_asset_registry_fallback(self):
        record = get_asset_record("unknown_microwave_123")
        self.assertEqual(record["verification_status"], "ESTIMATED_GENERIC_FALLBACK")
        self.assertIn("recovery_data", record)

    def test_list_registered_assets(self):
        assets = list_registered_assets()
        self.assertGreaterEqual(len(assets), 4)
        ids = [a["id"] for a in assets]
        self.assertIn("realme_11_pro", ids)
        self.assertIn("iphone_15_pro", ids)
        self.assertIn("circuit_board_pcb", ids)

if __name__ == "__main__":
    unittest.main()
