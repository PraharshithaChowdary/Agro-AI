# AGRO AI — Large-Scale Botanical Dataset & Model Training Pipeline Specification

**Project:** AGRO AI — Large-Scale Plant Identification and Smart Agriculture  
**Academic Degree:** Final Year Project (B.Tech / B.E. Computer Science & AI / Agriculture Engineering)  
**Document Type:** Dataset Provenance, Scalable Architecture & Machine Learning Pipeline Reference  
**Last Verified:** October 2026  

---

## 1. Executive Overview & Problem Formulation

Standard academic plant identification projects are typically confined to closed-set classification benchmarks consisting of 14, 30, or 50 plant classes (e.g. basic PlantVillage subsets). While these models achieve nominal accuracy on laboratory-acquired foliar images, they fail catastrophically in real-world deployment:
1. **Repeated & Random Predictions:** Uncalibrated softmax heads output 95%+ confidence on arbitrary classes when encountering unfamiliar species, out-of-distribution flora, or non-foliar organs.
2. **Artificial Taxonomic Scarcity:** A 30-class model cannot serve real agricultural or botanical queries across India's rich biodiversity (over 47,000 recorded plant species).
3. **Absence of Botanical Intelligence:** Simple vision classifiers lack contextual plant metadata, regional vernacular nomenclature, soil affinity, cultivation cycles, and foliar health indicators.

To address these limitations, **AGRO AI** decouples the botanical knowledge base from the deep learning visual inference engine while providing an architecturally sound pathway toward large-scale visual recognition.

---

## 2. Botanical Knowledge Base Architecture (10,206 Verified Species)

### 2.1 Database Scale & Taxonomic Diversity
The searchable botanical database is hosted in SQLite (`backend/agro_ai.db`) and indexed via SQLAlchemy. As of October 2026, the database contains **10,206 verified botanical species records** spanning **45 plant families**:

| Botanical Group / Category | Species Count | Representative Families & Genera |
|:---|:---:|:---|
| **Agricultural Crops & Cereals** | 1,248 | Poaceae (*Zea mays*, *Oryza sativa*, *Triticum aestivum*, *Sorghum bicolor*) |
| **Medicinal & Aromatic Plants** | 1,860 | Lamiaceae (*Ocimum tenuiflorum*), Meliaceae (*Azadirachta indica*), Zingiberaceae |
| **Vegetables & Legumes** | 1,420 | Solanaceae (*Solanum lycopersicum*), Fabaceae (*Cajanus cajan*, *Glycine max*) |
| **Fruit Trees & Orchard Crops** | 1,180 | Rutaceae (*Citrus sinensis*), Rosaceae (*Malus domestica*, *Prunus*), Vitaceae |
| **Flowering & Ornamental Plants**| 1,650 | Asteraceae (*Helianthus*, *Tagetes*), Malvaceae (*Hibiscus*), Orchidaceae |
| **Forest Trees & Timber** | 1,210 | Moraceae (*Ficus benghalensis*), Fabaceae (*Dalbergia sissoo*), Dipterocarpaceae |
| **Shrubs, Grasses & Vines** | 1,120 | Cucurbitaceae (*Cucurbita pepo*), Convolvulaceae, Apocynaceae |
| **Aquatic & Wild Flora** | 518 | Nymphaeaceae (*Nelumbo nucifera*), Araceae, Pontederiaceae |
| **Total Verified Species** | **10,206** | **45 Major Botanical Families** |

### 2.2 Multilingual Vernacular Nomenclature
Every species record contains verified common, scientific, and Indian vernacular names:
- **English:** Common agricultural or commercial names.
- **Telugu (తెలుగు):** e.g., మొక్కజొన్న (*Zea mays*), టమాటో (*Solanum lycopersicum*), వేప (*Azadirachta indica*), తులసి (*Ocimum tenuiflorum*).
- **Hindi (हिन्दी):** e.g., मक्का (*Zea mays*), टमाटर (*Solanum lycopersicum*), नीम (*Azadirachta indica*), तुलसी (*Ocimum tenuiflorum*).
- **Tamil (தமிழ்):** e.g., சோளம் (*Zea mays*), தக்காளி (*Solanum lycopersicum*), வேம்பு (*Azadirachta indica*), துளசி (*Ocimum tenuiflorum*).
- **Taxonomic Rank:** Family, Genus, Species, Botanical Synonyms.

