import uuid
import json
import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.nutrition import NutritionProfile, SavedDietPlan
from app.models.user import User
from app.api.auth import get_current_user_optional

def get_current_user_required(user: Optional[User] = Depends(get_current_user_optional)) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to perform this action."
        )
    return user
from app.services.nutrition_calculator import NutritionCalculatorService
from app.services.diet_planner import DietPlannerService
from app.services.food_database import FOOD_DATABASE, IFCT_INGREDIENT_CATALOG
from app.schemas.nutrition import (
    NutritionProfileInputSchema,
    NutritionCalculationOut,
    WeeklyDietPlanResponseSchema,
    SavedWeeklyPlanSummarySchema,
    FoodItemSchema,
    UserProfileOutSchema,
    UserProfileUpdateSchema
)

router = APIRouter(prefix="/api/nutrition", tags=["Better Nutrition"])

@router.post("/calculate", response_model=NutritionCalculationOut)
def calculate_nutrition(payload: NutritionProfileInputSchema):
    try:
        results = NutritionCalculatorService.calculate_metrics(
            age=payload.age,
            gender=payload.gender,
            height_cm=payload.heightCm,
            weight_kg=payload.weightKg,
            activity_level=payload.activityLevel,
            goal=payload.goal,
            goal_weight_kg=payload.goalWeightKg,
            meals_per_day=payload.mealsPerDay,
            target_timeline_weeks=payload.targetTimelineWeeks,
            dietary_focus=payload.dietaryRestrictions,
            food_preference=payload.foodPreference
        )
        return results
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(val_err)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to calculate nutritional metrics: {str(e)}"
        )

