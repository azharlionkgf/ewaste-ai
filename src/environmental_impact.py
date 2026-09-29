import pandas as pd

class EnvironmentalImpactCalculator:
    """Calculates environmental savings from properly recycling E-Waste."""
    def __init__(self):
        # Base environmental savings per kg of e-waste recycled vs landfilled
        # (These are simulated constants based on typical LCA studies)
        self.co2_factors = {
            'Mobile Phones': 0.15, 'Laptops': 2.5, 'Desktop Computers': 7.5,
            'Tablets': 0.8, 'Monitors/Displays': 5.0, 'Televisions': 12.0,
            'Printers': 4.5, 'Batteries': 0.5, 'PCBs/Circuit Boards': 1.2,
            'Cables & Wires': 0.8, 'Small Appliances': 2.0, 'Large Appliances': 25.0,
            'Lighting Equipment': 0.3, 'Audio/Video Equipment': 3.5, 'Networking Equipment': 2.2
        } # kg CO2 equivalent saved per unit
        
        self.water_savings = {
            'Mobile Phones': 50, 'Laptops': 500, 'Desktop Computers': 1500,
            'Tablets': 200, 'Monitors/Displays': 800, 'Televisions': 1800,
            'Printers': 600, 'Batteries': 150, 'PCBs/Circuit Boards': 300,
            'Cables & Wires': 100, 'Small Appliances': 300, 'Large Appliances': 4000,
            'Lighting Equipment': 20, 'Audio/Video Equipment': 400, 'Networking Equipment': 500
        } # Liters of water saved per unit
        
        self.energy_savings = {
            'Mobile Phones': 2.5, 'Laptops': 45.0, 'Desktop Computers': 120.0,
            'Tablets': 12.0, 'Monitors/Displays': 80.0, 'Televisions': 150.0,
            'Printers': 65.0, 'Batteries': 10.0, 'PCBs/Circuit Boards': 25.0,
            'Cables & Wires': 8.0, 'Small Appliances': 25.0, 'Large Appliances': 300.0,
            'Lighting Equipment': 2.0, 'Audio/Video Equipment': 35.0, 'Networking Equipment': 40.0
        } # kWh saved per unit
        
        self.toxic_prevention = {
            'Mobile Phones': 0.05, 'Laptops': 0.2, 'Desktop Computers': 0.5,
            'Tablets': 0.1, 'Monitors/Displays': 1.5, 'Televisions': 3.0,
            'Printers': 0.3, 'Batteries': 0.4, 'PCBs/Circuit Boards': 0.2,
            'Cables & Wires': 0.1, 'Small Appliances': 0.2, 'Large Appliances': 1.0,
            'Lighting Equipment': 0.05, 'Audio/Video Equipment': 0.2, 'Networking Equipment': 0.15
        } # kg of toxic leakage (lead, mercury, etc.) prevented
    
    def calculate_impact(self, device_type, quantity=1):
        if device_type not in self.co2_factors:
            return {"error": "Unknown device type"}
            
        return {
            'co2_saved_kg': self.co2_factors[device_type] * quantity,
            'water_saved_liters': self.water_savings[device_type] * quantity,
            'energy_saved_kwh': self.energy_savings[device_type] * quantity,
            'toxic_prevented_kg': self.toxic_prevention[device_type] * quantity
        }
    
    def batch_impact(self, predictions_df):
        total_co2 = 0
        total_water = 0
        total_energy = 0
        total_toxic = 0
        
        for _, row in predictions_df.iterrows():
            device = row['device_type'] if 'device_type' in row else row['prediction']
            impact = self.calculate_impact(device, quantity=1)
            if 'error' not in impact:
                total_co2 += impact['co2_saved_kg']
                total_water += impact['water_saved_liters']
                total_energy += impact['energy_saved_kwh']
                total_toxic += impact['toxic_prevented_kg']
                
        return {
            'total_co2_saved_kg': total_co2,
            'total_water_saved_liters': total_water,
            'total_energy_saved_kwh': total_energy,
            'total_toxic_prevented_kg': total_toxic
        }
    
    def get_impact_summary(self, predictions_df):
        totals = self.batch_impact(predictions_df)
        
        # Equivalences
        trees_equivalent = totals['total_co2_saved_kg'] / 21.0 # ~21kg CO2 per tree per year
        cars_equivalent = totals['total_co2_saved_kg'] / 4600.0 # ~4.6 metric tons per car per year
        homes_powered = totals['total_energy_saved_kwh'] / 893.0 # ~893 kWh per home per month
        
        return {
            'Metrics': totals,
            'Equivalences': {
                'Trees Planted (absorbing 1 year)': round(trees_equivalent, 2),
                'Cars Taken Off Road (1 year)': round(cars_equivalent, 4),
                'Homes Powered (1 month)': round(homes_powered, 2)
            }
        }
    
    def get_sdg_alignment(self, device_type):
        return [
            "Goal 12: Responsible Consumption and Production",
            "Goal 13: Climate Action",
            "Goal 9: Industry, Innovation and Infrastructure",
            "Goal 11: Sustainable Cities and Communities"
        ]
