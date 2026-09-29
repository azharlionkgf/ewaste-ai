"""
Generate realistic synthetic e-waste data for classification.
"""
import os
import pandas as pd
import numpy as np
import sys

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from src.utils import setup_directories, get_logger

logger = get_logger(__name__)

def generate_synthetic_data(num_samples=config.DATASET_SIZE, random_seed=config.RANDOM_SEED):
    """Generates synthetic E-Waste dataset with distinct device profiles."""
    np.random.seed(random_seed)
    
    device_types = config.E_WASTE_CATEGORIES
    n_devices = len(device_types)
    
    data = []
    
    # Base profiles for separability (Mean values)
    # [weight, len, wid, height, plastic%, metal%, glass%, pcb%, ceramic%, 
    # gold, silver, copper, palladium, platinum, rare_earth, 
    # power, original_price, comp_count, conn_count]
    base_profiles = {
        'Mobile Phones': [0.15, 15, 7, 0.8, 20, 30, 40, 9, 1, 30, 300, 15, 10, 1, 2, 5, 800, 50, 2],
        'Laptops': [1.5, 35, 25, 2, 30, 40, 10, 18, 2, 200, 1000, 150, 50, 5, 10, 45, 1200, 200, 10],
        'Desktop Computers': [8, 45, 20, 45, 20, 60, 2, 16, 2, 300, 1500, 300, 80, 10, 15, 250, 900, 300, 20],
        'Tablets': [0.5, 25, 18, 0.6, 25, 30, 35, 9, 1, 50, 400, 25, 15, 2, 4, 15, 600, 80, 2],
        'Monitors/Displays': [5, 60, 40, 10, 40, 30, 20, 8, 2, 50, 200, 100, 10, 2, 5, 40, 300, 150, 5],
        'Televisions': [15, 120, 70, 8, 45, 35, 10, 8, 2, 80, 300, 200, 20, 5, 10, 120, 700, 250, 10],
        'Printers': [7, 45, 35, 25, 60, 25, 5, 8, 2, 30, 150, 80, 5, 1, 2, 35, 150, 300, 8],
        'Batteries': [0.2, 10, 5, 5, 10, 80, 0, 5, 5, 5, 10, 20, 1, 0, 0, 0, 20, 5, 2],
        'PCBs/Circuit Boards': [0.3, 20, 15, 0.2, 10, 40, 5, 40, 5, 400, 2000, 100, 150, 20, 5, 0, 50, 500, 50],
        'Cables & Wires': [0.5, 200, 1, 1, 40, 60, 0, 0, 0, 0, 0, 450, 0, 0, 0, 0, 15, 1, 2],
        'Small Appliances': [2, 30, 20, 20, 50, 40, 5, 3, 2, 5, 20, 80, 2, 0, 1, 800, 100, 50, 3],
        'Large Appliances': [50, 80, 80, 160, 20, 70, 5, 3, 2, 20, 100, 800, 10, 5, 5, 1500, 800, 150, 10],
        'Lighting Equipment': [0.1, 15, 5, 5, 30, 20, 45, 3, 2, 1, 5, 10, 0, 0, 30, 15, 10, 10, 2],
        'Audio/Video Equipment': [4, 40, 30, 15, 40, 40, 5, 12, 3, 40, 150, 150, 10, 2, 8, 100, 400, 200, 15],
        'Networking Equipment': [1.2, 25, 18, 4, 30, 40, 0, 25, 5, 100, 300, 80, 30, 5, 2, 25, 200, 150, 12]
    }
    
    # Categorical distributions
    func_status = ['working', 'partial', 'non_functional']
    damage_lvls = ['none', 'minor', 'moderate', 'severe']
    energy_ratings = ['A+++', 'A++', 'A+', 'A', 'B', 'C', 'D']
    brands = ['premium', 'mid_range', 'budget']
    countries = ['China', 'USA', 'Japan', 'South Korea', 'Germany', 'Vietnam', 'India']
    
    logger.info(f"Generating {num_samples} samples of e-waste data...")
    
    # Pre-calculate counts for each device
    counts = np.random.multinomial(num_samples, [1/n_devices]*n_devices)
    
    for i, device in enumerate(device_types):
        n = counts[i]
        if n == 0: continue
        
        prof = base_profiles[device]
        
        def gen_norm(mean, std_ratio=0.1, n=n, clip_min=0):
            return np.clip(np.random.normal(mean, max(mean * std_ratio, 0.001), n), clip_min, None)
            
        weight = gen_norm(prof[0])
        length = gen_norm(prof[1])
        width = gen_norm(prof[2])
        height = gen_norm(prof[3])
        
        # Compositions
        plas, met, glas, pcb, cer = gen_norm(prof[4]), gen_norm(prof[5]), gen_norm(prof[6]), gen_norm(prof[7]), gen_norm(prof[8])
        total_comp = plas + met + glas + pcb + cer + 1e-5
        plas, met, glas, pcb, cer = plas/total_comp*100, met/total_comp*100, glas/total_comp*100, pcb/total_comp*100, cer/total_comp*100
        
        au, ag, cu, pd_mg, pt, re = gen_norm(prof[9]), gen_norm(prof[10]), gen_norm(prof[11]), gen_norm(prof[12]), gen_norm(prof[13]), gen_norm(prof[14])
        power, price = gen_norm(prof[15]), gen_norm(prof[16])
        comp_c, conn_c = np.round(gen_norm(prof[17])).astype(int), np.round(gen_norm(prof[18])).astype(int)
        
        age = np.random.uniform(0.5, 20, n)
        cond = np.clip(np.round(np.random.normal(5, 2, n)), 1, 10)
        cond = np.clip(cond - (age * 0.2), 1, 10) # Correlate condition with age
        repair = np.clip(np.round(np.random.exponential(1.5, n)).astype(int), 0, 10)
        year = 2024 - age
        
        has_batt = np.random.rand(n) < (0.9 if device in ['Mobile Phones', 'Laptops', 'Tablets'] else (1.0 if device == 'Batteries' else 0.05))
        has_screen = np.random.rand(n) < (0.95 if device in ['Mobile Phones', 'Laptops', 'Tablets', 'Monitors/Displays', 'Televisions'] else 0.01)
        has_storage = np.random.rand(n) < (0.9 if device in ['Mobile Phones', 'Laptops', 'Desktop Computers', 'Tablets'] else 0.05)
        
        lead = np.random.rand(n) < (0.8 if device in ['Monitors/Displays', 'Televisions', 'PCBs/Circuit Boards'] else 0.2)
        mercury = np.random.rand(n) < (0.9 if device == 'Lighting Equipment' else 0.05)
        cadmium = np.random.rand(n) < (0.8 if device == 'Batteries' else 0.1)
        chromium = np.random.rand(n) < (0.5 if device in ['Large Appliances', 'Desktop Computers'] else 0.1)
        bfr = np.random.rand(n) < (0.7 if device in ['PCBs/Circuit Boards', 'Laptops', 'Desktop Computers', 'Networking Equipment'] else 0.2)
        
        batt_health = np.where(has_batt, np.clip(np.random.normal(60 - age*3, 20, n), 0, 100), np.nan)
        scr_size = np.where(has_screen, gen_norm(prof[1] * 0.8), np.nan)
        storage = np.where(has_storage, np.random.choice([16, 32, 64, 128, 256, 512, 1024, 2048], n), np.nan)
        
        df = pd.DataFrame({
            'device_type': [device]*n,
            'weight_kg': weight, 'length_cm': length, 'width_cm': width, 'height_cm': height,
            'plastic_pct': plas, 'metal_pct': met, 'glass_pct': glas, 'pcb_pct': pcb, 'ceramic_pct': cer,
            'gold_mg': au, 'silver_mg': ag, 'copper_g': cu, 'palladium_mg': pd_mg, 'platinum_mg': pt, 'rare_earth_g': re,
            'age_years': age, 'condition_score': cond, 'repair_count': repair,
            'battery_health_pct': batt_health, 'screen_size_inch': scr_size, 'storage_capacity_gb': storage,
            'power_consumption_watts': power, 'manufacturing_year': year, 'original_price_usd': price,
            'component_count': comp_c, 'connector_count': conn_c,
            'functional_status': np.random.choice(func_status, n, p=[0.3, 0.4, 0.3]),
            'damage_level': np.random.choice(damage_lvls, n, p=[0.2, 0.4, 0.3, 0.1]),
            'energy_rating': np.random.choice(energy_ratings, n),
            'brand_tier': np.random.choice(brands, n, p=[0.3, 0.5, 0.2]),
            'country_of_origin': np.random.choice(countries, n),
            'lead_present': lead, 'mercury_present': mercury, 'cadmium_present': cadmium, 
            'chromium_present': chromium, 'bfr_present': bfr, 'battery_present': has_batt,
            'screen_present': has_screen, 'data_storage_present': has_storage
        })
        data.append(df)
        
    final_df = pd.concat(data, ignore_index=True).sample(frac=1, random_state=random_seed).reset_index(drop=True)
    
    setup_directories()
    out_path = os.path.join(config.DIRS['raw_data'], 'e_waste_data.csv')
    final_df.to_csv(out_path, index=False)
    logger.info(f"Generated data saved to {out_path}")
    return final_df

if __name__ == '__main__':
    generate_synthetic_data()
