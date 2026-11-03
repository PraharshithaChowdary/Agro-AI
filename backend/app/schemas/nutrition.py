from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class NutritionProfileInputSchema(BaseModel):
    age: int = Field(..., ge=10, le=120, description="Age in years")
    gender: str = Field(..., pattern="^(male|female)$", description="Biological sex for metabolic equations")
    heightCm: float = Field(..., ge=70.0, le=260.0, description="Height in centimetres")
    weightKg: float = Field(..., ge=25.0, le=300.0, description="Current weight in kilograms")
    goalWeightKg: Optional[float] = Field(None, ge=25.0, le=300.0, description="Target weight in kilograms")
    activityLevel: str = Field(..., pattern="^(sedentary|light|moderate|active|very_active)$")
    goal: str = Field(..., pattern="^(weight_loss|maintenance|weight_gain|healthy_eating)$")
    foodPreference: str = Field(..., pattern="^(vegetarian|non_vegetarian|vegan|eggetarian|pescatarian|jain)$")
    mealsPerDay: int = Field(default=5, ge=3, le=6, description="Number of daily meals")
    targetTimelineWeeks: Optional[int] = Field(default=None, ge=1, le=52, description="Target timeline in weeks")
    allergies: List[str] = Field(default_factory=list, description="Predefined allergen identifiers")
    customAllergies: str = Field(default="", description="Free-text custom allergies or ingredients to avoid")
    intolerances: List[str] = Field(default_factory=list, description="Intolerances e.g. lactose, fructose")
    dislikedFoods: str = Field(default="", description="Free-text disliked foods or ingredients to minimize")
    dietaryRestrictions: List[str] = Field(default_factory=list, description="Special Dietary Focus tags")
    preferredCuisine: str = Field(default="indian")
    budgetTier: str = Field(default="moderate", pattern="^(budget_friendly|moderate|premium)$")
    cookingTimePref: str = Field(default="moderate", pattern="^(quick_easy|moderate|elaborate)$")
    variationSeed: Optional[int] = Field(default=0, description="Deterministic seed for recipe rotation/regeneration")
    generateNewWeek: Optional[bool] = Field(default=False, description="Flag indicating user explicitly requests next week's plan")
    weekNumber: Optional[int] = Field(default=None, description="Requested week index (e.g. 1, 2, 3...)")
    weekStartDate: Optional[str] = Field(default=None, description="Starting date of the week in YYYY-MM-DD format")

class NutritionCalculationOut(BaseModel):
    bmi: float
    bmiCategory: str
    bmr: float
    tdee: float
    goalAdjustmentCalories: int = 0
    targetCalories: int
    targetProteinGrams: int
    targetCarbsGrams: int
    targetFatGrams: int
    targetFibreGrams: int = 35
    mealsPerDay: int = 5
    mealCalorieTargets: Dict[str, int] = {}
    formulaUsed: str
    safetyWarnings: List[str] = []
    incompatibleNotices: List[str] = []
    disclaimer: str

class IngredientSchema(BaseModel):
    name: str
    quantityGrams: float
    measure: str
    calories: int
    protein: float
    carbs: float
    fat: float
    fibre: float = 0.0
    calcium_mg: float = 0.0
    iron_mg: float = 0.0
    allergens: List[str] = []
    source: str = "IFCT 2017"
    verification_status: str = "verified"

class FoodItemSchema(BaseModel):
    name: str
    portion: str
    calories: int
    proteinGrams: float
    carbsGrams: float
    fatGrams: float
    fibreGrams: float = 0.0
    category: str
    isVegetarian: bool
    isVegan: bool = False
    allergens: List[str] = []
    ingredients: List[IngredientSchema] = []
    preparationInstructions: str = ""
    goalFitReason: str = ""
    cuisine: str = "Indian"
    dishId: Optional[str] = None

class MealSchema(BaseModel):
    mealType: str
    timeSuggestion: str
    items: List[FoodItemSchema]
    totalCalories: int
    totalProtein: float
    totalCarbs: float = 0.0
    totalFat: float = 0.0
    totalFibre: float = 0.0

class DailyDietPlanSchema(BaseModel):
    dayNumber: int
    dayName: str
    meals: List[MealSchema]
    dailyTargetCalories: int
    dailyTotalCalories: int
    calorieDifference: int = 0
    calorieDifferencePercent: float = 0.0
    isWithinTolerance: bool = True
    dailyTotalProtein: float
    dailyTotalCarbs: float
    dailyTotalFat: float
    dailyTotalFibre: float = 0.0
    hydrationTip: str
    macroReconciliation: Optional[Dict[str, Any]] = None

class FoodRecommendationItem(BaseModel):
    group: str
    items: List[str]
    rationale: str

