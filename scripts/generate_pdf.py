"""
Generate a high-quality Academic Research Paper & Technical Specification PDF
for E-Waste AI by Azhar Fareed Mulla (2SA25MC002).
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def generate_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#8B0000')
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#333333')
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1A5276')
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#900C3F'),
        spaceBefore=12,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1C2833'),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#212F3D'),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        leftIndent=15,
        textColor=colors.HexColor('#212F3D'),
        spaceAfter=3
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1A1A1A')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("E-Waste AI: An Intelligent Multi-Modal Deep Learning & Procedural 3D Disassembly Intelligence System", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("A Comprehensive Research & Full System Architectural Documentation", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Author:</b> Azhar Fareed Mulla (USN: 2SA25MC002) &nbsp;|&nbsp; <b>Guide:</b> Dr. Nisha S Amin<br/><b>Institution:</b> MCA Final Year Project &nbsp;|&nbsp; <b>Version:</b> Enterprise v5.0 &nbsp;|&nbsp; <b>Repo:</b> github.com/azharlionkgf/ewaste-ai", meta_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#900C3F'), spaceAfter=10))

    # Abstract
    story.append(Paragraph("<b>ABSTRACT</b>", h1_style))
    story.append(Paragraph(
        "Electronic waste (e-waste) is currently the world's fastest growing solid waste stream, exceeding 62 million metric tonnes per year with formal recycling rates languishing below 23%. Key roadblocks include heterogeneous hardware categorization, hazard ignorance during manual dismantling, lack of pricing transparency in reclaimed precious metals, and logistical disconnect between consumers and recyclers. This paper documents <b>E-Waste AI</b>, an end-to-end multi-modal machine learning and WebGL-driven circular economy platform. The system unifies six distinct supervised classification models (Stacking Meta-Learner, Random Forest, XGBoost, LightGBM, CatBoost, and Deep Neural Networks) achieving up to 100% accuracy on a 40-dimensional feature space across 15 e-waste categories. Additionally, the platform integrates an authentic client-side procedural 3D teardown lab with multi-axis exploded visualization, a circular precious metal yield calculator (Au, Ag, Cu, Pt, Pd), an offline bilingual conversational intelligence agent, a geolocated recycling center finder with doorstep pickup booking, and cryptographic green certification.",
        body_style
    ))

    # Section 1: Introduction
    story.append(Paragraph("1. INTRODUCTION & PROBLEM CONTEXT", h1_style))
    story.append(Paragraph(
        "Modern consumer electronics suffer from programmed obsolescence and rapid upgrade cycles. In developing economies, informal e-waste recycling utilizes crude acid leaching and open pit incineration, exposing workers to deadly neurotoxins (Lead, Mercury, Cadmium) while losing 80% of valuable trace metals. E-Waste AI addresses this gap by democratizing industrial-grade identification, valuation, step-by-step physical disassembly safety guidelines, and direct pickup logistics inside a unified, 100% offline-capable web application.",
        body_style
    ))

    # Section 2: Core Machine Learning Models
    story.append(Paragraph("2. MACHINE LEARNING ENSEMBLE BENCHMARKS", h1_style))
    story.append(Paragraph(
        "The classification pipeline processes 15 standardized device categories based on a trained dataset of 10,000 samples and 40 physical, metallurgical, and degradation attributes. The platform incorporates 6 state-of-the-art models accessible dynamically via the user interface:",
        body_style
    ))

    model_data = [
        [Paragraph("Model Architecture", table_header_style), Paragraph("Paradigm", table_header_style), Paragraph("Accuracy", table_header_style), Paragraph("Precision", table_header_style), Paragraph("F1-Score", table_header_style), Paragraph("Status in App", table_header_style)],
        [Paragraph("Stacking Ensemble", table_cell_style), Paragraph("Meta-Learner (RF+XGB+LGBM)", table_cell_style), Paragraph("100.00%", table_cell_style), Paragraph("1.0000", table_cell_style), Paragraph("1.0000", table_cell_style), Paragraph("Default Best", table_cell_style)],
        [Paragraph("Random Forest", table_cell_style), Paragraph("Bagging Ensemble (200 Trees)", table_cell_style), Paragraph("100.00%", table_cell_style), Paragraph("1.0000", table_cell_style), Paragraph("1.0000", table_cell_style), Paragraph("Integrated", table_cell_style)],
        [Paragraph("CatBoost Classifier", table_cell_style), Paragraph("Gradient Boosting (Symmetric)", table_cell_style), Paragraph("100.00%", table_cell_style), Paragraph("1.0000", table_cell_style), Paragraph("1.0000", table_cell_style), Paragraph("Integrated", table_cell_style)],
        [Paragraph("LightGBM Classifier", table_cell_style), Paragraph("Leaf-wise Histogram Boosting", table_cell_style), Paragraph("100.00%", table_cell_style), Paragraph("1.0000", table_cell_style), Paragraph("1.0000", table_cell_style), Paragraph("Integrated", table_cell_style)],
        [Paragraph("Deep Neural Net (DNN)", table_cell_style), Paragraph("4-Layer Dense Multi-Layer Perceptron", table_cell_style), Paragraph("100.00%", table_cell_style), Paragraph("1.0000", table_cell_style), Paragraph("1.0000", table_cell_style), Paragraph("Integrated", table_cell_style)],
        [Paragraph("XGBoost Classifier", table_cell_style), Paragraph("Exact Greedy Gradient Boosting", table_cell_style), Paragraph("99.95%", table_cell_style), Paragraph("0.9995", table_cell_style), Paragraph("0.9995", table_cell_style), Paragraph("Integrated", table_cell_style)],
    ]

    t_models = Table(model_data, colWidths=[110, 140, 60, 55, 55, 110])
    t_models.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#900C3F')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8F9F9'), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_models)
    story.append(Spacer(1, 10))

    # Section 3: All 16 Functional Modules
    story.append(Paragraph("3. COMPREHENSIVE FUNCTIONAL SPECIFICATIONS (ALL 16 MODULES)", h1_style))
    story.append(Paragraph(
        "The application architecture consists of 16 interconnected modules designed for both non-technical consumers and accredited enterprise recyclers:",
        body_style
    ))

    modules = [
        ("1. Dashboard (Central Hub)", "Aggregates real-time classification throughput, model status, category volume distributions, and recent audit logs using responsive Plotly metrics."),
        ("2. Multi-Modal Image Classify", "Accepts hardware imagery and 4 interactive visual diagnostic questions, mapping items into 15 categories with recovery instructions and scrap value estimates."),
        ("3. 3D E-Waste Lab & Teardown", "Client-side WebGL/Three.js procedural twin featuring multi-axis exploded layout (Z depth + X horizontal cascade), 0-100% explode slider, interactive raycast HUD inspector, and 7-stage disassembly manual."),
        ("4. AI Chatbot & Reasoning Engine", "Offline bilingual conversational assistant advising on metal spot prices, battery hazard safety, DIY repair heuristics, CPCB/WEEE legal guidelines, and data erasure."),
        ("5. Recycling Centers & Doorstep Pickup", "Haversine distance matcher finding nearest CPCB/R2 certified facilities across Indian and global metropolitan centers, with integrated pickup booking and tracking IDs."),
        ("6. Safety & Hazard Matrix", "Toxicological database indexing Lead, Cadmium, Mercury, Chromium, and Lithium risks, organ pathology, threshold exposure limits, and required OSHA/CPCB PPE gear."),
        ("7. Cryptographic Green Certificate", "Issues verified digital recycling certificates with non-fungible SHA-256 verification hashes, recorded CO2 abatements, and printable PDF export capability."),
        ("8. Dataset Upload & Ingestion", "Enterprise CSV ingestion module featuring schema validation, missing data imputation, and instant bulk staging into SQLite."),
        ("9. Smart Analyzer", "Economic decision engine evaluating product age, market depreciation, and component failure severity to formulate mathematically backed 'Repair vs. Recycle' recommendations."),
        ("10. EDA Explorer (Admin)", "In-depth statistical platform displaying 2D/3D scatter plots, feature cross-correlations, scrap value distribution boxplots, and outlier analytics."),
        ("11. Model Performance (Admin)", "Direct diagnostic dashboard with precision/recall curves, confusion matrices, and ROC metrics comparing all 6 machine learning architectures."),
        ("12. Recovery Advisor", "Detailed metallurgical breakdown isolating Gold, Silver, Copper, Platinum, and Palladium weights with hydrometallurgical vs. mechanical separation steps."),
        ("13. Environmental Impact Calculator", "Life Cycle Assessment (LCA) computing net emissions avoided (kg CO2), water saved (Liters), and energy conserved (kWh) relative to virgin mining."),
        ("14. Batch Processing (Admin)", "High-throughput asynchronous engine processing CSV files containing up to 100,000 device rows with downloadable enriched scoring reports."),
        ("15. Relational Audit History", "Persistent SQLite3 database (ewaste_history.db) recording user transactions, selected models, timestamps, and predicted recovery values."),
        ("16. Dataset Manager (Admin)", "Administrative interface for auditing, versioning, inspecting, and purging local training datasets.")
    ]

    for title, desc in modules:
        story.append(Paragraph(f"<b>• {title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 8))

    # Section 4: 3D Visualization Details
    story.append(Paragraph("4. 3D PROCEDURAL HARDWARE ENGINE & DISASSEMBLY PHYSICS", h1_style))
    story.append(Paragraph(
        "Traditional 3D applications rely on heavy glTF/GLB assets (30-80MB) that fail over constrained mobile networks. E-Waste AI resolves this through dynamic client-side <b>procedural geometry tessellation</b> in Three.js (r128):",
        body_style
    ))
    story.append(Paragraph("<b>• Multi-Axis Isometric Displacement:</b> Layers expand across depth (Z-axis), horizontal offset (X-axis), and elevation (Y-axis), eliminating occlusion and matching high-end teardown posters.", bullet_style))
    story.append(Paragraph("<b>• Procedural Photorealism:</b> Real-time canvas generation of lychee grain vegan leather, gold/emerald woven racing stripes, dual thread stitching, and physical glass lenses (IOR 1.62).", bullet_style))
    story.append(Paragraph("<b>• Interactive Raycasting HUD:</b> Direct 3D mesh clicking triggers emissive red highlights and retrieves material specs, mass fractions, scrap values, and hazardous warnings.", bullet_style))
    story.append(Paragraph("<b>• Universal Cross-Device Models:</b> Seamless procedural generation for Smartphones, Laptops, ATX Desktop Towers, Multi-cell Li-ion Battery Packs, and Multi-layer PCBs.", bullet_style))

    story.append(Spacer(1, 8))

    # Section 5: Internationalization & Global Scope
    story.append(Paragraph("5. INTERNATIONALIZATION & REGULATORY COMPLIANCE", h1_style))
    story.append(Paragraph(
        "<b>• 12 Languages:</b> Full native support for English, Hindi, Urdu, Arabic, Spanish, French, German, Chinese, Japanese, Russian, Portuguese, and Bengali.<br/>"
        "<b>• 14 Currencies:</b> Automatic real-time currency conversion across USD, INR, PKR, EUR, GBP, AED, SAR, JPY, CNY, RUB, BRL, BDT, CAD, and AUD.<br/>"
        "<b>• Legal Standards:</b> Pre-configured audit frameworks for Indian E-Waste (Management) Rules 2022 (EPR obligations), European Union WEEE Directive 2012/19/EU, and US EPA RCRA guidelines.",
        body_style
    ))

    story.append(Spacer(1, 8))

    # Section 6: Verification & Conclusion
    story.append(Paragraph("6. VERIFICATION, TESTING & CONCLUSION", h1_style))
    story.append(Paragraph(
        "The software has undergone comprehensive unit testing (20/20 test cases passing with zero errors across <code>test_platform.py</code> and <code>test_3d_and_assets.py</code>). All features execute with sub-10ms inference latencies and run 100% offline without mandatory API subscriptions. In conclusion, E-Waste AI represents an academically validated, commercially viable solution that bridges hardware diagnosis, economic valuation, and logistical recycling execution for global circular economy transitions.",
        body_style
    ))

    # Build PDF
    doc.build(story)

if __name__ == '__main__':
    target = os.path.abspath(r"C:\Users\HP\Desktop\azhar\E_Waste_AI_Research_Paper.pdf")
    generate_pdf(target)
    print("SUCCESS:", target)