@router.post("/weekly-plan", response_model=WeeklyDietPlanResponseSchema)
def generate_weekly_plan(
    payload: NutritionProfileInputSchema,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional)
):
    try:
        prev_week_dish_ids: List[str] = []
        next_week_num = payload.weekNumber or 1
        week_start_date = payload.weekStartDate or datetime.date.today().isoformat()

        if user:
            latest_saved = (
                db.query(SavedDietPlan)
                .filter(SavedDietPlan.user_id == user.id)
                .order_by(SavedDietPlan.week_number.desc(), SavedDietPlan.created_at.desc())
                .first()
            )
            if latest_saved:
                if payload.generateNewWeek:
                    next_week_num = (latest_saved.week_number or 1) + 1
                    try:
                        p_date = datetime.date.fromisoformat(latest_saved.week_start_date)
                        week_start_date = (p_date + datetime.timedelta(days=7)).isoformat()
                    except Exception:
                        week_start_date = datetime.date.today().isoformat()
                else:
                    next_week_num = latest_saved.week_number or 1

                if latest_saved.selected_dish_ids_json:
                    try:
                        prev_week_dish_ids = json.loads(latest_saved.selected_dish_ids_json)
                    except Exception:
                        pass
                if not prev_week_dish_ids and latest_saved.plan_data_json:
                    try:
                        p_dict = json.loads(latest_saved.plan_data_json)
                        prev_week_dish_ids = p_dict.get("selectedDishIds", [])
                    except Exception:
                        pass
        elif payload.weekNumber:
            next_week_num = payload.weekNumber

        profile_dict = payload.model_dump()
        if user:
            profile_dict["user_id"] = user.id

        plan = DietPlannerService.generate_seven_day_plan(
            profile_dict,
            previous_week_dish_ids=prev_week_dish_ids,
            week_number=next_week_num,
            week_start_date=week_start_date
        )

        plan_id = str(uuid.uuid4())
        plan["id"] = plan_id
        plan["weekNumber"] = next_week_num
        plan["weekStartDate"] = week_start_date
        plan["savedToAccount"] = bool(user)
        plan["persistenceMessage"] = "Plan and profile inputs saved to your account." if user else "Preview only — sign in to save this plan and your profile inputs."

        # The account role can tailor practical context, but personal targets still come
        # from age/body measurements/activity/goal/preferences—not the permission role.
        if user:
            role_note = {
                "farmer": "For long or outdoor workdays, plan safe drinking water and portable meals around your schedule; calorie and hydration needs can vary with heat and exertion.",
                "buyer": "For market/travel days, plan portable balanced meals and safe food storage so busy hours do not replace regular meals.",
                "general": "Use this plan as an estimate; update your profile when body weight, activity, preferences, or goals change.",
            }.get(user.get_role_value())
            if role_note:
                if not isinstance(plan.get("nutritionalNotes"), list):
                    plan["nutritionalNotes"] = []
                if role_note not in plan["nutritionalNotes"]:
                    plan["nutritionalNotes"].append(role_note)

        # Persist to database if authenticated
        if user:
            days = plan.get("days", [])
            total_cals_avg = sum(d.get("dailyTotalCalories", 0) for d in days) / max(1, len(days))
            total_prot_avg = sum(d.get("dailyTotalProtein", 0) for d in days) / max(1, len(days))
            total_carbs_avg = sum(d.get("dailyTotalCarbs", 0) for d in days) / max(1, len(days))
            total_fat_avg = sum(d.get("dailyTotalFat", 0) for d in days) / max(1, len(days))

            saved_record = SavedDietPlan(
                id=plan_id,
                user_id=user.id,
                week_number=next_week_num,
                week_start_date=week_start_date,
                target_calories=plan["profileSummary"]["targetCalories"],
                selected_dish_ids_json=json.dumps(plan.get("selectedDishIds", [])),
                total_calories_avg=total_cals_avg,
                total_protein_avg=total_prot_avg,
                total_carbs_avg=total_carbs_avg,
                total_fat_avg=total_fat_avg,
                profile_summary_json=json.dumps(plan["profileSummary"]),
                plan_data_json=json.dumps(plan)
            )
            db.add(saved_record)

            # Sync user profile
            existing_prof = db.query(NutritionProfile).filter(NutritionProfile.user_id == user.id).first()
            if not existing_prof:
                existing_prof = NutritionProfile(
                    id=str(uuid.uuid4()),
                    user_id=user.id,
                    age=payload.age,
                    gender=payload.gender,
                    height_cm=payload.heightCm,
                    weight_kg=payload.weightKg,
                    goal_weight_kg=payload.goalWeightKg,
                    meals_per_day=payload.mealsPerDay,
                    target_timeline_weeks=payload.targetTimelineWeeks,
                    activity_level=payload.activityLevel,
                    goal=payload.goal,
                    food_preference=payload.foodPreference,
                    allergies_json=json.dumps(payload.allergies),
                    custom_allergies=payload.customAllergies,
                    intolerances_json=json.dumps(payload.intolerances),
                    disliked_foods_json=json.dumps(payload.dislikedFoods),
                    restrictions_json=json.dumps(payload.dietaryRestrictions),
                    preferred_cuisine=payload.preferredCuisine,
                    budget_tier=payload.budgetTier,
                    cooking_time_pref=payload.cookingTimePref,
                    bmi=plan["profileSummary"]["bmi"],
                    bmr=plan["profileSummary"]["bmr"],
                    tdee=plan["profileSummary"]["tdee"],
                    target_calories=plan["profileSummary"]["targetCalories"],
                    target_protein=int(round(plan["profileSummary"]["targetProtein"])),
                    target_carbs=int(round(plan["profileSummary"]["targetCarbs"])),
                    target_fat=int(round(plan["profileSummary"]["targetFat"])),
                    target_fibre=int(round(plan["profileSummary"]["targetFibre"]))
                )
                db.add(existing_prof)
            else:
                existing_prof.age = payload.age
                existing_prof.gender = payload.gender
                existing_prof.height_cm = payload.heightCm
                existing_prof.weight_kg = payload.weightKg
                existing_prof.goal_weight_kg = payload.goalWeightKg
                existing_prof.meals_per_day = payload.mealsPerDay
                existing_prof.target_timeline_weeks = payload.targetTimelineWeeks
                existing_prof.activity_level = payload.activityLevel
                existing_prof.goal = payload.goal
                existing_prof.food_preference = payload.foodPreference
                existing_prof.allergies_json = json.dumps(payload.allergies)
                existing_prof.custom_allergies = payload.customAllergies
                existing_prof.intolerances_json = json.dumps(payload.intolerances)
                existing_prof.disliked_foods_json = json.dumps(payload.dislikedFoods)
                existing_prof.restrictions_json = json.dumps(payload.dietaryRestrictions)
                existing_prof.preferred_cuisine = payload.preferredCuisine
                existing_prof.budget_tier = payload.budgetTier
                existing_prof.cooking_time_pref = payload.cookingTimePref
                existing_prof.bmi = plan["profileSummary"]["bmi"]
                existing_prof.bmr = plan["profileSummary"]["bmr"]
                existing_prof.tdee = plan["profileSummary"]["tdee"]
                existing_prof.target_calories = plan["profileSummary"]["targetCalories"]
                existing_prof.target_protein = int(round(plan["profileSummary"]["targetProtein"]))
                existing_prof.target_carbs = int(round(plan["profileSummary"]["targetCarbs"]))
                existing_prof.target_fat = int(round(plan["profileSummary"]["targetFat"]))
                existing_prof.target_fibre = int(round(plan["profileSummary"]["targetFibre"]))
            db.commit()

        return plan
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(val_err)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Plan generation failed. No successful save was recorded; please retry."
        ) from e

