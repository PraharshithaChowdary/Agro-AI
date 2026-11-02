# AGRO AI — Model Weights Directory

This directory stores exported machine learning models and metadata for the AGRO AI platform.

## Expected Files

- `agricultural_relevance.keras`: Binary classifier separating agricultural photos from non-agricultural imagery.
- `crop_disease.keras`: Multi-class MobileNetV2 classifier for crop species and foliar pathogens.
- `soil_classifier.keras`: Multi-class visual soil category classifier.
- `model_metadata.json`: Model versioning, class mappings, preprocessing details, and metrics.

## How to Generate & Export Trained Weights

1. **Google Colab Notebook (Recommended for GPU Acceleration):**
   Open and run all cells in `training/agro_ai_production_training.ipynb`.
   Download the resulting `.keras` files and place them into this `backend/models/` folder.

2. **Local Training Scripts:**
   ```bash
   python training/train_agricultural_relevance.py
   python training/train_crop_disease.py
   python training/train_soil_classifier.py
   ```

3. **Verify Loaded Models:**
   ```bash
   python backend/scripts/check_models.py
   ```
