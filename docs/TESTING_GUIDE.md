# AGRO AI — Testing & Verification Guide

**Tagline:** Smart Agriculture. Healthy Lives. Better Future.

---

## 1. Automated Test Suite Execution

The backend contains a complete Pytest automated test suite covering all modules:

```bash
# Run all automated tests
pytest
```

### Test Suite Coverage
| Test File | Scope | Status |
|---|---|---|
| `backend/tests/test_health.py` | API health, CORS, status metadata | Passed |
| `backend/tests/test_production.py` | Crop diagnosis, soil assessment, non-agri rejection, malformed byte handling, history | Passed |
| `backend/tests/test_nutrition.py` | BMR & TDEE mathematical vectors, 7-day 5-meal schedule, strict allergy exclusion | Passed |
| `backend/tests/test_assistant.py` | Intent parsing, disease Q&A, soil guidance, nutrition advice, fallback clarification | Passed |

---

## 2. Manual Verification Test Matrix

Execute these manual tests through the React frontend UI or API client to verify end-to-end behavior:

| Test Case # | Input Type / Image Category | Expected System Behavior | Result Status |
|---|---|---|---|
| **TC-01** | Genuine Green Leaf (Healthy Tomato/Potato) | Agricultural check passes. Predicts healthy crop foliage with high confidence (>90%). Generates care tips. | Verified |
| **TC-02** | Diseased Leaf (Early/Late Blight or Rust) | Agricultural check passes. Identifies pathogen, assigns severity level, outputs 4-5 actionable recommendations. | Verified |
| **TC-03** | Genuine Soil Photo (Dark Earth / Red Sand) | Agricultural check passes. Predicts soil category, lists physical characteristics, suitable crops, and displays lab disclaimer. | Verified |
| **TC-04** | Agricultural Field / Farming Landscape | Passes agricultural validation. Categorizes as agricultural environment. | Verified |
| **TC-05** | Human Portrait / Selfie | Rejects with message: *"Invalid Image — This image does not appear to be related to crops, soil, or farming. Please upload a suitable agricultural image."* | Verified |
| **TC-06** | Motor Vehicle / Car | Rejects with 400 Bad Request error and non-agricultural notice. | Verified |
| **TC-07** | Processed Food (Pizza / Burger) | Rejects with non-agricultural notice. Zero false agricultural recommendations generated. | Verified |
| **TC-08** | Random Household Object (Keyboard / Phone) | Rejects with non-agricultural notice. | Verified |
| **TC-09** | Blurry / Ambiguous Photo | Returns uncertainty advisory: *"Uncertain Image — The photograph detail is unclear. Please provide a clear, well-lit image..."* | Verified |
| **TC-10** | Nutrition: Peanut & Dairy Allergy | Generates full 7-day 5-meal schedule with 0% peanut or dairy items across all 35 meals. | Verified |
| **TC-11** | AGRO AI Assistant: Crop Disease Query | Returns structured Markdown response detailing symptoms, organic remedies, cultural practices, and deep-link button. | Verified |

---

## 3. Frontend Build & Typecheck Validation

To test that all TypeScript interfaces, JSX templates, and Tailwind styles compile cleanly:

```bash
cd frontend
npm run build
```

Expected output:
```
✓ built in ~30s
dist/index.html
dist/assets/index.css
dist/assets/index.js
```
