import datetime
from typing import Dict, Any, List
import numpy as np
from app.ml.model_loader import model_registry
from app.ml.preprocessing import (
    load_and_preprocess_image,
    extract_visual_color_features,
    extract_botanical_feature_vector
)

# Comprehensive Agronomic Knowledge Base for Diverse Plant Species
EXPANDED_CROP_KNOWLEDGE_BASE = {
    # ------------------- ROSE -------------------
    "Rose___healthy": {
        "crop": "Rose (Rosa rubiginosa / hybrid)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 96.0,
        "severity": "None",
        "scientific_name": "Rosa spp.",
        "explanation": "The rose foliage displays vigorous chlorophyll density, healthy serrated margins, and no signs of Diplocarpon black spot or powdery mildew.",
        "recommendations": [
            {"title": "Optimal Sunlight & Airflow", "description": "Ensure at least 6 hours of direct morning sunlight to keep leaf surfaces dry and encourage prolific blooming.", "type": "action"},
            {"title": "Slight Care: Balanced Potassium Feed", "description": "Apply a mild rose fertilizer (NPK 8-12-16) or bone meal around the drip line to support robust bud formation.", "type": "action"},
            {"title": "Deadheading Routine", "description": "Prune spent blooms down to the first 5-leaflet leaf node at a 45-degree angle to stimulate new flower flushes.", "type": "action"},
            {"title": "Preventive Organic Neem Wash", "description": "Apply a light 0.5% cold-pressed neem oil spray once a month during dusk as a protective barrier against aphids and fungal spores.", "type": "organic"},
            {"title": "Base Drip Watering", "description": "Water deeply at ground level in the morning. Avoid wetting rose buds and foliage during evenings.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Maintain 3 feet of open spacing between rose bushes for unimpeded air circulation.",
            "Apply a 2-inch layer of pine bark mulch around the root zone, keeping 3 inches away from the main stem."
        ]
    },
    "Rose___Black_spot": {
        "crop": "Rose (Rosa rubiginosa / hybrid)",
        "condition": "Rose Black Spot (Diplocarpon rosae)",
        "is_healthy": False,
        "default_health": 48.0,
        "severity": "Moderate",
        "scientific_name": "Rosa spp.",
        "explanation": "Black Spot produces circular black spots with feathery, fringed edges on upper leaf surfaces, leading to yellowing chlorosis and premature defoliation.",
        "recommendations": [
            {"title": "Immediate Leaf Sanitation", "description": "Carefully pick off and bag all black-spotted leaves. Thoroughly rake and discard fallen leaves from beneath the bush.", "type": "action"},
            {"title": "Organic Potassium Bicarbonate Spray", "description": "Spray organic potassium bicarbonate or sulfur-based bio-fungicide every 7-10 days to inhibit fungal sporulation.", "type": "organic"},
            {"title": "Pruning Lower Stems", "description": "Prune out dense interior twig growth to increase sunlight penetration and air movement through the center of the bush.", "type": "action"},
            {"title": "Strict Ground Irrigation", "description": "Cease all overhead hose watering immediately. Moisture on rose leaves for more than 7 hours triggers spore germination.", "type": "prevention"},
            {"title": "Fungicidal Protection", "description": "If infection spreads in humid rainy seasons, apply Myclobutanil or copper octanoate per product instructions.", "type": "chemical"}
        ],
        "prevention_tips": [
            "Select black-spot resistant rose cultivars (such as Knock Out or Rugosa varieties) for new plantings.",
            "Sterilize pruning shears between rose bushes with 70% rubbing alcohol."
        ]
    },
    "Rose___Powdery_mildew": {
        "crop": "Rose (Rosa rubiginosa / hybrid)",
        "condition": "Rose Powdery Mildew (Podosphaera pannosa)",
        "is_healthy": False,
        "default_health": 55.0,
        "severity": "Moderate",
        "scientific_name": "Rosa spp.",
        "explanation": "Powdery Mildew appears as a white to light-grey talcum-like powdery fungal coating on young leaves, tender shoots, and developing flower calyxes, causing curling and distortion.",
        "recommendations": [
            {"title": "Milk or Baking Soda Solution", "description": "Spray a 1:9 milk-water foliar mixture or 1 tsp baking soda with horticultural oil in 1 liter of water during bright morning hours.", "type": "organic"},
            {"title": "Prune Distorted Shoot Tips", "description": "Snip off severely curled terminal shoots and dispose of them in sealed refuse bags.", "type": "action"},
            {"title": "Avoid High Nitrogen Feeding", "description": "Cease quick-release nitrogen fertilizers which promote succulent, hyper-susceptible young foliage.", "type": "action"},
            {"title": "Sulfur Dust Application", "description": "Apply wettable sulfur early in the morning when temperatures are below 28°C.", "type": "chemical"}
        ],
        "prevention_tips": [
            "Plant roses in full sunlight locations with good air drainage.",
            "Water early in the day so sunlight dries any incidental moisture."
        ]
    },

    # ------------------- BRINJAL / EGGPLANT -------------------
    "Brinjal___healthy": {
        "crop": "Brinjal / Eggplant (Solanum melongena)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 95.0,
        "severity": "None",
        "scientific_name": "Solanum melongena",
        "explanation": "Brinjal foliage shows broad, well-expanded pubescent leaves with strong vascular turgidity and no evidence of Phomopsis blight or shoot borer damage.",
        "recommendations": [
            {"title": "Slight Care: Organic Mulching", "description": "Apply 2 inches of dried straw or compost mulch around the base to keep root zones evenly moist and prevent weed competition.", "type": "action"},
            {"title": "Balanced Flowering Nutrition", "description": "Top-dress with vermicompost and wood ash (potassium source) when first purple flower buds emerge.", "type": "action"},
            {"title": "Pest Scouting", "description": "Inspect leaf undersides weekly for early flea beetles, aphids, or whiteflies.", "type": "prevention"},
            {"title": "Staking Heavy Plants", "description": "Provide wooden stakes to support heavy branches as developing eggplants gain weight.", "type": "action"}
        ],
        "prevention_tips": [
            "Maintain 2.5 to 3 feet spacing between brinjal rows.",
            "Ensure full sun exposure for 6-8 hours daily."
        ]
    },
    "Brinjal___Phomopsis_blight": {
        "crop": "Brinjal / Eggplant (Solanum melongena)",
        "condition": "Brinjal Phomopsis Blight (Phomopsis vexans)",
        "is_healthy": False,
        "default_health": 44.0,
        "severity": "Moderate",
        "scientific_name": "Solanum melongena",
        "explanation": "Phomopsis Blight creates distinct circular to irregular brown necrotic lesions with concentric rings and pale centers, which can cause leaf blight, stem cankers, and fruit rot.",
        "recommendations": [
            {"title": "Sanitation & Pruning", "description": "Prune and destroy infected lower leaves and blighted stems immediately to arrest pycnidia spore dispersal.", "type": "action"},
            {"title": "Copper Bio-Fungicide Spray", "description": "Apply copper oxychloride (0.25%) or Bordeaux mixture at 10-day intervals during humid vegetative periods.", "type": "organic"},
            {"title": "Improve Drainage", "description": "Ensure no standing water remains around the root collar after irrigation or rain.", "type": "action"},
            {"title": "Seed Treatment & Crop Rotation", "description": "Rotate with non-solanaceous crops (cereals/legumes) for 3 years; use certified disease-free seeds.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Treat seeds with hot water (50°C for 30 minutes) or Trichoderma viride before sowing.",
            "Harvest fruits promptly before over-ripening."
        ]
    },
    "Brinjal___Little_leaf": {
        "crop": "Brinjal / Eggplant (Solanum melongena)",
        "condition": "Brinjal Little Leaf Disease (Phytoplasma)",
        "is_healthy": False,
        "default_health": 35.0,
        "severity": "Severe",
        "scientific_name": "Solanum melongena",
        "explanation": "Little Leaf is a destructive phytoplasma infection transmitted by leafhoppers (*Hishimonus phycitis*), causing leaves to become extremely miniature, pale, and forming a sterile bushy rosette.",
        "recommendations": [
            {"title": "Rogue Out Infected Plants", "description": "Immediately uproot and burn all affected little-leaf plants. They will not bear fruit and act as permanent pathogen reservoirs.", "type": "action"},
            {"title": "Leafhopper Vector Control", "description": "Spray neem seed kernel extract (NSKE 5%) or Imidacloprid (0.3 ml/L) to control leafhopper vectors.", "type": "organic"},
            {"title": "Yellow Sticky Traps", "description": "Install yellow sticky traps (10-12 per acre) across the field to monitor and trap migrating jassid populations.", "type": "prevention"},
            {"title": "Barrier Cropping", "description": "Plant 2-3 rows of tall border crops (maize or sorghum) around brinjal fields to deflect insect vector swarms.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Dip seedlings in Tetracycline hydrochloride solution (500 ppm) for 30 minutes before transplanting.",
            "Keep field borders clear of wild weed hosts."
        ]
    },

    # ------------------- WHEAT -------------------
    "Wheat___healthy": {
        "crop": "Wheat (Triticum aestivum)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 97.0,
        "severity": "None",
        "scientific_name": "Triticum aestivum",
        "explanation": "Wheat blades display uniform deep green coloration, upright blade posture, clean parallel venation, and strong crown tillering without rust pustules.",
        "recommendations": [
            {"title": "Slight Care: Critical Stage Irrigation", "description": "Ensure timely irrigation at Crown Root Initiation (CRI at 21 days) and Flowering stage.", "type": "action"},
            {"title": "Nitrogen Top-Dressing", "description": "Apply split dose of nitrogen before second irrigation to support spikelet development.", "type": "action"},
            {"title": "Weed Management", "description": "Scout and remove broadleaf weeds (*Chenopodium*, *Phalaris minor*) before canopy closure.", "type": "prevention"},
            {"title": "Zinc & Micronutrient Boost", "description": "Foliar spray with 0.5% zinc sulfate + 2% urea if light chlorosis appears in cooler winter periods.", "type": "organic"}
        ],
        "prevention_tips": [
            "Maintain optimal seeding depth of 4-5 cm in well-pulverized seedbed.",
            "Use certified high-yielding rust-resistant varieties."
        ]
    },
    "Wheat___Leaf_rust": {
        "crop": "Wheat (Triticum aestivum)",
        "condition": "Wheat Brown / Leaf Rust (Puccinia triticina)",
        "is_healthy": False,
        "default_health": 52.0,
        "severity": "Moderate",
        "scientific_name": "Triticum aestivum",
        "explanation": "Leaf Rust produces circular to oval orange-brown powdery pustules (uredinia) scattered randomly across upper leaf surfaces, draining plant sugars and lowering grain weight.",
        "recommendations": [
            {"title": "Targeted Triazole Spray", "description": "Apply Propiconazole (Tilt 25 EC at 1 ml/L) or Tebuconazole at first rust pustule detection across the field.", "type": "chemical"},
            {"title": "Avoid Late-Season Excess Nitrogen", "description": "Excessive late nitrogen creates lush, hyper-susceptible blade tissue; maintain balanced potassium.", "type": "action"},
            {"title": "Field Surveillance", "description": "Scout warmer, humid field pockets daily for windblown spore influxes.", "type": "action"},
            {"title": "Resistant Cultivar Adoption", "description": "Sow multi-gene rust-resistant wheat varieties (such as HD-2967, DBW-187, PBW-550) for next season.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Plant wheat synchronously during the optimal regional sowing window.",
            "Eradicate self-sown volunteer wheat plants near field channels."
        ]
    },
    "Wheat___Yellow_rust": {
        "crop": "Wheat (Triticum aestivum)",
        "condition": "Wheat Stripe / Yellow Rust (Puccinia striiformis)",
        "is_healthy": False,
        "default_health": 46.0,
        "severity": "Severe",
        "scientific_name": "Triticum aestivum",
        "explanation": "Yellow Stripe Rust forms characteristic linear bright-yellow stripe pustules running parallel along blade veins, which coalesce and desiccate green leaf tissue rapidly in cool, humid weather.",
        "recommendations": [
            {"title": "Immediate Systemic Spray", "description": "Spray Propiconazole 25 EC (1 ml/L) or Azoxystrobin immediately upon detecting yellow stripe foci.", "type": "chemical"},
            {"title": "Field Hotspot Isolation", "description": "Treat 10-meter boundary zones surrounding initial yellow rust infection pockets.", "type": "action"},
            {"title": "Avoid Excess Irrigation in Cool Foggy Weather", "description": "Delay sprinkler irrigation during extended misty mornings.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Use certified stripe-rust resistant wheat seeds (e.g., HD-3086, DBW-222).",
            "Monitor northern cooler plains and foothill microclimates closely."
        ]
    },

    # ------------------- RICE / PADDY -------------------
    "Rice___healthy": {
        "crop": "Rice / Paddy (Oryza sativa)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 96.0,
        "severity": "None",
        "scientific_name": "Oryza sativa",
        "explanation": "Rice tillers show erect green leaf blades with strong chlorophyll density, uniform vein structure, and no blast lesions or sheath rot.",
        "recommendations": [
            {"title": "Slight Care: Standing Water Depth", "description": "Maintain 2-5 cm of shallow standing water during active tillering and panicle initiation.", "type": "action"},
            {"title": "Potassium Supplementation", "description": "Apply muriate of potash (MOP) in two splits to toughen epidermal leaf cell walls against fungal penetration.", "type": "action"},
            {"title": "Alternate Wetting and Drying (AWD)", "description": "Practice AWD water management to aerate roots and reduce methane emissions.", "type": "organic"},
            {"title": "Routine BPH Scouting", "description": "Part the canopy and inspect stem bases for brown planthopper (BPH) nymphs.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Incorporate zinc sulfate (25 kg/ha) at final land preparation.",
            "Maintain clean bunds free from weed reservoirs."
        ]
    },
    "Rice___Brown_Spot": {
        "crop": "Rice / Paddy (Oryza sativa)",
        "condition": "Rice Brown Spot (Bipolaris oryzae)",
        "is_healthy": False,
        "default_health": 49.0,
        "severity": "Moderate",
        "scientific_name": "Oryza sativa",
        "explanation": "Brown Spot creates oval to circular dark brown lesions with yellow chlorotic halos, frequently associated with potassium deficiency or soil moisture stress.",
        "recommendations": [
            {"title": "Correct Soil Nutrient Deficiencies", "description": "Top-dress with potassium (MOP) and 0.5% zinc sulfate to revitalize root uptake.", "type": "action"},
            {"title": "Foliar Fungicide Spray", "description": "Apply Tricyclazole (75 WP @ 0.6 g/L) or Hexaconazole at early vegetative onset.", "type": "chemical"},
            {"title": "Water Level Stabilization", "description": "Avoid severe drying cycles; maintain steady soil saturation during vegetative phases.", "type": "action"},
            {"title": "Certified Seed Treatment", "description": "Treat seed lots with hot water or Carbendazim (2g/kg seed) before sowing.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Incorporate farmyard manure or green manure to build soil organic matter.",
            "Avoid planting in severely depleted sandy soils without adequate organic amendments."
        ]
    },
    "Rice___Leaf_Blast": {
        "crop": "Rice / Paddy (Oryza sativa)",
        "condition": "Rice Blast (Magnaporthe oryzae)",
        "is_healthy": False,
        "default_health": 38.0,
        "severity": "Severe",
        "scientific_name": "Oryza sativa",
        "explanation": "Rice Blast produces spindle-shaped / diamond-shaped lesions with grey centers and dark brownish-red borders, which expand and girdle leaf blades and neck nodes.",
        "recommendations": [
            {"title": "Targeted Blast Fungicide", "description": "Apply Tricyclazole 75% WP @ 0.6g/L or Isoprothiolane 40% EC @ 1.5ml/L at earliest lesion sighting.", "type": "chemical"},
            {"title": "Split Nitrogen Feeding", "description": "Avoid large single nitrogen doses; split nitrogen into 3-4 applications.", "type": "action"},
            {"title": "Maintain Continuous Shallow Water", "description": "Never allow blast-infected fields to dry out completely as water stress accelerates disease severity.", "type": "action"}
        ],
        "prevention_tips": [
            "Treat seeds with Tricyclazole (2 g/kg seed) prior to nursery germination.",
            "Burn or compost heavily infected stubbles."
        ]
    },

    # ------------------- TOMATO -------------------
    "Tomato___healthy": {
        "crop": "Tomato (Solanum lycopersicum)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 97.0,
        "severity": "None",
        "scientific_name": "Solanum lycopersicum",
        "explanation": "The tomato plant exhibits vibrant green pigmentation, uniform cellular structure, and no visible necrotic lesions or pathogen sporulation.",
        "recommendations": [
            {"title": "Slight Care: Prune Bottom Suckers", "description": "Pinch off non-fruiting lower suckers up to 12 inches off the ground to boost airflow and focus energy into fruit clusters.", "type": "action"},
            {"title": "Maintain Balanced N-P-K", "description": "Continue steady feeding with 5-10-10 or balanced organic compost tea to support fruit development.", "type": "action"},
            {"title": "Consistent Moisture Management", "description": "Provide 1-1.5 inches of water weekly at the base to prevent blossom end rot and fruit cracking.", "type": "action"},
            {"title": "Soil Calcium Maintenance", "description": "Maintain adequate soil calcium through gypsum or bone meal to strengthen fruit skins.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Maintain organic straw mulching to keep root zones evenly cool and moist.",
            "Stake or cage indeterminate tomato vines off damp soil."
        ]
    },
    "Tomato___Early_blight": {
        "crop": "Tomato (Solanum lycopersicum)",
        "condition": "Tomato Early Blight (Alternaria solani)",
        "is_healthy": False,
        "default_health": 45.0,
        "severity": "Moderate",
        "scientific_name": "Solanum lycopersicum",
        "explanation": "Early Blight produces characteristic concentric target-board dark brown spots with yellow chlorotic halos, typically initiating on older lower leaves before spreading upward.",
        "recommendations": [
            {"title": "Remove Affected Lower Foliage", "description": "Prune and safely destroy lower infected leaves to inhibit fungal conidia splash onto upper healthy leaves.", "type": "action"},
            {"title": "Apply Organic Bio-Fungicide", "description": "Spray copper-based fungicide or Bacillus subtilis formulations during cool evening hours to arrest fungal progression.", "type": "organic"},
            {"title": "Drip Irrigation Transition", "description": "Switch from overhead sprinklers to drip irrigation to keep canopy and leaf surfaces strictly dry.", "type": "action"},
            {"title": "Straw Mulching", "description": "Apply 2-3 inches of clean straw mulch around plant bases to prevent soil-borne spore splashing during rain.", "type": "prevention"},
            {"title": "Crop Rotation Protocol", "description": "Avoid planting Solanaceae family crops in this plot for at least 2-3 growing seasons.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Maintain 24-30 inch plant spacing to encourage rapid air circulation and canopy drying.",
            "Disinfect pruning shears between plants with a 70% isopropyl alcohol solution."
        ]
    },
    "Tomato___Late_blight": {
        "crop": "Tomato (Solanum lycopersicum)",
        "condition": "Tomato Late Blight (Phytophthora infestans)",
        "is_healthy": False,
        "default_health": 32.0,
        "severity": "Severe",
        "scientific_name": "Solanum lycopersicum",
        "explanation": "Late Blight is a destructive oomycete pathogen producing rapid water-soaked lesions that turn dark brown to purplish with pale fungal sporulation underneath during high humidity.",
        "recommendations": [
            {"title": "Immediate Isolation & Pruning", "description": "Immediately remove and bag infected stems to prevent aerial spore dissemination across the field.", "type": "action"},
            {"title": "Systemic Targeted Fungicide", "description": "Apply targeted oomycete fungicides (such as Chlorothalonil or Mancozeb) in accordance with local agricultural guidelines.", "type": "chemical"},
            {"title": "Canopy Airflow Enhancement", "description": "Aggressively thin dense suckers and increase inter-row spacing to reduce microclimate humidity.", "type": "action"},
            {"title": "Resistant Cultivar Selection", "description": "Plant certified Late Blight resistant tomato hybrids (e.g., Mountain Magic, Defiant PHR) in subsequent seasons.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Monitor regional weather alerts for humid, cool conditions (15-22°C with high humidity).",
            "Destroy volunteer tomato and potato plants near field margins."
        ]
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato (Solanum lycopersicum)",
        "condition": "Tomato Leaf Mold (Passalora fulva)",
        "is_healthy": False,
        "default_health": 52.0,
        "severity": "Moderate",
        "scientific_name": "Solanum lycopersicum",
        "explanation": "Leaf Mold develops as pale green to yellow chlorotic spots on upper leaf surfaces accompanied by olive-green to brown velvety fungal patches underneath in high greenhouse humidity.",
        "recommendations": [
            {"title": "Lower Greenhouse Humidity", "description": "Increase cross-ventilation and exhaust fans to maintain relative humidity below 85%.", "type": "action"},
            {"title": "Bio-Fungicidal Foliar Wash", "description": "Spray potassium bicarbonate or copper hydroxide targeting the undersides of leaves.", "type": "organic"},
            {"title": "Selective De-leafing", "description": "Remove heavily affected lower foliage up to the lowest fruit truss.", "type": "action"}
        ],
        "prevention_tips": [
            "Heat greenhouse during early morning hours to prevent dew point condensation.",
            "Water early so leaves remain dry through the night."
        ]
    },
    "Tomato___Bacterial_spot": {
        "crop": "Tomato (Solanum lycopersicum)",
        "condition": "Tomato Bacterial Spot (Xanthomonas spp.)",
        "is_healthy": False,
        "default_health": 48.0,
        "severity": "Moderate",
        "scientific_name": "Solanum lycopersicum",
        "explanation": "Bacterial Spot causes small (less than 3mm), dark brown water-soaked angular spots on foliage and raised scabby pustules on fruit skins.",
        "recommendations": [
            {"title": "Copper-Mancozeb Tank Mix", "description": "Apply a combination of fixed copper bactericide and mancozeb for synergistic bacterial suppression.", "type": "chemical"},
            {"title": "Avoid Handling Wet Foliage", "description": "Do not prune, tie, or harvest plants while dew or rain droplets are present to prevent bacterial transmission.", "type": "action"}
        ],
        "prevention_tips": [
            "Use certified hot-water treated or bleach-treated seeds.",
            "Sterilize greenhouse equipment and trellising stakes."
        ]
    },
    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato (Solanum lycopersicum)",
        "condition": "Tomato Septoria Leaf Spot (Septoria lycopersici)",
        "is_healthy": False,
        "default_health": 50.0,
        "severity": "Moderate",
        "scientific_name": "Solanum lycopersicum",
        "explanation": "Septoria produces numerous small circular spots with grey-tan centers and dark brown margins studded with tiny black pycnidia speckles.",
        "recommendations": [
            {"title": "Bottom Leaf Pruning", "description": "Prune all diseased lower foliage up to 18 inches off the ground.", "type": "action"},
            {"title": "Protective Fungicide", "description": "Apply Chlorothalonil or copper octanoate at 7-10 day intervals.", "type": "chemical"}
        ],
        "prevention_tips": [
            "Mulch beds heavily to prevent soil splash.",
            "Maintain 3-year crop rotation away from solanaceous plants."
        ]
    },

    # ------------------- POTATO -------------------
    "Potato___healthy": {
        "crop": "Potato (Solanum tuberosum)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 96.0,
        "severity": "None",
        "scientific_name": "Solanum tuberosum",
        "explanation": "Potato canopy shows strong chlorophyll density, uniform leaflet margins, and no foliar necrosis or mosaic virus mottling.",
        "recommendations": [
            {"title": "Slight Care: Mound Earth Around Stems", "description": "Maintain high soil mounds around stems to shield growing tubers from sunlight (preventing green solanine toxic greening).", "type": "action"},
            {"title": "Consistent Tuber Bulking Water", "description": "Keep soil evenly moist during tuber bulking phase to avoid hollow heart or misshapen potatoes.", "type": "action"},
            {"title": "Preventive Pest Monitoring", "description": "Scout for Colorado potato beetle egg clusters on underside of leaves.", "type": "prevention"},
            {"title": "Potassium Top-Dress", "description": "Supplement with potassium sulfate to enhance tuber starch density and storage life.", "type": "action"}
        ],
        "prevention_tips": [
            "Practice 3-year crop rotations with cereals or legumes.",
            "Ensure rapid soil drainage to avoid tuber rot."
        ]
    },
    "Potato___Early_blight": {
        "crop": "Potato (Solanum tuberosum)",
        "condition": "Potato Early Blight (Alternaria solani)",
        "is_healthy": False,
        "default_health": 50.0,
        "severity": "Moderate",
        "scientific_name": "Solanum tuberosum",
        "explanation": "Identified circular to angular dark brown target-spot lesions on foliage, which can cause premature defoliation and tuber size reduction.",
        "recommendations": [
            {"title": "Foliar Fungicide Application", "description": "Apply copper hydroxide or Azoxystrobin early in the morning when calm conditions prevail.", "type": "chemical"},
            {"title": "Maintain Plant Vigour", "description": "Ensure optimal nitrogen and potassium nutrition; stressed senescing foliage is significantly more vulnerable.", "type": "action"},
            {"title": "Controlled Irrigation Timing", "description": "Irrigate early in the day so foliage completely dries before sunset.", "type": "action"},
            {"title": "Harvest Management", "description": "Allow tuber skin to mature for 2 weeks after vine kill before digging to prevent tuber rot.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Use certified disease-free seed tubers.",
            "Rotate with non-solanaceous crops for 3 years."
        ]
    },
    "Potato___Late_blight": {
        "crop": "Potato (Solanum tuberosum)",
        "condition": "Potato Late Blight (Phytophthora infestans)",
        "is_healthy": False,
        "default_health": 33.0,
        "severity": "Severe",
        "scientific_name": "Solanum tuberosum",
        "explanation": "Late Blight causes large, irregular water-soaked dark brown to black necrotic lesions on leaves and stems, with white mildew sporulation on the underside in damp weather.",
        "recommendations": [
            {"title": "Systemic Fungicide Spray", "description": "Spray Cymoxanil + Mancozeb or Metalaxyl immediately upon first symptom discovery.", "type": "chemical"},
            {"title": "Destroy Blighted Vines", "description": "Desiccate and kill infected vines 2 weeks before harvest to prevent spores washing into soil tubers.", "type": "action"}
        ],
        "prevention_tips": [
            "Plant certified late-blight resistant seed potatoes.",
            "Destroy cull piles and self-sown volunteer potato plants."
        ]
    },

    # ------------------- CORN / MAIZE -------------------
    "Corn___healthy": {
        "crop": "Corn / Maize (Zea mays)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 98.0,
        "severity": "None",
        "scientific_name": "Zea mays",
        "explanation": "Corn foliage displays broad deep green arching leaves, robust stalk diameter, clean veins, and no fungal pustules.",
        "recommendations": [
            {"title": "Slight Care: Knee-High Nitrogen Boost", "description": "Side-dress with urea or organic chicken manure tea when plants reach knee height (V6 stage).", "type": "action"},
            {"title": "Silking Water Priority", "description": "Ensure adequate moisture during tasseling and silking to guarantee complete kernel pollination.", "type": "action"},
            {"title": "Fall Armyworm Scouting", "description": "Inspect central whorls for early signs of pinhole feeding by fall armyworm larvae.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Maintain 75 cm row spacing for optimal light interception.",
            "Incorporate crop residues after harvest to replenish soil organic carbon."
        ]
    },
    "Corn___Common_rust": {
        "crop": "Corn / Maize (Zea mays)",
        "condition": "Corn Common Rust (Puccinia sorghi)",
        "is_healthy": False,
        "default_health": 55.0,
        "severity": "Moderate",
        "scientific_name": "Zea mays",
        "explanation": "Common Rust manifests as small, cinnamon-brown powdery pustules scattered across both upper and lower leaf surfaces, reducing active photosynthetic area.",
        "recommendations": [
            {"title": "Foliar Fungicide Assessment", "description": "Consider strobilurin or triazole fungicides if rust appears before silking on susceptible hybrids.", "type": "chemical"},
            {"title": "Rust-Resistant Hybrids", "description": "Select commercial corn hybrids carrying the Rp resistance gene for future planting.", "type": "prevention"},
            {"title": "Stalk Strength Monitoring", "description": "Scout for stalk cannibalization as severe foliar rust forces plants to draw nutrients from stalks.", "type": "action"},
            {"title": "Early Planting", "description": "Plant early in the season to escape peak mid-summer airborne spore influxes.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Manage field residues through shallow tillage or decomposition enhancers.",
            "Avoid excessive late-season nitrogen applications."
        ]
    },
    "Corn___Northern_Leaf_Blight": {
        "crop": "Corn / Maize (Zea mays)",
        "condition": "Corn Northern Leaf Blight (Exserohilum turcicum)",
        "is_healthy": False,
        "default_health": 44.0,
        "severity": "Severe",
        "scientific_name": "Zea mays",
        "explanation": "Northern Leaf Blight produces long, cigar-shaped elliptical grey-green to tan lesions (up to 15 cm long) that parallel leaf margins, causing extensive premature foliage burning.",
        "recommendations": [
            {"title": "Strobilurin-Triazole Fungicide", "description": "Apply Azoxystrobin + Propiconazole at tasseling (VT stage) if lesions reach the ear leaf.", "type": "chemical"},
            {"title": "Tillage Residue Burial", "description": "Incorporate corn residue deeply after harvest to bury overwintering chlamydospores.", "type": "action"}
        ],
        "prevention_tips": [
            "Plant resistant corn hybrids with Ht genes.",
            "Practice 2-year rotation with soybeans or pulses."
        ]
    },

    # ------------------- APPLE -------------------
    "Apple___healthy": {
        "crop": "Apple (Malus domestica)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 97.0,
        "severity": "None",
        "scientific_name": "Malus domestica",
        "explanation": "Orchard foliage shows glossy green ovate leaves, clean petioles, and no signs of scab or cedar apple rust.",
        "recommendations": [
            {"title": "Slight Care: Tree Basin Mulching", "description": "Maintain organic wood chip mulch around tree basin, keeping 6 inches clear of the trunk.", "type": "action"},
            {"title": "Summer Pruning for Light", "description": "Prune water sprouts and crossing branches to allow sunlight to reach ripening fruit.", "type": "action"},
            {"title": "Foliar Calcium Spray", "description": "Apply calcium chloride foliar sprays during fruit development to prevent bitter pit.", "type": "organic"}
        ],
        "prevention_tips": [
            "Maintain open canopy architecture with central leader pruning.",
            "Rake and destroy fallen leaves in autumn."
        ]
    },
    "Apple___Apple_scab": {
        "crop": "Apple (Malus domestica)",
        "condition": "Apple Scab (Venturia inaequalis)",
        "is_healthy": False,
        "default_health": 50.0,
        "severity": "Moderate",
        "scientific_name": "Malus domestica",
        "explanation": "Apple Scab produces olive-green to velvet black lesions on leaf surfaces and fruit skins, causing leaf drop and corky fruit blemishes.",
        "recommendations": [
            {"title": "Sanitation of Fallen Orchard Leaves", "description": "Rake, shred, or spray fallen leaves with urea (5%) in autumn to accelerate fungal pseudothecia decomposition.", "type": "action"},
            {"title": "Protective Fungicide Schedule", "description": "Apply sulfur or captan sprays from green tip through petal fall according to Mills scab infection periods.", "type": "organic"},
            {"title": "Canopy Pruning for Light & Air", "description": "Open tree canopy via structural pruning to ensure leaves dry within 6 hours following rainfall.", "type": "action"},
            {"title": "Plant Scab-Immune Cultivars", "description": "Choose scab-immune varieties (e.g., Liberty, Enterprise, Freedom) for new orchard blocks.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Prune diseased shoots during winter dormancy.",
            "Maintain weed-free tree rows to lower relative humidity."
        ]
    },
    "Apple___Black_rot": {
        "crop": "Apple (Malus domestica)",
        "condition": "Apple Black Rot (Botryosphaeria obtusa)",
        "is_healthy": False,
        "default_health": 45.0,
        "severity": "Moderate",
        "scientific_name": "Malus domestica",
        "explanation": "Black Rot causes 'frog-eye' leaf spots (small circular brown lesions with purple margins) and black mummified rotting fruit.",
        "recommendations": [
            {"title": "Prune Out Cankered Twigs", "description": "Prune all dead wood and fire-blight cankers 6 inches below visible infection.", "type": "action"},
            {"title": "Remove Mummified Fruit", "description": "Pick off and dispose of all shriveled mummies hanging from branches.", "type": "action"}
        ],
        "prevention_tips": [
            "Apply captan sprays during petal fall.",
            "Keep trees vigorous with balanced fertilization."
        ]
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple (Malus domestica)",
        "condition": "Cedar Apple Rust (Gymnosporangium juniperi-virginianae)",
        "is_healthy": False,
        "default_health": 53.0,
        "severity": "Moderate",
        "scientific_name": "Malus domestica",
        "explanation": "Cedar Apple Rust produces bright yellow-orange spots on the upper leaf surface with tiny black pycnia in the center and tube-like aecia underneath.",
        "recommendations": [
            {"title": "Protective Myclobutanil Spray", "description": "Apply Myclobutanil or Mancozeb from pink bud stage through petal fall.", "type": "chemical"},
            {"title": "Remove Nearby Juniper Galls", "description": "Remove cedar galls from eastern red cedar/juniper trees within 500 feet of the orchard.", "type": "action"}
        ],
        "prevention_tips": [
            "Plant rust-resistant apple varieties (e.g., Redfree, Prima).",
            "Maintain wide tree spacing."
        ]
    },

    # ------------------- COTTON -------------------
    "Cotton___healthy": {
        "crop": "Cotton (Gossypium hirsutum)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 96.0,
        "severity": "None",
        "scientific_name": "Gossypium spp.",
        "explanation": "Cotton leaves display healthy 3-5 palmate lobing, deep green pigmentation, intact leaf nectaries, and vigorous square development.",
        "recommendations": [
            {"title": "Slight Care: Square & Boll Retention", "description": "Foliar spray with 1% potassium nitrate (KNO3) during peak flowering to prevent square shedding.", "type": "action"},
            {"title": "Inter-Cultivation for Aeration", "description": "Perform shallow hoeing to break crusting and enhance root respiration.", "type": "action"},
            {"title": "Whitefly & Aphid Trapping", "description": "Install yellow sticky traps at canopy level.", "type": "prevention"},
            {"title": "Irrigation & Drainage Management", "description": "Ensure furrow irrigation prevents waterlogging during squaring and boll formation phases.", "type": "action"}
        ],
        "prevention_tips": [
            "Avoid excess nitrogen fertilizer which attracts sucking pests.",
            "Maintain ridge-and-furrow planting for proper drainage."
        ]
    },
    "Cotton___Bacterial_blight": {
        "crop": "Cotton (Gossypium hirsutum)",
        "condition": "Cotton Bacterial Blight / Angular Leaf Spot (Xanthomonas citri)",
        "is_healthy": False,
        "default_health": 45.0,
        "severity": "Moderate",
        "scientific_name": "Gossypium spp.",
        "explanation": "Bacterial Blight causes angular, water-soaked lesions bounded by leaf veinlets that turn dark brown to black (blackarm phase on stems).",
        "recommendations": [
            {"title": "Copper Oxychloride + Streptocycline", "description": "Spray Copper Oxychloride (0.25%) mixed with Streptocycline (100 ppm) at first sign of angular spotting.", "type": "chemical"},
            {"title": "Acid Delinting of Seeds", "description": "Ensure planting seeds are acid-delinted to destroy seed-coat bacterial colonies.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Sow certified resistant cotton hybrids.",
            "Burn crop residues after final picking."
        ]
    },

    # ------------------- MANGO -------------------
    "Mango___healthy": {
        "crop": "Mango (Mangifera indica)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 97.0,
        "severity": "None",
        "scientific_name": "Mangifera indica",
        "explanation": "Mango leaves show thick, leathery, dark green lanceolate blades with prominent midribs and no anthracnose spotting or powdery mildew.",
        "recommendations": [
            {"title": "Slight Care: Post-Harvest Pruning", "description": "Prune dead wood and overcrowded central branches to allow 360-degree sunlight penetration into the canopy.", "type": "action"},
            {"title": "Micronutrient Spray", "description": "Foliar spray with 0.2% Borax and 0.5% Zinc Sulfate before flower panicle emergence.", "type": "organic"},
            {"title": "Mango Hopper Monitoring", "description": "Inspect underside of leaves and young flower panicles during spring flush.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Apply neem cake (2-3 kg/tree) in the drip ring.",
            "Keep orchard floor free from rotting fallen fruit."
        ]
    },
    "Mango___Anthracnose": {
        "crop": "Mango (Mangifera indica)",
        "condition": "Mango Anthracnose (Colletotrichum gloeosporioides)",
        "is_healthy": False,
        "default_health": 48.0,
        "severity": "Moderate",
        "scientific_name": "Mangifera indica",
        "explanation": "Anthracnose produces circular to angular dark brown-to-black necrotic spots on young foliage, blossom blight on panicles, and tear-stain rot on fruit.",
        "recommendations": [
            {"title": "Pre-Bloom Copper Spray", "description": "Spray copper oxychloride (3 g/L) or Carbendazim (1 g/L) at flower bud emergence and fruit set.", "type": "chemical"},
            {"title": "Prune Diseased Twigs", "description": "Prune infected twig tips 2 inches into healthy green wood after harvest.", "type": "action"}
        ],
        "prevention_tips": [
            "Dip harvested mangoes in hot water (52°C for 5 minutes) to prevent storage decay.",
            "Maintain open tree canopy to reduce humidity."
        ]
    },

    # ------------------- CUCUMBER / GOURD -------------------
    "Cucumber___healthy": {
        "crop": "Cucumber (Cucumis sativus)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 95.0,
        "severity": "None",
        "scientific_name": "Cucumis sativus",
        "explanation": "Cucumber vines exhibit broad triangular-ovate rough foliage, strong tendrils, and clean yellow blossoms without downy mildew angular spots.",
        "recommendations": [
            {"title": "Slight Care: Vertical Trellising", "description": "Train cucumber vines upward onto vertical netting or bamboo trellises to keep fruits and leaves off wet soil.", "type": "action"},
            {"title": "Drip Irrigation Under Mulch", "description": "Water via drip lines beneath plastic mulch to prevent any leaf wetting.", "type": "action"},
            {"title": "Pollinator Protection", "description": "Avoid spraying during morning hours when honeybees and wild pollinators are visiting yellow female flowers.", "type": "prevention"}
        ],
        "prevention_tips": [
            "Maintain 2 feet between plants on the trellis.",
            "Rotate vine crops away from the same soil bed for 2 years."
        ]
    },
    "Cucumber___Downy_mildew": {
        "crop": "Cucumber (Cucumis sativus)",
        "condition": "Cucumber Downy Mildew (Pseudoperonospora cubensis)",
        "is_healthy": False,
        "default_health": 42.0,
        "severity": "Severe",
        "scientific_name": "Cucumis sativus",
        "explanation": "Downy Mildew produces distinct angular bright yellow chlorotic spots delimited by major leaf veins, with purple-grey downy sporulation on the underside.",
        "recommendations": [
            {"title": "Targeted Oomycete Fungicide", "description": "Apply Cyazofamid or Fluopicolide + Mancozeb immediately upon detecting angular yellow patches.", "type": "chemical"},
            {"title": "Improve Canopy Aeration", "description": "Thin lower foliage to reduce relative humidity inside vine tunnels.", "type": "action"}
        ],
        "prevention_tips": [
            "Grow downy-mildew resistant slicing/pickling hybrids.",
            "Cease all late-afternoon overhead watering."
        ]
    },

    # ------------------- GRAPE -------------------
    "Grape___healthy": {
        "crop": "Grape (Vitis vinifera)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 96.0,
        "severity": "None",
        "scientific_name": "Vitis vinifera",
        "explanation": "Grape leaves exhibit healthy 3-5 palmate lobing, deep emerald green foliage, clean serrated margins, and vigorous shoot cane elongation.",
        "recommendations": [
            {"title": "Slight Care: Canopy Shoot Positioning", "description": "Tuck shoots into trellis wires to maximize leaf exposure to full sun.", "type": "action"},
            {"title": "Defoliation Around Fruit Zone", "description": "Pluck 2-3 leaves around ripening grape clusters to accelerate color development.", "type": "action"}
        ],
        "prevention_tips": [
            "Maintain dormant winter spray with lime sulfur.",
            "Ensure weed-free vineyard floor."
        ]
    },
    "Grape___Black_rot": {
        "crop": "Grape (Vitis vinifera)",
        "condition": "Grape Black Rot (Guignardia bidwellii)",
        "is_healthy": False,
        "default_health": 47.0,
        "severity": "Moderate",
        "scientific_name": "Vitis vinifera",
        "explanation": "Black Rot produces small circular reddish-brown spots with dark borders and tiny black pycnidia on leaves, turning berries into shriveled hard black mummies.",
        "recommendations": [
            {"title": "Myclobutanil or Mancozeb Spray", "description": "Apply protectant fungicide from early shoot emergence through 4 weeks post-bloom.", "type": "chemical"},
            {"title": "Remove Grape Mummies", "description": "Prune and destroy all mummified grape clusters from canes and ground.", "type": "action"}
        ],
        "prevention_tips": [
            "Prune out diseased canes during winter.",
            "Keep canopy open for rapid drying."
        ]
    },
    "Grape___Leaf_blight": {
        "crop": "Grape (Vitis vinifera)",
        "condition": "Grape Leaf Blight (Isariopsis clavispora)",
        "is_healthy": False,
        "default_health": 51.0,
        "severity": "Moderate",
        "scientific_name": "Vitis vinifera",
        "explanation": "Identified irregular brown necrotic blotches with dark halos on mature leaves, causing premature autumn defoliation and weakened canes.",
        "recommendations": [
            {"title": "Copper Bio-Fungicide", "description": "Apply copper hydroxide or Bordeaux mixture post-harvest to protect foliage.", "type": "organic"},
            {"title": "Rake Fallen Leaves", "description": "Collect and compost or burn fallen infected leaves.", "type": "action"}
        ],
        "prevention_tips": [
            "Maintain balanced potassium nutrition.",
            "Avoid excessive late-season nitrogen."
        ]
    },

    # ------------------- PEPPER / CHILLI -------------------
    "Pepper___healthy": {
        "crop": "Chilli / Bell Pepper (Capsicum annuum)",
        "condition": "Healthy & Thriving Foliage",
        "is_healthy": True,
        "default_health": 96.0,
        "severity": "None",
        "scientific_name": "Capsicum annuum",
        "explanation": "Chilli foliage shows smooth, glossy, deep green ovate-lanceolate leaves with clean margins, healthy white flower buds, and firm branching.",
        "recommendations": [
            {"title": "Slight Care: Calcium & Boron Spray", "description": "Foliar spray 0.2% calcium nitrate + 0.1% Borax during flowering to prevent flower drop and blossom end rot.", "type": "action"},
            {"title": "Moisture Consistency", "description": "Maintain steady soil moisture; irregular drying cycles cause blossom drop in peppers.", "type": "action"},
            {"title": "Thrips & Mite Scouting", "description": "Inspect young terminal leaves for upward leaf curling caused by thrips or yellow mites.", "type": "prevention"},
            {"title": "Potassium Supplementation", "description": "Top dress with potassium sulfate (0-0-50) at early fruit set to increase pod wall thickness and pungency/sweetness.", "type": "action"},
            {"title": "Preventive Organic Neem Wash", "description": "Apply cold-pressed neem oil (3 ml/L) once a month during evening hours to repel whiteflies and aphids.", "type": "organic"}
        ],
        "prevention_tips": [
            "Install blue sticky traps for thrips monitoring.",
            "Apply silver reflective mulch to repel sucking pests."
        ]
    },

    "Pepper___Bacterial_spot": {
        "crop": "Chilli / Bell Pepper (Capsicum annuum)",
        "condition": "Pepper Bacterial Spot (Xanthomonas campestris)",
        "is_healthy": False,
        "default_health": 48.0,
        "severity": "Moderate",
        "scientific_name": "Capsicum annuum",
        "explanation": "Bacterial Spot produces small (1-3mm) circular to irregular dark brown water-soaked lesions with yellow halos that cause severe leaf defoliation and rough scabby spots on peppers.",
        "recommendations": [
            {"title": "Copper + Mancozeb Application", "description": "Apply copper hydroxide tank-mixed with mancozeb every 7-10 days during rainy spells.", "type": "chemical"},
            {"title": "Avoid Overhead Sprinklers", "description": "Use drip irrigation exclusively to eliminate splash transmission.", "type": "action"}
        ],
        "prevention_tips": [
            "Plant resistant pepper varieties (e.g., cultivars with Bs2 gene).",
            "Treat seeds with 20% bleach solution for 15 minutes before sowing."
        ]
    }
}

class CropInferenceService:
    @staticmethod
    def _match_species_heuristically(features: dict, feature_vector: np.ndarray) -> str:
        """
        Botanical multi-feature matching engine:
        Evaluates floral color, leaf texture, linearity, aspect ratio, serration, and disease signatures
        to identify the exact plant species and health condition.
        """
        rose_pink = features["rose_pink_ratio"]
        violet = features["violet_ratio"]
        linear_blade = features["linear_blade_index"]
        aspect_ratio = features["aspect_ratio"]
        green = features["green_ratio"]
        deep_green = features["deep_green_ratio"]
        yellow_green = features["yellow_green_ratio"]
        yellow = features["yellow_ratio"]
        brown = features["brown_ratio"]
        white_mildew = features["white_mildew_ratio"]
        gradient = features["gradient_magnitude"]
        serration = float(feature_vector[33]) if len(feature_vector) > 33 else 0.1
        vert_dom = float(feature_vector[32]) if len(feature_vector) > 32 else 1.0

        # 1. ROSE DETECTION (Sharp serrated margins, compound leaflets, deep emerald / pink / bronze traces)
        if serration > 0.35 or rose_pink > 0.03 or (deep_green > 0.18 and gradient > 16.0 and vert_dom < 1.4):
            if white_mildew > 0.04:
                return "Rose___Powdery_mildew"
            elif brown > 0.06 or yellow > 0.08:
                return "Rose___Black_spot"
            else:
                return "Rose___healthy"

        # 2. BRINJAL / EGGPLANT DETECTION (Violet/purple anthocyanin hues, broad fuzzy foliage)
        if violet > 0.03 or (green > 0.20 and violet > 0.01 and gradient < 24.0 and vert_dom < 1.3):
            if yellow > 0.15:
                return "Brinjal___Little_leaf"
            elif brown > 0.07:
                return "Brinjal___Phomopsis_blight"
            else:
                return "Brinjal___healthy"

        # 3. WHEAT / RICE / CEREAL BLADE DETECTION (High linear blade index, narrow elongated aspect ratio)
        if vert_dom > 2.0 or aspect_ratio > 2.0 or linear_blade > 1.8:
            if yellow_green > 0.20:
                # Rice tends to have higher lighter yellow-green hues
                if brown > 0.06 or yellow > 0.10:
                    return "Rice___Brown_Spot"
                else:
                    return "Rice___healthy"
            else:
                # Wheat has deeper green erect blades
                if brown > 0.06 or yellow > 0.10:
                    return "Wheat___Leaf_rust"
                else:
                    return "Wheat___healthy"

        # 4. CORN / MAIZE DETECTION (Wide strap-like leaves with parallel venation)
        if vert_dom > 1.5 and aspect_ratio > 1.4 and green > 0.30:
            if brown > 0.08:
                return "Corn___Common_rust"
            else:
                return "Corn___healthy"

        # 5. CUCUMBER / GOURD (Broad triangular leaves with yellow-green tint and rough texture)
        if yellow_green > 0.25 and gradient > 18.0:
            if yellow > 0.15:
                return "Cucumber___Downy_mildew"
            return "Cucumber___healthy"

        # 6. MANGO / APPLE (Dark leathery glossy foliage)
        if deep_green > 0.30:
            if brown > 0.08:
                return "Apple___Apple_scab"
            else:
                return "Mango___healthy"

        # 7. COTTON (Palmate lobed structure)
        if green > 0.30 and serration > 0.15:
            return "Cotton___healthy"

        # 8. TOMATO & POTATO (Solanaceous compound foliage)
        if brown > 0.14:
            return "Tomato___Late_blight"
        elif brown > 0.07 or yellow > 0.12:
            return "Tomato___Early_blight"
        elif green > 0.35:
            return "Tomato___healthy"
        else:
            return "Potato___healthy"

    @staticmethod
    def analyze_crop_image(image_bytes: bytes) -> Dict[str, Any]:
        """
        Executes crop species identification using the trained ML ensemble, calculates
        precise Health % and damage severity %, and outputs agronomic remedies or growth adjustments.
        """
        features_vec = extract_botanical_feature_vector(image_bytes)
        features = extract_visual_color_features(image_bytes)
        now_iso = datetime.datetime.utcnow().isoformat()
        
        # Calculate dynamic Health % and Damage %
        health_pct = float(features["health_percentage"])
        damage_pct = float(features["damage_severity_percentage"])

        model = model_registry.get_model("crop_disease")
        predicted_key = None
        # No real-photo holdout evaluation is included in this project archive.
        # Start with no confidence rather than presenting a made-up high score.
        confidence = 0.0
        model_status = "visual_rule_based_unvalidated"

        # Check botanical distinct traits
        rose_pink = features["rose_pink_ratio"]
        violet = features["violet_ratio"]
        linear_blade = features["linear_blade_index"]
        serration = float(features_vec[33]) if len(features_vec) > 33 else 0.1

        if model is not None:
            try:
                # 1. Check if model is joblib ensemble
                if hasattr(model, "predict_proba"):
                    probs = np.array(model.predict_proba([features_vec])[0], dtype=np.float32)
                    classes = model_registry.get_classes("crop_disease")

                    # Use the model's output without domain-prior multipliers or
                    # confidence floors. Its scores are not validated/calibrated on
                    # real field photographs, so the response carries a disclaimer.
                    prob_sum = float(np.sum(probs))
                    if not np.isfinite(prob_sum) or prob_sum <= 0:
                        raise ValueError("Classifier returned invalid probability scores")
                    probs = probs / prob_sum
                    top_idx = int(np.argmax(probs))
                    confidence = float(probs[top_idx])
                    
                    if top_idx < len(classes):
                        predicted_key = classes[top_idx]
                        model_status = "unvalidated_feature_vector_model"

                elif hasattr(model, "predict"): # Keras model
                    processed = load_and_preprocess_image(image_bytes)
                    predictions = model.predict(processed, verbose=0)[0]
                    top_idx = int(predictions.argmax())
                    confidence = float(predictions[top_idx])
                    
                    classes = model_registry.get_classes("crop_disease")
                    if top_idx < len(classes):
                        predicted_key = classes[top_idx]
                        model_status = "unvalidated_cnn_model"
            except Exception as e:
                print(f"[WARN] Error in crop ML model inference: {e}")

        if not predicted_key or predicted_key not in EXPANDED_CROP_KNOWLEDGE_BASE:
            predicted_key = CropInferenceService._match_species_heuristically(features, features_vec)
            # A handcrafted colour/shape fallback is a candidate generator, not a
            # measured disease diagnosis; never attach a high confidence score.
            confidence = 0.0
            model_status = "visual_rule_based_unvalidated"

        kb_data = EXPANDED_CROP_KNOWLEDGE_BASE.get(
            predicted_key,
            EXPANDED_CROP_KNOWLEDGE_BASE["Tomato___healthy"]
        )

        is_healthy = kb_data["is_healthy"]
        
        # These are colour-feature estimates, not measured plant pathology.
        # Do not force artificial health/damage floors based on the predicted label.
        health_score = round(float(np.clip(health_pct, 0.0, 100.0)), 1)
        damage_score = round(float(np.clip(damage_pct, 0.0, 100.0)), 1)
        severity = kb_data["severity"] if not is_healthy else "Not confirmed by laboratory/field diagnosis"

        limitations = (
            "Screening limitation: the supplied archive does not contain a verified, "
            "real-field-photo validation set for this disease model. The candidate and "
            "colour-based health/damage scores are not a confirmed diagnosis or calibrated "
            "probability. Confirm symptoms with a local agricultural extension officer/KVK "
            "before applying any crop-protection chemical."
        )
        explanation = f"{kb_data['explanation']}\n\n{limitations}"
        recommendations = [
            rec for rec in kb_data["recommendations"]
            if str(rec.get("type", "")).lower() != "chemical"
        ]
        recommendations.append({
            "title": "Confirm before treatment",
            "description": "Compare symptoms with an agricultural extension officer or KVK and follow only locally registered product labels. A visual model result alone is not enough to select a pesticide.",
            "type": "info"
        })

        return {
            "isAgricultural": True,
            "predictedCrop": kb_data["crop"],
            "predictedCondition": kb_data["condition"],
            "isHealthy": is_healthy,
            "healthPercentage": health_score,
            "damageSeverityPercentage": damage_score,
            "confidence": round(confidence, 4),
            "severityLevel": severity,
            "explanation": explanation,
            "recommendations": recommendations,
            "preventionTips": kb_data["prevention_tips"],
            "scientificName": kb_data["scientific_name"],
            "modelStatus": model_status,
            "analysisTimestamp": now_iso
        }

