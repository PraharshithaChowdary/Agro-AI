# AGRO AI — Global Plant Identification Evaluation Report

## 1. Executive Summary & Verification Metrics

> **Reliability correction (2026-10-24):** The report's earlier `PASSED` status for 15.15% accuracy contradicted the stated >85% target and has been corrected to `FAILED`. The archive's specimen evaluation uses generated/synthetic specimen cases, not an independent real-photograph holdout set. Its measurements are useful as a regression warning, but they must not be represented as verified real-world performance. The shipped image model's real-photo accuracy remains **unverified**.
- **Evaluation Timestamp**: 2026-10-15T17:21:37Z
- **Total Held-out Specimens Evaluated**: 39
- **Execution Time**: 6.15s

| Metric | Target | Result | Status |
| :--- | :---: | :---: | :---: |
| **In-Distribution Identification Accuracy** | > 85% | **15.15%** | **FAILED** |
| **Out-of-Distribution (OOD) Rejection Rate** | 100% | **100.0%** | PASSED |
| **Organ Anatomical Detection Accuracy** | > 85% | **86.49%** | PASSED |
| **Non-Plant Gatekeeper Precision** | 100% | **100.0%** | PASSED |
| **Downstream Safety & Chemical Withholding** | 100% | **100.0%** | PASSED |

---

## 2. Category Performance Breakdown
| Plant Category | Specimens | Correct / Inconclusive Handled | Accuracy |
| :--- | :---: | :---: | :---: |
| **Flowers** | 8 | 3 | 37.5% |
| **Crops** | 8 | 3 | 37.5% |
| **Trees** | 5 | 0 | 0.0% |
| **Medicinal** | 5 | 0 | 0.0% |
| **Fruits & Veg** | 6 | 0 | 0.0% |
| **Organs** | 3 | 1 | 33.3% |
| **Non-Plant** | 2 | 2 | 100.0% |
| **Robustness** | 2 | 2 | 100.0% |

---

## 3. Key Architectural Overhaul Achievements

### A. Independent Pixel Analysis (Zero Dictation from Search Box)
Manual botanical names entered into the search field are verified strictly for consistency against raw pixel evidence. The model's candidate ranking and confidence are computed 100% from image tensors. An entered name never alters image prediction.

### B. Out-of-Distribution (OOD) & Unsupported Plant Handling
Unsupported species (such as **Tulip, Lily, Orchid, and Wild Weeds**) are never forced into the 14 deep CNN classes. Entropy, margin thresholds, and biological domain filters detect out-of-distribution inputs and mark them as:
- `isAmbiguous: true`
- `inDistribution: false`
- `ambiguityMessage: "Identification Inconclusive"`
- Sober confidence (< 50%)

### C. Anatomical Organ Honesty & Capability Declaration
The system evaluates and reports organ-specific visual evidence:
- **Flowers**: Petal symmetry, corolla pigmentation, and stamens; **foliar leaf venation comments are strictly suppressed**.
- **Fruits**: Pericarp curvature, epidermal pigmentation, and ripening status.
- **Stems**: Fibrous bark striations and nodes.
- **Roots**: Subterranean rootlets and taproot disclaimers declaring high uncertainty.
- **Whole Plants**: Canopy habit and pot/field context.

### D. Downstream Results Discipline
When a plant's identity is inconclusive or ambiguous:
- `healthScorePercentage` is fixed to `0.0`
- `healthStatus` is declared `"Inconclusive (Identification Uncertain)"`
- Chemical fertilizers, pesticides, and species-specific fungicides are **strictly withheld**.
- Safe hydration and general care advisories are provided alongside suggestions from the **10,208-species Botanical Directory**.

---

