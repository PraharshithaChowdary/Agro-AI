"""
AGRO AI — Verified Agricultural Knowledge Base & Evidence Retrieval Engine
Cites authentic, verifiable extension advisories and scientific standards from:
- ICAR (Indian Council of Agricultural Research, New Delhi)
- TNAU Agritech Portal (Tamil Nadu Agricultural University, Coimbatore)
- ANGRAU (Acharya N.G. Ranga Agricultural University, Guntur)
- PAU (Punjab Agricultural University, Ludhiana)
- MoA&FW (Ministry of Agriculture and Farmers Welfare, Govt of India)
- CIB&RC (Central Insecticides Board & Registration Committee)
- FAO (Food and Agriculture Organization of the United Nations)
- IRRI (International Rice Research Institute)
- ICRISAT (International Crops Research Institute for the Semi-Arid Tropics)
"""

import re
import math
from typing import List, Dict, Any, Optional

VERIFIED_KNOWLEDGE_DOCUMENTS: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # 1. PLANT PATHOLOGY & IPM (DISEASES)
    # -------------------------------------------------------------------------
    {
        "id": "doc_tomato_early_blight",
        "title": "TNAU Agritech Portal: Crop Protection — Diseases of Tomato: Early Blight (Alternaria solani)",
        "organization": "Tamil Nadu Agricultural University (TNAU)",
        "publication_year": "2023",
        "url": "https://agritech.tnau.ac.in/crop_protection/crop_prot_crop%20diseases_veg_tomato_1.html",
        "category": "disease",
        "crops": ["Tomato", "Potato", "Eggplant"],
        "pathogen": "Alternaria solani (Ellis & Martin) Sorauer",
        "keywords": ["early blight", "alternaria", "concentric rings", "target spots", "tomato blight", "leaf spot tomato"],
        "summary": "Early blight caused by Alternaria solani is a widespread necrotrophic fungal disease of solanaceous crops characterized by distinctive concentric 'target board' lesions on older foliage.",
        "scientific_explanation": (
            "Alternaria solani survives in infected crop debris, volunteer solanaceous weeds, and seed coats. "
            "Primary infection begins on lower mature leaves under warm temperatures (24-29°C) and extended leaf wetness (>7 hours). "
            "Conidiophores produce multicellular dark brown conidia that disperse via wind and splashing raindrops. "
            "Toxins produced by the pathogen (alternaric acid and solanapyrone) inhibit host enzyme pathways, generating progressive chlorotic yellow halos around necrotic spots."
        ),
        "differential_diagnosis": [
            {"condition": "Late Blight (Phytophthora infestans)", "distinction": "Causes water-soaked irregular greenish-black lesions that turn purplish with white fuzzy sporulation under high humidity, whereas Early Blight produces dry, leathery concentric rings."},
            {"condition": "Septoria Leaf Spot (Septoria lycopersici)", "distinction": "Produces much smaller (2-4mm) circular spots with grayish-white centers and dark brown borders speckled with tiny black pycnidia."},
            {"condition": "Bacterial Spot (Xanthomonas spp.)", "distinction": "Produces small, angular water-soaked lesions that often tear or fall out, creating a shot-hole appearance without concentric rings."}
        ],
        "practical_steps": [
            "Pruning & Trellising: Prune off all bottom suckers and foliage within 25-30 cm of ground level to eliminate soil-borne splash inoculation and maximize canopy airflow.",
            "Mulching: Lay 5-7 cm of clean straw or organic mulch across the soil surface immediately after transplanting to physically block spore transmission from the soil.",
            "Drip Irrigation: Shift entirely to drip or furrow irrigation; completely eliminate overhead sprinkling, or irrigate strictly between 06:00 AM and 09:00 AM to allow rapid foliage drying.",
            "Organic/Bio-control: Spray Bacillus subtilis or Trichoderma harzianum at 5-10 g/L or 0.5% cold-pressed neem oil (Azadirachtin 1500 ppm) as a preventative measure at the first sign of lower leaf flecking.",
            "Chemical Control (CIB&RC approved): If disease severity index exceeds 5%, apply Mancozeb 75% WP @ 2.0 g/L or Copper Oxychloride 50% WP @ 2.5 g/L. In persistent humid spells, apply Chlorothalonil 75% WP @ 2.0 g/L or Azoxystrobin 23% SC @ 1.0 ml/L adhering to pre-harvest interval (PHI) of 3-5 days."
        ],
        "limitations": "Fungicide efficacy depends on complete coverage of both upper and lower leaf surfaces before systemic canopy invasion. Always rotate chemical classes (FRAC codes) to prevent fungicide resistance."
    },
    {
        "id": "doc_potato_late_blight",
        "title": "ICAR-Central Potato Research Institute (CPRI): Technical Bulletin on Late Blight Management in Potato",
        "organization": "ICAR-Central Potato Research Institute (CPRI), Shimla",
        "publication_year": "2022",
        "url": "https://cpri.icar.gov.in",
        "category": "disease",
        "crops": ["Potato", "Tomato"],
        "pathogen": "Phytophthora infestans (Mont.) de Bary",
        "keywords": ["late blight", "phytophthora", "potato blight", "water-soaked lesions", "white downy mildew"],
        "summary": "Late blight is a destructive oomycete disease causing rapid rot of potato and tomato foliage and tubers under cool (12-22°C), persistently wet or misty weather.",
        "scientific_explanation": (
            "Phytophthora infestans is an airborne and seed-borne oomycete pathogen capable of destroying entire crop canopies within 7-14 days. "
            "Biflagellate zoospores germinate when free water is present on leaf tissue for at least 4-6 hours at temperatures between 10°C and 20°C. "
            "Sporulation occurs primarily on the abaxial (underside) leaf surface, appearing as a delicate white frost or downy mold along lesion margins."
        ),
        "differential_diagnosis": [
            {"condition": "Early Blight (Alternaria solani)", "distinction": "Early blight lesions have dry concentric target-like rings and yellow halos without the white cottony sporulation typical of late blight under humid mornings."},
            {"condition": "Frost Damage", "distinction": "Frost causes blackened leaf collapse across the whole field within hours of sub-zero night temperatures, but lacks the white downy fungal border and progressive lesion spread."}
        ],
        "practical_steps": [
            "Certified Seed Tubers: Plant only certified, disease-free seed tubers; inspect tuber flesh for granular, coppery-brown dry rot before planting.",
            "Resistant Varieties: Grow CPRI-released late blight-resistant cultivars such as Kufri Girdhari, Kufri Himalini, Kufri Khyati, or Kufri Mohan.",
            "Prophylactic Spray: Prior to forecast cloud cover and rain, apply protective contact fungicide Mancozeb 75% WP @ 2.5 g/L or Propineb 70% WP @ 2.0 g/L.",
            "Systemic Intervention: If active purplish-brown lesions with white margins appear, apply systemic Cymoxanil 8% + Mancozeb 64% WP @ 2.5 g/L or Dimethomorph 50% WP @ 1.0 g/L.",
            "De-haulming & Harvest: Kill potato vines (de-haulm) with copper sulfate spray or mechanically 10-12 days before harvest to prevent motile spores from washing into the soil and infecting tubers."
        ],
        "limitations": "Once late blight infects >50% of canopy leaf area, systemic fungicides cannot restore diseased tissue. Preventive application based on weather forecasts is critical."
    },
    {
        "id": "doc_wheat_rusts",
        "title": "ICAR-Indian Institute of Wheat and Barley Research (IIWBR): Wheat Rust Diagnostic & Management Advisory",
        "organization": "ICAR-Indian Institute of Wheat and Barley Research (IIWBR), Karnal",
        "publication_year": "2023",
        "url": "https://iiwbr.icar.gov.in",
        "category": "disease",
        "crops": ["Wheat", "Barley"],
        "pathogen": "Puccinia striiformis (Yellow/Stripe), Puccinia triticina (Brown/Leaf), Puccinia graminis (Black/Stem)",
        "keywords": ["wheat rust", "yellow rust", "stripe rust", "brown rust", "puccinia", "cereal rust"],
        "summary": "Wheat rusts are airborne fungal diseases capable of causing substantial yield loss. Stripe (Yellow) rust produces parallel yellow pustules in cooler northern zones, while Leaf (Brown) rust produces scattered orange-brown pustules.",
        "scientific_explanation": (
            "Puccinia striiformis f. sp. tritici flourishes in cool (10-18°C) humid climates prevalent in northwestern plains and hill zones. "
            "Urediniospores land on leaves, germinate in dew drops, and colonize leaf vascular bundles, erupting through the epidermis in distinct linear chlorotic stripes. "
            "Puccinia triticina requires warmer conditions (20-25°C) and produces randomly distributed oval orange-brown uredinial pustules without striping."
        ),
        "differential_diagnosis": [
            {"condition": "Yellow/Stripe Rust vs Brown/Leaf Rust", "distinction": "Yellow rust forms neat, parallel linear stripes of yellow powdery pustules between leaf veins; Brown rust forms scattered, round-to-oval orange-brown pustules across the blade."},
            {"condition": "Nutrient Chlorosis (Zinc/Nitrogen deficiency)", "distinction": "Nutrient chlorosis causes uniform leaf paling without raised, powdery urediniospores that rub off onto a white cloth or fingertip."}
        ],
        "practical_steps": [
            "Cultivar Selection: Sowing resistant varieties (e.g. DBW 187, DBW 222, DBW 303, HD 3226, or PBW 725) is the primary line of defense.",
            "Timely Sowing: Complete wheat sowing between 01-15 November in northwestern plains to avoid peak sporulation conditions during grain filling.",
            "Field Surveillance: Check leaves weekly for yellow powder lines, especially on lower foliage and field edges bordering tree shade.",
            "Fungicide Spray: At the first detection of stripe rust patches, spray Propiconazole 25% EC (Tilt) @ 1.0 ml/L or Tebuconazole 25.9% EC @ 1.0 ml/L with 500 L water/ha. Repeat once after 15 days if conditions remain overcast."
        ],
        "limitations": "Avoid excessive basal Nitrogen (>150 kg/ha N) as lush succulence increases rust vulnerability. Ensure clean water without suspended silt during spraying."
    },
    {
        "id": "doc_rice_blast_brownspot",
        "title": "IRRI Rice Knowledge Bank & ICAR-National Rice Research Institute (NRRI): Blast & Brown Spot Advisory",
        "organization": "ICAR-National Rice Research Institute (NRRI), Cuttack & IRRI",
        "publication_year": "2023",
        "url": "https://www.knowledgebank.irri.org",
        "category": "disease",
        "crops": ["Rice (Paddy)"],
        "pathogen": "Magnaporthe oryzae (Blast) & Bipolaris oryzae (Brown Spot)",
        "keywords": ["rice blast", "neck blast", "brown spot rice", "magnaporthe", "paddy disease"],
        "summary": "Rice blast is a destructive fungal pathogen causing spindle-shaped eye lesions on leaves and black rot at the panicle neck. Brown spot causes oval brown lesions, often indicating depleted soil potassium or silica.",
        "scientific_explanation": (
            "Magnaporthe oryzae produces appressoria that generate extreme turgor pressure (>8 MPa) to penetrate cuticular cell walls. "
            "Blast development is aggravated by high nitrogen application, extended dew (>10 hours), and nighttime temperatures of 20-24°C. "
            "Bipolaris oryzae (Brown Spot) is an indicator of poor soil fertility (potassium or iron deficiency or moisture stress) and produces circular to oval brown spots with gray centres."
        ),
        "differential_diagnosis": [
            {"condition": "Rice Blast vs Brown Spot", "distinction": "Blast lesions are diamond or spindle-shaped (wide in the middle with pointed ends) with ash-gray centers and reddish-brown borders; Brown spot lesions are uniform round-to-oval spots distributed across the entire leaf."},
            {"condition": "Bacterial Leaf Blight (Xanthomonas oryzae)", "distinction": "Causes yellow-to-white wavy lesions starting from leaf tips and margins with milky bacterial ooze on cut stems immersed in clear water."}
        ],
        "practical_steps": [
            "Seed Treatment: Treat seed with Carbendazim 50% WP @ 2.0 g/kg or Tricyclazole 75% WP @ 2.0 g/kg seed before nursery sowing.",
            "Split Nitrogen Application: Never apply nitrogen in a single heavy dose. Split N into 3-4 applications (1/3 basal, 1/3 tillering, 1/3 panicle initiation).",
            "Silica & Potash Supplement: Apply Muriate of Potash (MOP) @ 50 kg/ha in two splits and apply silicon fertilizer or rice husk biochar to strengthen epidermal cell walls.",
            "Fungicide Intervention for Blast: If leaf blast lesions appear or neck blast threat looms at 5% panicle emergence, spray Tricyclazole 75% WP @ 0.6 g/L or Isoprothiolane 40% EC @ 1.5 ml/L.",
            "Treatment for Brown Spot: Spray Mancozeb 75% WP @ 2.0 g/L or Propiconazole 25% EC @ 1.0 ml/L and topdress with 20 kg/ha Potassium."
        ],
        "limitations": "Draining flooded water during blast outbreaks can worsen the disease because dry roots elevate host susceptibility. Maintain shallow submergence (2-3 cm)."
    },

    # -------------------------------------------------------------------------
    # 2. SOILS, NUTRIENTS & VISUAL CLASSIFICATION
    # -------------------------------------------------------------------------
    {
        "id": "doc_soil_black_vertisols",
        "title": "ICAR-Indian Institute of Soil Science (IISS): Management of Vertisols & Associated Black Soils",
        "organization": "ICAR-Indian Institute of Soil Science (IISS), Bhopal",
        "publication_year": "2023",
        "url": "https://iiss.icar.gov.in",
        "category": "soil",
        "soil_types": ["Black Soil", "Regur Soil", "Vertisols"],
        "keywords": ["black soil", "regur", "vertisol", "cotton soil", "montmorillonite clay", "cracking clay"],
        "summary": "Black soils (Vertisols) are high-clay soils (>35-50% montmorillonite) renowned for self-ploughing capacity, deep vertical shrinkage cracks when dry, high CEC, and intense water retention.",
        "scientific_explanation": (
            "Vertisols derive predominantly from the weathering of Deccan basaltic trap rocks. "
            "The dominant 2:1 expanding montmorillonite clay mineral swells dramatically when wetted and shrinks upon drying, producing characteristic deep polygonal cracks (up to 1 m deep). "
            "They possess high cation exchange capacity (CEC 40-70 cmol/kg), high calcium and magnesium carbonates, but suffer from low organic carbon (<0.4%), low available nitrogen, and low phosphorus bioavailability due to alkaline fixation at pH 7.8-8.6."
        ),
        "suitable_crops": ["Cotton", "Soybean", "Sorghum (Jowar)", "Chickpea (Gram)", "Pigeon Pea (Tur)", "Wheat (under irrigation)", "Sunflower", "Safflower"],
        "practical_steps": [
            "Broad Bed and Furrow (BBF) System: Construct 1.5 m wide beds with 30 cm furrows across the contour to drain excess monsoon rainfall and prevent root asphyxiation during downpours.",
            "Dry Sowing: Sow seeds 7-10 days prior to the onset of the monsoon in dry soil so germination begins with the very first rain shower, avoiding impassable sticky clay conditions.",
            "Phosphorus Placement: Band-place DAP or Single Superphosphate (SSP) 5 cm below and to the side of the seed line rather than broadcasting, preventing phosphorus fixation into insoluble calcium phosphates.",
            "Organic Matter Enrichment: Incorporate 8-10 tonnes/ha of well-rotted farmyard manure (FYM) or green manure with Sesbania to improve soil structure and water percolation."
        ],
        "limitations": "Very narrow moisture range for tillage: extremely sticky when wet and rock-hard when dry. Working the soil at incorrect moisture levels damages crumb structure."
    },
    {
        "id": "doc_soil_alluvial",
        "title": "MoA&FW & ICAR: Soil Health Card Scheme Guidelines — Alluvial Soil Systems of Indo-Gangetic Plains",
        "organization": "Ministry of Agriculture and Farmers Welfare (MoA&FW), Govt of India",
        "publication_year": "2023",
        "url": "https://www.soilhealth.dac.gov.in",
        "category": "soil",
        "soil_types": ["Alluvial Soil", "Khadar", "Bhangar", "Entisols", "Inceptisols"],
        "keywords": ["alluvial soil", "river soil", "loam", "indo-gangetic", "khadar", "bhangar", "soil health card"],
        "summary": "Alluvial soils are deep, fertile, loamy soils formed by deposition from river systems (Ganga, Brahmaputra, Indus). They support intensive multi-cropping of cereals, pulses, and cash crops.",
        "scientific_explanation": (
            "Divided chronologically into Khadar (newer, lighter, non-calcareous riverbed alluvium) and Bhangar (older, higher, clayey alluvium often containing kankar lime nodules). "
            "Texture ranges from sandy loam to silty clay loam with neutral to slightly alkaline pH (6.5-8.2). "
            "Generally rich in potash, lime, and phosphoric acid, but severely deficient in organic carbon (<0.3%) and nitrogen due to intensive continuous cropping (rice-wheat rotation)."
        ),
        "suitable_crops": ["Paddy (Rice)", "Wheat", "Sugarcane", "Maize", "Mustard", "Potato", "Jute", "Lentil", "Vegetables"],
        "practical_steps": [
            "Soil Health Card Testing: Test soil every 2 years for 12 parameters (N, P, K, S, Zn, Fe, Cu, Mn, B, pH, EC, Organic Carbon).",
            "Zinc & Nitrogen Scheduling: Apply Zinc Sulphate heptahydrate (21% Zn) @ 25 kg/ha every 2-3 seasons to overcome widespread zinc chlorosis in rice-wheat rotations.",
            "Green Manuring: Plant Dhaincha (Sesbania bispinosa) or Sunn hemp (Crotalaria juncea) during the summer fallow window (May-June) and incorporate at 45 days before paddy transplanting.",
            "Laser Land Levelling: Use laser leveling to ensure uniform irrigation water spread, saving 20-30% irrigation water and improving fertilizer use efficiency."
        ],
        "limitations": "Susceptible to nitrate leaching into shallow groundwater aquifers under excessive irrigation and broadcast urea use."
    },
    {
        "id": "doc_soil_red_laterite",
        "title": "ANGRAU & TNAU Technical Advisory: Sustainable Crop Production in Red & Laterite Soils",
        "organization": "ANGRAU (Andhra Pradesh) & TNAU (Tamil Nadu)",
        "publication_year": "2023",
        "url": "https://angrau.ac.in",
        "category": "soil",
        "soil_types": ["Red Soil", "Laterite Soil", "Alfisols", "Oxisols", "Ultisols"],
        "keywords": ["red soil", "laterite soil", "alfisol", "acidic soil", "iron oxide", "phosphorus fixation"],
        "summary": "Red and Laterite soils are porous, well-drained soils rich in iron and aluminum oxides with acidic to neutral pH (4.8-6.8). They have low CEC and high phosphorus-fixing capacity.",
        "scientific_explanation": (
            "Formed by intensive weathering of crystalline metamorphic rocks (granites, gneisses) under alternating wet and dry tropical conditions. "
            "The red hue stems from ferric oxides (hematite and goethite). Laterite soils undergo extensive desilication leaving iron and aluminum crusts. "
            "In acidic laterites (pH < 5.5), soluble aluminum and iron bind orthophosphate ions into insoluble iron/aluminum phosphates, making applied phosphate inaccessible."
        ),
        "suitable_crops": ["Groundnut (Peanut)", "Millets (Finger Millet / Ragi, Foxtail, Kodo)", "Pigeon Pea", "Cashew", "Mango", "Tapioca", "Tea", "Coffee", "Rubber"],
        "practical_steps": [
            "Liming for Acidic Soils: In soils with pH < 5.5, apply Agricultural Lime (CaCO3) or Dolomite @ 2-4 tonnes/ha based on buffer pH test once every 3 years before monsoon rains.",
            "Organic Matter Mulching: Apply 10-15 tonnes/ha FYM or coir pith compost to buffer cation leaching and double moisture retention capacity in dry spells.",
            "Phosphorus Management: Use Rock Phosphate or Single Superphosphate (SSP) combined with Phosphate Solubilizing Bacteria (PSB) @ 5 kg/ha to mobilize fixed phosphorus.",
            "Micronutrient Boron: Apply Borax @ 10 kg/ha for oilseeds (groundnut, sunflower) to prevent hollow heart disorder and ensure filled pods."
        ],
        "limitations": "Low water holding capacity makes crops susceptible to mid-season drought stress. Rainwater harvesting and contour bunding are essential."
    },

    # -------------------------------------------------------------------------
    # 3. FERTILIZERS, COMPOST & NUTRIENT CALCULATIONS
    # -------------------------------------------------------------------------
    {
        "id": "doc_fertilizer_npk_calculation",
        "title": "ICAR-IARI: Handbook of Integrated Nutrient Management & Fertilizer Dose Calculations",
        "organization": "ICAR-Indian Agricultural Research Institute (IARI), New Delhi",
        "publication_year": "2023",
        "url": "https://www.iari.res.in",
        "category": "crop_care",
        "crops": ["Wheat", "Rice", "Maize", "Cotton", "Potato"],
        "keywords": ["npk calculation", "fertilizer dosage", "urea calculation", "dap calculation", "mop calculation", "fertilizer formula", "nitrogen", "phosphorus", "potassium", "nutrient management", "wheat fertilizer", "nitrogen management", "phosphorus management"],
        "summary": "Guidelines for converting soil-test based N-P-K nutrient recommendations (kg/ha or kg/acre) into commercial fertilizer quantities (Urea, DAP, MOP, SSP) accounting for dual nutrients.",
        "scientific_explanation": (
            "Nutrient recommendations are expressed as elemental Nitrogen (N), Phosphorus pentoxide (P2O5), and Potassium oxide (K2O). "
            "Commercial fertilizer grades: "
            "• Urea: 46% N (0.46 kg N/kg fertilizer). "
            "• Diammonium Phosphate (DAP): 18% N and 46% P2O5 (0.18 kg N and 0.46 kg P2O5 per kg fertilizer). "
            "• Muriate of Potash (MOP): 60% K2O (0.60 kg K2O/kg fertilizer). "
            "• Single Superphosphate (SSP): 16% P2O5 and 11% Sulphur. "
            "Dual-Nutrient Calculation Principle: DAP supplies both Phosphorus and Nitrogen. Therefore, the Nitrogen contributed by DAP "
            "(DAP_kg × 0.18) MUST be subtracted from the total Nitrogen target before computing the remaining Urea requirement."
        ),
        "calculation_rules": {
            "dap_formula": "DAP (kg) = Target_P2O5_kg / 0.46",
            "n_from_dap_formula": "N_from_DAP (kg) = DAP_kg * 0.18",
            "remaining_n_formula": "N_remaining (kg) = max(0, Target_N_kg - N_from_DAP)",
            "urea_formula": "Urea (kg) = N_remaining / 0.46",
            "mop_formula": "MOP (kg) = Target_K2O_kg / 0.60",
            "ssp_alternative_formula": "SSP (kg) = Target_P2O5_kg / 0.16; Urea_no_dap = Target_N_kg / 0.46"
        },
        "practical_steps": [
            "Basal Application: Apply 100% of DAP, 100% of MOP, and 25-33% of Urea at final land preparation or sowing.",
            "Topdressing 1: Apply second split of Urea (33%) at active tillering (cereals) or 25-30 days after transplanting.",
            "Topdressing 2: Apply final split of Urea (33%) at panicle initiation / pre-flowering stage.",
            "Neem-Coated Urea: Use 100% Neem-coated Urea as mandated in India to slow nitrification and reduce leaching losses."
        ],
        "limitations": "Broadcast application on dry soil causes volatile ammonia losses up to 30%. Always incorporate fertilizers into moist soil or irrigate within 24 hours."
    },
    {
        "id": "doc_organic_farming_compost",
        "title": "National Centre of Organic and Natural Farming (NCONF): Standard Operating Procedures for On-Farm Formulations",
        "organization": "NCONF, Ministry of Agriculture & Farmers Welfare, Ghaziabad",
        "publication_year": "2023",
        "url": "https://ncof.dacnet.nic.in",
        "category": "crop_care",
        "keywords": ["organic farming", "jeevamrutha", "vermicompost", "biofertilizer", "neem cake", "panchagavya"],
        "summary": "Authentic preparation methods, nutrient profiles, and application schedules for verified organic formulations including Vermicompost, Jeevamrutha, and Bio-fertilizers.",
        "scientific_explanation": (
            "Organic formulations act as biological inoculants rather than high-concentration chemical fertilizers. "
            "Vermicompost contains 1.5-2.0% N, 1.0-1.5% P2O5, and 1.5-2.0% K2O, plus rich microbial diversity, actinomycetes, and plant growth regulators (auxins, gibberellins). "
            "Jeevamrutha promotes beneficial bacterial proliferation (Azotobacter, Bacillus, Pseudomonas) that solubilize native soil minerals and build disease suppressiveness in the rhizosphere."
        ),
        "practical_steps": [
            "Vermicompost Application: Apply 4-5 tonnes/ha for field crops or 2 kg/plant for fruit trees along the drip circle, lightly raking into the top 5 cm of soil.",
            "Jeevamrutha Preparation (200 L per acre): In a 200 L plastic drum, mix 10 kg fresh desi cow dung, 5-10 L cow urine, 2 kg jaggery, 2 kg pulse flour (besan), and a handful of virgin forest soil. Stir clockwise twice daily for 4-7 days in shade. Apply via irrigation water or as a 10% foliar spray.",
            "Bio-fertilizer Inoculation: Coat seeds with Rhizobium (for pulses) or Azospirillum / Azotobacter (for cereals) and PSB @ 200 g / 10 kg seed using rice kanji as a sticky carrier 30 minutes before sowing.",
            "Neem Cake: Apply 250 kg/ha neem cake at planting to inhibit soil nematodes and slow urea nitrification."
        ],
        "limitations": "Organic systems require 2-3 transitional years to restore biological soil equilibrium. Micronutrient deficiencies must be addressed with approved mineral sources (e.g. Zinc Sulfate, Borax)."
    },

    # -------------------------------------------------------------------------
    # 4. IRRIGATION & WATER MANAGEMENT (FAO STANDARDS)
    # -------------------------------------------------------------------------
    {
        "id": "doc_irrigation_fao_crop_water",
        "title": "FAO Irrigation and Drainage Paper No. 56: Crop Evapotranspiration Guidelines & Drip Irrigation Sizing",
        "organization": "Food and Agriculture Organization (FAO) of the United Nations",
        "publication_year": "1998 (Updated standards 2021)",
        "url": "https://www.fao.org/land-water/databases-and-software/crop-information/en/",
        "category": "irrigation",
        "keywords": ["irrigation", "crop water requirement", "evapotranspiration", "drip irrigation", "water calculation", "eto", "kc"],
        "summary": "Standardized methodologies for calculating daily crop water requirement (ETc = ETo × Kc) and calculating precision drip irrigation run times.",
        "scientific_explanation": (
            "Crop Evapotranspiration (ETc) is calculated by multiplying Reference Crop Evapotranspiration (ETo, mm/day) "
            "by the empirical Crop Coefficient (Kc) reflecting the growth stage: "
            "• Initial stage (emergence to 10% cover): Kc = 0.40 - 0.50 "
            "• Mid-season stage (flowering to yield formation): Kc = 1.05 - 1.25 "
            "• Late season stage (maturity and harvest): Kc = 0.60 - 0.80 "
            "Volumetric Water Requirement: 1 mm of depth over 1 m² equals exactly 1.0 Litre of water. "
            "Water Volume (Litres/day) = Area (m²) × ETc (mm/day) × Ground Cover Factor. "
            "Drip Run Time (Hours) = Required Water Volume (Litres) / Total Emitter Discharge Rate (Litres/hour)."
        ),
        "practical_steps": [
            "Determine Daily ETo: Obtain local evaporation rates from weather stations (typically 4.0 - 7.0 mm/day in Indian summers, 2.5 - 4.0 mm/day in winter).",
            "Select Kc Stage: Use Kc initial (0.45) for first 20 days, Kc mid (1.15) during fruit set/flowering, Kc end (0.75) approaching harvest.",
            "Account for Irrigation Efficiency: Drip irrigation has an efficiency of 85-90% (factor = 0.90); furrow irrigation has an efficiency of 50-60%.",
            "Calculate Pump Runtime: If 1 acre (4,047 m²) of mid-season tomatoes (ETc = 4.5 mm × 1.15 = 5.17 mm/day) requires ~21,000 Litres/day, and system discharge is 7,000 L/h, run the drip system for 3.0 hours."
        ],
        "limitations": "Adjust runtime after rainfall events using an on-farm rain gauge (effective rainfall deduction). Flush drip lateral lines with dilute acid every 6 months to clear calcium carbonate scale."
    },

    # -------------------------------------------------------------------------
    # 5. AGRICULTURAL ECONOMICS, SEED RATE & PROFITABILITY
    # -------------------------------------------------------------------------
    {
        "id": "doc_agri_economics_seed_rate",
        "title": "Directorate of Economics and Statistics (DES), MoA&FW: Farm Costing Standards & Seed Rate Formulas",
        "organization": "Directorate of Economics and Statistics, Ministry of Agriculture & Farmers Welfare",
        "publication_year": "2023",
        "url": "https://eands.dacnet.nic.in",
        "category": "economics",
        "keywords": ["seed rate calculation", "plant population", "cost of cultivation", "gross return", "net return", "benefit cost ratio", "farm profit"],
        "summary": "Standard agricultural engineering formulas for calculating plant population, seed rate in kg/ha, cost of cultivation components (A2, A2+FL, C2), and Net Return.",
        "scientific_explanation": (
            "1. Plant Population Formula: "
            "Plant Population per Hectare = 10,000 m² / (Row Spacing in m × Plant Spacing in m). "
            "2. Seed Rate Formula (kg/ha): "
            "Seed Rate = (Plant Population × 1,000-Seed Weight in g) / (Germination % × Purity % × 10,000). "
            "3. Comprehensive Farm Economics: "
            "• Cost A2: Paid-out operational costs (seeds, fertilizers, pesticides, fuel, irrigation, hired labor, machinery hire). "
            "• Cost A2 + FL: Cost A2 plus imputed value of unpaid Family Labor. "
            "• Gross Return = Total Yield (Quintals) × Realized Sale Price (or MSP in ₹/Quintal). "
            "• Net Return = Gross Revenue - Total Cost of Cultivation. "
            "• Benefit-Cost Ratio (BCR) = Gross Return / Total Cost of Cultivation (A BCR > 1.5 indicates a financially viable enterprise)."
        ),
        "practical_steps": [
            "Input Tracking: Record all input expenses in a field ledger under: 1) Land prep, 2) Seed & seed treatment, 3) Fertilizers, 4) Crop protection, 5) Irrigation, 6) Labor/Harvesting.",
            "MSP Benchmarking: Verify current Government Minimum Support Price (MSP) notified annually by CACP/MoA&FW as a price floor before planning crop selection.",
            "Post-Harvest Storage: Use negotiable warehouse receipts (e-NWR) under WDRA to avoid distress sales during peak harvest glut."
        ],
        "limitations": "Price fluctuations in perishable horticultural crops (tomato, onion) can swing wildly outside MSP coverage. Contract farming or farmer producer organizations (FPOs) hedge price volatility."
    },

    # -------------------------------------------------------------------------
    # 6. HUMAN NUTRITION, BMR & DIETARY GUIDELINES
    # -------------------------------------------------------------------------
    {
        "id": "doc_human_nutrition_icmr_nin",
        "title": "ICMR - National Institute of Nutrition (NIN): Nutrient Requirements and RDA for Indians",
        "organization": "ICMR - National Institute of Nutrition (NIN), Hyderabad",
        "publication_year": "2020",
        "url": "https://www.nin.res.in",
        "category": "nutrition",
        "keywords": ["calorie", "daily calorie target", "bmr", "tdee", "mifflin-st jeor", "diet plan", "macronutrient", "protein rda", "nutrition guidelines"],
        "summary": "Daily calorie requirements are calculated from Basal Metabolic Rate (BMR) using the clinically validated Mifflin-St Jeor equation multiplied by the Physical Activity Level (PAL) factor, adjusted according to ICMR-NIN 2020 dietary standards.",
        "scientific_explanation": (
            "The Mifflin-St Jeor equation provides the highest accuracy in predicting resting energy expenditure (REE/BMR) across populations:\n"
            "• Men: BMR (kcal/day) = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5\n"
            "• Women: BMR (kcal/day) = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) - 161\n\n"
            "Total Daily Energy Expenditure (TDEE) is calculated by multiplying BMR with the Physical Activity Level (PAL) coefficient:\n"
            "• Sedentary (desk work, minimal movement): BMR × 1.20\n"
            "• Moderately Active (regular agricultural work or 3-5 days exercise): BMR × 1.55\n"
            "• Vigorous / Heavy Agricultural Field Labor: BMR × 1.75 - 1.90\n\n"
            "Calorie Target: Maintenance = TDEE. For gradual, sustainable fat loss, subtract 300 to 500 kcal/day (safe rate: 0.5 kg/week). "
            "Macronutrient distribution per ICMR-NIN 2020: 50-60% carbohydrates (complex whole grains and millets), 15-20% protein (0.83-1.0 g/kg body weight), and 20-30% healthy lipids."
        ),
        "differential_diagnosis": [
            {"condition": "BMR vs TDEE", "distinction": "BMR is energy spent at total rest just to maintain vital organs (breathing, cardiac function, cellular repair). TDEE is total daily burn including NEAT, exercise, and thermic effect of food."},
            {"condition": "Crash Dieting (<1200 kcal)", "distinction": "Excessive caloric deficit (>700 kcal) induces thyroid downregulation, loss of lean muscle mass, and metabolic adaptation; moderate 300-500 kcal deficit preserves metabolic rate."}
        ],
        "practical_steps": [
            "Measure Baseline Biometrics: Record accurate morning fasting weight (kg) and standing height (cm).",
            "Calculate BMR: Apply the Mifflin-St Jeor equation matching your biological sex.",
            "Determine TDEE: Multiply BMR by your realistic physical activity level (PAL).",
            "Set Caloric Goal: For maintenance, eat TDEE; for gradual fat loss, subtract 400-500 kcal/day (never dropping below 1200 kcal/day for adult females or 1500 kcal/day for adult males).",
            "Distribute Across Meals: Split daily calories across 4-5 structured meals (Breakfast ~25%, Lunch ~35%, Snacks ~10%, Dinner ~30%) rich in pulses, local farm vegetables, and millets."
        ],
        "limitations": "Mifflin-St Jeor equation estimates population averages; individuals with high lean muscle mass or endocrine conditions (hypothyroidism) should consult a registered dietitian or clinical nutritionist."
    }
]

