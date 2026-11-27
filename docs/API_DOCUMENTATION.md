# E-Waste AI — API Documentation (Phase 4)

## Base URL
- **Local:** `http://localhost:8000`
- **API Docs (Swagger):** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **GitHub:** https://github.com/azharlionkgf/ewaste-ai

## Authentication

All protected endpoints require a Bearer JWT token.

```http
Authorization: Bearer <access_token>
```

### Register
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "operator1",
  "email": "op1@company.com",
  "password": "SecurePass123!",
  "full_name": "Operator One",
  "role": "operator"
}
```

### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{ "username": "operator1", "password": "SecurePass123!" }
```
**Response:**
```json
{ "access_token": "eyJ...", "token_type": "bearer", "expires_in": 3600 }
```

## Batch Management

### Register Batch
```http
POST /api/v1/batches
Content-Type: application/json

{
  "source": "ABC Electronics",
  "total_weight_kg": 500.0,
  "waste_category": "WEEE Category 4",
  "location": "Warehouse B"
}
```

### List Batches
```http
GET /api/v1/batches?status=received&limit=50
```

### Update Status
```http
PATCH /api/v1/batches/{id}/status
{ "status": "sorted" }
```
Valid statuses: `received` → `sorted` → `dismantled` → `processed` → `completed`

### Add Device to Batch
```http
POST /api/v1/batches/{id}/devices
{ "device_type": "laptop", "weight_kg": 1.8, "condition": "damaged" }
```

## AI Model Integration

### Check Model Availability
```http
GET /api/v1/ai/status
```
Response shows which task types have trained models available.

### Tabular Prediction
```http
POST /api/v1/ai/predict/tabular
{
  "task_type": "ewaste_classification",
  "input_data": { "feature1": 1.0, "feature2": 0.5 },
  "model_id": null
}
```
If no model is trained: returns `prediction_type: "unavailable"` with instructions.

### Image Classification
```http
POST /api/v1/ai/classify/image
Content-Type: multipart/form-data
file: <image file>
```
Max size: 50 MB. Allowed: JPEG, PNG, WebP.

### Batch Prediction
```http
POST /api/v1/ai/predict/batch?task_type=ewaste_classification
[
  { "feature1": 1.0 },
  { "feature1": 2.5 }
]
```
Limit: 1000 records per request.

## Recovery Intelligence

### Estimate Recovery
```http
POST /api/v1/intelligence/recovery/estimate
{ "device_type": "laptop", "weight_kg": 1.5 }
```
Returns: material breakdown, recoverable quantities, recommendations, disclaimer.
All values clearly labeled as `rule_based` with composition data sources.

## Economic Intelligence

### Economic Analysis
```http
POST /api/v1/intelligence/economics/analyze
{ "device_type": "smartphone", "weight_kg": 0.2 }
```
Returns: gross value, processing cost, net value, material breakdown, price sources.
All values clearly labeled as ESTIMATES with disclaimer.

### Material Price Reference
```http
GET /api/v1/intelligence/economics/prices/gold
```

## Decision Support

### Get Recommendations
```http
POST /api/v1/intelligence/decisions/recommend?device_type=laptop
```
Returns: step-by-step processing recommendations with reasoning, hazard flags, disclaimer.

## Environmental Reporting

### Generate Batch Environmental Report
```http
POST /api/v1/environmental/report/{batch_id}
```

## Reports

### Generate Batch Report
```http
POST /api/v1/reports/batch/{batch_id}?format=json
```
Supported formats: `json`, `csv`

## Error Responses

All errors return:
```json
{ "success": false, "error": "Description", "detail": "Optional detail" }
```

| Code | Meaning |
|------|---------|
| 400 | Bad request / validation error |
| 401 | Invalid or expired token |
| 403 | Forbidden (insufficient role) |
| 404 | Resource not found |
| 413 | File too large |
| 429 | Rate limit exceeded |
| 500 | Internal error (detail hidden in production) |

## API Versioning

All endpoints are versioned: `/api/v1/...`

Future versions will use `/api/v2/...` with backwards compatibility notes.