@router.get("/profile", response_model=Optional[UserProfileOutSchema])
def get_user_profile(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_required)
):
    """
    Retrieves the authenticated user's saved nutritional profile and biometric targets.
    """
    profile = db.query(NutritionProfile).filter(NutritionProfile.user_id == user.id).first()
    if not profile:
        return None

    return UserProfileOutSchema(
        id=profile.id,
        userId=profile.user_id,
        age=profile.age,
        gender=profile.gender,
        heightCm=profile.height_cm,
        weightKg=profile.weight_kg,
        goalWeightKg=profile.goal_weight_kg,
        mealsPerDay=profile.meals_per_day or 5,
        targetTimelineWeeks=profile.target_timeline_weeks,
        activityLevel=profile.activity_level,
        goal=profile.goal,
        foodPreference=profile.food_preference,
        allergies=json.loads(profile.allergies_json) if profile.allergies_json else [],
        customAllergies=profile.custom_allergies or "",
        intolerances=json.loads(profile.intolerances_json) if profile.intolerances_json else [],
        dislikedFoods=json.loads(profile.disliked_foods_json) if profile.disliked_foods_json else "",
        dietaryRestrictions=json.loads(profile.restrictions_json) if profile.restrictions_json else [],
        preferredCuisine=profile.preferred_cuisine or "indian",
        budgetTier=profile.budget_tier or "moderate",
        cookingTimePref=profile.cooking_time_pref or "moderate",
        bmi=profile.bmi,
        bmr=profile.bmr,
        tdee=profile.tdee,
        targetCalories=profile.target_calories,
        targetProtein=profile.target_protein,
        targetCarbs=profile.target_carbs,
        targetFat=profile.target_fat,
        targetFibre=profile.target_fibre,
        bmrFormula=profile.bmr_formula or "Mifflin-St Jeor"
    )

@router.put("/profile", response_model=UserProfileOutSchema)
def update_user_profile(
    updates: UserProfileUpdateSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_required)
):
    """
    Updates the authenticated user's nutritional profile and recalculates metabolic metrics.
    """
    profile = db.query(NutritionProfile).filter(NutritionProfile.user_id == user.id).first()
    if not profile:
        profile = NutritionProfile(
            id=str(uuid.uuid4()),
            user_id=user.id,
            age=updates.age or 28,
            gender=updates.gender or "male",
            height_cm=updates.heightCm or 172.0,
            weight_kg=updates.weightKg or 68.0,
            activity_level=updates.activityLevel or "moderate",
            goal=updates.goal or "weight_loss",
            food_preference=updates.foodPreference or "vegetarian",
            preferred_cuisine=updates.preferredCuisine or "indian"
        )
        db.add(profile)

    update_data = updates.model_dump(exclude_unset=True)
    if "age" in update_data:
        profile.age = update_data["age"]
    if "gender" in update_data:
        profile.gender = update_data["gender"]
    if "heightCm" in update_data:
        profile.height_cm = update_data["heightCm"]
    if "weightKg" in update_data:
        profile.weight_kg = update_data["weightKg"]
    if "goalWeightKg" in update_data:
        profile.goal_weight_kg = update_data["goalWeightKg"]
    if "mealsPerDay" in update_data:
        profile.meals_per_day = update_data["mealsPerDay"]
    if "targetTimelineWeeks" in update_data:
        profile.target_timeline_weeks = update_data["targetTimelineWeeks"]
    if "activityLevel" in update_data:
        profile.activity_level = update_data["activityLevel"]
    if "goal" in update_data:
        profile.goal = update_data["goal"]
    if "foodPreference" in update_data:
        profile.food_preference = update_data["foodPreference"]
    if "allergies" in update_data:
        profile.allergies_json = json.dumps(update_data["allergies"])
    if "customAllergies" in update_data:
        profile.custom_allergies = update_data["customAllergies"]
    if "intolerances" in update_data:
        profile.intolerances_json = json.dumps(update_data["intolerances"])
    if "dislikedFoods" in update_data:
        profile.disliked_foods_json = json.dumps(update_data["dislikedFoods"])
    if "dietaryRestrictions" in update_data:
        profile.restrictions_json = json.dumps(update_data["dietaryRestrictions"])
    if "preferredCuisine" in update_data:
        profile.preferred_cuisine = update_data["preferredCuisine"]
    if "budgetTier" in update_data:
        profile.budget_tier = update_data["budgetTier"]
    if "cookingTimePref" in update_data:
        profile.cooking_time_pref = update_data["cookingTimePref"]

    # Recalculate metrics
    new_metrics = NutritionCalculatorService.calculate_metrics(
        age=profile.age,
        gender=profile.gender,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        activity_level=profile.activity_level,
        goal=profile.goal,
        goal_weight_kg=profile.goal_weight_kg,
        meals_per_day=profile.meals_per_day,
        target_timeline_weeks=profile.target_timeline_weeks,
        food_preference=profile.food_preference
    )
    profile.bmi = new_metrics["bmi"]
    profile.bmr = new_metrics["bmr"]
    profile.tdee = new_metrics["tdee"]
    profile.target_calories = new_metrics["targetCalories"]
    profile.target_protein = new_metrics["targetProteinGrams"]
    profile.target_carbs = new_metrics["targetCarbsGrams"]
    profile.target_fat = new_metrics["targetFatGrams"]
    profile.target_fibre = new_metrics["targetFibreGrams"]
    db.commit()

    return UserProfileOutSchema(
        id=profile.id,
        userId=profile.user_id,
        age=profile.age,
        gender=profile.gender,
        heightCm=profile.height_cm,
        weightKg=profile.weight_kg,
        goalWeightKg=profile.goal_weight_kg,
        mealsPerDay=profile.meals_per_day,
        targetTimelineWeeks=profile.target_timeline_weeks,
        activityLevel=profile.activity_level,
        goal=profile.goal,
        foodPreference=profile.food_preference,
        allergies=json.loads(profile.allergies_json) if profile.allergies_json else [],
        customAllergies=profile.custom_allergies or "",
        intolerances=json.loads(profile.intolerances_json) if profile.intolerances_json else [],
        dislikedFoods=json.loads(profile.disliked_foods_json) if profile.disliked_foods_json else "",
        dietaryRestrictions=json.loads(profile.restrictions_json) if profile.restrictions_json else [],
        preferredCuisine=profile.preferred_cuisine,
        budgetTier=profile.budget_tier,
        cookingTimePref=profile.cooking_time_pref,
        bmi=profile.bmi,
        bmr=profile.bmr,
        tdee=profile.tdee,
        targetCalories=profile.target_calories,
        targetProtein=profile.target_protein,
        targetCarbs=profile.target_carbs,
        targetFat=profile.target_fat,
        targetFibre=profile.target_fibre,
        bmrFormula=profile.bmr_formula
    )

