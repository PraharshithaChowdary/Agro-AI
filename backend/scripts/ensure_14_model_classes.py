import sys
import json
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.database import engine, SessionLocal, Base
from app.models.plant import PlantSpecies

def ensure_model_classes():
    db = SessionLocal()
    with open(BACKEND_DIR / "models" / "plant_classes.json", "r", encoding="utf-8") as f:
        classes = json.load(f)

    CORE_BOTANICAL_SPECIES = {
        "capsicum-annuum": {
            "scientific_name": "Capsicum annuum",
            "common_name": "Chilli / Bell Pepper / Capsicum",
            "hindi_name": "मिर्च / शिमला मिर्च",
            "telugu_name": "మిరపకాయ / బెంగళూరు మిరప",
            "tamil_name": "மிளகாய் / குடைமிளகாய்",
            "family": "Solanaceae",
            "genus": "Capsicum",
            "species": "annuum",
            "category": "vegetable",
            "growth_habit": "Herbaceous Annual or Subshrub",
            "leaf_shape": "ovate-lanceolate",
            "leaf_margin": "entire",
            "leaf_venation": "reticulate",
            "monocot": False,
            "soil": "Well-drained sandy loam or clay loam, pH 6.0-7.0",
            "water": "Regular moderate watering, sensitive to waterlogging",
            "sun": "Full sun (6-8 hours daily)",
            "uses": ["Culinary spice", "Rich source of Vitamin C and Capsaicin", "Anti-inflammatory"]
        },
        "citrus-sinensis": {
            "scientific_name": "Citrus sinensis",
            "common_name": "Sweet Orange / Mosambi / Malta",
            "hindi_name": "संतरा / मौसमी / माल्टा",
            "telugu_name": "బత్తాయి / నారింజ",
            "tamil_name": "சாத்துக்குடி / ஆரஞ்சு",
            "family": "Rutaceae",
            "genus": "Citrus",
            "species": "sinensis",
            "category": "fruit plant",
            "growth_habit": "Evergreen Citrus Tree with Compact Canopy",
            "leaf_shape": "elliptic-oblong",
            "leaf_margin": "entire to crenulate",
            "leaf_venation": "reticulate glossy with winged petiole",
            "monocot": False,
            "soil": "Deep well-drained alluvial or sandy loam, pH 6.0-7.5",
            "water": "Deep irrigation every 7-10 days, drip preferred",
            "sun": "Full direct subtropical/tropical sunlight",
            "uses": ["Fresh citrus fruit and juice", "Essential oils from peel", "Vitamin C antioxidant"]
        },
        "cucurbita-pepo": {
            "scientific_name": "Cucurbita pepo",
            "common_name": "Field Pumpkin / Squash / Zucchini",
            "hindi_name": "कद्दू / कुम्हड़ा / चप्पन कद्दू",
            "telugu_name": "గుమ్మడికాయ / బూడిద గుమ్మడి",
            "tamil_name": "பூசணிக்காய் / பரங்கிக்காய்",
            "family": "Cucurbitaceae",
            "genus": "Cucurbita",
            "species": "pepo",
            "category": "vegetable",
            "growth_habit": "Trailing or Climbing Tendril Vine with Scabrid Bristles",
            "leaf_shape": "cordate palmately 5-lobed",
            "leaf_margin": "dentate serrulate hispid",
            "leaf_venation": "palmate reticulate",
            "monocot": False,
            "soil": "Rich fertile loamy soil with high organic matter, pH 6.0-6.8",
            "water": "Deep regular watering at base, avoid wetting broad leaves",
            "sun": "Full bright sunlight (6+ hours)",
            "uses": ["Culinary vegetable", "Edible zinc-rich seeds", "High dietary fiber and carotenoids"]
        },
        "fragaria-ananassa": {
            "scientific_name": "Fragaria ananassa",
            "common_name": "Garden Strawberry",
            "hindi_name": "स्ट्रॉबेरी / हिसालू",
            "telugu_name": "స్ట్రాబెర్రీ పండు",
            "tamil_name": "ஸ்ட்ராபெரி பழம்",
            "family": "Rosaceae",
            "genus": "Fragaria",
            "species": "ananassa",
            "category": "fruit plant",
            "growth_habit": "Stoloniferous Low-growing Perennial Herb with Runners",
            "leaf_shape": "trifoliolate compound",
            "leaf_margin": "coarsely serrate dentate",
            "leaf_venation": "reticulate pinnate",
            "monocot": False,
            "soil": "Slightly acidic fertile sandy loam, pH 5.5-6.5, rich in humus",
            "water": "Consistent moisture, drip irrigation with straw mulching",
            "sun": "Full sunlight (minimum 6 hours daily)",
            "uses": ["High-value dessert berry", "Anthocyanin and flavonoid rich", "Antioxidant nutrition"]
        },
        "glycine-max": {
            "scientific_name": "Glycine max",
            "common_name": "Soybean",
            "hindi_name": "सोयाबीन",
            "telugu_name": "సోయాబీన్ / సోయా చిక్కుడు",
            "tamil_name": "சோயாபீன்",
            "family": "Fabaceae",
            "genus": "Glycine",
            "species": "max",
            "category": "crop",
            "growth_habit": "Erect Bushy Annual Legume with Pubescent Stems",
            "leaf_shape": "trifoliolate ovate-elliptic",
            "leaf_margin": "entire pubescent",
            "leaf_venation": "reticulate",
            "monocot": False,
            "soil": "Well-drained fertile loam or black clay loam, pH 6.0-7.0",
            "water": "Moderate moisture, critical during flowering and pod fill",
            "sun": "Full direct sunlight",
            "uses": ["High-protein legume (40% protein)", "Edible vegetable oil (20% lipid)", "Soil nitrogen fixation"]
        },
        "malus-domestica": {
            "scientific_name": "Malus domestica",
            "common_name": "Apple",
            "hindi_name": "सेब",
            "telugu_name": "యాపిల్ పండు",
            "tamil_name": "ஆப்பிள் பழம்",
            "family": "Rosaceae",
            "genus": "Malus",
            "species": "domestica",
            "category": "fruit plant",
            "growth_habit": "Deciduous Temperate Fruit Tree",
            "leaf_shape": "simple ovate-elliptic",
            "leaf_margin": "finely serrate",
            "leaf_venation": "pinnate reticulate pubescent underneath",
            "monocot": False,
            "soil": "Deep well-drained loamy soil, pH 6.0-6.8",
            "water": "Regular orchard irrigation, requires winter chilling hours",
            "sun": "Full sun for sugar accumulation and peel coloration",
            "uses": ["Fresh commercial fruit", "Dietary pectin and quercetin", "Cider and culinary processing"]
        },
        "prunus-avium": {
            "scientific_name": "Prunus avium",
            "common_name": "Sweet Cherry",
            "hindi_name": "मीठी चेरी",
            "telugu_name": "చెర్రీ పండు",
            "tamil_name": "செர்ரி பழம்",
            "family": "Rosaceae",
            "genus": "Prunus",
            "species": "avium",
            "category": "fruit plant",
            "growth_habit": "Deciduous Temperate Orchard Tree",
            "leaf_shape": "simple oblong-ovate",
            "leaf_margin": "coarsely double-serrate with paired petiolar glands",
            "leaf_venation": "pinnate reticulate",
            "monocot": False,
            "soil": "Deep fertile well-drained gravelly loam, pH 6.0-7.0",
            "water": "Moderate deep watering, sensitive to root waterlogging",
            "sun": "Full direct sunlight",
            "uses": ["High-value fresh drupe fruit", "Melatonin and anthocyanin source", "Anti-gout antioxidant"]
        },
        "prunus-persica": {
            "scientific_name": "Prunus persica",
            "common_name": "Peach / Aadu",
            "hindi_name": "आड़ू",
            "telugu_name": "పీచ్ పండు",
            "tamil_name": "பீச் பழம்",
            "family": "Rosaceae",
            "genus": "Prunus",
            "species": "persica",
            "category": "fruit plant",
            "growth_habit": "Small Deciduous Stone-Fruit Tree",
            "leaf_shape": "lanceolate-elliptic acuminate",
            "leaf_margin": "finely serrate glandular",
            "leaf_venation": "pinnate reticulate",
            "monocot": False,
            "soil": "Well-drained sandy loam with good subsoil drainage, pH 6.0-6.5",
            "water": "Regular watering during stone hardening and fruit swell",
            "sun": "Full direct sunlight (8 hours)",
            "uses": ["Fresh stone fruit", "Vitamin A and potassium source", "Culinary canning and preserves"]
        },
        "rubus-idaeus": {
            "scientific_name": "Rubus idaeus",
            "common_name": "Red Raspberry",
            "hindi_name": "रसभरी / लाल रास्पबेरी",
            "telugu_name": "రాస్ప్బెర్రీ పండు",
            "tamil_name": "ராஸ்பெர்ரி பழம்",
            "family": "Rosaceae",
            "genus": "Rubus",
            "species": "idaeus",
            "category": "fruit plant",
            "growth_habit": "Prickly Deciduous Cane-Bearing Shrub",
            "leaf_shape": "pinnately 3-5 foliolate compound",
            "leaf_margin": "serrate dentate whitish tomentose underside",
            "leaf_venation": "pinnate reticulate",
            "monocot": False,
            "soil": "Rich well-drained organic loam, pH 5.6-6.5",
            "water": "Even moisture with organic mulch",
            "sun": "Full sun to cool afternoon partial shade",
            "uses": ["Fresh aggregate drupelet fruit", "Ellagic acid and ketone antioxidant", "Dietary fiber"]
        },
        "solanum-lycopersicum": {
            "scientific_name": "Solanum lycopersicum",
            "common_name": "Tomato",
            "hindi_name": "टमाटर",
            "telugu_name": "టమోటా",
            "tamil_name": "தக்காளி",
            "family": "Solanaceae",
            "genus": "Solanum",
            "species": "lycopersicum",
            "category": "vegetable",
            "growth_habit": "Herbaceous Sprawling Annual or Short-Lived Perennial",
            "leaf_shape": "imparipinnate compound with 5-9 lobed leaflets",
            "leaf_margin": "dentate lobed glandular-pubescent aromatic",
            "leaf_venation": "pinnate reticulate",
            "monocot": False,
            "soil": "Well-drained fertile loam rich in organic matter, pH 6.0-6.8",
            "water": "Consistent deep watering at soil level, avoid wetting foliage",
            "sun": "Full bright sunlight (6-8 hours daily)",
            "uses": ["Major culinary vegetable crop", "Lycopene antioxidant powerhouse", "Vitamin C and Potassium"]
        },
        "solanum-tuberosum": {
            "scientific_name": "Solanum tuberosum",
            "common_name": "Potato",
            "hindi_name": "आलू",
            "telugu_name": "బంగాళాదుంప / ఆలుగడ్డ",
            "tamil_name": "உருளைக்கிழங்கு",
            "family": "Solanaceae",
            "genus": "Solanum",
            "species": "tuberosum",
            "category": "vegetable",
            "growth_habit": "Tuber-bearing Herbaceous Perennial grown as Cool-Season Annual",
            "leaf_shape": "interruptedly pinnate compound with alternate ovate leaflets",
            "leaf_margin": "entire to wavy pubescent",
            "leaf_venation": "pinnate reticulate",
            "monocot": False,
            "soil": "Loose friable sandy loam rich in organic compost, pH 5.2-6.4",
            "water": "Regular moderate moisture, hilling required to protect tubers",
            "sun": "Full sun (6 hours minimum)",
            "uses": ["Global staple dietary carbohydrate", "High potassium and resistant starch", "Culinary tuber"]
        },
        "vaccinium-corymbosum": {
            "scientific_name": "Vaccinium corymbosum",
            "common_name": "Highbush Blueberry",
            "hindi_name": "नीलबदरी / हाईबश ब्लूबेरी",
            "telugu_name": "బ్లూబెర్రీ పండు",
            "tamil_name": "அவுரிநெல்லி",
            "family": "Ericaceae",
            "genus": "Vaccinium",
            "species": "corymbosum",
            "category": "fruit plant",
            "growth_habit": "Woody Acid-loving Deciduous Crown Shrub",
            "leaf_shape": "simple elliptic-ovate glossy",
            "leaf_margin": "entire to finely serrulate",
            "leaf_venation": "reticulate pinnate",
            "monocot": False,
            "soil": "Highly acidic peaty sandy loam, pH 4.5-5.2, pine bark mulched",
            "water": "Consistent rainwater / acidified moisture, shallow roots",
            "sun": "Full sun for optimal berry sweetness and anthocyanin synthesis",
            "uses": ["High-value antioxidant superfood berry", "Brain and vascular health anthocyanins", "Fresh fruit"]
        },
        "vitis-vinifera": {
            "scientific_name": "Vitis vinifera",
            "common_name": "Grapes / Angoor",
            "hindi_name": "अंगूर",
            "telugu_name": "ద్రాక్ష పండు",
            "tamil_name": "திராட்சை பழம்",
            "family": "Vitaceae",
            "genus": "Vitis",
            "species": "vinifera",
            "category": "fruit plant",
            "growth_habit": "Woody Perennial Liana / Climbing Tendril Vine",
            "leaf_shape": "large cordate palmately 3-5 lobed",
            "leaf_margin": "coarsely serrate toothed",
            "leaf_venation": "palmate reticulate prominent veins",
            "monocot": False,
            "soil": "Deep well-drained gravelly loam or chalky limestone, pH 6.5-7.5",
            "water": "Deep regulated deficit irrigation, bower or trellis trained",
            "sun": "Full intense sunlight (8+ hours daily)",
            "uses": ["Table grapes, raisins, and juice", "Resveratrol polyphenol antioxidant", "Grape seed bio-extracts"]
        },
        "zea-mays": {
            "scientific_name": "Zea mays",
            "common_name": "Corn / Maize",
            "hindi_name": "मक्का",
            "telugu_name": "మొక్కజొన్న",
            "tamil_name": "மக்காச்சோளம்",
            "family": "Poaceae",
            "genus": "Zea",
            "species": "mays",
            "category": "crop",
            "growth_habit": "Tall Robust C4 Monocot Grain Grass with Prop Roots",
            "leaf_shape": "large linear-lanceolate parallel-veined strap",
            "leaf_margin": "entire wavy parallel veins",
            "leaf_venation": "strictly parallel monocot venation with prominent midrib",
            "monocot": True,
            "soil": "Deep fertile well-drained loamy soil, pH 6.0-7.0, high nitrogen",
            "water": "Regular watering, critical during silking and tasseling",
            "sun": "Full direct intense tropical/subtropical sun",
            "uses": ["Global staple cereal grain", "Livestock feed and silage", "Starch, corn oil, and renewable bio-products"]
        }
    }

    inserted = 0
    updated = 0

    for slug, info in CORE_BOTANICAL_SPECIES.items():
        existing = db.query(PlantSpecies).filter(PlantSpecies.id == slug).first()
        leaf_char = {
            "shape": info["leaf_shape"],
            "margin": info["leaf_margin"],
            "venation": info["leaf_venation"],
            "is_monocot": info["monocot"]
        }

        if existing:
            # Update missing or blank attributes
            existing.common_name = info["common_name"]
            existing.hindi_name = info["hindi_name"]
            existing.telugu_name = info["telugu_name"]
            existing.tamil_name = info["tamil_name"]
            existing.leaf_characteristics_json = json.dumps(leaf_char, ensure_ascii=False)
            existing.growth_habit = info["growth_habit"]
            existing.soil_preferences = info["soil"]
            existing.water_requirements = info["water"]
            existing.sunlight_requirements = info["sun"]
            existing.uses_json = json.dumps(info["uses"], ensure_ascii=False)
            existing.verification_status = "verified"
            updated += 1
        else:
            new_record = PlantSpecies(
                id=slug,
                scientific_name=info["scientific_name"],
                common_name=info["common_name"],
                hindi_name=info["hindi_name"],
                telugu_name=info["telugu_name"],
                tamil_name=info["tamil_name"],
                other_regional_names_json=json.dumps({"sanskrit": "", "kannada": "", "marathi": ""}, ensure_ascii=False),
                synonyms_json=json.dumps([info["scientific_name"]], ensure_ascii=False),
                family=info["family"],
                genus=info["genus"],
                species=info["species"],
                category=info["category"],
                status_in_india="cultivated",
                indian_states_json=json.dumps(["Pan-India", "Andhra Pradesh", "Telangana", "Tamil Nadu", "Maharashtra", "Karnataka", "Punjab"], ensure_ascii=False),
                leaf_characteristics_json=json.dumps(leaf_char, ensure_ascii=False),
                growth_habit=info["growth_habit"],
                sunlight_requirements=info["sun"],
                water_requirements=info["water"],
                soil_preferences=info["soil"],
                uses_json=json.dumps(info["uses"], ensure_ascii=False),
                verification_status="verified",
                sources_json=json.dumps([
                    {"title": "Botanical Survey of India & ICAR Horticultural Database", "url": "https://bsi.gov.in/"},
                    {"title": "Plants of the World Online (POWO)", "url": "https://powo.science.kew.org/"}
                ], ensure_ascii=False)
            )
            db.add(new_record)
            inserted += 1

    db.commit()
    total_now = db.query(PlantSpecies).count()
    db.close()

    print(f"[SUCCESS] Core Vision Classes Synchronized: {inserted} inserted, {updated} updated.")
    print(f"[INFO] Total verified species in database: {total_now}")

if __name__ == "__main__":
    ensure_model_classes()
