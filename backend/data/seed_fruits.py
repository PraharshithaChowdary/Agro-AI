"""
AGRO AI — Indian Fruit Plants Seed Data
Contains verified botanical records for Mango, Banana, Guava, Papaya, Coconut,
Arecanut, Jackfruit, Pomegranate, Grapes, Lemon, Lime, Sweet Orange, Sapota,
Custard Apple, Amla, Tamarind, Jamun, Watermelon, Muskmelon, Pineapple, and Ber.
"""

import json
from pathlib import Path
from generate_verified_seed_catalog import make_plant, DATA_DIR

def get_fruits():
    return [
        make_plant(
            "mangifera-indica", "Mangifera indica", "Mango / King of Fruits / Aam", "आम (Aam)",
            "మామిడి (Mamidi)", "மாம்பழம் (Mambazham)",
            {"kannada": "ಮಾವಿನ ಹಣ್ಣು (Mavina Hannu)", "malayalam": "മാങ്ങ (Maanga)", "bengali": "আম (Aam)", "marathi": "आंबा (Aamba)"},
            [], "Anacardiaceae", "Mangifera", "indica", "fruit plant", "native",
            ["Uttar Pradesh", "Andhra Pradesh", "Karnataka", "Bihar", "Gujarat", "Maharashtra", "West Bengal", "Telangana"],
            "Simple, coriaceous (leathery), oblong-lanceolate leaves, copper-red when young turning dark lustrous green", "Alternate, spiral", "Entire, wavy", "Pinnate", "Dark glossy green",
            "Stout, erect trunk with rough, dark grey-brown fissured bark and dense spreading dome canopy, 10–30 m",
            "Terminal large branched panicles with thousands of tiny fragrant yellowish-pink flowers (hermaphrodite and male)",
            "Large fleshy drupe with prominent resinous stone (endocarp), yellow/orange/red skin with sweet juicy pulp",
            "Large majestic evergreen canopy tree, 10–30 meters tall",
            "Tropical and sub-tropical climate; distinct dry period essential for profuse winter flowering",
            "Full blazing tropical sun (8+ hours daily)", "Moderate; critical during fruit development; withhold before flowering",
            "Deep, well-drained alluvial loams and fertile red loams, pH 5.5–7.5",
            "Spring flowering (Jan–March), summer harvest (April–July)", ["Veneer grafting, epicotyl grafting, inarching"],
            ["King of fruits; eaten fresh (Alphonso, Banganapalli, Dasheri, Kesar, Langra)", "Processed: mango pulp, aam papad, pickles, mango lassi", "Mango wood for religious havans and timber"],
            "Mango sap / stem peel contains urushiol contact resin causing contact dermatitis in allergic individuals.", False,
            [
                {"name": "Anthracnose (Colletotrichum gloeosporioides)", "type": "fungal", "symptoms": "Dark brown tear-stain necrotic spots on foliage, blossom blight, and black rotting on ripening fruits", "management": "Foliar Copper Oxychloride (2.5 g/L) or Carbendazim (1 g/L)"},
                {"name": "Powdery Mildew (Oidium mangiferae)", "type": "fungal", "symptoms": "White powdery fungal growth covering panicles causing total flower drop and fruit drop", "management": "Wettable Sulfur (2 g/L) or Dinocap (1 ml/L) at panicle emergence"}
            ],
            ["Spray Paclobutrazol (Cultar) in soil basin in Sept-Oct to promote profuse flowering", "Prune congested dead branches after post-harvest to allow sunlight into canopy"]
        ),
        make_plant(
            "musa-acuminata", "Musa acuminata", "Banana / Plantain / Kela", "केला (Kela)",
            "అరటి (Arati)", "வாழைப்பழம் (Vazhaippazham)",
            {"kannada": "ಬಾಳೆಹಣ್ಣು (Balehannu)", "malayalam": "വാഴപ്പഴം (Vazhappazham)", "bengali": "কলা (Kola)", "marathi": "केळे (Kele)"},
            ["Musa paradisiaca", "Musa sapientum"], "Musaceae", "Musa", "acuminata", "fruit plant", "cultivated",
            ["Tamil Nadu", "Maharashtra", "Gujarat", "Andhra Pradesh", "Karnataka", "Kerala", "Bihar", "West Bengal"],
            "Gigantic oblong-elliptic smooth arching blades with prominent central midrib and lateral transverse parallel veins", "Spirally arranged", "Entire, tearing naturally along transverse veins in wind", "Parallel-pinnate", "Bright lush green",
            "Pseudostem formed by tightly packed overlapping concentric leaf sheaths, 2–6 m tall",
            "Large terminal pendulous inflorescence with purple-red ovate bracts, female flowers at base, male bud (heart) at tip",
            "Elongated parthenocarpic fleshy berry (finger) in tiered clusters (hands) along central stalk (bunch)",
            "Large arborescent perennial evergreen giant herb, 2–6 meters",
            "Warm, humid tropical climate with high rainfall and temperature 22°C–35°C; highly sensitive to frost",
            "Full sun (6–8 hours)", "High water requirement (1800–2200 mm); sensitive to drought stress",
            "Deep, rich, well-drained loamy to clay loam soils with high organic matter, pH 6.0–7.5",
            "Year-round planting and harvesting (Grand Naine, Robusta, Poovan, Nendran)", ["Sword suckers (1.5–2.0 kg) or certified tissue culture plantlets"],
            ["Major fruit crop; fresh dessert fruit, baby food, chips, plantain curry", "Flower heart (vazhaipoo) and pseudostem core (vazhaithandu) cooked as vegetables", "Broad leaves used as traditional biodegradable dining plates across South India"],
            "Safe for consumption.", False,
            [
                {"name": "Panama Wilt (Fusarium oxysporum f. sp. cubense)", "type": "fungal", "symptoms": "Yellowing of lower leaf margins, petiole buckling, vascular discoloration of pseudostem, plant collapse", "management": "Plant resistant Grand Naine; dip suckers in Carbendazim (2 g/L); apply Trichoderma viride with FYM"},
                {"name": "Sigatoka Leaf Spot (Pseudocercospora musae)", "type": "fungal", "symptoms": "Spindle-shaped chlorotic streaks turning dark brown/black with light grey sunken centers", "management": "Foliar spray of Propiconazole (1 ml/L) mixed with mineral oil"}
            ],
            ["De-suckering: retain only one follower sucker per clump to channel nutrients to main bunch", "Bag developing bunch with perforated blue polyethylene sleeves to protect from sunburn and thrips"]
        ),
        make_plant(
            "psidium-guajava", "Psidium guajava", "Guava / Amrood", "अमरूद (Amrood)",
            "జామ (Jaama)", "கொய்யாப்பழம் (Koyyappazham)",
            {"kannada": "ಸೀಬೆಹಣ್ಣು (Seebehannu)", "malayalam": "പേരയ്ക്ക (Perakka)", "bengali": "পেয়ারা (Peyara)", "marathi": "पेरू (Peru)"},
            [], "Myrtaceae", "Psidium", "guajava", "fruit plant", "naturalized",
            ["Uttar Pradesh (Allahabad)", "Madhya Pradesh", "Bihar", "Andhra Pradesh", "Maharashtra", "Gujarat", "Karnataka", "West Bengal"],
            "Simple, elliptic to oblong leathery leaves with prominent raised parallel veins beneath", "Opposite, decussate", "Entire", "Pinnate with sunken veins above", "Dull medium green with aromatic glandular dots",
            "Smooth, thin, peeling coppery-brown bark with green patches, quadrangular young twigs, 3–8 m",
            "White solitary or 2–3 clustered flowers with numerous showy white stamens",
            "Globose to pyriform berry with persistent calyx, green skin ripening yellow, white or pink pulp with hard seeds",
            "Small evergreen or semi-deciduous tree or spreading shrub, 3–8 meters",
            "Tropical and sub-tropical climate; highly adaptable and drought hardy",
            "Full sunlight (8 hours)", "Moderate; drought tolerant once established",
            "Tolerates varied soils: alluvial loams, clay loams, red soils; withstands soil salinity and pH 4.5–8.2",
            "Two main crops: Mrig Bahar (winter fruiting, superior quality) and Ambe Bahar (monsoon fruiting)", ["Air layering (guttee), wedge grafting, or budding (Lucknow 49 / Sardar, Allahabad Safeda)"],
            ["High-vitamin C fruit (4 times higher than orange); eaten fresh with chaat masala", "Jams, jellies (high natural pectin content), guava nectar", "Tender leaves boiled for mouth ulcers and gastrointestinal soothing"],
            "Safe for human nutrition.", False,
            [
                {"name": "Guava Wilt (Fusarium oxysporum f. sp. psidii)", "type": "fungal", "symptoms": "Rapid yellowing and browning of leaves, twig die-back, complete wilting of mature tree", "management": "Drench basin with Carbendazim (2 g/L); graft on resistant Psidium cattleianum rootstock"}
            ],
            ["Withhold irrigation in summer to force winter Mrig Bahar crop", "Fruit bagging with foam nets protects from fruit flies"]
        ),
        make_plant(
            "carica-papaya", "Carica papaya", "Papaya / Papita", "पपीता (Papita)",
            "బొప్పాయి (Boppayi)", "பப்பாளி (Pappali)",
            {"kannada": "ಪಪ್ಪಾಯಿ (Pappayi)", "malayalam": "പപ്പായ (Pappaya)", "bengali": "পেঁপে (Pnepne)", "marathi": "पपई (Papai)"},
            [], "Caricaceae", "Carica", "papaya", "fruit plant", "naturalized",
            ["Andhra Pradesh", "Gujarat", "Karnataka", "Madhya Pradesh", "Maharashtra", "West Bengal", "Tamil Nadu", "Telangana"],
            "Large, palmately 7–11 deeply lobed leaves (50–70 cm across) with hollow cylindrical petioles (1 m)", "Spirally clustered at stem apex", "Deeply lobed", "Palmate", "Vibrant light green to dark green",
            "Soft-wooded, erect, hollow unbranched single cylindrical trunk with prominent leaf scars, 2–8 m",
            "Polygamous (dioecious, gynodioecious, hermaphrodite): waxy creamy-white to yellow fragrant tubular flowers",
            "Large cylindrical to globose berry (0.5–3.0 kg), orange-yellow skin, salmon-orange flesh with gelatinous black seeds",
            "Fast-growing soft-wooded herbaceous tree-like perennial, 2–8 meters",
            "Warm tropical climate; completely intolerant of frost and waterlogging",
            "Full sunlight (8 hours daily)", "Regular moderate moisture; collar region must stay dry to prevent stem rot",
            "Deep, fertile, well-drained rich sandy loam with high organic matter, pH 6.0–7.0",
            "Year-round fruiting (Red Lady 786, Pusa Delicious, Coorg Honey Dew)", ["Seed sowing in nursery polybags"],
            ["Sweet dessert fruit rich in beta-carotene and Vitamin C", "Raw green papaya cooked in curries (som tam, chutney)", "Latex source of papain enzyme for meat tenderizing and digestive therapeutics"],
            "Unripe green papaya latex contains papain enzyme; pregnant women are advised to avoid raw unpeeled papaya.", False,
            [
                {"name": "Papaya Ringspot Virus (PRSV)", "type": "viral", "symptoms": "Yellow mosaic mottling on leaves, shoestring distortion, water-soaked oily rings on stems and fruits", "management": "Vector aphid control with systemic insecticides; rogue infected trees immediately"},
                {"name": "Foot Rot / Stem Rot (Pythium aphanidermatum)", "type": "fungal", "symptoms": "Water-soaked soft rotting at soil collar level causing tree toppling", "management": "Ensure elevated mound planting; drench collar with Metalaxyl + Mancozeb (2.5 g/L)"}
            ],
            ["Plant on 20 cm raised mounds to ensure water never pools around stem collar", "Maintain 1 male tree for every 10 female trees in dioecious orchards"]
        ),
        make_plant(
            "cocos-nucifera", "Cocos nucifera", "Coconut Palm / Kalpavriksha / Nariyal", "नारियल (Nariyal)",
            "కొబ్బరి (Kobbari)", "தேங்காய் (Thengai)",
            {"kannada": "ತೆಂಗಿನಕಾಯಿ (Tenginakayi)", "malayalam": "തേങ്ങ (Thenga)", "bengali": "নারকেল (Narkel)", "marathi": "नारळ (Naral)"},
            [], "Arecaceae", "Cocos", "nucifera", "plantation", "native",
            ["Kerala", "Tamil Nadu", "Karnataka", "Andhra Pradesh", "Odisha", "West Bengal", "Goa", "Maharashtra", "Gujarat"],
            "Large pinnately divided feather-like arching fronds (4–6 m long) with numerous linear-lanceolate rigid leaflets", "Crown rosette", "Entire", "Parallel", "Lustrous emerald green to golden green",
            "Tall, slender, unbranched cylindrical ringed trunk with swollen base and adventitious root bole, 15–30 m",
            "Monoecious: spadix inflorescence enclosed in woody spathe; male flowers numerous at tip, female button flowers at base",
            "Large fibrous 3-sided ovoid drupe with smooth exocarp, thick fibrous coir mesocarp, hard stony endocarp, and sweet liquid/solid endosperm",
            "Tall majestic single-stemmed evergreen palm tree, 15–30 meters",
            "Warm humid tropical maritime coastal belt and river basins; frost-free",
            "Full intense sun", "High (40–50 liters/palm/day in summer); responds to coastal saltwater and brackish aquifers",
            "Deep coastal sandy soils, alluvial loams, and red laterites with good percolation, pH 5.2–8.0",
            "Perennial continuous fruiting (West Coast Tall, East Coast Tall, Chowghat Orange Dwarf, DXT hybrids)", ["Selected mature seed coconut germination"],
            ["Kalpavriksha (tree of heaven): tender coconut water (natural electrolyte), coconut oil, copra, grated coconut in food", "Coir fiber for ropes, geotextiles, mattresses, and coir pith compost", "Leaves for thatch, trunk for building timber"],
            "Safe for human nutrition.", False,
            [
                {"name": "Rhinoceros Beetle (Oryctes rhinoceros)", "type": "pest", "symptoms": "Geometric V-shaped geometric cuts on emerging fronds; chewing into cabbage crown", "management": "Hook out beetles from crown; pack top leaf axils with sevidol/sand mixture (1:1)"},
                {"name": "Root (Wilt) Disease", "type": "phytoplasma", "symptoms": "Flaccidity and abnormal inward ribbing of leaflets, marginal necrosis, yellowing", "management": "Balanced NPK + Magnesium Sulfate (500 g/palm); intercrop with green manure"}
            ],
            ["Apply 1 kg urea, 2 kg single superphosphate, and 2 kg muriate of potash per mature palm annually", "Practice basin mulching with coconut leaves and coir pith"]
        ),
        make_plant(
            "areca-catechu", "Areca catechu", "Arecanut / Betel Nut Palm / Supari", "सुपारी (Supari)",
            "పోకచెక్క (Pokachekka)", "பாக்கு (Paakku)",
            {"kannada": "ಅಡಿಕೆ (Adike)", "malayalam": "അടയ്ക്ക (Adaykka)", "bengali": "সুপারি (Shupari)", "marathi": "सुपारी (Supari)"},
            [], "Arecaceae", "Areca", "catechu", "plantation", "cultivated",
            ["Karnataka", "Kerala", "Assam", "Meghalaya", "West Bengal", "Tamil Nadu"],
            "Pinnately divided arching fronds (1.5–2 m) crowded at stem crown with lanceolate clustered pinnae", "Terminal crown", "Entire", "Parallel", "Dark glossy green",
            "Slender, perfectly straight erect annulated trunk (15–20 cm diameter) with distinct pale nodal rings, 12–25 m",
            "Spadix inflorescence branching under crownshaft; small fragrant white male flowers and fewer female flowers",
            "Fibrous ovoid to globose drupe (4–6 cm), bright orange-red when ripe, enclosing hard ruminate seed (nut)",
            "Slender tall single-stemmed evergreen feather palm, 12–25 meters",
            "Humid tropical rainforest zones and foothills (Western Ghats and Northeast India); sensitive to drought and sunscald",
            "Partial shade when young; filtered to full sun as canopy matures", "High regular moisture; sensitive to water deficit",
            "Deep fertile lateritic loams and clay loams rich in organic matter with excellent drainage, pH 5.5–6.5",
            "Perennial fruiting (Mangala, Sumangala, Mohitnagar, South Kanara)", ["Ripe seed nut nursery germination"],
            ["Betel nut chewed with paan (piper betle leaf and slaked lime)", "Tannins for dyeing and leather tanning", "Areca leaf sheaths pressed into eco-friendly biodegradable plates and bowls"],
            "Habitual chewing of areca nut with tobacco is clinically proven to cause oral submucous fibrosis and oral carcinomas.", False,
            [
                {"name": "Koleroga / Fruit Rot (Phytophthora meadii)", "type": "fungal", "symptoms": "Water-soaked lesions on nuts causing heavy premature rotting and dropping of green nuts during monsoon", "management": "Prophylactic spraying of 1% Bordeaux mixture before monsoon onset; cover bunches with polythene bags"}
            ],
            ["Tie polyethylene bags over developing nut bunches before heavy monsoon to prevent Koleroga", "Intercrop with Pepper, Banana, and Cocoa"]
        ),
        make_plant(
            "artocarpus-heterophyllus", "Artocarpus heterophyllus", "Jackfruit / Kathal", "कटहल (Kathal)",
            "పనస (Panasa)", "பலாப்பழம் (Palappazham)",
            {"kannada": "ಹಲಸಿನ ಹಣ್ಣು (Halasina Hannu)", "malayalam": "ചക്ക (Chakka)", "bengali": "কাঁঠাল (Kanthal)", "marathi": "फणस (Phanas)"},
            [], "Moraceae", "Artocarpus", "heterophyllus", "fruit plant", "native",
            ["Kerala", "Tamil Nadu", "Karnataka", "Assam", "West Bengal", "Tripura", "Odisha", "Maharashtra", "Goa"],
            "Simple, coriaceous (leathery), elliptic to obovate glossy dark green leaves", "Alternate, spiral", "Entire", "Pinnate", "Dark glossy green above, paler beneath",
            "Stout, straight trunk with rough dark grey-brown bark; exhibits cauliflory (flowers directly on trunk and older boughs), 10–20 m",
            "Monoecious: cylindrical fleshy spikes; male spikes on younger twigs, female spikes directly on main trunk and thick branches",
            "World's largest tree-borne fruit: giant syncarp (10–35 kg) with spiny pyramidal rind holding golden-yellow aromatic bulbs (arils)",
            "Large stately evergreen canopy tree, 10–20 meters",
            "Humid tropical Western Ghats and Northeast rainforests; warm and frost-free",
            "Full sunlight to light shade", "Moderate; deep taproot system withstands dry periods",
            "Deep, fertile, well-drained alluvial and lateritic sandy loams; strictly avoids waterlogged roots",
            "Summer fruiting (March–July)", ["Seeds (fresh), approach grafting, air layering"],
            ["Raw tender green jackfruit cooked as vegetarian 'plant meat' curry (kathal sabzi)", "Ripe golden bulbs eaten fresh, halwa, chips, ice cream", "Nutritious seeds boiled or roasted", "Valuable yellow timber for furniture and musical instruments"],
            "Latex sap is very sticky; grease hands and knives with coconut oil before cutting.", False,
            [
                {"name": "Rhizopus Fruit Rot (Rhizopus artocarpi)", "type": "fungal", "symptoms": "Soft watery black rot on male inflorescences and young fruitlets covered in greyish-black whisker mycelium", "management": "Foliar spray of Copper Oxychloride (2.5 g/L) or Mancozeb"}
            ],
            ["Prune dead wood and water sprouts to keep main trunk clean for cauliflorous fruit emergence"]
        ),
        make_plant(
            "punica-granatum", "Punica granatum", "Pomegranate / Anar", "अनार (Anar)",
            "దానిమ్మ (Danimma)", "மாதுளம்பழம் (Madhulampazham)",
            {"kannada": "ದಾಳಿಂಬೆ (Dalimbe)", "malayalam": "മാതളനാരങ്ങ (Mathalanaranga)", "bengali": "বেদানা / ডালিম (Bedana / Dalim)", "marathi": "डाळಿಂಬ (Dalimb)"},
            [], "Lythraceae", "Punica", "granatum", "fruit plant", "cultivated",
            ["Maharashtra (Solapur, Nashik)", "Gujarat", "Karnataka", "Andhra Pradesh", "Rajasthan", "Madhya Pradesh"],
            "Narrow, oblong-lanceolate smooth glossy leaves with short reddish petiole", "Opposite or clustered on spur twigs", "Entire", "Pinnate", "Lustrous bright green",
            "Multi-stemmed spiny spreading shrub or small tree with grey bark, 3–6 m",
            "Showy solitary or clustered bright scarlet-red tubular flowers with fleshy calyx",
            "Globose berry (balausta) with tough leathery red/yellow rind and persistent crown calyx, interior filled with ruby-red juicy arils",
            "Deciduous spiny spreading shrub or small tree, 3–6 meters",
            "Semi-arid sub-tropical to tropical climate with dry hot summers and cool winters",
            "Full bright sun (8+ hours daily)", "Moderate; highly drought hardy, but uniform drip irrigation prevents fruit cracking",
            "Well-drained light loamy soils to medium black soils, pH 6.5–8.0",
            "Mrig Bahar (monsoon flower, winter harvest) and Hastha Bahar (Bhagwa / Sindhuri / Ganesh)", ["Air layering, hardwood cuttings, or tissue culture"],
            ["Nutrient-dense superfruit rich in punicalagins, ellagic acid, and antioxidants", "Fresh arils, pure juice, anardana (dried sour seeds as spice)", "Rind used in Ayurvedic remedies for diarrhea"],
            "Safe for human nutrition.", False,
            [
                {"name": "Bacterial Blight / Telya (Xanthomonas axonopodis pv. punicae)", "type": "bacterial", "symptoms": "Water-soaked angular black spots on leaves, black cankers on twigs, Y-shaped or L-shaped black oily cracks on fruits", "management": "Strict sanitation; prune infected twigs; spray Streptocycline (0.5 g/L) + Copper Oxychloride (2.5 g/L)"},
                {"name": "Fruit Borer / Anar Butterfly (Deudorix isocrates)", "type": "pest", "symptoms": "Caterpillar bores inside developing fruit, causing rotting and fruit drop with foul frass", "management": "Bag young fruits with butter paper/cloth bags at marble stage; spray Chlorantraniliprole"}
            ],
            ["Bag young developing fruits (5 cm diameter) with butter paper bags to prevent 100% insect and sunscald damage", "Adopt drip irrigation to avoid wet foliage"]
        ),
        make_plant(
            "vitis-vinifera", "Vitis vinifera", "Grapes / Angoor", "अंगूर (Angoor)",
            "ద్రాక్ష (Draksha)", "திராட்சை (Thiratchai)",
            {"kannada": "ದ್ರಾಕ್ಷಿ (Drakshi)", "malayalam": "മുന്തിരി (Munthiri)", "bengali": "আঙুর (Angur)", "marathi": "द्राक्षे (Drakashe)"},
            [], "Vitaceae", "Vitis", "vinifera", "fruit plant", "cultivated",
            ["Maharashtra (Nashik, Sangli)", "Karnataka", "Tamil Nadu", "Andhra Pradesh", "Telangana", "Punjab", "Haryana"],
            "Large, cordate palmately 3–5 lobed leaves with coarsely serrate margins", "Alternate, distichous", "Coarsely serrate", "Palmate", "Rich green with distinct veins",
            "Woody climbing deciduous vine with leaf-opposed branched coiled tendrils, up to 15 m",
            "Dense panicles of tiny yellowish-green fragrant flowers",
            "Globose to ellipsoid fleshy juicy berries in tight pendulous bunches (green, purple, red, black)",
            "Vigorous woody perennial climbing liana, trained on overhead pandals, 3–15 m",
            "Warm dry Mediterranean to subtropical climate; dry rainless sunny weather during berry ripening is essential",
            "Full intense sun", "Controlled drip irrigation; withholding water before harvest enhances Brix sugars",
            "Deep, well-drained sandy loam or gravelly loam soils, pH 6.5–7.8",
            "Double pruning system: Foundation pruning (April) and Forward fruiting pruning (October)", ["Hardwood cuttings grafted on Dog Ridge rootstock (Thomson Seedless, Sonaka, Sharad Seedless)"],
            ["Fresh table fruit, sweet raisins (kishmish), premium wine production", "Grape seed oil and resveratrol antioxidant extract"],
            "Safe for human consumption. TOXIC to dogs (causes acute kidney failure).", False,
            [
                {"name": "Downy Mildew (Plasmopara viticola)", "type": "fungal", "symptoms": "Yellowish translucent 'oil spots' on upper leaf surface with dense white cottony fungal growth on underside", "management": "Spray Bordeaux mixture 1% or Metalaxyl + Mancozeb (2.5 g/L)"},
                {"name": "Powdery Mildew (Uncinula necator)", "type": "fungal", "symptoms": "Ash-grey powdery coating on leaves and young berries causing berry cracking", "management": "Foliar sulfur dust or Azoxystrobin (1 ml/L)"}
            ],
            ["Train on Bower / Pergola trellises for optimal airflow and sunlight interception", "Dip developing bunches in Gibberellic Acid (GA3 @ 10–40 ppm) for berry elongation"]
        ),
        make_plant(
            "citrus-limon", "Citrus limon", "Lemon / Nimbu / Baramasi Nimbu", "नींबू (Nimbu)",
            "నిమ్మకాయ (Nimmakaya)", "எலுமிச்சை (Elumichai)",
            {"kannada": "ನಿಂಬೆಹಣ್ಣು (Nimbehanu)", "malayalam": "ചെറുനാരങ്ങ (Cherunaranga)", "bengali": "লেবু (Lebu)", "marathi": "लिंबू (Limbu)"},
            [], "Rutaceae", "Citrus", "limon", "fruit plant", "cultivated",
            ["Andhra Pradesh", "Gujarat", "Maharashtra", "Tamil Nadu", "Karnataka", "Madhya Pradesh", "Rajasthan"],
            "Simple elliptic-ovate coriaceous leaves with narrowly winged petiole and citrus aroma", "Alternate", "Crenate to serrulate", "Pinnate", "Glossy dark green with translucent oil glands",
            "Spreading thorny shrub or small tree with sharp axillary spines, 3–6 m",
            "Fragrant solitary or clustered white flowers with purplish-tinted exterior petals",
            "Ovoid to ellipsoid hesperidium with distinct terminal nipple, yellow rind, and sour acidic juice",
            "Small evergreen thorny tree or spreading shrub, 3–6 meters",
            "Sub-tropical and tropical climate; frost sensitive",
            "Full sun (6–8 hours)", "Regular moderate watering; avoids soggy root zones",
            "Well-drained light loamy soils to medium black soils, pH 6.0–7.5",
            "Year-round flowering and fruiting with major flushes (Kagzi, Baramasi, Eureka)", ["T-budding, air layering, or seedling"],
            ["Universal culinary souring agent, fresh nimbu pani (lemonade), pickles", "Rich source of Vitamin C and citric acid; preservation and cleansing"],
            "Plant has sharp axillary thorns. Peel contains photosensitizing psoralen oils.", False,
            [
                {"name": "Citrus Canker (Xanthomonas citri)", "type": "bacterial", "symptoms": "Raised, corky, rough brownish pustules surrounded by yellow chlorotic halo on leaves, twigs, and fruits", "management": "Prune cankered twigs; spray Streptocycline (100 ppm) + Copper Oxychloride (2.5 g/L)"},
                {"name": "Citrus Leaf Miner (Phyllocnistis citrella)", "type": "pest", "symptoms": "Silvery serpentine zigzag mines on tender young leaves causing severe leaf curling", "management": "Spray Imidacloprid 17.8 SL (0.3 ml/L) or Neem oil (5 ml/L)"}
            ],
            ["Prune interior water shoots and cross branches annually", "Paint trunk base with Bordeaux paste to prevent gummosis"]
        ),
        make_plant(
            "citrus-aurantiifolia", "Citrus aurantiifolia", "Acid Lime / Kagzi Nimbu", "कागज़ी नींबू (Kagzi Nimbu)",
            "పుల్లనిమ్మ (Pullanimmma)", "எலுமிச்சம்பழம் (Elumichampazham)",
            {"kannada": "ಹುಳಿ ನಿಂಬೆ (Huli Nimbe)", "malayalam": "നാരങ്ങ (Naranga)", "bengali": "কাগজি লেবু (Kagzi Lebu)", "marathi": "कागदी लिंबू (Kagadi Limbu)"},
            [], "Rutaceae", "Citrus", "aurantiifolia", "fruit plant", "cultivated",
            ["Andhra Pradesh", "Gujarat", "Maharashtra", "Tamil Nadu", "Karnataka", "Telangana", "Bihar"],
            "Elliptic-oval leathery aromatic leaves with narrowly spathulate-winged petioles", "Alternate", "Crenulate", "Pinnate", "Bright shiny green",
            "Dense bushy spreading thorny shrub or small tree with short stiff sharp spines, 2–4 m",
            "Small pure white fragrant flowers in axillary clusters of 2–7",
            "Small globose to sub-globose thin-skinned hesperidium (3–5 cm), greenish-yellow with intensely sour juice",
            "Small dense thorny evergreen bushy tree, 2.5–5 meters",
            "Warm tropical and subtropical climate; heat tolerant but susceptible to frost",
            "Full sunlight (8 hours)", "Regular moderate moisture; sensitive to drought at fruit set",
            "Deep fertile well-drained sandy loam or light alluvial soils, pH 6.5–7.5",
            "Year-round fruiting (major peaks in summer and monsoon)", ["Seedling propagation (polyembryonic) or T-budding"],
            ["Premier Indian lime for pickles, seasoning, cooling drinks, dal souring", "High citric acid content"],
            "Thorns on branches. Safe for consumption.", False,
            [
                {"name": "Citrus Canker", "type": "bacterial", "symptoms": "Corky eruptive spots on foliage and lime fruits", "management": "Streptocycline + Copper Oxychloride"}
            ],
            ["Mulch basin with organic matter", "Maintain good drainage to prevent phytophthora gummosis"]
        ),
        make_plant(
            "citrus-sinensis", "Citrus sinensis", "Sweet Orange / Mosambi / Malta", "मौसंबी / माल्टा (Mosambi)",
            "బత్తాయి (Batthayi)", "சாத்துக்குடி (Saathukudi)",
            {"kannada": "ಮೋಸಂಬಿ (Mosambi)", "malayalam": "മൊസമ്പി (Mosambi)", "bengali": "মৌসম্বি (Moushambi)", "marathi": "मोसंबी (Mosambi)"},
            [], "Rutaceae", "Citrus", "sinensis", "fruit plant", "cultivated",
            ["Maharashtra (Jalna, Aurangabad)", "Andhra Pradesh", "Telangana", "Punjab", "Rajasthan", "Madhya Pradesh"],
            "Elliptic-oblong glossy coriaceous leaves with medium-winged petiole and distinct citrus fragrance", "Alternate", "Entire to crenulate", "Pinnate", "Dark glossy green",
            "Medium-sized compact evergreen tree with rounded canopy and slender thorns, 4–8 m",
            "Intensely fragrant solitary or clustered pure white waxy flowers",
            "Globose hesperidium with smooth green to golden-yellow rind, sweet mild juice with low acidity",
            "Compact evergreen rounded fruit tree, 4–8 meters",
            "Subtropical to tropical climate with dry winter and warm sunny summers",
            "Full sun (8 hours)", "Moderate regular drip irrigation",
            "Well-drained deep loamy and black soils with good aeration, pH 6.5–7.5",
            "Ambe Bahar (Feb–March flower, Nov–Dec harvest) and Mrig Bahar", ["T-budding on Rangpur Lime or Jatti Khatti rootstock"],
            ["India's most popular fresh juice fruit (sweet mosambi juice, rich in Vitamin C and potassium)", "Table fruit and therapeutic rehydration for convalescents"],
            "Safe for human nutrition.", False,
            [
                {"name": "Die-back / Gummosis (Phytophthora nicotianae)", "type": "fungal", "symptoms": "Gum exudation from trunk base, bark splitting, yellowing and dying back of twigs", "management": "Scrape gummed bark; apply Bordeaux paste; drench with Fosetyl-Al (2 g/L)"}
            ],
            ["Bud on Phytophthora-tolerant Rangpur Lime rootstock", "Keep graft union at least 25 cm above ground level"]
        ),
        make_plant(
            "manilkara-zapota", "Manilkara zapota", "Sapota / Chikoo", "चीकू (Chikoo)",
            "సపోటా (Sapota)", "சப்போட்டா (Sappotta)",
            {"kannada": "ಚಿಕ್ಕು (Chikku)", "malayalam": "ചിക്കു (Chikku)", "bengali": "সফেদা (Sofeda)", "marathi": "चिकू (Chiku)"},
            ["Achras zapota"], "Sapotaceae", "Manilkara", "zapota", "fruit plant", "naturalized",
            ["Gujarat (Navsari)", "Maharashtra (Dahanu)", "Karnataka", "Tamil Nadu", "Andhra Pradesh", "Kerala", "West Bengal"],
            "Simple, coriaceous (leathery), elliptic-lanceolate glossy dark green leaves crowded at twig ends", "Alternate, clustered at branch tips", "Entire", "Pinnate", "Dark lustrous green with prominent veins",
            "Stout, erect trunk with dark grey-brown rough fissured bark and horizontal branching, 8–15 m",
            "Small, bell-shaped solitary white or pale cream flowers on rusty-hairy pedicels in leaf axils",
            "Globose to ovoid fleshy berry with rough scurfy brown rind; sweet, brown, granular, honey-sweet pulp with shiny black seeds",
            "Medium to large evergreen rounded tree, 8–15 meters tall",
            "Warm humid tropical coastal climate; withstands coastal saline sea breezes and windstorms",
            "Full sunlight (8 hours)", "Moderate; highly drought hardy once mature",
            "Tolerates varied soils: coastal alluvium, sandy loams, deep black soils, and laterites, pH 6.0–8.0",
            "Continuous year-round fruiting with two peak harvest seasons (Kalipatti, Cricket Ball, PKM-1)", ["Approach grafting (inarching) or softwood grafting on Khirni (Manilkara hexandra) rootstock"],
            ["Popular sweet table fruit (chikoo shakes, ice creams, halwa)", "Natural source of sugars (fructose/sucrose) and dietary fiber", "Traditional source of chicle latex used in chewing gum"],
            "Seeds have an apical hook that can catch in the throat if swallowed whole. Discard seeds.", False,
            [
                {"name": "Leaf Spot (Phaeophleospora indica)", "type": "fungal", "symptoms": "Small circular brown spots with whitish centers on leaves causing defoliation", "management": "Spray Mancozeb (2 g/L) or Carbendazim (1 g/L)"},
                {"name": "Bud Borer (Anarsia achrasella)", "type": "pest", "symptoms": "Caterpillar webs together buds and tender leaves, boring into flower buds", "management": "Spray Quinalphos or Chlorpyrifos"}
            ],
            ["Graft on hardy Khirni (Manilkara hexandra) rootstock for lifelong vigor", "Harvest mature fruits when brown scurf rubs off easily and skin shows yellowish-green tinge underneath"]
        ),
        make_plant(
            "annona-squamosa", "Annona squamosa", "Custard Apple / Sugar Apple / Sitaphal", "सीताफल / शरीफा (Sitaphal)",
            "సీతాఫలం (Seethaphalam)", "சீத்தாப்பழம் (Seethappazham)",
            {"kannada": "ಸೀತಾಫಲ (Seethaphala)", "malayalam": "ആത്തച്ചക്ക (Aathachakka)", "bengali": "আতা (Aata)", "marathi": "सीताफळ (Sitaphal)"},
            [], "Annonaceae", "Annona", "squamosa", "fruit plant", "naturalized",
            ["Maharashtra", "Telangana", "Andhra Pradesh", "Karnataka", "Madhya Pradesh", "Gujarat", "Rajasthan", "Tamil Nadu"],
            "Simple, oblong-lanceolate smooth thin leaves with distinct aromatic odor when crushed", "Alternate, 2-ranked", "Entire", "Pinnate", "Dull blue-green above, paler glaucous beneath",
            "Slender, branched small deciduous tree or large shrub with thin grey bark, 3–6 m",
            "Solitary or clustered greenish-yellow drooping fleshy 3-petaled flowers with numerous stamens",
            "Globose to heart-shaped tuberculate syncarp with prominent rounded polygonal knobs/segments (carpels); creamy sweet white pulp with glossy black seeds",
            "Small deciduous tree or sprawling shrub, 3–6 meters",
            "Tropical and sub-tropical semi-arid climate; exceptionally drought hardy and heat tolerant",
            "Full intense sun", "Low water requirement; survives in rainfed rocky terrain",
            "Rocky, gravelly, shallow soils, light sandy loams, and red soils, pH 6.0–7.5",
            "Autumn harvest (September–November) (Balanagar, Arka Sahan, NMK-1 Golden)", ["Seeds, wedge grafting, or budding on seedling rootstocks"],
            ["Delicious sweet dessert fruit; sitaphal ice cream, basundi, shakes", "Seeds contain insecticidal acetogenins traditionally used against lice and crop pests"],
            "CRITICAL NOTE: Seeds are toxic and should not be crushed or chewed. Do not consume seeds.", False,
            [
                {"name": "Mealybug (Maconellicoccus hirsutus)", "type": "pest", "symptoms": "White waxy colonies clustered in grooves between fruit segments, producing sooty mold", "management": "Release Cryptolaemus montrouzieri ladybird predator; spray Buprofezin (1 ml/L) or Neem oil"}
            ],
            ["Hand pollination in morning hours increases fruit set by 60% and eliminates lopsided fruits"]
        ),
        make_plant(
            "phyllanthus-emblica", "Phyllanthus emblica", "Indian Gooseberry / Amla", "आंवला (Amla)",
            "ఉసిరికాయ (Usirikaya)", "நெல்லிக்காய் (Nellikai)",
            {"kannada": "ನೆಲ್ಲಿಕಾಯಿ (Nellikayi)", "malayalam": "നെല്ലിക്ക (Nellikka)", "bengali": "আমলকী (Amloki)", "marathi": "आवळा (Aawla)"},
            ["Emblica officinalis"], "Phyllanthaceae", "Phyllanthus", "emblica", "fruit plant", "native",
            ["Uttar Pradesh (Pratapgarh)", "Gujarat", "Rajasthan", "Madhya Pradesh", "Tamil Nadu", "Maharashtra", "Karnataka"],
            "Small, linear-oblong, closely spaced pinnately arranged leaves on deciduous branchlets resembling compound leaves", "Alternate, 2-ranked on branchlets", "Entire", "Inconspicuous", "Light fresh green",
            "Small to medium deciduous tree with flaking greenish-grey bark revealing pinkish underbark, 6–12 m",
            "Small, inconspicuous greenish-yellow flowers in compact axillary clusters on lower branchlets",
            "Depressed globose 6-lobed smooth fleshy berry (2–4 cm), pale yellow-green with 6-ribbed hard stone",
            "Small to medium deciduous tree, 6–12 meters",
            "Sub-tropical and tropical semi-arid zones; highly drought hardy and tolerant of light frost",
            "Full sun (8 hours)", "Low to moderate; withstands long dry spells",
            "Highly versatile: thrives in sodic/alkaline soils (pH up to 9.0), gravelly red soils, and alluvium",
            "Winter harvest (November–February) (NA-7, Chakaiya, Kanchan, Banarasi, Krishna)", ["Patch budding or shield budding on wild seedling rootstocks"],
            ["Premier Ayurvedic rasayana (rejuvenator); primary ingredient in Chyawanprash and Triphala", "Richest natural source of Vitamin C (600–900 mg/100g, stabilized by tannins)", "Amla murabba, candy, pickles, hair oil, digestive supari"],
            "Extremely safe and revered in traditional and modern nutrition.", False,
            [
                {"name": "Amla Rust (Ravenelia emblicae)", "type": "fungal", "symptoms": "Ring of brownish pustules on leaflets and circular black spots on fruits", "management": "Spray Wettable Sulfur (2 g/L) or Mancozeb"}
            ],
            ["Prune dead branches and thin crowded shoots annually after harvest", "Mulch tree basin with paddy straw to conserve moisture"]
        ),
        make_plant(
            "tamarindus-indica", "Tamarindus indica", "Tamarind / Imli", "इमली (Imli)",
            "చింతపండు (Chintapandu)", "புளி (Puli)",
            {"kannada": "ಹುಣಸೆಹಣ್ಣು (Hunasehannu)", "malayalam": "പുളി (Puli)", "bengali": "তেঁতুল (Tentul)", "marathi": "चिंच (Chinch)"},
            [], "Fabaceae", "Tamarindus", "indica", "fruit plant", "native",
            ["Tamil Nadu", "Andhra Pradesh", "Karnataka", "Maharashtra", "Telangana", "Madhya Pradesh", "Odisha", "Chhattisgarh"],
            "Evenly pinnate compound leaves with 10–18 pairs of small oblong obtuse leaflets that fold at night", "Alternate", "Entire", "Pinnate", "Fresh pale to medium green",
            "Massive, imposing trunk with rough dark grey fissured bark and dense spreading rounded dome canopy, 12–25 m",
            "Small pale yellow 5-petaled flowers with reddish-orange veins in drooping racemes",
            "Cinnamon-brown indehiscent curved pendulous pod with brittle shell, thick sour-sweet tart pulp, and glossy brown seeds",
            "Large, long-lived stately evergreen tree living over 200 years, 12–25 meters",
            "Semi-arid tropical and subtropical plains; exceptionally drought and wind resistant",
            "Full blazing sun", "Low; rainfed once established",
            "Deep, well-drained loams, gravelly red soils, and riverbanks; tolerates salinity and pH 5.5–8.5",
            "Winter flowering, late spring/summer harvest (March–May) (PKM-1, Urigam, Prathisthan)", ["Grafting, air layering, or seed"],
            ["Essential souring agent across South Indian cookery: sambar, rasam, puliyodharai, imli chutney", "High in natural tartaric acid, potassium, and pectin", "Valuable hard timber and shade avenue tree"],
            "Safe for culinary consumption.", False,
            [
                {"name": "Powdery Mildew", "type": "fungal", "symptoms": "White powdery fungal spots on tender leaves", "management": "Sulfur spray"}
            ],
            ["Plant along field boundaries and road avenues as living windbreaks"]
        ),
        make_plant(
            "syzygium-cumini", "Syzygium cumini", "Jamun / Black Plum / Java Plum", "जामुन (Jamun)",
            "నేరేడు (Neredu)", "நாவல்பழം (Navalpazham)",
            {"kannada": "ನೇರಳೆ ಹಣ್ಣು (Nerale Hannu)", "malayalam": "ഞാവൽ (Njaval)", "bengali": "জাম (Jaam)", "marathi": "जांभूळ (Jambhul)"},
            ["Eugenia jambolana"], "Myrtaceae", "Syzygium", "cumini", "fruit plant", "native",
            ["Uttar Pradesh", "Maharashtra", "Gujarat", "Tamil Nadu", "Andhra Pradesh", "Karnataka", "Bihar", "West Bengal"],
            "Opposite, coriaceous (leathery), oblong-elliptic glossy dark green leaves with faint turpentine aroma", "Opposite", "Entire", "Pinnate with numerous fine parallel lateral veins", "Lustrous dark green above, paler beneath",
            "Stout, majestic trunk with rough light grey-brown exfoliating bark and dense spreading canopy, 10–25 m",
            "Small, fragrant greenish-white flowers in branched cymes on older twigs",
            "Oblong-ellipsoid fleshy berry (2–4 cm), green ripening to lustrous deep purple-black with pink-purple staining astringent-sweet juice",
            "Large handsome evergreen canopy tree, 10–25 meters",
            "Tropical and sub-tropical plains, riverine tracts, and moist depressions; tolerates waterlogging",
            "Full sun", "Moderate; withstands seasonal flooding",
            "Deep fertile alluvial loams and moist soils near watercourses, pH 6.0–7.5",
            "Monsoon harvest (June–July) coinciding with onset of rains", ["Softwood grafting or seeds (CISH J-37, CISH J-42)"],
            ["Antioxidant-rich monsoon fruit (anthocyanins); fresh fruit with black salt", "Seed powder widely used in Ayurveda for managing type 2 diabetes mellitus", "Water-resistant timber traditionally used for well linings"],
            "Dark anthocyanin juice temporarily stains tongue and teeth deep purple. Safe.", False,
            [
                {"name": "Anthracnose", "type": "fungal", "symptoms": "Leaf spots and fruit rot", "management": "Copper oxychloride spray"}
            ],
            ["Pick fruits manually when fully purple-black; fallen fruits bruise easily"]
        ),
        make_plant(
            "citrullus-lanatus", "Citrullus lanatus", "Watermelon / Tarbooz", "तरबूज (Tarbooz)",
            "పుచ్చకాయ (Pucchakaya)", "தர்பூசணி (Tharpoosani)",
            {"kannada": "ಕಲ್ಲಂಗಡಿ (Kallangadi)", "malayalam": "തണ്ണിമത്തൻ (Thannimathan)", "bengali": "তরমুজ (Tormuj)", "marathi": "कलिंगड (Kalingad)"},
            [], "Cucurbitaceae", "Citrullus", "lanatus", "fruit plant", "cultivated",
            ["Uttar Pradesh", "Karnataka", "Andhra Pradesh", "Tamil Nadu", "Maharashtra", "Gujarat", "Rajasthan", "Madhya Pradesh"],
            "Large, deeply pinnatifid 3–5 lobed leaves with undulating round-tipped lobes and rough hairs", "Alternate", "Pinnatifid lobed", "Pinnate", "Greyish green with scabrid pubescence",
            "Trailing angular hairy grooved vine with 2–3 branched coiled tendrils, 2–4 m",
            "Solitary pale yellow 5-petaled flowers; female flowers have hairy inferior ovary",
            "Large globose to oblong smooth pepo (3–12 kg) with green striped rind, deep crimson-red sugary pulp (92% water) and flat black seeds",
            "Annual trailing herbaceous sprawling vine, 2–4 meters",
            "Warm, dry, sunny summer climate; requires hot days (28°C–35°C) and cool nights for high sugar accumulation",
            "Full blazing sun (8 hours)", "Regular uniform irrigation; stop watering 7–10 days before harvest to build sweetness",
            "Deep, well-drained sandy riverbeds and sandy loam soils, pH 6.0–7.0",
            "Summer (Zaid) season (January–April in riverbeds)", ["Direct seed pit sowing on mounds or riverbed Diara farming"],
            ["India's premier summer hydrating fruit; rich in lycopene, citrulline, and electrolytes", "Seeds roasted as nutritious protein-rich snack"],
            "Safe for human diet.", False,
            [
                {"name": "Fusarium Wilt (Fusarium oxysporum f. sp. niveum)", "type": "fungal", "symptoms": "Unilateral wilting of runner vines, vascular browning, sudden collapse", "management": "Crop rotation with non-cucurbits; seed treatment with Trichoderma (5 g/kg)"},
                {"name": "Downy Mildew", "type": "fungal", "symptoms": "Angular yellow patches on foliage", "management": "Metalaxyl spray"}
            ],
            ["Riverbed 'Diara' cultivation utilizes natural subsoil moisture in dry sandy river courses", "Tap fruit: dull hollow thumping sound indicates full ripeness"]
        ),
        make_plant(
            "cucumis-melo", "Cucumis melo", "Muskmelon / Kharbuja / Cantaloupe", "खरबूजा (Kharbuja)",
            "కర్బూజ (Karbhooja)", "முலாம் பழம் (Mulam Pazham)",
            {"kannada": "ಖರ್ಬೂಜ (Kharbuja)", "malayalam": "തൈര്മത്തൻ (Thayirmathan)", "bengali": "খরমুজ (Khormuj)", "marathi": "खरबूज (Kharbuj)"},
            [], "Cucurbitaceae", "Cucumis", "melo", "fruit plant", "cultivated",
            ["Uttar Pradesh", "Punjab", "Haryana", "Rajasthan", "Madhya Pradesh", "Andhra Pradesh", "Karnataka"],
            "Sub-orbicular to reniform shallowly 3–5 angled cordate leaves with soft rough hairs", "Alternate", "Denticulate", "Palmate", "Fresh green with rough hispid hairs",
            "Sprawling grooved hairy vine with simple unbranched tendrils, 1.5–3.0 m",
            "Small yellow bell-shaped flowers in leaf axils",
            "Globose to oval fragrant pepo with netted (reticulate) or smooth ribbed rind; sweet orange or green flesh with central cavity of seeds",
            "Annual sprawling trailing vine, 1.5–3.0 meters",
            "Hot, dry sunny summer climate; high humidity invites foliar diseases and reduces sugar content",
            "Full blazing sun (8 hours)", "Moderate; avoid wetting developing fruits directly",
            "Deep, well-drained sandy loams and river sand beds, pH 6.0–7.5",
            "Summer (Zaid) (February–May)", ["Direct pit sowing on mounds"],
            ["Aromatic sweet summer fruit; cooling, rich in beta-carotene and potassium", "Seeds dried and ground in traditional cooling thandai drink"],
            "Safe for human nutrition.", False,
            [
                {"name": "Powdery Mildew", "type": "fungal", "symptoms": "White powdery fungal patches on foliage", "management": "Wettable sulfur or Azoxystrobin spray"}
            ],
            ["Harvest at 'half-slip' to 'full-slip' stage when fruit easily detaches from vine with slight thumb pressure"]
        ),
        make_plant(
            "ananas-comosus", "Ananas comosus", "Pineapple / Ananas", "अनानास (Ananas)",
            "అనాస (Anaasa)", "அன்னாசிப்பழம் (Annasippazham)",
            {"kannada": "ಅನಾನಸ್ (Ananas)", "malayalam": "കൈതച്ചക്ക (Kaithachakka)", "bengali": "আনারস (Anaros)", "marathi": "अननस (Ananas)"},
            [], "Bromeliaceae", "Ananas", "comosus", "fruit plant", "cultivated",
            ["Assam", "West Bengal", "Tripura", "Meghalaya", "Kerala", "Karnataka", "Goa", "Bihar"],
            "Rosette of 30–50 sword-shaped rigid waxy trough-like leaves with sharp marginal spines and pointed tip", "Spiral dense rosette", "Spiny serrate with sharp teeth", "Parallel", "Dark glossy green with reddish or silvery glaucous underside",
            "Short, stout fleshy unbranched stem terminating in central composite flower head, 0.8–1.2 m",
            "Compact dense cylindrical spike of 50–200 purplish-blue flowers topped by a crown of small leaves",
            "Large cylindrical multiple fruit (syncarp, 1–2.5 kg) formed by fusion of berrylets around fibrous central core; crowned by leafy top",
            "Terrestrial evergreen perennial bromeliad herb, 0.8–1.2 meters",
            "Warm, humid tropical climate with high rainfall; sensitive to frost and waterlogging",
            "Filtered to full sun", "Moderate; trough leaves channel dew and rain directly into stem core",
            "Well-drained light sandy loam and acidic lateritic soils, pH 4.5–5.5",
            "Year-round fruiting with chemical induction (Giant Kew, Queen, Mauritius)", ["Slips, suckers, or fruit crowns"],
            ["Sweet-tart tropical fruit eaten fresh, canned slices, juice", "Contains bromelain proteolytic enzyme used for tenderizing and anti-inflammatory therapy", "Piña fiber extracted from leaves for textiles"],
            "Contains bromelain enzyme which may cause mild tingling sensation on tongue.", False,
            [
                {"name": "Heart Rot (Phytophthora cinnamomi)", "type": "fungal", "symptoms": "Heart leaves turn yellow, pull out easily from stem base with foul rotting odor", "management": "Ensure elevated bed drainage; dip suckers in Metalaxyl (2 g/L) before planting"}
            ],
            ["Spray Ethephon (100 ppm) into heart of 35-leaf plants to trigger synchronized flowering across orchard"]
        ),
        make_plant(
            "ziziphus-mauritiana", "Ziziphus mauritiana", "Indian Jujube / Ber / Poor Man's Apple", "बेर (Ber)",
            "రేగు (Regu)", "இலந்தைப்பழம் (Ilandhai)",
            {"kannada": "ಬೋರೆ ಹಣ್ಣು (Borehannu)", "malayalam": "എലന്ത (Elantha)", "bengali": "কুল (Kul)", "marathi": "बोर (Bor)"},
            [], "Rhamnaceae", "Ziziphus", "mauritiana", "fruit plant", "native",
            ["Rajasthan", "Haryana", "Punjab", "Gujarat", "Maharashtra", "Madhya Pradesh", "Uttar Pradesh", "Andhra Pradesh"],
            "Small, ovate to elliptic glossy dark green leaves, densely covered with white/buff felted tomentum beneath", "Alternate, 2-ranked", "Finely serrate", "3 prominent basal longitudinal veins", "Glossy dark green above, whitish woolly beneath",
            "Spreading thorny shrub or small tree with zigzag branchlets and sharp paired stipular spines (one straight, one hooked), 4–10 m",
            "Small inconspicuous greenish-yellow fragrant flowers in axillary cymes",
            "Globose to oblong fleshy drupe (2–5 cm) with smooth shiny skin, green turning golden-yellow to reddish-brown; sweet-sour pulp with hard stone",
            "Extremely hardy spiny evergreen or semi-deciduous tree, 4–10 meters",
            "Arid and semi-arid desert climate; extreme drought hardiness and heat tolerance (up to 48°C)",
            "Full blazing sun", "Very low; survives where other fruit trees fail",
            "Tolerates poor soils: sandy, gravelly, saline, and alkaline soils, pH 6.5–9.0",
            "Winter harvest (December–March) (Gola, Seb, Umran, Kaithli, Apple Ber)", ["Ring budding or shield budding on wild Ziziphus rotundifolia rootstock"],
            ["Poor man's apple: eaten fresh, dried, candies, and pickles", "Valuable source of Vitamin C and minerals in desert ecosystems", "Host plant for lac insects (Kerria lacca) and silkworms; dry spiny branches for livestock fencing"],
            "Sharp paired hooked spines require careful manual picking. Safe.", False,
            [
                {"name": "Powdery Mildew (Oidium erysiphoides f. sp. ziziphi)", "type": "fungal", "symptoms": "White powdery fungal growth on developing fruits causing skin corking and fruit drop", "management": "Spray Wettable Sulfur (2 g/L) or Dinocap during marble stage"}
            ],
            ["Annual severe pruning in May–June is essential to stimulate vigorous new fruiting wood for winter crop"]
        )
    ]

def save_fruits():
    fruits = get_fruits()
    with open(DATA_DIR / "fruits.json", "w", encoding="utf-8") as f:
        json.dump(fruits, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(fruits)} fruit plant records in fruits.json")

if __name__ == "__main__":
    save_fruits()