@router.get("/weekly-plan", response_model=Optional[WeeklyDietPlanResponseSchema])
def get_latest_plan(
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional)
):
    if not user:
        return None
    latest_saved = (
        db.query(SavedDietPlan)
        .filter(SavedDietPlan.user_id == user.id)
        .order_by(SavedDietPlan.week_number.desc(), SavedDietPlan.created_at.desc())
        .first()
    )
    if latest_saved and latest_saved.plan_data_json:
        try:
            plan = json.loads(latest_saved.plan_data_json)
            plan["id"] = latest_saved.id
            plan["weekNumber"] = latest_saved.week_number or 1
            plan["weekStartDate"] = latest_saved.week_start_date
            plan["savedToAccount"] = True
            plan["persistenceMessage"] = "Loaded from your saved account history."
            if "selectedDishIds" not in plan and latest_saved.selected_dish_ids_json:
                plan["selectedDishIds"] = json.loads(latest_saved.selected_dish_ids_json)
            return plan
        except Exception:
            return None
    return None

@router.get("/weekly-plans", response_model=List[SavedWeeklyPlanSummarySchema])
def get_user_weekly_plans(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_required)
):
    """
    Returns history of all saved weekly plans for the authenticated user.
    """
    plans = (
        db.query(SavedDietPlan)
        .filter(SavedDietPlan.user_id == user.id)
        .order_by(SavedDietPlan.week_number.desc(), SavedDietPlan.created_at.desc())
        .all()
    )
    results = []
    for p in plans:
        results.append(
            SavedWeeklyPlanSummarySchema(
                id=p.id,
                weekNumber=p.week_number or 1,
                weekStartDate=p.week_start_date,
                targetCalories=p.target_calories,
                totalCaloriesAvg=p.total_calories_avg,
                totalProteinAvg=p.total_protein_avg,
                createdAt=p.created_at.isoformat() if p.created_at else ""
            )
        )
    return results

