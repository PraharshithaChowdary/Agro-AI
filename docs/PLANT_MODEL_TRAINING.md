# AGRO AI — Plant Model Training, Calibration & Transfer Learning

## 1. Architecture Overview

Plant identification across thousands of species requires balancing two competing objectives:
1. **High Visual Discrimination**: Capturing subtle differences in venation, margin dentition, and floral petal geometry.
2. **Honest Uncertainty & Fast Inference**: Providing calibrated class posterior probabilities and rejecting ambiguous or out-of-distribution foliage without prohibitive computational latency on edge/server instances.

AGRO AI adopts a dual-tier approach:
- **Tier 1 (Production Botanical Feature Ensemble)**: Fast, calibrated Extra-Trees and CalibratedClassifierCV over a 42-dimensional botanical feature representation (`backend/models/plant_identifier.joblib`).
- **Tier 2 (Deep Transfer Learning Pipeline)**: MobileNetV2 / EfficientNet-B0 backbone fine-tuned on Indian plant image datasets via Google Colab (`training/indian_plant_identification.ipynb`).

---

## 2. 42-Dimensional Botanical Feature Representation

The lightweight production inference service extracts a 42-dimensional feature vector per species/image:

1. **Color Profile (Dimensions 0–14)**:
   - Green chlorophyll ratio ($G / (R + G + B)$).
   - Red anthocyanin ratio and yellow carotenoid ratio.
   - HSV color space means and standard deviations (Hue, Saturation, Value).
   - LAB lightness and a/b color opponent coordinates.
2. **Texture & Edge Density (Dimensions 15–24)**:
   - Sobel gradient energy across horizontal and vertical axes (representing leaf venation prominence).
   - Laplacian variance (focus quality and surface roughness).
   - Gray-Level Co-occurrence Matrix (GLCM) contrast and homogeneity proxies.
3. **Morphology & Organ Geometry (Dimensions 25–34)**:
   - Aspect ratio, eccentricity, and perimeter-to-area compactness.
   - Organ encoding (leaf, flower, fruit, bark, whole plant).
4. **Taxonomic & Categorical Priors (Dimensions 35–41)**:
   - Category encoding (`crop`, `vegetable`, `fruit`, `medicinal_spice`, `tree_ornamental`).
   - Growth habit indicators (herb, shrub, tree, climber).

---

## 3. Probability Calibration & Uncertainty Estimation

Uncalibrated deep networks and decision trees often exhibit extreme overconfidence even when incorrect. To guarantee reliable decisions:

### Platt Scaling & CalibratedClassifierCV
The ensemble uses 3-fold cross-validated sigmoid calibration (`CalibratedClassifierCV(method='sigmoid', cv=3)`):
$$P(Y = c \mid X) = \frac{1}{1 + \exp(A \cdot f(X) + B)}$$
This maps raw decision function scores to true empirical probabilities.

### Shannon Entropy for Ambiguity Rejection
The model computes the Shannon entropy across the top-5 probability vector:
$$H(p) = -\sum_{i=1}^{5} p_i \log_2(p_i + 10^{-12})$$
- If $H(p) > 2.0$ or $\max(p) < 0.28$, the system classifies the sample as **Ambiguous**.
- Instead of returning a false high-confidence label, the UI presents the ambiguity banner and advises the user to check alternative organs or verify regional names.

---

## 4. Local Training Script (`training/train_plant_identification.py`)

To re-train or update the local model when adding new catalog species:

```bash
# Run using the project Python virtual environment
.\venv\Scripts\python training/train_plant_identification.py
```

### Script Execution Flow:
1. Loads the unified catalog from `backend/data/manifests/unified_plant_manifest.json` (or database).
2. Synthesizes feature distributions per species based on catalogue traits (leaf shape, margin, color, growth habit). This is a prototype for structured-feature classification, not a substitute for supervised training on labelled photographs.
3. Adds realistic Gaussian jitter ($\sigma = 0.05$) to simulate field lighting and camera variance.
4. Trains an `ExtraTreesClassifier` (120 estimators, balanced class weights).
5. Fits a `CalibratedClassifierCV` wrapper for well-behaved posterior probabilities.
6. Reports Top-1 and Top-5 metrics for the generated-feature hold-out split. These synthetic-feature metrics are not evidence of real-photo accuracy and must not be reported as field performance. Any previously stated 100% Top-5 result is historical and has not been independently reproduced in this handover.
7. Serializes the pipeline to `backend/models/plant_identifier.joblib`.
8. Updates metadata in `backend/models/model_metadata.json`.

---

## 5. Google Colab Deep Transfer Learning Notebook

For large-scale deep vision training on GPUs:
- **Notebook Path**: `training/indian_plant_identification.ipynb`
- **Backbone**: `MobileNetV2` pretrained on ImageNet (lightweight, mobile-ready).
- **Resolution**: $224 \times 224 \times 3$ with standard normalization.
- **Data Augmentation**:
  - Random horizontal and vertical flips.
  - Rotation ($\pm 25^\circ$).
  - Zoom and brightness variations ($\pm 20\%$).
- **Loss Function**: Categorical Crossentropy with Label Smoothing ($\epsilon = 0.1$).
- **Optimizer**: Adam with learning rate warmup and Cosine Annealing decay.
- **Export Targets**:
  - `keras_model.h5`
  - `tflite_quantized_model.tflite` for edge deployment on farmer mobile devices.
