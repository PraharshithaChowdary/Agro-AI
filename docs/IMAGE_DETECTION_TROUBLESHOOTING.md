# AGRO AI — Image Detection Troubleshooting & Diagnostics

> **Diagnostic guide for resolving misclassifications, class-mapping discrepancies, and modality issues.**

---

## 🔍 Common Detection Questions & Solutions

### 1. "Corn leaf is identified as Cucumber or Pepper"
- **Cause:** Class-index mismatch between training labels and prediction dictionaries, or improper foreground isolation.
- **Solution:** 
  1. Class mappings are strictly locked to `backend/models/model_metadata.json`.
  2. Botanical linear blade ratios ($vert\_dom > 2.0$, aspect ratio $> 1.8$) give high prior weighting to monocot cereal crops (Corn, Wheat, Rice) and prevent broadleaf confusion.
  3. Ensure photos are well-lit and focused on the leaf surface.

### 2. "Soil sample uploaded to Crop Analysis is rejected"
- **Behavior:** This is an intentional safety feature.
- **Guidance:** The Agricultural Relevance Gatekeeper detects soil texture and prompts the user with a direct switch button to the **Soil Category Assessment** module (`/production/soil`).

### 3. "Image rejected with Non-Agricultural Warning"
- **Cause:** The image contains artificial screen blues, high synthetic saturation, selfies, cars, furniture, or buildings.
- **Guidance:** Ensure the camera is directed at actual farming subjects: crops, plant foliage, leaves, or soil surfaces.

### 4. "Blurry or Low-Resolution Images"
- **Constraint:** Images under $50 \times 50$ pixels or with extreme motion blur cannot be reliably analyzed. Upload a clear photograph of at least $224 \times 224$ resolution.
