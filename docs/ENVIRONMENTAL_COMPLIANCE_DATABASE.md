# E-WASTE AI — Environmental, Compliance & AI Database

Covers **Module 13 (Environmental & Compliance Records — 8 Tables)** and **Module 14 (AI & Automation Database — 8 Tables)**.

---

## 1. Environmental & Hazardous Compliance Tracking (Module 13)

- **Tables:** `authorized_recycler_records`, `hazardous_waste_movements`, `environmental_measurements`, `waste_disposal_records`, `compliance_documents`, `compliance_observations`, `environmental_audit_records`, and extended `environmental_reports`.
- **Configurable Categories & Jurisdictions:** `compliance_documents`, `environmental_measurements`, and `environmental_reports` support configurable `compliance_category` and `jurisdiction_ref` metadata alongside supporting document links (`supporting_document_id` / `document_url`).
- **Zero Auto-Certification Policy:**
  - `ComplianceDocument.is_legal_certification` defaults to `False`.
  - **Report 13 (`environmental_records_report`)** explicitly flags `"is_certified": False` and states *"Internal operational records summary — does NOT represent legal regulatory certification."*
  - **Report 12 (`hazardous_waste_tracking_report`)** aggregates real `hazardous_material_records` vs `hazardous_waste_movements` weights without inventing disposal manifests or regulatory approvals.

---

## 2. AI & Automation Integration (Module 14)

- **Tables:** `ai_models`, `ai_model_versions`, extended `ai_predictions`, `ai_prediction_feedback`, `recovery_recommendations`, `anomaly_records`, `forecasting_results`, and `automation_jobs`.
- **Model-to-Batch Traceability:** Extended columns on `ai_predictions` link AI predictions directly to `company_id`, `branch_id`, `incoming_batch_id`, and `ai_model_version_id`, alongside `review_status`, `human_verified`, `verified_by`, `verified_at`, and `final_measured_outcome`.
- **Human-in-the-Loop Verification:** `ComplianceAIService.verify_ai_prediction()` (exposed at `POST /api/v1/erp/ai/feedback`) records operator feedback in `ai_prediction_feedback`, updates `ai_predictions`, feeds **Report 14 (`ai_prediction_performance_report`)**, and logs `VERIFY_AI` in `audit_logs`.
