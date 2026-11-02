# AGRO AI — Model Deployment & Production Loading Guide

This document outlines how trained machine learning models are registered, loaded into memory, and served via the FastAPI backend.

---

## 🏛️ Model Registry Architecture

The backend implements a thread-safe singleton `ModelRegistry` in [`backend/app/ml/model_loader.py`](file:///c:/Users/praha/Desktop/PDD%20AGRO%20AI/backend/app/ml/model_loader.py).

### Loading Precedence:
1. **Pre-compiled Scikit-Learn Ensembles (`.joblib`):** Loaded via `joblib.load()` into RAM upon server startup for sub-millisecond CPU inference without external runtime dependencies.
2. **Deep Learning Weights (`.keras`):** Loaded via `tensorflow.keras.models.load_model()` when `.keras` artifacts are placed in `backend/models/`.
3. **Structured Agronomic Knowledge Bases:** Enrich predictions with actionable organic remedies, prevention steps, scientific names, and disclaimers.

---

## 📁 Model Directory Structure

Trained artifacts are stored in `backend/models/`:

```
backend/models/
├── agricultural_relevance.joblib    # Modality & non-agri filter
├── crop_disease.joblib              # 39-class foliar & pathogen ensemble
├── soil_classifier.joblib           # 6-class visual soil classifier
└── model_metadata.json              # Canonical class mappings and feature specs
```

---

## 🔍 Model Verification Command

Verify the presence and integrity of all registered models:

```bash
python backend/scripts/check_models.py
```

Expected diagnostic output:
```
[FOUND] crop_disease.joblib (Size: ~489 MB)
[FOUND] soil_classifier.joblib (Size: ~650 KB)
[FOUND] agricultural_relevance.joblib (Size: ~100 KB)
[FOUND] model_metadata.json (Classes mapped: 39 crop, 6 soil, 3 modality)
```