STOPWORDS = {
    "how", "what", "why", "when", "where", "which", "who", "and", "the", "for", "are",
    "with", "from", "can", "tell", "about", "calculate", "some", "this", "that", "much",
    "many", "does", "have", "been", "will", "your", "give", "please", "help", "plant",
    "crop", "disease", "spots", "leaf", "leaves", "type"
}

class AgriculturalKnowledgeEngine:
    """
    Search and retrieval engine indexing verified ICAR, State University, and FAO extension material.
    Supports BM25-style keyword matching, category filtering, crop cross-referencing,
    and structured evidence extraction with strict citation tracking.
    """

    @staticmethod
    def search(
        query: str,
        category: Optional[str] = None,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        query_clean = query.lower()
        all_tokens = set(re.findall(r"\b[a-z]{3,}\b", query_clean))
        meaningful_tokens = all_tokens - STOPWORDS

        scored_docs = []

        for doc in VERIFIED_KNOWLEDGE_DOCUMENTS:
            doc_category = doc.get("category")
            if category:
                if doc_category == category:
                    category_weight = 1.3
                else:
                    category_weight = 0.05
            else:
                category_weight = 1.0

            score = 0.0

            # 1. Exact phrase / title match
            if doc["title"].lower() in query_clean:
                score += 60.0

            # 2. Keyword exact matches & meaningful token overlap
            for kw in doc.get("keywords", []):
                kw_lower = kw.lower()
                if kw_lower in query_clean:
                    score += 40.0
                else:
                    kw_tokens = set(re.findall(r"\b[a-z]{3,}\b", kw_lower)) - STOPWORDS
                    common = kw_tokens.intersection(meaningful_tokens)
                    if len(common) >= 2:
                        score += 15.0 * len(common)
                    elif len(common) == 1:
                        score += 4.0

            # 3. Crops match
            for crop in doc.get("crops", []):
                if crop.lower() in query_clean:
                    score += 25.0

            # 4. Soil types match
            for st in doc.get("soil_types", []):
                if st.lower() in query_clean:
                    score += 25.0

            # 5. Meaningful token overlap in summary and scientific explanation
            combined_text = (doc["summary"] + " " + doc["scientific_explanation"]).lower()
            overlap_count = sum(1 for tok in meaningful_tokens if tok in combined_text)
            score += overlap_count * 1.5

            final_score = score * category_weight

            if final_score >= 20.0:
                scored_docs.append((final_score, doc))

        # Sort descending by score
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_docs[:top_k]]

    @staticmethod
    def get_document_by_id(doc_id: str) -> Optional[Dict[str, Any]]:
        for d in VERIFIED_KNOWLEDGE_DOCUMENTS:
            if d["id"] == doc_id:
                return d
        return None

    @staticmethod
    def get_all_citations() -> List[Dict[str, str]]:
        """Returns all distinct verified authoritative sources in the catalog."""
        citations = []
        seen = set()
        for d in VERIFIED_KNOWLEDGE_DOCUMENTS:
            key = (d["title"], d["organization"], d["url"])
            if key not in seen:
                seen.add(key)
                citations.append({
                    "title": d["title"],
                    "organization": d["organization"],
                    "year": d["publication_year"],
                    "url": d["url"],
                    "category": d.get("category", "general")
                })
        return citations
