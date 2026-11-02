from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey, inspect, text
from app.database import Base, engine

class NutritionProfile(Base):
    __tablename__ = "nutrition_profiles"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    goal_weight_kg = Column(Float, nullable=True)
    meals_per_day = Column(Integer, default=5, nullable=False)
    target_timeline_weeks = Column(Integer, nullable=True)
    activity_level = Column(String(30), nullable=False)
    goal = Column(String(30), nullable=False)
    food_preference = Column(String(30), nullable=False)
    allergies_json = Column(Text, nullable=True)
    custom_allergies = Column(Text, nullable=True)
    intolerances_json = Column(Text, nullable=True)
    disliked_foods_json = Column(Text, nullable=True)
    restrictions_json = Column(Text, nullable=True)
    preferred_cuisine = Column(String(50), nullable=False, default="indian")
    budget_tier = Column(String(30), default="moderate", nullable=False)
    cooking_time_pref = Column(String(30), default="moderate", nullable=False)
    bmi = Column(Float, nullable=True)
    bmr = Column(Float, nullable=True)
    tdee = Column(Float, nullable=True)
    target_calories = Column(Integer, nullable=True)
    target_protein = Column(Integer, nullable=True)
    target_carbs = Column(Integer, nullable=True)
    target_fat = Column(Integer, nullable=True)
    target_fibre = Column(Integer, nullable=True)
    bmr_formula = Column(String(50), default="Mifflin-St Jeor", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SavedDietPlan(Base):
    __tablename__ = "saved_diet_plans"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    week_number = Column(Integer, default=1, nullable=False)
    week_start_date = Column(String(20), nullable=True)
    target_calories = Column(Integer, nullable=True)
    selected_dish_ids_json = Column(Text, nullable=True)
    total_calories_avg = Column(Float, nullable=True)
    total_protein_avg = Column(Float, nullable=True)
    total_carbs_avg = Column(Float, nullable=True)
    total_fat_avg = Column(Float, nullable=True)
    profile_summary_json = Column(Text, nullable=False)
    plan_data_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

def auto_migrate_nutrition_columns():
    """
    Safely inspects and adds missing columns to existing SQLite tables
    without dropping or modifying existing user records.
    """
    try:
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        with engine.connect() as conn:
            if "nutrition_profiles" in table_names:
                existing_cols = {col["name"] for col in inspector.get_columns("nutrition_profiles")}
                columns_to_add = [
                    ("goal_weight_kg", "FLOAT"),
                    ("meals_per_day", "INTEGER DEFAULT 5"),
                    ("target_timeline_weeks", "INTEGER"),
                    ("custom_allergies", "TEXT"),
                    ("intolerances_json", "TEXT"),
                    ("disliked_foods_json", "TEXT"),
                    ("budget_tier", "VARCHAR(30) DEFAULT 'moderate'"),
                    ("cooking_time_pref", "VARCHAR(30) DEFAULT 'moderate'"),
                    ("target_protein", "INTEGER"),
                    ("target_carbs", "INTEGER"),
                    ("target_fat", "INTEGER"),
                    ("target_fibre", "INTEGER"),
                    ("bmr_formula", "VARCHAR(50) DEFAULT 'Mifflin-St Jeor'")
                ]
                for col_name, col_type in columns_to_add:
                    if col_name not in existing_cols:
                        conn.execute(text(f"ALTER TABLE nutrition_profiles ADD COLUMN {col_name} {col_type};"))

            if "saved_diet_plans" in table_names:
                existing_plan_cols = {col["name"] for col in inspector.get_columns("saved_diet_plans")}
                plan_cols_to_add = [
                    ("week_number", "INTEGER DEFAULT 1"),
                    ("week_start_date", "VARCHAR(20)"),
                    ("target_calories", "INTEGER"),
                    ("selected_dish_ids_json", "TEXT"),
                    ("total_calories_avg", "FLOAT"),
                    ("total_protein_avg", "FLOAT"),
                    ("total_carbs_avg", "FLOAT"),
                    ("total_fat_avg", "FLOAT")
                ]
                for col_name, col_type in plan_cols_to_add:
                    if col_name not in existing_plan_cols:
                        conn.execute(text(f"ALTER TABLE saved_diet_plans ADD COLUMN {col_name} {col_type};"))

            conn.commit()
    except Exception as e:
        # Avoid crashing if already migrated or non-SQLite
        pass

# Run auto-migration on import
auto_migrate_nutrition_columns()
