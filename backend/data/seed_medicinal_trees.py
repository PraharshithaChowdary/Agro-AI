"""
AGRO AI — Indian Medicinal Plants, Spices, Trees, and Ornamentals Seed Data
Contains verified records for:
- Medicinal & Spices: Tulsi, Neem, Aloe Vera, Turmeric, Ginger, Black Pepper, Cardamom,
  Cinnamon, Clove, Curry Leaf, Lemongrass, Ashwagandha, Brahmi, Hibiscus, Jasmine,
  Rose, Marigold, Periwinkle.
- Trees & Ornamentals: Banyan, Peepal, Indian Teak, Sal, Arjuna, Gulmohar, Rain Tree,
  Eucalyptus, Bamboo, Acacia/Babool, Bougainvillea, Money Plant, Snake Plant, Areca Palm.
"""

import json
from pathlib import Path
from generate_verified_seed_catalog import make_plant, DATA_DIR

def get_medicinal_and_spices():
    return [
        make_plant(
            "ocimum-tenuiflorum", "Ocimum tenuiflorum", "Tulsi / Holy Basil", "तुलसी (Tulsi)",
            "తులసి (Tulasi)", "துளசி (Thulasi)",
            {"kannada": "ತುಳಸಿ (Tulasi)", "malayalam": "തുളസി (Thulasi)", "bengali": "তুলসী (Tulsi)", "marathi": "तुळस (Tulas)"},
            ["Ocimum sanctum"], "Lamiaceae", "Ocimum", "tenuiflorum", "medicinal plant", "native",
            ["Pan-India (Uttar Pradesh, Madhya Pradesh, Andhra Pradesh, Tamil Nadu, Karnataka, Maharashtra, West Bengal)"],
            "Simple, ovate-elliptic leaves with glandular hairs, pungent aromatic fragrance, green (Rama Tulsi) or purple-tinted (Krishna Tulsi)", "Opposite, decussate", "Serrate to dentate", "Pinnate", "Green or deep purplish green",
            "Erect, much-branched quadrangular pubescent woody stem, 30–75 cm",
            "Small purplish-pink or white 2-lipped flowers in terminal verticillaster racemes",
            "Small subglobose nutlets enclosed in persistent calyx",
            "Erect aromatic perennial herb/subshrub, 30–80 cm",
            "Tropical and sub-tropical climate across India; revered sacred courtyard plant",
            "Full sunlight (6–8 hours)", "Moderate regular watering; avoids water stagnation",
            "Well-drained rich sandy loam or fertile potting soil, pH 6.0–7.5",
            "Year-round cultivation", ["Seeds or semi-hardwood stem cuttings"],
            ["Queen of Ayurvedic herbs: adaptogen, respiratory decongestant (eugenol), immune booster, herbal teas (tulsi green tea)", "Sacred worship in Hindu households and courtyards"],
            "Safe for daily culinary herbal infusion. Avoid excessive concentrated medicinal extracts during pregnancy.", False,
            [
                {"name": "Powdery Mildew", "type": "fungal", "symptoms": "White powdery coating on aromatic leaves", "management": "Neem oil spray (3 ml/L) or baking soda solution"}
            ],
            ["Pinch flower spikes (manjari) regularly to encourage bushy vegetative leaf growth", "Water at soil level to prevent fungal leaf spot"]
        ),
        make_plant(
            "azadirachta-indica", "Azadirachta indica", "Neem / Indian Lilac", "नीम (Neem)",
            "వేప (Vepa)", "வேம்பு (Vembu)",
            {"kannada": "ಬೇವು (Bevu)", "malayalam": "വേപ്പ് (Veppu)", "bengali": "নিম (Nim)", "marathi": "कडुनिंब (Kadunimb)"},
            ["Melia azadirachta"], "Meliaceae", "Azadirachta", "indica", "tree", "native",
            ["Pan-India (Rajasthan, Uttar Pradesh, Maharashtra, Andhra Pradesh, Tamil Nadu, Karnataka, Gujarat, Madhya Pradesh)"],
            "Pinnately compound with 20–30 falcate (curved sickle-shaped) asymmetric lanceolate leaflets, intensely bitter", "Alternate", "Coarsely serrate", "Pinnate", "Lustrous medium green",
            "Stout, straight trunk with dark grey-brown rough deeply grooved furrowed bark and broad rounded canopy, 15–25 m",
            "Small, fragrant white star-shaped bisexual and male flowers in drooping axillary panicles",
            "Ellipsoid smooth glabrous drupe (1–2 cm), green ripening to golden-yellow with sweetish pulp and single hard seed",
            "Large, deep-rooted evergreen to semi-deciduous tree, 15–25 meters",
            "Semi-arid tropical and subtropical plains; extreme drought and heat tolerance",
            "Full blazing sun", "Low; rainfed once established",
            "Thrives in varied soils: rocky, dry, shallow soils, sandy loams, and black soils, pH 5.5–8.5",
            "Spring flowering (March–April), summer fruiting (June–August)", ["Fresh seeds or root suckers"],
            ["Village pharmacy: organic biopesticide (azadirachtin), neem oil foliar spray for organic farming", "Neem-coated urea fertilizer inhibitor", "Ayurvedic antibacterial skin remedies, dental twig (datun), soaps"],
            "Neem oil and concentrated seed extracts are not for direct oral ingestion by infants or pregnant women.", False,
            [
                {"name": "Tea Mosquito Bug (Helopeltis antonii)", "type": "pest", "symptoms": "Necrotic brownish-black spots on tender shoots and panicles", "management": "Foliar spray of Quinalphos or Dimethoate"}
            ],
            ["Extract neem seed kernel extract (NSKE 5%) as non-toxic broad-spectrum organic insect repellent across agricultural crops"]
        ),
        make_plant(
            "aloe-barbadensis", "Aloe vera", "Aloe Vera / Ghritkumari", "घृतकुमारी / एलोवेरा (Ghritkumari)",
            "కలబంద (Kalabanda)", "சோற்றுக்கற்றாழை (Sotrukatraazhai)",
            {"kannada": "ಲೋಳೆಸರ (Lolesara)", "malayalam": "കറ്റാർവാഴ (Kattarvazha)", "bengali": "ঘৃতকুমারী (Ghritokumari)", "marathi": "कोरफड (Korphad)"},
            ["Aloe barbadensis"], "Asphodelaceae", "Aloe", "vera", "medicinal plant", "naturalized",
            ["Rajasthan", "Gujarat", "Andhra Pradesh", "Tamil Nadu", "Maharashtra", "Madhya Pradesh", "Karnataka"],
            "Thick, fleshy, succulent ensiform (sword-shaped) dagger-like leaves filled with clear soothing mucilaginous gel and yellow latex (aloin)", "Dense basal rosette", "Spiny dentate with white marginal teeth", "Parallel", "Greyish green with occasional white spots when young",
            "Stemless (acaulescent) or very short woody stock with prolific basal offshoots (pups), 40–80 cm",
            "Tubular pendulous bright yellow to orange flowers in dense terminal raceme on tall central scape",
            "3-valved triangular capsule holding winged seeds (rarely sets in cultivated clumps)",
            "Stemless xerophytic succulent perennial herb, 40–90 cm",
            "Arid and semi-arid desert and coastal zones; exceptional drought and heat resilience",
            "Bright indirect to full sunlight", "Low; allow soil to dry completely between waterings",
            "Well-drained porous sandy, gravelly, or cactus potting mix, pH 6.0–8.0",
            "Year-round vegetative growth", ["Basal offshoots (pups / suckers) division"],
            ["Clear inner gel used globally for skincare, sunburn relief, wound healing, cosmetic moisturizers", "Aloe juice for digestive soothing", "Commercial extraction of acemannan and anthraquinones"],
            "The yellow bitter sap (aloin latex) directly under the green skin is a strong laxative. Wash clear gel thoroughly before internal use.", False,
            [
                {"name": "Root Rot / Soft Rot (Erwinia chrysanthemi)", "type": "bacterial", "symptoms": "Water-soaked soft brown decay at base of leaves caused by overwatering", "management": "Withhold water; improve drainage; drench with Copper Oxychloride"}
            ],
            ["Plant in terracotta pots or raised sandy beds with gravel drainage hole", "Never let water stand in central leaf crown"]
        ),
        make_plant(
            "curcuma-longa", "Curcuma longa", "Turmeric / Haldi", "हल्दी (Haldi)",
            "పసుపు (Pasupu)", "மஞ்சள் (Manjal)",
            {"kannada": "ಅರಿಶಿನ (Arishina)", "malayalam": "മഞ്ഞൾ (Manjal)", "bengali": "হলুদ (Holud)", "marathi": "हळद (Halad)"},
            ["Curcuma domestica"], "Zingiberaceae", "Curcuma", "longa", "spice", "native",
            ["Telangana", "Andhra Pradesh", "Tamil Nadu", "Odisha", "Karnataka", "West Bengal", "Maharashtra"],
            "Large, oblong-lanceolate smooth bright green leaves with long channeled petiole arising from underground rhizome", "Alternate, 2-ranked", "Entire", "Parallel-pinnate", "Lush vibrant green",
            "Pseudostem formed by overlapping leaf sheaths (1 m) arising from thick aromatic golden-orange underground rhizome",
            "Dense cylindrical terminal spike of pale yellow flowers surrounded by large pinkish-white bracts",
            "Rarely sets fruit; propagation is purely vegetative via rhizomes",
            "Perennial rhizomatous erect herb grown as annual, 80–120 cm",
            "Warm humid tropical monsoon climate with rich rainfall and filtered sunlight",
            "Partial shade to filtered sun", "High; requires regular uniform moisture during vegetative phase",
            "Deep, friable, fertile sandy loam or clay loam rich in organic humus, pH 6.0–7.5",
            "Kharif planting (May–June), harvested in 8–9 months (Jan–March) (Prathiba, IISR Alleppey Supreme, Duggirala)", ["Mother or finger rhizome setts (20–40 g) with prominent buds"],
            ["Golden spice of India: curries, preservative, yellow natural food coloring", "Medicinal powerhouse: potent anti-inflammatory curcumin, wound healing, golden turmeric milk", "Sacred ceremonial paste in Indian rituals (haldi ceremony)"],
            "Safe for human nutrition. Concentrated curcumin supplements should be taken with caution alongside anticoagulant medication.", False,
            [
                {"name": "Rhizome Rot (Pythium aphanidermatum)", "type": "fungal", "symptoms": "Water-soaked soft rotting of rhizomes with yellowing and drying of foliage from margins inwards", "management": "Treat seed rhizomes with Metalaxyl (2 g/L) before planting; provide deep drainage ridges"}
            ],
            ["Mulch heavily with green leaves (15 t/ha at planting and 7.5 t/ha at 50 and 90 DAS) to conserve moisture and suppress weeds"]
        ),
        make_plant(
            "zingiber-officinale", "Zingiber officinale", "Ginger / Adrak", "अदरक (Adrak)",
            "అల్లం (Allam)", "இஞ்சி (Inji)",
            {"kannada": "ಶುಂಠಿ (Shunti)", "malayalam": "ഇഞ്ചി (Inji)", "bengali": "আদা (Aada)", "marathi": "आले (Aale)"},
            [], "Zingiberaceae", "Zingiber", "officinale", "spice", "native",
            ["Assam", "Kerala", "Meghalaya", "Karnataka", "West Bengal", "Odisha", "Himachal Pradesh", "Sikkim"],
            "Linear-lanceolate smooth grass-like leaves with sheathing bases arising from underground aromatic rhizome", "Alternate, distichous", "Entire", "Parallel", "Deep glossy green with distinct spicy scent",
            "Slender leafy pseudostem formed by leaf sheaths, 60–100 cm tall, rising from subterranean branched tuberous rhizome",
            "Dense conical spike with green bracts and yellowish-green flowers with purple lips (rarely blooms)",
            "Vegetatively propagated via rhizomes",
            "Erect perennial rhizomatous herb grown as annual, 60–100 cm",
            "Warm humid tropical and sub-tropical climate with abundant rainfall and warm shade",
            "Partial shade (thrives under 25–50% shade or agroforestry intercropping)", "High; regular soil moisture essential; highly sensitive to waterlogging",
            "Rich, loose, well-drained friable sandy loam or forest loam high in organic humus, pH 5.5–6.8",
            "Planted with pre-monsoon showers (April–May), harvested at 8–10 months (IISR Rejatha, Varada, Mahima)", ["Rhizome seed pieces (bits) with 1–2 viable sprouts"],
            ["Essential aromatic culinary rhizome (adrak chai, ginger garlic paste, curries)", "Medicinal: gingerol and shogaol soothe nausea, morning sickness, digestive indigestion, and throat irritation", "Dry ginger (sonth) for spice blends"],
            "Safe for human nutrition.", False,
            [
                {"name": "Soft Rot / Rhizome Rot (Pythium myriotylum)", "type": "fungal", "symptoms": "Water-soaked basal leaf sheaths, yellowing and sudden wilting of tillers, foul soft rot of underground rhizome", "management": "Seed rhizome dip in Metalaxyl (2 g/L); drench affected beds; ensure high raised beds"}
            ],
            ["Plant on 15–20 cm raised beds to ensure rapid excess water drainage", "Mulch with 12 t/ha green tree leaves in three split applications"]
        ),
        make_plant(
            "piper-nigrum", "Piper nigrum", "Black Pepper / King of Spices / Kali Mirch", "काली मिर्च (Kali Mirch)",
            "మిరియాలు (Miriyalu)", "மிளகு (Milagu)",
            {"kannada": "ಕಾಳುಮೆಣಸು (Kalumenasu)", "malayalam": "കുരുമുളക് (Kurumulaku)", "bengali": "গোলমরিচ (Golmorich)", "marathi": "काळी मिरी (Kali Miri)"},
            [], "Piperaceae", "Piper", "nigrum", "spice", "native",
            ["Kerala", "Karnataka (Kodagu, Malnad)", "Tamil Nadu", "Goa", "Assam", "Meghalaya"],
            "Simple, coriaceous (leathery), broadly ovate to cordate leaves with acuminate tip and prominent sunken veins", "Alternate", "Entire", "Curved palmate-pinnate", "Dark lustrous green above, paler beneath",
            "Woody perennial evergreen climbing liana with swollen nodes producing adventitious clinging roots, 4–10 m",
            "Slender, pendulous catkin-like spikes (8–15 cm) with 50–150 tiny unisexual or bisexual flowers",
            "Globose sessile berry (drupe, 4–6 mm), green turning orange-red when ripe; dried with wrinkled black skin enclosing white seed",
            "Woody evergreen climbing vine trained on support trees/standards, 4–10 meters",
            "Hot, humid tropical Western Ghats rainforest climate with 2000–3000 mm rainfall and 20°C–35°C",
            "Filtered dappled shade to partial sun", "High; requires humid atmosphere; sensitive to prolonged drought",
            "Rich, deep, well-drained fertile forest lateritic loams and red clay loams, pH 5.5–6.5",
            "Flowering with onset of monsoon (May–June), harvesting Dec–March (Panniyur-1, Panniyur-5, Karimunda)", ["Rooted runner shoot cuttings in polybags"],
            ["King of spices: global seasoning, piperine alkaloid enhances bioavailability of turmeric curcumin by 2000%", "Black pepper (harvested green and sun-dried), White pepper (fully ripe skin removed)", "Ayurvedic respiratory Trikatu formula"],
            "Safe for human nutrition.", False,
            [
                {"name": "Quick Wilt / Foot Rot (Phytophthora capsici)", "type": "fungal", "symptoms": "Sudden black necrotic lesions on collar, leaf drop, rapid death of entire vine within 15–20 days of monsoon", "management": "Drench basin with 1% Bordeaux mixture or Potassium Phosphonate (3 ml/L) in May and August"},
                {"name": "Pollu Beetle (Longitarsus nigripennis)", "type": "pest", "symptoms": "Larvae bore into tender berries rendering them hollow and black (pollu)", "management": "Spray Quinalphos (2 ml/L) in July and October"}
            ],
            ["Train vines on living tree standards (Silver Oak, Arecanut, Erythrina)", "Prune top shade of standards before monsoon"]
        ),
        make_plant(
            "elettaria-cardamomum", "Elettaria cardamomum", "Small Cardamom / Queen of Spices / Elaichi", "इलायची (Elaichi)",
            "ఏలకులు (Yelakulu)", "ஏலக்காய் (Yelakkai)",
            {"kannada": "ಏಲಕ್ಕಿ (Elakki)", "malayalam": "ഏലം (Elam)", "bengali": "এলাচ (Elach)", "marathi": "वेलची (Velchi)"},
            [], "Zingiberaceae", "Elettaria", "cardamomum", "spice", "native",
            ["Kerala (Idukki - Cardamom Hills)", "Karnataka", "Tamil Nadu"],
            "Long, lanceolate smooth arching dark green leaves with aromatic pungent aroma", "Alternate, 2-ranked", "Entire", "Parallel-pinnate", "Dark glossy green",
            "Erect leafy pseudostem formed by sheaths (2–4 m), subterranean rhizome producing prostrate or erect flowering panicles",
            "Spreading prostrate panicles arising from base of pseudostem; white or pale violet labellum with purplish-blue streaks",
            "Small, 3-sided ovoid-trilocular capsule (1–2 cm), green with thin ribbed shell holding aromatic angular black seeds",
            "Robust perennial shade-loving rhizomatous herb, 2–4 meters",
            "High-elevation (600–1500 m) evergreen Western Ghats shola forest climate with cool temperatures (10°C–35°C) and heavy mist",
            "Deep dappled forest shade (50–60% overhead shade)", "High; requires consistent soil moisture and atmospheric humidity; avoids drought",
            "Rich forest humus, loamy laterites, and well-drained forest soils, pH 4.5–6.0",
            "Flowering throughout monsoon, harvesting August–February (Malabar, Mysore, Vazhukka)", ["Rhizome divisions or sucker splits (ICRI-1, PV-1)"],
            ["Queen of spices: intensely aromatic flavoring in biryani, sweets, chai, garam masala, desserts", "Natural breath freshener, digestive carminative, essential oils"],
            "Safe for human nutrition.", False,
            [
                {"name": "Katte Disease / Mosaic Virus", "type": "viral", "symptoms": "Discontinuous chlorotic stripes on young leaves, stunted tillers, slender capsules", "management": "Vector aphid (Pentalonia nigronervosa) control with Dimethoate; rogue diseased clumps"},
                {"name": "Cardamom Thrips (Sciothrips cardamomi)", "type": "pest", "symptoms": "Thrips lacerate flower buds and capsule rind causing scabby, warted corky fruit skin", "management": "Spray Quinalphos (2 ml/L) or Spinosad"}
            ],
            ["Maintain 50% overhead forest canopy shade using indigenous trees (Jackfruit, Red Cedar)", "Cure harvested green capsules in specialized curing chambers at 45°C–50°C to preserve vivid green color"]
        ),
        make_plant(
            "cinnamomum-verum", "Cinnamomum verum", "True Cinnamon / Dalchini", "दालचीनी (Dalchini)",
            "దాల్చిన చెక్క (Dalchina Chekka)", "இலவங்கப்பட்டை (Ilavangapattai)",
            {"kannada": "ದಾಲ್ಚಿನ್ನಿ (Dalchinni)", "malayalam": "കറുവാപ്പട്ട (Karuvapatta)", "bengali": "দারুচিনি (Daruchini)", "marathi": "दालचिनी (Dalchini)"},
            ["Cinnamomum zeylanicum"], "Lauraceae", "Cinnamomum", "verum", "spice", "native",
            ["Kerala", "Karnataka", "Tamil Nadu", "Andhra Pradesh", "Goa", "Maharashtra"],
            "Simple, coriaceous (leathery), ovate-lanceolate leaves with 3–5 prominent pale longitudinal veins, aromatic when bruised", "Opposite or sub-opposite", "Entire", "3–5 prominent longitudinal basal veins", "Pinkish-red when young, mature glossy dark green",
            "Medium evergreen tree coppiced into dense bush of straight slender poles with smooth aromatic bark, 6–12 m",
            "Small, inconspicuous pale yellowish-white flowers in silky axillary and terminal panicles",
            "Small dark purple ovoid fleshy berry resting in persistent cup-like calyx with single seed",
            "Medium evergreen tree coppiced to commercial bush, 6–12 m (coppiced to 2 m)",
            "Warm humid tropical rainforest climate with abundant rainfall (2000–2500 mm)",
            "Filtered sunlight to full sun", "High; requires moist well-drained root zone",
            "Well-drained sandy loam or lateritic soil rich in organic humus, pH 5.5–6.5",
            "Harvested twice yearly after monsoon flushes (IISR Nithyashree, Navashree)", ["Seeds or semi-hardwood stem cuttings"],
            ["Prized aromatic culinary spice (true Ceylon cinnamon with delicate sweet cinnamaldehyde flavor)", "Inner bark peeled and curled into concentric quills", "Regulates blood glucose, antioxidant, antimicrobial"],
            "True Ceylon cinnamon (C. verum) contains very low coumarin (<0.004%), unlike Cassia (C. cassia) which has high coumarin harmful to liver.", False,
            [
                {"name": "Leaf Spot and Die-back (Colletotrichum gloeosporioides)", "type": "fungal", "symptoms": "Brown necrotic spots on leaves and drying of shoot tips", "management": "Spray 1% Bordeaux mixture"}
            ],
            ["Coppice stems at 2 years by cutting near base to induce multiple straight slender shoots for high-grade quill peeling"]
        ),
        make_plant(
            "syzygium-aromaticum", "Syzygium aromaticum", "Clove / Laung", "लौंग (Laung)",
            "లవంగాలు (Lavangalu)", "கிராம்பு (Krambu)",
            {"kannada": "ಲವಂಗ (Lavanga)", "malayalam": "ഗ്രാമ്പൂ (Grampoo)", "bengali": "লবঙ্গ (Lobongo)", "marathi": "लवंग (Lavang)"},
            ["Eugenia caryophyllata"], "Myrtaceae", "Syzygium", "aromaticum", "spice", "cultivated",
            ["Tamil Nadu (Kanyakumari, Nilgiris)", "Kerala (Kottayam, Kollam)", "Karnataka"],
            "Opposite, coriaceous, lanceolate-elliptic glossy leaves densely dotted with translucent aromatic oil glands", "Opposite", "Entire", "Pinnate with numerous fine veins", "Copper-red when young, turning dark lustrous green",
            "Medium conical evergreen tree with smooth grey bark and dense ascending canopy, 8–15 m",
            "Terminal trichotomous cymes of unopened flower buds; unopened bud comprises long fleshy calyx tube topped by 4 unopened petals",
            "Oblong-obovate fleshy dark purple drupe (mother of clove) containing 1–2 seeds",
            "Pyramidal evergreen canopy tree, 8–15 meters",
            "Warm, humid tropical island and coastal hill climate with sea breezes and rainfall over 1500 mm",
            "Full sun when mature; partial shade during first 3–4 years", "Moderate to high; avoids waterlogging",
            "Rich, deep, well-drained red lateritic and forest loams, pH 5.5–6.5",
            "Harvesting unopened buds before flower opens (Dec–March)", ["Ripe seed nursery germination"],
            ["Unopened dried flower bud is world's most pungent aromatic spice (eugenol)", "Essential ingredient in garam masala, biryani, curries", "Clove oil used globally in dental analgesia and toothache remedies"],
            "Clove oil is intensely concentrated; do not apply undiluted oil directly to mucous membranes.", False,
            [
                {"name": "Leaf Rot / Die-back (Corticium salmonicolor)", "type": "fungal", "symptoms": "Pinkish fungal crust on twigs causing die-back of branches", "management": "Prune affected twigs; apply Bordeaux paste to cut ends"}
            ],
            ["Harvest buds precisely when green calyx turns pinkish-red before white petals open"]
        ),
        make_plant(
            "murraya-koenigii", "Murraya koenigii", "Curry Leaf / Kadi Patta", "कढ़ी पत्ता (Kadi Patta)",
            "కరివేపాకు (Karivepaku)", "கறிவேப்பிலை (Kariveppilai)",
            {"kannada": "ಕರಿಬೇವಿನ ಸೊಪ್ಪು (Karibevina Soppu)", "malayalam": "കറിവേപ്പില (Kariveppila)", "bengali": "কারিপাতা (Karipata)", "marathi": "कढीपत्ता (Kadipatta)"},
            [], "Rutaceae", "Murraya", "koenigii", "herb", "native",
            ["Pan-India (Tamil Nadu, Andhra Pradesh, Karnataka, Kerala, Maharashtra, Gujarat, Uttar Pradesh, West Bengal)"],
            "Pinnate compound leaves with 11–25 small asymmetric ovate leaflets with intensely aromatic citrus-pungent odor", "Alternate", "Obliquely ovate, crenulate", "Pinnate", "Bright to dark shiny green with oil glands",
            "Slender, branched small aromatic evergreen tree or large shrub with dark brown bark, 2–5 m",
            "Small fragrant white flowers in terminal corymbose cymes",
            "Small sub-globose fleshy berry (1 cm), green ripening to lustrous purple-black with single large seed",
            "Small aromatic evergreen tree or shrub, 2–5 meters",
            "Tropical and sub-tropical plains; drought hardy once established",
            "Full sun to light afternoon shade", "Regular moderate watering; avoids soggy root zone",
            "Well-drained fertile loamy to red soil rich in organic matter, pH 6.0–7.5",
            "Year-round continuous harvesting (DWD-1, DWD-2, Suwasini)", ["Seeds (fresh) or root suckers"],
            ["Indispensable aromatic tempering spice (tadka) in South and West Indian cooking", "Promotes digestion, hair health, rich in iron, folic acid, and carbazole alkaloids", "Natural antioxidant and hypoglycemic properties"],
            "Safe for daily culinary consumption.", False,
            [
                {"name": "Citrus Psyllid (Diaphorina citri)", "type": "pest", "symptoms": "Nymphs secrete white waxy filaments, suck sap curling young shoots", "management": "Spray Dimethoate (1.5 ml/L) or Neem oil (3 ml/L)"}
            ],
            ["Prune shoot tips regularly to maintain bushy productive branching", "Apply well-decomposed cow dung manure monthly"]
        ),
        make_plant(
            "cymbopogon-citratus", "Cymbopogon citratus", "Lemongrass / Lemon Grass", "नींबू घास (Nimbu Ghas)",
            "నిమ్మగడ్డి (Nimmagaddi)", "எலுமிச்சம்புல் (Elumichampul)",
            {"kannada": "ಮಜ್ಜಿಗೆ ಹುಲ್ಲು (Majjige Hullu)", "malayalam": "വാസനപ്പുല്ല് (Vasanappullu)", "bengali": "লেমনগ্রাস (Lemongrass)", "marathi": "गवती चहा (Gavati Chaha)"},
            [], "Poaceae", "Cymbopogon", "citratus", "herb", "cultivated",
            ["Kerala", "Tamil Nadu", "Karnataka", "Assam", "Uttar Pradesh", "Odisha", "Maharashtra"],
            "Long, linear strap-like arching leaves (1 m) with sharp rough margins emitting powerful lemon-citral fragrance when rubbed", "Clustered basal clumps", "Scabrous sharp", "Parallel", "Vibrant light to bluish green",
            "Short underground rhizome producing dense multi-tillered clump of leafy culms with swollen base, 1–1.8 m",
            "Large loose nodding compound panicle (rarely flowers under regular cutting)",
            "Propagated vegetatively via slip division",
            "Dense perennial clump-forming aromatic tussock grass, 1–1.8 meters",
            "Warm tropical and sub-tropical climate with abundant sunshine and warm temperatures",
            "Full blazing sun (8 hours)", "Low to moderate; highly drought resilient",
            "Well-drained sandy loam, gravelly red soils, and laterites, pH 5.5–7.5",
            "Perennial with 4–5 harvests per year (Krishna, Cauvery, Pragati)", ["Division of rooted slips from mature clumps"],
            ["Fresh leaves brewed in traditional herbal teas (Gavati Chaha, green tea)", "Commercial distillation of lemongrass essential oil (75–85% citral)", "Natural mosquito repellent and aromatherapy"],
            "Leaf margins are sharp; wear gloves during bulk harvesting.", False,
            [
                {"name": "Rust (Puccinia nakanishikii)", "type": "fungal", "symptoms": "Brown linear rust pustules on leaf blades", "management": "Harvest mature foliage; spray Mancozeb if severe"}
            ],
            ["Cut foliage 10 cm above ground level every 60–75 days to stimulate fresh shoots"]
        ),
        make_plant(
            "withania-somnifera", "Withania somnifera", "Ashwagandha / Indian Ginseng", "अश्वगंधा (Ashwagandha)",
            "అశ్వగంధ / పెన్నేరు (Aswagandha)", "அமுக்கிராங்கிழங்கு (Amukkira)",
            {"kannada": "ಅಶ್ವಗಂಧ (Ashwagandha)", "malayalam": "അമുക്കുരം (Amukkiram)", "bengali": "অশ্বগন্ধা (Oshwagandha)", "marathi": "अश्वगंधा (Ashwagandha)"},
            [], "Solanaceae", "Withania", "somnifera", "medicinal plant", "native",
            ["Madhya Pradesh (Neemuch, Mandsaur)", "Rajasthan", "Gujarat", "Andhra Pradesh", "Punjab", "Haryana"],
            "Simple, ovate to elliptic dull green leaves covered with fine starry tomentose hairs with characteristic horse-like aroma", "Alternate or sub-opposite", "Entire", "Pinnate", "Dull greyish-green with starry hairs",
            "Erect, branching tomentose semi-woody shrub with pale green-brown stem, 30–120 cm",
            "Small greenish-yellow bell-shaped flowers clustered in axils (3–6 flowers)",
            "Globose smooth berry (6 mm), bright orange-red when ripe, enclosed inside an enlarged papery inflated calyx",
            "Erect branching semi-woody perennial shrub grown as annual, 30–120 cm",
            "Semi-arid subtropical and tropical dry climate; dry weather required for root development",
            "Full bright sun", "Low; highly drought hardy",
            "Well-drained light sandy loam or red gravelly soils, pH 7.0–8.0",
            "Late Kharif sowing (July–August), harvested 150–180 days in winter (JA-20, Poshita)", ["Direct seed line sowing"],
            ["Premier Ayurvedic adaptogen: reduces cortisol stress, enhances vitality and endurance (withanolides)", "Tuberous roots dried and powdered for medicinal formulations", "Leaves used in traditional poultices for joint swelling"],
            "Roots have strong adaptogenic potency; pregnant women should avoid unprescribed medicinal doses.", False,
            [
                {"name": "Seedling Blight (Alternaria alternata)", "type": "fungal", "symptoms": "Brown circular spots on leaves and seedling damping-off", "management": "Seed treatment with Trichoderma (4 g/kg)"}
            ],
            ["Harvest roots when berries turn orange-red and leaves begin drying", "Grade roots based on diameter (A, B, C grade)"]
        ),
        make_plant(
            "bacopa-monnieri", "Bacopa monnieri", "Brahmi / Water Hyssop", "ब्राह्मी (Brahmi)",
            "సరస్వతీ ఆకు (Saraswathi Aaku)", "பிராமி / வல்லாரை (Brahmi)",
            {"kannada": "ಬ್ರಾಹ್ಮಿ (Brahmi)", "malayalam": "ബ്രഹ്മി (Brahmi)", "bengali": "ব্রাহ্মী (Brahmi)", "marathi": "ब्राह्मी (Brahmi)"},
            [], "Plantaginaceae", "Bacopa", "monnieri", "medicinal plant", "native",
            ["Pan-India wetlands (Kerala, West Bengal, Odisha, Uttar Pradesh, Tamil Nadu, Karnataka)"],
            "Small, succulent, oblanceolate to spatulate sessile leaves (1–2 cm) dotted with minute black specks", "Opposite", "Entire", "Inconspicuous", "Bright emerald green",
            "Slender, succulent creeping prostrate stem rooting at every node forming dense carpets, 10–30 cm",
            "Small solitary pale blue, pink, or white 5-lobed flowers on slender axillary pedicels",
            "Ovoid-globose 2-grooved capsule holding numerous minute seeds",
            "Prostrate creeping succulent wetland perennial herb, 10–30 cm",
            "Warm humid tropical and sub-tropical wetlands, marsh edges, and riverbanks",
            "Full sunlight to partial shade", "High; requires consistently saturated, marshy, or waterlogged soil",
            "Wet alluvial loams, clayey marsh soils rich in organic matter, pH 6.0–7.5",
            "Year-round cultivation under wet conditions", ["Stem cuttings with root nodes"],
            ["Renowned Ayurvedic medhya rasayana (brain tonic): enhances memory, cognitive clarity, and neuroplasticity (bacosides A & B)", "Traditional memory syrup (Brahmi Ghrita), herbal teas"],
            "Safe in dietary and herbal amounts.", False,
            [
                {"name": "Damping Off", "type": "fungal", "symptoms": "Rotting of creeping runners in stagnant foul water", "management": "Maintain fresh water flow; avoid foul water stagnation"}
            ],
            ["Maintain standing water layer of 2–3 cm in cultivated paddy-like beds"]
        ),
        make_plant(
            "hibiscus-rosa-sinensis", "Hibiscus rosa-sinensis", "Hibiscus / China Rose / Gudhal", "गुड़हल (Gudhal)",
            "మందారం (Mandaram)", "செம்பருத்தி (Sembaruthi)",
            {"kannada": "ದಾಸವಾಳ (Dasavala)", "malayalam": "ചെമ്പരത്തി (Chembarathi)", "bengali": "জবা (Joba)", "marathi": "जास्वंद (Jaswand)"},
            [], "Malvaceae", "Hibiscus", "rosa-sinensis", "flower", "cultivated",
            ["Pan-India (Tamil Nadu, West Bengal, Kerala, Andhra Pradesh, Maharashtra, Karnataka, Uttar Pradesh)"],
            "Simple, ovate to broadly lanceolate glossy dark green leaves with distinct serrate margins", "Alternate, spiral", "Serrate to dentate", "Palmate-pinnate", "Dark glossy green",
            "Multi-stemmed woody erect branching evergreen shrub, 1.5–4.0 m",
            "Large, showy solitary funnel-shaped 5-petaled flowers (crimson, red, yellow, pink) with long protruding staminal column",
            "Rarely sets capsule under cultivation in India",
            "Vigorous bushy evergreen woody ornamental and medicinal shrub, 1.5–4.0 meters",
            "Warm tropical and sub-tropical climate; completely frost-tender",
            "Full bright sun (6+ hours daily)", "Regular moderate watering; keep moist but well-drained",
            "Fertile, rich, well-drained loamy soil rich in organic compost, pH 6.0–7.0",
            "Year-round continuous blooming in tropics", ["Semi-hardwood stem cuttings or air layering"],
            ["Revered sacred flower offered to deities (Goddess Kali, Lord Ganesha)", "Traditional hair care: petals and leaves crushed into natural conditioning shampoo and hair growth oil", "Hibiscus sour tea rich in Vitamin C and anthocyanins"],
            "Safe for topical and dietary culinary use.", False,
            [
                {"name": "Mealybug (Ferrisia virgata)", "type": "pest", "symptoms": "White waxy clusters on flower buds and leaf axils causing bud drop", "management": "Spray Neem oil (5 ml/L) + liquid soap or Imidacloprid"}
            ],
            ["Prune in early spring to stimulate vigorous new flowering shoots", "Spray iron chelate if interveinal yellowing (chlorosis) appears"]
        ),
        make_plant(
            "jasminum-sambac", "Jasminum sambac", "Arabian Jasmine / Mogra / Chameli", "मोगरा / चमेली (Mogra)",
            "మల్లెపువ్వు (Mallepuvvu)", "மல்லிகை (Malligai / Madurai Malli)",
            {"kannada": "ಮಲ್ಲಿಗೆ (Mallige)", "malayalam": "മുല്ല (Mulla)", "bengali": "বেলি ফুল (Beli Phul)", "marathi": "मोगरा (Mogra)"},
            [], "Oleaceae", "Jasminum", "sambac", "flower", "native",
            ["Tamil Nadu (Madurai)", "Karnataka", "Andhra Pradesh", "Telangana", "Maharashtra", "West Bengal", "Gujarat"],
            "Simple, broadly ovate to elliptic glossy dark green opposite leaves with prominent veins", "Opposite or in whorls of 3", "Entire, slightly undulate", "Pinnate", "Dark lustrous green",
            "Erect or scrambling woody perennial shrub or twining climber, 1–3 m",
            "Intensely fragrant solitary or clustered pure white waxy flowers opening at dusk (single or multi-whorled double petals)",
            "Small globose purple-black berry (rarely produces seeds under cultivation)",
            "Dense bushy evergreen woody shrub or scrambling climber, 1–3 meters",
            "Warm tropical and sub-tropical plains; flourishes in hot sunny summers",
            "Full blazing sun (6–8 hours)", "Regular moderate watering; withstands brief drying",
            "Well-drained rich sandy loam to clay loam rich in organic manure, pH 6.5–7.5",
            "Summer and Monsoon blooming flush (March–September)", ["Semi-hardwood stem cuttings or ground layering"],
            ["World-renowned aromatic floral crop: Madurai Malli garland flowers for temple rituals and weddings", "Mogra attar and perfume extraction, jasmine green tea", "Aromatherapy for relaxation and stress relief"],
            "Safe and celebrated in traditional culture.", False,
            [
                {"name": "Bud Worm (Hendecasis duplifascialis)", "type": "pest", "symptoms": "Caterpillar bores inside unopened white flower buds causing reddish-brown discoloration and bud drop", "management": "Foliar spray of Spinosad 45 SC (0.3 ml/L) or Neem oil"}
            ],
            ["Annual pruning to 45 cm height in November–December is mandatory for profuse summer flowering flushes"]
        ),
        make_plant(
            "rosa-indica", "Rosa indica", "Rose / Gulab / Desi Gulab", "गुलाब (Gulab)",
            "గులాబీ (Gulabi)", "ரோஜா (Roja)",
            {"kannada": "ಗುಲಾಬಿ (Gulabi)", "malayalam": "റോസാപ്പൂവ് (Rosappoovu)", "bengali": "গোলাপ (Golap)", "marathi": "गुलाब (Gulab)"},
            ["Rosa chinensis", "Rosa damascena"], "Rosaceae", "Rosa", "indica", "flower", "cultivated",
            ["Uttar Pradesh (Kannauj)", "Rajasthan (Pushkar)", "Karnataka", "Tamil Nadu", "Maharashtra (Pune)", "West Bengal"],
            "Odd-pinnate compound leaves with 3–7 ovate serrate leaflets and spiny glandular petioles", "Alternate", "Serrate sharp", "Pinnate", "Rich dark green with reddish flush on young growth",
            "Woody, prickly erect or scrambling shrub with curved prickles (thorns) on green stems, 1–2.5 m",
            "Exquisitely fragrant solitary or clustered multi-petaled flowers (pink, red, white, yellow) with numerous stamens",
            "Fleshy red to orange globose hypanthium (rose hip) holding achene seeds",
            "Prickly deciduous or semi-evergreen woody perennial shrub, 1–2.5 meters",
            "Mild temperate to subtropical climate; requires warm sunny days and cool nights for maximum fragrance",
            "Full sunlight (6–8 hours daily)", "Regular moderate watering; keep root zone moist but never waterlogged",
            "Deep, rich, well-drained fertile loamy soil high in organic humus, pH 6.0–6.8",
            "Winter and Spring peak blooming (Desi Gulab, Damask Rose, Hybrid Teas)", ["T-budding on Rosa multiflora rootstock or hardwood cuttings"],
            ["Desi Gulab / Damask Rose for Kannauj rose water (gulab jal) and pure rose attar", "Sweet gulkand (rose petal preserve) for cooling Ayurvedic health", "Commercial cut flower bouquets and garlands"],
            "Stems have sharp prickles (thorns). Wear protective gloves.", False,
            [
                {"name": "Black Spot (Diplocarpon rosae)", "type": "fungal", "symptoms": "Fringed circular black spots on leaves leading to severe yellowing and premature leaf drop", "management": "Foliar spray of Mancozeb (2 g/L) or Trifloxystrobin; water at base, not on leaves"},
                {"name": "Powdery Mildew (Podosphaera pannosa)", "type": "fungal", "symptoms": "White talc-like powdery fungal growth on young leaves, buds, and stems causing distortion", "management": "Spray Wettable Sulfur (2 g/L) or Hexaconazole"}
            ],
            ["Annual pruning in October (cut back to 40 cm with angled cuts) stimulates vigorous winter blooming", "Apply mustard oil cake and bone meal around root basin"]
        ),
        make_plant(
            "tagetes-erecta", "Tagetes erecta", "Marigold / Genda", "गेंदा (Genda)",
            "బంతిపువ్వు (Banthipuvvu)", "சாமந்தி / செண்டுமல்லி (Chendumalli)",
            {"kannada": "ಚೆಂಡುಹೂ (Chenduhu)", "malayalam": "ചെണ്ടുമല്ലി (Chendumalli)", "bengali": "গাঁদা ফুল (Gada Phul)", "marathi": "झेंडू (Zendu)"},
            [], "Asteraceae", "Tagetes", "erecta", "flower", "cultivated",
            ["Maharashtra", "Karnataka", "Gujarat", "Andhra Pradesh", "Telangana", "Haryana", "West Bengal", "Uttar Pradesh"],
            "Pinnately divided feathery aromatic leaves with narrow lanceolate serrate segments dotted with oil glands", "Opposite below, alternate above", "Deeply serrate / pinnatifid", "Pinnate", "Dark green with pungent distinctive aroma",
            "Erect, grooved herbaceous branching stem with strong aromatic scent, 30–100 cm",
            "Large, dense, globose composite flower heads (capitulum) packed with bright orange or yellow ray florets",
            "Slender, compressed black cypsela (achene) topped by pappus bristles",
            "Erect bushy annual herbaceous flowering plant, 30–100 cm",
            "Warm sub-tropical and tropical climate; performs outstandingly in bright dry sunny weather",
            "Full blazing sun (6–8 hours)", "Moderate regular watering; avoids wet soggy soil",
            "Well-drained fertile sandy loam to clay loam rich in organic matter, pH 6.5–7.5",
            "All three seasons (Kharif, Winter, and Summer for festive demand)", ["Certified seed sowing or terminal cuttings"],
            ["Major commercial garland flower for Diwali, Dussehra, pujas, weddings", "Rich source of natural lutein pigment used in eye health supplements and poultry feed", "Potent nematicidal root exudates (alpha-terthienyl) suppress root-knot nematodes in soil"],
            "Safe for cultivation.", False,
            [
                {"name": "Leaf Spot / Blight (Alternaria tagetica)", "type": "fungal", "symptoms": "Circular brownish-black necrotic spots on leaves and flower ray florets", "management": "Foliar spray of Mancozeb (2 g/L)"}
            ],
            ["Plant as companion trap crop around tomato, brinjal, and chilli borders to eliminate parasitic nematodes", "Pinch terminal growing tip at 30 days to stimulate 15–20 productive lateral branches"]
        ),
        make_plant(
            "catharanthus-roseus", "Catharanthus roseus", "Madagascar Periwinkle / Sadabahar", "सदाबहार (Sadabahar)",
            "బిళ్ళగన్నేరు (Billa Ganneru)", "நித்திய கல்யாணி (Nithya Kalyani)",
            {"kannada": "ಸದಾಪುಷ್ಪ (Sadapushpa)", "malayalam": "ശവംനാറി / നിത്യകല്യാണി (Nithyakalyani)", "bengali": "নয়নতারা (Nayantora)", "marathi": "सदाफुली (Sadaphuli)"},
            ["Vinca rosea"], "Apocynaceae", "Catharanthus", "roseus", "medicinal plant", "naturalized",
            ["Pan-India (Tamil Nadu, Karnataka, Andhra Pradesh, Gujarat, Maharashtra, Rajasthan, Uttar Pradesh, West Bengal)"],
            "Simple, opposite, elliptic-obovate glossy dark green leaves with pale midrib and milky sap", "Opposite, decussate", "Entire", "Pinnate with distinct pale midrib", "Glossy dark green",
            "Erect herbaceous to semi-woody branched subshrub with smooth green or purplish stems, 30–90 cm",
            "Salverform 5-lobed flat flowers, pure white or vivid rosy-pink with dark reddish-purple eye",
            "Paired cylindrical dehiscent follicles (2–4 cm) holding small black grooved seeds",
            "Hardy erect bushy perennial subshrub, 30–90 cm",
            "Tropical and sub-tropical semi-arid climate; extraordinary drought and heat tolerance",
            "Full blazing sun to light shade", "Very low; highly drought resistant",
            "Thrives in poor, sandy, gravelly, rocky, and saline soils, pH 6.0–8.0",
            "Year-round continuous flowering (Sadabahar literally means 'ever-blooming')", ["Seeds or soft-wood stem cuttings"],
            ["Commercial source of life-saving vinca alkaloids (vincristine and vinblastine used in chemotherapy for leukemia and Hodgkin's lymphoma)", "Ayurvedic remedies for type 2 diabetes and hypertension", "Hardy ornamental border plant"],
            "CRITICAL TOXICITY WARNING: Contains over 130 powerful cytotoxic indole alkaloids. Plant is poisonous if ingested in unprescribed quantities. Keep away from pets and small children.", True,
            [
                {"name": "Die-back / Twig Blight (Colletotrichum gloeosporioides)", "type": "fungal", "symptoms": "Drying of upper twigs during heavy monsoon", "management": "Ensure good drainage; spray Copper Oxychloride"}
            ],
            ["Thrives in neglected sunny dry gardens with near-zero maintenance"]
        )
    ]

