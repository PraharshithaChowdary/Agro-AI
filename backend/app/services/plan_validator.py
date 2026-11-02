"""
AGRO AI — Post-Generation Diet Plan Validator
Performs exhaustive secondary verification on every generated plan to ensure:
1. Absolute compliance with allergen exclusions, custom free-text exclusions, and dietary rules.
2. Exact arithmetic consistency: sum(ingredients) == item == sum(items) == meal == sum(meals) == day.
"""

from typing import Dict, Any, List
from app.services.allergy_filter_service import AllergyFilterService

class PlanValidatorService:
    @staticmethod
    def validate_plan_compliance_and_math(
        plan: Dict[str, Any],
        food_preference: str,
        allergies: List[str],
        custom_allergies_text: str = "",
        intolerances: List[str] = None,
        dietary_focus: List[str] = None
    ) -> bool:
        """
        Validates the entire 7-day diet plan after generation.
        Raises ValueError if any leak or arithmetic discrepancy is detected.
        """
        if intolerances is None:
            intolerances = []
        if dietary_focus is None:
            dietary_focus = []

        days = plan.get("days", [])
        if not days or len(days) != 7:
            raise ValueError(f"Plan validation failed: expected exactly 7 days, got {len(days)}.")

        for day in days:
            day_num = day.get("dayNumber")
            meals = day.get("meals", [])
            if not meals:
                raise ValueError(f"Plan validation failed: Day {day_num} has no meals.")

            computed_day_calories = 0
            computed_day_protein = 0.0
            computed_day_carbs = 0.0
            computed_day_fat = 0.0
            computed_day_fibre = 0.0

            for meal in meals:
                meal_type = meal.get("mealType")
                items = meal.get("items", [])
                if not items:
                    raise ValueError(f"Plan validation failed: Day {day_num} {meal_type} has no items.")

                computed_meal_calories = 0
                computed_meal_protein = 0.0
                computed_meal_carbs = 0.0
                computed_meal_fat = 0.0
                computed_meal_fibre = 0.0

                for item in items:
                    # 1. Check food safety compliance at item and ingredient level
                    compliant, reason = AllergyFilterService.is_food_compliant(
                        food=item,
                        food_preference=food_preference,
                        allergies=allergies,
                        custom_allergies_text=custom_allergies_text,
                        intolerances=intolerances,
                        dietary_focus=dietary_focus
                    )
                    if not compliant:
                        raise ValueError(
                            f"Safety validation failure on Day {day_num} [{meal_type}]: {reason}"
                        )

                    # 2. Check item-to-ingredient math
                    ingredients = item.get("ingredients", [])
                    if ingredients:
                        ing_cal_sum = sum(ing["calories"] for ing in ingredients)
                        if ing_cal_sum != item["calories"]:
                            raise ValueError(
                                f"Arithmetic discrepancy in item '{item['name']}': "
                                f"ingredient sum ({ing_cal_sum} kcal) does not match item calories ({item['calories']} kcal)."
                            )

                    computed_meal_calories += item["calories"]
                    computed_meal_protein += item.get("proteinGrams", 0.0)
                    computed_meal_carbs += item.get("carbsGrams", 0.0)
                    computed_meal_fat += item.get("fatGrams", 0.0)
                    computed_meal_fibre += item.get("fibreGrams", 0.0)

                # Verify meal sum matches
                if meal.get("totalCalories") != computed_meal_calories:
                    raise ValueError(
                        f"Arithmetic discrepancy in Day {day_num} [{meal_type}]: "
                        f"items sum ({computed_meal_calories} kcal) does not match meal.totalCalories ({meal.get('totalCalories')} kcal)."
                    )

                computed_day_calories += computed_meal_calories
                computed_day_protein += computed_meal_protein
                computed_day_carbs += computed_meal_carbs
                computed_day_fat += computed_meal_fat
                computed_day_fibre += computed_meal_fibre

            # Verify day sum matches
            if day.get("dailyTotalCalories") != computed_day_calories:
                raise ValueError(
                    f"Arithmetic discrepancy in Day {day_num}: "
                    f"meals sum ({computed_day_calories} kcal) does not match day.dailyTotalCalories ({day.get('dailyTotalCalories')} kcal)."
                )

        return True
