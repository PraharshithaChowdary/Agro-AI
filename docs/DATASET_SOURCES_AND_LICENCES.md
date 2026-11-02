# AGRO AI — Dataset Sources, Licences, and Botanical Provenance

## 1. Ethical Data Governance & Licensing Principles

AGRO AI strictly relies on public domain, permissive Creative Commons, and open governmental data sources. No proprietary APIs, paywalled databases, or uncredited copyrighted photography are utilized.

All datasets referenced below adhere to open research standards with appropriate academic attribution.

---

## 2. Botanical Reference Databases & Checklists

| Source | Organization | Description | Applicable Licence | Official Access URL |
| :--- | :--- | :--- | :--- | :--- |
| **eFlora of India** | Botanical Survey of India (BSI) / eFlora Community | Comprehensive flora checklists covering North, South, East, and Western Ghats taxa | Open Educational / CC BY-NC-SA 4.0 | [efloras.org / efloraofindia](https://efloraofindia.com/) |
| **Indian Virtual Herbarium (IVH)** | Ministry of Environment, Forest and Climate Change (MoEFCC), Govt. of India | High-resolution digitized herbarium specimens and state distributions | Open Government Data (OGD) Licence India | [ivh.bsi.gov.in](https://ivh.bsi.gov.in/) |
| **Flowers of India** | FOI Team (Curated by Tabish Qureshi & Thingnam Girija) | Field photographs, vernacular names in 10+ Indian languages, flowering season | Open Educational Resource / Attribution | [flowersofindia.net](https://www.flowersofindia.net/) |
| **Ayurvedic Pharmacopoeia of India (API)** | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Standard medicinal properties, therapeutic uses, and official Sanskrit/vernacular names | Public Sector Information (Govt. of India) | [pcimh.gov.in](https://pcimh.gov.in/) |
| **World Flora Online (WFO)** | WFO Consortium / Royal Botanic Gardens Kew | Global consensus taxonomic classification and accepted binomials | CC0 / Open Access Data | [worldfloraonline.org](https://www.worldfloraonline.org/) |
| **Global Biodiversity Information Facility (GBIF)** | GBIF Secretariat | Geospatial occurrence records and regional Indian herbarium specimens | CC BY 4.0 / CC0 | [gbif.org](https://www.gbif.org/) |

---

## 3. Computer Vision & Plant Disease Datasets

| Dataset | Creators & Institution | Contents | Licence | Usage in AGRO AI |
| :--- | :--- | :--- | :--- | :--- |
| **PlantVillage** | David P. Hughes & Marcel Salathé (Penn State University & EPFL) | 54,303 leaf images across 14 crop species and 26 disease classes | Open Access (CC BY-SA 4.0) | Powers verified crop disease diagnosis models (Tomato, Potato, Corn, Apple, Grape, Pepper) |
| **PlantDoc** | Arunabh Singh et al. (IIT Delhi) | Real-world Indian field images of plant disease in unconstrained environments | Open Research (MIT / Academic) | In-field robustness validation and complex background benchmarking |
| **PlantCLEF** | LifeCLEF Initiative / Inria / CIRAD | Large-scale multi-organ plant identification benchmark (leaves, flowers, fruits, bark) | CC BY-SA 4.0 | Organ classification benchmarking and feature extractor validation |
| **Crop Pest and Disease Image Dataset (CPDID)** | Indian Council of Agricultural Research (ICAR) & State Agricultural Universities | Indigenous crop leaf images for Rice, Cotton, Wheat, Sugarcane, and Mango | Academic Fair Use / Open Access | Specific Indian pest symptom extraction profiles |

---

## 4. Attribution & Terms of Use

### PlantVillage
> Hughes, D. P., & Salathé, M. (2015). *An open access repository of images on plant health to enable the development of mobile disease diagnostics.* arXiv preprint arXiv:1511.08060.
> Distributed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

### PlantDoc
> Singh, A., et al. (2020). *PlantDoc: A Dataset for Visual Plant Disease Detection in the Wild.* Proceedings of the 7th ACM IKDD CoDS and 25th COMAD.
> Code and annotations made freely available for academic and agricultural research.

### Botanical Survey of India (BSI)
> Metadata derived from official publications of the Botanical Survey of India, Ministry of Environment, Forest and Climate Change, Government of India. Utilized under the National Data Sharing and Accessibility Policy (NDSAP).

---

## 5. Guidelines for Ingesting Additional Taxa (Scaling to 10,000 Species)

When adding new records to reach the 10,000 target:
1. **Verify Taxonomic Authority**: Every species must have a source citation linking to BSI, IPNI, or WFO.
2. **Attribution for Images**: Any local reference image stored in `backend/data/plant_images/` must record `author`, `license`, and `sourceUrl` in the `imageReferences` array.
3. **No Commercial Key Requirements**: Automated crawlers or scrapers must respect `robots.txt` and use cached open archives rather than querying public endpoints excessively.