def get_trees_and_ornamentals():
    return [
        make_plant(
            "ficus-benghalensis", "Ficus benghalensis", "Banyan Tree / National Tree of India / Bargad", "बरगद / वटवृक्ष (Bargad)",
            "మర్రి చెట్టు (Marri Chettu)", "ஆலமரம் (Aalamaram)",
            {"kannada": "ಆಲದ ಮರ (Aalada Mara)", "malayalam": "പേരാൽ (Peral)", "bengali": "বটগাছ (Botgach)", "marathi": "वड (Vad)"},
            [], "Moraceae", "Ficus", "benghalensis", "tree", "native",
            ["Pan-India (Uttar Pradesh, Bihar, Andhra Pradesh, Tamil Nadu, Karnataka, Maharashtra, Gujarat, West Bengal)"],
            "Large, coriaceous (leathery), broadly ovate to elliptic glossy leaves with 5–7 prominent basal nerves and milky white latex", "Alternate, spiral", "Entire", "Palmate-pinnate", "Glossy dark green with pale veins",
            "Massive, monumental trunk with smooth grey bark producing descending aerial prop roots from horizontal boughs that root into soil forming auxiliary supporting trunks, 15–30 m tall, spread >100 m",
            "Inconspicuous flowers enclosed inside specialized hollow fleshy receptacle (syconium / fig), pollinated by specialized mutualist fig wasps (Eupristina masoni)",
            "Paired sessile globose figs (1.5–2.5 cm), scarlet-red when ripe in leaf axils",
            "Colossal spreading evergreen canopy tree living for over 500 years, 20–30 meters tall with canopy spread up to 2 hectares",
            "Tropical and sub-tropical plains, roadsides, and village common lands; drought hardy",
            "Full bright sun", "Low to moderate once established; deep taproots and prop roots reach deep water tables",
            "Highly adaptable: alluvial loams, clay loams, rocky crevices, even masonry walls, pH 6.0–8.0",
            "Year-round evergreen foliage; figs mature in spring and summer", ["Seeds spread by birds, air layering, or large hardwood truncheons"],
            ["National Tree of India: cultural symbol of immortality and shelter", "Sacred in Hindu and Buddhist traditions (Vat Savitri puja)", "Aerial prop roots used for traditional toothbrushes; milky latex in Ayurvedic medicine for joint pain", "Massive wildlife refuge for birds, bats, and pollinators"],
            "Produces milky latex sap that may cause mild skin irritation in sensitive people. Safe shade tree.", False,
            [
                {"name": "Fig Wasp Mutualism", "type": "info", "symptoms": "Obligate mutualist fig wasps inhabit figs", "management": "Natural ecological balance; do not spray pesticides on flowering figs"}
            ],
            ["Needs very large open space; never plant within 20 meters of building foundations due to powerful invasive roots"]
        ),
        make_plant(
            "ficus-religiosa", "Ficus religiosa", "Sacred Fig / Peepal / Bodhi Tree", "पीपल (Peepal)",
            "రావి చెట్టు (Raavi Chettu)", "அரசமரம் (Arasamaram)",
            {"kannada": "ಅರಳಿ ಮರ (Arali Mara)", "malayalam": "അരയാൽ (Arayal)", "bengali": "অশ্বত্থ (Oshwottho)", "marathi": "पिंपळ (Pimpal)"},
            [], "Moraceae", "Ficus", "religiosa", "tree", "native",
            ["Pan-India (Bihar - Bodh Gaya, Uttar Pradesh, Madhya Pradesh, Maharashtra, Andhra Pradesh, Tamil Nadu, Karnataka, Punjab)"],
            "Distinctive broadly ovate cordate leaves with a remarkable long, slender, tapering tail-like drip tip (caudate apex, 2–5 cm) that rustles in the slightest breeze", "Alternate, spiral", "Entire, undulate with elongated caudate drip tip", "Palmate with 5–7 basal veins", "Pinkish-copper when young, turning lustrous dark green with ivory veins",
            "Large, massive trunk with smooth grey bark that turns flaking with age, wide spreading irregular canopy, 20–30 m",
            "Inconspicuous flowers enclosed inside hollow syconium, pollinated by specialized fig wasp (Blastophaga quadriceps)",
            "Sessile paired axillary sub-globose figs (1–1.5 cm), green ripening to dark purple-black",
            "Large spreading semi-deciduous to evergreen tree, living for over 1000 years, 20–30 meters",
            "Sub-tropical and tropical climate; extreme heat and drought hardiness",
            "Full blazing sun", "Low; exceptionally drought resilient",
            "Tolerates varied soils: rocks, dry gravel, alkaline soils, brick masonry, pH 6.0–8.5",
            "New copper-pink leaf flush in spring (March–April)", ["Seeds (spread by birds) or hardwood cuttings"],
            ["Supreme sacred tree in Hinduism, Buddhism (Bodhi Tree of Buddha's enlightenment), and Jainism", "Exceptional oxygen release through Crassulacean Acid Metabolism (CAM) pathway at night", "Bark decoction used in Ayurveda for diabetes and wound healing", "Sacred temple tree across India"],
            "Extremely powerful roots can crack concrete foundations and walls. Plant away from buildings.", False,
            [
                {"name": "Natural Ecological Host", "type": "info", "symptoms": "Hosts diverse wild avian species and pollinators", "management": "Conserve as vital biodiversity keystone species"}
            ],
            ["Plant along temple perimeters, village squares, and rural avenues rather than near urban buildings"]
        ),
        make_plant(
            "tectona-grandis", "Tectona grandis", "Indian Teak / Sagwan", "सागवान / सागौन (Sagwan)",
            "టేకు (Teku)", "தேக்கு (Thekku)",
            {"kannada": "ತೇಗ (Tega)", "malayalam": "തേക്ക് (Thekku)", "bengali": "সেগুন (Segun)", "marathi": "सागवान (Sagwan)"},
            [], "Lamiaceae", "Tectona", "grandis", "tree", "native",
            ["Madhya Pradesh (Hoshangabad)", "Maharashtra", "Kerala (Nilambur Teak)", "Karnataka", "Gujarat", "Andhra Pradesh", "Odisha"],
            "Huge, opposite, ovate-elliptic coriaceous leaves (30–60 cm long) with dense whitish-grey stellate tomentum beneath, yielding blood-red sap when crushed", "Opposite, decussate", "Entire", "Pinnate", "Rough dark green above, pale woolly beneath",
            "Tall, straight, majestic cylindrical trunk with thick grey-brown fibrous vertically fissured bark, 20–40 m",
            "Large, erect, branched terminal panicles (40–80 cm) with thousands of small fragrant white flowers",
            "Sub-globose hard bony 4-celled nut enclosed in inflated papery bladder-like calyx (2–3 cm)",
            "Large deciduous timber tree, 20–40 meters tall",
            "Tropical moist and dry deciduous forests with warm monsoon climate and distinct dry season",
            "Full intense sun (strictly light-demanding pioneer tree)", "Moderate (1200–2500 mm rain); deep taproot",
            "Deep, fertile, well-drained alluvial and volcanic black loam soils rich in calcium, pH 6.5–7.5",
            "Deciduous in dry season (Dec–Feb); new flushes in monsoon; harvest timber at 20–30 years", ["Stump planting (root-shoot cuttings from 1-year nursery seedlings)"],
            ["World's premier luxury timber: naturally weather-proof, termite-resistant, dimensionally stable due to natural tectoquinones and silica", "Shipbuilding, yacht decking, fine furniture, architectural joinery"],
            "Safe for cultivation.", False,
            [
                {"name": "Teak Defoliator (Hyblaea puera)", "type": "pest", "symptoms": "Massive caterpillar outbreaks defoliating entire teak forests in early monsoon", "management": "Release biological parasitoids; aerial Bt spray in commercial plantations"},
                {"name": "Teak Skeletonizer (Eutectona machaeralis)", "type": "pest", "symptoms": "Larvae eat leaf tissue leaving only skeleton veins", "management": "Light traps; microbial control"}
            ],
            ["Stump planting (20 cm taproot + 2 cm shoot collar) ensures 95% survival and rapid growth"]
        ),
        make_plant(
            "shorea-robusta", "Shorea robusta", "Sal Tree / Sakhu", "साल / साखू (Sal)",
            "గుగ్గిలం / సాల వృక్షం (Guggilam)", "குங்கிலியம் (Kungiliyam)",
            {"kannada": "ಸಾಲ ಮರ (Saala Mara)", "malayalam": "മരുത് / സാൽ (Sal)", "bengali": "শালগাছ (Shalgach)", "marathi": "राळ (Ral)"},
            [], "Dipterocarpaceae", "Shorea", "robusta", "tree", "native",
            ["Central & Eastern India (Madhya Pradesh, Chhattisgarh, Odisha, Jharkhand, West Bengal, Assam, Uttar Pradesh Terai)"],
            "Simple, coriaceous (leathery), ovate-oblong glossy leaves with pale prominent veins", "Alternate", "Entire", "Pinnate with 12–16 pairs of secondary veins", "Glossy dark green",
            "Tall, massive straight cylindrical trunk with thick dark brown deeply furrowed bark, 20–35 m",
            "Yellowish-white fragrant flowers in large terminal and axillary racemose panicles",
            "Ovoid nut enclosed by 5 enlarged persistent wing-like calyx lobes (3 long, 2 short) facilitating wind dispersal",
            "Large, slow-growing semi-deciduous climax forest tree, 20–35 meters",
            "Sub-tropical and tropical moist deciduous belt; frost-tolerant in Terai foothills",
            "Moderate to full sun", "Moderate to high (1000–2000 mm rain)",
            "Deep, well-drained sandy loam to gravelly lateritic forest soils, pH 5.5–6.8",
            "Flowering in spring (Feb–April), seed fall in May", ["Fresh recalcitrant seeds sown immediately after falling"],
            ["Heavy construction timber for railway sleepers, bridges, house construction (second only to teak)", "Sal resin (dammar) burned as fragrant incense (dhoop)", "Sal seeds yield edible sal butter used in confectionery and cosmetics", "Leaves stitched into traditional disposable dining plates (patravali / dona)"],
            "Safe for forest ecology.", False,
            [
                {"name": "Sal Heartwood Borer (Hoplocerambyx spinicornis)", "type": "pest", "symptoms": "Grubs bore massive galleries into heartwood of mature trees causing tree death and timber destruction", "management": "Trap-tree operation during monsoon to collect and destroy adult beetles"}
            ],
            ["Seeds have zero dormancy (recalcitrant); must be sown within 7 days of collection"]
        ),
        make_plant(
            "terminalia-arjuna", "Terminalia arjuna", "Arjuna Tree / Kahua", "अर्जुन (Arjuna)",
            "మద్ది చెట్టు (Maddi Chettu)", "மருத மரம் (Marutha Maram)",
            {"kannada": "ಮತ್ತಿ ಮರ (Matti Mara)", "malayalam": "നീർമരുത് (Neermaruthu)", "bengali": "অর্জুন (Arjun)", "marathi": "अर्जुन (Arjun)"},
            [], "Combretaceae", "Terminalia", "arjuna", "medicinal plant", "native",
            ["Madhya Pradesh, Uttar Pradesh, Bihar, Maharashtra, Andhra Pradesh, Tamil Nadu, Karnataka, Odisha, West Bengal"],
            "Sub-opposite, oblong-elliptic coriaceous leaves with 1–2 prominent round glands at base of blade", "Sub-opposite", "Entire to crenulate", "Pinnate", "Dull green above, pale green beneath",
            "Massive buttressed trunk with remarkably smooth pinkish-grey peeling bark and spreading canopy, 15–25 m",
            "Small, pale yellowish-white sessile flowers in drooping axillary spikes and terminal panicles",
            "Ovoid-oblong fibrous woody drupe (2.5–5 cm) with 5 prominent hard longitudinal wings",
            "Large majestic buttressed semi-evergreen riverine tree, 15–25 meters",
            "Riverbanks, ravines, and moist stream valleys across peninsular India",
            "Full sun to light shade", "Moderate; thrives along rivercourses with permanent groundwater",
            "Fertile alluvial soils, river silts, and moist loams, pH 6.0–8.0",
            "Flowering in April–July, fruit maturation in winter", ["Seeds (presoaked for 48 hours)"],
            ["Premier Ayurvedic cardioprotective cardiotonic: bark decoction strengthens cardiac muscles, regulates blood pressure, lowers cholesterol (arjunolic acid, flavonoids)", "Host plant for tropical Tasar silkworms (Antheraea mylitta)", "Heavy timber and avenue shade tree"],
            "Safe in traditional Ayurvedic dosage under guidance.", False,
            [
                {"name": "Bark Regrowth", "type": "info", "symptoms": "Bark regenerates naturally if harvested sustainably in vertical strips without girdling", "management": "Harvest bark sustainably leaving 50% circumference intact"}
            ],
            ["Plant along riverbanks and farm pond boundaries to prevent severe soil erosion"]
        ),
        make_plant(
            "delonix-regia", "Delonix regia", "Gulmohar / Royal Poinciana / Flame Tree", "गुलमोहर (Gulmohar)",
            "తురాయి చెట్టు (Thurayi Chettu)", "செம்மயிர்க்கொன்றை (Semmayirkkondrai)",
            {"kannada": "ಕತ್ತಿಕಾಯಿ ಮರ (Katthikayi Mara)", "malayalam": "ഗുൽമോഹർ (Gulmohar)", "bengali": "কৃষ্ণচূড়া (Krishnachura)", "marathi": "गुलमोहर (Gulmohar)"},
            [], "Fabaceae", "Delonix", "regia", "ornamental", "naturalized",
            ["Pan-India (Maharashtra, Karnataka, Tamil Nadu, West Bengal, Uttar Pradesh, Delhi, Andhra Pradesh, Gujarat)"],
            "Bipinnate feathery compound leaves (30–50 cm) with 20–40 pairs of pinnae and hundreds of tiny oblong leaflets that fold at sunset", "Alternate", "Entire", "Pinnate feathery", "Fresh vibrant light green",
            "Broad spreading umbrella-like flat-topped canopy with smooth grey bark and buttressed base, 10–18 m",
            "Spectacular mass displays of large brilliant scarlet-orange 5-petaled flowers; fifth petal (standard) is white-streaked with red and yellow",
            "Massive, woody, flattened pendulous dark brown/black pod (30–65 cm long) persisting on tree",
            "Spreading flat-topped umbrella-canopy deciduous ornamental tree, 10–18 meters",
            "Warm tropical and sub-tropical plains; flourishes in hot dry summers",
            "Full bright sun (8 hours)", "Low to moderate once established; drought hardy",
            "Well-drained sandy, loamy, or gravelly soils, pH 6.0–7.5",
            "Spectacular blooming in peak summer heat (April–June)", ["Seeds (presoaked in hot water to soften hard seed coat)"],
            ["One of the world's most spectacular ornamental flowering avenue trees (Flame of the Forest)", "Provides expansive cooling shade in hot Indian summers"],
            "Superficial spreading root system; can lift pavements if planted too close to walkways.", False,
            [
                {"name": "Wind Damage", "type": "physiological", "symptoms": "Brittle branches can snap in severe monsoon squalls", "management": "Prune weak crotches in young trees"}
            ],
            ["Soak hard seeds in boiling water for 10 seconds then warm water for 24 hours to trigger 90% germination"]
        ),
        make_plant(
            "samanea-saman", "Samanea saman", "Rain Tree / Vilayati Siris", "विलायती सिरिस / रेन ट्री (Rain Tree)",
            "నిద్రగన్నేరు (Nidraganneru)", "தூங்குமூஞ்சி மரம் (Thoongumoonji Maram)",
            {"kannada": "ಮಳೆ ಮರ (Male Mara)", "malayalam": "മഴമരം (Mazhamaram)", "bengali": "শিরীষ / রেনট্রি (Raintree)", "marathi": "रेन ट्री (Rain Tree)"},
            ["Albizia saman"], "Fabaceae", "Samanea", "saman", "tree", "naturalized",
            ["Pan-India (West Bengal, Tamil Nadu, Maharashtra, Karnataka, Kerala, Andhra Pradesh)"],
            "Bipinnate compound leaves with 2–6 pairs of pinnae; leaflets fold together during cloudy overcast weather and at night (giving name 'sleeping tree')", "Alternate", "Entire", "Pinnate", "Dark green above, finely downy beneath",
            "Short stout trunk with dark grey rough fissured bark and an immense, broad dome-shaped spreading canopy (up to 40 m wide), 15–25 m",
            "Showy powder-puff clusters of bi-colored pink and white flowers with numerous long silky stamens",
            "Thick, oblong, flattened black woody pod (15–20 cm) with sweet sticky pulp and brown seeds",
            "Giant umbrella-canopy spreading semi-deciduous tree, 15–25 meters tall with 30–50 m crown",
            "Warm humid tropical plains and coastal cities",
            "Full sun", "Moderate; deep root system",
            "Fertile alluvial loams and urban soils, pH 6.0–7.5",
            "Spring and summer flowering flush", ["Seeds"],
            ["Monumental shade and avenue tree for wide boulevards, public parks, and campus grounds", "Sweet pods eaten by cattle (monkeys and livestock)"],
            "Safe avenue tree.", False,
            [
                {"name": "Powdery Mildew", "type": "fungal", "symptoms": "Mild foliar mildew in humid seasons", "management": "Natural biocontrol"}
            ],
            ["Needs very wide avenues due to immense horizontal branch spread (over 30 meters)"]
        ),
        make_plant(
            "eucalyptus-globulus", "Eucalyptus globulus", "Tasmanian Blue Gum / Nilgiri Eucalyptus", "नीलगिरी (Nilgiri)",
            "నీలగిరి చెట్టు (Neelagiri Chettu)", "நீலகிரி மரம் (Neelagiri Maram)",
            {"kannada": "ನೀಲಗಿರಿ (Neelagiri)", "malayalam": "യൂക്കാലിപ്റ്റസ് (Eucalyptus)", "bengali": "ইউক্যালিপটাস (Eucalyptus)", "marathi": "निलगिरी (Nilgiri)"},
            [], "Myrtaceae", "Eucalyptus", "globulus", "tree", "cultivated",
            ["Tamil Nadu (Nilgiris, Kodaikanal)", "Karnataka", "Andhra Pradesh", "Punjab", "Haryana", "Himachal Pradesh"],
            "Dimorphic: juvenile leaves opposite, sessile, ovate, glaucous silvery-blue; adult leaves alternate, falcate (curved sickle-shaped) lanceolate, coriaceous, aromatic with cineole", "Alternate (adult)", "Entire", "Pinnate with intramarginal vein", "Silvery-blue (juvenile) to dark green (adult)",
            "Exceptionally tall, straight cylindrical trunk with peeling ribbons of smooth bluish-white and grey bark, 20–55 m",
            "Solitary or clustered cream-white flowers with operculum (cap) and numerous showy stamens",
            "Hard woody 4-ribbed top-shaped warty capsule releasing minute seeds",
            "Gigantic fast-growing evergreen hardwood tree, 20–55 meters",
            "Sub-tropical and temperate mountain plateaus (Nilgiri hills, 1500–2500 m) and irrigated plains",
            "Full intense sun", "High water uptake capacity; deep taproot extracts subsoil water",
            "Deep, well-drained loamy soils; avoids waterlogged poorly drained pans, pH 5.0–7.0",
            "Harvested for pulpwood on 5–7 year short coppice rotation", ["Seeds or clonal rooted ramets"],
            ["Commercial paper pulpwood and rayon manufacture", "Nilgiri eucalyptus essential oil (cineole/eucalyptol) for cold decongestants, balms, and liniments", "Poles for scaffolding and rural construction"],
            "Concentrated pure eucalyptus oil is toxic if swallowed in quantity. High water consumption makes it unsuitable directly adjacent to water-sensitive field crops.", False,
            [
                {"name": "Gall Wasp (Leptocybe invasa)", "type": "pest", "symptoms": "Swollen galls on midribs and young petioles causing leaf curl and stunting", "management": "Release Quadrastichus mendeli parasitoid; plant tolerant clones"}
            ],
            ["Plant as agroforestry windbreak along field edges with deep root barriers"]
        ),
        make_plant(
            "bambusa-vulgaris", "Bambusa vulgaris", "Common Bamboo / Golden Bamboo / Bans", "बांस (Bans)",
            "వెదురు (Veduru)", "மூங்கில் (Moongil)",
            {"kannada": "ಬಿದಿರು (Bidiru)", "malayalam": "മുള (Mula)", "bengali": "বাঁশ (Bansh)", "marathi": "बांबू (Bambu)"},
            [], "Poaceae", "Bambusa", "vulgaris", "grass", "native",
            ["Assam", "West Bengal", "Odisha", "Madhya Pradesh", "Karnataka", "Kerala", "Maharashtra", "Tamil Nadu"],
            "Linear-lanceolate smooth leaves with short petiole and hairy sheaths on branching nodes", "Alternate, 2-ranked", "Scabrous entire", "Parallel with cross veinlets", "Lustrous green or green with yellow striping",
            "Giant clump-forming woody jointed culms (stems) with thick walls and prominent ring nodes, 10–20 m tall, 4–10 cm diameter",
            "Large leafless compound panicles with clusters of spikelets (flowers once in several decades: gregarious monocarpic flowering)",
            "Caryopsis (bamboo rice, produced once in 30–50 years after mass flowering)",
            "Giant clump-forming woody perennial arborescent grass, 10–20 meters",
            "Humid tropical and subtropical riverbanks, moist valleys, and forest margins",
            "Full sun to light shade", "Moderate to high; responds rapidly to monsoon moisture",
            "Fertile, well-drained alluvial loams and river silts; avoids heavy poorly drained clays, pH 5.5–7.0",
            "New shoots emerge rapidly during monsoon (June–September)", ["Rhizome offsets, culm cuttings, or tissue culture"],
            ["'Green Gold': scaffolding, construction poles, furniture, handicraft baskets, paper pulp", "Tender young bamboo shoots cooked in Northeast Indian cuisine (bamboo shoot curry)", "Soil erosion control on riverbanks"],
            "Raw shoots contain cyanogenic glycosides; must be boiled thoroughly with water discarded before consumption.", False,
            [
                {"name": "Bamboo Borer (Dinoderus minutus)", "type": "pest", "symptoms": "Fine powder falling from harvested dry bamboo culms", "management": "Soak harvested culms in boric acid-borax solution (1:1 @ 2%) for 48 hours"}
            ],
            ["Harvest mature 3–4 year old culms while leaving young 1–2 year culms to nourish clump"]
        ),
        make_plant(
            "vachellia-nilotica", "Vachellia nilotica", "Babool / Gum Arabic Tree / Kikar", "बबूल / कीकर (Babool)",
            "తుమ్మ చెట్టు (Thumma Chettu)", "கருவேலம் (Karuvelam)",
            {"kannada": "ಜಾಲಿ ಮರ (Jali Mara)", "malayalam": "കരിവേലം (Karivelam)", "bengali": "বাবলা (Babla)", "marathi": "बाभळ (Babhul)"},
            ["Acacia nilotica", "Acacia arabica"], "Fabaceae", "Vachellia", "nilotica", "tree", "native",
            ["Rajasthan", "Gujarat", "Haryana", "Punjab", "Maharashtra", "Andhra Pradesh", "Karnataka", "Madhya Pradesh"],
            "Bipinnate feathery compound leaves with 3–6 pairs of pinnae and 10–25 pairs of minute oblong leaflets; sharp paired straight white stipular spines at nodes", "Alternate", "Entire", "Pinnate", "Dark grey-green",
            "Stout, crooked trunk with blackish deeply fissured rough bark and rounded crown, 6–15 m",
            "Globose fluffy bright golden-yellow fragrant flower heads clustered in leaf axils",
            "Constricted, deeply lobed grey-white felted indehiscent pod (necklace-like necklace pod, 10–15 cm) with brown seeds",
            "Hardy spiny evergreen or semi-deciduous tree, 6–15 meters",
            "Arid and semi-arid desert plains, black cotton soil tracts, and saline wastelands; heat and drought champion",
            "Full blazing sun", "Low; exceptional drought hardiness; tolerates seasonal flooding",
            "Deep black cotton soils, saline-alkaline tracts, and gravelly alluvium, pH 6.5–9.0",
            "Flowering in monsoon (June–Sept), pods ripen in winter", ["Seeds (presoaked in sulfuric acid or cow dung slurry)"],
            ["Ayurvedic dental twig (babool datun) for oral hygiene and gum strengthening", "High-tannin bark used for leather tanning", "Nutritious protein pods and foliage for goats and camels in arid zones", "Natural Gum Arabic (babul gond) used in sweets (gond ke laddu) and pharmaceuticals"],
            "Sharp straight white thorns (1–5 cm long). Wear thick gloves when handling.", False,
            [
                {"name": "Powdery Mildew", "type": "fungal", "symptoms": "White fungal coating on young leaves", "management": "Natural tolerance in arid conditions"}
            ],
            ["Outstanding species for reclaiming degraded sodic soils and barren ravines"]
        ),
        make_plant(
            "bougainvillea-spectabilis", "Bougainvillea spectabilis", "Bougainvillea / Paper Flower", "बोगनवेलिया (Bougainvillea)",
            "కాగితాల పూలు (Kagithala Poolu)", "காகிதப்பூ (Kagithapoo)",
            {"kannada": "ಕಾಗದದ ಹೂವು (Kagadada Huvu)", "malayalam": "കടലാസുപൂവ് (Kadalasoopoovu)", "bengali": "বাগানবিলাস (Baganbilas)", "marathi": "बोगनवेल (Boganvel)"},
            [], "Nyctaginaceae", "Bougainvillea", "spectabilis", "ornamental", "naturalized",
            ["Pan-India (Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Kolkata, Jaipur, Lucknow)"],
            "Simple, ovate to broadly elliptic leaves with soft pubescence and sharp curved axillary thorns", "Alternate", "Entire", "Pinnate", "Rich green with distinct veins",
            "Vigorous scrambling woody climbing liana or trained hedge shrub with sharp curved spines, 3–12 m",
            "Small tubular creamy-white flowers surrounded by 3 large, papery, brightly colored petal-like bracts (magenta, purple, red, orange, pink, white)",
            "Inconspicuous ribbed achene (rarely sets seed under cultivation)",
            "Vigorous woody perennial scrambling thorny climber or pruned shrub, 3–12 meters",
            "Tropical and sub-tropical plains; withstands extreme heat, dry weather, and urban traffic pollution",
            "Full blazing sun (needs 6+ hours of intense sun for heavy blooming)", "Low; drought stress triggers profuse flower bract emergence",
            "Well-drained sandy loam or garden soil; dislikes heavy waterlogged soil, pH 5.5–7.0",
            "Year-round blooming with peak flushes in dry summer and winter", ["Hardwood or semi-hardwood stem cuttings"],
            ["India's most popular colorful ornamental boundary hedge, compound wall cover, and pergola climber", "Air pollution tolerant and livestock-resistant living fence"],
            "Equipped with sharp curved thorns. Safe ornamental.", False,
            [
                {"name": "Leaf-eating Caterpillars", "type": "pest", "symptoms": "Chewed holes in colorful bracts", "management": "Hand picking or neem spray"}
            ],
            ["Withhold water slightly to induce spectacular mass blooming flushes", "Prune hard after flowering flushes"]
        ),
        make_plant(
            "epipremnum-aureum", "Epipremnum aureum", "Money Plant / Golden Pothos / Devil's Ivy", "मनी प्लांट (Money Plant)",
            "మనీ ప్లాంట్ (Money Plant)", "மணி பிளான்ட் (Money Plant)",
            {"kannada": "ಮನಿ ಪ್ಲಾಂಟ್ (Money Plant)", "malayalam": "മണി പ്ലാന്റ് (Money Plant)", "bengali": "মানিপ্ল্যান্ট (Money Plant)", "marathi": "मनी प्लांट (Money Plant)"},
            [], "Araceae", "Epipremnum", "aureum", "ornamental", "naturalized",
            ["Pan-India (ubiquitous indoor houseplant and shaded garden climber across all states)"],
            "Heart-shaped (cordate) glossy waxy leaves with golden-yellow or creamy-white variegated marbling; juvenile leaves small (10–15 cm), climbing adult leaves gigantic (up to 1 m) with natural perforations", "Alternate", "Entire (juvenile) to pinnatifid (mature climbing)", "Palmate-pinnate", "Lustrous emerald green with yellow/cream variegation",
            "Succulent climbing or trailing vine with aerial adventitious clinging roots at every node, 2–15 m",
            "Spadix in spathe (rarely or never flowers in cultivation; blind liana)",
            "Propagated exclusively vegetatively via stem cuttings",
            "Trailing evergreen perennial climber or indoor pot vine, 1–15 meters",
            "Tropical warm humid climate; thrives in indoors room temperature (18°C–32°C)",
            "Bright indirect light to partial shade (leaves burn in direct midday scorching sun)", "Moderate; allow top 2 inches of soil to dry between waterings; also thrives purely in clean water jars",
            "Porous, well-drained potting mix (soil, cocopeat, compost 1:1:1), pH 6.0–7.0",
            "Year-round continuous indoor/outdoor vegetative growth", ["Single-node stem cuttings rooted in soil or water"],
            ["India's most famous indoor lucky plant; associated with positive Vastu and prosperity", "NASA Clean Air study top indoor air purifier (removes formaldehyde, benzene, xylene)", "Trailing hanging baskets, moss-stick vertical poles"],
            "Contains insoluble calcium oxalate needle crystals. Chewing leaves causes oral swelling and burning. Keep away from chewing pets (cats and dogs).", True,
            [
                {"name": "Root Rot", "type": "fungal", "symptoms": "Yellowing mushy leaves from overwatering in non-draining pots", "management": "Reduce watering; use pots with drainage holes"}
            ],
            ["Grows indefinitely in simple glass jars filled with clean water changed weekly", "Train on moss pole to double leaf size"]
        ),
        make_plant(
            "dracaena-trifasciata", "Dracaena trifasciata", "Snake Plant / Mother-in-Law's Tongue", "स्नेक प्लांट (Snake Plant)",
            "స్నేక్ ప్లాంట్ (Snake Plant)", "பாம்பு செடி (Snake Plant)",
            {"kannada": "ಸ್ನೇಕ್ ಪ್ಲಾಂಟ್ (Snake Plant)", "malayalam": "പാമ്പ് ചെടി (Snake Plant)", "bengali": "স্নেক প্ল্যান্ট (Snake Plant)", "marathi": "स्नेक प्लांट (Snake Plant)"},
            ["Sansevieria trifasciata"], "Asparagaceae", "Dracaena", "trifasciata", "ornamental", "naturalized",
            ["Pan-India (popular indoor plant across all Indian cities and corporate workspaces)"],
            "Rigid, erect, sword-shaped thick succulent fibrous leaves with sharp fibrous tips and dark green zigzag cross-banding, often with creamy-yellow golden margins (Laurentii)", "Basal rosette", "Entire", "Parallel fibrous", "Dark green with light grey-green transverse bands and yellow margins",
            "Stemless succulent perennial arising from tough creeping horizontal underground orange rhizome, 40–120 cm",
            "Slender raceme of fragrant greenish-white tubular flowers (infrequent indoors)",
            "Small globose orange-red berry",
            "Erect architectural clump-forming evergreen succulent, 40–120 cm",
            "Warm tropical and sub-tropical indoor/outdoor climate; near indestructible",
            "Extremely versatile: thrives in low light, fluorescent office lights, to full bright sun", "Very low; allow potting mix to dry out completely between waterings (once every 2–3 weeks)",
            "Very well-drained sandy potting soil, cactus mix, or perlite-rich loam, pH 6.0–7.5",
            "Year-round evergreen architectural plant", ["Rhizome division or leaf blade cuttings"],
            ["Top-ranked NASA air-purifying plant: removes airborne toxins (benzene, formaldehyde, trichloroethylene)", "Produces oxygen at night via Crassulacean Acid Metabolism (ideal bedroom plant)", "Modern indoor architecture and low-maintenance landscaping"],
            "Contains saponins; mildly toxic to dogs and cats if chewed in quantity.", True,
            [
                {"name": "Overwatering Soft Rot", "type": "fungal", "symptoms": "Mushy brown leaves collapsing at base", "management": "Withhold water; ensure drainage hole is never blocked"}
            ],
            ["The number one rule: when in doubt, do not water. Snake plants thrive on neglect"]
        ),
        make_plant(
            "dypsis-lutescens", "Dypsis lutescens", "Areca Palm / Butterfly Palm / Golden Cane Palm", "अरेका पाम (Areca Palm)",
            "అరెకా పామ్ (Areca Palm)", "அரேகா பாம் (Areca Palm)",
            {"kannada": "ಅರೆಕಾ ಪಾಮ್ (Areca Palm)", "malayalam": "അരെക്ക പാം (Areca Palm)", "bengali": "আরেকা পাম (Areca Palm)", "marathi": "अरेका पाम (Areca Palm)"},
            ["Chrysalidocarpus lutescens"], "Arecaceae", "Dypsis", "lutescens", "ornamental", "naturalized",
            ["Pan-India (popular ornamental clumping landscape and indoor container palm)"],
            "Pinnate arching graceful feathery fronds (1.5–2 m) with 40–60 pairs of narrow lanceolate leaflets and golden-yellow petioles", "Clustered crown", "Entire", "Parallel", "Vibrant bright green with yellow-green midribs",
            "Multi-stemmed clump-forming clustered bamboo-like ringed canes, golden-yellow to green, 2–6 m",
            "Branched panicles of small yellow flowers emerging below leaf crown",
            "Small oblong yellowish fruit turning black when ripe",
            "Multi-stemmed clumping evergreen feather palm, 2–6 meters",
            "Warm, humid tropical climate; sensitive to dry scorching hot winds and frost",
            "Bright indirect filtered sunlight (direct harsh midday summer sun scorches foliage)", "Moderate regular moisture; keep root ball evenly moist with good drainage",
            "Rich, loose, well-drained potting mix with compost and cocopeat, pH 6.0–7.0",
            "Year-round evergreen ornamental growth", ["Clump division or fresh seeds"],
            ["India's most popular indoor luxury container palm and garden border screening palm", "Top-rated indoor humidifier and air purifier (removes airborne xylene and toluene)", "Non-toxic to pets"],
            "Completely non-toxic to dogs, cats, and humans. Safe indoor plant.", False,
            [
                {"name": "Spider Mites (Tetranychidae)", "type": "pest", "symptoms": "Fine webbing beneath fronds, stippled yellowing foliage in dry indoor air", "management": "Mist fronds regularly; spray neem oil or water jet"}
            ],
            ["Use filtered or rested tap water to avoid brown crispy leaf tips from fluoride/chlorine salts", "Wipe dust off fronds monthly"]
        )
    ]

def save_all():
    med_and_spices = get_medicinal_and_spices()
    trees_and_ornamentals = get_trees_and_ornamentals()
    
    with open(DATA_DIR / "medicinal_and_spices.json", "w", encoding="utf-8") as f:
        json.dump(med_and_spices, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(med_and_spices)} medicinal and spice records in medicinal_and_spices.json")
    
    with open(DATA_DIR / "trees_and_ornamentals.json", "w", encoding="utf-8") as f:
        json.dump(trees_and_ornamentals, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(trees_and_ornamentals)} tree and ornamental records in trees_and_ornamentals.json")

if __name__ == "__main__":
    save_all()
