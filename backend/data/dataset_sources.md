# AGRO AI — Indian Botanical & Plant Vision Dataset Sources and Licences

This document provides complete documentation of authoritative taxonomic and computer vision datasets used for the **Indian Plant Explorer & Health Analyzer** in AGRO AI.

---

## 🏛️ 1. Authoritative Indian Botanical Databases

| Source | Official URL | Authority | Scope & Description | Access & Licence Terms |
|---|---|---|---|---|
| **India Flora Online** | [indiaflora-ces.iisc.ac.in](https://indiaflora-ces.iisc.ac.in/) | Centre for Ecological Sciences (CES), Indian Institute of Science (IISc), Bangalore | Comprehensive digital flora portal covering vascular flora across peninsular India and Western Ghats. Verified taxonomic descriptions, distribution, and phenology. | Academic & educational open reference; respect crawler politeness and attribution. |
| **eFlora of India** | [efloraofindia.com](https://efloraofindia.com/) | Citizen science initiative affiliated with Indian botanical taxonomy community | Crowdsourced repository documenting >14,000 Indian plant taxa with regional names in Telugu, Tamil, Hindi, Kannada, Malayalam, Marathi, and Bengali. | Creative Commons Attribution-NonCommercial (CC BY-NC 4.0). Requires photographer/contributor attribution. |
| **Botanical Survey of India (BSI)** | [bsi.gov.in](https://bsi.gov.in/) | Ministry of Environment, Forest and Climate Change (MoEFCC), Govt. of India | National apex taxonomic authority. Official custodian of Flora of India fascicles, State floras, and Red Data Book of Indian Plants. | Govt. of India open government data access; non-commercial educational reuse permitted with official citation. |
| **Indian Virtual Herbarium (IVH)** | [ivh.bsi.gov.in](https://ivh.bsi.gov.in/) | Botanical Survey of India | Digital repository housing >100,000 digitized herbarium specimen sheets with barcoding, high-resolution scans, type specimens, and provenance. | Official government portal; open for research viewing, metadata indexing with BSI herbarium accession citations. |
| **ICAR & Agricultural Universities** | [icar.org.in](https://icar.org.in/) | Indian Council of Agricultural Research (ICAR), IARI, TNAU, UAS Bangalore | Agronomic growing recommendations, crop disease thresholds, and regional package of practices across Indian agro-climatic zones. | Public agronomic advisory documentation. |

---

## 📸 2. Computer Vision & Plant Disease Datasets

| Dataset | Provider / Source | Image Count | Classes & Focus | Licence |
|---|---|---|---|---|
| **PlantVillage** | Hughes & Salathé / Penn State ([GitHub Repo](https://github.com/spMohanty/PlantVillage-Dataset)) | 54,303 leaf images | 38 crop & disease classes including Tomato, Potato, Corn, Apple, Grape, Pepper, Strawberry | Creative Commons Zero (CC0 1.0 Universal) / Public Domain |
| **PlantCLEF (LifeCLEF)** | ImageCLEF Consortium ([imageclef.org](https://www.imageclef.org/node/332)) | Multi-million botanical images | Global plant identification challenge covering leaves, flowers, fruits, stems, and whole habits | Research and educational evaluation use under challenge terms |
| **PlantDoc** | IIT Delhi ([GitHub Repo](https://github.com/pratik2901/PlantDoc-Dataset)) | 2,598 field images | Real-world in-situ field leaf images across 13 plant species and 17 diseases | MIT License / Open Academic Research |
| **Botanical Garden & Field Flora Collections** | AGRO AI Project Curated Samples | High-resolution field photos | Verified Indian crops, Ayurvedic medicinal plants (Tulsi, Neem, Aloe Vera), fruits (Mango, Papaya, Guava), spices | CC BY 4.0 / AGRO AI Project Open Data |

---

## ⚖️ 3. Data Ingestion & Ethical Guidelines

1. **No Bulk Unsolicited Scraping**: All data ingest pipelines follow `robots.txt` guidelines and do not perform unauthorized scraping of protected portals.
2. **Stable Taxonomic Identifiers**: Scientific names are verified against the accepted binomials in the World Checklist of Vascular Plants (WCVP) / Plants of the World Online (POWO) and BSI checklists.
3. **Regional Vernacular Integrity**: Vernacular names in Telugu (తెలుగు), Tamil (தமிழ்), Hindi (हिन्दी), and other Indian scripts are cross-verified and never automatically hallucinated.
4. **Honest Uncertainty & Verification Flags**: Plant records have strict `verification_status` flags (`verified`, `provisional`, `pending_review`). Unverified attributes are explicitly left as `unknown`.
5. **Separation of Species ID and Disease Diagnosis**: Plant species identification models are isolated from pathogen/disease models to avoid misleading diagnoses on unsupported species.
