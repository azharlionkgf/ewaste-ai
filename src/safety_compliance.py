"""
⚠️ Safety Protocols & Global Regulatory Compliance Engine
=========================================================
Jurisdiction-specific regulatory databases across all major continents and countries:
(India, USA, European Union, UK, UAE, Saudi Arabia, Pakistan, China, Japan, Brazil, Canada, Australia, Basel International)
and critical stop-work protocols for hazardous components.
"""

from typing import Dict, List, Any

# Critical Stop-Work Hazards requiring qualified intervention
HAZARD_PROTOCOLS = {
    'battery_thermal_runaway': {
        'hazard': 'Swollen / Damaged Lithium-Ion Battery (Li-Po / Li-Ion)',
        'severity': 'CRITICAL (Fire, Explosion & Toxic Hydrogen Fluoride Gas)',
        'action': 'STOP WORK IMMEDIATELY',
        'instructions': [
            'Do NOT puncture, crush, bend, or force open the casing.',
            'Immediately isolate the unit inside an airtight, non-combustible metal container filled with dry sand, vermiculite, or Class D fire suppression powder.',
            'Keep away from flammable structures, liquids, and oxygen sources.',
            'Never dispose of in household municipal waste, landfills, or trash compactors.',
            'Contact a certified hazardous waste handler or manufacturer authorized take-back center.'
        ]
    },
    'crt_implosion': {
        'hazard': 'Cathode Ray Tube (CRT) High-Vacuum & Lead Glass',
        'severity': 'HIGH (Implosion & Toxic Lead Poisoning)',
        'action': 'SPECIALIZED DISMANTLING REQUIRED',
        'instructions': [
            'Do NOT break the funnel or glass faceplate.',
            'CRTs maintain a deep internal vacuum and contain 1.5 to 3.5 kg of toxic lead in the funnel glass.',
            'Wear full face protection and Kevlar cut-resistant gloves.',
            'Discharge anode residual high-voltage (up to 25kV-30kV) using an insulated grounding tool before opening.'
        ]
    },
    'refrigerant_leak': {
        'hazard': 'Pressurized Refrigerants (CFC, HCFC, HFC, Isobutane R600a)',
        'severity': 'HIGH (Ozone Depletion, Flammability, Asphyxiation)',
        'action': 'CERTIFIED HVAC RECOVERY ONLY',
        'instructions': [
            'Illegal venting violates international environmental laws (Clean Air Act, Montreal Protocol, Kigali Amendment).',
            'Isobutane (R600a) is highly explosive; work in spark-free explosion-proof environments.',
            'Refrigerant gas must be extracted using a sealed closed-loop recovery machine before compressor removal.'
        ]
    },
    'high_voltage_capacitors': {
        'hazard': 'Charged Power Supply Capacitors (SMPS / Inverters / Microwave Magnetrons)',
        'severity': 'LETHAL (Electric Shock Hazard)',
        'action': 'DISCHARGE BEFORE TOUCHING',
        'instructions': [
            'Power supply capacitors and microwave transformers store lethal DC voltages (300V - 2500V) long after unplugging.',
            'Wait minimum 30 minutes after disconnection, then discharge across a 10k ohm 10W power resistor.',
            'Never bridge high-voltage terminals directly with a bare metal tool or screwdriver.'
        ]
    },
    'mercury_backlights': {
        'hazard': 'Cold Cathode Fluorescent Lamps (CCFL) Mercury Vapor',
        'severity': 'CRITICAL (Neurotoxic Vapor Inhalation)',
        'action': 'GENTLE EXTRACTION UNDER FUME HOOD',
        'instructions': [
            'Found in older LCD screens, monitors, and scanners.',
            'Do NOT crack the micro-glass CCFL tubes.',
            'If broken, evacuate room for 15 minutes, ventilate immediately, and use specialized mercury spill amalgam kit.'
        ]
    }
}

