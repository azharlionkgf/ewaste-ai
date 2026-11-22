# E-WASTE AI — Industrial Workflow Architecture

## Overview

The E-WASTE AI industrial workflow maps the complete lifecycle of incoming electronic waste from reception through material recovery and final reporting. This workflow is designed for real electronic waste recycling facilities and integrates AI-powered classification at key decision points.

The workflow operates across **13 sequential phases**, each producing structured records that feed downstream phases and populate the research database for analysis.

---

## Phase 1: Incoming E-Waste Registration

**Purpose:** Record all incoming e-waste at the point of arrival.

**Activities:**
- Supplier/donor identification and verification
- Gross weight measurement of the shipment
- Initial visual inspection for visible hazards (leaking batteries, broken CRTs)
- Generation of a unique **Batch Reference Code** (e.g., `BATCH-20240115-0001`)
- Assignment to a receiving operator

**Data Captured:**
- Source (company, individual, municipality)
- Arrival date and time
- Gross weight (kg)
- Estimated item count
- Collection point / geographic origin
- Receiving operator ID

**Output:** Registered batch in `waste_batches` table with status `registered`.

---

## Phase 2: Initial Assessment and Batch Creation

**Purpose:** Conduct a quick manual triage to prioritise processing.

**Activities:**
- Open batch and conduct item-level inventory
- Assign each item a unique **Item ID**
- Record device type (approximate), brand, model if visible
- Weigh individual items or groups
- Flag visibly damaged, leaking or high-hazmat items for segregation

**Data Captured:**
- Per-item: device_type, brand, model, weight_kg, condition, serial number
- Hazmat flags (leaking battery, broken CRT glass, etc.)

**Output:** `batch_items` records created; batch status updated to `assessed`.

---

## Phase 3: AI-Powered Classification

**Purpose:** Use trained AI models to classify each item accurately.

**Activities:**
- Capture image of each item (optional, if camera station available)
- Run image through CNN classifier (MobileNetV3 / EfficientNet) if model is trained
- Run tabular features through tabular classifier (RF / XGBoost) as alternative
- Record top-k predictions with confidence scores
- Items with confidence < 0.5 → flagged for expert review

**AI Decision Rules:**
| Confidence | Action |
|------------|--------|
| ≥ 0.80 | Auto-process — proceed to sorting |
| 0.50–0.79 | Manual review by trained operator |
| < 0.50 | Expert assessment required |

**Data Captured:**
- Predicted device category, confidence score, top-5 predictions
- Classification method (AI_CNN, AI_tabular, manual)

**Output:** `item_classifications` records; batch status → `classified`.

---

## Phase 4: Sorting and Categorisation

**Purpose:** Physically sort items into processing streams based on classification.

**Activities:**
- Route items to designated processing areas by device category
- Segregate high-hazmat items (CRT, mercury lamps, NiCd batteries)
- Group by material recovery priority (high precious metal content first)
- Apply WEEE category labels

**Sorting Streams:**
1. High-value PCBs and circuit boards (precious metal recovery)
2. Li-ion batteries (lithium/cobalt recovery)
3. Lead-acid batteries (lead recovery)
4. Ferrous metals (steel/iron bulk)
5. CRT/mercury hazmat (specialised disposal)
6. Plastic/glass (shredding/separation)

**Output:** Items assigned to processing streams; batch status → `sorted`.

---

## Phase 5: Dismantling and Component Extraction

**Purpose:** Manual or mechanical disassembly to separate components.

**Activities:**
- Remove batteries before any shredding
- Extract PCBs and circuit boards
- Remove displays, screens
- Separate cables, connectors
- Remove hazardous components (mercury lamps, capacitors)
- Record dismantling operator and time

**Compliance Requirements:**
- Batteries must be discharged before removal
- Mercury-containing components require sealed handling
- All dismantling records signed by operator