@router.get("/weekly-plans/{plan_id}", response_model=WeeklyDietPlanResponseSchema)
def get_weekly_plan_by_id(
    plan_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_required)
):
    """
    Returns a specific saved weekly plan by its unique ID, strictly verifying user ownership.
    """
    plan_record = (
        db.query(SavedDietPlan)
        .filter(SavedDietPlan.id == plan_id, SavedDietPlan.user_id == user.id)
        .first()
    )
    if not plan_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diet plan not found or does not belong to the authenticated user."
        )
    try:
        plan_data = json.loads(plan_record.plan_data_json)
        plan_data["id"] = plan_record.id
        plan_data["weekNumber"] = plan_record.week_number or 1
        plan_data["weekStartDate"] = plan_record.week_start_date
        plan_data["savedToAccount"] = True
        plan_data["persistenceMessage"] = "Loaded from your saved account history."
        if "selectedDishIds" not in plan_data and plan_record.selected_dish_ids_json:
            plan_data["selectedDishIds"] = json.loads(plan_record.selected_dish_ids_json)
        return plan_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse stored plan: {str(e)}"
        )

@router.post("/save-plan")
def save_plan(
    plan_data: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_required)
):
    """Persist a plan only to its authenticated owner; never report local-only data as database-saved."""
    record_id = plan_data.get("id") or str(uuid.uuid4())
    existing = db.query(SavedDietPlan).filter(SavedDietPlan.id == record_id).first()
    if existing:
        if existing.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diet plan not found or does not belong to the authenticated user."
            )
        existing.plan_data_json = json.dumps(plan_data)
        existing.profile_summary_json = json.dumps(plan_data.get("profileSummary", {}))
        db.commit()
        return {"message": "Plan successfully updated in your account.", "id": record_id}

    days = plan_data.get("days", [])
    total_cals_avg = sum(d.get("dailyTotalCalories", 0) for d in days) / max(1, len(days)) if days else 0
    total_prot_avg = sum(d.get("dailyTotalProtein", 0) for d in days) / max(1, len(days)) if days else 0
    total_carbs_avg = sum(d.get("dailyTotalCarbs", 0) for d in days) / max(1, len(days)) if days else 0
    total_fat_avg = sum(d.get("dailyTotalFat", 0) for d in days) / max(1, len(days)) if days else 0

    saved = SavedDietPlan(
        id=record_id,
        user_id=user.id,
        week_number=plan_data.get("weekNumber", 1),
        week_start_date=plan_data.get("weekStartDate"),
        target_calories=plan_data.get("profileSummary", {}).get("targetCalories", 2000),
        selected_dish_ids_json=json.dumps(plan_data.get("selectedDishIds", [])),
        total_calories_avg=total_cals_avg,
        total_protein_avg=total_prot_avg,
        total_carbs_avg=total_carbs_avg,
        total_fat_avg=total_fat_avg,
        profile_summary_json=json.dumps(plan_data.get("profileSummary", {})),
        plan_data_json=json.dumps(plan_data)
    )
    db.add(saved)
    db.commit()
    return {"message": "Plan successfully saved to your cloud profile.", "id": record_id}

@router.get("/foods")
def search_food_database(
    query: Optional[str] = Query(None, description="Search term for dish or ingredient"),
    category: Optional[str] = Query(None, description="Meal category: breakfast, lunch, dinner, mid_morning, evening_snack"),
    cuisine: Optional[str] = Query(None, description="Cuisine preference filter")
):
    """
    Search verified recipe catalog and IFCT 2017 nutritional ingredient data.
    """
    results = []
    for dish in FOOD_DATABASE:
        if category and dish.get("category") != category:
            continue
        if cuisine and cuisine.lower() not in [c.lower() for c in dish.get("cuisines", [])]:
            continue
        if query:
            q_norm = query.lower()
            dish_name = dish.get("name", "").lower()
            ing_names = [ing["name"].lower() for ing in dish.get("ingredients", [])]
            if q_norm not in dish_name and not any(q_norm in iname for iname in ing_names):
                continue

        results.append({
            "id": dish.get("id"),
            "name": dish.get("name"),
            "category": dish.get("category"),
            "cuisines": dish.get("cuisines", []),
            "calories": dish.get("calories"),
            "protein": dish.get("protein"),
            "carbs": dish.get("carbs"),
            "fat": dish.get("fat"),
            "fibre": dish.get("fibre", 0.0),
            "dietaryTags": dish.get("dietary_tags", []),
            "allergens": dish.get("allergens", []),
            "ingredientCount": len(dish.get("ingredients", []))
        })

    return {
        "count": len(results),
        "totalCatalogSize": len(FOOD_DATABASE),
        "source": "ICMR-NIN Indian Food Composition Tables (IFCT 2017)",
        "results": results[:50]
    }