# Global Regulatory Frameworks across Worldwide Jurisdictions
GLOBAL_REGULATIONS = {
    'India': {
        'jurisdiction': 'Republic of India 🇮🇳',
        'agency': 'Central Pollution Control Board (CPCB) / MoEFCC',
        'statute': 'E-Waste (Management) Rules, 2022 (Effective April 1, 2023)',
        'effective_date': 'April 1, 2023',
        'key_requirements': [
            'Extended Producer Responsibility (EPR) mandatory for manufacturers and importers.',
            'Producers must achieve graduated recycling targets through registered recyclers on the CPCB portal.',
            'Informal burning (acid leaching/open smelting) is strictly prohibited under Environment Protection Act, 1986.',
            'Penalties include environmental compensation fines and prosecution under statutory clauses.'
        ],
        'compliance_tier': 'Mandatory National CPCB Registration'
    },
    'United States': {
        'jurisdiction': 'United States of America 🇺🇸',
        'agency': 'US Environmental Protection Agency (EPA) & State Regulators',
        'statute': 'Resource Conservation and Recovery Act (RCRA) & State E-Waste Mandates (e.g. California SB 20/50)',
        'effective_date': 'Varies by State (28 States have E-Waste Acts)',
        'key_requirements': [
            'Cathode Ray Tubes (CRTs) and certain toxic components are classified as hazardous waste under 40 CFR 261.',
            'Commercial generators cannot dispose of CRTs or mercury-containing lamps in municipal landfills.',
            'Producer responsibility programs mandate certified recycling financing.',
            'Accredited certifications: R2v3 (Sustainable Electronics Recycling) and e-Stewards standard.'
        ],
        'compliance_tier': 'Hybrid Federal RCRA / State EPR Matrix'
    },
    'European Union (Germany/France/Spain)': {
        'jurisdiction': 'European Union (EU-27) 🇪🇺',
        'agency': 'European Commission & National Environmental Ministries (Umweltbundesamt, ADEME)',
        'statute': 'WEEE Directive (2012/19/EU) & RoHS Directive (2011/65/EU) Recast',
        'effective_date': 'Current Active Directive',
        'key_requirements': [
            'RoHS restricts Lead (Pb), Mercury (Hg), Cadmium (Cd), Hexavalent Chromium (Cr6+), PBBs, and PBDEs (<0.1% / <0.01% Cd).',
            'Minimum collection target of 65% of average weight of EEE placed on the market.',
            'Producers must finance separate collection, treatment, and environmentally sound disposal.',
            'Right to Repair (R2R) directive mandates spare parts availability for 7-10 years.'
        ],
        'compliance_tier': 'Comprehensive Statutory Standard (CE / WEEE / RoHS)'
    },
    'United Kingdom': {
        'jurisdiction': 'United Kingdom 🇬🇧',
        'agency': 'Environment Agency (EA) / DEFRA',
        'statute': 'The Waste Electrical and Electronic Equipment Regulations 2013',
        'effective_date': 'Current UK Statutory Framework',
        'key_requirements': [
            'UK WEEE regulations require producers to join an approved Producer Compliance Scheme (PCS).',
            'Approved Authorised Treatment Facilities (AATFs) must handle depollution and precious metal recovery.',
            'Strict ban on disposing of hazardous electronic components in domestic black bag waste.'
        ],
        'compliance_tier': 'UK DEFRA Producer Compliance Scheme'
    },
    'United Arab Emirates (UAE)': {
        'jurisdiction': 'United Arab Emirates 🇦🇪',
        'agency': 'Ministry of Climate Change and Environment (MOCCAE) & Tadweer',
        'statute': 'Federal Law No. 12 of 2018 on Integrated Waste Management',
        'effective_date': 'Current Active Law',
        'key_requirements': [
            'Mandates circular economy initiatives and diversion of electronic waste from landfills.',
            'Prohibits illegal incineration and unauthorized dismantling of hazardous IT equipment.',
            'Certification required through local municipalities (Dubai Municipality, Tadweer Abu Dhabi).'
        ],
        'compliance_tier': 'UAE Federal Green Circular Standard'
    },
    'Saudi Arabia': {
        'jurisdiction': 'Kingdom of Saudi Arabia 🇸🇦',
        'agency': 'National Center for Waste Management (MWAN)',
        'statute': 'Saudi National Waste Management Framework (Vision 2030 Circular Economy)',
        'effective_date': 'Current Framework',
        'key_requirements': [
            'MWAN licensing mandatory for all e-waste collection, transport, and recycling facilities.',
            'Zero landfill policy targeted for hazardous electronic streams by 2035.',
            'Full documentation and tracking for industrial electronic asset decommission.'
        ],
        'compliance_tier': 'MWAN Certified Circular Standard'
    },
    'Pakistan': {
        'jurisdiction': 'Islamic Republic of Pakistan 🇵🇰',
        'agency': 'Pakistan Environmental Protection Agency (Pak-EPA)',
        'statute': 'Pakistan Environmental Protection Act 1997 & Hazardous Waste Regulations',
        'effective_date': 'Current EPA Framework',
        'key_requirements': [
            'Regulation of electronic waste recycling and scrap importation.',
            'Prohibition of open air burning of cables and acid-bath metal recovery.',
            'Encouragement of formalized municipal drop-off centers.'
        ],
        'compliance_tier': 'Pak-EPA Environmental Protection Framework'
    },
    'Bangladesh': {
        'jurisdiction': 'People\'s Republic of Bangladesh 🇧🇩',
        'agency': 'Department of Environment (DoE), Ministry of Environment, Forest and Climate Change',
        'statute': 'Hazardous Waste and E-Waste Management Rules, 2021',
        'effective_date': 'June 2021',
        'key_requirements': [
            'Extended Producer Responsibility (EPR) mandates collection targets for electronics manufacturers.',
            'Prohibits import of toxic second-hand electronic scrap without clearance.',
            'Mandatory licensing for recycling units with effluent treatment plants (ETP).'
        ],
        'compliance_tier': 'DoE Hazardous & E-Waste Statutory Rules 2021'
    },
    'China': {
        'jurisdiction': 'People\'s Republic of China 🇨🇳',
        'agency': 'Ministry of Ecology and Environment (MEE) & MIIT',
        'statute': 'Regulation on the Management of the Recycling and Disposal of Waste Electrical and Electronic Equipment (China WEEE)',
        'effective_date': 'Current Framework',
        'key_requirements': [
            'China RoHS restricts hazardous chemicals in electrical and electronic products.',
            'Government-managed E-Waste Disposal Fund providing subsidies to certified recycling plants.',
            'Ban on illegal dismantling and stringent effluent discharge standards.'
        ],
        'compliance_tier': 'China RoHS & MIIT Certified Facility Standard'
    },
    'Japan': {
        'jurisdiction': 'Japan 🇯🇵',
        'agency': 'Ministry of the Environment (MOE) & METI',
        'statute': 'Home Appliance Recycling Act & Small Appliance Recycling Act (Kogata Kaden)',
        'effective_date': 'Current Active Acts',
        'key_requirements': [
            'Consumers, retailers, and manufacturers share responsibilities for appliance recycling.',
            'Retailers are legally required to take back old appliances when selling replacements.',
            'Extremely high statutory metal recovery rates (>80% metals, plastics recycled).'
        ],
        'compliance_tier': 'Strict Japanese METI / MOE Statutory Standard'
    },
    'Brazil': {
        'jurisdiction': 'Federative Republic of Brazil 🇧🇷',
        'agency': 'Ministry of the Environment and Climate Change (MMA) / IBAMA',
        'statute': 'National Solid Waste Policy (PNRS - Law 12.305/2010 & Decree 10.240/2020)',
        'effective_date': 'Current Sectoral Agreement',
        'key_requirements': [
            'Reverse Logistics System (Logística Reversa) for electronics and household appliances.',
            'Producers, distributors, and retailers must establish consumer drop-off points (PEVs).',
            'Certified recycling mandatory to extract secondary raw materials safely.'
        ],
        'compliance_tier': 'PNRS Reverse Logistics Legal Framework'
    },
    'Canada': {
        'jurisdiction': 'Canada 🇨🇦',
        'agency': 'Environment and Climate Change Canada (ECCC) & Provincial Stewardship Bodies',
        'statute': 'Canadian Environmental Protection Act (CEPA) & Provincial EPR Regulations (e.g. EPRA)',
        'effective_date': 'Provincial Mandatory Programs',
        'key_requirements': [
            'Electronic Products Recycling Association (EPRA) manages end-of-life electronics across provinces.',
            'Environmental Handling Fees (EHF) fund provincial collection and processing networks.',
            'Zero hazardous e-waste exported to non-OECD countries.'
        ],
        'compliance_tier': 'Canadian EPRA / Recycler Qualification Standard (RQS)'
    },
    'Australia': {
        'jurisdiction': 'Commonwealth of Australia 🇦🇺',
        'agency': 'Department of Climate Change, Energy, the Environment and Water (DCCEEW)',
        'statute': 'National Television and Computer Recycling Scheme (NTCRS)',
        'effective_date': 'Product Stewardship Act 2011',
        'key_requirements': [
            'Importers and manufacturers of TVs and computers fund recycling through co-regulatory arrangements.',
            'Industry must achieve material recovery rates of at least 90%.',
            'Free drop-off services for households and small businesses nationwide.'
        ],
        'compliance_tier': 'NTCRS Co-Regulatory Standard'
    },
    'International': {
        'jurisdiction': 'Global Transboundary 🌐',
        'agency': 'United Nations Environment Programme (UNEP)',
        'statute': 'Basel Convention on the Control of Transboundary Movements of Hazardous Wastes (E-Waste Amendments)',
        'effective_date': 'E-Waste Amendments (Effective Jan 1, 2025)',
        'key_requirements': [
            'All transboundary movements of e-waste require Prior Informed Consent (PIC) before shipment.',
            'Prevents illegal dumping of toxic electronic scrap into developing nations.',
            'Exporters must prove recipient facility maintains verified environmentally sound management (ESM).'
        ],
        'compliance_tier': 'UNEP Basel Convention International Treaty'
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
    if country in GLOBAL_REGULATIONS:
        return GLOBAL_REGULATIONS[country]
    # Check for prefix or substring match (e.g. 'European Union' in 'European Union (Germany/France/Spain)')
    for k, v in GLOBAL_REGULATIONS.items():
        if country.lower() in k.lower() or k.lower() in country.lower():
            return v
    return GLOBAL_REGULATIONS.get('International', {})
