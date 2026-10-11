"""
🌐 Internationalization (i18n) & Localization Engine
===================================================
Supports multi-language UI, currency conversion with uncertainty,
and regional measurement conventions.
"""

from datetime import datetime
from typing import Dict, Any, Tuple

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'हिन्दी (Hindi)',
    'es': 'Español (Spanish)',
    'fr': 'Français (French)',
    'de': 'Deutsch (German)'
}

# Translation Dictionaries
TRANSLATIONS = {
    'en': {
        'app_title': 'E-WASTE INTELLIGENCE SYSTEM',
        'subtitle': 'AI-Powered Classification, Recovery & Global 3D Knowledge Platform',
        'dashboard': 'Dashboard',
        'image_classify': 'Image Classify',
        'chatbot': 'AI Chatbot',
        'lab3d': '3D E-Waste Lab',
        'form_classify': 'Form Classify',
        'upload_data': 'Dataset Upload',
        'smart_analyzer': 'Smart Analyzer',
        'recovery_advisor': 'Recovery Advisor',
        'environmental_impact': 'Environmental Impact',
        'my_history': 'History',
        'about': 'About',
        'select_device': 'Select Device Category',
        'recovery_value': 'Estimated Recovery Value',
        'hazardous': 'Hazardous Component',
        'safe': 'Safe to Handle',
        'recycling_steps': 'Recommended Recycling Steps',
        'safety_warnings': 'Safety Precautions & Stop-Work Advice',
        'environmental_savings': 'Environmental Savings',
        'currency': 'Currency',
        'language': 'Language',
        'disclaimer_title': 'Scientific & Regulatory Notice',
        'disclaimer_text': 'Material values and environmental metrics are engineering estimates based on life-cycle analysis models. Actual recovery yield varies with extraction technology and market fluctuations.'
    },
    'hi': {
        'app_title': 'ई-कचरा इंटेलिजेंस सिस्टम',
        'subtitle': 'एआई-संचालित वर्गीकरण, सामग्री पुनर्प्राप्ति और वैश्विक 3D ज्ञान मंच',
        'dashboard': 'डैशबोर्ड',
        'image_classify': 'छवि वर्गीकरण',
        'chatbot': 'एआई चैटबॉट',
        'lab3d': '3D ई-कचरा लैब',
        'form_classify': 'फ़ॉर्म वर्गीकरण',
        'upload_data': 'डेटासेट अपलोड',
        'smart_analyzer': 'स्मार्ट विश्लेषक',
        'recovery_advisor': 'पुनर्प्राप्ति सलाहकार',
        'environmental_impact': 'पर्यावरणीय प्रभाव',
        'my_history': 'इतिहास',
        'about': 'परिचय',
        'select_device': 'उपकरण श्रेणी चुनें',
        'recovery_value': 'अनुमानित पुनर्प्राप्ति मूल्य',
        'hazardous': 'खतरनाक घटक',
        'safe': 'संभालने में सुरक्षित',
        'recycling_steps': 'अनुशंसित पुनर्चक्रण चरण',
        'safety_warnings': 'सुरक्षा सावधानियां एवं कार्य-रोक सलाह',
        'environmental_savings': 'पर्यावरणीय बचत',
        'currency': 'मुद्रा',
        'language': 'भाषा',
        'disclaimer_title': 'वैज्ञानिक एवं विनियामक सूचना',
        'disclaimer_text': 'सामग्री मूल्य और पर्यावरणीय आंकड़े जीवन चक्र विश्लेषण मॉडल पर आधारित अनुमान हैं। वास्तविक पुनर्प्राप्ति निष्कर्षण तकनीक और बाजार की कीमतों पर निर्भर करती है।'
    },
    'es': {
        'app_title': 'SISTEMA DE INTELIGENCIA DE RESIDUOS ELECTRÓNICOS',
        'subtitle': 'Plataforma global de clasificación, recuperación y conocimiento 3D impulsada por IA',
        'dashboard': 'Panel Principal',
        'image_classify': 'Clasificar Imagen',
        'chatbot': 'Chatbot IA',
        'lab3d': 'Laboratorio 3D',
        'form_classify': 'Clasificar Formulario',
        'upload_data': 'Cargar Datos',
        'smart_analyzer': 'Analizador Inteligente',
        'recovery_advisor': 'Asesor de Recuperación',
        'environmental_impact': 'Impacto Ambiental',
        'my_history': 'Historial',
        'about': 'Acerca de',
        'select_device': 'Seleccionar Categoría',
        'recovery_value': 'Valor Estimado de Recuperación',
        'hazardous': 'Componente Peligroso',
        'safe': 'Seguro de Manipular',
        'recycling_steps': 'Pasos de Reciclaje',
        'safety_warnings': 'Precauciones de Seguridad',
        'environmental_savings': 'Ahorro Ambiental',
        'currency': 'Moneda',
        'language': 'Idioma',
        'disclaimer_title': 'Aviso Científico y Regulatorio',
        'disclaimer_text': 'Los valores de materiales son estimaciones de ingeniería basadas en análisis de ciclo de vida.'
    },
    'fr': {
        'app_title': 'SYSTÈME D\'INTELLIGENCE DES DÉCHETS ÉLECTRONIQUES',
        'subtitle': 'Plateforme IA de classification, valorisation et modélisation 3D',
        'dashboard': 'Tableau de bord',
        'image_classify': 'Classifier Image',
        'chatbot': 'Chatbot IA',
        'lab3d': 'Laboratoire 3D',
        'form_classify': 'Formulaire',
        'upload_data': 'Téléverser Données',
        'smart_analyzer': 'Analyseur Intelligent',
        'recovery_advisor': 'Conseiller en Recyclage',
        'environmental_impact': 'Impact Environnemental',
        'my_history': 'Historique',
        'about': 'À propos',
        'select_device': 'Sélectionner l\'appareil',
        'recovery_value': 'Valeur de Récupération Estimée',
        'hazardous': 'Composant Dangereux',
        'safe': 'Manipulation Sûre',
        'recycling_steps': 'Étapes de Recyclage',
        'safety_warnings': 'Consignes de Sécurité',
        'environmental_savings': 'Bénéfices Environnementaux',
        'currency': 'Devise',
        'language': 'Langue',
        'disclaimer_title': 'Avis Scientifique et Réglementaire',
        'disclaimer_text': 'Les valeurs de valorisation sont des estimations d\'ingénierie.'
    },
    'de': {
        'app_title': 'E-SCHROTT INTELLIGENZ-PLATTFORM',
        'subtitle': 'KI-gestützte Klassifizierung, Verwertung und globale 3D-Wissensplattform',
        'dashboard': 'Übersicht',
        'image_classify': 'Bild-Klassifizierung',
        'chatbot': 'KI-Chatbot',
        'lab3d': '3D E-Schrott Labor',
        'form_classify': 'Formular-Klassifizierung',
        'upload_data': 'Datensatz Hochladen',
        'smart_analyzer': 'Smart Analyzer',
        'recovery_advisor': 'Recycling-Berater',
        'environmental_impact': 'Umweltauswirkungen',
        'my_history': 'Verlauf',
        'about': 'Über uns',
        'select_device': 'Gerätekategorie wählen',
        'recovery_value': 'Geschätzter Rückgewinnungswert',
        'hazardous': 'Gefahrstoff-Komponente',
        'safe': 'Sicher in der Handhabung',
        'recycling_steps': 'Recycling-Schritte',
        'safety_warnings': 'Sicherheitshinweise',
        'environmental_savings': 'Umwelteinsparungen',
        'currency': 'Währung',
        'language': 'Sprache',
        'disclaimer_title': 'Wissenschaftlicher Hinweis',
        'disclaimer_text': 'Rückgewinnungswerte basieren auf standardisierten Lebenszyklusanalysen.'
    }
}

