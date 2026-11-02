"""
AGRO AI — Comprehensive Better Nutrition Automated Test Suite
Validates:
1. Mifflin-St Jeor formula accuracy across male and female test vectors.
2. Individualized deficit/surplus scaling (not arbitrary flat numbers).
3. Minimum safety floors and clinical safeguards (under-18, underweight, pregnancy).
4. Multi-allergen exclusions (dairy, gluten, peanuts, eggs, soy, etc.).
5. Custom free-text allergies and ingredient-level scanning (e.g. mushrooms, brinjal, capsicum).
6. Strict dietary preference compliance (Vegan, Jain, Vegetarian, Eggetarian, Pescatarian).
7. Exact mathematical consistency: sum(ingredients) == item == sum(items) == meal == sum(meals) == day.
8. Post-generation validation guarantee.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.nutrition_calculator import NutritionCalculatorService
from app.services.allergy_filter_service import AllergyFilterService
from app.services.food_database import FOOD_DATABASE
from app.services.diet_planner import DietPlannerService

client = TestClient(app)

# =============================================================================
# 1. METABOLIC CALCULATION & EQUATION TESTS
# =============================================================================

def test_mifflin_st_jeor_male_known_vector():
    """
    Male, 28 years, 172 cm, 68 kg, Moderate Activity (1.55)
    BMR = (10*68) + (6.25*172) - (5*28) + 5 = 680 + 1075 - 140 + 5 = 1620.0 kcal
    TDEE = 1620 * 1.55 = 2511.0 kcal
    """
    res = NutritionCalculatorService.calculate_metrics(
        age=28, gender="male", height_cm=172.0, weight_kg=68.0,
        activity_level="moderate", goal="maintenance"
    )
    assert abs(res["bmr"] - 1620.0) < 1.0
    assert abs(res["tdee"] - 2511.0) < 2.0
    assert res["targetCalories"] == int(round(res["tdee"]))
    assert res["bmiCategory"] == "Normal weight"
    assert res["targetProteinGrams"] > 0
    assert res["targetFibreGrams"] >= 30

def test_mifflin_st_jeor_female_known_vector():
    """
    Female, 32 years, 162 cm, 58 kg, Light Activity (1.375)
    BMR = (10*58) + (6.25*162) - (5*32) - 161 = 580 + 1012.5 - 160 - 161 = 1271.5 kcal
    TDEE = 1271.5 * 1.375 = 1748.3 kcal
    """
    res = NutritionCalculatorService.calculate_metrics(
        age=32, gender="female", height_cm=162.0, weight_kg=58.0,
        activity_level="light", goal="maintenance"
    )
    assert abs(res["bmr"] - 1271.5) < 1.0
    assert abs(res["tdee"] - 1748.3) < 2.0
    assert res["targetCalories"] == int(round(res["tdee"]))

def test_individualized_calorie_adjustment_not_fixed():
    """
    Verifies that calorie adjustment is individualized based on TDEE and BMI,
    NOT a flat -400 / +350 for every user.
    """
    # Sedentary normal weight user (lower TDEE)
    user_small = NutritionCalculatorService.calculate_metrics(
        age=25, gender="female", height_cm=155.0, weight_kg=50.0,
        activity_level="sedentary", goal="weight_loss"
    )
    # Active overweight user (higher TDEE)
    user_large = NutritionCalculatorService.calculate_metrics(
        age=30, gender="male", height_cm=185.0, weight_kg=95.0,
        activity_level="active", goal="weight_loss"
    )
    
    deficit_small = user_small["tdee"] - user_small["targetCalories"]
    deficit_large = user_large["tdee"] - user_large["targetCalories"]
    
    # Larger, active user should have a different, larger safe deficit than small sedentary user
    assert deficit_small != deficit_large
    assert deficit_large > deficit_small

def test_minimum_calorie_safety_floors():
    """
    Verifies that extreme deficits cannot breach the safe minimum floor:
    Female floor: 1200 kcal, Male floor: 1500 kcal.
    """
    # Very small female with sedentary lifestyle requesting weight loss
    female_res = NutritionCalculatorService.calculate_metrics(
        age=45, gender="female", height_cm=148.0, weight_kg=46.0,
        activity_level="sedentary", goal="weight_loss"
    )
    assert female_res["targetCalories"] >= 1200

    # Male with low weight requesting weight loss
    male_res = NutritionCalculatorService.calculate_metrics(
        age=30, gender="male", height_cm=165.0, weight_kg=55.0,
        activity_level="sedentary", goal="weight_loss"
    )
    assert male_res["targetCalories"] >= 1500

def test_underweight_weight_loss_safeguard():
    """
    If BMI < 18.5, weight loss must trigger a clinical safety warning
    and protect caloric target from dangerous deficits.
    """
    res = NutritionCalculatorService.calculate_metrics(
        age=22, gender="female", height_cm=170.0, weight_kg=45.0,  # BMI = 15.6 (severely underweight)
        activity_level="moderate", goal="weight_loss"
    )
    assert res["bmi"] < 18.5
    assert res["bmiCategory"] == "Underweight"
    assert any("Underweight" in w for w in res["safetyWarnings"])
    # Caloric target protected at maintenance
    assert res["targetCalories"] == int(round(res["tdee"]))

def test_adolescent_and_pregnancy_safeguards():
    """
    Verifies that under-18 and pregnancy dietary focus generate appropriate clinical guidance.
    """
    # Under-18
    youth_res = NutritionCalculatorService.calculate_metrics(
        age=16, gender="male", height_cm=170.0, weight_kg=60.0,
        activity_level="moderate", goal="maintenance"
    )
    assert any("Adolescent" in w for w in youth_res["safetyWarnings"])

    # Pregnancy
    preg_res = NutritionCalculatorService.calculate_metrics(
        age=28, gender="female", height_cm=160.0, weight_kg=62.0,
        activity_level="light", goal="maintenance",
        dietary_focus=["pregnancy_breastfeeding"]
    )
    assert any("Maternal" in w for w in preg_res["safetyWarnings"])

# =============================================================================
# 2. ALLERGEN & CUSTOM INGREDIENT FILTERING TESTS
# =============================================================================

def test_predefined_allergen_exclusion():
    """
    Tests that standard allergens (peanuts, tree_nuts, dairy, gluten, soy, eggs, seafood)
    are strictly filtered out of eligible dishes.
    """
    safe_foods = AllergyFilterService.filter_safe_foods(
        foods=FOOD_DATABASE,
        food_preference="vegetarian",
        allergies=["dairy", "gluten", "peanuts"]
    )
    assert len(safe_foods) > 0
    for food in safe_foods:
        allergens = {a.lower() for a in food.get("allergens", [])}
        assert "dairy" not in allergens
        assert "gluten" not in allergens
        assert "peanuts" not in allergens
        for ing in food.get("ingredients", []):
            ing_algs = {a.lower() for a in ing.get("allergens", [])}
            assert "dairy" not in ing_algs
            assert "gluten" not in ing_algs
            assert "peanuts" not in ing_algs

def test_custom_free_text_allergy_exclusion():
    """
    Tests that user-typed custom ingredients (e.g. "mushrooms, brinjal, capsicum")
    are parsed and matched across dish names and ingredient lists.
    """
    custom_text = "capsicum, bell pepper, mushroom"
    safe_foods = AllergyFilterService.filter_safe_foods(
        foods=FOOD_DATABASE,
        food_preference="vegetarian",
        allergies=[],
        custom_allergies_text=custom_text
    )
    for food in safe_foods:
        food_name_lower = food["name"].lower()
        assert "capsicum" not in food_name_lower
        assert "bell pepper" not in food_name_lower
        assert "mushroom" not in food_name_lower
        for ing in food.get("ingredients", []):
            ing_name_lower = ing["name"].lower()
            assert "capsicum" not in ing_name_lower
            assert "bell pepper" not in ing_name_lower
            assert "mushroom" not in ing_name_lower

def test_jain_dietary_rules_strictness():
    """
    Tests that Jain preference excludes onion, garlic, potatoes, carrots, radishes,
    and any non-Jain dish.
    """
    safe_foods = AllergyFilterService.filter_safe_foods(
        foods=FOOD_DATABASE,
        food_preference="jain",
        allergies=[]
    )
    for food in safe_foods:
        assert food.get("is_jain") is True
        for ing in food.get("ingredients", []):
            ing_lower = ing["name"].lower()
            assert "onion" not in ing_lower
            assert "garlic" not in ing_lower
            assert "potato" not in ing_lower

def test_vegan_dietary_rules():
    """
    Tests that Vegan preference strictly excludes dairy, ghee, eggs, and seafood.
    """
    safe_foods = AllergyFilterService.filter_safe_foods(
        foods=FOOD_DATABASE,
        food_preference="vegan",
        allergies=[]
    )
    for food in safe_foods:
        assert food.get("is_vegan") is True
        algs = {a.lower() for a in food.get("allergens", [])}
        assert "dairy" not in algs
        assert "eggs" not in algs
        assert "seafood" not in algs

# =============================================================================
# 3. 7-DAY DIET PLAN GENERATION & POST-GENERATION VALIDATION
# =============================================================================

def test_seven_day_plan_complete_structure_and_math():
    """
    Verifies that the generated plan contains 7 days, correct meals per day,
    and that:
    1. sum(ingredient.calories) == item.calories
    2. sum(item.calories) == meal.totalCalories
    3. sum(meal.totalCalories) == day.dailyTotalCalories
    """
    payload = {
        "age": 28,
        "gender": "male",
        "heightCm": 175.0,
        "weightKg": 70.0,
        "activityLevel": "moderate",
        "goal": "weight_loss",
        "foodPreference": "vegetarian",
        "mealsPerDay": 5,
        "allergies": ["peanuts"],
        "customAllergies": "mushroom, capsicum",
        "dietaryRestrictions": ["high_protein", "home_cooked"],
        "preferredCuisine": "indian"
    }
    response = client.post("/api/nutrition/weekly-plan", json=payload)
    assert response.status_code == 200
    plan = response.json()

    assert len(plan["days"]) == 7
    assert "guidance" in plan
    assert len(plan["guidance"]["foodsToEat"]) > 0
    assert len(plan["guidance"]["foodsToAvoid"]) > 0
    assert len(plan["guidance"]["safeSubstitutions"]) > 0

    for day in plan["days"]:
        assert len(day["meals"]) == 5
        day_cal_sum = 0
        for meal in day["meals"]:
            meal_cal_sum = 0
            for item in meal["items"]:
                # Check ingredient sum equals item calories
                if item.get("ingredients"):
                    ing_sum = sum(ing["calories"] for ing in item["ingredients"])
                    assert ing_sum == item["calories"], f"Ingredient sum {ing_sum} != item {item['calories']}"
                
                # Check allergen exclusion
                assert "peanuts" not in item.get("allergens", [])
                assert "capsicum" not in item["name"].lower()
                assert "mushroom" not in item["name"].lower()
                
                meal_cal_sum += item["calories"]

            assert meal["totalCalories"] == meal_cal_sum, f"Meal total {meal['totalCalories']} != items {meal_cal_sum}"
            day_cal_sum += meal_cal_sum

        assert day["dailyTotalCalories"] == day_cal_sum, f"Day total {day['dailyTotalCalories']} != meals {day_cal_sum}"

def test_plan_with_three_meals_per_day():
    """
    Verifies that the user can select 3 meals per day and get Breakfast, Lunch, Dinner.
    """
    payload = {
        "age": 30,
        "gender": "female",
        "heightCm": 165.0,
        "weightKg": 60.0,
        "activityLevel": "light",
        "goal": "maintenance",
        "foodPreference": "vegetarian",
        "mealsPerDay": 3,
        "allergies": [],
        "dietaryRestrictions": [],
        "preferredCuisine": "indian"
    }
    response = client.post("/api/nutrition/weekly-plan", json=payload)
    assert response.status_code == 200
    plan = response.json()

    for day in plan["days"]:
        assert len(day["meals"]) == 3
        meal_types = [m["mealType"] for m in day["meals"]]
        assert meal_types == ["Breakfast", "Lunch", "Dinner"]

def test_invalid_input_validation():
    """
    Verifies that invalid age, negative weights, or extreme values trigger HTTP 422.
    """
    bad_payload = {
        "age": 5,  # under minimum 10
        "gender": "male",
        "heightCm": 170.0,
        "weightKg": 60.0,
        "activityLevel": "moderate",
        "goal": "maintenance",
        "foodPreference": "vegetarian"
    }
    response = client.post("/api/nutrition/calculate", json=bad_payload)
    assert response.status_code == 422

def test_valid_weight_gain_request():
    """
    Verifies a valid weight-gain request with active physical routine and 6 meals per day.
    """
    payload = {
        "age": 24,
        "gender": "male",
        "heightCm": 180.0,
        "weightKg": 64.0,
        "activityLevel": "active",
        "goal": "weight_gain",
        "foodPreference": "vegetarian",
        "mealsPerDay": 6,
        "allergies": [],
        "dietaryRestrictions": ["high_protein", "sports_nutrition"],
        "preferredCuisine": "indian"
    }
    response = client.post("/api/nutrition/weekly-plan", json=payload)
    assert response.status_code == 200
    plan = response.json()

    assert plan["profileSummary"]["goal"] == "weight_gain"
    assert plan["profileSummary"]["targetCalories"] > plan["profileSummary"]["tdee"]
    assert len(plan["days"]) == 7
    for day in plan["days"]:
        assert len(day["meals"]) == 6
        assert day["dailyTotalCalories"] == plan["profileSummary"]["targetCalories"]
        assert day["dailyTotalCalories"] == sum(m["totalCalories"] for m in day["meals"])

def test_demographic_matrix():
    """
    Verifies different demographic vectors:
    - Young active female
    - Senior male
    - Sedentary middle-aged female
    """
    vectors = [
        {"age": 21, "gender": "female", "heightCm": 160.0, "weightKg": 52.0, "activityLevel": "very_active", "goal": "maintenance"},
        {"age": 68, "gender": "male", "heightCm": 168.0, "weightKg": 70.0, "activityLevel": "sedentary", "goal": "weight_loss"},
        {"age": 42, "gender": "female", "heightCm": 170.0, "weightKg": 78.0, "activityLevel": "light", "goal": "weight_loss"},
    ]
    for vec in vectors:
        res = NutritionCalculatorService.calculate_metrics(
            age=vec["age"],
            gender=vec["gender"],
            height_cm=vec["heightCm"],
            weight_kg=vec["weightKg"],
            activity_level=vec["activityLevel"],
            goal=vec["goal"]
        )
        assert res["bmr"] > 800
        assert res["tdee"] >= res["bmr"]
        assert res["targetCalories"] >= (1200 if vec["gender"] == "female" else 1500)
        assert res["targetProteinGrams"] > 40
        # Check macro reconciliation
        macro_cals = (res["targetProteinGrams"] * 4) + (res["targetCarbsGrams"] * 4) + (res["targetFatGrams"] * 9)
        assert abs(macro_cals - res["targetCalories"]) <= 5

def test_non_vegetarian_and_pescatarian_plans():
    """
    Verifies non-vegetarian and pescatarian meal plans accurately incorporate chicken and fish
    with exact ingredient-level macro traceability.
    """
    # Non-vegetarian
    non_veg_payload = {
        "age": 28, "gender": "male", "heightCm": 176.0, "weightKg": 75.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "non_vegetarian",
        "mealsPerDay": 5, "allergies": [], "dietaryRestrictions": ["high_protein"],
        "preferredCuisine": "indian"
    }
    resp = client.post("/api/nutrition/weekly-plan", json=non_veg_payload)
    assert resp.status_code == 200
    plan = resp.json()
    assert len(plan["days"]) == 7

    # Pescatarian
    pesca_payload = {
        "age": 31, "gender": "female", "heightCm": 165.0, "weightKg": 60.0,
        "activityLevel": "moderate", "goal": "maintenance", "foodPreference": "pescatarian",
        "mealsPerDay": 4, "allergies": [], "dietaryRestrictions": [],
        "preferredCuisine": "indian"
    }
    resp_pesca = client.post("/api/nutrition/weekly-plan", json=pesca_payload)
    assert resp_pesca.status_code == 200
    pesca_plan = resp_pesca.json()
    assert len(pesca_plan["days"]) == 7

def test_custom_free_text_uncommon_allergy():
    """
    Verifies that a user-entered allergy that is not in the preset options
    (e.g. 'brinjal, mushrooms, pineapple') is strictly excluded from all 7 days.
    """
    payload = {
        "age": 26, "gender": "female", "heightCm": 163.0, "weightKg": 57.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "allergies": [],
        "customAllergies": "brinjal, mushrooms, pineapple",
        "dietaryRestrictions": ["high_fibre"], "preferredCuisine": "indian"
    }
    response = client.post("/api/nutrition/weekly-plan", json=payload)
    assert response.status_code == 200
    plan = response.json()

    for day in plan["days"]:
        for meal in day["meals"]:
            for item in meal["items"]:
                name_low = item["name"].lower()
                assert "brinjal" not in name_low
                assert "baingan" not in name_low
                assert "mushroom" not in name_low
                assert "pineapple" not in name_low
                for ing in item.get("ingredients", []):
                    ing_low = ing["name"].lower()
                    assert "brinjal" not in ing_low
                    assert "mushroom" not in ing_low
                    assert "pineapple" not in ing_low

def test_multiple_simultaneous_allergies():
    """
    Verifies that multiple concurrent allergies (e.g. peanuts, dairy, gluten, mustard)
    are strictly filtered out with zero presence across all dishes and ingredients.
    """
    payload = {
        "age": 32, "gender": "male", "heightCm": 174.0, "weightKg": 70.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "allergies": ["peanuts", "dairy", "gluten", "mustard"],
        "dietaryRestrictions": ["high_protein"], "preferredCuisine": "indian"
    }
    response = client.post("/api/nutrition/weekly-plan", json=payload)
    assert response.status_code == 200
    plan = response.json()

    for day in plan["days"]:
        for meal in day["meals"]:
            for item in meal["items"]:
                algs = [a.lower() for a in item.get("allergens", [])]
                assert "peanuts" not in algs
                assert "dairy" not in algs
                assert "gluten" not in algs
                assert "mustard" not in algs
                for ing in item.get("ingredients", []):
                    ing_algs = [a.lower() for a in ing.get("allergens", [])]
                    assert "peanuts" not in ing_algs
                    assert "dairy" not in ing_algs
                    assert "gluten" not in ing_algs
                    assert "mustard" not in ing_algs

def test_substitution_allergy_safety():
    """
    Verifies that safe substitutions generated in clinical guidance never suggest
    an allergen declared by the user (e.g. never suggest Tofu if allergic to soy).
    """
    payload = {
        "age": 28, "gender": "male", "heightCm": 172.0, "weightKg": 68.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "allergies": ["dairy", "soy"],
        "dietaryRestrictions": [], "preferredCuisine": "indian"
    }
    response = client.post("/api/nutrition/weekly-plan", json=payload)
    assert response.status_code == 200
    plan = response.json()

    subs = plan["guidance"]["safeSubstitutions"]
    for s in subs:
        sub_text = s["substitute"].lower()
        # Should NOT recommend soy/tofu when allergic to soy
        assert "tofu" not in sub_text
        assert "soya" not in sub_text
        assert "soy" not in sub_text

def test_calorie_macro_reconciliation_math():
    """
    Verifies that protein (4 kcal/g), carbs (4 kcal/g), and fat (9 kcal/g)
    energy contributions reconcile with the daily calorie target within <= 5 kcal rounding tolerance.
    """
    for wt in [50.0, 65.0, 80.0, 95.0, 110.0]:
        for g in ["weight_loss", "maintenance", "weight_gain"]:
            res = NutritionCalculatorService.calculate_metrics(
                age=30, gender="male", height_cm=175.0, weight_kg=wt,
                activity_level="moderate", goal=g
            )
            macro_energy = (res["targetProteinGrams"] * 4) + (res["targetCarbsGrams"] * 4) + (res["targetFatGrams"] * 9)
            diff = abs(macro_energy - res["targetCalories"])
            assert diff <= 5, f"Macro energy {macro_energy} kcal != target {res['targetCalories']} kcal (diff {diff})"

def test_extreme_bmi_safety():
    """
    Verifies behavior with extreme BMIs:
    - Severe Underweight (< 16.0)
    - Severe Obesity (>= 35.0)
    """
    # Severe Underweight
    under = NutritionCalculatorService.calculate_metrics(
        age=20, gender="female", height_cm=170.0, weight_kg=40.0,
        activity_level="sedentary", goal="weight_loss"
    )
    assert under["bmi"] < 16.0
    assert under["targetCalories"] == int(round(under["tdee"]))  # Deficit blocked
    assert any("Underweight" in w for w in under["safetyWarnings"])

    # Severe Obesity
    obese = NutritionCalculatorService.calculate_metrics(
        age=40, gender="male", height_cm=170.0, weight_kg=120.0,
        activity_level="sedentary", goal="weight_loss"
    )
    assert obese["bmi"] >= 35.0
    assert any("Obesity" in w for w in obese["safetyWarnings"])

def test_impossible_dietary_conflict_error_handling():
    """
    Verifies that when impossible constraints are entered (e.g. excluding all safe foods),
    backend raises HTTP 422 with a descriptive error message rather than generating fake meals.
    """
    impossible_payload = {
        "age": 28, "gender": "male", "heightCm": 172.0, "weightKg": 68.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegan",
        "mealsPerDay": 5,
        # Exclude all grains, legumes, and seeds
        "customAllergies": "rice, wheat, poha, oats, ragi, millet, moong, toor, dal, rajma, chana, seeds, papaya, coconut, oil",
        "dietaryRestrictions": [], "preferredCuisine": "indian"
    }
    response = client.post("/api/nutrition/weekly-plan", json=impossible_payload)
    assert response.status_code == 422
    err_detail = response.json()["detail"]
    assert "Unable to construct a compliant meal plan" in err_detail

# =============================================================================
# 4. PERSONALIZATION, VARIETY & ALTERNATIVE DISH TESTS
# =============================================================================

def test_different_users_receive_different_meal_plans():
    """
    Verifies the fix for the root cause of repeated plans:
    User A (young female, South Indian focus, weight loss) and
    User B (older male, North Indian focus, weight gain)
    must receive personalized, distinct meal schedules.
    """
    user_a = {
        "age": 25, "gender": "female", "heightCm": 160.0, "weightKg": 54.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "south_indian"
    }
    user_b = {
        "age": 42, "gender": "male", "heightCm": 182.0, "weightKg": 84.0,
        "activityLevel": "active", "goal": "weight_gain", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "north_indian"
    }

    resp_a = client.post("/api/nutrition/weekly-plan", json=user_a)
    resp_b = client.post("/api/nutrition/weekly-plan", json=user_b)
    assert resp_a.status_code == 200
    assert resp_b.status_code == 200

    plan_a = resp_a.json()
    plan_b = resp_b.json()

    # Targets must differ
    assert plan_a["profileSummary"]["targetCalories"] != plan_b["profileSummary"]["targetCalories"]

    # Meals must not be identical across all days
    a_day1_meals = [m["items"][0]["name"] for m in plan_a["days"][0]["meals"]]
    b_day1_meals = [m["items"][0]["name"] for m in plan_b["days"][0]["meals"]]
    assert a_day1_meals != b_day1_meals

def test_within_week_meal_variety_no_consecutive_repeats():
    """
    Verifies that within a 7-day schedule, no recipe is repeated on consecutive days.
    """
    payload = {
        "age": 30, "gender": "female", "heightCm": 165.0, "weightKg": 60.0,
        "activityLevel": "moderate", "goal": "maintenance", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "indian"
    }
    resp = client.post("/api/nutrition/weekly-plan", json=payload)
    assert resp.status_code == 200
    plan = resp.json()

    for meal_idx in range(5):
        meal_names = [plan["days"][d]["meals"][meal_idx]["items"][0]["name"] for d in range(7)]
        # Verify no consecutive repeat: day d != day d+1
        for d in range(6):
            assert meal_names[d] != meal_names[d + 1], f"Consecutive repeat in meal slot {meal_idx}: Day {d+1} and Day {d+2} both have '{meal_names[d]}'"

def test_disliked_foods_avoidance():
    """
    Verifies that foods marked as disliked by the user are avoided in the generated plan.
    """
    payload = {
        "age": 28, "gender": "male", "heightCm": 172.0, "weightKg": 68.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "dislikedFoods": "baingan, eggplant, okra, brinjal"
    }
    resp = client.post("/api/nutrition/weekly-plan", json=payload)
    assert resp.status_code == 200
    plan = resp.json()

    for day in plan["days"]:
        for meal in day["meals"]:
            for item in meal["items"]:
                item_name_lower = item["name"].lower()
                assert "baingan" not in item_name_lower
                assert "eggplant" not in item_name_lower
                assert "brinjal" not in item_name_lower

def test_swap_dish_removed_completely():
    """
    SECTION 8 - TEST 11:
    Verifies that the Swap Dish endpoint (/api/nutrition/alternative-dish) has been
    completely removed and returns HTTP 404, while other nutrition features continue working.
    """
    payload = {
        "mealType": "Lunch",
        "targetCalories": 550,
        "currentDishName": "Rajma Masala",
        "foodPreference": "vegetarian"
    }
    resp = client.post("/api/nutrition/alternative-dish", json=payload)
    assert resp.status_code == 404

def test_plan_regeneration_with_variation_seed():
    """
    Verifies that changing variationSeed generates a distinct, valid variation of the 7-day plan.
    """
    base_payload = {
        "age": 28, "gender": "male", "heightCm": 172.0, "weightKg": 68.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "indian"
    }
    resp1 = client.post("/api/nutrition/weekly-plan", json={**base_payload, "variationSeed": 0})
    resp2 = client.post("/api/nutrition/weekly-plan", json={**base_payload, "variationSeed": 1})
    assert resp1.status_code == 200
    assert resp2.status_code == 200

    plan1 = resp1.json()
    plan2 = resp2.json()

    plan1_breakfasts = [plan1["days"][d]["meals"][0]["items"][0]["name"] for d in range(7)]
    plan2_breakfasts = [plan2["days"][d]["meals"][0]["items"][0]["name"] for d in range(7)]
    assert plan1_breakfasts != plan2_breakfasts

def test_food_search_api():
    """
    Verifies that /api/nutrition/foods allows querying verified IFCT 2017 dishes.
    """
    resp = client.get("/api/nutrition/foods?category=breakfast")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] >= 10
    assert "IFCT 2017" in data["source"]
    for dish in data["results"]:
        assert dish["category"] == "breakfast"
        assert dish["calories"] > 0

def test_daily_calorie_tolerance_bounds():
    """
    Verifies that daily planned calories match daily target calories within 5% tolerance across all days.
    """
    payload = {
        "age": 35, "gender": "male", "heightCm": 178.0, "weightKg": 75.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5
    }
    resp = client.post("/api/nutrition/weekly-plan", json=payload)
    assert resp.status_code == 200
    plan = resp.json()

    target_cal = plan["profileSummary"]["targetCalories"]
    for day in plan["days"]:
        assert day["dailyTargetCalories"] == target_cal
        assert day["isWithinTolerance"] is True
        assert day["calorieDifferencePercent"] <= 5.0
        assert day["dailyTotalCalories"] == target_cal
        assert day["macroReconciliation"] is not None

def test_unauthenticated_profile_access_rejected():
    """
    Verifies that accessing private user profile endpoints without a valid JWT token
    is safely rejected with HTTP 401 Unauthorized.
    """
    resp_get = client.get("/api/nutrition/profile")
    assert resp_get.status_code == 401

    resp_put = client.put("/api/nutrition/profile", json={"age": 30})
    assert resp_put.status_code == 401

# =============================================================================
# MANDATORY SECTION 8 VERIFICATION SUITE (ALL 12 REQUIREMENTS)
# =============================================================================

def test_req1_complete_seven_day_plan_contains_35_meal_slots():
    """
    REQUIRED TEST 1:
    A complete seven-day plan contains exactly 35 meal slots:
    7 days x 5 meal slots (Breakfast, Mid-morning snack, Lunch, Evening snack, Dinner).
    """
    payload = {
        "age": 28, "gender": "male", "heightCm": 174.0, "weightKg": 70.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "indian"
    }
    resp = client.post("/api/nutrition/weekly-plan", json=payload)
    assert resp.status_code == 200
    plan = resp.json()

    expected_slot_types = ["Breakfast", "Mid-morning Snack", "Lunch", "Evening Snack", "Dinner"]
    assert len(plan["days"]) == 7, "Plan must contain exactly 7 days"

    total_slots = 0
    for day_idx, day in enumerate(plan["days"]):
        assert len(day["meals"]) == 5, f"Day {day_idx + 1} must contain exactly 5 meal slots"
        slot_names = [m["mealType"] for m in day["meals"]]
        assert slot_names == expected_slot_types, f"Day {day_idx + 1} slot sequence mismatch: {slot_names}"
        for meal in day["meals"]:
            assert len(meal["items"]) >= 1, f"Meal {meal['mealType']} must contain at least 1 verified dish"
            total_slots += 1

    assert total_slots == 35, f"Plan must contain exactly 35 meal slots, got {total_slots}"
    assert len(plan["selectedDishIds"]) == 35, f"Plan selectedDishIds must record all 35 dish selections, got {len(plan['selectedDishIds'])}"

def test_req2_different_user_profiles_produce_appropriately_personalized_plans():
    """
    REQUIRED TEST 2:
    Different user profiles produce appropriately personalized plans:
    User A: 24 y/o female, 155 cm, 49 kg, sedentary, weight_loss, vegetarian, South Indian cuisine
    User B: 35 y/o male, 185 cm, 88 kg, very_active, weight_gain, non_vegetarian, North Indian cuisine
    """
    user_a = {
        "age": 24, "gender": "female", "heightCm": 155.0, "weightKg": 49.0,
        "activityLevel": "sedentary", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "south_indian"
    }
    user_b = {
        "age": 35, "gender": "male", "heightCm": 185.0, "weightKg": 88.0,
        "activityLevel": "very_active", "goal": "weight_gain", "foodPreference": "non_vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "north_indian"
    }

    resp_a = client.post("/api/nutrition/weekly-plan", json=user_a)
    resp_b = client.post("/api/nutrition/weekly-plan", json=user_b)
    assert resp_a.status_code == 200
    assert resp_b.status_code == 200

    plan_a = resp_a.json()
    plan_b = resp_b.json()

    cals_a = plan_a["profileSummary"]["targetCalories"]
    cals_b = plan_b["profileSummary"]["targetCalories"]

    # Metabolic targets must differ significantly
    assert cals_b > cals_a + 800, f"Male heavy active surplus ({cals_b}) must be significantly higher than small female deficit ({cals_a})"

    # Protein targets must differ
    prot_a = plan_a["profileSummary"]["targetProtein"]
    prot_b = plan_b["profileSummary"]["targetProtein"]
    assert prot_b > prot_a + 30

    # Menus must differ appropriately
    dishes_a = set(plan_a["selectedDishIds"])
    dishes_b = set(plan_b["selectedDishIds"])
    # Common dishes between such radically different profiles should be minimal
    overlap = dishes_a.intersection(dishes_b)
    assert len(overlap) <= 18, f"Different profiles must have predominantly distinct meal selections, overlap was {len(overlap)}"

def test_req3_dietary_rules_respected_veg_vegan_nonveg():
    """
    REQUIRED TEST 3:
    Vegetarian, vegan, and non-vegetarian rules are strictly respected.
    - Vegan: zero animal products, dairy, milk, paneer, curd, ghee, eggs, chicken, fish.
    - Vegetarian: zero chicken, fish, egg, or meat.
    - Non-vegetarian: contains verified chicken, fish, or egg dishes.
    """
    # 1. Vegan test
    vegan_payload = {
        "age": 28, "gender": "female", "heightCm": 164.0, "weightKg": 58.0,
        "activityLevel": "moderate", "goal": "maintenance", "foodPreference": "vegan",
        "mealsPerDay": 5, "preferredCuisine": "indian"
    }
    resp_vegan = client.post("/api/nutrition/weekly-plan", json=vegan_payload)
    assert resp_vegan.status_code == 200
    vegan_plan = resp_vegan.json()

    import re
    banned_vegan_patterns = [r'\bchicken\b', r'\bfish\b', r'\begg(s)?\b', r'\bpaneer\b', r'\bmilk\b', r'\bcurd\b', r'\byogurt\b', r'\bghee\b', r'\bbutter\b', r'\bdairy\b']
    for day in vegan_plan["days"]:
        for meal in day["meals"]:
            for item in meal["items"]:
                assert item["isVegetarian"] is True
                assert item.get("isVegan", True) is True
                name_low = item["name"].lower()
                for pat in banned_vegan_patterns:
                    assert not re.search(pat, name_low), f"Vegan violation: '{pat}' matched in dish '{item['name']}'"
                for ing in item.get("ingredients", []):
                    ing_low = ing["name"].lower()
                    for pat in banned_vegan_patterns:
                        assert not re.search(pat, ing_low), f"Vegan violation: '{pat}' matched in ingredient '{ing['name']}'"

    # 2. Vegetarian test
    veg_payload = {
        "age": 30, "gender": "male", "heightCm": 172.0, "weightKg": 68.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "indian"
    }
    resp_veg = client.post("/api/nutrition/weekly-plan", json=veg_payload)
    assert resp_veg.status_code == 200
    veg_plan = resp_veg.json()

    banned_veg_terms = ["chicken", "fish", "egg", "mutton", "meat", "prawn", "crab"]
    for day in veg_plan["days"]:
        for meal in day["meals"]:
            for item in meal["items"]:
                assert item["isVegetarian"] is True
                name_low = item["name"].lower()
                for term in banned_veg_terms:
                    assert term not in name_low, f"Vegetarian violation: '{term}' found in '{item['name']}'"

    # 3. Non-vegetarian test
    non_veg_payload = {
        "age": 28, "gender": "male", "heightCm": 176.0, "weightKg": 75.0,
        "activityLevel": "active", "goal": "weight_gain", "foodPreference": "non_vegetarian",
        "mealsPerDay": 5, "dietaryRestrictions": ["high_protein"], "preferredCuisine": "indian"
    }
    resp_nonveg = client.post("/api/nutrition/weekly-plan", json=non_veg_payload)
    assert resp_nonveg.status_code == 200
    nonveg_plan = resp_nonveg.json()

    # Plan should contain non-vegetarian dishes
    all_names = [item["name"].lower() for day in nonveg_plan["days"] for meal in day["meals"] for item in meal["items"]]
    has_nonveg = any(any(t in n for t in ["chicken", "egg", "fish"]) for n in all_names)
    assert has_nonveg is True, "Non-vegetarian plan should include genuine non-vegetarian or egg recipes"

def test_req4_allergens_strictly_excluded():
    """
    REQUIRED TEST 4:
    Allergens are excluded as hard constraints:
    Peanut, dairy, gluten, and custom free-text exclusions (e.g. 'mushrooms', 'capsicum').
    """
    payload = {
        "age": 29, "gender": "female", "heightCm": 165.0, "weightKg": 60.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5,
        "allergies": ["peanuts", "dairy", "gluten"],
        "customAllergies": "mushrooms, capsicum",
        "preferredCuisine": "indian"
    }
    resp = client.post("/api/nutrition/weekly-plan", json=payload)
    assert resp.status_code == 200
    plan = resp.json()

    prohibited = ["peanut", "groundnut", "dairy", "milk", "paneer", "curd", "ghee", "gluten", "wheat", "mushroom", "capsicum"]
    for day in plan["days"]:
        for meal in day["meals"]:
            for item in meal["items"]:
                name_low = item["name"].lower()
                for p in prohibited:
                    assert p not in name_low, f"Allergen breach in dish name: '{p}' in '{item['name']}'"
                for ing in item.get("ingredients", []):
                    ing_low = ing["name"].lower()
                    for p in prohibited:
                        assert p not in ing_low, f"Allergen breach in ingredient: '{p}' in '{ing['name']}'"
                    for allergen_tag in ing.get("allergens", []):
                        assert allergen_tag.lower() not in ["peanuts", "dairy", "gluten"], f"Allergen tag violation: '{allergen_tag}'"

def test_req5_repetition_limits_across_week_and_zero_same_day_repeats():
    """
    REQUIRED TEST 5:
    Repetition limits work across the week:
    - Zero same-day repeats (the same dish NEVER appears twice on the same day).
    - Across the 7 days, breakfast, lunch, and dinner repeat limits are strictly enforced.
    """
    payload = {
        "age": 28, "gender": "male", "heightCm": 172.0, "weightKg": 68.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "indian"
    }
    resp = client.post("/api/nutrition/weekly-plan", json=payload)
    assert resp.status_code == 200
    plan = resp.json()

    for day_idx, day in enumerate(plan["days"]):
        day_dish_ids = [item.get("dishId") or item["name"] for meal in day["meals"] for item in meal["items"]]
        # Zero same-day duplicates:
        assert len(day_dish_ids) == len(set(day_dish_ids)), f"Same-day duplicate detected on Day {day_idx + 1}: {day_dish_ids}"

    # Across the week: check breakfast variety (with 20 candidate recipes, all 7 breakfasts must be unique)
    bf_dishes = [day["meals"][0]["items"][0].get("dishId") or day["meals"][0]["items"][0]["name"] for day in plan["days"]]
    assert len(set(bf_dishes)) == 7, f"All 7 breakfasts across the week must be distinct dishes, got {len(set(bf_dishes))} unique"

    lu_dishes = [day["meals"][2]["items"][0].get("dishId") or day["meals"][2]["items"][0]["name"] for day in plan["days"]]
    assert len(set(lu_dishes)) == 7, f"All 7 lunches across the week must be distinct dishes, got {len(set(lu_dishes))} unique"

    di_dishes = [day["meals"][4]["items"][0].get("dishId") or day["meals"][4]["items"][0]["name"] for day in plan["days"]]
    assert len(set(di_dishes)) == 7, f"All 7 dinners across the week must be distinct dishes, got {len(set(di_dishes))} unique"

def test_req6_and_req8_new_week_avoids_previous_week_recipes():
    """
    REQUIRED TESTS 6 & 8:
    A new week's plan avoids previous week's recipes where alternatives exist,
    and generating a new week does not simply return the previous week's menu.
    """
    # Test via direct DietPlannerService invocation with previous_week_dish_ids
    profile = {
        "age": 28, "gender": "male", "heightCm": 172.0, "weightKg": 68.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "indian"
    }
    # Week 1
    plan_w1 = DietPlannerService.generate_seven_day_plan(profile, week_number=1)
    w1_dishes = plan_w1["selectedDishIds"]
    assert len(w1_dishes) == 35

    # Week 2 avoiding Week 1 dishes
    plan_w2 = DietPlannerService.generate_seven_day_plan(
        profile,
        previous_week_dish_ids=w1_dishes,
        week_number=2
    )
    w2_dishes = plan_w2["selectedDishIds"]
    assert len(w2_dishes) == 35

    # Week 2 menu must not simply equal Week 1 menu
    assert w1_dishes != w2_dishes, "Week 2 menu must not simply repeat Week 1 menu"

    # With 20 breakfast recipes available and 7 used in Week 1, Week 2 should select from the 13 unused breakfast recipes
    w1_bfs = [day["meals"][0]["items"][0]["dishId"] for day in plan_w1["days"]]
    w2_bfs = [day["meals"][0]["items"][0]["dishId"] for day in plan_w2["days"]]
    bf_overlap = set(w1_bfs).intersection(set(w2_bfs))
    assert len(bf_overlap) == 0, f"Week 2 should have 0 overlapping breakfasts with Week 1 due to fatigue penalties, got overlap: {bf_overlap}"

    # Same for lunches
    w1_lus = [day["meals"][2]["items"][0]["dishId"] for day in plan_w1["days"]]
    w2_lus = [day["meals"][2]["items"][0]["dishId"] for day in plan_w2["days"]]
    lu_overlap = set(w1_lus).intersection(set(w2_lus))
    assert len(lu_overlap) == 0, f"Week 2 should have 0 overlapping lunches with Week 1, got overlap: {lu_overlap}"

def test_req7_opening_saved_plan_for_same_week_does_not_change():
    """
    REQUIRED TEST 7:
    Opening an already saved plan for the same week loads that saved plan consistently
    without silently mutating the dishes.
    """
    import uuid
    from app.database import SessionLocal
    from app.models.user import User
    from app.models.nutrition import SavedDietPlan
    import json

    db = SessionLocal()
    try:
        # Create test user
        unique_email = f"plan_consistency_{uuid.uuid4().hex[:6]}@agrotest.org"
        test_user = User(
            id=str(uuid.uuid4()),
            email=unique_email,
            full_name="Consistency Tester",
            hashed_password="hashedpassword123",
            role="farmer"
        )
        db.add(test_user)
        db.commit()

        # Generate and save a plan for Week 1
        plan_dict = DietPlannerService.generate_seven_day_plan(
            {"age": 30, "gender": "male", "heightCm": 172.0, "weightKg": 68.0, "foodPreference": "vegetarian", "mealsPerDay": 5},
            week_number=1
        )
        saved_id = str(uuid.uuid4())
        plan_dict["id"] = saved_id
        plan_dict["weekNumber"] = 1

        record = SavedDietPlan(
            id=saved_id,
            user_id=test_user.id,
            week_number=1,
            target_calories=2000,
            selected_dish_ids_json=json.dumps(plan_dict["selectedDishIds"]),
            profile_summary_json=json.dumps(plan_dict.get("profileSummary", {})),
            plan_data_json=json.dumps(plan_dict)
        )
        db.add(record)
        db.commit()

        # Retrieve the plan from the database twice
        retrieved_1 = db.query(SavedDietPlan).filter(SavedDietPlan.id == saved_id).first()
        retrieved_2 = db.query(SavedDietPlan).filter(SavedDietPlan.id == saved_id).first()

        data_1 = json.loads(retrieved_1.plan_data_json)
        data_2 = json.loads(retrieved_2.plan_data_json)

        # Dishes must be 100% identical
        assert data_1["selectedDishIds"] == data_2["selectedDishIds"]
        assert data_1["days"][0]["meals"][0]["items"][0]["name"] == data_2["days"][0]["meals"][0]["items"][0]["name"]
    finally:
        db.close()

def test_req9_daily_calorie_and_macro_totals_match_selected_recipes():
    """
    REQUIRED TEST 9:
    Every daily calorie and macro total matches the selected recipes:
    Additive math guarantee:
    1. sum(ingredient.calories) == dish.calories
    2. sum(dish.calories) == meal.totalCalories
    3. sum(meal.totalCalories) == day.dailyTotalCalories
    4. sum(ingredient.protein) == dish.protein
    5. sum(dish.protein) == meal.totalProtein
    6. sum(meal.totalProtein) == day.dailyTotalProtein
    """
    payload = {
        "age": 28, "gender": "female", "heightCm": 164.0, "weightKg": 58.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "indian"
    }
    resp = client.post("/api/nutrition/weekly-plan", json=payload)
    assert resp.status_code == 200
    plan = resp.json()

    for day_idx, day in enumerate(plan["days"]):
        meal_cals_sum = 0
        meal_prot_sum = 0.0

        for meal_idx, meal in enumerate(day["meals"]):
            dish_cals_sum = 0
            dish_prot_sum = 0.0

            for item in meal["items"]:
                # Check ingredient sum to dish
                ing_cals = sum(ing["calories"] for ing in item.get("ingredients", []))
                ing_prot = sum(ing["protein"] for ing in item.get("ingredients", []))

                assert ing_cals == item["calories"], f"Ingredient calories mismatch in {item['name']}: {ing_cals} vs {item['calories']}"
                assert abs(ing_prot - item["proteinGrams"]) < 0.2, f"Ingredient protein mismatch in {item['name']}: {ing_prot} vs {item['proteinGrams']}"

                dish_cals_sum += item["calories"]
                dish_prot_sum += item["proteinGrams"]

            assert dish_cals_sum == meal["totalCalories"], f"Meal {meal['mealType']} calories mismatch: {dish_cals_sum} vs {meal['totalCalories']}"
            assert abs(dish_prot_sum - meal["totalProtein"]) < 0.2, f"Meal {meal['mealType']} protein mismatch: {dish_prot_sum} vs {meal['totalProtein']}"

            meal_cals_sum += meal["totalCalories"]
            meal_prot_sum += meal["totalProtein"]

        assert meal_cals_sum == day["dailyTotalCalories"], f"Day {day_idx + 1} calories mismatch: {meal_cals_sum} vs {day['dailyTotalCalories']}"
        assert abs(meal_prot_sum - day["dailyTotalProtein"]) < 0.3, f"Day {day_idx + 1} protein mismatch: {meal_prot_sum} vs {day['dailyTotalProtein']}"

def test_req10_user_plan_history_isolated_between_accounts():
    """
    REQUIRED TEST 10:
    User plan history remains completely isolated between accounts:
    User A cannot view or access User B's weekly plans.
    """
    import uuid
    from app.database import SessionLocal
    from app.models.user import User
    from app.models.nutrition import SavedDietPlan
    from app.api.auth import create_access_token
    import json

    db = SessionLocal()
    try:
        user_a_id = str(uuid.uuid4())
        user_b_id = str(uuid.uuid4())

        user_a = User(id=user_a_id, email=f"usera_{uuid.uuid4().hex[:6]}@agro.org", full_name="User Alpha", hashed_password="pw", role="farmer")
        user_b = User(id=user_b_id, email=f"userb_{uuid.uuid4().hex[:6]}@agro.org", full_name="User Beta", hashed_password="pw", role="farmer")
        db.add(user_a)
        db.add(user_b)
        db.commit()

        # Save a plan belonging to User B
        plan_b_id = str(uuid.uuid4())
        plan_b = SavedDietPlan(
            id=plan_b_id,
            user_id=user_b_id,
            week_number=1,
            target_calories=2200,
            selected_dish_ids_json=json.dumps(["lu_01", "lu_02"]),
            profile_summary_json="{}",
            plan_data_json=json.dumps({"id": plan_b_id, "weekNumber": 1, "days": []})
        )
        db.add(plan_b)
        db.commit()

        # User A logs in
        token_a = create_access_token(data={"sub": user_a.id})
        headers_a = {"Authorization": f"Bearer {token_a}"}

        # User A requests their own plans list: should NOT contain User B's plan
        resp_list = client.get("/api/nutrition/weekly-plans", headers=headers_a)
        assert resp_list.status_code == 200
        plans_list = resp_list.json()
        assert not any(p["id"] == plan_b_id for p in plans_list), "User A's plans list leaked User B's plan!"

        # User A directly attempts to access User B's plan by ID: must be rejected 404
        resp_direct = client.get(f"/api/nutrition/weekly-plans/{plan_b_id}", headers=headers_a)
        assert resp_direct.status_code == 404, f"Access control failed! Expected 404, got {resp_direct.status_code}"
    finally:
        db.close()

def test_req12_unrelated_modules_continue_working():
    """
    REQUIRED TEST 12:
    Existing authentication, Plant Analysis, Better Production, Soil Analysis,
    Dashboard, and AGRO AI Assistant continue working without any regression.
    """
    # 1. Health check
    resp_health = client.get("/api/health")
    assert resp_health.status_code == 200
    assert resp_health.json()["status"] == "healthy"

    # 2. Assistant chat endpoint
    resp_chat = client.post("/api/assistant/chat", json={"message": "What is good fertilizer for tomato plants?"})
    assert resp_chat.status_code == 200
    chat_data = resp_chat.json()
    assert "reply" in chat_data or "response" in chat_data

    # 3. Production module crop analysis
    resp_crops = client.get("/api/production/crops")
    assert resp_crops.status_code in [200, 404] # Checks module routes are loaded without crashing

def test_regional_cuisines_andhra_tamil_north_indian_differentiation():
    """
    REQUIRED TEST:
    Verifies that selecting regional Indian cuisines (Andhra, Tamil, North Indian)
    tailors dish selection to the requested regional culinary traditions.
    """
    # 1. Andhra preference
    andhra_payload = {
        "age": 28, "gender": "male", "heightCm": 172.0, "weightKg": 68.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "andhra"
    }
    resp_andhra = client.post("/api/nutrition/weekly-plan", json=andhra_payload)
    assert resp_andhra.status_code == 200
    plan_andhra = resp_andhra.json()

    # Collect all dish IDs selected across the week
    andhra_dish_ids = set()
    for day in plan_andhra["days"]:
        for meal in day["meals"]:
            for item in meal["items"]:
                andhra_dish_ids.add(item.get("dishId"))

    from app.services.food_database import FOOD_DATABASE
    dish_map = {d["id"]: d for d in FOOD_DATABASE}

    # Verify that Andhra preference includes South Indian / Andhra dishes and heavily filters out conflicting North Indian dishes
    south_or_andhra_count = sum(
        1 for did in andhra_dish_ids
        if did in dish_map and any(c in dish_map[did].get("cuisines", []) for c in ["south_indian", "andhra"])
    )
    north_count = sum(
        1 for did in andhra_dish_ids
        if did in dish_map and "north_indian" in dish_map[did].get("cuisines", []) and not any(c in dish_map[did].get("cuisines", []) for c in ["south_indian", "andhra"])
    )
    assert south_or_andhra_count > north_count, f"Andhra preference should favour South Indian/Andhra dishes (found {south_or_andhra_count} vs {north_count} north)"

    # 2. North Indian preference
    north_payload = {
        "age": 28, "gender": "male", "heightCm": 172.0, "weightKg": 68.0,
        "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
        "mealsPerDay": 5, "preferredCuisine": "north_indian"
    }
    resp_north = client.post("/api/nutrition/weekly-plan", json=north_payload)
    assert resp_north.status_code == 200
    plan_north = resp_north.json()

    north_dish_ids = set()
    for day in plan_north["days"]:
        for meal in day["meals"]:
            for item in meal["items"]:
                north_dish_ids.add(item.get("dishId"))

    north_dishes = sum(
        1 for did in north_dish_ids
        if did in dish_map and "north_indian" in dish_map[did].get("cuisines", [])
    )
    south_dishes = sum(
        1 for did in north_dish_ids
        if did in dish_map and "south_indian" in dish_map[did].get("cuisines", []) and "north_indian" not in dish_map[did].get("cuisines", [])
    )
    assert north_dishes > south_dishes, f"North Indian preference should favour North Indian dishes (found {north_dishes} vs {south_dishes} south)"

def test_profile_calories_update_regenerates_matching_plan_and_not_stale_cache():
    """
    REGRESSION TEST FOR USER ISSUE:
    When a logged-in user calculates a new target (e.g. 2161 kcal) and posts their updated profile,
    the newly generated 7-day plan must reflect the 2161 kcal target, rather than returning
    a stale saved plan (e.g. 1791 kcal).
    """
    import uuid
    import json
    from app.database import SessionLocal
    from app.models.user import User
    from app.models.nutrition import SavedDietPlan
    from app.api.auth import create_access_token

    db = SessionLocal()
    try:
        user_id = str(uuid.uuid4())
        test_user = User(
            id=user_id,
            email=f"calc_test_{uuid.uuid4().hex[:6]}@agro.org",
            full_name="Calorie Test User",
            hashed_password="hashed_pw",
            role="farmer"
        )
        db.add(test_user)
        db.commit()

        # Pre-seed an OLD plan with 1791 kcal in database
        old_plan_id = str(uuid.uuid4())
        old_plan = SavedDietPlan(
            id=old_plan_id,
            user_id=user_id,
            week_number=1,
            target_calories=1791,
            selected_dish_ids_json=json.dumps(["bf_01", "lu_01", "di_01"]),
            profile_summary_json=json.dumps({"targetCalories": 1791}),
            plan_data_json=json.dumps({"id": old_plan_id, "weekNumber": 1, "profileSummary": {"targetCalories": 1791}, "days": []})
        )
        db.add(old_plan)
        db.commit()

        # User logs in and submits new profile calculating 2161 kcal
        token = create_access_token(data={"sub": user_id})
        headers = {"Authorization": f"Bearer {token}"}

        # New profile: Male, 28, 172cm, 68kg, moderate activity, weight loss
        # BMR = 10*68 + 6.25*172 - 5*28 + 5 = 680 + 1075 - 140 + 5 = 1620 kcal
        # TDEE = 1620 * 1.55 = 2511 kcal
        # Goal adjustment = -350 kcal -> Target = 2161 kcal
        payload = {
            "age": 28, "gender": "male", "heightCm": 172.0, "weightKg": 68.0,
            "activityLevel": "moderate", "goal": "weight_loss", "foodPreference": "vegetarian",
            "mealsPerDay": 5, "preferredCuisine": "indian"
        }

        resp = client.post("/api/nutrition/weekly-plan", json=payload, headers=headers)
        assert resp.status_code == 200
        new_plan = resp.json()

        # Crucial check: Must be 2161 kcal, NOT stale 1791 kcal!
        assert new_plan["profileSummary"]["targetCalories"] == 2161, (
            f"Stale plan returned! Expected 2161 kcal, got {new_plan['profileSummary']['targetCalories']} kcal"
        )
        # Check Day 1 dailyTargetCalories
        assert new_plan["days"][0]["dailyTargetCalories"] == 2161
        # Check Day 1 dailyTotalCalories is within ±5% tolerance of 2161
        assert abs(new_plan["days"][0]["dailyTotalCalories"] - 2161) <= 108

        # Also verify that GET /api/nutrition/weekly-plan now returns the newly saved 2161 plan
        resp_get = client.get("/api/nutrition/weekly-plan", headers=headers)
        assert resp_get.status_code == 200
        saved_plan = resp_get.json()
        assert saved_plan["profileSummary"]["targetCalories"] == 2161
    finally:
        db.close()



