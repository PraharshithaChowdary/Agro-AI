"""
AGRO AI — Target Training Species Database Verification
Ensures all target species from the training dataset pipeline (including Mint and Betel)
exist in the SQLite database with complete verified botanical records and vernaculars.
"""

import sys
import json
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.models.plant import PlantSpecies

TARGET_ADDITIONAL_SPECIES = {
    "mentha-arvensis": {
        "scientific_name": "Mentha arvensis",
        "common_name": "Field Mint / Corn Mint / Pudina",
        "hindi_name": "पुदीना / देशी पुदीना",
        "telugu_name": "పుదీనా (Pudina)",
        "tamil_name": "புதினா (Pudhina)",
        "family": "Lamiaceae",
        "genus": "Mentha",
        "species": "arvensis",
        "category": "medicinal",
        "growth_habit": "Aromatic Perennial Herb with Creeping Stolons",
        "leaf_shape": "ovate-elliptic with serrated margin",
        "leaf_margin": "serrated",
        "leaf_venation": "reticulate with gland dots",
        "monocot": False,
        "soil": "Rich, moist, humus-laden loamy soil, pH 6.0-7.0",
        "water": "Regular moist soil, does not tolerate drought",
        "sun": "Full sun to partial shade",
        "uses": ["Digestive herbal tonic", "Menthol extraction", "Culinary flavoring and chutneys"]
    },
    "piper-betle": {
        "scientific_name": "Piper betle",
        "common_name": "Betel Leaf / Paan / Betel Vine",
        "hindi_name": "पान / नागरबेल",
        "telugu_name": "తమలపాకు (Tamalapaku)",
        "tamil_name": "வெற்றிலை (Vettilai)",
        "family": "Piperaceae",
        "genus": "Piper",
        "species": "betle",
        "category": "medicinal",
        "growth_habit": "Dioecious Evergreen Perennial Climber Vine",
        "leaf_shape": "cordate (heart-shaped) with pointed apex",
        "leaf_margin": "entire",
        "leaf_venation": "palmate-reticulate with 5-7 basal veins",
        "monocot": False,
        "soil": "Well-drained friable clay loam or sandy loam with rich organic humus, pH 7.0-7.5",
        "water": "Frequent light watering to maintain high humidity",
        "sun": "Filtered shade under trellises or live standards",
        "uses": ["Mouth freshener and carminative", "Traditional Ayurvedic digestive stimulant", "Antimicrobial essential oil"]
    }
}

def seed_missing_target_species():
    db = SessionLocal()
    added = 0
    for plant_id, info in TARGET_ADDITIONAL_SPECIES.items():
        existing = db.query(PlantSpecies).filter(PlantSpecies.id == plant_id).first()
        if not existing:
            leaf_char = {
                "shape": info["leaf_shape"],
                "margin": info["leaf_margin"],
                "venation": info["leaf_venation"],
                "is_monocot": info["monocot"]
            }
            p = PlantSpecies(
                id=plant_id,
                scientific_name=info["scientific_name"],
                common_name=info["common_name"],
                hindi_name=info["hindi_name"],
                telugu_name=info["telugu_name"],
                tamil_name=info["tamil_name"],
                family=info["family"],
                genus=info["genus"],
                species=info["species"],
                category=info["category"],
                growth_habit=info["growth_habit"],
                soil_preferences=info["soil"],
                water_requirements=info["water"],
                sunlight_requirements=info["sun"],
                uses_json=json.dumps(info["uses"]),
                leaf_characteristics_json=json.dumps(leaf_char),
                verification_status="verified",
                status_in_india="Native / Widely Cultivated in India"
            )
            db.add(p)
            added += 1
            print(f"[+] Added target training species: {plant_id} ({info['common_name']})")
        else:
            print(f"[*] Already present: {plant_id}")
    
    db.commit()
    db.close()
    print(f"[DONE] Seeded {added} missing target training species.")

if __name__ == "__main__":
    seed_missing_target_species()