### 2.3 Sub-60ms Multilingual Autocomplete
Autocomplete queries execute via `GET /api/plants/autocomplete?q=<prefix>&limit=8`.
- Multi-column B-tree indexed searching across `scientific_name`, `common_name`, `telugu_name`, `hindi_name`, and `tamil_name`.
- Instant sub-60ms response latency on SQLite, allowing instant discovery of 10,206 species directly in the frontend regardless of whether the species is in the current vision model.

---

## 3. Large-Scale Vision Dataset Research & Feasibility Analysis

### 3.1 Dataset Comparison Matrix

| Dataset | Images | Classes / Species | License | Uncompressed Size | Hardware Requirement | Feasibility for Local / Free Colab |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **PlantVillage** | 54,306 | 14 crops (38 health states) | CC0 / Public Domain | ~1.5 GB | Any CPU / GPU | **Fully Feasible** (Current local ONNX) |
| **Indian Medicinal Leaves** | 6,900 | 40 species | Research / Open | ~1.8 GB | Standard Colab T4 | **Fully Feasible** |
| **PlantNet-300K** | 306,293 | 1,081 species | CC BY-SA 4.0 | ~35 GB | Multi-GPU / Colab Pro | **Moderate Feasibility** (Subsets) |
| **PlantCLEF 2024 / Pl@ntNet** | 1,483,165 | 7,806 species | CC BY-SA 4.0 | ~420 GB | Multi-A100 cluster / TB storage | **Requires Cloud Storage & Embedding Retrieval** |
| **Kaggle 100 Indian Plants** | ~12,000 | 100 species | Research | ~4.5 GB | Standard Colab T4 | **High Feasibility** |

### 3.2 Storage & Hardware Feasibility Findings
1. **Local Machine Storage:** Local development machines typically possess 10–50 GB free disk space. Downloading the full 420 GB PlantCLEF 2024 archive locally is technically infeasible and would cause disk exhaustion.
2. **Google Colab Free Tier:** Colab free sessions allocate ~75–100 GB ephemeral disk space and disconnect after 12 hours. A full 420 GB dataset cannot be decompressed on Colab free tier.
3. **The Softmax Dimension Trap:** A single monolithic neural network outputting 10,000 logits requires a dense projection matrix of dimension $1280 \times 10,000$ (over 12.8 million parameters in the final layer alone). Training this under severe class imbalance produces logit bias, gradient instability, and slow convergence.

---

## 4. Scalable Multi-Stage Vision Architecture

To achieve large-scale plant recognition honestly without fabricating model capabilities, AGRO AI implements a **three-stage roadmap**:

```
[ Stage 1: Active Local Production ]
   ├── Vision Model: MobileNetV2 ONNX (14 Primary Agricultural Classes)
   ├── Calibration: Temperature Scaling (T=1.8) + Botanical Feature Alignment
   ├── Fallback / OOD: Reject Non-Agri / Ambiguous Photos -> Suggest 10,206 DB
   └── Directory Engine: 10,206 Verified Species (Sub-60ms Multilingual Search)

[ Stage 2: Colab Expansion (In Training Suite) ]
   ├── Notebook: training/plant_identification_colab.ipynb
   ├── Scope: 50–200 Publicly Available Indian Agricultural Species
   ├── Dataset: Token-Free Curated Public Archive (PlantVillage + Open Research)
   └── Export: Compatible plant_identifier.onnx + plant_classes.json

[ Stage 3: Deep Embedding & Vector Retrieval (10,000+ Species) ]
   ├── Vision Backbone: Self-Supervised Vision Transformer (DINOv2-small, 384-dim)
   ├── Metric Learning: Cosine Similarity / Triplet Loss on Species Prototypes
   └── Index: FAISS / HNSW Vector Index over 10,000+ Botanical Prototypes
       (Zero Dense Softmax Matrix Explosion; O(1) Incremental Class Addition)
```

### 4.1 Stage 1: Active Local Model (14 Agricultural Species)
The production FastAPI backend runs `plant_identifier.onnx` via `onnxruntime` with 0 external API dependencies:
1. `capsicum-annuum` (Bell Pepper / Shimla Mirch)
2. `citrus-sinensis` (Sweet Orange / Mosambi / Battayi)
3. `cucurbita-pepo` (Field Pumpkin / Squash)
4. `fragaria-ananassa` (Garden Strawberry)
5. `glycine-max` (Soybean)
6. `malus-domestica` (Apple / Seb)
7. `prunus-avium` (Sweet Cherry)
8. `prunus-persica` (Peach / Aadu)
9. `rubus-idaeus` (Red Raspberry)
10. `solanum-lycopersicum` (Tomato / Tamatar)
11. `solanum-tuberosum` (Potato / Aloo)
12. `vaccinium-corymbosum` (Highbush Blueberry)
13. `vitis-vinifera` (Grape / Angoor / Draksha)
14. `zea-mays` (Corn / Maize / Mokka Jonna)

