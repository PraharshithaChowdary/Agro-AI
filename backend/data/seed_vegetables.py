"""
AGRO AI — Indian Vegetables Seed Data
Contains verified records for Tomato, Potato, Onion, Garlic, Brinjal, Chilli, Okra,
Cabbage, Cauliflower, Spinach, Amaranth, Coriander, Fenugreek, Cucumber, Pumpkin,
Bottle Gourd, Bitter Gourd, Ridge Gourd, Snake Gourd, Drumstick, Radish, Carrot,
Beetroot, Peas, and Beans.
"""

import json
from pathlib import Path
from generate_verified_seed_catalog import make_plant, DATA_DIR

def get_vegetables():
    return [
        make_plant(
            "solanum-lycopersicum", "Solanum lycopersicum", "Tomato", "टमाटर (Tamatar)",
            "టమాటా (Tamata)", "தக்காளி (Thakkali)",
            {"kannada": "ಟೊಮೆಟೊ (Tomato)", "malayalam": "തക്കാളി (Thakkali)", "bengali": "টমেটো (Tomato)", "marathi": "टोमॅटो (Tomato)"},
            ["Lycopersicon esculentum"], "Solanaceae", "Solanum", "lycopersicum", "vegetable", "cultivated",
            ["Andhra Pradesh", "Madhya Pradesh", "Karnataka", "Gujarat", "Odisha", "West Bengal", "Maharashtra", "Bihar"],
            "Imparipinnate compound with 5–9 lobed glandular-pubescent ovate leaflets", "Alternate", "Dentate to lobed", "Pinnate", "Medium to dark green, pungent solanaceous aroma",
            "Herbaceous, branched, glandular-hairy, erect or decumbent, 0.5–2.0 m",
            "Cymes of yellow 5-lobed star-shaped flowers with reflexed petals",
            "Fleshy berry, globose or pyriform, ripening from green to lustrous red",
            "Erect to sprawling short-lived perennial herb grown as annual, 60–180 cm",
            "Warm temperate to sub-tropical climate, frost-sensitive, optimal 20°C–27°C",
            "Full sun (6–8 hours daily)", "Regular moderate watering; avoid wetting foliage",
            "Well-drained fertile sandy loam to clay loam rich in organic matter, pH 6.0–7.0",
            "Autumn-Winter (Rabi), Spring-Summer, and Rainy (Kharif)", ["Seed nursery transplanting (25–30 days)"],
            ["Fresh culinary fruit/vegetable, curries, chutneys, salads", "Commercial processing: purees, sauces, ketchups, lycopene extract"],
            "Green unripe leaves and stems contain tomatine and solanine alkaloids. Do not consume foliage.", False,
            [
                {"name": "Early Blight (Alternaria solani)", "type": "fungal", "symptoms": "Concentric target-board rings on older lower leaves with yellow halo", "management": "Foliar Mancozeb (2 g/L) or Azoxystrobin"},
                {"name": "Late Blight (Phytophthora infestans)", "type": "fungal", "symptoms": "Water-soaked dark lesions rapidly turning necrotic with white fungal down on leaf undersides", "management": "Metalaxyl + Mancozeb (2.5 g/L) spray"},
                {"name": "Tomato Leaf Curl Virus (ToLCV)", "type": "viral", "symptoms": "Severe upward leaf curling, puckering, vein clearing, stunted bushy growth", "management": "Control whitefly vector with Imidacloprid (0.3 ml/L); grow ToLCV-resistant hybrids"}
            ],
            ["Stake indeterminate plants with bamboo trellising", "Mulch around roots with straw to prevent soil splashing", "Avoid overhead irrigation"]
        ),
        make_plant(
            "solanum-tuberosum", "Solanum tuberosum", "Potato", "आलू (Aloo)",
            "బంగాళాదుంప (Bangaladumpa)", "உருளைக்கிழங்கு (Urulaikizhangu)",
            {"kannada": "ಆಲೂಗಡ್ಡೆ (Aaloogadde)", "malayalam": "ഉരുളക്കിഴങ്ങ് (Urulakkizhangu)", "bengali": "আলু (Aloo)", "marathi": "बटाटा (Batata)"},
            [], "Solanaceae", "Solanum", "tuberosum", "vegetable", "cultivated",
            ["Uttar Pradesh", "West Bengal", "Bihar", "Gujarat", "Madhya Pradesh", "Punjab", "Assam"],
            "Pinnately compound with alternate large and small ovate leaflets", "Alternate", "Entire", "Pinnate", "Dark green with soft pubescence",
            "Herbaceous branched aerial stems rising from underground rhizomatous stolons, 30–80 cm",
            "White, pink, or purplish star-shaped flowers with yellow stamens",
            "Underground modified stem tuber with 'eyes' (buds); aerial small green poisonous berry",
            "Erect to spreading annual tuberous herb, 30–80 cm",
            "Cool winter climate; requires night temperature of 15°C–20°C for tuberization",
            "Full sun", "Moderate; regular light irrigations until 10 days before harvest",
            "Loose, friable well-drained fertile sandy loam with high organic humus, pH 5.2–6.5",
            "Rabi (October/November to January/February)", ["Sprouted seed tuber pieces with eyes"],
            ["World's major non-cereal carbohydrate staple", "Boiled, fried, curries (aloo paratha, samosa, chips)"],
            "Green potatoes and sprouted shoots contain toxic solanine. Never eat green tubers.", False,
            [
                {"name": "Late Blight (Phytophthora infestans)", "type": "fungal", "symptoms": "Dark water-soaked lesions on leaf tips turning black, purplish white mildew underneath", "management": "Prophylactic Mancozeb spray; Cymoxanil + Mancozeb at infection"},
                {"name": "Early Blight (Alternaria solani)", "type": "fungal", "symptoms": "Brown target-ring spots on leaves", "management": "Chlorothalonil or Mancozeb"}
            ],
            ["Earth up ridges twice (at 25 and 45 DAS) to prevent tubers from greening under sunlight", "Use certified disease-free seed tubers (Kufri Pukhraj, Kufri Jyoti)"]
        ),
        make_plant(
            "allium-cepa", "Allium cepa", "Onion", "प्याज़ (Pyaz)",
            "ఉల్లిపాయ (Ullipaya)", "வெங்காயம் (Vengayam)",
            {"kannada": "ಈರುಳ್ಳಿ (Eerulli)", "malayalam": "സവാള / ഉള്ളി (Savala)", "bengali": "পেঁয়াজ (Penyaj)", "marathi": "कांदा (Kanda)"},
            [], "Amaryllidaceae", "Allium", "cepa", "vegetable", "cultivated",
            ["Maharashtra", "Madhya Pradesh", "Karnataka", "Gujarat", "Rajasthan", "Bihar", "Andhra Pradesh", "Tamil Nadu"],
            "Hollow, cylindrical (fistular) glaucous leaves with flattened upper surface", "Alternate, basal distichous", "Entire", "Parallel", "Glaucous bluish-green",
            "Reduced underground discoid stem plate bearing concentric fleshy leaf sheaths forming bulb",
            "Dense terminal globose umbel on hollow flowering scape, small white or greenish flowers",
            "3-valved capsule holding small angled black seeds",
            "Biennial bulb-forming herb grown as annual, 30–60 cm",
            "Mild temperate to subtropical climate; requires warm dry weather for bulb curing",
            "Full sunlight (6–8 hours)", "Frequent light irrigations; withhold water 15 days before harvest",
            "Well-drained loose fertile sandy loam or silty loam rich in humus, pH 6.0–7.5",
            "Kharif, Late Kharif, and Rabi", ["Seedling transplanting (6–8 week old) or small bulblets (sets)"],
            ["Essential culinary foundation across all Indian cuisines", "Raw in salads, cooked in gravies, dehydrated flakes", "Natural source of quercetin and organosulfur compounds"],
            "Safe for human nutrition. Toxic to dogs and cats.", False,
            [
                {"name": "Purple Blotch (Alternaria porri)", "type": "fungal", "symptoms": "Sunken whitish flecks turning purple-brown with yellow borders on leaves", "management": "Foliar Mancozeb (2.5 g/L) or Tebuconazole"},
                {"name": "Thrips (Thrips tabaci)", "type": "pest", "symptoms": "Silver mottling and distortion of leaves caused by sap-sucking nymphs", "management": "Spray Fipronil 5 SC (1 ml/L) or spinosad"}
            ],
            ["Cure harvested bulbs in shade for 10–12 days before storage", "Plant on raised beds to avoid collar rot"]
        ),
        make_plant(
            "allium-sativum", "Allium sativum", "Garlic", "लहसुन (Lahsun)",
            "వెల్లుల్లి (Vellulli)", "பூண்டு (Poondu)",
            {"kannada": "ಬೆಳ್ಳುಳ್ಳಿ (Bellulli)", "malayalam": "വെളുത്തുള്ളി (Veluthulli)", "bengali": "রসুন (Roshun)", "marathi": "लसूण (Lasun)"},
            [], "Amaryllidaceae", "Allium", "sativum", "vegetable", "cultivated",
            ["Madhya Pradesh", "Rajasthan", "Gujarat", "Uttar Pradesh", "Maharashtra", "Odisha"],
            "Flat, solid, linear-lanceolate keeled blades with distinct midline fold", "Alternate, basal distichous", "Entire", "Parallel", "Greyish green",
            "Flattened basal stem plate bearing 10–25 fleshy cloves (bulblets) enclosed in papery tunic",
            "Small whitish flowers and bulbils in terminal umbel on solid flowering scape",
            "Capsule (rarely sets fertile seed)",
            "Perennial bulbous herb grown as annual, 30–60 cm",
            "Cool winter climate for vegetative growth, followed by warm dry weather for bulb maturation",
            "Full sun", "Regular light irrigations; stop 2 weeks prior to harvest",
            "Rich, friable loamy soil with high organic matter and good drainage, pH 6.0–7.5",
            "Rabi (October–November to March–April)", ["Planting individual healthy cloves with tip facing up"],
            ["Universal aromatic culinary seasoning and spice", "Medicinal: cardioprotective, lowers blood pressure, antimicrobial (allicin)"],
            "Safe for human consumption. Toxic to pets (dogs and cats).", False,
            [
                {"name": "Purple Blotch", "type": "fungal", "symptoms": "Purplish oval lesions on foliage", "management": "Mancozeb (2 g/L) + sticker"},
                {"name": "Stem & Bulb Nematode", "type": "pest", "symptoms": "Stunted, twisted swollen foliage", "management": "Crop rotation with non-host crops"}
            ],
            ["Select bold exterior cloves for planting", "Dip cloves in carbendazim (1 g/L) before planting"]
        ),
        make_plant(
            "solanum-melongena", "Solanum melongena", "Brinjal / Eggplant / Aubergine", "बैंगन (Baingan)",
            "వంకాయ (Vankaya)", "கத்தரிக்காய் (Kathirikkai)",
            {"kannada": "ಬದನೆಕಾಯಿ (Badanekayi)", "malayalam": "വഴുതനങ്ങ (Vazhuthananga)", "bengali": "বেগুন (Begun)", "marathi": "वांगे (Vange)"},
            [], "Solanaceae", "Solanum", "melongena", "vegetable", "cultivated",
            ["West Bengal", "Odisha", "Gujarat", "Madhya Pradesh", "Bihar", "Karnataka", "Maharashtra", "Andhra Pradesh"],
            "Large, ovate to oblong coarsely lobed pubescent leaves; sometimes prickly along veins", "Alternate", "Coarsely lobed to sinuate", "Pinnate", "Dull greyish green with starry pubescence",
            "Herbaceous, semi-woody branching erect stem, often equipped with spines, 0.6–1.5 m",
            "Solitary or clustered violet-purple star-shaped flowers with prominent yellow anthers",
            "Large fleshy pendulous berry, spherical to oblong, glossy purple, green, or variegated",
            "Semi-woody erect perennial herb grown as annual, 60–150 cm",
            "Warm tropical and subtropical seasons; highly susceptible to frost",
            "Full sun (6–8 hours)", "Regular moderate irrigation",
            "Deep fertile well-drained silt loam to clay loam, pH 5.5–6.8",
            "All three seasons (Kharif, Rabi, Summer)", ["Seedling transplanting (4–5 week old)"],
            ["Major Indian vegetable; curries (baingan bharta, gutti vankaya, sambar)", "Rich in dietary fiber, polyphenols, and nasunin antioxidant"],
            "Raw green fruit and leaves contain solanine; consume cooked.", False,
            [
                {"name": "Shoot and Fruit Borer (Leucinodes orbonalis)", "type": "pest", "symptoms": "Wilted drooping shoot tips in vegetative stage; bore holes and frass in fruits", "management": "Clip wilted shoots weekly; install sex pheromone traps (10/acre); spray Chlorantraniliprole 18.5 SC (0.4 ml/L)"},
                {"name": "Phomopsis Blight", "type": "fungal", "symptoms": "Circular brown leaf spots with pycnidia; soft rot on fruits", "management": "Spray Zineb or Copper Oxychloride"},
                {"name": "Little Leaf of Brinjal", "type": "phytoplasma", "symptoms": "Extremely reduced tiny clustered leaves, phyllody, bush-like appearance", "management": "Rogue infected plants; control vector leafhopper with Dimethoate"}
            ],
            ["Adopt regular clipping of infested shoots every 7 days", "Intercrop with Coriander or Fennel to attract beneficial predators"]
        ),
        make_plant(
            "capsicum-annuum", "Capsicum annuum", "Chilli / Hot Pepper", "मिर्च (Mirch)",
            "మిరపకాయ (Mirapakaya)", "பச்சை மிளகாய் (Pachai Milagai)",
            {"kannada": "ಮೆಣಸಿನಕಾಯಿ (Menasinakayi)", "malayalam": "പച്ചമുളക് (Pachamulaku)", "bengali": "লঙ্কা (Lanka)", "marathi": "मिरची (Mirchi)"},
            ["Capsicum frutescens"], "Solanaceae", "Capsicum", "annuum", "vegetable", "cultivated",
            ["Andhra Pradesh", "Telangana", "Karnataka", "Madhya Pradesh", "Maharashtra", "Gujarat", "West Bengal"],
            "Simple, ovate to elliptic lanceolate smooth leaves with acute apex", "Alternate", "Entire", "Pinnate", "Lustrous bright to dark green",
            "Herbaceous to semi-woody angular erect branched stem, 40–120 cm",
            "Small solitary or paired white star-shaped flowers with purplish-blue anthers",
            "Pungent elongate berry with persistent green calyx, turning green to fiery red",
            "Erect branching subshrub grown as annual, 40–120 cm",
            "Warm tropical and sub-tropical climate; 20°C–30°C optimal for fruit set",
            "Full sunlight (6–8 hours)", "Regular moderate moisture; sensitive to both waterlogging and drought stress",
            "Well-drained light loamy and black soils with good aeration, pH 6.0–7.5",
            "Kharif, Rabi, and Summer", ["Seedling nursery transplanting (30–35 days)"],
            ["Essential spice imparting pungency and color (capsaicin, capsanthin)", "Green chillies fresh in food; red dry chillies powdered for curries", "Industrial oleoresin extraction"],
            "Capsaicin causes intense burning sensation on skin and eyes. Wear gloves during harvest/processing.", False,
            [
                {"name": "Chilli Leaf Curl Virus (ChiLCV)", "type": "viral", "symptoms": "Upward curling of leaves, puckering, reduction of leaf blade, bushy stunted plant", "management": "Whitefly vector management with Diafenthiuron 50 WP (1 g/L); yellow sticky traps (15/acre)"},
                {"name": "Anthracnose / Die-back (Colletotrichum capsici)", "type": "fungal", "symptoms": "Necrotic black spots on mature fruits with concentric rings; terminal twigs dry from top down", "management": "Spray Azoxystrobin (1 ml/L) or Copper Oxychloride (2.5 g/L)"},
                {"name": "Thrips and Mites Complex", "type": "pest", "symptoms": "Upward cup-like leaf curling (thrips) or downward boat-like curling (mites)", "management": "Fipronil 5 SC (1.5 ml/L) or Spiromesifen 22.9 SC (1 ml/L)"}
            ],
            ["Install yellow and blue sticky traps (20 each/ha)", "Practice border cropping with maize or sorghum to impede vector entry"]
        ),
        make_plant(
            "abelmoschus-esculentus", "Abelmoschus esculentus", "Okra / Lady's Finger / Bhindi", "भिंडी (Bhindi)",
            "బెండకాయ (Bendakaya)", "வெண்டைக்காய் (Vendaikkai)",
            {"kannada": "ಬೆಂಡೆಕಾಯಿ (Bendekayi)", "malayalam": "വെണ്ടയ്ക്ക (Vendakka)", "bengali": "ঢেঁড়শ (Dhyarosh)", "marathi": "भेंडी (Bhendi)"},
            ["Hibiscus esculentus"], "Malvaceae", "Abelmoschus", "esculentus", "vegetable", "cultivated",
            ["Gujarat", "West Bengal", "Bihar", "Madhya Pradesh", "Andhra Pradesh", "Odisha", "Maharashtra"],
            "Large palmately 5–7 lobed cordate leaves with rough hispid hairs", "Alternate", "Coarsely serrate / toothed", "Palmate", "Vibrant green with prominent light green veins",
            "Erect semi-woody fibrous stem with hispid bristly hairs, 1.0–2.0 m",
            "Large showy solitary yellow flowers with dark crimson-purple center",
            "Elongate 5–8 ridged beaked mucilaginous capsule containing spherical seeds",
            "Stout erect annual fibrous herb, 1.0–2.2 meters",
            "Warm tropical and sub-tropical climate; optimal temperature 24°C–35°C",
            "Full sunshine (8 hours)", "Regular weekly irrigations during dry periods",
            "Loose fertile sandy loam to clay loam rich in organic matter, pH 6.0–7.5",
            "Kharif (June–July) and Summer (February–March)", ["Direct seed line sowing"],
            ["Tender pods cooked as vegetable (bhindi masala, sambar, kurkuri bhindi)", "Mucilage used as clarifying agent in sugarcane jaggery making"],
            "Surface hairs may cause mild contact skin irritation during harvest.", False,
            [
                {"name": "Yellow Vein Mosaic Virus (YVMV)", "type": "viral", "symptoms": "Vein clearing turning completely yellow, whole leaf chlorotic with stunted growth and fibrous yellow pods", "management": "Cultivate resistant varieties (Parbhani Kranti, Arka Anamika); spray Acetamiprid against whitefly"},
                {"name": "Fruit Borer (Earias vittella)", "type": "pest", "symptoms": "Bored holes plugged with excreta in fruits, deformed twisted pods", "management": "Pheromone traps; spray Spinosad 45 SC (0.3 ml/L)"}
            ],
            ["Soak seeds in water for 12 hours before sowing for uniform germination", "Pick pods every 2–3 days while tender (8–10 cm length)"]
        ),
        make_plant(
            "moringa-oleifera", "Moringa oleifera", "Drumstick / Moringa / Sahjan", "सहजन / मुनगा (Sahjan)",
            "మునగకాయ (Munagakaya)", "முருங்கைக்காய் (Murungaikkai)",
            {"kannada": "ನುಗ್ಗೆಕಾಯಿ (Nuggekayi)", "malayalam": "മുരിങ്ങക്കായ (Muringakka)", "bengali": "সজনে ডাঁটা (Sojne data)", "marathi": "शेवगा (Shevga)"},
            ["Moringa pterygosperma"], "Moringaceae", "Moringa", "oleifera", "vegetable", "cultivated",
            ["Tamil Nadu", "Andhra Pradesh", "Karnataka", "Telangana", "Gujarat", "Maharashtra", "Odisha"],
            "Tripinnate compound feathery leaves with small obovate leaflets", "Alternate", "Entire", "Pinnate", "Bright lush green",
            "Soft-wooded, corky whitish-grey bark with brittle branches, 4–10 m",
            "Fragrant yellowish-white bisexual flowers in spreading drooping panicles",
            "Long, 3-sided pendulous pendular ribbed pods (20–60 cm) with 3-winged seeds",
            "Fast-growing soft-wooded deciduous perennial tree, 4–10 m",
            "Tropical and sub-tropical semi-arid climate; exceptionally drought resilient",
            "Full sun", "Low to moderate once established",
            "Well-drained sandy loam or alluvial soil; avoids waterlogging",
            "Perennial fruiting twice a year", ["Air layering, seeds, or limb cuttings (PKM-1, PKM-2)"],
            ["Pods cooked in sambar and curries", "Leaves highly nutritious superfood (rich in vitamin A, C, calcium, iron)", "Purifying water with seed powder"],
            "Root bark contains alkaloids (moringinine); avoid excessive root ingestion.", False,
            [
                {"name": "Hairy Caterpillar (Eupterote mollifera)", "type": "pest", "symptoms": "Massive nocturnal swarms defoliating tree canopy, congregating on trunk", "management": "Collect egg masses; flame congregate colonies on trunk; spray Dichlorvos"}
            ],
            ["Pinch main shoot at 1 m height to stimulate multiple bushy fruiting laterals", "Harvest pods before seeds become hard"]
        ),
        make_plant(
            "brassica-oleracea-capitata", "Brassica oleracea var. capitata", "Cabbage / Patta Gobhi", "पत्ता गोभी (Patta Gobhi)",
            "క్యాబేజీ (Cabbage)", "முட்டைக்கோஸ் (Muttaikkose)",
            {"kannada": "ಕೋಸು (Kosu)", "malayalam": "മുട്ടക്കോസ് (Muttakkos)", "bengali": "বাঁধাকপি (Badhakopi)", "marathi": "कोबी (Kobi)"},
            [], "Brassicaceae", "Brassica", "oleracea", "vegetable", "cultivated",
            ["West Bengal", "Odisha", "Bihar", "Madhya Pradesh", "Gujarat", "Karnataka", "Assam"],
            "Broad, fleshy, glaucous obovate leaves tightly packed into a dense compact spherical head", "Basal spiral rosette", "Wavy, dentate", "Pinnate", "Glaucous light green to bluish green",
            "Short, thickened fleshy stem supporting the terminal compact head",
            "Yellow 4-petaled cross-shaped flowers on elongated flowering raceme (second year)",
            "Slender cylindrical 2-valved silique with spherical dark brown seeds",
            "Biennial herbaceous vegetable grown as annual head crop, 30–50 cm",
            "Cool temperate to sub-tropical winter climate; optimal head formation at 15°C–20°C",
            "Full sun (6 hours)", "Moderate regular moisture; avoid water stress during head formation",
            "Rich, fertile loamy soil with high moisture retention and good drainage, pH 6.0–6.8",
            "Rabi (Winter season in plains, year-round in hills)", ["Seedling nursery transplanting (25–30 days)"],
            ["Fresh salad, stir-fries, curries, sabzi, coleslaw", "Rich source of Vitamin C, K, and indole-3-carbinol"],
            "Wash thoroughly to remove surface insects.", False,
            [
                {"name": "Diamondback Moth (Plutella xylostella)", "type": "pest", "symptoms": "Larvae skeletonize leaves leaving transparent parchment-like patches and shot holes", "management": "Install pheromone traps (5/acre); spray Bacillus thuringiensis (Bt @ 1 g/L) or Spinosad"},
                {"name": "Black Rot (Xanthomonas campestris pv. campestris)", "type": "bacterial", "symptoms": "Characteristic V-shaped yellow chlorotic lesions from leaf margins with blackened veinlets", "management": "Seed treatment with hot water (50°C for 30 min) + Streptocycline (100 ppm)"}
            ],
            ["Use mustard as trap crop (sow 2 rows of mustard for every 25 rows of cabbage)", "Harvest firm heads before bursting occurs"]
        ),
        make_plant(
            "brassica-oleracea-botrytis", "Brassica oleracea var. botrytis", "Cauliflower / Phool Gobhi", "फूल गोभी (Phool Gobhi)",
            "క్యాలీఫ్లవర్ (Cauliflower)", "காலிஃபிளவர் (Cauliflower)",
            {"kannada": "ಹೂಕೋಸು (Hukosu)", "malayalam": "കോളിഫ്ലവർ (Cauliflower)", "bengali": "ফুলকপি (Phulkopi)", "marathi": "फ्लॉवर (Flower)"},
            [], "Brassicaceae", "Brassica", "oleracea", "vegetable", "cultivated",
            ["Bihar", "Uttar Pradesh", "West Bengal", "Madhya Pradesh", "Odisha", "Gujarat", "Haryana", "Punjab"],
            "Long, oblong-elliptic erect leaves with prominent pale midrib enclosing curd", "Rosette", "Entire to slightly dentate", "Pinnate", "Dark grey-green with glaucous waxy bloom",
            "Short, stout fleshy unbranched stem terminating in dense hypertrophied inflorescence",
            "Compact dense aborted pre-floral fleshy curd made of tightly packed meristems",
            "Silique with small globose seeds (produced only when curd bolts)",
            "Annual cool-season herbaceous crop, 40–60 cm",
            "Cool, moist climate; sensitive to both extreme cold and hot dry spells during curd initiation",
            "Full sun", "Regular uniform irrigation; sensitive to drought during curd development",
            "Deep fertile well-drained sandy loam or clay loam rich in organic matter, pH 6.0–7.0",
            "Rabi (Early, mid, and late varieties spanning September to March)", ["Seedling nursery transplanting"],
            ["Staple winter vegetable (aloo gobhi, gobhi paratha, mixed vegetable, pakoras)", "Rich in choline, antioxidants, glucosinolates"],
            "Safe for consumption.", False,
            [
                {"name": "Buttoning", "type": "physiological", "symptoms": "Development of tiny, premature button-like curds due to transplanting aged seedlings or nitrogen deficiency", "management": "Transplant 25-day old vigorous seedlings; apply balanced nitrogen"},
                {"name": "Whiptail", "type": "physiological", "symptoms": "Leaf blades fail to expand properly leaving only thin distorted midribs like whip tails (Molybdenum deficiency in acidic soils)", "management": "Liming acidic soil; foliar spray of Sodium Molybdate (1 g/L)"}
            ],
            ["Blanch curds by tying outer leaves over developing curd to keep it creamy white", "Harvest compact heads before curds loosen (riciness)"]
        ),
        make_plant(
            "spinacia-oleracea", "Spinacia oleracea", "Spinach / Palak", "पालक (Palak)",
            "పాలకూర (Palakura)", "பசலைக் கீரை (Pasalai Keerai)",
            {"kannada": "ಪಾಲಕ್ ಸೊಪ್ಪು (Palak Soppu)", "malayalam": "പാലക്ക് ചീര (Palak Cheera)", "bengali": "পালং শাক (Palong Shaak)", "marathi": "पालक (Palak)"},
            [], "Amaranthaceae", "Spinacia", "oleracea", "vegetable", "cultivated",
            ["Uttar Pradesh", "West Bengal", "Maharashtra", "Punjab", "Gujarat", "Andhra Pradesh", "Karnataka"],
            "Fleshy, succulent ovate to triangular-hastate tender leaves with long petiole", "Basal rosette", "Entire to wavy sinuate", "Pinnate", "Glossy dark green",
            "Short crown stem during vegetative phase; rapidly elongates into hollow flowering scape in long days",
            "Dioecious; small inconspicuous greenish flowers in axillary clusters",
            "Small hard spiny or smooth utricle enclosing round seed",
            "Fast-growing cool-season annual leafy green, 20–40 cm",
            "Cool climate; easily bolts (premature flowering) in hot long summer days",
            "Full sun to light afternoon shade", "Regular frequent light irrigations; keep soil moist",
            "Fertile, moisture-retentive sandy loam or silt loam high in organic matter, pH 6.5–7.5",
            "Winter (September–November) and early Spring", ["Direct line sowing in beds"],
            ["Nutrient-dense leafy green; palak paneer, dal palak, saag, smoothies", "High source of dietary iron, folate, lutein, and Vitamin K"],
            "Contains oxalates. People prone to calcium-oxalate kidney stones should boil and drain cooking water.", False,
            [
                {"name": "Downy Mildew (Peronospora effusa)", "type": "fungal", "symptoms": "Yellowish chlorotic angular spots on upper leaf surface, purplish grey downy mold beneath", "management": "Spray Metalaxyl or Mancozeb; ensure good plant spacing for air circulation"}
            ],
            ["Multi-cut harvesting: cut outer leaves 2 cm above crown every 12–15 days for continuous yield", "Provide well-decomposed vermicompost"]
        ),
        make_plant(
            "amaranthus-cruentus", "Amaranthus cruentus", "Amaranth / Chaulai / Thotakura", "चौलाई (Chaulai)",
            "తోటకూర (Thotakura)", "முளைக்கீரை / அரைக்கீரை (Keerai)",
            {"kannada": "ದಂಟು ಸೊಪ್ಪು (Dantu Soppu)", "malayalam": "ചീര (Cheera)", "bengali": "নটে শাক (Note Shaak)", "marathi": "राजगिरा / माठ (Rajgira / Math)"},
            ["Amaranthus paniculatus"], "Amaranthaceae", "Amaranthus", "cruentus", "vegetable", "cultivated",
            ["Andhra Pradesh", "Tamil Nadu", "Kerala", "Karnataka", "West Bengal", "Maharashtra", "Odisha"],
            "Broad ovate to rhomboid-elliptic leaves with long petioles, green or deep burgundy-red", "Alternate", "Entire", "Pinnate", "Green, red, or variegated green-purple",
            "Erect, grooved, fleshy succulent branching stem, 0.5–1.5 meters",
            "Dense feathery terminal and axillary spikes with tiny flowers and colorful bracts",
            "Circumscissile capsule with tiny lenticular glossy black or pale cream seeds",
            "Fast-growing erect C4 annual herbaceous leafy vegetable, 50–150 cm",
            "Warm tropical and sub-tropical plains; rapid 25–40 day harvest cycle",
            "Full sun", "Moderate; responds well to light regular irrigation",
            "Well-drained fertile loamy soils rich in organic matter, pH 6.0–7.5",
            "Year-round in southern India; Summer and Kharif in North", ["Direct seed broadcast or line sowing"],
            ["Popular leafy vegetable (saag, thotakura fry, sambar)", "Grain amaranth (rajgira) consumed on fasting days; complete protein with lysine"],
            "Safe for consumption.", False,
            [
                {"name": "White Rust (Albugo bliti)", "type": "fungal", "symptoms": "White pustules on lower leaf surface with yellow patches on upper surface", "management": "Spray Mancozeb (2 g/L); remove infected leaves"}
            ],
            ["Mix fine seeds with sand (1:4 ratio) for even sowing", "Harvest tender shoots when 15–20 cm tall"]
        ),
        make_plant(
            "coriandrum-sativum", "Coriandrum sativum", "Coriander / Cilantro / Dhania", "धनिया (Dhania)",
            "కొత్తిమీర (Kothimeera)", "கொத்தமல்லி (Kothamalli)",
            {"kannada": "ಕೊತ್ತಂಬರಿ (Kothambari)", "malayalam": "മല്ലിയില (Malliyila)", "bengali": "ধনে পাতা (Dhone pata)", "marathi": "कोथिंबीर (Kothimbir)"},
            [], "Apiaceae", "Coriandrum", "sativum", "herb", "cultivated",
            ["Madhya Pradesh", "Rajasthan", "Gujarat", "Andhra Pradesh", "Telangana", "Karnataka", "Tamil Nadu"],
            "Dimorphic: lower leaves pinnately lobed with fan-like segments; upper leaves finely dissected into filiform linear segments", "Alternate", "Incised / dissected", "Reticulate", "Vibrant aromatic green",
            "Slender, erect hollow branching glabrous stem, 30–70 cm",
            "Compound umbels of small white to pale pink asymmetrical flowers",
            "Globose ribbed schizocarp splitting into two aromatic mericarps (coriander seeds)",
            "Erect aromatic annual herb, 30–70 cm",
            "Cool, dry winter climate for vegetative greens; dry warm sunny weather for seed setting",
            "Full sun to light partial shade", "Frequent light irrigations; avoids dry soil",
            "Well-drained rich loamy soil with good moisture holding capacity, pH 6.0–7.5",
            "Rabi and early Spring (year-round in mild climates)", ["Crushed split seed (mericarps) sowing"],
            ["Universal fresh garnish in Indian cookery (kothimeera, dhania chutney)", "Aromatic dry spice powder (dhania powder) forming core curry base"],
            "Safe for human diet.", False,
            [
                {"name": "Powdery Mildew (Erysiphe polygoni)", "type": "fungal", "symptoms": "White talcum-like powdery coating over leaves and umbels preventing seed fill", "management": "Spray Wettable Sulfur (2 g/L) or Dinocap"},
                {"name": "Stem Gall (Protomyces macrosporus)", "type": "fungal", "symptoms": "Tumor-like swellings and galls on stems, pedicels, and fruits", "management": "Seed treatment with Thiram (3 g/kg)"}
            ],
            ["Gently crush seeds into halves before sowing to promote rapid emergence", "Sow in succession every 15 days for continuous fresh greens"]
        ),
        make_plant(
            "trigonella-foenum-graecum", "Trigonella foenum-graecum", "Fenugreek / Methi", "मेथी (Methi)",
            "మెంతులు (Menthulu)", "வெந்தயம் (Vendhayam)",
            {"kannada": "ಮೆಂತ್ಯ (Menthya)", "malayalam": "ഉലുവ (Uluva)", "bengali": "মেথি (Methi)", "marathi": "मेथी (Methi)"},
            [], "Fabaceae", "Trigonella", "foenum-graecum", "herb", "cultivated",
            ["Rajasthan", "Gujarat", "Madhya Pradesh", "Uttar Pradesh", "Maharashtra", "Punjab"],
            "Trifoliolate compound leaves with obovate to wedge-shaped leaflets", "Alternate", "Denticulate towards apex", "Pinnate", "Fresh medium green",
            "Erect or spreading smooth branched herbaceous stem, 30–60 cm",
            "Sessile solitary or paired yellowish-white to pale lilac papilionaceous flowers",
            "Slender curved beaked pod (10–15 cm) holding 10–20 rhombic golden-yellow seeds",
            "Erect annual legume herb, 30–60 cm",
            "Cool, dry winter climate; frost tolerant",
            "Full sun", "Moderate light irrigations every 7–10 days",
            "Well-drained fertile loamy to clay loam soils, pH 6.0–7.5",
            "Rabi (October–November to February–March)", ["Direct seed line sowing"],
            ["Fresh leafy greens (methi thepla, aloo methi, methi paratha)", "Aromatic bitter seeds for tempering, pickles, sambar powder", "Rich in soluble fiber (galactomannan) for blood sugar management"],
            "Safe for human nutrition.", False,
            [
                {"name": "Powdery Mildew", "type": "fungal", "symptoms": "White powder on foliage", "management": "Wettable sulfur (2 g/L)"},
                {"name": "Downy Mildew", "type": "fungal", "symptoms": "Yellow leaf patches with downy growth beneath", "management": "Mancozeb spray"}
            ],
            ["First harvest of tender greens (kasuri methi) at 25–30 days; subsequent cuts every 15 days"]
        ),
        make_plant(
            "cucumis-sativus", "Cucumis sativus", "Cucumber / Khira / Kakdi", "खीरा / ककड़ी (Khira / Kakdi)",
            "దోసకాయ (Dosakaya)", "வெள்ளரிக்காய் (Vellarikkai)",
            {"kannada": "ಸೌತೆಕಾಯಿ (Southekayi)", "malayalam": "വെള്ളരിക്ക (Vellarikka)", "bengali": "শসা (Shosha)", "marathi": "काकडी (Kakdi)"},
            [], "Cucurbitaceae", "Cucumis", "sativus", "vegetable", "cultivated",
            ["Uttar Pradesh", "Karnataka", "Madhya Pradesh", "West Bengal", "Andhra Pradesh", "Telangana", "Punjab", "Haryana"],
            "Large, triangular-cordate palmately 3–5 lobed leaves with rough hispid hairs", "Alternate", "Dentate serrate", "Palmate", "Rich medium green",
            "Trailing or climbing rough hairy ridged vine with simple unbranched tendrils, 1.5–3.0 m",
            "Monoecious: bright yellow bell-shaped 5-lobed flowers; female flowers have inferior ovary resembling mini cucumber",
            "Elongate cylindrical pepo with smooth or tuberculate skin, green turning yellowish",
            "Annual climbing or sprawling rough herbaceous vine, 1.5–3.0 meters",
            "Warm sub-tropical and tropical seasons; optimal temperature 22°C–32°C",
            "Full sun (6–8 hours)", "Regular uniform irrigation; irregular watering causes fruit bitterness (cucurbitacins)",
            "Fertile, loose, well-drained sandy loam rich in organic manure, pH 6.0–7.0",
            "Summer (Zaid) and Rainy (Kharif)", ["Direct pit sowing or protected plug trays"],
            ["Fresh hydrating salad vegetable (contains 95% water)", "Cooling raita, pickles, detox juice", "Skincare and eye compress"],
            "Bitter cucumbers containing excessive cucurbitacins should not be consumed in large amounts.", False,
            [
                {"name": "Downy Mildew (Pseudoperonospora cubensis)", "type": "fungal", "symptoms": "Angular yellow chlorotic lesions delimited by leaf veins with purplish-grey sporulation beneath", "management": "Spray Cymoxanil + Mancozeb (2 g/L) or Metalaxyl"},
                {"name": "Powdery Mildew (Podosphaera xanthii)", "type": "fungal", "symptoms": "Talc-like white circular powder covering leaf surfaces", "management": "Spray Wettable Sulfur or Azoxystrobin"}
            ],
            ["Trellis vines on bower or vertical net system to keep fruits straight and unblemished", "Ensure active bee pollination or use gynoecious parthenocarpic hybrids"]
        ),
        make_plant(
            "cucurbita-moschata", "Cucurbita moschata", "Pumpkin / Kaddu / Sitaphal", "कद्दू / कुम्हड़ा (Kaddu)",
            "గుమ్మడికాయ (Gummadikaya)", "பூசணிக்காய் (Poosanikkai)",
            {"kannada": "ಕುಂಬಳಕಾಯಿ (Kumbalakayi)", "malayalam": "മത്തങ്ങ (Matthanga)", "bengali": "মিষ্টি কুমড়ো (Misti Kumro)", "marathi": "भोपळा (Bhopla)"},
            [], "Cucurbitaceae", "Cucurbita", "moschata", "vegetable", "cultivated",
            ["West Bengal", "Odisha", "Uttar Pradesh", "Bihar", "Tamil Nadu", "Kerala", "Karnataka", "Madhya Pradesh"],
            "Broad, shallowly 5-lobed cordate leaves with soft velvety hairs and white silvery mottling along vein junctions", "Alternate", "Denticulate", "Palmate", "Medium to dark green with distinctive white silvery blotches",
            "Robust trailing or climbing angular grooved vine with branched tendrils, 3–8 meters",
            "Large showy bright yellow-orange bell-shaped flowers with spreading reflexed lobes",
            "Large variable pepo (globose, depressed, ribbed) with thick rind; orange flesh and white flat seeds",
            "Vigorous sprawling perennial vine grown as warm-season annual, 3–10 m",
            "Warm tropical and subtropical climate; heat tolerant",
            "Full sun", "Deep irrigation at 7–10 day intervals; avoid wetting foliage",
            "Well-drained fertile sandy loam to clay loam rich in compost, pH 6.0–7.5",
            "Summer and Rainy (Kharif) seasons", ["Direct seed pit sowing on mounds"],
            ["Nutritious yellow vegetable rich in beta-carotene; kaddu ki sabzi, sambar, kheer", "Seeds roasted as zinc-rich pepitas snack", "Tender leaf shoots cooked in Bengali/Odia cuisine"],
            "Safe for human nutrition.", False,
            [
                {"name": "Fruit Fly (Bactrocera cucurbitae)", "type": "pest", "symptoms": "Punctures on young fruits causing oozing of fluid, decay, and rotting", "management": "Install cue-lure pheromone traps (10/acre); cover young fruits with paper bags"},
                {"name": "Mosaic Virus", "type": "viral", "symptoms": "Mottling, blistered leaf texture, distorted fruits", "management": "Control aphid vectors; rogue infected vines"}
            ],
            ["Apply 10 kg farmyard manure per pit before sowing", "Harvest mature fruits with intact pedicel for long storage up to 6 months"]
        ),
        make_plant(
            "lagenaria-siceraria", "Lagenaria siceraria", "Bottle Gourd / Lauki / Ghiya", "लौकी / घिया (Lauki)",
            "సొరకాయ / ఆనపకాయ (Sorakaya)", "சுரைக்காய் (Suraikkai)",
            {"kannada": "ಸೋರೆಕಾಯಿ (Sorekayi)", "malayalam": "ചുരയ്ക്ക (Churakka)", "bengali": "লাউ (Lau)", "marathi": "दुधी भोपळा (Dudhi Bhopla)"},
            [], "Cucurbitaceae", "Lagenaria", "siceraria", "vegetable", "cultivated",
            ["Uttar Pradesh", "Bihar", "Madhya Pradesh", "West Bengal", "Haryana", "Andhra Pradesh", "Tamil Nadu"],
            "Large, reniform to cordate shallowly lobed velvety leaves with two distinct glands on petiole apex", "Alternate", "Repand to denticulate", "Palmate", "Pale to bright green with soft velvety pubescence",
            "Vigorous ridged climbing or trailing pubescent vine with 2-branched tendrils, 3–6 m",
            "Showy solitary white nocturnal flowers with crinkled petals opening at dusk",
            "Variable elongated cylindrical or bottle-shaped smooth light-green pepo with white spongy flesh",
            "Vigorous annual climbing or sprawling herbaceous vine, 3–8 m",
            "Warm sub-tropical and tropical climate; frost sensitive",
            "Full sun", "Regular weekly irrigation",
            "Fertile, rich well-drained sandy loam with good moisture retention, pH 6.0–7.5",
            "Summer (Zaid) and Rainy (Kharif)", ["Direct pit sowing"],
            ["Light, highly digestible cooling vegetable (lauki ki sabzi, lauki kheer, kofta)", "Ayurvedic rejuvenating vegetable; dried hard rinds traditionally used as musical instruments (tanpura, sitar, ektara)"],
            "HEALTH WARNING: If bottle gourd juice tastes unusually bitter, DO NOT DRINK IT. Extremely bitter juice contains toxic cucurbitacins which cause severe gastrointestinal hemorrhaging.", False,
            [
                {"name": "Anthracnose (Colletotrichum orbiculare)", "type": "fungal", "symptoms": "Circular water-soaked lesions on leaves turning brown, sunken fruit spots", "management": "Spray Mancozeb (2 g/L) or Carbendazim (1 g/L)"}
            ],
            ["Grow on overhead bower / pandal trellises to ensure straight, blemish-free hanging fruits"]
        ),
        make_plant(
            "momordica-charantia", "Momordica charantia", "Bitter Gourd / Karela", "करेला (Karela)",
            "కాకరకాయ (Kakarakaya)", "பாகற்காய் (Pavakkai)",
            {"kannada": "ಹಾಗಲಕಾಯಿ (Hagalakayi)", "malayalam": "പാവയ്ക്ക (Pavakka)", "bengali": "করলা / উচ্ছে (Korola)", "marathi": "कारले (Karle)"},
            [], "Cucurbitaceae", "Momordica", "charantia", "vegetable", "cultivated",
            ["Maharashtra", "Gujarat", "Andhra Pradesh", "Telangana", "Kerala", "Tamil Nadu", "West Bengal", "Odisha"],
            "Palmately 5–7 deeply lobed leaves with slender petioles and characteristic pungent aroma", "Alternate", "Dentate to lobed", "Palmate", "Bright vibrant green",
            "Slender, grooved puberulent climbing vine with simple unbranched tendrils, 2–4 m",
            "Solitary yellow 5-petaled flowers with rounded bract on pedicel",
            "Oblong-fusiform pepo covered with prominent warty ridges, green turning orange-yellow when ripe with red arils",
            "Annual slender climbing herbaceous vine, 2–4 meters",
            "Warm tropical and subtropical climate; heat loving",
            "Full sun (6–8 hours)", "Regular light watering; avoid water stagnation",
            "Well-drained sandy loam rich in organic matter, pH 6.0–7.0",
            "Summer (February–March) and Monsoon (June–July)", ["Direct pit sowing with presoaked seeds"],
            ["Renowned bitter vegetable (bharwan karela, karela chips, theeyal)", "Medicinal: potent hypoglycemic properties (charantin, vicine, polypeptide-p) aiding diabetes control"],
            "Safe when cooked. Red arils of overripe fruit are mildly toxic to young children in large quantities.", False,
            [
                {"name": "Downy Mildew", "type": "fungal", "symptoms": "Yellow angular leaf spots", "management": "Metalaxyl + Mancozeb spray"},
                {"name": "Fruit Fly (Bactrocera cucurbitae)", "type": "pest", "symptoms": "Maggots inside fruit causing rotting", "management": "Cue-lure pheromone traps (10/ha)"}
            ],
            ["Soak hard seeds in warm water for 24 hours to accelerate germination", "Train vines on vertical wire trellis"]
        ),
        make_plant(
            "luffa-acutangula", "Luffa acutangula", "Ridge Gourd / Torai / Turai", "तोरी / तोरई (Torai)",
            "బీరకాయ (Beerakaya)", "பீர்க்கங்காய் (Peerkangai)",
            {"kannada": "ಹೀರೆಕಾಯಿ (Heerekayi)", "malayalam": "പീച്ചിങ്ങ (Peechinga)", "bengali": "ঝিঙে (Jhinge)", "marathi": "दोडका (Dodka)"},
            [], "Cucurbitaceae", "Luffa", "acutangula", "vegetable", "cultivated",
            ["Andhra Pradesh", "Tamil Nadu", "Karnataka", "Maharashtra", "Uttar Pradesh", "West Bengal"],
            "Palmately 5–7 angled or shallowly lobed scabrous cordate leaves", "Alternate", "Denticulate", "Palmate", "Medium green, rough to touch",
            "Strong 5-angled grooved climbing vine with multi-branched tendrils, 3–6 m",
            "Showy pale yellow flowers opening late in afternoon; male in racemes, female solitary",
            "Clavate club-shaped fruit with 10 prominent sharp longitudinal ribs (ridges), tapering towards stem",
            "Vigorous annual climbing vine, 3–6 m",
            "Warm humid tropical and sub-tropical climate",
            "Full sun", "Regular weekly irrigation",
            "Fertile, well-drained loamy soil, pH 6.0–7.5",
            "Summer and Rainy seasons", ["Direct pit sowing"],
            ["Tender ridged fruits cooked in curries (turai sabzi, beerakaya curry, peerkangai kootu)", "Mature dried fibrous sponge skeleton used as natural bathing loofah scrubber"],
            "Safe for consumption.", False,
            [
                {"name": "Downy Mildew", "type": "fungal", "symptoms": "Angular yellow patches on leaves", "management": "Foliar Mancozeb spray"}
            ],
            ["Train on pandal / trellis to let fruits hang freely without curling", "Harvest every 3–4 days while ribs are tender"]
        ),
        make_plant(
            "trichosanthes-cucumerina", "Trichosanthes cucumerina", "Snake Gourd / Chichinda", "चिचिंडा / चचेंडा (Chichinda)",
            "పొట్లకాయ (Potlakaya)", "புடலங்காய் (Pudalangai)",
            {"kannada": "ಪಡುವಲಕಾಯಿ (Padavalakayi)", "malayalam": "പടവലങ്ങ (Padavalanga)", "bengali": "চিচিঙ্গা (Chichinga)", "marathi": "पडवळ (Padwal)"},
            ["Trichosanthes anguina"], "Cucurbitaceae", "Trichosanthes", "cucumerina", "vegetable", "cultivated",
            ["Tamil Nadu", "Kerala", "Andhra Pradesh", "Karnataka", "West Bengal", "Odisha", "Maharashtra"],
            "Broadly palmately 3–7 lobed cordate leaves with soft pubescence", "Alternate", "Dentate", "Palmate", "Vibrant green with distinct cucurbitaceous musky scent",
            "Slender, grooved climbing vine with branched tendrils, 3–6 m",
            "Exquisite white nocturnal flowers with beautifully fringed, lace-like petal margins",
            "Extremely long, cylindrical, coiled snake-like pendulous fruit (0.5–1.5 m) with white stripes",
            "Annual climbing herbaceous vine, 3–6 meters",
            "Warm, humid tropical climate with abundant sunshine",
            "Full sun", "Regular watering; sensitive to drought stress",
            "Sandy loam to rich river valley alluvial loams, pH 6.0–7.5",
            "Rainy (Kharif) and Summer", ["Direct seed pit sowing on mounds"],
            ["Tender fruits sliced in South Indian kootu, poriyal, stir-fries, and curries", "High moisture and dietary fiber content"],
            "Safe for cooking.", False,
            [
                {"name": "Fruit Fly", "type": "pest", "symptoms": "Maggots inside fruit causing distortion", "management": "Pheromone traps; bag young fruits"}
            ],
            ["Traditional practice: tie a small pebble to fruit tip to encourage straight hanging growth"]
        ),
        make_plant(
            "raphanus-sativus", "Raphanus sativus", "Radish / Mooli", "मूली (Mooli)",
            "ముల్లంగి (Mullangi)", "முள்ளங்கி (Mullangi)",
            {"kannada": "ಮೂಲಂಗಿ (Moolangi)", "malayalam": "മുള്ളങ്കി (Mullanki)", "bengali": "মুলো (Mulo)", "marathi": "मुळा (Mula)"},
            [], "Brassicaceae", "Raphanus", "sativus", "vegetable", "cultivated",
            ["West Bengal", "Bihar", "Uttar Pradesh", "Punjab", "Haryana", "Karnataka", "Tamil Nadu"],
            "Lyrate-pinnatifid coarse rough leaves with large terminal lobe and bristly hairs", "Basal rosette", "Crenate to dentate", "Pinnate", "Medium green with rough prickly hairs",
            "Compressed crown stem; elongates into branched flowering stem during bolting",
            "White to pale lilac cross-shaped 4-petaled flowers with purple veins",
            "Enlarged fleshy pungent taproot (white, red, or purple); spongy indehiscent beaked silique pod (moongre)",
            "Fast-growing cool-season annual or biennial root crop, 20–40 cm",
            "Cool temperate to sub-tropical climate; 30–50 day maturity from seed",
            "Full sun", "Regular uniform light watering; drought induces extreme woody pungency and pithiness",
            "Deep, friable, loose sandy loam free from stones and clods, pH 6.0–7.0",
            "Rabi in plains (September–January); Asiatic types grown in Summer/Monsoon", ["Direct line sowing on ridges"],
            ["Crisp pungent root eaten raw in salads, mooli paratha, sambar, pickles", "Tender leaves (mooli ka saag) and seed pods (moongre) cooked as vegetables", "Digestive and liver tonic"],
            "Pungent isothiocyanates give sharp bite. Safe for consumption.", False,
            [
                {"name": "Pithiness / Sponginess", "type": "physiological", "symptoms": "Roots become hollow, dry, and woody when harvest is delayed", "management": "Harvest promptly at root maturity (30–45 days)"}
            ],
            ["Sow on 15 cm high raised ridges for straight unbranched root development", "Thin seedlings to 8–10 cm spacing"]
        ),
        make_plant(
            "daucus-carota", "Daucus carota", "Carrot / Gajar", "गाजर (Gajar)",
            "క్యారెట్ (Carrot)", "கேரட் (Carrot)",
            {"kannada": "ಕ್ಯಾರೆಟ್ (Carrot)", "malayalam": "കാരറ്റ് (Carrot)", "bengali": "গাজর (Gajor)", "marathi": "गाजर (Gajar)"},
            ["Daucus carota subsp. sativus"], "Apiaceae", "Daucus", "carota", "vegetable", "cultivated",
            ["Haryana", "Punjab", "Uttar Pradesh", "Karnataka", "Tamil Nadu (Nilgiris)", "Madhya Pradesh"],
            "Finely dissected 2–3 pinnately compound feathery lacy leaves with long petioles", "Basal rosette", "Deeply incised / dissected", "Pinnate", "Bright lush green",
            "Compressed crown stem giving rise to swollen fleshy taproot; branched umbel flowering scape upon bolting",
            "Compound umbel of tiny white flowers, often with a solitary dark red flower in center",
            "Enlarged fleshy conical taproot (orange, red, black, or purple); schizocarp seed with bristly spines",
            "Biennial root vegetable grown as cool-season annual, 30–60 cm",
            "Cool winter climate; optimal temperature 15°C–20°C for deep red/orange lycopene and carotene accumulation",
            "Full sun", "Uniform light irrigation; excess water after dry spell causes root splitting",
            "Deep, loose, stone-free friable sandy loam with high organic humus, pH 6.0–7.0",
            "Rabi (September–November in plains; year-round in temperate hills)", ["Direct seed line sowing on ridges"],
            ["Nutrient-dense root rich in beta-carotene (Vitamin A) and lycopene; raw salad, gajar ka halwa, curries, pickles"],
            "Safe for human nutrition.", False,
            [
                {"name": "Root Forking / Splitting", "type": "physiological", "symptoms": "Taproot branches into multiple distorted fangs due to hard subsoil pan or undecomposed FYM", "management": "Deep ploughing; avoid fresh unrotted manure"}
            ],
            ["Rub seeds to remove bristles before sowing for uniform distribution", "Thin to 6–8 cm apart at 20 days"]
        ),
        make_plant(
            "beta-vulgaris", "Beta vulgaris", "Beetroot / Chukandar", "चुकंदर (Chukandar)",
            "బీట్‌రూట్ (Beetroot)", "பீட்ரூட் (Beetroot)",
            {"kannada": "ಬೀಟ್‌ರೂಟ್ (Beetroot)", "malayalam": "ബീറ്റ്റൂട്ട് (Beetroot)", "bengali": "বিট (Bit)", "marathi": "बीट (Beat)"},
            ["Beta vulgaris subsp. vulgaris"], "Amaranthaceae", "Beta", "vulgaris", "vegetable", "cultivated",
            ["Haryana", "Uttar Pradesh", "Karnataka", "Maharashtra", "Tamil Nadu", "West Bengal"],
            "Glossy, ovate to cordate fleshy wavy leaves with prominent crimson-red veins and petioles", "Basal rosette", "Entire to wavy undulate", "Pinnate", "Dark green suffused with deep purple-red",
            "Short crown stem terminating in swollen subterranean hypocotyl tuber",
            "Inconspicuous greenish flowers in dense spikes on tall flowering scape",
            "Swollen globose to napiform fleshy hypocotyl taproot with deep ruby-red betalain pigmentation",
            "Biennial root vegetable grown as annual, 30–50 cm",
            "Cool, sunny winter climate; tolerates light frost and mild soil salinity",
            "Full sun", "Uniform regular watering; alternating dry and wet cycles causes concentric internal white rings",
            "Well-drained deep friable sandy loam or alluvial loam, pH 6.0–7.5",
            "Rabi (October–November in plains; year-round in hills)", ["Direct seed line sowing of multigerm seed balls"],
            ["Deep red sweet root eaten raw, boiled in salads, juices, poriyal, halwa", "Natural source of dietary nitrates (boosts athletic endurance and blood flow) and betalains"],
            "Betalain excretion causes harmless temporary red urine (beeturia).", False,
            [
                {"name": "Cercospora Leaf Spot (Cercospora beticola)", "type": "fungal", "symptoms": "Circular spots with grey center and reddish-purple border on leaves", "management": "Foliar Mancozeb or Copper Oxychloride"}
            ],
            ["Thin clustered seedlings emerging from multigerm seed balls to single robust plants 10 cm apart"]
        ),
        make_plant(
            "pisum-sativum", "Pisum sativum", "Peas / Garden Pea / Matar", "मटर (Matar)",
            "బఠానీలు (Bataneelu)", "பட்டாணி (Pattani)",
            {"kannada": "ಬಟಾಣಿ (Batani)", "malayalam": "പട്ടാണി (Pattani)", "bengali": "মটরশুঁটি (Matorshuti)", "marathi": "मटार (Matar)"},
            ["Pisum arvense"], "Fabaceae", "Pisum", "sativum", "vegetable", "cultivated",
            ["Uttar Pradesh", "Madhya Pradesh", "Punjab", "Himachal Pradesh", "Bihar", "Rajasthan", "Haryana"],
            "Pinnate compound leaves with 1–3 pairs of ovate leaflets ending in branched climbing tendrils and large leafy stipules", "Alternate", "Entire to denticulate", "Pinnate", "Soft glaucous bluish-green",
            "Weak, hollow, succulent climbing stem with nodes, 0.4–1.8 m",
            "Showy white or pale pinkish-purple papilionaceous flowers solitary or in pairs",
            "Swollen straight or curved 2-valved dehiscent pod holding 4–10 sweet spherical green seeds",
            "Climbing cool-season annual herbaceous legume, 40–180 cm",
            "Cool temperate to sub-tropical winter climate; sensitive to hot dry weather during flowering",
            "Full sun (6 hours)", "Moderate; critical irrigations at flowering and pod filling",
            "Well-drained fertile friable loamy soil, pH 6.0–7.5",
            "Rabi (October–November to February–March)", ["Direct seed line sowing with Rhizobium leguminosarum"],
            ["Popular fresh winter vegetable (matar paneer, aloo matar, samosa, kachori)", "Frozen and dehydrated peas for year-round culinary use; fixes soil nitrogen"],
            "Safe for human nutrition.", False,
            [
                {"name": "Powdery Mildew (Erysiphe pisi)", "type": "fungal", "symptoms": "White flour-like powdery growth covering foliage, stems, and pods in late season", "management": "Spray Wettable Sulfur (2 g/L) or Dinocap; grow resistant varieties (Arka Ajit, AP 3)"}
            ],
            ["Stake tall climbing varieties with bamboo sticks or netting", "Pick pods before peas become starchy and hard"]
        ),
        make_plant(
            "phaseolus-vulgaris", "Phaseolus vulgaris", "French Bean / Common Bean / Rajma", "फ्रेंच बीन / राजमा (French Bean)",
            "బీన్స్ (Beans)", "பீன்ஸ் (Beans)",
            {"kannada": "ಹುರುಳಿಕಾಯಿ (Hurulikayi)", "malayalam": "ബീൻസ് (Beans)", "bengali": "শিম / বিন্স (Shim / Beans)", "marathi": "फरसबी (Farasbi)"},
            [], "Fabaceae", "Phaseolus", "vulgaris", "vegetable", "cultivated",
            ["Karnataka", "Maharashtra", "Tamil Nadu", "Himachal Pradesh", "Jammu & Kashmir", "Uttarakhand", "Andhra Pradesh"],
            "Trifoliolate compound leaves with broadly ovate pointed leaflets", "Alternate", "Entire", "Reticulate", "Medium to dark green",
            "Bush type (determinate erect, 30–60 cm) or pole type (indeterminate twining climber, 2–3 m)",
            "Small clusters of white, pink, or light violet papilionaceous flowers",
            "Slender straight or curved fleshy pod (10–20 cm) with cylindrical succulent green pods or dry kidney beans",
            "Annual bushy herb or twining climbing vine, 30–250 cm",
            "Mild temperate to subtropical climate; highly sensitive to frost and high heat (>32°C causes flower drop)",
            "Full sun", "Regular moderate watering; avoids waterlogging",
            "Well-drained rich friable loamy soil rich in organic matter, pH 5.5–6.8",
            "Spring and Autumn in hills; Winter in plains", ["Direct seed line sowing"],
            ["Tender green pods cooked as French beans vegetable", "Dry mature seeds cooked as renowned North Indian Rajma curry (high protein)"],
            "Raw dry kidney beans contain phytohaemagglutinin (lectin); MUST be soaked and boiled thoroughly before eating.", False,
            [
                {"name": "Bean Anthracnose (Colletotrichum lindemuthianum)", "type": "fungal", "symptoms": "Dark brown sunken eye-shaped lesions on pods with pink spore masses", "management": "Seed treatment with Carbendazim (2 g/kg); spray Mancozeb"}
            ],
            ["Pole varieties require sturdy trellis staking for high yields", "Harvest green pods while fleshy and stringless"]
        )
    ]

def save_vegetables():
    veggies = get_vegetables()
    with open(DATA_DIR / "vegetables.json", "w", encoding="utf-8") as f:
        json.dump(veggies, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(veggies)} vegetable records in vegetables.json")

if __name__ == "__main__":
    save_vegetables()
