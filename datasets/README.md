# AGRO AI — Dataset Strategy & Setup Guide

**Tagline:** Smart Agriculture. Healthy Lives. Better Future.

---

## Important archive limitation

The current project archive contains four CSV files of engineered 48-dimensional feature rows. It does **not** contain the raw image directories sketched below (`train`, `validation`, `test`, `agriculture`, or `non_agriculture`). Therefore the CSVs cannot be used to retrain or honestly benchmark a raw-image CNN by themselves. Before claiming improved image accuracy, add licensed, labelled photographs for each target class, split them by source/plant (to avoid duplicate leakage), and evaluate once on an untouched real-photo test set. The existing model files are retained, but their reported accuracy is not independently verified against real photographs in this archive.

## 1. Directory Structure

```
datasets/
    agricultural_relevance/
        agriculture/        # Leaf photos, crops, fields, soil, farming scenes
        non_agriculture/    # Cars, selfies, phones, buildings, pizza, electronics
    crop_disease/
        train/              # Stratified training classes (e.g., Tomato___Early_blight, etc.)
        validation/         # Validation split for hyperparameter tuning & early stopping
        test/               # Unseen test split for final accuracy, precision, recall & confusion matrix
    soil/
        train/              # Labeled soil categories (Alluvial, Black, Clay, Laterite, Red, Sandy)
        validation/         # Validation split
        test/               # Unseen test split
```

---

## 2. Dataset Sources & Licenses

### A. Crop Foliar Disease Datasets
- **PlantVillage Dataset**: Contains over 54,306 images of healthy and diseased crop leaves across 38 class labels.
  - *Source:* [CrowdAI / PlantVillage](https://github.com/spMohanty/PlantVillage-Dataset)
  - *License:* Open Access / CC BY-SA 4.0.
- **PlantDoc Dataset**: Contains real-world field-condition photographs of plant diseases for enhanced domain generalization.
  - *Source:* [IIT Delhi PlantDoc](https://github.com/pratikkayal/PlantDoc-Dataset)
  - *License:* Academic & Research Open Use.

### B. Agricultural Relevance Filter Datasets
- **Agriculture Split**: Sampled evenly from PlantVillage, PlantDoc, soil samples, and farming landscape photographs.
- **Non-Agriculture Split**: Sampled from standard general-object benchmark datasets (such as COCO, ImageNet, or Pascal VOC subsets) including:
  - People / Selfies
  - Motor vehicles (cars, motorcycles)
  - Electronics (laptops, mobile phones)
  - Architectural scenes (buildings, interiors)
  - Processed foods (pizza, burgers, beverages)

### C. Soil Image Datasets
- **Soil Classification Dataset**: Multi-class surface soil photography.
  - *Categories:* Alluvial, Black (Regur), Red, Laterite, Heavy Clay, Sandy Loam.
  - *Source:* Kaggle Soil Types / ICAR agricultural soil collections.

---

## 3. Dataset Setup Workflow

To initialize folders and run integrity verification:
```bash
python training/prepare_dataset.py
```
