"""
🧪 Automated Test Suite for E-Waste Intelligence Platform
========================================================
Covers i18n, currency conversions, safety compliance protocols,
recovery engine calculations, and knowledge engine database integrity.
"""

import unittest
import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.i18n import get_text, convert_currency, format_recovery_range, SUPPORTED_LANGUAGES, CURRENCY_RATES
from src.safety_compliance import get_hazard_protocol, get_regulatory_framework, HAZARD_PROTOCOLS, GLOBAL_REGULATIONS
from src.recovery_engine import RecoveryRecommendationEngine
from src.environmental_impact import EnvironmentalImpactCalculator
from app.knowledge_engine import DEVICE_KNOWLEDGE, get_device_info, save_device_knowledge, get_device_knowledge

class TestInternationalization(unittest.TestCase):
    def test_supported_languages(self):
        self.assertIn('en', SUPPORTED_LANGUAGES)
        self.assertIn('hi', SUPPORTED_LANGUAGES)
        self.assertIn('es', SUPPORTED_LANGUAGES)

    def test_translation_retrieval(self):
        en_title = get_text('app_title', 'en')
        hi_title = get_text('app_title', 'hi')
        self.assertEqual(en_title, 'E-WASTE INTELLIGENCE SYSTEM')
        self.assertIn('ई-कचरा', hi_title)

    def test_currency_conversion(self):
        usd_amt = 100.0
        inr_val, symbol, formatted = convert_currency(usd_amt, 'INR')
        self.assertEqual(symbol, '₹')
        self.assertGreater(inr_val, 8000.0)
        self.assertIn('INR', formatted)

    def test_recovery_range_formatting(self):
        res = format_recovery_range(50.0, 'USD', uncertainty_pct=20.0)
        self.assertIn('$50.00', res)
        self.assertIn('$40.00', res)
        self.assertIn('$60.00', res)

class TestSafetyCompliance(unittest.TestCase):
    def test_hazard_protocol_thermal_runaway(self):
        proto = get_hazard_protocol('battery_thermal_runaway')
        self.assertEqual(proto['action'], 'STOP WORK IMMEDIATELY')
        self.assertIn('CRITICAL', proto['severity'])
        self.assertTrue(len(proto['instructions']) >= 3)

    def test_hazard_protocol_capacitors(self):
        proto = get_hazard_protocol('high_voltage_capacitors')
        self.assertIn('DISCHARGE', proto['action'])

    def test_regulatory_framework_india(self):
        reg = get_regulatory_framework('India')
        self.assertIn('CPCB', reg['agency'])
        self.assertIn('E-Waste (Management) Rules', reg['statute'])

    def test_regulatory_framework_eu(self):
        reg = get_regulatory_framework('European Union')
        self.assertIn('WEEE Directive', reg['statute'])

class TestRecoveryEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RecoveryRecommendationEngine()

    def test_mobile_recommendation(self):
        rec = self.engine.get_recommendation('Mobile Phones')
        self.assertNotIn('error', rec)
        self.assertIn('recoverable_materials', rec)
        self.assertGreater(rec['estimated_value_usd'], 0.0)
        cb = rec['cost_benefit_analysis']
        self.assertIn('gross_value_range_usd', cb)
        self.assertIn('net_value_range_usd', cb)
        self.assertTrue(len(cb['gross_value_range_usd']) == 2)
        # Check lower bound is less than upper bound
        self.assertLess(cb['gross_value_range_usd'][0], cb['gross_value_range_usd'][1])

    def test_unknown_device_handling(self):
        rec = self.engine.get_recommendation('NonExistentDeviceTypeXYZ')
        self.assertIn('error', rec)

class TestEnvironmentalImpact(unittest.TestCase):
    def setUp(self):
        self.calc = EnvironmentalImpactCalculator()

    def test_impact_calculation(self):
        imp = self.calc.calculate_impact('Laptops', quantity=2)
        self.assertNotIn('error', imp)
        self.assertEqual(imp['co2_saved_kg'], 5.0) # 2.5 * 2
        self.assertEqual(imp['water_saved_liters'], 1000) # 500 * 2

class TestKnowledgeEngine(unittest.TestCase):
    def test_device_knowledge_coverage(self):
        # Must have at least 15 comprehensive categories now
        self.assertGreaterEqual(len(DEVICE_KNOWLEDGE), 15)
        self.assertIn('Mobile Phones', DEVICE_KNOWLEDGE)
        self.assertIn('Servers & Data Centers', DEVICE_KNOWLEDGE)
        self.assertIn('Solar Inverters & Renewables', DEVICE_KNOWLEDGE)
        self.assertIn('Medical & Diagnostic Electronics', DEVICE_KNOWLEDGE)

    def test_device_info_lookup(self):
        info = get_device_info('Solar Inverters & Renewables')
        self.assertIsNotNone(info)
        self.assertEqual(info['category'], 'Solar Inverters & Renewables')
        self.assertTrue(len(info['components']) >= 5)

if __name__ == '__main__':
    unittest.main()
