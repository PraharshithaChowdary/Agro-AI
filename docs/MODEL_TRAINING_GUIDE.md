# AGRO AI — Model Training & Machine Learning Guide

> **Smart Agriculture. Healthy Lives. Better Future.**

This guide details the end-to-end Machine Learning training workflow for plant species identification, leaf disease diagnosis, and soil categorization across local environments and **Google Colab**.

---

## 🎯 Target Goals vs. Active Capabilities

| Domain | Long-Term Target | Active Supported Benchmark | Backbone Architecture |
|---|---|---|---|
| **Plant Species** | Up to 10,000 Species (PlantCLEF) | 13 Agricultural Flora Species | MobileNetV2 / Botanical Ensemble |
| **Leaf Pathogens** | 100+ Plant Pathogens | 39 Disease & Healthy States | MobileNetV2 + ExtraTrees Ensemble |
| **Soil Categories** | Up to 50 Soil Series | 6 Major Visual Categories | Random Forest + Color Moments |
| **Modality Verifier** | General Agricultural | 3 Modalities (`crop_leaf`, `soil`, `non_agri`) | 42-Dim Feature Ensemble |

---

## 🚀 Step-by-Step Training Procedures

### Pipeline 1: Local Ensemble Training (Fast & Offline)
To train the multi-spectral feature ensemble on 70,800 augmented data samples:
```bash
python backend/scripts/train_botanical_classifier.py
```
This generates and exports:
- `backend/models/crop_disease.joblib`
- `backend/models/soil_classifier.joblib`
- `backend/models/agricultural_relevance.joblib`
- `backend/models/model_metadata.json`

### Pipeline 2: Google Colab Deep Learning Transfer Learning
For deep CNN fine-tuning with GPU acceleration:
1. Open [Google Colaboratory](https://colab.research.google.com).
2. Upload the desired notebook from `training/`:
   - `training/plant_species_training.ipynb`
   - `training/leaf_disease_training.ipynb`
   - `training/soil_classification_training.ipynb`
3. Navigate to: `Runtime` -> `Change runtime type` -> **Hardware accelerator: T4 GPU**.
4. Run all cells to download public benchmarks, augment images, train the model, evaluate classification reports and confusion matrices, and export `.keras` weight files.
5. Place downloaded `.keras` files into `backend/models/`.

---

## 🔬 Image Preprocessing & Normalization Parity

Training and inference pipelines must strictly adhere to identical image transformations:
- **Input Resolution:** Standardized to $224 \times 224 \times 3$ pixels.
- **Color Conversion:** Enforced standard RGB.
- **Pixel Normalization:** Scaled to $[0.0, 1.0]$.
- **Data Augmentation:** Random rotations ($\pm 25^\circ$), horizontal flips, zoom ($\pm 20\%$), shear ($\pm 15\%$), and illumination jitter.

---

## 📊 Evaluation Metrics & Uncertainty Thresholds

- **Calibrated Confidence:** Models output calibrated prediction confidence.
- **Uncertainty Rejection:** If maximum probability falls below 40% or synthetic/non-agricultural signatures are detected, the system safely returns an informative uncertainty message rather than forcing an inaccurate classification.
