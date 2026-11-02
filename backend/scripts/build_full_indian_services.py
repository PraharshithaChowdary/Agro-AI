# -*- coding: utf-8 -*-
"""
Master Indian Plants and Soils Database & Engine Builder
"""
import os
import json

PLANTS_DATA = [
    # ------------------ 1. CEREALS & MILLETS ------------------
    {
        "id": "rice",
        "canonical_name": "Rice / Paddy (Dhan)",
        "hindi_name": "धान / चावल (Dhan / Chawal)",
        "scientific_name": "Oryza sativa",
        "category": "Cereals & Millets",
        "indian_season": "Kharif (June–Nov) & Rabi (Nov–April)",
        "major_states": "West Bengal, Uttar Pradesh, Punjab, Andhra Pradesh, Telangana, Odisha, Tamil Nadu, Bihar",
        "disease_model_available": True,
        "supported_diseases": ["Bacterial Leaf Blight", "Brown Spot", "Leaf Blast", "Sheath Blight"],
        "care_guide": {
            "watering": "Maintain 2–5 cm standing water layer from transplanting till grain filling; drain field 10–14 days prior to harvest.",
            "sunlight": "Full direct tropical sunlight (6–8 hours daily); optimal temperature range 22°C to 32°C.",
            "soil": "Heavy clayey or silty alluvial soils with high water holding capacity and pH 5.5 to 7.0.",
            "humidity": "High humidity (70%–90%) during vegetative growth.",
            "nutrition": "Recommended NPK 120:60:40 kg/ha. Apply Nitrogen in 3 splits (Basal, Tillering, Panicle Initiation). Supplement 25 kg/ha Zinc Sulfate."
        },
        "default_management": [
            "Treat seeds with Pseudomonas fluorescens (10g/kg) or Trichoderma viride before sowing.",
            "Practice Alternate Wetting and Drying (AWD) water management to save 30% irrigation water and reduce methane emissions.",
            "Maintain 20cm x 15cm hill spacing for optimal tillering and sun penetration.",
            "Apply Neem-coated urea to minimize volatilization loss and boost nitrogen uptake efficiency."
        ],
        "aliases": ["rice", "paddy", "dhan", "chawal", "oryza", "basmati", "sona masoori", "ir64", "swarna", "ponni", "sambha", "bPT 5204"]
    },
    {
        "id": "wheat",
        "canonical_name": "Wheat (Gehun)",
        "hindi_name": "गेहूं (Gehun)",
        "scientific_name": "Triticum aestivum",
        "category": "Cereals & Millets",
        "indian_season": "Rabi (Oct/Nov–March/April)",
        "major_states": "Uttar Pradesh, Punjab, Haryana, Madhya Pradesh, Rajasthan, Bihar, Gujarat",
        "disease_model_available": True,
        "supported_diseases": ["Yellow Rust (Stripe Rust)", "Brown Rust (Leaf Rust)", "Loose Smut", "Powdery Mildew", "Karnal Bunt"],
        "care_guide": {
            "watering": "Provide 4–6 critical irrigations: Crown Root Initiation (21 DAS), Tillering (40 DAS), Jointing (60 DAS), Flowering (80 DAS), and Milk stage (100 DAS).",
            "sunlight": "Bright clear sunny winter days (6–8 hours); cool temperature during vegetative stage (15–20°C) and warm during maturity (25°C).",
            "soil": "Well-drained fertile loamy to clay loam alluvial soils with neutral pH 6.0–7.5.",
            "humidity": "Moderate humidity (50–65%). High humidity and overcast weather invite stripe rust outbreaks.",
            "nutrition": "NPK 120:60:40 kg/ha. Apply 50% N + full P & K as basal; remaining N split between first and second irrigation."
        },
        "default_management": [
            "Sow certified rust-resistant varieties (e.g., HD 2967, HD 3086, DBW 187, DBW 222, PBW 550) between Nov 1–15.",
            "Apply Pendimethalin (1.0 kg a.i./ha) within 3 days of sowing for pre-emergence weed suppression.",
            "Avoid excessive irrigation during late milky stage to prevent lodging caused by western disturbances / hail.",
            "Foliar spray of 0.2% Propiconazole (Tilt 25 EC) at first sight of yellow rust pustules on foliage."
        ],
        "aliases": ["wheat", "gehun", "gehu", "triticum", "atta", "durum", "sharbati", "lokwan", "kalyansona", "sonalika"]
    },
    {
        "id": "maize",
        "canonical_name": "Maize / Corn (Makka)",
        "hindi_name": "मक्का (Makka)",
        "scientific_name": "Zea mays",
        "category": "Cereals & Millets",
        "indian_season": "Kharif (June–Oct), Rabi (Oct–March) & Spring (Jan–May)",
        "major_states": "Karnataka, Madhya Pradesh, Maharashtra, Bihar, Rajasthan, Andhra Pradesh, Telangana",
        "disease_model_available": True,
        "supported_diseases": ["Northern Corn Leaf Blight", "Common Rust", "Gray Leaf Spot", "Bacterial Stalk Rot"],
        "care_guide": {
            "watering": "Irrigate at critical moisture stages: Tasseling, Silking, and Grain Filling. Avoid waterlogging which causes severe root hypoxia.",
            "sunlight": "Full direct sunlight, 7–8 hours daily. Optimum growth temperature 21°C–30°C.",
            "soil": "Deep, rich, well-drained alluvial or red sandy loam soils with pH 5.8–7.2.",
            "humidity": "Moderate (60–70%).",
            "nutrition": "NPK 120:60:40 kg/ha for hybrids. Top-dress nitrogen at knee-high stage and pretasseling stage."
        },
        "default_management": [
            "Install pheromone traps (5 traps/acre) for early monitoring of Fall Armyworm (Spodoptera frugiperda).",
            "Spray Emamectin Benzoate 5% SG (0.4 g/L) or Chlorantraniliprole 18.5% SC into the leaf whorls if FAW damage exceeds 10%.",
            "Ensure field ridges and furrows to drain excess monsoon water rapidly.",
            "Practice intercropping with Cowpea or Soybean for weed suppression and atmospheric nitrogen fixation."
        ],
        "aliases": ["maize", "corn", "makka", "bhutta", "makki", "zea", "sweet corn", "popcorn", "zea mays"]
    },
    {
        "id": "jowar",
        "canonical_name": "Sorghum / Great Millet (Jowar)",
        "hindi_name": "ज्वार (Jowar)",
        "scientific_name": "Sorghum bicolor",
        "category": "Cereals & Millets",
        "indian_season": "Kharif & Rabi (Maharashtra / Karnataka)",
        "major_states": "Maharashtra, Karnataka, Rajasthan, Tamil Nadu, Andhra Pradesh, Madhya Pradesh",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Highly drought-resilient. Requires 1–2 supplemental irrigations at boot leaf and flowering stages during dry spells.",
            "sunlight": "Abundant direct tropical sunlight (7+ hours). Ideal temperature 26°C–33°C.",
            "soil": "Thrives across medium to deep Black (Vertisol) and Red loamy soils; tolerates mild salinity.",
            "humidity": "Low to moderate humidity (40–60%).",
            "nutrition": "NPK 80:40:40 kg/ha for hybrids. Apply 5 tons/ha well-rotted FYM during land preparation."
        },
        "default_management": [
            "Seed treatment with Imidacloprid 70 WS (5 g/kg seed) to safeguard seedlings from Sorghum shoot fly.",
            "Intercrop with Pigeon Pea (Tur/Arhar) in a 2:1 or 3:1 row ratio for risk mitigation in rainfed zones.",
            "Harvest panicles when grain moisture drops to 15% and black layer forms at the grain base."
        ],
        "aliases": ["jowar", "sorghum", "great millet", "cholam", "jonna", "sorghum bicolor", "maldandi"]
    },
    {
        "id": "bajra",
        "canonical_name": "Pearl Millet (Bajra)",
        "hindi_name": "बाजरा (Bajra)",
        "scientific_name": "Pennisetum glaucum",
        "category": "Cereals & Millets",
        "indian_season": "Kharif (July–Oct) & Summer (Feb–May)",
        "major_states": "Rajasthan, Uttar Pradesh, Gujarat, Haryana, Maharashtra",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Exceptional drought tolerance. Requires 250–350 mm total rainfall; 1 irrigation at panicle emergence boosts yield by 40%.",
            "sunlight": "Full direct intense sunlight (8+ hours daily); tolerates ambient heat up to 42°C.",
            "soil": "Light sandy loam, arid soils, or red soils with good drainage; tolerates low fertility.",
            "humidity": "Low ambient humidity (30–50%).",
            "nutrition": "NPK 60:30:20 kg/ha. Apply Azospirillum and PSB biofertilizers (2 kg/ha each) with 500 kg compost."
        },
        "default_management": [
            "Soak seeds in 20% salt solution to float off and discard Ergot-sclerotia contaminated seeds.",
            "Spray Mancozeb (2 g/L) at boot-leaf stage if downy mildew (green ear disease) is reported in locality.",
            "Maintain plant population of 175,000 plants/ha with 45cm x 12cm spacing."
        ],
        "aliases": ["bajra", "pearl millet", "kambu", "sajjalu", "bajri", "pennisetum glaucum", "cumbu"]
    },
    {
        "id": "ragi",
        "canonical_name": "Finger Millet (Ragi / Mandua)",
        "hindi_name": "रागी / मंडुआ (Ragi / Mandua)",
        "scientific_name": "Eleusine coracana",
        "category": "Cereals & Millets",
        "indian_season": "Kharif & Early Rabi (South India)",
        "major_states": "Karnataka, Tamil Nadu, Uttarakhand, Odisha, Andhra Pradesh, Maharashtra, Jharkhand",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Rainfed crop; provide life-saving irrigation at tillering and grain filling if dry spell exceeds 15 days.",
            "sunlight": "Full sunshine (6–8 hours daily). Tolerates mountain slope solar conditions.",
            "soil": "Red loamy soils, lateritic soils, and light alluvial soils with good surface drainage.",
            "humidity": "Moderate (50–70%).",
            "nutrition": "NPK 60:30:30 kg/ha. Excellent response to organic farmyard manure (7.5 t/ha) and Azospirillum seed inoculation."
        },
        "default_management": [
            "Transplant 21-day-old seedlings at 22.5cm x 10cm spacing for 35% higher grain yield than broadcasting.",
            "Spray Tricyclazole 75 WP (0.6 g/L) to prevent Ragi finger blast and neck blast during cloudy monsoon spells.",
            "Intercrop with Field Bean (Avarekai) or Groundnut (4:1 row ratio) for soil nutrient replenishment."
        ],
        "aliases": ["ragi", "finger millet", "mandua", "nachani", "kezhvaragu", "ragulu", "eleusine coracana", "madua"]
    },
    {
        "id": "foxtail_millet",
        "canonical_name": "Foxtail Millet (Kangni / Kakun)",
        "hindi_name": "कंगनी / काकुन (Kangni / Kakun)",
        "scientific_name": "Setaria italica",
        "category": "Cereals & Millets",
        "indian_season": "Kharif (June–Sept) & Summer",
        "major_states": "Andhra Pradesh, Karnataka, Telangana, Tamil Nadu, Rajasthan, UP",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Low water requirement (200–300 mm); thrives in rainfed conditions.",
            "sunlight": "Full sunlight (6–8 hours daily).",
            "soil": "Light well-drained sandy loam or red loam soils.",
            "humidity": "Low to moderate humidity.",
            "nutrition": "NPK 40:20:0 kg/ha along with 5 tons/ha organic compost."
        },
        "default_management": [
            "Weed at 20 and 40 DAS to prevent crop-weed competition in initial growth phase.",
            "Seed treatment with Trichoderma viride (4 g/kg seed) to prevent seedling blight."
        ],
        "aliases": ["foxtail millet", "kangni", "kakun", "tenai", "korra", "navane", "setaria italica", "rala"]
    },
    {
        "id": "little_millet",
        "canonical_name": "Little Millet (Kutki / Sama)",
        "hindi_name": "कुटकी / सामा (Kutki / Sama)",
        "scientific_name": "Panicum sumatrense",
        "category": "Cereals & Millets",
        "indian_season": "Kharif (June–Aug)",
        "major_states": "Madhya Pradesh, Odisha, Jharkhand, Chhattisgarh, Tamil Nadu, Karnataka",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Highly drought-hardy rainfed cereal; withstands water stress and shallow soils.",
            "sunlight": "Full sun (6–8 hours daily).",
            "soil": "Marginal, shallow, gravelly red and tribal hilly soils.",
            "humidity": "Moderate (50–65%).",
            "nutrition": "NPK 30:15:0 kg/ha + 5 t/ha FYM."
        },
        "default_management": [
            "Sow on contour lines in hilly tribal tracts to prevent soil erosion.",
            "Harvest panicles when grains turn golden-brown (75–85 days)."
        ],
        "aliases": ["little millet", "kutki", "sama", "samai", "same", "samalu", "panicum sumatrense"]
    },
    {
        "id": "kodo_millet",
        "canonical_name": "Kodo Millet (Kodon / Varagu)",
        "hindi_name": "कोदो / कोदों (Kodo / Kodon)",
        "scientific_name": "Paspalum scrobiculatum",
        "category": "Cereals & Millets",
        "indian_season": "Kharif (June–Oct)",
        "major_states": "Madhya Pradesh (Dindori, Mandla), Chhattisgarh, Tamil Nadu, Karnataka, Gujarat",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Rainfed; requires 300–400 mm rainfall.",
            "sunlight": "Full sunlight (7–8 hours daily).",
            "soil": "Gravelly, stony, shallow red and lateritic soils.",
            "humidity": "Low to moderate humidity.",
            "nutrition": "NPK 40:20:0 kg/ha."
        },
        "default_management": [
            "Ensure line sowing at 30cm row spacing rather than broadcasting for easier weeding.",
            "Store grain at <10% moisture to prevent fungal mycotoxin formation (Kodo poisoning)."
        ],
        "aliases": ["kodo millet", "kodo", "kodon", "varagu", "harka", "arixalu", "paspalum scrobiculatum"]
    },
    {
        "id": "barnyard_millet",
        "canonical_name": "Barnyard Millet (Sanwa / Jhangora)",
        "hindi_name": "सांवा / झंगोरा (Sanwa / Jhangora)",
        "scientific_name": "Echinochloa frumentacea",
        "category": "Cereals & Millets",
        "indian_season": "Kharif (June–Sept) & Summer",
        "major_states": "Uttarakhand (Hills), Uttar Pradesh, Madhya Pradesh, Bihar, Tamil Nadu",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Fastest growing millet (matures in 45–60 days); ideal for emergency flood/drought situations.",
            "sunlight": "Full sunlight; tolerates cool mountain conditions.",
            "soil": "Sandy loam to clay loam; tolerates waterlogged marginal soils.",
            "humidity": "Moderate (55–70%).",
            "nutrition": "NPK 40:20:0 kg/ha + 5 tons FYM."
        },
        "default_management": [
            "Excellent dual-purpose crop for nutritive grain (Vrat food) and green forage for cattle.",
            "Harvest when head turns light yellow."
        ],
        "aliases": ["barnyard millet", "sanwa", "jhangora", "kuthiraivali", "odalu", "echinochloa frumentacea", "samvat"]
    },
    {
        "id": "barley",
        "canonical_name": "Barley (Jau)",
        "hindi_name": "जौ (Jau)",
        "scientific_name": "Hordeum vulgare",
        "category": "Cereals & Millets",
        "indian_season": "Rabi (Oct/Nov–March)",
        "major_states": "Rajasthan, Uttar Pradesh, Madhya Pradesh, Haryana, Punjab, Bihar",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "2–3 irrigations at tillering, flowering, and grain filling stages.",
            "sunlight": "Full winter sun; tolerates cold and semi-arid conditions.",
            "soil": "Sandy loam to clay loam; outstanding tolerance to saline and alkaline (Usar) soils.",
            "humidity": "Low humidity (35–55%).",
            "nutrition": "NPK 60:30:20 kg/ha. Avoid high nitrogen for malting barley to maintain low grain protein (<11%)."
        },
        "default_management": [
            "Sow in first fortnight of November at 22.5cm row spacing.",
            "Treat seed with Carboxin (Vitavax 2g/kg) to eliminate covered smut spores."
        ],
        "aliases": ["barley", "jau", "jav", "hordeum vulgare", "jau grain", "yava"]
    },
    {
        "id": "oats",
        "canonical_name": "Oats (Jai)",
        "hindi_name": "जई (Jai)",
        "scientific_name": "Avena sativa",
        "category": "Cereals & Millets",
        "indian_season": "Rabi (Oct/Nov–March/April)",
        "major_states": "Punjab, Haryana, Uttar Pradesh, Madhya Pradesh, Himachal Pradesh, Rajasthan",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "3–4 irrigations at 20–25 day intervals.",
            "sunlight": "Cool sunny winter weather.",
            "soil": "Well-drained loam to clay loam with pH 6.0–7.5.",
            "humidity": "Moderate (50–65%).",
            "nutrition": "NPK 80:40:0 kg/ha. Top-dress 40 kg N after first cutting for fodder."
        },
        "default_management": [
            "Take first cut at 55–60 DAS for fodder, leaving 5 cm stubble for grain regeneration.",
            "Harvest grain at full ripe stage when grains become firm and golden."
        ],
        "aliases": ["oats", "jai", "avena sativa", "oatmeal grain"]
    },
    {
        "id": "buckwheat",
        "canonical_name": "Buckwheat (Kuttu / Phappar)",
        "hindi_name": "कुट्टू / फाफर (Kuttu / Phappar)",
        "scientific_name": "Fagopyrum esculentum",
        "category": "Cereals & Millets",
        "indian_season": "Kharif & Summer in Himalayan highlands (July–Oct)",
        "major_states": "Jammu & Kashmir (Ladakh), Himachal Pradesh (Kinnaur, Lahaul), Uttarakhand, Sikkim, Arunachal",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Short season crop (60–75 days); moderate moisture requirement.",
            "sunlight": "High altitude mountain sunshine (cool climate <25°C).",
            "soil": "Light, sandy, acidic mountain soils with pH 5.0–6.5.",
            "humidity": "Moderate mountain humidity.",
            "nutrition": "NPK 30:20:20 kg/ha + organic compost."
        },
        "default_management": [
            "Key fasting grain (Vrat Atta) rich in rutin antioxidant and gluten-free protein.",
            "Harvest early morning when 75% seeds turn dark brown to prevent shattering."
        ],
        "aliases": ["buckwheat", "kuttu", "phappar", "ogla", "kutu", "fagopyrum esculentum", "kuttu atta"]
    },
    {
        "id": "amaranth_grain",
        "canonical_name": "Amaranth Grain (Rajgira / Ramdana)",
        "hindi_name": "राजगिरा / रामदाना (Rajgira / Ramdana)",
        "scientific_name": "Amaranthus cruentus / Amaranthus hypochondriacus",
        "category": "Cereals & Millets",
        "indian_season": "Rabi in plains (Oct–March); Kharif in hills (May–Oct)",
        "major_states": "Gujarat, Maharashtra, Uttarakhand, Himachal Pradesh, Tamil Nadu",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "2–3 light irrigations; drought and heat tolerant C4 pseudo-cereal.",
            "sunlight": "Full direct sunlight (7–8 hours daily).",
            "soil": "Adaptable to diverse loamy and red soils with pH 6.0–7.5.",
            "humidity": "Low to moderate humidity.",
            "nutrition": "NPK 50:25:20 kg/ha + 5 t/ha compost."
        },
        "default_management": [
            "Maintain 45cm x 15cm plant spacing.",
            "Cut large colorful seed heads when seeds become hard and resist thumbnail pressing."
        ],
        "aliases": ["rajgira", "ramdana", "amaranth grain", "chaulai grain", "chua", "amaranthus hypochondriacus"]
    },

    # ------------------ 2. PULSES & LEGUMES ------------------
    {
        "id": "chickpea",
        "canonical_name": "Chickpea / Bengal Gram (Chana)",
        "hindi_name": "चना / काबुली चना (Chana / Kabuli Chana)",
        "scientific_name": "Cicer arietinum",
        "category": "Pulses & Legumes",
        "indian_season": "Rabi (Oct–March)",
        "major_states": "Madhya Pradesh, Maharashtra, Rajasthan, Karnataka, Uttar Pradesh, Andhra Pradesh",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Requires 1–2 light irrigations (pre-flowering and pod development). Over-irrigation causes excessive vegetative growth and wilt.",
            "sunlight": "Bright clear winter sunshine (6–8 hours); optimum temperature 18°C–26°C.",
            "soil": "Deep Black soil or well-drained medium alluvial loam; sensitive to waterlogging and salinity.",
            "humidity": "Low humidity (30–50%). Foggy/cloudy weather at flowering causes severe flower drop.",
            "nutrition": "NPK 20:40:20 kg/ha as basal + 20 kg/ha Sulfur. Inoculate seeds with Rhizobium leguminosarum + PSB culture."
        },
        "default_management": [
            "Nip apical vegetative shoots at 35–40 DAS to stimulate extensive lateral branching and double pod formation.",
            "Install bird perches (15–20/acre) and pheromone traps for natural Helicoverpa armigera (pod borer) predation.",
            "Deep summer ploughing to expose soilborne Fusarium oxysporum (wilt) fungal resting spores to direct sun heat."
        ],
        "aliases": ["chickpea", "bengal gram", "chana", "kabuli chana", "desi chana", "kala chana", "harbara", "kadale", "cicer arietinum", "gram"]
    },
    {
        "id": "pigeon_pea",
        "canonical_name": "Pigeon Pea / Red Gram (Arhar / Toor Dal)",
        "hindi_name": "अरहर / तूर दाल (Arhar / Toor Dal)",
        "scientific_name": "Cajanus cajan",
        "category": "Pulses & Legumes",
        "indian_season": "Kharif (June/July–Dec/Jan)",
        "major_states": "Maharashtra, Madhya Pradesh, Karnataka, Uttar Pradesh, Gujarat, Telangana, Jharkhand",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Primarily rainfed; deep taproot draws subsoil moisture. 1 irrigation at pod development stage during dry winter.",
            "sunlight": "Full tropical sun (7–8 hours daily).",
            "soil": "Deep, well-drained loam or Black soil (Vertisol) with pH 6.5–7.5; waterlogging kills seedlings within 48 hours.",
            "humidity": "Moderate (55–70%).",
            "nutrition": "NPK 20:50:20 kg/ha + 20 kg Sulfur/ha. Basal application of Single Super Phosphate (SSP) is highly beneficial."
        },
        "default_management": [
            "Grow wilt-resistant and sterility mosaic resistant varieties (e.g., Asha / ICPL 87119, Maruti / ICP 8863, BDN 711).",
            "Spray Chlorantraniliprole 18.5 SC (0.3 ml/L) or Spinosad 45 SC (0.3 ml/L) at 50% flowering to control pod borers (Maruca & Helicoverpa).",
            "Intercrop with Sorghum, Maize, or Soybean (1:2 row ratio) for enhanced land equivalent ratio."
        ],
        "aliases": ["pigeon pea", "red gram", "arhar", "toor", "tur", "toor dal", "tuvar", "kandi", "cajanus cajan", "togari"]
    },
    {
        "id": "green_gram",
        "canonical_name": "Green Gram / Mung Bean (Moong)",
        "hindi_name": "मूंग दाल (Moong Dal)",
        "scientific_name": "Vigna radiata",
        "category": "Pulses & Legumes",
        "indian_season": "Kharif (June–Aug), Rabi (South India) & Zaid / Summer (March–May)",
        "major_states": "Rajasthan, Madhya Pradesh, Maharashtra, Karnataka, Andhra Pradesh, Odisha, Bihar, UP",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "For summer crop: 3–4 light irrigations at 10–12 day intervals. Discontinue watering when 80% pods turn black.",
            "sunlight": "Warm, sunny weather (6–8 hours daily); optimum temp 27°C–35°C.",
            "soil": "Well-drained fertile sandy loam to alluvial loam with neutral pH 6.5–7.5.",
            "humidity": "Moderate (50–65%).",
            "nutrition": "NPK 20:40:20 kg/ha. Treat seeds with Rhizobium and Trichoderma (5 g/kg seed)."
        },
        "default_management": [
            "Grow Mungbean Yellow Mosaic Virus (MYMV) resistant varieties (e.g., IPM 02-3, Samrat, Pusa Vishal, SML 668).",
            "Spray Thiamethoxam 25 WG (0.3 g/L) at 15–20 DAS to suppress Whiteflies (Bemisia tabaci) that transmit MYMV.",
            "Harvest matured pods in 2 hand-pickings or use uniform ripening cultivars for combine harvesting."
        ],
        "aliases": ["green gram", "mung bean", "moong", "moong dal", "mung", "pesalu", "hesaru", "vigna radiata", "pasi payaru"]
    },
    {
        "id": "black_gram",
        "canonical_name": "Black Gram / Urad Bean (Urad)",
        "hindi_name": "उड़द दाल (Urad Dal)",
        "scientific_name": "Vigna mungo",
        "category": "Pulses & Legumes",
        "indian_season": "Kharif (June–Sept), Summer & Rabi (Rice fallows of coastal AP & TN)",
        "major_states": "Madhya Pradesh, Uttar Pradesh, Andhra Pradesh, Tamil Nadu, Maharashtra, Karnataka, Gujarat",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "In rice fallows: utilizes residual soil moisture. In summer: 3 light irrigations.",
            "sunlight": "Full direct sunlight, 6–8 hours daily.",
            "soil": "Medium to heavy Black soils, loams, and alluvial soils with adequate drainage.",
            "humidity": "Moderate to high humidity.",
            "nutrition": "NPK 20:40:20 kg/ha + 2% DAP foliar spray at flowering and pod filling."
        },
        "default_management": [
            "Broadcast seeds directly into standing paddy field 2–3 days before paddy harvest (relay cropping).",
            "Spray Propiconazole 25 EC (1 ml/L) if powdery mildew or Cercospora leaf spot appears on foliage."
        ],
        "aliases": ["black gram", "urad", "urad dal", "mash", "minumulu", "uddu", "vigna mungo", "ulundu"]
    },
    {
        "id": "red_lentil",
        "canonical_name": "Red Lentil (Masoor Dal)",
        "hindi_name": "मसूर दाल (Masoor Dal)",
        "scientific_name": "Lens culinaris",
        "category": "Pulses & Legumes",
        "indian_season": "Rabi (Oct/Nov–March)",
        "major_states": "Madhya Pradesh (Bundelkhand), Uttar Pradesh, Bihar, West Bengal, Rajasthan",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "1–2 irrigations at 40 DAS and flowering stage.",
            "sunlight": "Clear cool sunny winter days (18°C–25°C).",
            "soil": "Alluvial loams to clay loams; tolerates mild acidity.",
            "humidity": "Low humidity (35–50%).",
            "nutrition": "NPK 20:40:20 kg/ha + Rhizobium culture."
        },
        "default_management": [
            "Sow in first fortnight of November at 20cm row spacing.",
            "Spray Mancozeb (2 g/L) if Lentil Rust (Uromyces viciae-fabae) is noticed."
        ],
        "aliases": ["red lentil", "masoor", "masoor dal", "lens culinaris", "massar", "misure"]
    },
    {
        "id": "cowpea",
        "canonical_name": "Cowpea / Black-eyed Pea (Lobia / Chawli)",
        "hindi_name": "लोबिया / चावली (Lobia / Chawli)",
        "scientific_name": "Vigna unguiculata",
        "category": "Pulses & Legumes",
        "indian_season": "Kharif (June–Oct) & Summer (Feb–May)",
        "major_states": "Rajasthan, Karnataka, Kerala, Tamil Nadu, Maharashtra, Uttar Pradesh, Gujarat",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Rainfed in Kharif; 3–4 irrigations in summer. Outstanding drought tolerance.",
            "sunlight": "Full hot tropical sun (7–8 hours daily).",
            "soil": "Sandy loam, red loam, or alluvial soil with pH 5.5–7.5.",
            "humidity": "Moderate (50–70%).",
            "nutrition": "NPK 20:40:20 kg/ha."
        },
        "default_management": [
            "Harvest green tender pods for vegetable use (Chawli phali) or dry pods for pulse grain.",
            "Dual benefit: green foliage fixes 70 kg atmospheric N/ha and serves as succulent cattle fodder."
        ],
        "aliases": ["cowpea", "lobia", "chawli", "black eyed pea", "alasande", "karamani", "vigna unguiculata"]
    },
    {
        "id": "kidney_bean",
        "canonical_name": "Kidney Beans (Rajma)",
        "hindi_name": "राजमा (Rajma)",
        "scientific_name": "Phaseolus vulgaris",
        "category": "Pulses & Legumes",
        "indian_season": "Rabi in Northern plains (Oct–March); Kharif in Himalayan valleys (May–Sept)",
        "major_states": "Jammu & Kashmir (Bhaderwah), Himachal Pradesh, Uttarakhand, Maharashtra, Bihar, UP",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Provide 3–4 irrigations at 25, 50, 75, and 90 DAS. Extremely sensitive to water stagnation.",
            "sunlight": "Bright sunny days; prefers cool mild temperatures (15°C–22°C).",
            "soil": "Deep, rich, loose, well-drained fertile loam with pH 6.0–7.0.",
            "humidity": "Moderate (50–65%).",
            "nutrition": "High nitrogen demand (lacks native nodulation in Indian soils): NPK 100:60:40 kg/ha in 3 split doses."
        },
        "default_management": [
            "Treat seeds with Rhizobium phaseoli strain (special culture) before sowing.",
            "Spray Carbendazim (1 g/L) if Anthracnose pod spots appear."
        ],
        "aliases": ["kidney bean", "rajma", "rajmah", "french bean grain", "phaseolus vulgaris", "chitra rajma", "bhaderwah rajma"]
    },
    {
        "id": "soybean",
        "canonical_name": "Soybean (Bhat)",
        "hindi_name": "सोयाबीन (Soyabean)",
        "scientific_name": "Glycine max",
        "category": "Pulses & Legumes",
        "indian_season": "Kharif (June/July–Oct)",
        "major_states": "Madhya Pradesh, Maharashtra, Rajasthan, Karnataka, Telangana, Gujarat",
        "disease_model_available": True,
        "supported_diseases": ["Soybean Rust", "Bacterial Pustule", "Frogeye Leaf Spot", "Yellow Mosaic"],
        "care_guide": {
            "watering": "Rainfed in Kharif. Ensure soil moisture at pod initiation and seed development stages.",
            "sunlight": "Full direct sun (7–8 hours daily). Optimum temperature 25°C–30°C.",
            "soil": "Deep, fertile, well-drained Black soil (Vertisol) or clay loam with pH 6.5–7.5.",
            "humidity": "High monsoon humidity (65–85%).",
            "nutrition": "NPK 25:60:40 kg/ha + 20 kg/ha Sulfur + 5 kg Zinc Sulfate. Inoculate seed with Bradyrhizobium japonicum."
        },
        "default_management": [
            "Use broad bed and furrow (BBF) or ridge-and-furrow planting to drain excess monsoon rainwater safely.",
            "Spray Hexaconazole 5 EC (1 ml/L) upon detecting initial Asian Soybean Rust pustules on lower leaves."
        ],
        "aliases": ["soybean", "soyabean", "soya", "glycine max", "soya bean"]
    },
    {
        "id": "green_pea",
        "canonical_name": "Field Pea / Green Pea (Matar)",
        "hindi_name": "मटर (Matar)",
        "scientific_name": "Pisum sativum",
        "category": "Pulses & Legumes",
        "indian_season": "Rabi (Oct–Feb in plains; March–Sept in hills)",
        "major_states": "Uttar Pradesh, Madhya Pradesh, Punjab, Bihar, Himachal Pradesh, Rajasthan",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "2–3 light irrigations at pre-flowering and pod filling stages.",
            "sunlight": "Cool sunny winter weather (12°C–20°C).",
            "soil": "Well-drained fertile sandy loam to silt loam with pH 6.0–7.5.",
            "humidity": "Moderate (50–65%).",
            "nutrition": "NPK 20:50:40 kg/ha + 10 tons FYM."
        },
        "default_management": [
            "Spray Wettable Sulfur (2 g/L) or Dinocap (1 ml/L) at first sign of white powdery mildew on foliage.",
            "Harvest tender sweet green pods in morning hours."
        ],
        "aliases": ["pea", "green pea", "matar", "pattani", "batani", "pisum sativum"]
    },
    {
        "id": "horse_gram",
        "canonical_name": "Horse Gram (Kulthi / Hurali)",
        "hindi_name": "कुलथी (Kulthi)",
        "scientific_name": "Macrotyloma uniflorum",
        "category": "Pulses & Legumes",
        "indian_season": "Late Kharif / Early Rabi (Aug–Nov)",
        "major_states": "Karnataka, Tamil Nadu, Andhra Pradesh, Odisha, Uttarakhand, Maharashtra",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "Extreme drought tolerance; thrives on marginal residual moisture.",
            "sunlight": "Full tropical sun.",
            "soil": "Poor, shallow, gravelly red and lateritic soils.",
            "humidity": "Low to moderate humidity.",
            "nutrition": "NPK 15:30:0 kg/ha."
        },
        "default_management": [
            "Excellent soil cover crop preventing hill slope soil erosion during monsoon end.",
            "Valued in Ayurveda for dissolving kidney stones (Ashmarihara)."
        ],
        "aliases": ["horse gram", "kulthi", "hurali", "kollu", "ulavalu", "macrotyloma uniflorum"]
    },
    {
        "id": "cluster_bean",
        "canonical_name": "Cluster Bean / Guar (Gwar Phali)",
        "hindi_name": "ग्वार फली (Gwar Phali)",
        "scientific_name": "Cyamopsis tetragonoloba",
        "category": "Pulses & Legumes",
        "indian_season": "Kharif (July–Nov) & Summer (March–June)",
        "major_states": "Rajasthan (80% of global production), Haryana, Gujarat, Punjab",
        "disease_model_available": False,
        "supported_diseases": [],
        "care_guide": {
            "watering": "High drought resistance; 1–2 supplemental irrigations in dry spells.",
            "sunlight": "Full hot desert sun (8+ hours daily); temperature up to 45°C.",
            "soil": "Sandy, sandy loam arid soils with pH 7.0–8.5.",
            "humidity": "Low humidity (25–45%).",
            "nutrition": "NPK 20:40:20 kg/ha."
        },
        "default_management": [
            "Major industrial crop for Guar Gum (galactomannan) extraction used in food and energy sectors.",
            "Spray Streptocycline (0.1 g/L) + Copper Oxychloride (2 g/L) for Bacterial Blight control."
        ],
        "aliases": ["cluster bean", "guar", "gwar", "gwar phali", "goru chikkudu", "kothavarangai", "cyamopsis tetragonoloba"]
    }
]

print(f"Base dataset configured with {len(PLANTS_DATA)} primary profiles.")
'''
