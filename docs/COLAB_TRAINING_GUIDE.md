# AGRO AI — Google Colab Model Training Guide

**Tagline:** Smart Agriculture. Healthy Lives. Better Future.

---

## 1. Introduction

This guide walks you through executing the end-to-end Machine Learning training workflow in **Google Colab** with GPU acceleration.

Notebook Location: `training/agro_ai_production_training.ipynb`

---

## 2. Step-by-Step Google Colab Workflow

### Step 1: Open Google Colab
1. Navigate to [Google Colaboratory](https://colab.research.google.com).
2. Click **Upload** and select `training/agro_ai_production_training.ipynb` from your local workspace.

### Step 2: Enable GPU Hardware Acceleration
1. In Colab, go to the top menu: `Runtime` -> `Change runtime type`.
2. Select **Hardware accelerator: T4 GPU** (or A100 if available).
3. Click **Save**.

### Step 3: Execute Cells Sequentially
The notebook contains 20 numbered cells:
- **Cells 1-2:** Environment initialization & GPU verification.
- **Cells 3-7:** Dataset tree inspection, class distribution plots, integrity verification, corrupt image quarantine, and duplicate MD5 hash detection.
- **Cells 8-10:** Image normalization ($224 \times 224$), stratified train/val/test splitting, and data augmentation.
- **Cells 11-13:** MobileNetV2 transfer learning model architecture definition, Adam optimizer compilation, and training with `EarlyStopping` & `ModelCheckpoint`.
- **Cells 14-17:** Validation curve plotting, test set evaluation, classification report (Precision, Recall, F1), and Confusion Matrix heatmap.
- **Cells 18-20:** Model export to `.keras` format, metadata JSON generation, and single-image test inference.

### Step 4: Export Trained Weights to AGRO AI
Once training completes, download the exported file:
- `crop_disease.keras` -> Copy to `backend/models/crop_disease.keras`
- `agricultural_relevance.keras` -> Copy to `backend/models/agricultural_relevance.keras`
- `soil_classifier.keras` -> Copy to `backend/models/soil_classifier.keras`

### Step 5: Verify in Backend
Run the model diagnostic tool in your backend:
```bash
python backend/scripts/check_models.py
```
The status will display `[FOUND]` for all newly placed model weight files.
