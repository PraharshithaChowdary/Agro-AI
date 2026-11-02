# AGRO AI — Troubleshooting & Operations Guide

## 1. Quick Diagnostic Checklist

| Check | Expected Result | Command / Action |
| :--- | :--- | :--- |
| **Backend Health** | HTTP 200 `{"status": "healthy"}` | Query `GET http://127.0.0.1:8000/api/health` |
| **Plant Catalog API** | HTTP 200 with the botanical text directory; image identification supports only the 14 labels documented in model_metadata.json | Query `GET http://127.0.0.1:8000/api/plants/stats` |
| **Frontend Dev Server** | HTTP 200 on port 5173 | Navigate to `http://localhost:5173/` |
| **Database Status** | `agro_ai.db` populated with records | Check SQLite tables: `plant_species`, `users`, `history` |
| **Unit Tests** | 37 passing tests | Run `.\venv\Scripts\python -m pytest backend/tests` |

---

## 2. Common Errors and Solutions

### Issue A: Windows PowerShell Script Execution Policy (`npm.ps1 cannot be loaded`)
**Symptom**:
```
npm : File C:\Program Files\nodejs\npm.ps1 cannot be loaded because running scripts is disabled on this system.
```
**Fix**:
Use the `.cmd` executable directly:
```powershell
npm.cmd run dev
npm.cmd run build
```

---

### Issue B: Missing Plant Catalog Database (`table plant_species not found` or 0 results)
**Symptom**:
Navigating to `/plants` shows no species, or searching returns an empty result set.
**Fix**:
Re-run the database catalog importer:
```powershell
.\venv\Scripts\python backend/data/import_plant_catalog.py
```
This script reads the verified seed JSON files in `backend/data/plant_catalog/` and populates `backend/agro_ai.db`.

---

### Issue C: Plant Identifier Model Not Found (`plant_identifier.joblib`)
**Symptom**:
Backend logs show:
```
WARNING: Plant identifier model file not found at .../plant_identifier.joblib
```
**Fix**:
Re-run the training script to export the calibrated ensemble model:
```powershell
.\venv\Scripts\python training/train_plant_identification.py
```
This generates `backend/models/plant_identifier.joblib` and updates `backend/models/model_metadata.json`.

---

### Issue D: Non-Agricultural Image Rejection
**Symptom**:
Upload returns:
```json
{
  "isAgricultural": false,
  "rejectionReason": "Uploaded image does not appear to contain recognizable agricultural foliage, leaves, crops, or soil."
}
```
**Explanation**:
This is an intentional safety feature. AGRO AI validates color histograms, chlorophyll ratios, and edge structures before classification to avoid generating false agricultural diagnoses for selfies, cars, furniture, or pets.
**Fix**:
Ensure the photograph depicts genuine leaves, flowers, fruits, bark, or plants against a natural or neutral background.

---

### Issue E: Port Conflicts (Port 8000 or 5173 Already in Use)
**Symptom**:
```
ERROR: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)
```
**Fix**:
Identify and terminate the lingering process or specify an alternative port:
```powershell
# Check process holding port 8000
netstat -ano | findstr :8000

# Kill process by PID
taskkill /F /PID <PID>

# Or start on another port
.\venv\Scripts\python -m uvicorn app.main:app --port 8001
```

---

## 3. Verifying System Endpoints

### 1. Catalog Statistics
```bash
curl -X GET "http://127.0.0.1:8000/api/plants/stats"
```
**Expected Response**:
```json
{
  "totalVerifiedSpecies": 98,
  "targetSpeciesCount": 10000,
  "categoriesCount": {
    "crop": 20,
    "vegetable": 25,
    "fruit": 21,
    "medicinal_spice": 18,
    "tree_ornamental": 14
  },
  "supportedDiseaseModelsCount": 13,
  "languagesSupported": 8
}
```

### 2. Search Plants
```bash
curl -X GET "http://127.0.0.1:8000/api/plants/search?q=moringa"
```

### 3. Automatic Mode A Identification
```bash
curl -X POST "http://127.0.0.1:8000/api/plants/identify" \
  -F "file=@leaf_sample.jpg" \
  -F "organ=leaf"
```

### 4. Plant Foliar Health Check
```bash
curl -X POST "http://127.0.0.1:8000/api/plants/analyze-health" \
  -F "file=@leaf_sample.jpg" \
  -F "plantName=Tomato"
```
