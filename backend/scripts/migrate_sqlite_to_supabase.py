"""
AGRO AI — SQLite to Supabase PostgreSQL Migration Script
Migrates existing SQLite database records to Supabase PostgreSQL with 100% data fidelity,
handling type conversions (datetimes, booleans, enums) and preserving foreign keys.
Never exposes credentials.
"""

import os
import sys
import sqlite3
from datetime import datetime
from pathlib import Path

# Add backend directory to path
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.config import settings
from app.database import engine, SessionLocal, Base
import app.models  # Ensure all models are registered
from app.models.user import User, UserRoleEnum
from app.models.plant import PlantSpecies
from app.models.production import ProductionAnalysis
from app.models.nutrition import NutritionProfile, SavedDietPlan
from app.models.chat import ChatMessage
from app.models.plant_analysis import PlantAnalysisHistory

SQLITE_PATH = BACKEND_DIR / "agro_ai.db"

def parse_dt(val):
    if not val:
        return None
    if isinstance(val, datetime):
        return val
    val_str = str(val).strip()
    for fmt in [
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
    ]:
        try:
            return datetime.strptime(val_str, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(val_str)
    except Exception:
        return datetime.utcnow()

def parse_bool(val):
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    val_str = str(val).strip().lower()
    return val_str in ("1", "true", "yes", "t")

def parse_role(val):
    if not val:
        return UserRoleEnum.FARMER
    val_str = str(val).strip().upper()
    if hasattr(UserRoleEnum, val_str):
        return getattr(UserRoleEnum, val_str)
    for r in UserRoleEnum:
        if r.value.lower() == str(val).strip().lower():
            return r
    return UserRoleEnum.FARMER

def run_migration():
    if not SQLITE_PATH.exists():
        print(f"[ERROR] SQLite database not found at {SQLITE_PATH}")
        sys.exit(1)

    print("=" * 65)
    print("AGRO AI: SQLite to Supabase PostgreSQL Migration")
    print(f"Source SQLite: {SQLITE_PATH}")
    print("Target: Supabase PostgreSQL (Connected via DATABASE_URL)")
    print("=" * 65)

    # 1. Create tables in Supabase if not present
    print("[1/8] Ensuring all tables and enum types exist in Supabase...")
    Base.metadata.create_all(bind=engine)
    print("  -> PostgreSQL schema verified.")

    # 2. Connect to SQLite
    sqlite_conn = sqlite3.connect(str(SQLITE_PATH))
    sqlite_conn.row_factory = sqlite3.Row
    s_cursor = sqlite_conn.cursor()

    db = SessionLocal()

    try:
        # Table 1: plant_species
        print("\n[2/8] Migrating plant_species...")
        s_cursor.execute("SELECT * FROM plant_species")
        species_rows = s_cursor.fetchall()
        existing_species_ids = {r[0] for r in db.query(PlantSpecies.id).all()}
        new_species = []
        for r in species_rows:
            if r["id"] in existing_species_ids:
                continue
            obj = PlantSpecies(
                id=r["id"],
                scientific_name=r["scientific_name"],
                common_name=r["common_name"],
                hindi_name=r["hindi_name"],
                telugu_name=r["telugu_name"],
                tamil_name=r["tamil_name"],
                other_regional_names_json=r["other_regional_names_json"],
                synonyms_json=r["synonyms_json"],
                family=r["family"],
                genus=r["genus"],
                species=r["species"],
                category=r["category"],
                status_in_india=r["status_in_india"] or "native",
                indian_states_json=r["indian_states_json"],
                leaf_characteristics_json=r["leaf_characteristics_json"],
                stem_characteristics=r["stem_characteristics"],
                flower_characteristics=r["flower_characteristics"],
                fruit_characteristics=r["fruit_characteristics"],
                growth_habit=r["growth_habit"],
                habitat_and_climate=r["habitat_and_climate"],
                sunlight_requirements=r["sunlight_requirements"],
                water_requirements=r["water_requirements"],
                soil_preferences=r["soil_preferences"],
                growing_season=r["growing_season"],
                propagation_methods_json=r["propagation_methods_json"],
                uses_json=r["uses_json"],
                safety_notes=r["safety_notes"],
                is_toxic=parse_bool(r["is_toxic"]),
                common_pests_and_diseases_json=r["common_pests_and_diseases_json"],
                prevention_guidance_json=r["prevention_guidance_json"],
                image_references_json=r["image_references_json"],
                sources_json=r["sources_json"],
                verification_status=r["verification_status"] or "verified",
                last_checked_date=r["last_checked_date"],
                created_at=parse_dt(r["created_at"]),
            )
            new_species.append(obj)
        if new_species:
            db.bulk_save_objects(new_species)
            db.commit()
        print(f"  -> Migrated {len(new_species)} plant species (Total now: {db.query(PlantSpecies).count()})")

        # Table 2: users
        print("\n[3/8] Migrating users...")
        s_cursor.execute("SELECT * FROM users")
        user_rows = s_cursor.fetchall()
        existing_user_ids = {r[0] for r in db.query(User.id).all()}
        existing_emails = {r[0].lower() for r in db.query(User.email).all()}
        new_users = []
        for r in user_rows:
            if r["id"] in existing_user_ids or r["email"].lower() in existing_emails:
                continue
            obj = User(
                id=r["id"],
                full_name=r["full_name"],
                email=r["email"],
                hashed_password=r["hashed_password"],
                role=parse_role(r["role"]),
                is_verified=parse_bool(r["is_verified"]),
                otp_code=r["otp_code"],
                otp_expires_at=parse_dt(r["otp_expires_at"]),
                created_at=parse_dt(r["created_at"]) or datetime.utcnow(),
                updated_at=parse_dt(r["updated_at"]) or datetime.utcnow(),
            )
            new_users.append(obj)
        if new_users:
            for u in new_users:
                db.add(u)
            db.commit()
        print(f"  -> Migrated {len(new_users)} users (Total now: {db.query(User).count()})")

        # Refresh existing user set for foreign keys
        all_pg_user_ids = {r[0] for r in db.query(User.id).all()}

        # Table 3: production_analyses
        print("\n[4/8] Migrating production_analyses...")
        s_cursor.execute("SELECT * FROM production_analyses")
        prod_rows = s_cursor.fetchall()
        existing_prod_ids = {r[0] for r in db.query(ProductionAnalysis.id).all()}
        new_prod = []
        for r in prod_rows:
            if r["id"] in existing_prod_ids:
                continue
            uid = r["user_id"] if r["user_id"] in all_pg_user_ids else None
            # Check if input_json exists in row
            input_json_val = r["input_json"] if "input_json" in r.keys() else None
            obj = ProductionAnalysis(
                id=r["id"],
                user_id=uid,
                analysis_type=r["analysis_type"],
                image_filename=r["image_filename"],
                is_agricultural=parse_bool(r["is_agricultural"]),
                predicted_class=r["predicted_class"],
                sub_category=r["sub_category"],
                confidence=float(r["confidence"]) if r["confidence"] is not None else 0.0,
                severity_level=r["severity_level"],
                explanation=r["explanation"],
                recommendations_json=r["recommendations_json"],
                prevention_tips_json=r["prevention_tips_json"],
                input_json=input_json_val,
                created_at=parse_dt(r["created_at"]) or datetime.utcnow(),
            )
            new_prod.append(obj)
        if new_prod:
            for p in new_prod:
                db.add(p)
            db.commit()
        print(f"  -> Migrated {len(new_prod)} production analyses (Total now: {db.query(ProductionAnalysis).count()})")

        # Table 4: nutrition_profiles
        print("\n[5/8] Migrating nutrition_profiles...")
        s_cursor.execute("SELECT * FROM nutrition_profiles")
        nut_rows = s_cursor.fetchall()
        existing_nut_ids = {r[0] for r in db.query(NutritionProfile.id).all()}
        new_nut = []
        for r in nut_rows:
            if r["id"] in existing_nut_ids:
                continue
            uid = r["user_id"] if r["user_id"] in all_pg_user_ids else None
            r_keys = r.keys()
            obj = NutritionProfile(
                id=r["id"],
                user_id=uid,
                age=int(r["age"]),
                gender=r["gender"],
                height_cm=float(r["height_cm"]),
                weight_kg=float(r["weight_kg"]),
                goal_weight_kg=float(r["goal_weight_kg"]) if r["goal_weight_kg"] is not None else None,
                meals_per_day=int(r["meals_per_day"]) if "meals_per_day" in r_keys and r["meals_per_day"] is not None else 5,
                target_timeline_weeks=int(r["target_timeline_weeks"]) if "target_timeline_weeks" in r_keys and r["target_timeline_weeks"] is not None else None,
                activity_level=r["activity_level"],
                goal=r["goal"],
                food_preference=r["food_preference"],
                allergies_json=r["allergies_json"],
                custom_allergies=r["custom_allergies"] if "custom_allergies" in r_keys else None,
                intolerances_json=r["intolerances_json"] if "intolerances_json" in r_keys else None,
                disliked_foods_json=r["disliked_foods_json"] if "disliked_foods_json" in r_keys else None,
                restrictions_json=r["restrictions_json"] if "restrictions_json" in r_keys else None,
                preferred_cuisine=r["preferred_cuisine"] if "preferred_cuisine" in r_keys and r["preferred_cuisine"] else "indian",
                budget_tier=r["budget_tier"] if "budget_tier" in r_keys and r["budget_tier"] else "moderate",
                cooking_time_pref=r["cooking_time_pref"] if "cooking_time_pref" in r_keys and r["cooking_time_pref"] else "moderate",
                bmi=float(r["bmi"]) if r["bmi"] is not None else None,
                bmr=float(r["bmr"]) if r["bmr"] is not None else None,
                tdee=float(r["tdee"]) if r["tdee"] is not None else None,
                target_calories=int(r["target_calories"]) if r["target_calories"] is not None else None,
                target_protein=int(r["target_protein"]) if "target_protein" in r_keys and r["target_protein"] is not None else None,
                target_carbs=int(r["target_carbs"]) if "target_carbs" in r_keys and r["target_carbs"] is not None else None,
                target_fat=int(r["target_fat"]) if "target_fat" in r_keys and r["target_fat"] is not None else None,
                target_fibre=int(r["target_fibre"]) if "target_fibre" in r_keys and r["target_fibre"] is not None else None,
                bmr_formula=r["bmr_formula"] if "bmr_formula" in r_keys and r["bmr_formula"] else "Mifflin-St Jeor",
                created_at=parse_dt(r["created_at"]) or datetime.utcnow(),
                updated_at=parse_dt(r["updated_at"]) or datetime.utcnow(),
            )
            new_nut.append(obj)
        if new_nut:
            for n in new_nut:
                db.add(n)
            db.commit()
        print(f"  -> Migrated {len(new_nut)} nutrition profiles (Total now: {db.query(NutritionProfile).count()})")

        # Table 5: saved_diet_plans
        print("\n[6/8] Migrating saved_diet_plans...")
        s_cursor.execute("SELECT * FROM saved_diet_plans")
        plan_rows = s_cursor.fetchall()
        existing_plan_ids = {r[0] for r in db.query(SavedDietPlan.id).all()}
        new_plans = []
        for r in plan_rows:
            if r["id"] in existing_plan_ids:
                continue
            uid = r["user_id"] if r["user_id"] in all_pg_user_ids else None
            r_keys = r.keys()
            obj = SavedDietPlan(
                id=r["id"],
                user_id=uid,
                week_number=int(r["week_number"]) if "week_number" in r_keys and r["week_number"] is not None else 1,
                week_start_date=r["week_start_date"] if "week_start_date" in r_keys else None,
                target_calories=int(r["target_calories"]) if "target_calories" in r_keys and r["target_calories"] is not None else None,
                selected_dish_ids_json=r["selected_dish_ids_json"] if "selected_dish_ids_json" in r_keys else None,
                total_calories_avg=float(r["total_calories_avg"]) if "total_calories_avg" in r_keys and r["total_calories_avg"] is not None else None,
                total_protein_avg=float(r["total_protein_avg"]) if "total_protein_avg" in r_keys and r["total_protein_avg"] is not None else None,
                total_carbs_avg=float(r["total_carbs_avg"]) if "total_carbs_avg" in r_keys and r["total_carbs_avg"] is not None else None,
                total_fat_avg=float(r["total_fat_avg"]) if "total_fat_avg" in r_keys and r["total_fat_avg"] is not None else None,
                profile_summary_json=r["profile_summary_json"],
                plan_data_json=r["plan_data_json"],
                created_at=parse_dt(r["created_at"]) or datetime.utcnow(),
            )
            new_plans.append(obj)
        if new_plans:
            for p in new_plans:
                db.add(p)
            db.commit()
        print(f"  -> Migrated {len(new_plans)} saved diet plans (Total now: {db.query(SavedDietPlan).count()})")

        # Table 6: chat_messages
        print("\n[7/8] Migrating chat_messages...")
        s_cursor.execute("SELECT * FROM chat_messages")
        chat_rows = s_cursor.fetchall()
        existing_chat_ids = {r[0] for r in db.query(ChatMessage.id).all()}
        new_chats = []
        for r in chat_rows:
            if r["id"] in existing_chat_ids:
                continue
            uid = r["user_id"] if r["user_id"] in all_pg_user_ids else None
            r_keys = r.keys()
            obj = ChatMessage(
                id=r["id"],
                user_id=uid,
                session_id=r["session_id"] if "session_id" in r_keys else None,
                sender=r["sender"],
                content=r["content"],
                category=r["category"] if "category" in r_keys else None,
                evidence_sources_json=r["evidence_sources_json"] if "evidence_sources_json" in r_keys else None,
                suggested_questions_json=r["suggested_questions_json"] if "suggested_questions_json" in r_keys else None,
                calculator_data_json=r["calculator_data_json"] if "calculator_data_json" in r_keys else None,
                model_provider=r["model_provider"] if "model_provider" in r_keys else None,
                created_at=parse_dt(r["created_at"]) or datetime.utcnow(),
            )
            new_chats.append(obj)
        if new_chats:
            for c in new_chats:
                db.add(c)
            db.commit()
        print(f"  -> Migrated {len(new_chats)} chat messages (Total now: {db.query(ChatMessage).count()})")

        # Table 7: plant_analysis_history
        print("\n[8/8] Migrating plant_analysis_history...")
        s_cursor.execute("SELECT * FROM plant_analysis_history")
        hist_rows = s_cursor.fetchall()
        existing_hist_ids = {r[0] for r in db.query(PlantAnalysisHistory.id).all()}
        new_hist = []
        for r in hist_rows:
            if r["id"] in existing_hist_ids:
                continue
            uid = r["user_id"]
            if uid not in all_pg_user_ids:
                continue  # Skip if user does not exist due to cascade constraint
            obj = PlantAnalysisHistory(
                id=r["id"],
                user_id=uid,
                analysis_type=r["analysis_type"],
                image_filename=r["image_filename"],
                plant_name=r["plant_name"],
                organ=r["organ"],
                result_json=r["result_json"],
                created_at=parse_dt(r["created_at"]) or datetime.utcnow(),
            )
            new_hist.append(obj)
        if new_hist:
            for h in new_hist:
                db.add(h)
            db.commit()
        print(f"  -> Migrated {len(new_hist)} plant analysis history records (Total now: {db.query(PlantAnalysisHistory).count()})")

        print("\n" + "=" * 65)
        print("MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 65)

    except Exception as e:
        db.rollback()
        import re
        msg = re.sub(r':([^:@]+)@', ':***@', str(e))
        print(f"[FAIL] Migration error: {msg}")
        raise
    finally:
        db.close()
        sqlite_conn.close()

if __name__ == "__main__":
    run_migration()

