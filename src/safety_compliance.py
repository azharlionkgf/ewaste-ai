"""
⚠️ Safety Protocols & Global Regulatory Compliance Engine
=========================================================
Jurisdiction-specific regulatory databases (CPCB, EU WEEE, US EPA, Basel)
and critical stop-work protocols for hazardous components.
"""

from typing import Dict, List, Any

# Critical Stop-Work Hazards requiring qualified intervention
HAZARD_PROTOCOLS = {
    'battery_thermal_runaway': {
        'hazard': 'Swollen / Damaged Lithium-Ion Battery',
        'severity': 'CRITICAL (Fire & Explosion Hazard)',
        'action': 'STOP WORK IMMEDIATELY',
        'instructions': [
            'Do NOT puncture, crush, bend, or force open the casing.',
            'Immediately isolate the unit inside an airtight, non-combustible metal container filled with dry sand or vermiculite.',
            'Keep away from flammable structures, liquids, and oxygen sources.',
            'Never dispose of in household municipal waste or trash compactors.',
            'Contact a certified hazardous waste handler or manufacturer take-back center.'
        ]
    },
    'crt_implosion': {
        'hazard': 'Cathode Ray Tube (CRT) High-Vacuum & Lead Glass',
        'severity': 'HIGH (Implosion & Toxic Lead Poisoning)',
        'action': 'SPECIALIZED DISMANTLING REQUIRED',
        'instructions': [
            'Do NOT break the funnel or glass faceplate.',
            'CRTs maintain a deep internal vacuum and contain 1.5 to 3 kg of toxic lead in the funnel glass.',
            'Wear full face protection and Kevlar cut-resistant gloves.',
            'Only discharge anode residual high-voltage (up to 25kV) using an insulated grounding tool before opening.'
        ]
    },
    'refrigerant_leak': {
        'hazard': 'Pressurized Refrigerants (CFC, HCFC, HFC, Isobutane R600a)',
        'severity': 'HIGH (Ozone Depletion, Flammability, Asphyxiation)',
        'action': 'CERTIFIED HVAC RECOVERY ONLY',
        'instructions': [
            'Illegal venting violates international environmental laws (Clean Air Act, Montreal Protocol).',
            'Isobutane (R600a) is highly explosive; work in spark-free explosion-proof environments.',
            'Refrigerant gas must be extracted using a sealed closed-loop recovery machine before compressor removal.'
        ]
    },
    'high_voltage_capacitors': {
        'hazard': 'Charged Power Supply Capacitors (SMPS / Inverters / Microwave Transformers)',
        'severity': 'LETHAL (Electric Shock Hazard)',
        'action': 'DISCHARGE BEFORE TOUCHING',
        'instructions': [
            'Power supply capacitors and microwave magnetrons store lethal DC voltages (300V - 2000V) long after unplugging.',
            'Wait minimum 30 minutes after disconnection, then discharge across a 10k ohm 10W power resistor.',
            'Never bridge high-voltage terminals directly with a standard screwdriver.'
        ]
    }
}

# Global Regulatory Frameworks
GLOBAL_REGULATIONS = {
    'India': {
        'jurisdiction': 'Republic of India',
        'agency': 'Central Pollution Control Board (CPCB) / MoEFCC',
        'statute': 'E-Waste (Management) Rules, 2022',
        'effective_date': 'April 1, 2023',
        'key_requirements': [
            'Extended Producer Responsibility (EPR) mandatory for manufacturers and importers.',
            'Producers must meet graduated recycling targets through registered recyclers on the CPCB portal.',
            'Informal burning (acid leaching/open smelting) is strictly prohibited under Environment Protection Act, 1986.',
            'Penalties include environmental compensation and imprisonment for non-compliance.'
        ],
        'compliance_tier': 'Mandatory Registration'
    },
    'European Union': {
        'jurisdiction': 'European Union (EU-27)',
        'agency': 'European Commission / National Environmental Agencies',
        'statute': 'WEEE Directive (2012/19/EU) & RoHS Directive (2011/65/EU)',
        'effective_date': 'Current Recast',
        'key_requirements': [
            'RoHS restricts Lead (Pb), Mercury (Hg), Cadmium (Cd), Hexavalent Chromium (Cr6+), PBBs, and PBDEs (<0.1% / <0.01% Cd).',
            'Minimum collection target of 65% of average weight of EEE placed on the market in the three preceding years.',
            'Producers must finance separate collection, treatment, and environmentally sound disposal.',
            'Retailers must offer free 1:1 take-back of very small e-waste (<25 cm) without purchase obligation.'
        ],
        'compliance_tier': 'Comprehensive Statutory Standard'
    },
    'United States': {
        'jurisdiction': 'United States of America',
        'agency': 'US Environmental Protection Agency (EPA) & State Regulators',
        'statute': 'Resource Conservation and Recovery Act (RCRA) & State E-Waste Mandates',
        'effective_date': 'Varies by State (28 States have E-Waste Acts)',
        'key_requirements': [
            'Cathode Ray Tubes (CRTs) and certain toxic components are classified as hazardous waste under 40 CFR 261.',
            'Commercial generators cannot dispose of CRTs or mercury-containing lamps in municipal landfills.',
            'State-specific producer responsibility laws (e.g. California SB 20/SB 50, NY State E-Waste Act) mandate funding.',
            'Certification programs (e-Stewards, R2v3) provide verified third-party facility audits.'
        ],
        'compliance_tier': 'Hybrid Federal/State Matrix'
    },
    'International': {
        'jurisdiction': 'Global Transboundary',
        'agency': 'United Nations Environment Programme (UNEP)',
        'statute': 'Basel Convention on the Control of Transboundary Movements of Hazardous Wastes',
        'effective_date': 'E-Waste Amendments (Effective Jan 1, 2025)',
        'key_requirements': [
            'All e-waste movements (hazardous or non-hazardous) require Prior Informed Consent (PIC) before export.',
            'Prevents illegal dumping of toxic electronic scrap into developing nations under guise of second-hand reuse.',
            'Exporters must prove importing facility operates state-of-the-art environmentally sound recovery.'
        ],
        'compliance_tier': 'International Treaty'
    }
}

def get_hazard_protocol(hazard_key: str) -> Dict[str, Any]:
    """Retrieve safety handling instructions for dangerous components."""
    return HAZARD_PROTOCOLS.get(hazard_key, {
        'hazard': 'General Electrical & Physical Risk',
        'severity': 'MODERATE',
        'action': 'STANDARD PPE REQUIRED',
        'instructions': ['Disconnect power.', 'Wear safety glasses and puncture-resistant gloves.', 'Work in ventilated area.']
    })

def get_regulatory_framework(country: str = 'India') -> Dict[str, Any]:
    """Retrieve jurisdiction-specific e-waste statutory details."""
    return GLOBAL_REGULATIONS.get(country, GLOBAL_REGULATIONS['International'])
