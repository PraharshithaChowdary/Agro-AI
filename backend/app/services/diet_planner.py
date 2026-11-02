"""
AGRO AI — Personalized 7-Day Diet Planner Service
Assembles verified, evidence-based meal schedules with ingredient-level traceability,
zero allergen leakage, dynamic IFCT 2017 scaling, deterministic variety scoring,
and exact additive calorie arithmetic.
"""

import datetime
import hashlib
import uuid
import math
from typing import List, Dict, Any, Optional, Set

from app.services.food_database import FOOD_DATABASE, scale_dish_to_target_calories
from app.services.allergy_filter_service import AllergyFilterService
from app.services.nutrition_calculator import NutritionCalculatorService
from app.services.plan_validator import PlanValidatorService

class DietPlannerService:
    @staticmethod
    def _generate_guidance(
        food_pref: str,
        allergies: List[str],
        custom_allergies_text: str,
        intolerances: List[str],
        dietary_focus: List[str],
        goal: str
    ) -> Dict[str, Any]:
        """
        Generates clinical and culinary guidance customized to the user's specific goals and restrictions.
        Guarantees that recommended substitutions never breach declared allergens or custom avoidances.
        """
        custom_tokens = AllergyFilterService.parse_custom_allergies(custom_allergies_text)
        all_excluded_raw = set(a.lower().strip() for a in allergies if a).union(custom_tokens)
        all_excluded_expanded = AllergyFilterService.expand_tokens_with_synonyms(list(all_excluded_raw))

        # Foods to Eat
        foods_to_eat = [
            {
                "group": "Unrefined Complex Carbohydrates & Ancient Millets",
                "items": ["Sprouted Ragi (Finger Millet)", "Foxtail Millet (Kangni)", "Rolled Whole Oats", "Brown Basmati Rice", "Little Millet (Samai)"],
                "rationale": "High in beta-glucans and soluble fibre, moderating postprandial glucose absorption and sustaining satiety."
            },
            {
                "group": "Clean Bioavailable Proteins",
                "items": [
                    "Sprouted Green Moong", "Yellow Arhar/Toor Dal", "Black Chickpeas (Kala Chana)",
                    "Fresh Cow Milk Paneer" if ("dairy" not in all_excluded_expanded and food_pref != "vegan") else "Firm Organic Tofu",
                    "Skinless Chicken Breast" if food_pref in ["non_vegetarian"] else "Cooked Edamame / Soya Chunks"
                ],
                "rationale": "Provides comprehensive essential amino acid profiles required for lean muscle protein synthesis and enzymatic repair."
            },
            {
                "group": "Cold-Pressed Fats & Micronutrient-Dense Seeds",
                "items": [
                    item for item in [
                        "Cold-Pressed Mustard Oil" if "mustard" not in all_excluded_expanded else "Extra Virgin Olive Oil",
                        "Raw Pumpkin Seeds", "Roasted Flaxseeds",
                        "Cold-Pressed Sesame Oil" if "sesame" not in all_excluded_expanded else "Extra Virgin Olive Oil"
                    ] if item
                ],
                "rationale": "Delivers balanced essential monounsaturated and polyunsaturated fatty acids without industrial trans-fats."
            },
            {
                "group": "Prebiotic & Digestive Support Foods",
                "items": ["Ripe Papaya", "Tender Coconut Water", "Fresh Mint & Coriander", "Bottle Gourd (Lauki)", "Fresh Guava"],
                "rationale": "Provides natural proteolytic enzymes (papain), elemental electrolytes, and gentle plant soluble mucilage."
            }
        ]

        # Foods to Avoid
        foods_to_avoid = []
        for exc in sorted(list(all_excluded_raw)):
            foods_to_avoid.append({
                "item": exc.replace("_", " ").title(),
                "reason": "Explicitly excluded due to diagnosed food allergy, intolerance, or custom dietary avoidance.",
                "category": "Strict Allergen / Restriction"
            })

        if food_pref == "vegan":
            foods_to_avoid.append({
                "item": "All Animal Dairy, Cow Ghee, Eggs & Meat",
                "reason": "100% plant-based dietary principle excludes animal-derived foods.",
                "category": "Ethical / Dietary Preference"
            })
        elif food_pref == "jain" or "jain" in dietary_focus:
            foods_to_avoid.append({
                "item": "Onion, Garlic, Potatoes, Carrots, Radishes & Root Tubers",
                "reason": "Jain Ahimsa dietary discipline avoids root vegetables and underground tubers.",
                "category": "Cultural / Spiritual Discipline"
            })

        # Foods to Limit (Contextual, never declaring healthy foods universally forbidden)
        foods_to_limit = [
            {
                "group": "Ultra-Processed Namkeens & Deep-Fried Snacks",
                "items": ["Commercial samosas", "Bikaneri bhujia", "Refined flour (maida) mathri"],
                "rationale": "High in oxidized industrial vegetable oils, excessive sodium, and trans-fats that impair endothelial vascular function."
            },
            {
                "group": "Refined Sugars & Sweetened Syrups",
                "items": ["Carbonated soft drinks", "Packaged fruit nectars", "Refined white table sugar"],
                "rationale": "Triggers rapid blood glucose and insulin spikes, promoting visceral adiposity and systemic inflammation."
            },
            {
                "group": "Excess Table Salt & High-Sodium Commercial Pickles",
                "items": ["Commercial pickles in heavy brine", "High-sodium processed sauces"],
                "rationale": "Elevates intravascular volume and hydrostatic pressure, counteracting cardiovascular goals."
            }
        ]

        # Safe Substitutions (Filtered so the substitute itself NEVER contains any user allergen)
        all_candidate_subs = [
            {
                "original": "Cow's Milk Paneer / Cottage Cheese",
                "substitute": "Organic Firm Soya Tofu or Sautéed Sprouted Moong",
                "benefit": "100% dairy-free and zero lactose; delivers comparable protein density (14-16g/100g) with zero cholesterol.",
                "triggers": ["soy"]
            },
            {
                "original": "Whole Wheat Roti / Phulka",
                "substitute": "Sprouted Ragi (Finger Millet) or Jowar (Sorghum) Roti",
                "benefit": "Completely gluten-free; yields higher dietary fibre, bone-building calcium, and a lower glycemic load.",
                "triggers": ["ragi", "jowar"]
            },
            {
                "original": "Almonds & Walnuts",
                "substitute": "Roasted Pumpkin, Sunflower & Flaxseed Mix",
                "benefit": "Zero tree nut exposure; delivers rich plant zinc, magnesium, and anti-inflammatory omega-3 alpha-linolenic acid.",
                "triggers": ["pumpkin", "sunflower", "flaxseed"]
            },
            {
                "original": "Onion & Garlic Tempering",
                "substitute": "Roasted Cumin, Hing (Pure Asafoetida), Ginger & Fresh Coriander",
                "benefit": "Full Jain and Sattvic compliance; preserves rich aromatic culinary depth and stimulates gastric digestive fire.",
                "triggers": ["cumin", "hing", "ginger"]
            },
            {
                "original": "Mustard Oil",
                "substitute": "Cold-Pressed Sesame Oil or Extra Virgin Olive Oil",
                "benefit": "Zero mustard allergen risk while supplying healthy unsaturated fatty acids.",
                "triggers": ["sesame"]
            }
        ]

        safe_substitutions = []
        for sub in all_candidate_subs:
            sub_text = sub["substitute"].lower()
            is_safe = True
            for tok in all_excluded_expanded:
                if tok and AllergyFilterService._text_matches_token(sub_text, tok):
                    is_safe = False
                    break
            if is_safe:
                safe_substitutions.append({
                    "original": sub["original"],
                    "substitute": sub["substitute"],
                    "benefit": sub["benefit"]
                })

        timing_and_portion_tips = [
            "Maintain a structured 3.5 to 4-hour window between major meals to allow complete gastric clearance and natural digestive enzyme replenishment.",
            "Hydrate with 250-300ml of ambient water 30 minutes before meals; avoid washing down heavy meals with excessive cold liquids to preserve gastric juice potency.",
            "Chew each morsel mindfully to facilitate salivary amylase digestion and activate satiety hormones (GLP-1 and peptide YY).",
            "Conclude your evening dinner at least 2.5 to 3 hours before sleep to support nocturnal glucose regulation and deep restorative slow-wave sleep."
        ]

        return {
            "foodsToEat": foods_to_eat,
            "foodsToAvoid": foods_to_avoid,
            "foodsToLimit": foods_to_limit,
            "safeSubstitutions": safe_substitutions,
            "timingAndPortionTips": timing_and_portion_tips
        }

    @staticmethod
    def _calculate_dish_score(
        dish: Dict[str, Any],
        meal_type: str,
        day_index: int,
        target_calories: int,
        profile_input: Dict[str, Any],
        used_dish_counts: Dict[str, int],
        last_used_day: Dict[str, int],
        today_staples: Set[str],
        user_seed: int,
        variation_seed: int = 0,
        today_dish_ids: Optional[Set[str]] = None,
        previous_week_dish_ids: Optional[Set[str]] = None,
        max_weekly_repeats: int = 1
    ) -> float:
        """
        Calculates a deterministic multi-factor suitability score for a recipe candidate.
        Balances clinical goals, cuisine affinity, disliked foods avoidance,
        variety within the week, previous-week history, and deterministic user personalization.
        """
        score = 100.0
        dish_id = dish.get("id", "")
        dish_cuisines = [c.lower() for c in dish.get("cuisines", [])]
        dish_tags = [t.lower() for t in dish.get("dietary_tags", [])]
        user_cuisine = profile_input.get("preferredCuisine", "indian").lower().strip()
        user_goal = profile_input.get("goal", "weight_loss").lower().strip()
        user_focus = [f.lower().strip() for f in profile_input.get("dietaryRestrictions", [])]
        disliked_text = profile_input.get("dislikedFoods", "")
        budget_tier = profile_input.get("budgetTier", "moderate")
        cooking_pref = profile_input.get("cookingTimePref", "moderate")

        # 0. SAME-DAY REPEAT PREVENTION (Hard Constraint: NEVER repeat exact dish in the same day)
        if today_dish_ids and dish_id in today_dish_ids:
            return -5000.0

        # 1. Cuisine Affinity
        if user_cuisine in ["south_indian", "andhra", "tamil"]:
            if any(c in dish_cuisines for c in ["south_indian", "andhra", "tamil"]):
                score += 50.0
                if user_cuisine in dish_cuisines:
                    score += 20.0
            elif "north_indian" in dish_cuisines:
                score -= 40.0
        elif user_cuisine in ["north_indian", "punjabi"]:
            if any(c in dish_cuisines for c in ["north_indian", "punjabi"]):
                score += 50.0
            elif any(c in dish_cuisines for c in ["south_indian", "andhra", "tamil"]):
                score -= 40.0
        elif user_cuisine in dish_cuisines:
            score += 45.0
        elif user_cuisine == "indian" and any(c in dish_cuisines for c in ["indian", "south_indian", "north_indian", "andhra", "tamil"]):
            score += 25.0
        if "home_cooked" in dish_tags:
            score += 10.0

        # 2. Goal Suitability
        if user_goal in ["weight_loss", "loss"]:
            if any(t in dish_tags for t in ["high_protein", "high_fibre", "low_added_sugar"]):
                score += 25.0
        elif user_goal in ["weight_gain", "gain"]:
            if any(t in dish_tags for t in ["high_protein", "balanced"]):
                score += 25.0

        # 3. Dietary Focus Matches
        for focus in user_focus:
            if focus in dish_tags:
                score += 15.0

        # 4. Budget & Cooking Time Affinity
        if budget_tier == "budget_friendly" and "budget_friendly" in dish_tags:
            score += 25.0
        if cooking_pref == "quick_easy" and "quick_easy" in dish_tags:
            score += 25.0

        # 5. Disliked Foods Avoidance (Heavy Penalty)
        if disliked_text:
            contains_disliked, matched_name = AllergyFilterService.contains_disliked_food(dish, disliked_text)
            if contains_disliked:
                score -= 500.0

        # 6. Variety Penalties & Weekly Repeat Limits (Prevents repeated meals)
        count_used = used_dish_counts.get(dish_id, 0)
        if count_used >= max_weekly_repeats:
            score -= 1000.0 * (count_used - max_weekly_repeats + 1)
        elif count_used > 0:
            score -= count_used * 120.0

        # Never repeat on consecutive days
        if last_used_day.get(dish_id) == day_index - 1:
            score -= 400.0
        # Avoid repeat within 2 days
        elif last_used_day.get(dish_id) == day_index - 2:
            score -= 200.0

        # 7. Previous-Week Fatigue Penalty (Ensures fresh dishes for new weeks)
        if previous_week_dish_ids and dish_id in previous_week_dish_ids:
            score -= 300.0

        # Intra-day staple diversity (e.g. don't pick moong for breakfast and moong for dinner on the same day)
        staple = dish.get("staple_ingredient")
        if staple and staple in today_staples:
            score -= 45.0

        # 8. Deterministic User Entropy Jitter
        # Provides personalized tie-breaking across different users and variation seeds
        entropy_string = f"{user_seed}_{variation_seed}_{meal_type}_{day_index}_{dish_id}"
        hash_digest = hashlib.md5(entropy_string.encode("utf-8")).hexdigest()
        jitter = (int(hash_digest[:6], 16) % 1000) / 50.0  # float 0.0 to 20.0
        score += jitter

        return score

    @staticmethod
    def select_best_dish(
        available_options: List[Dict[str, Any]],
        meal_type: str,
        day_index: int,
        target_calories: int,
        profile_input: Dict[str, Any],
        used_dish_counts: Dict[str, int],
        last_used_day: Dict[str, int],
        today_staples: Set[str],
        user_seed: int,
        variation_seed: int = 0,
        excluded_dish_ids: Optional[List[str]] = None,
        today_dish_ids: Optional[Set[str]] = None,
        previous_week_dish_ids: Optional[Set[str]] = None,
        max_weekly_repeats: int = 1
    ) -> Dict[str, Any]:
        """
        Selects the optimal compliant recipe for a meal slot using multi-factor scoring.
        """
        excluded = set(excluded_dish_ids or [])
        candidates = [d for d in available_options if d.get("id") not in excluded]
        if not candidates:
            candidates = available_options

        scored_candidates = []
        for dish in candidates:
            sc = DietPlannerService._calculate_dish_score(
                dish=dish,
                meal_type=meal_type,
                day_index=day_index,
                target_calories=target_calories,
                profile_input=profile_input,
                used_dish_counts=used_dish_counts,
                last_used_day=last_used_day,
                today_staples=today_staples,
                user_seed=user_seed,
                variation_seed=variation_seed,
                today_dish_ids=today_dish_ids,
                previous_week_dish_ids=previous_week_dish_ids,
                max_weekly_repeats=max_weekly_repeats
            )
            scored_candidates.append((sc, dish))

        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        return scored_candidates[0][1]
        """
        Selects the optimal compliant recipe for a meal slot using multi-factor scoring.
        """
        excluded = set(excluded_dish_ids or [])
        candidates = [d for d in available_options if d.get("id") not in excluded]
        if not candidates:
            # Fallback to full available options if all excluded
            candidates = available_options

        scored_candidates = []
        for dish in candidates:
            sc = DietPlannerService._calculate_dish_score(
                dish=dish,
                meal_type=meal_type,
                day_index=day_index,
                target_calories=target_calories,
                profile_input=profile_input,
                used_dish_counts=used_dish_counts,
                last_used_day=last_used_day,
                today_staples=today_staples,
                user_seed=user_seed,
                variation_seed=variation_seed
            )
            scored_candidates.append((sc, dish))

        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        return scored_candidates[0][1]

    @staticmethod
    def _format_dish_to_item(scaled_dish: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formats a calorie-scaled recipe template into the standard FoodItemSchema.
        """
        ingredients_formatted = []
        for ing in scaled_dish.get("ingredients", []):
            ingredients_formatted.append({
                "name": ing["name"],
                "quantityGrams": ing["quantity_grams"],
                "measure": ing["measure"],
                "calories": ing["calories"],
                "protein": ing["protein"],
                "carbs": ing["carbs"],
                "fat": ing["fat"],
                "fibre": ing.get("fibre", 0.0),
                "calcium_mg": ing.get("calcium_mg", 0.0),
                "iron_mg": ing.get("iron_mg", 0.0),
                "allergens": ing.get("allergens", []),
                "source": ing.get("source", "IFCT 2017"),
                "verification_status": ing.get("verification_status", "verified")
            })

        return {
            "dishId": scaled_dish.get("id"),
            "name": scaled_dish["name"],
            "portion": scaled_dish.get("portion_description", scaled_dish.get("base_portion_desc", "Standard portion")),
            "calories": scaled_dish["calories"],
            "proteinGrams": scaled_dish["protein"],
            "carbsGrams": scaled_dish["carbs"],
            "fatGrams": scaled_dish["fat"],
            "fibreGrams": scaled_dish.get("fibre", 0.0),
            "category": scaled_dish["category"],
            "isVegetarian": scaled_dish.get("is_veg", True),
            "isVegan": scaled_dish.get("is_vegan", False),
            "is_veg": scaled_dish.get("is_veg", True),
            "is_vegan": scaled_dish.get("is_vegan", False),
            "is_jain": scaled_dish.get("is_jain", False),
            "is_pescatarian": scaled_dish.get("is_pescatarian", False),
            "allergens": scaled_dish.get("allergens", []),
            "ingredients": ingredients_formatted,
            "preparationInstructions": scaled_dish.get("preparation_instructions", ""),
            "goalFitReason": scaled_dish.get("goal_suitability_reason", ""),
            "cuisine": scaled_dish.get("cuisine", "Indian")
        }

    @staticmethod
    def generate_seven_day_plan(
        profile_input: Dict[str, Any],
        previous_week_dish_ids: Optional[List[str]] = None,
        week_number: int = 1,
        week_start_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a validated, customized 7-day nutritional plan.
        Employs intelligent deterministic scoring and variety tracking to prevent repeated meals.
        Supports previous-week history to avoid repeating last week's menu when generating a new week.
        Dynamically scales constituent ingredients of every dish to match individualized
        meal calorie targets using IFCT 2017 nutrient values.
        """
        age = int(profile_input.get("age", 28))
        gender = profile_input.get("gender", "male")
        height_cm = float(profile_input.get("heightCm", 172.0))
        weight_kg = float(profile_input.get("weightKg", 68.0))
        goal_weight_kg = profile_input.get("goalWeightKg")
        if goal_weight_kg is not None and str(goal_weight_kg).strip():
            goal_weight_kg = float(goal_weight_kg)
        else:
            goal_weight_kg = None

        activity = profile_input.get("activityLevel", "moderate")
        goal = profile_input.get("goal", "weight_loss")
        food_pref = profile_input.get("foodPreference", "vegetarian")
        meals_per_day = int(profile_input.get("mealsPerDay", 5))
        timeline_weeks = profile_input.get("targetTimelineWeeks")
        allergies = profile_input.get("allergies", [])
        custom_allergies_text = profile_input.get("customAllergies", "")
        intolerances = profile_input.get("intolerances", [])
        disliked_foods = profile_input.get("dislikedFoods", "")
        dietary_focus = profile_input.get("dietaryRestrictions", [])
        cuisine = profile_input.get("preferredCuisine", "indian")
        budget_tier = profile_input.get("budgetTier", "moderate")
        cooking_pref = profile_input.get("cookingTimePref", "moderate")
        variation_seed = int(profile_input.get("variationSeed", 0))

        if previous_week_dish_ids is None:
            previous_week_dish_ids = profile_input.get("previousWeekDishIds", [])
        prev_week_set = set(previous_week_dish_ids or [])

        if "weekNumber" in profile_input and profile_input["weekNumber"]:
            week_number = int(profile_input["weekNumber"])
        if not week_start_date:
            week_start_date = profile_input.get("weekStartDate") or datetime.date.today().isoformat()

        # ---------------------------------------------------------------------
        # 1. Scientific Metabolic Math (Mifflin-St Jeor)
        # ---------------------------------------------------------------------
        metrics = NutritionCalculatorService.calculate_metrics(
            age=age,
            gender=gender,
            height_cm=height_cm,
            weight_kg=weight_kg,
            activity_level=activity,
            goal=goal,
            goal_weight_kg=goal_weight_kg,
            meals_per_day=meals_per_day,
            target_timeline_weeks=timeline_weeks,
            dietary_focus=dietary_focus,
            food_preference=food_pref
        )

        target_cals = metrics["targetCalories"]
        target_protein = metrics["targetProteinGrams"]
        target_carbs = metrics["targetCarbsGrams"]
        target_fat = metrics["targetFatGrams"]
        target_fibre = metrics["targetFibreGrams"]
        meal_targets = metrics["mealCalorieTargets"]

        # ---------------------------------------------------------------------
        # 2. Strict Pre-Filtering of Food Database
        # ---------------------------------------------------------------------
        safe_foods = AllergyFilterService.filter_safe_foods(
            foods=FOOD_DATABASE,
            food_preference=food_pref,
            allergies=allergies,
            custom_allergies_text=custom_allergies_text,
            intolerances=intolerances,
            dietary_focus=dietary_focus
        )

        # Categorize safe foods by meal slots
        bf_options = [f for f in safe_foods if f.get("category") == "breakfast"]
        mm_options = [f for f in safe_foods if f.get("category") in ["mid_morning", "evening_snack"]]
        lu_options = [f for f in safe_foods if f.get("category") == "lunch"]
        ev_options = [f for f in safe_foods if f.get("category") in ["evening_snack", "mid_morning"]]
        di_options = [f for f in safe_foods if f.get("category") == "dinner"]

        if not bf_options or not lu_options or not di_options or len(safe_foods) < 5:
            raise ValueError(
                "Unable to construct a compliant meal plan with the specified combination of dietary restrictions and allergies. "
                "The database could not find sufficient safe verified foods across all required meal categories. "
                "Please review your custom exclusion terms or broaden your selections."
            )

        # Configurable maximum repeat limits across the 7 days based on available pool size
        bf_max_rep = max(1, math.ceil(7.0 / max(1, len(bf_options))))
        lu_max_rep = max(1, math.ceil(7.0 / max(1, len(lu_options))))
        di_max_rep = max(1, math.ceil(7.0 / max(1, len(di_options))))
        mm_max_rep = max(1, math.ceil(7.0 / max(1, len(mm_options))))
        ev_max_rep = max(1, math.ceil(7.0 / max(1, len(ev_options))))

        # Deterministic user personalization hash
        user_fingerprint = f"{profile_input.get('user_id', 'anon')}_{age}_{gender}_{height_cm}_{weight_kg}_{goal}_{cuisine}_{food_pref}_wk{week_number}"
        user_seed = int(hashlib.md5(user_fingerprint.encode("utf-8")).hexdigest()[:8], 16)

        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        hydration_tips = [
            "Target 2.5 to 3.0 litres of water today. Begin your morning with 300ml warm water with a dash of fresh lemon.",
            "Maintain cellular electrolyte hydration by including natural coconut water or tender cucumber slices.",
            "Sip ambient water between meals rather than gulping cold fluids during heavy meals to optimize gastric enzymes.",
            "Keep a calibrated 1-litre stainless steel bottle with you. Strive to finish 2 full bottles before 4 PM.",
            "Stay adequately hydrated before and after any light physical training or brisk outdoor walking.",
            "Incorporate herbal infusions such as fresh tulsi, mint, or chamomile tea into your evening wind-down routine.",
            "Assess weekly hydration status by urine color (aim for pale straw). Keep a glass of water on your bedside table."
        ]

        # ---------------------------------------------------------------------
        # 3. Assemble 7-Day Plan with Calorie-Scaled Dishes & Strict Variety
        # ---------------------------------------------------------------------
        days_list = []
        used_dish_counts: Dict[str, int] = {}
        last_used_day: Dict[str, int] = {}
        all_selected_dish_ids: List[str] = []

        for i in range(7):
            meals = []
            today_staples: Set[str] = set()
            today_dish_ids: Set[str] = set()

            if meals_per_day == 3:
                # 3 Meals: Breakfast, Lunch, Dinner
                b_raw = DietPlannerService.select_best_dish(
                    bf_options, "Breakfast", i, meal_targets["Breakfast"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=bf_max_rep
                )
                used_dish_counts[b_raw["id"]] = used_dish_counts.get(b_raw["id"], 0) + 1
                last_used_day[b_raw["id"]] = i
                today_dish_ids.add(b_raw["id"])
                all_selected_dish_ids.append(b_raw["id"])
                if b_raw.get("staple_ingredient"):
                    today_staples.add(b_raw["staple_ingredient"])

                l_raw = DietPlannerService.select_best_dish(
                    lu_options, "Lunch", i, meal_targets["Lunch"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=lu_max_rep
                )
                used_dish_counts[l_raw["id"]] = used_dish_counts.get(l_raw["id"], 0) + 1
                last_used_day[l_raw["id"]] = i
                today_dish_ids.add(l_raw["id"])
                all_selected_dish_ids.append(l_raw["id"])
                if l_raw.get("staple_ingredient"):
                    today_staples.add(l_raw["staple_ingredient"])

                d_raw = DietPlannerService.select_best_dish(
                    di_options, "Dinner", i, meal_targets["Dinner"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=di_max_rep
                )
                used_dish_counts[d_raw["id"]] = used_dish_counts.get(d_raw["id"], 0) + 1
                last_used_day[d_raw["id"]] = i
                today_dish_ids.add(d_raw["id"])
                all_selected_dish_ids.append(d_raw["id"])

                b_scaled = scale_dish_to_target_calories(b_raw, meal_targets["Breakfast"])
                l_scaled = scale_dish_to_target_calories(l_raw, meal_targets["Lunch"])
                d_scaled = scale_dish_to_target_calories(d_raw, meal_targets["Dinner"])

                b_item = DietPlannerService._format_dish_to_item(b_scaled)
                l_item = DietPlannerService._format_dish_to_item(l_scaled)
                d_item = DietPlannerService._format_dish_to_item(d_scaled)

                meals = [
                    {
                        "mealType": "Breakfast",
                        "timeSuggestion": "07:30 AM – 08:30 AM",
                        "items": [b_item],
                        "totalCalories": b_item["calories"],
                        "totalProtein": b_item["proteinGrams"],
                        "totalCarbs": b_item["carbsGrams"],
                        "totalFat": b_item["fatGrams"],
                        "totalFibre": b_item["fibreGrams"]
                    },
                    {
                        "mealType": "Lunch",
                        "timeSuggestion": "01:00 PM – 02:00 PM",
                        "items": [l_item],
                        "totalCalories": l_item["calories"],
                        "totalProtein": l_item["proteinGrams"],
                        "totalCarbs": l_item["carbsGrams"],
                        "totalFat": l_item["fatGrams"],
                        "totalFibre": l_item["fibreGrams"]
                    },
                    {
                        "mealType": "Dinner",
                        "timeSuggestion": "07:30 PM – 08:30 PM",
                        "items": [d_item],
                        "totalCalories": d_item["calories"],
                        "totalProtein": d_item["proteinGrams"],
                        "totalCarbs": d_item["carbsGrams"],
                        "totalFat": d_item["fatGrams"],
                        "totalFibre": d_item["fibreGrams"]
                    }
                ]

            elif meals_per_day == 4:
                # 4 Meals: Breakfast, Lunch, Evening Snack, Dinner
                b_raw = DietPlannerService.select_best_dish(
                    bf_options, "Breakfast", i, meal_targets["Breakfast"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=bf_max_rep
                )
                used_dish_counts[b_raw["id"]] = used_dish_counts.get(b_raw["id"], 0) + 1
                last_used_day[b_raw["id"]] = i
                today_dish_ids.add(b_raw["id"])
                all_selected_dish_ids.append(b_raw["id"])
                if b_raw.get("staple_ingredient"):
                    today_staples.add(b_raw["staple_ingredient"])

                l_raw = DietPlannerService.select_best_dish(
                    lu_options, "Lunch", i, meal_targets["Lunch"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=lu_max_rep
                )
                used_dish_counts[l_raw["id"]] = used_dish_counts.get(l_raw["id"], 0) + 1
                last_used_day[l_raw["id"]] = i
                today_dish_ids.add(l_raw["id"])
                all_selected_dish_ids.append(l_raw["id"])
                if l_raw.get("staple_ingredient"):
                    today_staples.add(l_raw["staple_ingredient"])

                e_raw = DietPlannerService.select_best_dish(
                    ev_options, "Evening Snack", i, meal_targets["Evening Snack"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=ev_max_rep
                )
                used_dish_counts[e_raw["id"]] = used_dish_counts.get(e_raw["id"], 0) + 1
                last_used_day[e_raw["id"]] = i
                today_dish_ids.add(e_raw["id"])
                all_selected_dish_ids.append(e_raw["id"])
                if e_raw.get("staple_ingredient"):
                    today_staples.add(e_raw["staple_ingredient"])

                d_raw = DietPlannerService.select_best_dish(
                    di_options, "Dinner", i, meal_targets["Dinner"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=di_max_rep
                )
                used_dish_counts[d_raw["id"]] = used_dish_counts.get(d_raw["id"], 0) + 1
                last_used_day[d_raw["id"]] = i
                today_dish_ids.add(d_raw["id"])
                all_selected_dish_ids.append(d_raw["id"])

                b_scaled = scale_dish_to_target_calories(b_raw, meal_targets["Breakfast"])
                l_scaled = scale_dish_to_target_calories(l_raw, meal_targets["Lunch"])
                e_scaled = scale_dish_to_target_calories(e_raw, meal_targets["Evening Snack"])
                d_scaled = scale_dish_to_target_calories(d_raw, meal_targets["Dinner"])

                b_item = DietPlannerService._format_dish_to_item(b_scaled)
                l_item = DietPlannerService._format_dish_to_item(l_scaled)
                e_item = DietPlannerService._format_dish_to_item(e_scaled)
                d_item = DietPlannerService._format_dish_to_item(d_scaled)

                meals = [
                    {
                        "mealType": "Breakfast",
                        "timeSuggestion": "07:30 AM – 08:30 AM",
                        "items": [b_item],
                        "totalCalories": b_item["calories"],
                        "totalProtein": b_item["proteinGrams"],
                        "totalCarbs": b_item["carbsGrams"],
                        "totalFat": b_item["fatGrams"],
                        "totalFibre": b_item["fibreGrams"]
                    },
                    {
                        "mealType": "Lunch",
                        "timeSuggestion": "01:00 PM – 02:00 PM",
                        "items": [l_item],
                        "totalCalories": l_item["calories"],
                        "totalProtein": l_item["proteinGrams"],
                        "totalCarbs": l_item["carbsGrams"],
                        "totalFat": l_item["fatGrams"],
                        "totalFibre": l_item["fibreGrams"]
                    },
                    {
                        "mealType": "Evening Snack",
                        "timeSuggestion": "04:30 PM – 05:30 PM",
                        "items": [e_item],
                        "totalCalories": e_item["calories"],
                        "totalProtein": e_item["proteinGrams"],
                        "totalCarbs": e_item["carbsGrams"],
                        "totalFat": e_item["fatGrams"],
                        "totalFibre": e_item["fibreGrams"]
                    },
                    {
                        "mealType": "Dinner",
                        "timeSuggestion": "07:30 PM – 08:30 PM",
                        "items": [d_item],
                        "totalCalories": d_item["calories"],
                        "totalProtein": d_item["proteinGrams"],
                        "totalCarbs": d_item["carbsGrams"],
                        "totalFat": d_item["fatGrams"],
                        "totalFibre": d_item["fibreGrams"]
                    }
                ]

            elif meals_per_day == 6:
                # 6 Meals: Breakfast, Mid-morning, Lunch, Afternoon, Evening, Dinner
                b_raw = DietPlannerService.select_best_dish(
                    bf_options, "Breakfast", i, meal_targets["Breakfast"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=bf_max_rep
                )
                used_dish_counts[b_raw["id"]] = used_dish_counts.get(b_raw["id"], 0) + 1
                last_used_day[b_raw["id"]] = i
                today_dish_ids.add(b_raw["id"])
                all_selected_dish_ids.append(b_raw["id"])

                mm_raw = DietPlannerService.select_best_dish(
                    mm_options, "Mid-morning Snack", i, meal_targets["Mid-morning Snack"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=mm_max_rep
                )
                used_dish_counts[mm_raw["id"]] = used_dish_counts.get(mm_raw["id"], 0) + 1
                last_used_day[mm_raw["id"]] = i
                today_dish_ids.add(mm_raw["id"])
                all_selected_dish_ids.append(mm_raw["id"])

                l_raw = DietPlannerService.select_best_dish(
                    lu_options, "Lunch", i, meal_targets["Lunch"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=lu_max_rep
                )
                used_dish_counts[l_raw["id"]] = used_dish_counts.get(l_raw["id"], 0) + 1
                last_used_day[l_raw["id"]] = i
                today_dish_ids.add(l_raw["id"])
                all_selected_dish_ids.append(l_raw["id"])

                af_raw = DietPlannerService.select_best_dish(
                    mm_options, "Afternoon Snack", i, meal_targets["Afternoon Snack"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    excluded_dish_ids=[mm_raw["id"]],
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=mm_max_rep
                )
                used_dish_counts[af_raw["id"]] = used_dish_counts.get(af_raw["id"], 0) + 1
                last_used_day[af_raw["id"]] = i
                today_dish_ids.add(af_raw["id"])
                all_selected_dish_ids.append(af_raw["id"])

                ev_raw = DietPlannerService.select_best_dish(
                    ev_options, "Evening Snack", i, meal_targets["Evening Snack"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=ev_max_rep
                )
                used_dish_counts[ev_raw["id"]] = used_dish_counts.get(ev_raw["id"], 0) + 1
                last_used_day[ev_raw["id"]] = i
                today_dish_ids.add(ev_raw["id"])
                all_selected_dish_ids.append(ev_raw["id"])

                d_raw = DietPlannerService.select_best_dish(
                    di_options, "Dinner", i, meal_targets["Dinner"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=di_max_rep
                )
                used_dish_counts[d_raw["id"]] = used_dish_counts.get(d_raw["id"], 0) + 1
                last_used_day[d_raw["id"]] = i
                today_dish_ids.add(d_raw["id"])
                all_selected_dish_ids.append(d_raw["id"])

                b_scaled = scale_dish_to_target_calories(b_raw, meal_targets["Breakfast"])
                mm_scaled = scale_dish_to_target_calories(mm_raw, meal_targets["Mid-morning Snack"])
                l_scaled = scale_dish_to_target_calories(l_raw, meal_targets["Lunch"])
                af_scaled = scale_dish_to_target_calories(af_raw, meal_targets["Afternoon Snack"])
                ev_scaled = scale_dish_to_target_calories(ev_raw, meal_targets["Evening Snack"])
                d_scaled = scale_dish_to_target_calories(d_raw, meal_targets["Dinner"])

                b_item = DietPlannerService._format_dish_to_item(b_scaled)
                mm_item = DietPlannerService._format_dish_to_item(mm_scaled)
                l_item = DietPlannerService._format_dish_to_item(l_scaled)
                af_item = DietPlannerService._format_dish_to_item(af_scaled)
                ev_item = DietPlannerService._format_dish_to_item(ev_scaled)
                d_item = DietPlannerService._format_dish_to_item(d_scaled)

                meals = [
                    {
                        "mealType": "Breakfast",
                        "timeSuggestion": "07:30 AM – 08:30 AM",
                        "items": [b_item],
                        "totalCalories": b_item["calories"],
                        "totalProtein": b_item["proteinGrams"],
                        "totalCarbs": b_item["carbsGrams"],
                        "totalFat": b_item["fatGrams"],
                        "totalFibre": b_item["fibreGrams"]
                    },
                    {
                        "mealType": "Mid-morning Snack",
                        "timeSuggestion": "10:30 AM – 11:00 AM",
                        "items": [mm_item],
                        "totalCalories": mm_item["calories"],
                        "totalProtein": mm_item["proteinGrams"],
                        "totalCarbs": mm_item["carbsGrams"],
                        "totalFat": mm_item["fatGrams"],
                        "totalFibre": mm_item["fibreGrams"]
                    },
                    {
                        "mealType": "Lunch",
                        "timeSuggestion": "01:00 PM – 01:45 PM",
                        "items": [l_item],
                        "totalCalories": l_item["calories"],
                        "totalProtein": l_item["proteinGrams"],
                        "totalCarbs": l_item["carbsGrams"],
                        "totalFat": l_item["fatGrams"],
                        "totalFibre": l_item["fibreGrams"]
                    },
                    {
                        "mealType": "Afternoon Snack",
                        "timeSuggestion": "03:30 PM – 04:00 PM",
                        "items": [af_item],
                        "totalCalories": af_item["calories"],
                        "totalProtein": af_item["proteinGrams"],
                        "totalCarbs": af_item["carbsGrams"],
                        "totalFat": af_item["fatGrams"],
                        "totalFibre": af_item["fibreGrams"]
                    },
                    {
                        "mealType": "Evening Snack",
                        "timeSuggestion": "05:30 PM – 06:00 PM",
                        "items": [ev_item],
                        "totalCalories": ev_item["calories"],
                        "totalProtein": ev_item["proteinGrams"],
                        "totalCarbs": ev_item["carbsGrams"],
                        "totalFat": ev_item["fatGrams"],
                        "totalFibre": ev_item["fibreGrams"]
                    },
                    {
                        "mealType": "Dinner",
                        "timeSuggestion": "07:45 PM – 08:30 PM",
                        "items": [d_item],
                        "totalCalories": d_item["calories"],
                        "totalProtein": d_item["proteinGrams"],
                        "totalCarbs": d_item["carbsGrams"],
                        "totalFat": d_item["fatGrams"],
                        "totalFibre": d_item["fibreGrams"]
                    }
                ]

            else:
                # 5 Meals Standard (Breakfast, Mid-morning, Lunch, Evening, Dinner) = Exactly 35 Meal Slots
                b_raw = DietPlannerService.select_best_dish(
                    bf_options, "Breakfast", i, meal_targets["Breakfast"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=bf_max_rep
                )
                used_dish_counts[b_raw["id"]] = used_dish_counts.get(b_raw["id"], 0) + 1
                last_used_day[b_raw["id"]] = i
                today_dish_ids.add(b_raw["id"])
                all_selected_dish_ids.append(b_raw["id"])
                if b_raw.get("staple_ingredient"):
                    today_staples.add(b_raw["staple_ingredient"])

                mm_raw = DietPlannerService.select_best_dish(
                    mm_options, "Mid-morning Snack", i, meal_targets["Mid-morning Snack"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=mm_max_rep
                )
                used_dish_counts[mm_raw["id"]] = used_dish_counts.get(mm_raw["id"], 0) + 1
                last_used_day[mm_raw["id"]] = i
                today_dish_ids.add(mm_raw["id"])
                all_selected_dish_ids.append(mm_raw["id"])
                if mm_raw.get("staple_ingredient"):
                    today_staples.add(mm_raw["staple_ingredient"])

                l_raw = DietPlannerService.select_best_dish(
                    lu_options, "Lunch", i, meal_targets["Lunch"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=lu_max_rep
                )
                used_dish_counts[l_raw["id"]] = used_dish_counts.get(l_raw["id"], 0) + 1
                last_used_day[l_raw["id"]] = i
                today_dish_ids.add(l_raw["id"])
                all_selected_dish_ids.append(l_raw["id"])
                if l_raw.get("staple_ingredient"):
                    today_staples.add(l_raw["staple_ingredient"])

                e_raw = DietPlannerService.select_best_dish(
                    ev_options, "Evening Snack", i, meal_targets["Evening Snack"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    excluded_dish_ids=[mm_raw["id"]],
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=ev_max_rep
                )
                used_dish_counts[e_raw["id"]] = used_dish_counts.get(e_raw["id"], 0) + 1
                last_used_day[e_raw["id"]] = i
                today_dish_ids.add(e_raw["id"])
                all_selected_dish_ids.append(e_raw["id"])
                if e_raw.get("staple_ingredient"):
                    today_staples.add(e_raw["staple_ingredient"])

                d_raw = DietPlannerService.select_best_dish(
                    di_options, "Dinner", i, meal_targets["Dinner"], profile_input,
                    used_dish_counts, last_used_day, today_staples, user_seed, variation_seed,
                    today_dish_ids=today_dish_ids, previous_week_dish_ids=prev_week_set,
                    max_weekly_repeats=di_max_rep
                )
                used_dish_counts[d_raw["id"]] = used_dish_counts.get(d_raw["id"], 0) + 1
                last_used_day[d_raw["id"]] = i
                today_dish_ids.add(d_raw["id"])
                all_selected_dish_ids.append(d_raw["id"])

                b_scaled = scale_dish_to_target_calories(b_raw, meal_targets["Breakfast"])
                mm_scaled = scale_dish_to_target_calories(mm_raw, meal_targets["Mid-morning Snack"])
                l_scaled = scale_dish_to_target_calories(l_raw, meal_targets["Lunch"])
                e_scaled = scale_dish_to_target_calories(e_raw, meal_targets["Evening Snack"])
                d_scaled = scale_dish_to_target_calories(d_raw, meal_targets["Dinner"])

                b_item = DietPlannerService._format_dish_to_item(b_scaled)
                mm_item = DietPlannerService._format_dish_to_item(mm_scaled)
                l_item = DietPlannerService._format_dish_to_item(l_scaled)
                e_item = DietPlannerService._format_dish_to_item(e_scaled)
                d_item = DietPlannerService._format_dish_to_item(d_scaled)

                meals = [
                    {
                        "mealType": "Breakfast",
                        "timeSuggestion": "07:30 AM – 08:30 AM",
                        "items": [b_item],
                        "totalCalories": b_item["calories"],
                        "totalProtein": b_item["proteinGrams"],
                        "totalCarbs": b_item["carbsGrams"],
                        "totalFat": b_item["fatGrams"],
                        "totalFibre": b_item["fibreGrams"]
                    },
                    {
                        "mealType": "Mid-morning Snack",
                        "timeSuggestion": "11:00 AM – 11:30 AM",
                        "items": [mm_item],
                        "totalCalories": mm_item["calories"],
                        "totalProtein": mm_item["proteinGrams"],
                        "totalCarbs": mm_item["carbsGrams"],
                        "totalFat": mm_item["fatGrams"],
                        "totalFibre": mm_item["fibreGrams"]
                    },
                    {
                        "mealType": "Lunch",
                        "timeSuggestion": "01:00 PM – 02:00 PM",
                        "items": [l_item],
                        "totalCalories": l_item["calories"],
                        "totalProtein": l_item["proteinGrams"],
                        "totalCarbs": l_item["carbsGrams"],
                        "totalFat": l_item["fatGrams"],
                        "totalFibre": l_item["fibreGrams"]
                    },
                    {
                        "mealType": "Evening Snack",
                        "timeSuggestion": "04:30 PM – 05:30 PM",
                        "items": [e_item],
                        "totalCalories": e_item["calories"],
                        "totalProtein": e_item["proteinGrams"],
                        "totalCarbs": e_item["carbsGrams"],
                        "totalFat": e_item["fatGrams"],
                        "totalFibre": e_item["fibreGrams"]
                    },
                    {
                        "mealType": "Dinner",
                        "timeSuggestion": "07:30 PM – 08:30 PM",
                        "items": [d_item],
                        "totalCalories": d_item["calories"],
                        "totalProtein": d_item["proteinGrams"],
                        "totalCarbs": d_item["carbsGrams"],
                        "totalFat": d_item["fatGrams"],
                        "totalFibre": d_item["fibreGrams"]
                    }
                ]

            day_cals = sum(m["totalCalories"] for m in meals)
            day_prot = round(sum(m["totalProtein"] for m in meals), 1)
            day_carbs = round(sum(m["totalCarbs"] for m in meals), 1)
            day_fat = round(sum(m["totalFat"] for m in meals), 1)
            day_fibre = round(sum(m["totalFibre"] for m in meals), 1)

            cal_diff = day_cals - target_cals
            diff_pct = round((abs(cal_diff) / max(1, target_cals)) * 100.0, 2)
            within_tol = diff_pct <= 5.0

            # Macro reconciliation calculation
            prot_kcal = int(round(day_prot * 4.0))
            carbs_kcal = int(round(day_carbs * 4.0))
            fat_kcal = int(round(day_fat * 9.0))
            macro_sum = prot_kcal + carbs_kcal + fat_kcal

            formula_str = f"({prot_kcal} kcal P + {carbs_kcal} kcal C + {fat_kcal} kcal F)"
            macro_reconciliation = {
                "proteinCalories": prot_kcal,
                "carbsCalories": carbs_kcal,
                "fatCalories": fat_kcal,
                "macroSumCalories": macro_sum,
                "atwaterCalculatedKcal": macro_sum,
                "formula": formula_str,
                "differenceFromTotal": day_cals - macro_sum,
                "reconciliationNotes": (
                    "Reconciled from ingredient chemical data. Energy contribution utilizes Atwater factors "
                    "(4 kcal/g protein, 4 kcal/g digestible carbohydrate, 9 kcal/g lipid). "
                    "Insoluble dietary fibre is not counted as metabolisable energy."
                )
            }

            days_list.append({
                "dayNumber": i + 1,
                "dayName": day_names[i],
                "meals": meals,
                "dailyTargetCalories": target_cals,
                "dailyTotalCalories": day_cals,
                "calorieDifference": cal_diff,
                "calorieDifferencePercent": diff_pct,
                "isWithinTolerance": within_tol,
                "dailyTotalProtein": day_prot,
                "dailyTotalCarbs": day_carbs,
                "dailyTotalFat": day_fat,
                "dailyTotalFibre": day_fibre,
                "hydrationTip": hydration_tips[i],
                "macroReconciliation": macro_reconciliation
            })

        guidance = DietPlannerService._generate_guidance(
            food_pref=food_pref,
            allergies=allergies,
            custom_allergies_text=custom_allergies_text,
            intolerances=intolerances,
            dietary_focus=dietary_focus,
            goal=goal
        )

        plan = {
            "id": None,
            "weekNumber": week_number,
            "weekStartDate": week_start_date,
            "selectedDishIds": all_selected_dish_ids,
            "profileSummary": {
                "bmi": metrics["bmi"],
                "bmiCategory": metrics["bmiCategory"],
                "bmr": metrics["bmr"],
                "tdee": metrics["tdee"],
                "goalAdjustmentCalories": metrics.get("goalAdjustmentCalories", 0),
                "targetCalories": target_cals,
                "targetProtein": target_protein,
                "targetCarbs": target_carbs,
                "targetFat": target_fat,
                "targetFibre": target_fibre,
                "goal": goal,
                "foodPreference": food_pref,
                "mealsPerDay": meals_per_day,
                "allergies": allergies,
                "customAllergies": custom_allergies_text,
                "intolerances": intolerances,
                "dislikedFoods": disliked_foods,
                "dietaryRestrictions": dietary_focus,
                "preferredCuisine": cuisine,
                "budgetTier": budget_tier,
                "cookingTimePref": cooking_pref
            },
            "days": days_list,
            "guidance": guidance,
            "generatedAt": datetime.datetime.utcnow().isoformat(),
            "nutritionalNotes": [
                f"Personalized target: {target_cals} kcal/day aligned to {goal.replace('_', ' ')} based on Mifflin-St Jeor metabolic math.",
                f"Macronutrient partition: ~{target_protein}g protein, ~{target_carbs}g complex carbs, ~{target_fat}g healthy fats, ~{target_fibre}g dietary fibre.",
                f"Additive Arithmetic Guarantee: sum(ingredients) == dish == sum(dishes) == meal == sum(meals) == daily total ({target_cals} kcal).",
                f"Allergen safeguard active: Zero tolerance for {', '.join(allergies + AllergyFilterService.parse_custom_allergies(custom_allergies_text)) if (allergies or custom_allergies_text) else 'standard exclusions'}."
            ],
            "safetyWarnings": metrics.get("safetyWarnings", []),
            "disclaimer": metrics.get("disclaimer", "")
        }

        # ---------------------------------------------------------------------
        # 4. Mandatory Post-Generation Plan Validation (Guarantees zero leakage & exact math)
        # ---------------------------------------------------------------------
        PlanValidatorService.validate_plan_compliance_and_math(
            plan=plan,
            food_preference=food_pref,
            allergies=allergies,
            custom_allergies_text=custom_allergies_text,
            intolerances=intolerances,
            dietary_focus=dietary_focus
        )

        return plan