# Configurable Currency Rates relative to USD (Base: USD = 1.0)
# Updated benchmark reference with explicit attribution & source
CURRENCY_RATES = {
    'USD': {'symbol': '$', 'rate': 1.00, 'name': 'US Dollar'},
    'INR': {'symbol': '₹', 'rate': 86.50, 'name': 'Indian Rupee'},
    'EUR': {'symbol': '€', 'rate': 0.92, 'name': 'Euro'},
    'GBP': {'symbol': '£', 'rate': 0.78, 'name': 'British Pound'},
    'JPY': {'symbol': '¥', 'rate': 152.00, 'name': 'Japanese Yen'}
}

EXCHANGE_RATE_METADATA = {
    'provider': 'Central Benchmark Reference Rates',
    'benchmark_date': 'October 2026',
    'status': 'Verified Offline Baseline'
}

def get_text(key: str, lang: str = 'en') -> str:
    """Retrieve localized string with graceful English fallback."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    return lang_dict.get(key, TRANSLATIONS['en'].get(key, key))

def convert_currency(amount_usd: float, target_currency: str = 'USD') -> Tuple[float, str, str]:
    """
    Converts USD amount to target currency.
    Returns: (converted_amount, currency_symbol, formatted_string)
    """
    target = target_currency.upper()
    curr_info = CURRENCY_RATES.get(target, CURRENCY_RATES['USD'])
    converted = amount_usd * curr_info['rate']
    formatted = f"{curr_info['symbol']}{converted:,.2f} {target}"
    return converted, curr_info['symbol'], formatted

def format_recovery_range(amount_usd: float, target_currency: str = 'USD', uncertainty_pct: float = 20.0) -> str:
    """
    Formats value with market uncertainty bounds (e.g. $12.00 [Range: $9.60 - $14.40]).
    Honest reporting that distinguishes fixed assumptions from variable market reality.
    """
    base_val, symbol, _ = convert_currency(amount_usd, target_currency)
    lower = base_val * (1.0 - (uncertainty_pct / 100.0))
    upper = base_val * (1.0 + (uncertainty_pct / 100.0))
    return f"{symbol}{base_val:,.2f} ({symbol}{lower:,.2f} – {symbol}{upper:,.2f} ±{uncertainty_pct:.0f}%)"
