# AGRO AI — Dataset Engineering & Data Management

This directory contains the dataset configuration, acquisition scripts, splitting engines, and integrity validation tools for the **AGRO AI** machine learning vision pipelines.

---

## 📁 Directory Architecture

Ensure datasets are downloaded and partitioned according to this standard:

```
datasets/
├── plants/                 # Plant species taxonomy benchmark
│   ├── train/
│   ├── validation/
│   └── test/
├── leaf_diseases/          # Foliar pathogen diagnostics (PlantVillage / PlantDoc)
│   ├── train/
│   ├── validation/
│   └── test/
├── soil/                   # Pedological soil classifications
│   ├── train/
│   ├── validation/
│   └── test/
└── manifests/              # Immutable JSON manifests with MD5 deduplication
    ├── plants_manifest.json
    ├── leaf_diseases_manifest.json
    └── soil_manifest.json
```

---

## 🛠️ Dataset Management Scripts

### 1. Dataset Acquisition
Acquire official public benchmarks with disk space pre-flight verification:
```bash
python backend/data/download_datasets.py plantvillage
python backend/data/download_datasets.py plantdoc
```

### 2. Dataset Preparation & Partitioning
Partitions raw image files into stratified **Train (70%) / Validation (15%) / Test (15%)** splits and eliminates train-test contamination via MD5 hash matching:
```bash
python backend/data/prepare_datasets.py
```

### 3. Integrity & Leakage Auditor
Audits images for corruption, decodability, class distribution, and split leakage:
```bash
python backend/data/validate_datasets.py
```

---

## 📜 Dataset Sources & Attribution

1. **PlantVillage Dataset**:
   - URL: [https://github.com/spMohanty/PlantVillage-Dataset](https://github.com/spMohanty/PlantVillage-Dataset)
   - License: CC-BY-SA 4.0 / Open Academic Research
   - Modality: Standardized leaf laboratory photographs.

2. **PlantDoc Dataset**:
   - URL: [https://github.com/pratikkayal/PlantDoc-Dataset](https://github.com/pratikkayal/PlantDoc-Dataset)
   - License: MIT
   - Modality: In-field real-world agricultural photographs under variable lighting.

3. **PlantCLEF Species Identification Benchmark**:
   - URL: [https://www.imageclef.org/node/332](https://www.imageclef.org/node/332)
   - License: Research & Academic Use
   - Modality: Large-scale botanical flora taxonomy targeting up to 10,000 plant species.

4. **Kaggle Soil Types Benchmark**:
   - License: CC0 / Public Domain
   - Modality: Visual surface photographs across Alluvial, Black/Regur, Clay, Laterite, Red, and Sandy Loam soils.
