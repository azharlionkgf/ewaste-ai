"""
Unit tests for 3D Viewer (asset_registry removed — unused enterprise dead code)
"""

import unittest
from app.three_d_viewer import generate_3d_viewer

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

    def test_3d_viewer_laptop(self):
        html = generate_3d_viewer({"category": "Laptops", "brand": "Dell", "model": "XPS 15"})
        self.assertIn("buildLaptopLayers", html)
        self.assertNotIn("__SHAPE_TYPE__", html)

    def test_3d_viewer_pcb(self):
        html = generate_3d_viewer({"category": "PCBs/Circuit Boards", "brand": "Intel", "model": "Z790"})
        self.assertIn("buildPCBLayers", html)
        self.assertNotIn("__SHAPE_TYPE__", html)

    def test_3d_viewer_all_categories(self):
        cats = ["Mobile Phones","Laptops","Desktop Computers","Tablets","Televisions","Batteries","PCBs/Circuit Boards"]
        for cat in cats:
            html = generate_3d_viewer({"category": cat, "brand": "Test", "model": "M1"})
            self.assertIn("function init()", html)
            self.assertIn("function animate()", html)
            self.assertNotIn("__SHAPE_TYPE__", html)

    def test_3d_viewer_has_hologram(self):
        html = generate_3d_viewer({"category": "Mobile Phones", "brand": "Samsung", "model": "S23"})
        self.assertIn("holoContainer", html)
        self.assertIn("holoScanLines", html)
        self.assertIn("CylinderGeometry", html)

if __name__ == "__main__":
    unittest.main()