class FoodAvoidanceItem(BaseModel):
    item: str
    reason: str
    category: str

class FoodSubstitutionItem(BaseModel):
    original: str
    substitute: str
    benefit: str

class NutritionalGuidanceSchema(BaseModel):
    foodsToEat: List[FoodRecommendationItem] = []
    foodsToAvoid: List[FoodAvoidanceItem] = []
    foodsToLimit: List[FoodRecommendationItem] = []
    safeSubstitutions: List[FoodSubstitutionItem] = []
    timingAndPortionTips: List[str] = []

class ProfileSummarySchema(BaseModel):
    bmi: float
    bmiCategory: str
    bmr: float
    tdee: float
    goalAdjustmentCalories: int = 0
    targetCalories: int
    targetProtein: float
    targetCarbs: float
    targetFat: float
    targetFibre: float
    goal: str
    foodPreference: str
    mealsPerDay: int = 5
    allergies: List[str] = []
    customAllergies: str = ""
    intolerances: List[str] = []
    dislikedFoods: str = ""
    dietaryRestrictions: List[str] = []
    preferredCuisine: str = "indian"
    budgetTier: str = "moderate"
    cookingTimePref: str = "moderate"

class WeeklyDietPlanResponseSchema(BaseModel):
    id: Optional[str] = None
    weekNumber: int = 1
    weekStartDate: Optional[str] = None
    selectedDishIds: List[str] = Field(default_factory=list, description="IDs of all selected recipes across the 35 meal slots")
    profileSummary: ProfileSummarySchema
    days: List[DailyDietPlanSchema]
    guidance: NutritionalGuidanceSchema
    generatedAt: str
    nutritionalNotes: List[str]
    safetyWarnings: List[str] = []
    disclaimer: str
    savedToAccount: bool = False
    persistenceMessage: Optional[str] = None

class SavedWeeklyPlanSummarySchema(BaseModel):
    id: str
    weekNumber: int
    weekStartDate: Optional[str] = None
    targetCalories: Optional[int] = None
    totalCaloriesAvg: Optional[float] = None
    totalProteinAvg: Optional[float] = None
    totalCarbsAvg: Optional[float] = None
    totalFatAvg: Optional[float] = None
    goal: Optional[str] = None
    foodPreference: Optional[str] = None
    createdAt: str

class UserProfileOutSchema(BaseModel):
    id: str
    userId: Optional[str] = None
    age: int
    gender: str
    heightCm: float
    weightKg: float
    goalWeightKg: Optional[float] = None
    mealsPerDay: int = 5
    targetTimelineWeeks: Optional[int] = None
    activityLevel: str
    goal: str
    foodPreference: str
    allergies: List[str] = []
    customAllergies: str = ""
    intolerances: List[str] = []
    dislikedFoods: str = ""
    dietaryRestrictions: List[str] = []
    preferredCuisine: str = "indian"
    budgetTier: str = "moderate"
    cookingTimePref: str = "moderate"
    bmi: Optional[float] = None
    bmr: Optional[float] = None
    tdee: Optional[float] = None
    targetCalories: Optional[int] = None
    targetProtein: Optional[int] = None
    targetCarbs: Optional[int] = None
    targetFat: Optional[int] = None
    targetFibre: Optional[int] = None
    bmrFormula: str = "Mifflin-St Jeor"

class UserProfileUpdateSchema(BaseModel):
    age: Optional[int] = Field(None, ge=10, le=120)
    gender: Optional[str] = Field(None, pattern="^(male|female)$")
    heightCm: Optional[float] = Field(None, ge=70.0, le=260.0)
    weightKg: Optional[float] = Field(None, ge=25.0, le=300.0)
    goalWeightKg: Optional[float] = Field(None, ge=25.0, le=300.0)
    mealsPerDay: Optional[int] = Field(None, ge=3, le=6)
    targetTimelineWeeks: Optional[int] = Field(None, ge=1, le=52)
    activityLevel: Optional[str] = Field(None, pattern="^(sedentary|light|moderate|active|very_active)$")
    goal: Optional[str] = Field(None, pattern="^(weight_loss|maintenance|weight_gain|healthy_eating)$")
    foodPreference: Optional[str] = Field(None, pattern="^(vegetarian|non_vegetarian|vegan|eggetarian|pescatarian|jain)$")
    allergies: Optional[List[str]] = None
    customAllergies: Optional[str] = None
    intolerances: Optional[List[str]] = None
    dislikedFoods: Optional[str] = None
    dietaryRestrictions: Optional[List[str]] = None
    preferredCuisine: Optional[str] = None
    budgetTier: Optional[str] = Field(None, pattern="^(budget_friendly|moderate|premium)$")
    cookingTimePref: Optional[str] = Field(None, pattern="^(quick_easy|moderate|elaborate)$")