**Data Captured:**
- Components extracted per item
- Dismantling time, operator ID
- Hazmat components removed and segregated

**Output:** `item_components` records; batch status → `dismantled`.

---

## Phase 6: Material Identification and Quantification

**Purpose:** Identify and weigh recovered material streams.

**Activities:**
- Sort extracted components by material type
- Weigh each material stream
- Sample testing for purity (optional, for high-value streams)
- Record material quantities per batch

**Material Streams Tracked:**
- Precious metals (gold, silver, copper, palladium from PCBs)
- Base metals (aluminum, iron/steel, tin)
- Battery materials (lithium, cobalt, nickel)
- Plastics (sorted by polymer type where possible)
- Glass
- Hazardous waste (mercury, lead)

**Output:** `material_recovery` records with weights and estimated compositions.

---

## Phase 7: Recovery Planning

**Purpose:** Select the optimal recovery method for each material stream.

**Activities:**
- Review material composition estimates
- Select smelter, hydrometallurgical or mechanical processing routes
- Plan logistics for outbound material shipment
- Generate preliminary economic valuation

**Recovery Methods:**
| Material | Recommended Method |
|----------|-------------------|
| PCBs (Au, Ag, Pd) | Pyrometallurgical smelting |
| Copper wires | Mechanical separation + smelting |
| Li-ion batteries | Hydrometallurgical leaching |
| Lead-acid batteries | Lead smelting (sealed facility) |
| Aluminum | Aluminium smelter |
| Plastics | Polymer sorting + extrusion |

**Output:** Recovery plan document attached to batch record.

---

## Phase 8: Material Recovery Operations

**Purpose:** Execute the selected recovery processes.

**Activities:**
- Ship material streams to partner recyclers or process in-house
- Receive recovery certificates and purity reports from smelters
- Record actual recovered quantities (not estimates)
- Update recovery records with actual vs. estimated values

**Output:** `material_recovery` records updated with actual quantities; batch status → `recovered`.

---

## Phase 9: Inventory Update and Tracking

**Purpose:** Update inventory with recovered materials.

**Activities:**
- Record recovered material quantities in inventory system
- Track outbound shipments to refineries
- Update revenue tracking with material sale prices
- Maintain chain-of-custody documentation

**Output:** Inventory and valuation records updated.

---

## Phase 10: Cost Analysis and Economic Valuation

**Purpose:** Calculate financial performance of the batch.

**Activities:**
- Sum all processing costs (labour, energy, logistics, compliance)
- Calculate gross material recovery value at current market prices
- Compute net value: gross recovery − total processing costs
- Compare against preliminary estimate from Phase 7

**Key Metrics:**
- Gross recovery value (USD)
- Total processing cost (USD)
- Net batch value (USD)
- Recovery efficiency (actual vs. estimated, %)

**Output:** `economic_valuations` records per batch.

---

## Phase 11: Environmental Impact Assessment

**Purpose:** Quantify the environmental benefit of recycling.

**Activities:**
- Calculate CO₂ equivalent avoided (vs. virgin material extraction)
- Record energy consumed in processing
- Document waste diverted from landfill (kg)
- Calculate water savings

**Key Metrics (research estimates):**
- CO₂ avoided per tonne of e-waste processed
- Landfill diversion (kg)
- Energy saved vs. primary production (MJ)

**Note:** All environmental figures are research-based estimates labeled `is_estimate=True`.

**Output:** `environmental_impact` records per batch.

---

## Phase 12: Compliance and Hazmat Handling

**Purpose:** Ensure full regulatory compliance throughout processing.

**Activities:**
- Verify all hazardous materials handled per RoHS/WEEE regulations
- Complete hazmat disposal manifests
- Obtain certificates of destruction for data-bearing devices
- File regulatory compliance documentation

**Regulatory Framework:**
- **RoHS Directive 2011/65/EU** — Restricted substances
- **WEEE Directive 2012/19/EU** — Producer responsibility
- **Basel Convention** — Transboundary movement of hazardous waste
- **Local national e-waste regulations** (varies by country)