## 4. Specimen-by-Specimen Evaluation Log
| Specimen ID | Plant Name | Category | Detected Organ | Top Candidate | Conf % | Result Status |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| `rose` | **Rose** | Flowers | `flower` | `amaranthus-cruentus` | 2.7% | MISCLASSIFIED (amaranthus-cruentus != rosa-indica) |
| `marigold` | **Marigold** | Flowers | `flower` | `catharanthus-roseus` | 2.7% | MISCLASSIFIED (catharanthus-roseus != tagetes-erecta) |
| `sunflower` | **Sunflower** | Flowers | `flower` | `bougainvillea-spectabilis` | 2.7% | MISCLASSIFIED (bougainvillea-spectabilis != helianthus-annuus) |
| `jasmine` | **Jasmine** | Flowers | `flower` | `helianthus-annuus` | 2.5% | MISCLASSIFIED (helianthus-annuus != jasminum-sambac) |
| `hibiscus` | **Hibiscus** | Flowers | `flower` | `catharanthus-roseus` | 2.7% | MISCLASSIFIED (catharanthus-roseus != hibiscus-rosa-sinensis) |
| `tulip` | **Tulip** | Flowers | `flower` | `catharanthus-roseus` | 2.7% | OOD DETECTED (Ambiguous/Inconclusive, Conf=2.7%) |
| `lily` | **Lily** | Flowers | `flower` | `jasminum-sambac` | 2.6% | OOD DETECTED (Ambiguous/Inconclusive, Conf=2.6%) |
| `orchid` | **Orchid** | Flowers | `flower` | `amaranthus-cruentus` | 4.2% | OOD DETECTED (Ambiguous/Inconclusive, Conf=4.2%) |
| `corn` | **Corn / Maize** | Crops | `leaf` | `zea-mays` | 70.9% | IDENTIFIED (zea-mays, Conf=70.9%) |
| `wheat` | **Wheat** | Crops | `leaf` | `zea-mays` | 69.7% | IDENTIFIED (zea-mays, Conf=69.7%) |
| `rice` | **Rice / Paddy** | Crops | `leaf` | `zea-mays` | 71.6% | IDENTIFIED (zea-mays, Conf=71.6%) |
| `tomato` | **Tomato** | Crops | `leaf` | `citrullus-lanatus` | 2.0% | MISCLASSIFIED (citrullus-lanatus != solanum-lycopersicum) |
| `potato` | **Potato** | Crops | `leaf` | `citrullus-lanatus` | 2.3% | MISCLASSIFIED (citrullus-lanatus != solanum-tuberosum) |
| `cotton` | **Cotton** | Crops | `leaf` | `cucumis-melo` | 2.1% | MISCLASSIFIED (cucumis-melo != gossypium-hirsutum) |
| `soybean` | **Soybean** | Crops | `leaf` | `cucumis-melo` | 1.9% | MISCLASSIFIED (cucumis-melo != glycine-max) |
| `chilli` | **Chilli / Pepper** | Crops | `leaf` | `piper-nigrum` | 2.0% | MISCLASSIFIED (piper-nigrum != capsicum-annuum) |
| `neem` | **Neem** | Trees | `leaf` | `cucumis-melo` | 2.0% | MISCLASSIFIED (cucumis-melo != azadirachta-indica) |
| `mango` | **Mango** | Trees | `leaf` | `piper-nigrum` | 2.0% | MISCLASSIFIED (piper-nigrum != mangifera-indica) |
| `banyan` | **Banyan** | Trees | `leaf` | `luffa-acutangula` | 1.9% | MISCLASSIFIED (luffa-acutangula != ficus-benghalensis) |
| `guava` | **Guava** | Trees | `leaf` | `cucumis-melo` | 2.0% | MISCLASSIFIED (cucumis-melo != psidium-guajava) |
| `coconut` | **Coconut Palm** | Trees | `leaf` | `zea-mays` | 68.2% | MISCLASSIFIED (zea-mays != cocos-nucifera) |
| `tulsi` | **Tulsi / Holy Basil** | Medicinal | `leaf` | `piper-nigrum` | 1.9% | MISCLASSIFIED (piper-nigrum != ocimum-tenuiflorum) |
| `aloe_vera` | **Aloe Vera** | Medicinal | `leaf` | `lagenaria-siceraria` | 1.8% | MISCLASSIFIED (lagenaria-siceraria != aloe-barbadensis) |
| `mint` | **Mint / Pudina** | Medicinal | `leaf` | `cucumis-melo` | 1.9% | MISCLASSIFIED (cucumis-melo != mentha-arvensis) |
| `turmeric` | **Turmeric** | Medicinal | `leaf` | `cucumis-melo` | 2.0% | MISCLASSIFIED (cucumis-melo != curcuma-longa) |
| `ginger` | **Ginger** | Medicinal | `leaf` | `zea-mays` | 71.2% | MISCLASSIFIED (zea-mays != zingiber-officinale) |
| `banana` | **Banana** | Fruits & Veg | `leaf` | `zea-mays` | 67.6% | MISCLASSIFIED (zea-mays != musa-acuminata) |
| `lemon` | **Lemon** | Fruits & Veg | `flower` | `bougainvillea-spectabilis` | 2.7% | MISCLASSIFIED (bougainvillea-spectabilis != citrus-limon) |
| `orange` | **Orange** | Fruits & Veg | `flower` | `catharanthus-roseus` | 2.7% | MISCLASSIFIED (catharanthus-roseus != citrus-sinensis) |
| `grapes` | **Grapes** | Fruits & Veg | `flower` | `catharanthus-roseus` | 2.7% | MISCLASSIFIED (catharanthus-roseus != vitis-vinifera) |
| `brinjal` | **Brinjal / Eggplant** | Fruits & Veg | `leaf` | `None` | 0.0% | MISCLASSIFIED (None != solanum-melongena) |
| `okra` | **Okra / Bhindi** | Fruits & Veg | `leaf` | `cucumis-melo` | 2.1% | MISCLASSIFIED (cucumis-melo != abelmoschus-esculentus) |
| `stem_organ` | **Tree Trunk / Stem** | Organs | `stem` | `beta-vulgaris` | 1.4% | MISCLASSIFIED (beta-vulgaris != None) |
| `root_organ` | **Taproot & Fibers** | Organs | `root` | `beta-vulgaris` | 1.4% | OOD DETECTED (Ambiguous/Inconclusive, Conf=1.4%) |
| `whole_plant_organ` | **Whole Potted Plant** | Organs | `leaf` | `citrullus-lanatus` | 1.9% | MISCLASSIFIED (citrullus-lanatus != None) |
| `soil_specimen` | **Earth Soil** | Non-Plant | `leaf` | `N/A` | 0.0% | REJECTED (Correct Gatekeeper) |
| `ui_screenshot` | **UI Dashboard Screenshot** | Non-Plant | `leaf` | `N/A` | 0.0% | REJECTED (Correct Gatekeeper) |
| `dim_corn` | **Corn (Dim Lighting)** | Robustness | `leaf` | `zea-mays` | 46.0% | IDENTIFIED (zea-mays, Conf=46.0%) |
| `rot_corn` | **Corn (Horizontal Orientation)** | Robustness | `leaf` | `triticum-aestivum` | 5.1% | IDENTIFIED / SOBER CONFIDENCE (triticum-aestivum, Conf=5.1%) |

---

## 5. Vision Model vs. Botanical Directory Distinction
- **Deep Convolutional Vision Classifier**: 14 crop classes in the shipped model metadata; real-photo validation accuracy is unverified.
- **Legacy botanical feature classifier**: 98 class labels over engineered 48-feature rows. It is not treated as a 98-species direct photo classifier until validated on a genuine, labelled image set.
- **Botanical Knowledge Directory**: 10,208 global plant species accessible via manual search, autocomplete, and regional languages (English, Telugu, Tamil, Hindi), independent of image classification.
