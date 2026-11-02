"""
AGRO AI — Scientific Nutrition & Metabolic Calculator Service
Based on the Mifflin-St Jeor Equation, WHO BMI standards, and ICMR-NIN guidelines.
"""

from typing import Dict, Any, List, Optional

class NutritionCalculatorService:
    @staticmethod
    def calculate_metrics(
        age: int,
        gender: str,
        height_cm: float,
        weight_kg: float,
        activity_level: str,
        goal: str,
        goal_weight_kg: Optional[float] = None,
        meals_per_day: int = 5,
        target_timeline_weeks: Optional[int] = None,
        dietary_focus: Optional[List[str]] = None,
        food_preference: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculates validated BMR, TDEE, individualized calorie target, macronutrients,
        per-meal allocations, and medical safety flags.
        """
        dietary_focus = [d.lower().strip() for d in (dietary_focus or [])]
        food_preference = (food_preference or "").lower().strip()
        gender_norm = gender.lower().strip()
        goal_norm = goal.lower().strip()

        # ---------------------------------------------------------------------
        # 1. Validation & Input Sanitization
        # ---------------------------------------------------------------------
        if age < 10 or age > 120:
            raise ValueError(f"Age must be between 10 and 120 years. Received: {age}")
        if height_cm < 70 or height_cm > 260:
            raise ValueError(f"Height must be between 70 cm and 260 cm. Received: {height_cm}")
        if weight_kg < 25 or weight_kg > 300:
            raise ValueError(f"Weight must be between 25 kg and 300 kg. Received: {weight_kg}")
        if meals_per_day < 3 or meals_per_day > 6:
            raise ValueError(f"Meals per day must be between 3 and 6. Received: {meals_per_day}")

        # ---------------------------------------------------------------------
        # 2. BMI Calculation (WHO / ICMR-NIN Standards)
        # ---------------------------------------------------------------------
        height_m = height_cm / 100.0
        bmi = weight_kg / (height_m * height_m)

        if bmi < 18.5:
            bmi_category = "Underweight"
        elif bmi < 25.0:
            bmi_category = "Normal weight"
        elif bmi < 30.0:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obesity"

        # ---------------------------------------------------------------------
        # 3. Resting Metabolic Rate / BMR (Mifflin-St Jeor Equation)
        # Men: (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5
        # Women: (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) - 161
        # ---------------------------------------------------------------------
        if gender_norm == "male":
            bmr = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) + 5.0
            min_safe_floor = 1500
        else:
            bmr = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) - 161.0
            min_safe_floor = 1200

        # ---------------------------------------------------------------------
        # 4. Estimated Total Daily Energy Expenditure (TDEE) via Activity Multiplier
        # ---------------------------------------------------------------------
        activity_multipliers = {
            "sedentary": 1.20,     # Desk job, little or no exercise
            "light": 1.375,        # 1-3 days light exercise/walking
            "moderate": 1.55,      # 3-5 days moderate aerobic/resistance training
            "active": 1.725,       # 6-7 days vigorous exercise/athletics
            "very_active": 1.90,   # Physical labour / 2x daily intense sports training
        }
        multiplier = activity_multipliers.get(activity_level.lower().strip(), 1.55)
        tdee = bmr * multiplier

        # ---------------------------------------------------------------------
        # 5. Clinical Safety Warnings & Special Safeguards
        # ---------------------------------------------------------------------
        safety_warnings: List[str] = []
        incompatible_notices: List[str] = []

        if age < 18:
            safety_warnings.append(
                "Adolescent Nutrition Safeguard: Users under 18 years have elevated growth, skeletal mineralization, and micronutrient requirements. Equation-based caloric restriction is not recommended without pediatrician or pediatric dietitian oversight."
            )

        if "pregnancy_breastfeeding" in dietary_focus:
            safety_warnings.append(
                "Maternal Health Guidance: Energy restriction is clinically contraindicated during pregnancy and active lactation. Maternal nutrition requires an additional 300–500 kcal/day and targeted micronutrient supplementation (folate, iron, calcium, choline) under obstetric guidance."
            )

        if "diabetic_friendly" in dietary_focus:
            safety_warnings.append(
                "Glycemic Management Notice: Carbohydrates in this plan emphasize low glycemic index legumes, whole millets, and high soluble fibre. Medication dosages (such as insulin or sulfonylureas) must be coordinated with your healthcare provider."
            )

        if bmi >= 35.0:
            safety_warnings.append(
                "Clinical Assessment Notice: Your BMI falls into Class II/III Obesity. A comprehensive multidisciplinary metabolic evaluation by a physician or registered clinical dietitian is strongly encouraged."
            )

        # Goal weight validation
        if goal_weight_kg is not None:
            if goal_weight_kg < 25 or goal_weight_kg > 300:
                raise ValueError(f"Goal weight must be between 25 kg and 300 kg. Received: {goal_weight_kg}")

            target_bmi = goal_weight_kg / (height_m * height_m)
            if target_bmi < 18.5:
                safety_warnings.append(
                    f"Target Weight Warning: Your specified goal weight of {goal_weight_kg}kg results in an Underweight BMI ({target_bmi:.1f}). Caloric restriction towards an underweight status is medically contraindicated."
                )

            if goal_norm in ["weight_loss", "loss"] and goal_weight_kg >= weight_kg:
                safety_warnings.append(
                    f"Goal Notice: You selected 'Weight Loss', but your target weight ({goal_weight_kg}kg) is greater than or equal to current weight ({weight_kg}kg)."
                )

            if goal_norm in ["weight_gain", "gain"] and goal_weight_kg <= weight_kg:
                safety_warnings.append(
                    f"Goal Notice: You selected 'Weight Gain', but your target weight ({goal_weight_kg}kg) is less than or equal to current weight ({weight_kg}kg)."
                )

        # Incompatibility checks
        if food_preference == "vegan" and any(x in dietary_focus for x in ["eggetarian", "pescatarian"]):
            incompatible_notices.append(
                "Dietary conflict: Vegan preference selected alongside Eggetarian or Pescatarian focus. Vegan rules strictly take precedence (100% plant-based, zero animal products)."
            )

        # ---------------------------------------------------------------------
        # 6. Individualized Goal Caloric Target (Conservative Evidence-Based Math)
        # ---------------------------------------------------------------------
        if goal_norm in ["weight_loss", "loss"]:
            if bmi < 18.5:
                safety_warnings.append(
                    "Clinical Safety Alert: Your current BMI classifies as Underweight (<18.5). Active calorie deficits are medically contraindicated. Your caloric target has been automatically protected at full maintenance."
                )
                target_calories = int(round(tdee))
            else:
                # Moderate individualized deficit (15% to 20% of TDEE)
                if bmi >= 30.0:
                    deficit_percent = 0.20
                    max_deficit = 500
                elif bmi >= 25.0:
                    deficit_percent = 0.18
                    max_deficit = 450
                else:
                    deficit_percent = 0.15
                    max_deficit = 350

                raw_deficit = min(tdee * deficit_percent, max_deficit)
                target_calories = int(round(max(min_safe_floor, tdee - raw_deficit)))

        elif goal_norm in ["weight_gain", "gain"]:
            # Progressive surplus (12% to 14% of TDEE) supporting lean tissue accretion
            surplus_percent = 0.13
            raw_surplus = min(tdee * surplus_percent, 450)
            target_calories = int(round(tdee + raw_surplus))

        else:
            # Maintenance / General Healthy Eating
            target_calories = int(round(tdee))

        # ---------------------------------------------------------------------
        # 7. Macronutrient Distribution with Exact Calorie Reconciliation
        # ---------------------------------------------------------------------
        # Protein: 1.6 to 2.0g per kg body weight depending on goal and activity
        if goal_norm in ["weight_loss", "loss"]:
            protein_factor = 2.0 if activity_level in ["active", "very_active"] else 1.8
        elif goal_norm in ["weight_gain", "gain"]:
            protein_factor = 1.9
        else:
            protein_factor = 1.6

        target_protein = int(round(max(55, min(220, weight_kg * protein_factor))))
        protein_cals = target_protein * 4

        # Fat: 24% - 28% of total calories (9 kcal/g)
        target_fat = int(round(max(35, min(110, (target_calories * 0.25) / 9.0))))
        fat_cals = target_fat * 9

        # Carbohydrates: Remaining calories (4 kcal/g)
        remaining_cals = max(0, target_calories - protein_cals - fat_cals)
        target_carbs = max(40, int(round(remaining_cals / 4.0)))

        # Exact Reconciliation: ensure protein*4 + carbs*4 + fat*9 == target_calories within <= 4 kcal tolerance
        macro_sum_cals = (target_protein * 4) + (target_carbs * 4) + (target_fat * 9)
        cals_diff = target_calories - macro_sum_cals
        if abs(cals_diff) > 0:
            target_carbs += int(round(cals_diff / 4.0))

        # Dietary Fibre Target: 14g per 1000 kcal (ICMR-NIN & WHO standard)
        target_fibre = int(round(max(30, (target_calories / 1000.0) * 14.0)))

        # ---------------------------------------------------------------------
        # 8. Per-Meal Calorie Budgets (Guaranteed sum(meals) == target_calories)
        # ---------------------------------------------------------------------
        if meals_per_day == 3:
            b_cals = int(round(target_calories * 0.30))
            d_cals = int(round(target_calories * 0.30))
            l_cals = target_calories - b_cals - d_cals
            meal_allocations = {
                "Breakfast": b_cals,
                "Lunch": l_cals,
                "Dinner": d_cals
            }
        elif meals_per_day == 4:
            b_cals = int(round(target_calories * 0.25))
            e_cals = int(round(target_calories * 0.15))
            d_cals = int(round(target_calories * 0.25))
            l_cals = target_calories - b_cals - e_cals - d_cals
            meal_allocations = {
                "Breakfast": b_cals,
                "Lunch": l_cals,
                "Evening Snack": e_cals,
                "Dinner": d_cals
            }
        elif meals_per_day == 6:
            b_cals = int(round(target_calories * 0.20))
            mm_cals = int(round(target_calories * 0.10))
            af_cals = int(round(target_calories * 0.10))
            ev_cals = int(round(target_calories * 0.10))
            di_cals = int(round(target_calories * 0.20))
            lu_cals = target_calories - (b_cals + mm_cals + af_cals + ev_cals + di_cals)
            meal_allocations = {
                "Breakfast": b_cals,
                "Mid-morning Snack": mm_cals,
                "Lunch": lu_cals,
                "Afternoon Snack": af_cals,
                "Evening Snack": ev_cals,
                "Dinner": di_cals
            }
        else:
            # Standard 5 meals
            b_cals = int(round(target_calories * 0.25))
            mm_cals = int(round(target_calories * 0.10))
            ev_cals = int(round(target_calories * 0.10))
            di_cals = int(round(target_calories * 0.20))
            lu_cals = target_calories - (b_cals + mm_cals + ev_cals + di_cals)
            meal_allocations = {
                "Breakfast": b_cals,
                "Mid-morning Snack": mm_cals,
                "Lunch": lu_cals,
                "Evening Snack": ev_cals,
                "Dinner": di_cals
            }

        return {
            "bmi": round(bmi, 2),
            "bmiCategory": bmi_category,
            "bmr": round(bmr, 1),
            "tdee": round(tdee, 1),
            "goalAdjustmentCalories": target_calories - int(round(tdee)),
            "goal": goal,
            "targetCalories": target_calories,
            "targetProteinGrams": target_protein,
            "targetCarbsGrams": target_carbs,
            "targetFatGrams": target_fat,
            "targetFibreGrams": target_fibre,
            "mealsPerDay": meals_per_day,
            "mealCalorieTargets": meal_allocations,
            "formulaUsed": "Mifflin-St Jeor Equation, WHO BMI Guidelines & ICMR-NIN RDA",
            "safetyWarnings": safety_warnings,
            "incompatibleNotices": incompatible_notices,
            "disclaimer": (
                "Estimated Energy Expenditure Notice: Resting metabolic rate and TDEE are mathematical population estimates derived from the Mifflin-St Jeor equation. "
                "Individual measured metabolic rate varies with lean tissue mass, thyroid hormone kinetics, ambient temperature, and gut microbiome activity. "
                "These targets provide structured evidence-based baselines for lifestyle nutrition and should be calibrated with real-world biometric tracking."
            )
        }
