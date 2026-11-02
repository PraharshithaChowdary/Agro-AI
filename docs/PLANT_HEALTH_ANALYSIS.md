# AGRO AI — Plant Health Analysis Pipeline

## 1. Principles of Honest Agricultural Diagnostics

A fundamental pitfall of many mobile plant diagnostic apps is attempting to force an unstudied plant (e.g., *Tulsi*, *Moringa*, or *Teak*) into a disease classifier trained solely on *Tomato* or *Potato*, resulting in fabricated diagnoses such as *"Early Blight on Moringa"*.

AGRO AI implements a **Two-Tiered Honest Health Pipeline**:
1. **Tier 1: Observable Foliar Symptom Extraction**:
   - Universal feature extraction detecting real visual pathology regardless of species:
     - **Chlorosis (Yellowing %)**: Loss of chlorophyll, nitrogen deficiency, or viral mottling.
     - **Necrosis (Brown/Black Spotting %)**: Cell death, fungal leaf spot, or blight lesions.
     - **Powdery Mildew / Mold (White/Grey Coating %)**: Surface fungal mycelium.
     - **Dryness & Wilting %**: Dehydration, drought stress, or vascular wilt.
2. **Tier 2: Validated Disease Pathogen Classification**:
   - Executed **only** when the plant species matches one of the 13 verified crop models with trained, validated disease classes.
   - For all other species, the system returns observable symptom breakdown and cultural prevention advice without hallucinating pathogen labels.

---

## 2. Supported Crops with Verified Disease Models (13 Taxa)

| Crop Species | Scientific Name | Trained Pathogen Conditions |
| :--- | :--- | :--- |
| **Tomato** | *Solanum lycopersicum* | Healthy, Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus |
| **Potato** | *Solanum tuberosum* | Healthy, Early Blight (*Alternaria solani*), Late Blight (*Phytophthora infestans*) |
| **Rice (Paddy)** | *Oryza sativa* | Healthy, Bacterial Leaf Blight, Brown Spot, Leaf Smut, Blast |
| **Wheat** | *Triticum aestivum* | Healthy, Brown Rust, Yellow Rust, Stripe Rust, Septoria |
| **Cotton** | *Gossypium hirsutum* | Healthy, Bacterial Blight, Leaf Curl, Alternaria Leaf Spot |
| **Corn (Maize)** | *Zea mays* | Healthy, Common Rust, Gray Leaf Spot, Northern Leaf Blight |
| **Apple** | *Malus domestica* | Healthy, Apple Scab, Black Rot, Cedar Apple Rust |
| **Grape** | *Vitis vinifera* | Healthy, Black Rot, Esca (Black Measles), Leaf Blight (*Isariopsis*) |
| **Bell Pepper / Chilli** | *Capsicum annuum* | Healthy, Bacterial Spot |
| **Mango** | *Mangifera indica* | Healthy, Anthracnose, Powdery Mildew, Dieback |
| **Cucumber** | *Cucumis sativus* | Healthy, Downy Mildew, Powdery Mildew |
| **Eggplant (Brinjal)** | *Solanum melongena* | Healthy, Phomopsis Blight, Little Leaf |
| **Rose** | *Rosa spp.* | Healthy, Black Spot, Powdery Mildew |

---

## 3. Observable Symptom Calculation Methodology

Visual symptom percentages are calculated via computer vision color-space partitioning and texture gradients:

### 1. Chlorosis (Yellowing) Ratio
- Pixels where $R > 130$, $G > 130$, $B < 110$, and $(R + G) / 2 - B > 45$.
- Normalized against total foliage mask area to derive percentage severity.

### 2. Necrotic Spotting (Browning) Ratio
- Pixels where $R \in [50, 150]$, $G \in [30, 110]$, $B \in [20, 90]$, and $R > G > B$ with low overall luminance.

### 3. Powdery Coating (White Mildew) Ratio
- Pixels where $R > 180$, $G > 180$, $B > 180$, and saturation $S < 0.20$ within the leaf bounding region.

### 4. Overall Foliar Health Score
$$\text{Health Score} = \max\left(10, 100 - (\text{Chlorosis} \times 0.9 + \text{Necrosis} \times 1.2 + \text{Mildew} \times 1.5)\right)$$

Categorized into:
- **Optimal / Healthy** ($\ge 85\%$)
- **Mild Stress** ($65\% - 84\%$)
- **Moderate Stress** ($40\% - 64\%$)
- **Severe Stress** ($< 40\%$)

---

## 4. Structured Agronomic Recommendations

Every health analysis produces actionable, categorized guidance:
- **Action**: Immediate cultural remedy (e.g., prune diseased lower foliage, improve drainage).
- **Organic**: Bio-pesticides and natural interventions (e.g., Neem oil spray 5 ml/L, Trichoderma viride soil application).
- **Chemical**: Standard university-recommended fungicides/insecticides (e.g., Copper oxychloride, Mancozeb) with safety warnings.
- **Prevention**: Crop rotation, resistant varieties, optimal spacing.
- **Info**: Agronomic context regarding weather triggers (e.g., high humidity above 85%).
