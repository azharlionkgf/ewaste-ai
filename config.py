import os

# Project Root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Target Categories
E_WASTE_CATEGORIES = [
    'Mobile Phones', 'Laptops', 'Desktop Computers', 'Tablets', 
    'Monitors/Displays', 'Televisions', 'Printers', 'Batteries', 
    'PCBs/Circuit Boards', 'Cables & Wires', 'Small Appliances', 
    'Large Appliances', 'Lighting Equipment', 'Audio/Video Equipment', 
    'Networking Equipment'
]

# Constants
RANDOM_SEED = 42
DATASET_SIZE = 10000
TEST_SIZE = 0.2
N_FOLDS = 10

# Directory Paths
DIRS = {
    'raw_data': os.path.join(PROJECT_ROOT, 'data', 'raw'),
    'processed_data': os.path.join(PROJECT_ROOT, 'data', 'processed'),
    'models': os.path.join(PROJECT_ROOT, 'models', 'saved'),
    'figures': os.path.join(PROJECT_ROOT, 'reports', 'figures'),
    'metrics': os.path.join(PROJECT_ROOT, 'reports', 'metrics')
}

# Feature definitions
TARGET_COLUMN = 'device_type'

NUMERICAL_FEATURES = [
    'weight_kg', 'length_cm', 'width_cm', 'height_cm',
    'plastic_pct', 'metal_pct', 'glass_pct', 'pcb_pct', 'ceramic_pct',
    'gold_mg', 'silver_mg', 'copper_g', 'palladium_mg', 'platinum_mg',
    'rare_earth_g', 'age_years', 'condition_score', 'repair_count',
    'battery_health_pct', 'screen_size_inch', 'power_consumption_watts',
    'manufacturing_year', 'original_price_usd', 'component_count',
    'connector_count', 'storage_capacity_gb'
]

CATEGORICAL_FEATURES = [
    'functional_status', 'damage_level', 'energy_rating',
    'brand_tier', 'country_of_origin'
]

BINARY_FEATURES = [
    'lead_present', 'mercury_present', 'cadmium_present', 
    'chromium_present', 'bfr_present', 'battery_present',
    'screen_present', 'data_storage_present'
]

# Plot Color Scheme
COLOR_SCHEME = {
    'primary': '#00ADB5',
    'secondary': '#393E46',
    'background': '#222831',
    'text': '#EEEEEE',
    'accent_1': '#F08A5D',
    'accent_2': '#B83B5E',
    'accent_3': '#6A2C70'
}