**Output:** Compliance records and certificates attached to batch.

---

## Phase 13: Final Reporting and Documentation

**Purpose:** Generate comprehensive batch completion reports.

**Reports Generated:**
1. **Batch Summary Report** — All items, classifications, quantities
2. **Material Recovery Report** — What was recovered, in what quantities
3. **Economic Report** — Costs, revenues, net value
4. **Environmental Impact Report** — CO₂ avoided, landfill diversion
5. **Compliance Certificate** — Regulatory sign-off
6. **Research Data Export** — For academic analysis

**Output:** Reports saved as PDF/JSON; batch status → `completed`.

---

## Data Flow Diagram (ASCII)

```
Incoming E-Waste
      │
      ▼
[Phase 1] Registration ──────────────────────► waste_batches (registered)
      │
      ▼
[Phase 2] Assessment ────────────────────────► batch_items (created)
      │
      ▼
[Phase 3] AI Classification ─────────────────► item_classifications + confidence
      │            │
      │    [confidence < 0.5]
      │            └──────► Manual Expert Review
      │
      ▼
[Phase 4] Sorting ───────────────────────────► Processing streams assigned
      │
      ▼
[Phase 5] Dismantling ───────────────────────► item_components (extracted)
      │
      ▼
[Phase 6] Material Quantification ───────────► material_recovery (estimated)
      │
      ▼
[Phase 7] Recovery Planning ─────────────────► Recovery plan document
      │
      ▼
[Phase 8] Material Recovery ─────────────────► material_recovery (actual)
      │
      ▼
[Phase 9] Inventory Update ──────────────────► Inventory records
      │
      ▼
[Phase 10] Economic Valuation ───────────────► economic_valuations
      │
      ▼
[Phase 11] Environmental Assessment ─────────► environmental_impact
      │
      ▼
[Phase 12] Compliance ───────────────────────► Compliance certificates
      │
      ▼
[Phase 13] Final Reports ────────────────────► Reports (PDF/JSON)
                                               waste_batches (completed)
```

---

## Key Entities and Their Relationships

| Entity | Description | Key Relationships |
|--------|-------------|-------------------|
| `WasteBatch` | Top-level batch container | Has many BatchItems |
| `BatchItem` | Individual e-waste device | Belongs to WasteBatch; has Classifications, Components |
| `ItemClassification` | AI or manual classification result | Belongs to BatchItem |
| `ItemComponent` | Component extracted from item | Belongs to BatchItem |
| `MaterialRecovery` | Recovered material quantities | Belongs to WasteBatch |
| `EconomicValuation` | Financial analysis | Belongs to WasteBatch |
| `OperationalCost` | Processing cost records | Belongs to WasteBatch |

---

## Integration with AI Pipeline

The industrial workflow connects to the AI/ML pipeline at **Phase 3**:

1. A trained model is loaded from `saved_models/` via `ModelPredictor`
2. Item images or feature data are passed to `ClassificationWorkflow.classify_item()`
3. Results are written to `ItemClassification` records
4. Confidence thresholds route items to auto-process or manual review queues
5. Classification outcomes feed material estimation in Phase 6

**If no trained model exists:** The system flags all items for manual classification and continues the workflow. The AI pipeline does not block industrial operations.

---

## Environmental and Hazmat Notes

> **[!IMPORTANT]**
> Before starting any batch:
> 1. Check `HazmatChecker.check_device()` for all device types in the batch
> 2. Ensure appropriate PPE is available
> 3. Segregate CRT monitors, NiCd batteries, and mercury-containing devices before any bulk processing
> 4. All mercury-containing devices require sealed-room handling

> **[!WARNING]**
> Never shred or incinerate unknown device types without hazmat assessment. Burning e-waste releases toxic dioxins, furans, and heavy metal fumes.
