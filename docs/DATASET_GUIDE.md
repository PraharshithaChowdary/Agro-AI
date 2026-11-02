# AGRO AI — Dataset Guide & Large-Scale Data Strategy

> **Smart Agriculture. Healthy Lives. Better Future.**

---

## 1. Overview & Multi-Stage Dataset Pipeline

AGRO AI vision architecture separates visual intelligence into three dedicated tasks:
1. **Plant Species Identification:** Botanical flora taxonomy (13 active species, scaling towards 10,000 via PlantCLEF).
2. **Crop Foliar Disease Diagnosis:** 39 fine-grained healthy and pathogen classes (PlantVillage & PlantDoc).
3. **Pedological Soil Classification:** 6 visual soil classifications (Alluvial, Black/Regur, Clay, Laterite, Red, Sandy Loam — scaling towards 50).
4. **Agricultural Relevance & Modality:** Gatekeeper rejecting selfies, electronics, vehicles, and furniture.

---

## 2. Directory Layout & Organization

Datasets are structured into segregated task directories with train, validation, and test splits:

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
└── manifests/              # MD5 deduplication manifests
    ├── plants_manifest.json
    ├── leaf_diseases_manifest.json
    └── soil_manifest.json
```

---

## 3. Official Dataset Sources & Acquisition

### A. PlantCLEF Large-Scale Plant Identification
- **Source:** [PlantCLEF Official Benchmark](https://www.imageclef.org/node/332)
- **Target:** Up to 10,000 botanical plant species.
- **License:** Research & Academic Access.

### B. PlantVillage Dataset
- **Source:** [PlantVillage Repository on GitHub](https://github.com/spMohanty/PlantVillage-Dataset)
- **Content:** 54,306 laboratory leaf photographs across healthy and diseased states.
- **License:** CC-BY-SA 4.0.

### C. PlantDoc In-Field Dataset
- **Source:** [PlantDoc Repository on GitHub](https://github.com/pratikkayal/PlantDoc-Dataset)
- **Content:** 2,569 field photographs under natural lighting, complex backgrounds, and occlusion.
- **License:** MIT.

### D. Soil Type Benchmark
- **Source:** Kaggle Soil Types & ICAR regional survey collections.
- **Classes:** Alluvial Soil, Black Soil (Regur), Heavy Clay, Laterite Soil, Red Soil, Sandy Loam Soil.
- **License:** CC0 / Public Domain.

---

## 4. Dataset Management Tools

Execute data management via the `backend/data/` scripts:
```bash
# 1. Download official public benchmarks
python backend/data/download_datasets.py plantvillage

# 2. Partition into stratified splits with MD5 deduplication
python backend/data/prepare_datasets.py

# 3. Audit for corruption, leakage, and class distributions
python backend/data/validate_datasets.py
```
