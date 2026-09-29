import pandas as pd

class RecoveryRecommendationEngine:
    """Engine to recommend recovery methods and calculate value from e-waste."""
    def __init__(self):
        # Current average market prices in USD per gram
        self.material_prices = {
            'gold': 65.0,
            'silver': 0.85,
            'copper': 0.009,
            'palladium': 45.0,
            'platinum': 32.0,
            'lead': 0.002,
            'aluminum': 0.003,
            'rare_earth': 0.15,
            'plastic': 0.001,
            'glass': 0.0005,
            'cobalt': 0.03,
            'lithium': 0.02
        }
        
        self.recovery_methods = {
            'Mobile Phones': {
                'primary_method': 'chemical',
                'secondary_method': 'mechanical',
                'recovery_steps': [
                    '1. Remove battery manually',
                    '2. Dismantle casing and screen',
                    '3. Shred PCB (Printed Circuit Board)',
                    '4. Apply hydrometallurgical processing (acid leaching) to recover precious metals',
                    '5. Smelt plastics and lower grade metals'
                ],
                'required_equipment': ['Shredder', 'Acid Baths', 'Fume Hoods', 'PPE'],
                'safety_precautions': ['Acid resistant PPE', 'Ventilation', 'Fire safety for Li-ion'],
                'estimated_time_hours': 2.5,
                'difficulty_level': 'expert'
            },
            'Laptops': {
                'primary_method': 'mechanical',
                'secondary_method': 'thermal',
                'recovery_steps': [
                    '1. Remove battery and HDD',
                    '2. Separate RAM, CPU, and Motherboard',
                    '3. Mechanically shred chassis',
                    '4. Sort metals via eddy currents'
                ],
                'required_equipment': ['Screwdrivers', 'Eddy Current Separator', 'Shredder'],
                'safety_precautions': ['Gloves', 'Safety glasses'],
                'estimated_time_hours': 1.0,
                'difficulty_level': 'moderate'
            },
            'Desktop Computers': {
                'primary_method': 'manual',
                'secondary_method': 'mechanical',
                'recovery_steps': ['1. Open case', '2. Extract PSU, CPU, RAM, GPU', '3. Separate steel chassis', '4. Send PCB to chemical recovery'],
                'required_equipment': ['Basic hand tools'],
                'safety_precautions': ['Sharp edge protection', 'Heavy lifting precautions'],
                'estimated_time_hours': 0.5,
                'difficulty_level': 'easy'
            },
            'Tablets': {
                'primary_method': 'chemical',
                'secondary_method': 'mechanical',
                'recovery_steps': ['1. Heat to remove glued screen', '2. Extract glued battery', '3. Chemical leaching of PCB'],
                'required_equipment': ['Heat gun', 'Chemical bath'],
                'safety_precautions': ['Thermal gloves', 'Fume extraction'],
                'estimated_time_hours': 1.5,
                'difficulty_level': 'hard'
            },
            'Monitors/Displays': {
                'primary_method': 'mechanical',
                'secondary_method': 'manual',
                'recovery_steps': ['1. Remove plastic housing', '2. Extract PCB', '3. Separate LCD/LED panel', '4. Process glass'],
                'required_equipment': ['Screwdrivers', 'Glass processing unit'],
                'safety_precautions': ['Glass hazard PPE'],
                'estimated_time_hours': 0.75,
                'difficulty_level': 'moderate'
            },
            'Televisions': {
                'primary_method': 'manual',
                'secondary_method': 'mechanical',
                'recovery_steps': ['1. Dismantle outer shell', '2. Disconnect high voltage components', '3. Extract boards and copper coils'],
                'required_equipment': ['Discharge tools', 'Hand tools'],
                'safety_precautions': ['Capacitor discharge safety', 'Heavy lifting'],
                'estimated_time_hours': 1.5,
                'difficulty_level': 'hard'
            },
            'Printers': {
                'primary_method': 'mechanical',
                'secondary_method': 'manual',
                'recovery_steps': ['1. Remove ink/toner cartridges safely', '2. Shred plastic body', '3. Extract small motors and PCBs'],
                'required_equipment': ['Toner vacuum', 'Shredder'],
                'safety_precautions': ['Toner dust mask'],
                'estimated_time_hours': 1.0,
                'difficulty_level': 'moderate'
            },
            'Batteries': {
                'primary_method': 'chemical',
                'secondary_method': 'thermal',
                'recovery_steps': ['1. Discharge fully', '2. Mechanical shredding under inert gas', '3. Hydrometallurgical extraction of Co, Li, Ni'],
                'required_equipment': ['Discharge rig', 'Inert gas shredder', 'Chemical reactors'],
                'safety_precautions': ['Extreme fire hazard PPE', 'Explosion proof environment'],
                'estimated_time_hours': 4.0,
                'difficulty_level': 'expert'
            },
            'PCBs/Circuit Boards': {
                'primary_method': 'chemical',
                'secondary_method': 'thermal',
                'recovery_steps': ['1. Desolder valuable ICs', '2. Shred board', '3. Acid leaching for Au, Ag, Pd, Cu'],
                'required_equipment': ['Chemical baths', 'Fume hoods'],
                'safety_precautions': ['Acid resistant PPE', 'Toxic gas monitoring'],
                'estimated_time_hours': 3.0,
                'difficulty_level': 'expert'
            },
            'Cables & Wires': {
                'primary_method': 'mechanical',
                'secondary_method': 'thermal',
                'recovery_steps': ['1. Granulate cables', '2. Density separation of copper and plastic', '3. Smelt copper'],
                'required_equipment': ['Cable granulator', 'Air separator'],
                'safety_precautions': ['Dust masks', 'Hearing protection'],
                'estimated_time_hours': 0.5,
                'difficulty_level': 'easy'
            },
            'Small Appliances': {
                'primary_method': 'mechanical',
                'secondary_method': 'manual',
                'recovery_steps': ['1. Remove plug/cord', '2. Shred whole unit', '3. Magnetic separation of steel', '4. Eddy current for aluminum/copper'],
                'required_equipment': ['Industrial shredder', 'Magnetic separators'],
                'safety_precautions': ['Standard PPE', 'Noise protection'],
                'estimated_time_hours': 0.25,
                'difficulty_level': 'easy'
            },
            'Large Appliances': {
                'primary_method': 'mechanical',
                'secondary_method': 'manual',
                'recovery_steps': ['1. Recover refrigerants (if any)', '2. Remove compressor', '3. Heavy shredding of steel body', '4. Magnetic sort'],
                'required_equipment': ['Refrigerant recovery system', 'Heavy shredder', 'Cranes'],
                'safety_precautions': ['Gas recovery training', 'Heavy machinery protocols'],
                'estimated_time_hours': 1.0,
                'difficulty_level': 'moderate'
            },
            'Lighting Equipment': {
                'primary_method': 'chemical',
                'secondary_method': 'mechanical',
                'recovery_steps': ['1. Crush glass in vacuum', '2. Recover mercury vapor', '3. Separate aluminum caps and phosphor powder'],
                'required_equipment': ['Bulb crusher with vacuum', 'Mercury distillation'],
                'safety_precautions': ['Mercury hazard Hazmat', 'Respirators'],
                'estimated_time_hours': 0.5,
                'difficulty_level': 'hard'
            },
            'Audio/Video Equipment': {
                'primary_method': 'manual',
                'secondary_method': 'mechanical',
                'recovery_steps': ['1. Open chassis', '2. Extract copper transformers', '3. Remove PCBs', '4. Shred plastic casing'],
                'required_equipment': ['Hand tools', 'Shredder'],
                'safety_precautions': ['Standard PPE'],
                'estimated_time_hours': 0.75,
                'difficulty_level': 'easy'
            },
            'Networking Equipment': {
                'primary_method': 'manual',
                'secondary_method': 'chemical',
                'recovery_steps': ['1. Remove high-grade telecom PCBs', '2. Extract gold-plated connectors', '3. Send PCBs to chemical refining'],
                'required_equipment': ['Hand tools', 'Desoldering equipment'],
                'safety_precautions': ['Standard PPE'],
                'estimated_time_hours': 0.75,
                'difficulty_level': 'moderate'
            }
        }
        
        # Approximate grams of material recoverable per average unit
        self.material_recovery_rates = {
            'Mobile Phones': {'gold': 0.034, 'silver': 0.35, 'copper': 15.0, 'palladium': 0.015, 'cobalt': 5.0, 'plastic': 40.0, 'glass': 30.0},
            'Laptops': {'gold': 0.22, 'silver': 1.1, 'copper': 120.0, 'aluminum': 250.0, 'plastic': 800.0, 'cobalt': 35.0},
            'Desktop Computers': {'gold': 0.35, 'silver': 1.5, 'copper': 350.0, 'aluminum': 450.0, 'plastic': 1500.0, 'lead': 5.0},
            'Tablets': {'gold': 0.08, 'silver': 0.5, 'copper': 45.0, 'aluminum': 150.0, 'plastic': 200.0, 'glass': 100.0, 'cobalt': 20.0},
            'Monitors/Displays': {'gold': 0.05, 'copper': 80.0, 'aluminum': 120.0, 'plastic': 2500.0, 'glass': 1500.0},
            'Televisions': {'gold': 0.05, 'copper': 300.0, 'aluminum': 400.0, 'plastic': 6000.0, 'glass': 3000.0},
            'Printers': {'gold': 0.02, 'copper': 150.0, 'aluminum': 50.0, 'plastic': 4500.0},
            'Batteries': {'cobalt': 250.0, 'lithium': 50.0, 'copper': 100.0, 'aluminum': 100.0},
            'PCBs/Circuit Boards': {'gold': 0.5, 'silver': 2.5, 'palladium': 0.1, 'copper': 500.0, 'lead': 15.0},
            'Cables & Wires': {'copper': 600.0, 'plastic': 400.0},
            'Small Appliances': {'copper': 120.0, 'aluminum': 80.0, 'plastic': 800.0},
            'Large Appliances': {'copper': 800.0, 'aluminum': 1500.0, 'plastic': 4000.0},
            'Lighting Equipment': {'aluminum': 15.0, 'glass': 150.0, 'rare_earth': 2.0},
            'Audio/Video Equipment': {'gold': 0.05, 'copper': 200.0, 'aluminum': 150.0, 'plastic': 1500.0},
            'Networking Equipment': {'gold': 0.3, 'silver': 1.2, 'palladium': 0.08, 'copper': 250.0, 'aluminum': 200.0, 'plastic': 1000.0}
        }
    
    def get_recommendation(self, device_type, features_dict=None):
        if device_type not in self.recovery_methods:
            return {"error": f"Unknown device type: {device_type}"}
            
        method_info = self.recovery_methods[device_type]
        materials = self.material_recovery_rates.get(device_type, {})
        
        # Calculate value
        total_value = 0.0
        recoverable_materials_val = {}
        for mat, amount_grams in materials.items():
            price = self.material_prices.get(mat, 0)
            value = amount_grams * price
            recoverable_materials_val[mat] = {'amount_g': amount_grams, 'value_usd': round(value, 4)}
            total_value += value
            
        cost_of_processing = method_info['estimated_time_hours'] * 15.0 # Assuming $15/hr operational cost
        net_value = total_value - cost_of_processing
        
        return {
            'device_type': device_type,
            'recoverable_materials': recoverable_materials_val,
            'estimated_value_usd': round(total_value, 2),
            'recovery_method': method_info['primary_method'],
            'secondary_method': method_info['secondary_method'],
            'recovery_steps': method_info['recovery_steps'],
            'safety_precautions': method_info['safety_precautions'],
            'equipment_needed': method_info['required_equipment'],
            'difficulty': method_info['difficulty_level'],
            'time_estimate': f"{method_info['estimated_time_hours']} hours",
            'facility_type': 'Specialized E-Waste Refinery' if method_info['difficulty_level'] == 'expert' else 'Standard Recycling Plant',
            'cost_benefit_analysis': {
                'gross_value_usd': round(total_value, 2),
                'estimated_processing_cost_usd': round(cost_of_processing, 2),
                'net_value_usd': round(net_value, 2),
                'is_profitable': net_value > 0
            }
        }
    
    def batch_recommendations(self, predictions_df):
        recommendations = []
        for _, row in predictions_df.iterrows():
            device = row['device_type'] if 'device_type' in row else row['prediction']
            rec = self.get_recommendation(device)
            recommendations.append(rec)
        return recommendations
    
    def get_material_summary(self, predictions_df):
        total_materials = {}
        total_value = 0.0
        
        for _, row in predictions_df.iterrows():
            device = row['device_type'] if 'device_type' in row else row['prediction']
            mats = self.material_recovery_rates.get(device, {})
            
            for mat, amount in mats.items():
                if mat not in total_materials:
                    total_materials[mat] = 0.0
                total_materials[mat] += amount
                total_value += amount * self.material_prices.get(mat, 0)
                
        return {
            'total_materials_recovered_g': total_materials,
            'total_portfolio_value_usd': round(total_value, 2)
        }
