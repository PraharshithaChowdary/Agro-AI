# AGRO AI — REST API Documentation

**Tagline:** Smart Agriculture. Healthy Lives. Better Future.  
**Interactive Swagger UI:** `http://127.0.0.1:8000/docs`  
**ReDoc Documentation:** `http://127.0.0.1:8000/redoc`

---

## 1. General Endpoints

### `GET /api/health`
Returns system health, app name, and core capabilities.

**Sample Response (200 OK):**
```json
{
  "status": "healthy",
  "app": "AGRO AI",
  "tagline": "Smart Agriculture. Healthy Lives. Better Future.",
  "environment": "development",
  "features": [
    "Better Production (Crop & Soil Vision ML)",
    "Better Nutrition (BMR/TDEE & 7-Day Diet Planner)",
    "AGRO AI Assistant (Zero External Paid AI APIs)"
  ]
}
```

---

## 2. Authentication Endpoints

### `POST /api/auth/signup`
Registers a new user (Farmer, Buyer, or General User). Public Admin signup is rejected.

**Request Body:**
```json
{
  "fullName": "Maya Sharma",
  "email": "maya@example.com",
  "password": "SecurePassword123",
  "role": "farmer"
}
```

**Sample Response (201 Created):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "c1f7a075-8025-4b53-a5c3-...",
    "fullName": "Maya Sharma",
    "email": "maya@example.com",
    "role": "farmer",
    "createdAt": "2026-10-09T13:30:00"
  },
  "message": "Account registered successfully."
}
```

### `POST /api/auth/login`
Authenticates user and issues JWT bearer token.

---

## 3. Better Production Endpoints

### `POST /api/production/crop-analysis`
Accepts multipart image upload (`image/jpeg`, `image/png`, `image/webp`). Enforces agricultural relevance check before running disease inference.

**Sample Response (200 OK):**
```json
{
  "isAgricultural": true,
  "predictedCrop": "Tomato (Solanum lycopersicum)",
  "predictedCondition": "Early Blight (Alternaria solani)",
  "isHealthy": false,
  "confidence": 0.94,
  "severityLevel": "Moderate",
  "explanation": "Early Blight produces characteristic concentric target-board dark brown spots with yellow chlorotic halos...",
  "recommendations": [
    {
      "title": "Remove Affected Lower Foliage",
      "description": "Prune and safely destroy lower infected leaves...",
      "type": "action"
    },
    {
      "title": "Apply Organic Bio-Fungicide",
      "description": "Spray copper-based fungicide or Bacillus subtilis...",
      "type": "organic"
    }
  ],
  "preventionTips": [
    "Maintain 24-30 inch plant spacing for airflow.",
    "Use straw mulching to prevent spore splash."
  ],
  "scientificName": "Solanum lycopersicum",
  "modelStatus": "trained_model",
  "analysisTimestamp": "2026-10-09T13:35:00"
}
```

### `POST /api/production/soil-analysis`
Accepts soil photography, classifies visual soil category, and returns agronomic suitability.

---

## 4. Better Nutrition Endpoints

### `POST /api/nutrition/calculate`
Calculates BMR (Mifflin-St Jeor), TDEE, BMI, and macro splits.

### `POST /api/nutrition/weekly-plan`
Generates a complete 7-day schedule (5 meals per day) matching caloric targets and strictly respecting allergen exclusions.

---

## 5. AGRO AI Assistant Endpoints

### `POST /api/assistant/chat`
Offline knowledge-base chat endpoint.

**Request Body:**
```json
{
  "message": "How do I treat Tomato Early Blight?"
}
```

**Sample Response (200 OK):**
```json
{
  "response": "**Early Blight (*Alternaria solani*)** primarily affects tomatoes and potatoes...",
  "category": "disease",
  "suggestedQuestions": [
    "How to distinguish Early Blight from Late Blight?",
    "What are resistant tomato varieties?"
  ],
  "relatedAction": {
    "label": "Scan Tomato / Potato Leaf",
    "route": "/production/crop"
  }
}
```
