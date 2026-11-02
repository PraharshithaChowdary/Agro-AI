# AGRO AI — Large-Scale Botanical Dataset & Training Pipeline

This directory contains the dataset preparation, validation, and training infrastructure for AGRO AI's visual plant identification system.

---

## 1. Dataset Preparation & Validation Pipeline (`dataset_pipeline.py`)

The pipeline in [`training/dataset_pipeline.py`](file:///c:/Users/praha/Desktop/PDD%20AGRO%20AI/training/dataset_pipeline.py) provides:
- **Canonical Species Normalization:** Automatically maps varied raw folder names (e.g. `Neem (Azadirachta indica)`, `Tulsi`, `Mango Tree Leaves`, `Roses`, `Corn_(maize)___healthy`) into standard binomial slugs (`azadirachta-indica`, `ocimum-tenuiflorum`, `mangifera-indica`, `rosa-indica`, `zea-mays`).
- **Data Integrity & Corrupt Image Check:** Validates every image file using Pillow (`img.verify()`) to reject truncated, corrupted, or non-decodable files.
- **Cryptographic Duplicate Elimination:** Computes MD5 content hashes to eliminate exact duplicate images within classes.
- **Minimum Class Size Enforcement:** Filters out empty classes or classes with fewer than 20 genuine images.
- **Stratified Train / Val / Test Splitting:** Creates strictly partitioned Train (70%), Validation (15%), and Test (15%) splits with a deterministic random seed (`42`).
- **Exact Class Mapping Export:** Generates the matching [`plant_classes.json`](file:///c:/Users/praha/Desktop/PDD%20AGRO%20AI/backend/models/plant_classes.json) during dataset creation to ensure 100% mathematical alignment with model outputs.

### CLI Usage:
```bash
# Audit an existing dataset folder
python training/dataset_pipeline.py --audit /path/to/dataset

# Import raw downloaded folders and organize into canonical species slugs
python training/dataset_pipeline.py --organize-from /path/to/raw_folders --target-dir datasets/plant_species_organized

# Create stratified Train (70%), Val (15%), Test (15%) splits
python training/dataset_pipeline.py --split-from datasets/plant_species_organized --split-to datasets/plant_species_split
```

---

## 2. Google Colab GPU Training Workflow (`plant_identification_colab.ipynb`)

The training workflow is pre-packaged in [`training/plant_identification_colab.ipynb`](file:///c:/Users/praha/Desktop/PDD%20AGRO%20AI/training/plant_identification_colab.ipynb).

### Target Training Batch (40–60 Verified Species):
- **Indian Medicinal & Tree Flora:** Neem (*Azadirachta indica*), Tulsi (*Ocimum tenuiflorum*), Mango (*Mangifera indica*), Guava (*Psidium guajava*), Mint (*Mentha arvensis*), Peepal (*Ficus religiosa*), Banyan (*Ficus benghalensis*), Hibiscus (*Hibiscus rosa-sinensis*), Papaya (*Carica papaya*), Lemon (*Citrus limon*), Pomegranate (*Punica granatum*), Aloe Vera (*Aloe barbadensis*), Jamun (*Syzygium cumini*), Curry Leaf (*Murraya koenigii*), Amla (*Emblica officinalis*), Drumstick (*Moringa oleifera*), Betel (*Piper betle*), Periwinkle (*Catharanthus roseus*).
- **Agricultural Crops:** Corn / Maize (*Zea mays*), Tomato (*Solanum lycopersicum*), Potato (*Solanum tuberosum*), Bell Pepper (*Capsicum annuum*), Sweet Orange (*Citrus sinensis*), Apple (*Malus domestica*), Grape (*Vitis vinifera*), Soybean (*Glycine max*), Squash (*Cucurbita pepo*), Strawberry (*Fragaria ananassa*), Peach (*Prunus persica*), Cherry (*Prunus avium*), Blueberry (*Vaccinium corymbosum*), Raspberry (*Rubus idaeus*).
- **Flowers:** Rose (*Rosa indica*), Sunflower (*Helianthus annuus*), Marigold (*Tagetes erecta*), Jasmine (*Jasminum sambac*), Lotus (*Nelumbo nucifera*).

### Step-by-Step Execution in Google Colab:
1. Open [Google Colab](https://colab.research.google.com).
2. Click **File -> Upload notebook** and select `training/plant_identification_colab.ipynb`.
3. Set the hardware accelerator to **T4 GPU**:
   `Runtime -> Change runtime type -> Hardware accelerator -> T4 GPU` -> Click **Save**.
4. Run all cells sequentially (`Runtime -> Run all` or press `Ctrl + F9`).
5. The notebook will:
   - Automatically download the open PlantVillage dataset and Indian Medicinal Plants dataset (zero API keys, zero login).
   - Audit, deduplicate, and normalize folder names into 40–60 canonical species classes.
   - Partition into 70% Train, 15% Validation, and 15% Test.
   - Train MobileNetV2 with two-stage transfer learning (frozen base, followed by top 35-layer fine-tuning).
   - Evaluate on the unseen holdout test set, reporting Top-1/Top-5 accuracy, per-class Precision/Recall/F1, and confusion matrix.
   - Export universal ONNX and Keras weights.
6. The notebook will prompt you to download three files:
   - `plant_identifier.onnx`
   - `plant_classes.json`
   - `plant_identifier.keras`
7. Place `plant_identifier.onnx` and `plant_classes.json` into your local project at:
   - `backend/models/plant_identifier.onnx`
   - `backend/models/plant_classes.json`
8. Restart your local FastAPI backend.

---

## 3. Preserving Application Integrity

- The **10,206-species botanical catalog** in SQLite (`backend/agro_ai.db`) and multilingual autocomplete remain fully functional and completely independent of visual model size.
- The existing **14-class ONNX model** remains active in `backend/models/` until you train and drop in the replacement 40–60 class model from Colab.
- Any unmodeled or uncertain species uploaded to the vision endpoint is honestly flagged as `isAmbiguous: true` with suggested matches from the 10,206-species catalog.