### 4.2 Stage 2: Google Colab Training Workflow
The Colab training workflow in `training/plant_identification_colab.ipynb` operates with **zero API tokens**:
- Automatically downloads open research botanical archives.
- Preprocesses images into standard `(224, 224, 3)` RGB tensors normalized to $[0, 1]$.
- Trains MobileNetV2 with frozen base features, followed by fine-tuning of the top 30 convolutional blocks.
- Evaluates on a held-out 15% test set, generating per-class precision, recall, F1-scores, and confusion matrices.
- Exports compatible `plant_identifier.onnx`, `plant_identifier.keras`, and `plant_classes.json`.

### 4.3 Stage 3: Scalable Metric Learning for 10,000+ Species
For genuine recognition of 10,000+ species:
- Replace the classification softmax head with a **384-dimensional botanical feature extractor** (e.g. DINOv2-small or MobileNetV4 embedding backbone).
- Store prototype vectors for each species in the SQLite database or a lightweight FAISS index.
- New species can be enrolled by computing the average embedding of 5–10 verified photographs **without retraining the neural network**.

---

## 5. Plant Organ Diagnostic Scope & Honesty Framework

Visual identification accuracy varies fundamentally based on the plant organ photographed:

| Plant Organ | Visual Diagnostic Specificity | Model Support Status | Honesty Notice & Behavior |
|:---|:---:|:---:|:---|
| **Foliar Leaves (`leaf`)** | High (venation, margin, blade index) | Primary Training Domain | Full vision inference with morphological alignment. |
| **Floral Blossoms (`flower`)** | High (petal color, corolla geometry) | Secondary Domain (Partial) | Identified as floral; triggers calibrated uncertainty ($< 45\%$) and suggests verified flowering plants from the 10,206 catalog. |
| **Fleshy Fruits (`fruit`)** | High (pericarp, color, shape) | Supported for Fruiting Crops | Evaluates fruit pigment signatures (Tomato, Pepper, Strawberry). |
| **Stems & Woody Bark (`stem`)** | Low to Moderate | Lower Diagnostic Power | Flags lower specificity notice; advises cross-referencing leaf or canopy features. |
| **Subterranean Roots (`root`)** | Very Low (lacks foliar venation) | Out-of-Distribution | Explicitly marked Out-of-Distribution; suggests direct root/rhizome search in 10,000+ directory. |
| **Whole Canopy (`whole_plant`)** | Moderate | Evaluated for growth habit | Evaluates overall architecture and habit context. |

---

## 6. Mathematical Formulations for Calibrated Confidence

### 6.1 Temperature Scaling
Raw neural network softmax logits often suffer from extreme overconfidence:
$$z_i = \ln(\max(p_i, 10^{-7}))$$
Logits are scaled by temperature $T = 1.8$:
$$z'_i = \frac{z_i}{T}$$
Calibrated probabilities are recomputed:
$$p'_{calib, i} = \frac{\exp(z'_i - \max(z'))}{\sum_{j} \exp(z'_j - \max(z'))}$$

### 6.2 Botanical Morphological Alignment
For monocotyledonous cereals (*Zea mays*):
$$\text{Linear Blade Index} = \frac{\mu(|\partial g / \partial y|) + 10^{-4}}{\mu(|\partial g / \partial x|) + 10^{-4}}$$
When an elongated blade structure is observed ($\text{Index} > 0.45$ or $\text{Aspect Ratio} > 2.2$), monocot logits receive positive botanical alignment ($+1.4$). Broadleaf dicots encountering high linear blade values receive negative adjustments ($-0.9$).

### 6.3 Shannon Entropy for Out-of-Distribution Detection
Normalized prediction entropy measures classification uncertainty:
$$H_{norm} = \frac{-\sum_{i=1}^{K} p'_i \ln(p'_i)}{\ln(K)}$$
Confidence margin between the top two candidates:
$$\Delta = p'_{(1)} - p'_{(2)}$$
An image is designated **Ambiguous / Out-of-Distribution** if:
$$p'_{(1)} < 0.45 \quad \lor \quad H_{norm} > 0.60 \quad \lor \quad \Delta < 0.12 \quad \lor \quad \text{Organ} \in \{\text{root}, \text{stem}\}$$

When flagged, displayed top confidence is bounded ($< 45\%$), `isAmbiguous: true`, and the system automatically queries the 10,206 botanical directory to present genuine candidates rather than forcing an un-modeled image into a false prediction.
