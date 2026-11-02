"""
AGRO AI — Indian Plant Catalog Database Importer
Imports verified plant species records from JSON manifest into SQLite database.
Performs upserts against app.models.plant.PlantSpecies table.
"""

import os
import sys
import json
from pathlib import Path

# Add backend directory to sys.path so app modules can be imported
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.database import engine, SessionLocal, Base
from app.models.plant import PlantSpecies

MANIFEST_PATH = Path(__file__).resolve().parent / "manifests" / "unified_plant_manifest.json"

def import_plants(db=None):
    if not MANIFEST_PATH.exists():
        print(f"[ERROR] Unified manifest not found at {MANIFEST_PATH}. Run merge_plant_datasets.py first.")
        return 0

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Ensure tables are created
    Base.metadata.create_all(bind=engine)

    close_session = False
    if db is None:
        db = SessionLocal()
        close_session = True

    inserted_count = 0
    updated_count = 0

    try:
        for r in records:
            pid = r["id"]
            existing = db.query(PlantSpecies).filter(PlantSpecies.id == pid).first()

            other_names_str = json.dumps(r.get("other_regional_names", {}), ensure_ascii=False)
            synonyms_str = json.dumps(r.get("synonyms", []), ensure_ascii=False)
            states_str = json.dumps(r.get("indian_states", []), ensure_ascii=False)
            leaf_str = json.dumps(r.get("leaf_characteristics", {}), ensure_ascii=False)
            prop_str = json.dumps(r.get("propagation_methods", []), ensure_ascii=False)
            uses_str = json.dumps(r.get("uses", []), ensure_ascii=False)
            pests_str = json.dumps(r.get("common_pests_and_diseases", []), ensure_ascii=False)
            prev_str = json.dumps(r.get("prevention_guidance", []), ensure_ascii=False)
            img_str = json.dumps(r.get("image_references", []), ensure_ascii=False)
            sources_str = json.dumps(r.get("sources", []), ensure_ascii=False)

            if existing:
                existing.scientific_name = r["scientific_name"]
                existing.common_name = r["common_name"]
                existing.hindi_name = r.get("hindi_name")
                existing.telugu_name = r.get("telugu_name")
                existing.tamil_name = r.get("tamil_name")
                existing.other_regional_names_json = other_names_str
                existing.synonyms_json = synonyms_str
                existing.family = r["family"]
                existing.genus = r["genus"]
                existing.species = r["species"]
                existing.category = r["category"]
                existing.status_in_india = r.get("status_in_india", "native")
                existing.indian_states_json = states_str
                existing.leaf_characteristics_json = leaf_str
                existing.stem_characteristics = r.get("stem_characteristics")
                existing.flower_characteristics = r.get("flower_characteristics")
                existing.fruit_characteristics = r.get("fruit_characteristics")
                existing.growth_habit = r.get("growth_habit")
                existing.habitat_and_climate = r.get("habitat_and_climate")
                existing.sunlight_requirements = r.get("sunlight_requirements")
                existing.water_requirements = r.get("water_requirements")
                existing.soil_preferences = r.get("soil_preferences")
                existing.growing_season = r.get("growing_season")
                existing.propagation_methods_json = prop_str
                existing.uses_json = uses_str
                existing.safety_notes = r.get("safety_notes")
                existing.is_toxic = bool(r.get("is_toxic", False))
                existing.common_pests_and_diseases_json = pests_str
                existing.prevention_guidance_json = prev_str
                existing.image_references_json = img_str
                existing.sources_json = sources_str
                existing.verification_status = r.get("verification_status", "verified")
                existing.last_checked_date = r.get("last_checked_date")
                updated_count += 1
            else:
                new_plant = PlantSpecies(
                    id=pid,
                    scientific_name=r["scientific_name"],
                    common_name=r["common_name"],
                    hindi_name=r.get("hindi_name"),
                    telugu_name=r.get("telugu_name"),
                    tamil_name=r.get("tamil_name"),
                    other_regional_names_json=other_names_str,
                    synonyms_json=synonyms_str,
                    family=r["family"],
                    genus=r["genus"],
                    species=r["species"],
                    category=r["category"],
                    status_in_india=r.get("status_in_india", "native"),
                    indian_states_json=states_str,
                    leaf_characteristics_json=leaf_str,
                    stem_characteristics=r.get("stem_characteristics"),
                    flower_characteristics=r.get("flower_characteristics"),
                    fruit_characteristics=r.get("fruit_characteristics"),
                    growth_habit=r.get("growth_habit"),
                    habitat_and_climate=r.get("habitat_and_climate"),
                    sunlight_requirements=r.get("sunlight_requirements"),
                    water_requirements=r.get("water_requirements"),
                    soil_preferences=r.get("soil_preferences"),
                    growing_season=r.get("growing_season"),
                    propagation_methods_json=prop_str,
                    uses_json=uses_str,
                    safety_notes=r.get("safety_notes"),
                    is_toxic=bool(r.get("is_toxic", False)),
                    common_pests_and_diseases_json=pests_str,
                    prevention_guidance_json=prev_str,
                    image_references_json=img_str,
                    sources_json=sources_str,
                    verification_status=r.get("verification_status", "verified"),
                    last_checked_date=r.get("last_checked_date")
                )
                db.add(new_plant)
                inserted_count += 1

        db.commit()
        print(f"[SUCCESS] Database import complete: {inserted_count} inserted, {updated_count} updated.")
        total_in_db = db.query(PlantSpecies).count()
        print(f"[INFO] Total plant species records in database: {total_in_db}")
        return total_in_db
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Database import failed: {e}")
        raise e
    finally:
        if close_session:
            db.close()

if __name__ == "__main__":
    import_plants()
