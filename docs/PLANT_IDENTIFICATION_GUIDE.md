# AGRO AI — Indian Plant Identification System Guide

## 1. Overview

The **Indian Plant Explorer & Identification System** is an AI-powered diagnostic and botanical discovery engine tailored for Indian agricultural crops, horticultural plants, Ayurvedic medicinal flora, and endemic trees. 

The system supports two complementary identification workflows:
- **Mode A (Automatic Vision Identification)**: Predicts the plant species solely from an uploaded or captured photograph, providing ranked top-5 candidate matches, visual morphological evidence, and calibrated prediction uncertainty.
- **Mode B (Name-Assisted Consistency Verification)**: Takes an entered common or scientific name (with instant autocomplete across 98+ seed species and 10,000 target taxa) alongside a photograph, verifying whether the image morphology is consistent with the claimed species.

In addition, users can seamlessly transition any identification result into the **Dedicated Plant Foliar Health Analyzer**.

---

## 2. Supported Plant Organs

To optimize identification accuracy across different developmental stages and plant families, the vision pipeline supports five organ selection modes:

| Organ | Recommended Visual Features | Ideal Lighting & Framing |
| :--- | :--- | :--- |
| **Leaf / Foliage** | Entire leaf blade, margin serration, venation pattern, petiole | Flat surface or natural stem attachment; avoid motion blur |
| **Flower / Inflorescence** | Petal count, color gradient, stamen/pistil structure, floral symmetry | Close macro shot, high contrast against green foliage |
| **Fruit / Pod / Grain** | Surface texture, shape, color ripeness, calyx/stem junction | Sharp focus, natural daylight, isolated from dense background |
| **Bark / Stem / Trunk** | Bark furrow depth, lenticels, color, thorns/spines | 1–2 feet distance perpendicular to the trunk |
| **Whole Plant / Canopy** | Overall architecture, branching habit, height perspective | Stand 3–6 feet away to capture base, canopy, and habit |

---

## 3. Best Practices for Photography

To achieve maximum confidence and prevent ambiguous classifications:

1. **Natural Daylight**: Photograph during daylight hours (avoid harsh direct noon glare and dim twilight).
2. **Sharp Focus**: Tap your camera screen on the primary botanical feature (e.g., leaf margin or flower center) rather than background soil or weeds.
3. **Single Species per Frame**: Isolate the plant of interest. Multi-crop intercropping frames can confuse visual feature extractors.
4. **Avoid Non-Agricultural Objects**: The built-in agricultural relevance safety filter rejects non-plant images (e.g., automobiles, furniture, human faces, pets) with an honest guidance prompt.
5. **Multiple Angles**: If unsure of top candidate #1, capture a flower or fruit photo in addition to a leaf photo.

---

## 4. Understanding Identification Outputs

### Top Candidate & Ranked Top-5 Distribution
The model outputs a ranked list of the top 5 most probable species:
- **Confidence Score (%)**: Posterior probability calibrated via Platt scaling (`CalibratedClassifierCV`).
- **Rank 1 Candidate**: The primary botanical hypothesis.
- **Alternative Candidates (Ranks 2–5)**: Displayed alongside their relative probability to ensure transparent decision-making.

### Calibrated Uncertainty & Ambiguity Detection
Rather than making overconfident guesses on unfamiliar foliage, the system computes **Shannon entropy** across the probability distribution:
$$H(p) = -\sum_{i=1}^{K} p_i \log_2(p_i)$$
- **Low Entropy ($H < 1.5$)**: The prediction is decisive; top candidate confidence is strong ($> 65\%$).
- **High Entropy / Close Margins**: If the margin between candidate #1 and #2 is $< 10\%$, or the maximum confidence is $< 30\%$, the system flags an **Ambiguity Warning**:
  > *"Visual features share close morphological characteristics between [Species A] and [Species B]. Examine floral structure or verify regional names before field application."*

### Visual Evidence Breakdown
Every prediction includes extracted visual descriptors:
- Foliage color balance (e.g., chlorophyll green saturation, anthocyanin red tint).
- Edge texture complexity and venation density.
- Brightness and contrast profile.
- Organ alignment and morphological shape cues.

---

## 5. Mode B: Name-Assisted Consistency Verification

When a farmer or researcher already suspects a plant's identity (e.g., *"This is Moringa / Drumstick"*):
1. Enter the common name, scientific name, or regional name in Hindi/Telugu/Tamil into the input field.
2. The autocomplete dropdown displays matching verified species records.
3. The engine checks:
   - Does the image morphology match the targeted species' leaf shape, margin, and color profile?
   - Is the species present among the top ranked candidates from vision analysis?
4. **Result**:
   - **Consistent**: The image exhibits visual characteristics concordant with the claimed taxon.
   - **Incongruent / Doubtful**: The visual features diverge significantly (e.g., uploading grass foliage while claiming *"Mango"*). A polite alert highlights the discrepancy.

---

## 6. Seamless Transition to Foliar Health Analysis

From any identified plant card:
- Click **"Analyse Plant Health for this Species"**.
- The system automatically transfers the verified species name into the **Plant Health Analyzer**.
- If the species matches one of our 13 trained crop disease models (Tomato, Potato, Rice, Wheat, Cotton, Mango, Cucumber, Apple, Grape, Pepper, Rose, Brinjal, Corn), deep pathogen classification is performed.
- For other species, observable foliar symptom extraction (chlorosis %, necrotic lesions %, powdery mildew %, dehydration %) is computed alongside 5 species-tailored cultural management steps.

---

## 7. Safety & Agronomic Disclaimers

> [!IMPORTANT]
> - **Visual AI Assistance Only**: Image-based identification is an assistive agronomic tool, not a certified taxonomic authority.
> - **Never Ingest Wild Plants**: Never consume wild herbs, berries, or roots based solely on computer vision predictions.
> - **Field Verification**: For commercial pesticide, fungicide, or herbicide applications, always cross-verify symptoms with your local Krishi Vigyan Kendra (KVK) or State Agricultural University extension officer.
