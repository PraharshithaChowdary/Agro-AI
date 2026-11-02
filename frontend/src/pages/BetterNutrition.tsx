import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  HeartPulse,
  Scale,
  Flame,
  Activity,
  ArrowRight,
  ShieldCheck,
  AlertCircle,
  Loader2,
  Sparkles,
  Info,
  Plus,
  X,
  Clock,
  AlertTriangle,
} from 'lucide-react';
import { nutritionService } from '../services/nutritionService';
import {
  NutritionProfileInput,
  NutritionCalculationResult,
  Gender,
  ActivityLevel,
  NutritionGoal,
  FoodPreference,
  CuisineType,
} from '../types';

export const BetterNutrition: React.FC = () => {
  const navigate = useNavigate();

  // Biometrics & Personal Details
  const [age, setAge] = useState<number>(28);
  const [gender, setGender] = useState<Gender>('male');
  const [heightCm, setHeightCm] = useState<number>(172);
  const [weightKg, setWeightKg] = useState<number>(68);
  const [goalWeightKg, setGoalWeightKg] = useState<string>('');
  const [mealsPerDay, setMealsPerDay] = useState<number>(5);
  const [activityLevel, setActivityLevel] = useState<ActivityLevel>('moderate');

  // Goals & Preferences
  const [goal, setGoal] = useState<NutritionGoal>('weight_loss');
  const [foodPreference, setFoodPreference] = useState<FoodPreference>('vegetarian');
  const [preferredCuisine, setPreferredCuisine] = useState<CuisineType>('indian');

  // Allergies & Restrictions
  const [selectedAllergies, setSelectedAllergies] = useState<string[]>([]);
  const [customAllergyInput, setCustomAllergyInput] = useState<string>('');
  const [customAllergiesList, setCustomAllergiesList] = useState<string[]>([]);
  const [selectedIntolerances, setSelectedIntolerances] = useState<string[]>([]);
  const [selectedRestrictions, setSelectedRestrictions] = useState<string[]>(['high_protein', 'balanced']);

  // Disliked Foods & Lifestyle Preferences
  const [dislikedFoodsInput, setDislikedFoodsInput] = useState<string>('');
  const [dislikedFoodsList, setDislikedFoodsList] = useState<string[]>([]);
  const [budgetTier, setBudgetTier] = useState<'budget_friendly' | 'moderate' | 'premium'>('moderate');
  const [cookingTimePref, setCookingTimePref] = useState<'quick_easy' | 'moderate' | 'elaborate'>('moderate');

  // State Management
  const [calculating, setCalculating] = useState(false);
  const [generatingPlan, setGeneratingPlan] = useState(false);
  const [calculationResult, setCalculationResult] = useState<NutritionCalculationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Predefined Common Allergies
  const allergyOptions = [
    { id: 'peanuts', label: 'Peanuts' },
    { id: 'tree_nuts', label: 'Tree Nuts (Walnuts, Almonds, Cashews)' },
    { id: 'dairy', label: 'Dairy / Lactose' },
    { id: 'gluten', label: 'Gluten / Wheat' },
    { id: 'soy', label: 'Soy' },
    { id: 'eggs', label: 'Eggs' },
    { id: 'seafood', label: 'Seafood / Shellfish' },
    { id: 'sesame', label: 'Sesame' },
    { id: 'mustard', label: 'Mustard' },
    { id: 'sulfites', label: 'Sulfites' },
  ];

  // Intolerances & Food Avoidances
  const intoleranceOptions = [
    { id: 'lactose', label: 'Lactose Intolerance' },
    { id: 'fructose', label: 'Fructose Sensitivity' },
    { id: 'caffeine', label: 'Caffeine Sensitivity' },
    { id: 'artificial_sweeteners', label: 'Artificial Sweeteners' },
  ];

  // Expanded Special Dietary Focus (Section 4)
  const dietaryFocusOptions = [
    { id: 'high_protein', label: 'High Protein' },
    { id: 'high_fibre', label: 'High Fibre' },
    { id: 'balanced', label: 'Balanced Nutrition' },
    { id: 'low_added_sugar', label: 'Low Added Sugar' },
    { id: 'heart_conscious', label: 'Heart-Conscious Eating' },
    { id: 'gut_health', label: 'Gut-Health Support' },
    { id: 'vegetarian', label: 'Vegetarian' },
    { id: 'vegan', label: 'Vegan' },
    { id: 'eggetarian', label: 'Eggetarian' },
    { id: 'pescatarian', label: 'Pescatarian' },
    { id: 'dairy_free', label: 'Dairy-Free' },
    { id: 'gluten_free', label: 'Gluten-Free' },
    { id: 'lactose_free', label: 'Lactose-Free' },
    { id: 'jain', label: 'Jain Food Preference' },
    { id: 'south_indian', label: 'South Indian Meals' },
    { id: 'north_indian', label: 'North Indian Meals' },
    { id: 'budget_friendly', label: 'Budget-Friendly Meals' },
    { id: 'quick_easy', label: 'Quick & Easy Meals' },
    { id: 'home_cooked', label: 'Home-Cooked Meals' },
    { id: 'sports_nutrition', label: 'Sports & Exercise Nutrition' },
    { id: 'pregnancy_breastfeeding', label: 'Pregnancy / Breastfeeding Guidance' },
    { id: 'diabetic_friendly', label: 'Diabetes-Conscious Meal Planning' },
  ];

  const toggleAllergy = (id: string) => {
    setSelectedAllergies((prev) =>
      prev.includes(id) ? prev.filter((a) => a !== id) : [...prev, id]
    );
  };

  const toggleIntolerance = (id: string) => {
    setSelectedIntolerances((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  const toggleRestriction = (id: string) => {
    setSelectedRestrictions((prev) =>
      prev.includes(id) ? prev.filter((r) => r !== id) : [...prev, id]
    );
  };

  const handleAddCustomAllergy = () => {
    if (!customAllergyInput.trim()) return;
    const splitTokens = customAllergyInput
      .split(/[,;\n]+/)
      .map((t) => t.trim().toLowerCase())
      .filter((t) => t.length > 1);

    setCustomAllergiesList((prev) => Array.from(new Set([...prev, ...splitTokens])));
    setCustomAllergyInput('');
  };

  const handleRemoveCustomAllergy = (token: string) => {
    setCustomAllergiesList((prev) => prev.filter((t) => t !== token));
  };

  const handleCustomKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddCustomAllergy();
    }
  };

  const handleAddDislikedFood = () => {
    if (!dislikedFoodsInput.trim()) return;
    const splitTokens = dislikedFoodsInput
      .split(/[,;\n]+/)
      .map((t) => t.trim().toLowerCase())
      .filter((t) => t.length > 1);

    setDislikedFoodsList((prev) => Array.from(new Set([...prev, ...splitTokens])));
    setDislikedFoodsInput('');
  };

  const handleRemoveDislikedFood = (token: string) => {
    setDislikedFoodsList((prev) => prev.filter((t) => t !== token));
  };

  const handleDislikedKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddDislikedFood();
    }
  };

  // Build Profile Payload
  const getProfilePayload = (): NutritionProfileInput => ({
    age: Number(age),
    gender,
    heightCm: Number(heightCm),
    weightKg: Number(weightKg),
    goalWeightKg: goalWeightKg ? Number(goalWeightKg) : undefined,
    mealsPerDay: Number(mealsPerDay),
    activityLevel,
    goal,
    foodPreference,
    allergies: selectedAllergies,
    customAllergies: customAllergiesList.join(', '),
    intolerances: selectedIntolerances,
    dislikedFoods: dislikedFoodsList.join(', '),
    dietaryRestrictions: selectedRestrictions,
    preferredCuisine,
    budgetTier,
    cookingTimePref,
  });

  const handleCalculate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setCalculating(true);

    try {
      const payload = getProfilePayload();
      const res = await nutritionService.calculateMetrics(payload);
      setCalculationResult(res);
    } catch (err: any) {
      setError(err.message || 'Failed to calculate metabolic metrics.');
    } finally {
      setCalculating(false);
    }
  };

  const handleGenerateFullPlan = async () => {
    setError(null);
    setGeneratingPlan(true);

    try {
      const payload = getProfilePayload();
      const plan = await nutritionService.generateWeeklyPlan(payload);
      sessionStorage.setItem('agro_current_plan', JSON.stringify(plan));
      navigate('/nutrition/plan');
    } catch (err: any) {
      setError(err.message || 'Plan generation failed.');
    } finally {
      setGeneratingPlan(false);
    }
  };

  // Real-time incompatible combination warnings
  const conflicts: string[] = [];
  if (foodPreference === 'vegan' && (selectedAllergies.includes('dairy') === false && selectedRestrictions.includes('dairy_free') === false)) {
    // fine
  }
  if (foodPreference === 'vegan' && selectedRestrictions.includes('eggetarian')) {
    conflicts.push("Conflict: 'Vegan' preference selected with 'Eggetarian' focus. Vegan rules strictly take precedence.");
  }
  if (foodPreference === 'jain' && (selectedRestrictions.includes('eggetarian') || selectedRestrictions.includes('pescatarian'))) {
    conflicts.push("Conflict: Jain food preference is incompatible with animal or egg products.");
  }
  if (age < 18) {
    conflicts.push("Notice: Users under 18 years have specific developmental requirements. Please consult a registered pediatric dietitian.");
  }

  return (
    <div className="min-h-screen bg-[#fbfcf9] py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-emerald-100 text-emerald-900 text-xs font-bold tracking-wide">
            <HeartPulse className="w-3.5 h-3.5 text-emerald-600" />
            Personalized Diet & Nutrition Science
          </div>
          <h1 className="text-3xl font-extrabold text-agro-950">
            Better Nutrition: Personalized Meal Planner
          </h1>
          <p className="text-xs sm:text-sm text-gray-600">
            Calculate individualized energy requirements using the validated Mifflin-St Jeor equation, strict ingredient-level allergy filtering, and verified Indian Food Composition Tables.
          </p>
        </div>

        {error && (
          <div className="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-2xl text-red-800 text-xs animate-in fade-in">
            <AlertCircle className="w-5 h-5 shrink-0 text-red-600 mt-0.5" />
            <div>
              <p className="font-bold">Nutritional Planning Alert</p>
              <p className="leading-relaxed">{error}</p>
            </div>
          </div>
        )}

        {conflicts.length > 0 && (
          <div className="space-y-2">
            {conflicts.map((conf, idx) => (
              <div key={idx} className="flex items-center gap-2.5 p-3.5 bg-amber-50 border border-amber-200 rounded-2xl text-amber-900 text-xs">
                <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                <span>{conf}</span>
              </div>
            ))}
          </div>
        )}

        {/* Form Container */}
        <form onSubmit={handleCalculate} className="bg-white rounded-3xl p-6 sm:p-10 border border-gray-200 shadow-card space-y-8">
          
          {/* Section 1: Biometrics & Routine */}
          <div className="space-y-4">
            <h3 className="text-base font-bold text-agro-950 flex items-center gap-2 border-b pb-2">
              <Scale className="w-4 h-4 text-emerald-600" />
              1. Biometrics & Daily Activity
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4">
              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1">
                  Age (years)
                </label>
                <input
                  type="number"
                  min="10"
                  max="120"
                  required
                  value={age}
                  onChange={(e) => setAge(Number(e.target.value))}
                  className="w-full px-3.5 py-2 rounded-xl border border-gray-300 focus:ring-2 focus:ring-emerald-500 text-sm font-semibold outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1">
                  Gender
                </label>
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value as Gender)}
                  className="w-full px-3.5 py-2 rounded-xl border border-gray-300 focus:ring-2 focus:ring-emerald-500 text-sm font-semibold outline-none bg-white"
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1">
                  Height (cm)
                </label>
                <input
                  type="number"
                  min="70"
                  max="250"
                  required
                  value={heightCm}
                  onChange={(e) => setHeightCm(Number(e.target.value))}
                  className="w-full px-3.5 py-2 rounded-xl border border-gray-300 focus:ring-2 focus:ring-emerald-500 text-sm font-semibold outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1">
                  Current Weight (kg)
                </label>
                <input
                  type="number"
                  min="25"
                  max="280"
                  required
                  value={weightKg}
                  onChange={(e) => setWeightKg(Number(e.target.value))}
                  className="w-full px-3.5 py-2 rounded-xl border border-gray-300 focus:ring-2 focus:ring-emerald-500 text-sm font-semibold outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1">
                  Goal Weight (kg) <span className="text-[10px] text-gray-400 font-normal">(Optional)</span>
                </label>
                <input
                  type="number"
                  min="25"
                  max="280"
                  placeholder="e.g. 64"
                  value={goalWeightKg}
                  onChange={(e) => setGoalWeightKg(e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-gray-300 focus:ring-2 focus:ring-emerald-500 text-sm font-semibold outline-none"
                />
              </div>
            </div>

            {/* Daily Activity Level */}
            <div>
              <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">
                Daily Activity Level
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-5 gap-2.5">
                {[
                  { id: 'sedentary', label: 'Sedentary', desc: 'Desk job, little exercise' },
                  { id: 'light', label: 'Light', desc: '1-3 days light exercise' },
                  { id: 'moderate', label: 'Moderate', desc: '3-5 days moderate exercise' },
                  { id: 'active', label: 'Active', desc: '6-7 days intense sports' },
                  { id: 'very_active', label: 'Very Active', desc: 'Physical labour / 2x training' },
                ].map((act) => (
                  <button
                    key={act.id}
                    type="button"
                    onClick={() => setActivityLevel(act.id as ActivityLevel)}
                    className={`p-3 rounded-xl border text-left flex flex-col justify-between transition-all ${
                      activityLevel === act.id
                        ? 'border-emerald-600 bg-emerald-50 text-emerald-950 font-bold ring-2 ring-emerald-600'
                        : 'border-gray-200 hover:border-gray-300 text-gray-700'
                    }`}
                  >
                    <span className="text-xs">{act.label}</span>
                    <span className="text-[10px] text-gray-500 font-normal">{act.desc}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Meals Per Day */}
            <div>
              <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">
                Meals Per Day Schedule
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 max-w-xl">
                {[
                  { count: 3, label: '3 Meals', desc: 'Breakfast, Lunch, Dinner' },
                  { count: 4, label: '4 Meals', desc: 'Includes Evening Snack' },
                  { count: 5, label: '5 Meals (Standard)', desc: 'With Mid-Morning & Evening' },
                  { count: 6, label: '6 Meals', desc: 'Frequent small portions' },
                ].map((m) => (
                  <button
                    key={m.count}
                    type="button"
                    onClick={() => setMealsPerDay(m.count)}
                    className={`p-3 rounded-xl border text-left transition-all ${
                      mealsPerDay === m.count
                        ? 'border-emerald-600 bg-emerald-50 text-emerald-950 font-bold ring-2 ring-emerald-600'
                        : 'border-gray-200 hover:border-gray-300 text-gray-700'
                    }`}
                  >
                    <span className="text-xs block">{m.label}</span>
                    <span className="text-[10px] text-gray-500 font-normal block">{m.desc}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Section 2: Health Goal & Dietary Preference */}
          <div className="space-y-4">
            <h3 className="text-base font-bold text-agro-950 flex items-center gap-2 border-b pb-2">
              <Flame className="w-4 h-4 text-emerald-600" />
              2. Health Goal, Preference & Cuisine
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {/* Health Goal */}
              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1">
                  Health Goal
                </label>
                <select
                  value={goal}
                  onChange={(e) => setGoal(e.target.value as NutritionGoal)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-emerald-500 text-sm font-semibold outline-none bg-white"
                >
                  <option value="weight_loss">Weight Loss</option>
                  <option value="weight_gain">Weight Gain</option>
                  <option value="maintenance">Maintain Weight</option>
                  <option value="healthy_eating">General Healthy Eating</option>
                </select>
                <p className="text-[10px] text-gray-400 mt-1">
                  Individualized targets calculated from your metabolic metrics.
                </p>
              </div>

              {/* Food Preference */}
              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1">
                  Food Preference
                </label>
                <select
                  value={foodPreference}
                  onChange={(e) => setFoodPreference(e.target.value as FoodPreference)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-emerald-500 text-sm font-semibold outline-none bg-white"
                >
                  <option value="vegetarian">Pure Vegetarian (Lacto-Veg)</option>
                  <option value="vegan">Vegan (100% Plant-based)</option>
                  <option value="jain">Jain (No Root Veg, Pure Ahimsa)</option>
                  <option value="eggetarian">Eggetarian (Vegetarian + Eggs)</option>
                  <option value="non_vegetarian">Non-Vegetarian (Poultry/Meat)</option>
                  <option value="pescatarian">Pescatarian (Fish & Seafood)</option>
                </select>
              </div>

              {/* Preferred Cuisine */}
              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1">
                  Preferred Cuisine Style
                </label>
                <select
                  value={preferredCuisine}
                  onChange={(e) => setPreferredCuisine(e.target.value as CuisineType)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-emerald-500 text-sm font-semibold outline-none bg-white"
                >
                  <option value="indian">Indian (Traditional Whole Foods & Lentils)</option>
                  <option value="south_indian">South Indian (Millets, Idli, Dosa, Sambar & Poriyal)</option>
                  <option value="andhra">Andhra (Pesarattu, Spicy Pappu, Millets & Ragi)</option>
                  <option value="tamil">Tamil (Pongal, Sambar, Rasam, Adai & Poriyal)</option>
                  <option value="north_indian">North Indian (Dal Makhani, Paneer, Phulkas & Khichdi)</option>
                  <option value="mediterranean">Mediterranean (Olive oil, greens, fish)</option>
                  <option value="continental">Continental / Global</option>
                  <option value="asian">Asian (Rice bowls, stir-fry)</option>
                  <option value="general">Balanced General Diet</option>
                </select>
              </div>

              {/* Budget Preference */}
              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1">
                  Meal Budget
                </label>
                <select
                  value={budgetTier}
                  onChange={(e) => setBudgetTier(e.target.value as any)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-emerald-500 text-sm font-semibold outline-none bg-white"
                >
                  <option value="budget_friendly">Budget-Friendly (Staple Millets & Dals)</option>
                  <option value="moderate">Moderate / Standard Groceries</option>
                  <option value="premium">Premium (Organic & Diverse Seeds/Nuts)</option>
                </select>
              </div>

              {/* Cooking Time Preference */}
              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1">
                  Available Prep Time
                </label>
                <select
                  value={cookingTimePref}
                  onChange={(e) => setCookingTimePref(e.target.value as any)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-emerald-500 text-sm font-semibold outline-none bg-white"
                >
                  <option value="quick_easy">Quick & Easy (&lt; 20 mins)</option>
                  <option value="moderate">Moderate Prep (25–40 mins)</option>
                  <option value="elaborate">Elaborate / Traditional Home Cooking</option>
                </select>
              </div>
            </div>
          </div>

          {/* Section 3: Strict Allergy & Restriction Filtering */}
          <div className="space-y-6">
            <h3 className="text-base font-bold text-agro-950 flex items-center gap-2 border-b pb-2">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              3. Strict Allergy & Restriction Filtering
            </h3>

            {/* 3A: Common Allergens */}
            <div>
              <p className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">
                Common Allergens to Exclude:
              </p>
              <div className="flex flex-wrap gap-2">
                {allergyOptions.map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => toggleAllergy(item.id)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-all ${
                      selectedAllergies.includes(item.id)
                        ? 'bg-red-50 border-red-400 text-red-800 ring-1 ring-red-400'
                        : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    {selectedAllergies.includes(item.id) ? '✕ ' : '+ '}
                    {item.label}
                  </button>
                ))}
              </div>
            </div>

            {/* 3B: Custom Free-Text Allergy Input Bar */}
            <div className="bg-emerald-50/50 p-4 rounded-2xl border border-emerald-100 space-y-3">
              <label className="block text-xs font-bold text-agro-950 uppercase tracking-wider">
                Other Allergy or Food to Avoid (Type Any Food/Ingredient):
              </label>
              
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  placeholder="e.g. mushrooms, brinjal, capsicum, pineapple, coconut, onion, garlic..."
                  value={customAllergyInput}
                  onChange={(e) => setCustomAllergyInput(e.target.value)}
                  onKeyDown={handleCustomKeyDown}
                  className="flex-1 px-4 py-2.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-emerald-500 text-xs outline-none bg-white shadow-sm"
                />
                <button
                  type="button"
                  onClick={handleAddCustomAllergy}
                  className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold shadow-sm transition-colors"
                >
                  <Plus className="w-4 h-4" /> Add Food
                </button>
              </div>

              {/* Custom Tag Chips */}
              {customAllergiesList.length > 0 && (
                <div className="flex flex-wrap items-center gap-2 pt-1">
                  <span className="text-[11px] font-bold text-gray-500">Excluded Custom Items:</span>
                  {customAllergiesList.map((token) => (
                    <span
                      key={token}
                      className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-100 text-red-800 text-xs font-bold border border-red-200"
                    >
                      {token}
                      <button
                        type="button"
                        onClick={() => handleRemoveCustomAllergy(token)}
                        className="hover:text-red-950"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>
              )}
              <p className="text-[11px] text-gray-500">
                You can type multiple items separated by commas. These will be strictly excluded from all meals, ingredients, and substitutions.
              </p>
            </div>

            {/* 3C: Disliked Foods (Ingredients to Minimize or Avoid) */}
            <div className="bg-amber-50/50 p-4 rounded-2xl border border-amber-200/60 space-y-3">
              <label className="block text-xs font-bold text-amber-950 uppercase tracking-wider">
                Disliked Foods & Ingredients to Minimize (Personal Preferences):
              </label>
              
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  placeholder="e.g. karela, bitter gourd, brinjal, methi, capsicum, coriander, mushrooms..."
                  value={dislikedFoodsInput}
                  onChange={(e) => setDislikedFoodsInput(e.target.value)}
                  onKeyDown={handleDislikedKeyDown}
                  className="flex-1 px-4 py-2.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-amber-500 text-xs outline-none bg-white shadow-sm"
                />
                <button
                  type="button"
                  onClick={handleAddDislikedFood}
                  className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-amber-700 hover:bg-amber-800 text-white text-xs font-bold shadow-sm transition-colors"
                >
                  <Plus className="w-4 h-4" /> Add Disliked Food
                </button>
              </div>

              {/* Disliked Tag Chips */}
              {dislikedFoodsList.length > 0 && (
                <div className="flex flex-wrap items-center gap-2 pt-1">
                  <span className="text-[11px] font-bold text-gray-500">Items to Minimize:</span>
                  {dislikedFoodsList.map((token) => (
                    <span
                      key={token}
                      className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-100 text-amber-900 text-xs font-bold border border-amber-300"
                    >
                      {token}
                      <button
                        type="button"
                        onClick={() => handleRemoveDislikedFood(token)}
                        className="hover:text-amber-950"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>
              )}
              <p className="text-[11px] text-gray-500">
                Disliked ingredients will be penalized in dish selection and avoided whenever valid alternative recipes exist.
              </p>
            </div>

            {/* 3D: Intolerances & Avoidances */}
            <div>
              <p className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">
                Intolerances & Sensitivities:
              </p>
              <div className="flex flex-wrap gap-2">
                {intoleranceOptions.map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => toggleIntolerance(item.id)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-all ${
                      selectedIntolerances.includes(item.id)
                        ? 'bg-amber-50 border-amber-400 text-amber-900 ring-1 ring-amber-400'
                        : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    {selectedIntolerances.includes(item.id) ? '✓ ' : '+ '}
                    {item.label}
                  </button>
                ))}
              </div>
            </div>

            {/* 3E: Special Dietary Focus (Section 4) */}
            <div>
              <p className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">
                Special Dietary Focus (Multiple Selections Allowed):
              </p>
              <div className="flex flex-wrap gap-2">
                {dietaryFocusOptions.map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => toggleRestriction(item.id)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-all ${
                      selectedRestrictions.includes(item.id)
                        ? 'bg-emerald-50 border-emerald-400 text-emerald-900 ring-1 ring-emerald-400'
                        : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    {selectedRestrictions.includes(item.id) ? '✓ ' : '+ '}
                    {item.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="pt-2">
            <button
              type="submit"
              disabled={calculating}
              className="w-full flex items-center justify-center gap-2 py-3.5 px-6 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm shadow-md transition-all disabled:opacity-50"
            >
              {calculating ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-emerald-300" />
                  Calculating Metabolic Targets...
                </>
              ) : (
                <>
                  <Activity className="w-4 h-4 text-emerald-300" />
                  Calculate Metabolic Metrics & Targets
                </>
              )}
            </button>
          </div>
        </form>

        {/* Calculation Result Card */}
        {calculationResult && (
          <div className="bg-white rounded-3xl p-6 sm:p-10 border border-emerald-200 shadow-card space-y-6 animate-in fade-in slide-in-from-bottom-4">
            
            {/* Header info */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-gray-100">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
                  Mifflin-St Jeor Verified
                </span>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-agro-950 mt-2">
                  Daily Target: {calculationResult.targetCalories} kcal
                </h2>
                <p className="text-xs text-gray-500 mt-1">
                  Methodology: {calculationResult.formulaUsed}
                </p>
              </div>

              <div className="text-left sm:text-right">
                <span className="text-[10px] uppercase font-bold text-gray-400">BMI Index</span>
                <p className="text-2xl font-extrabold text-agro-950">
                  {calculationResult.bmi.toFixed(1)}
                  <span className="text-xs font-bold text-emerald-700 ml-1.5">
                    ({calculationResult.bmiCategory})
                  </span>
                </p>
              </div>
            </div>

            {/* Clinical / Safety Warnings */}
            {calculationResult.safetyWarnings && calculationResult.safetyWarnings.length > 0 && (
              <div className="space-y-2">
                {calculationResult.safetyWarnings.map((warn, i) => (
                  <div key={i} className="flex items-start gap-2.5 p-3.5 bg-amber-50 border border-amber-200 rounded-xl text-amber-900 text-xs">
                    <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                    <span>{warn}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Metabolic Breakdown Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-4 rounded-2xl bg-gray-50 border border-gray-200">
                <p className="text-[11px] font-bold text-gray-500 uppercase tracking-wide">1. Basal Metabolic Rate (BMR)</p>
                <p className="text-xl font-extrabold text-agro-950 mt-1">{calculationResult.bmr} <span className="text-xs font-semibold text-gray-500">kcal</span></p>
                <p className="text-[10px] text-gray-500 mt-0.5">Resting basal expenditure</p>
              </div>

              <div className="p-4 rounded-2xl bg-gray-50 border border-gray-200">
                <p className="text-[11px] font-bold text-gray-500 uppercase tracking-wide">2. Total Expenditure (TDEE)</p>
                <p className="text-xl font-extrabold text-agro-950 mt-1">{calculationResult.tdee} <span className="text-xs font-semibold text-gray-500">kcal</span></p>
                <p className="text-[10px] text-gray-500 mt-0.5">With activity multiplier</p>
              </div>

              <div className="p-4 rounded-2xl bg-indigo-50/70 border border-indigo-200">
                <p className="text-[11px] font-bold text-indigo-900 uppercase tracking-wide">3. Goal Adjustment</p>
                <p className="text-xl font-extrabold text-indigo-950 mt-1">
                  {calculationResult.goalAdjustmentCalories !== undefined && calculationResult.goalAdjustmentCalories > 0
                    ? `+${calculationResult.goalAdjustmentCalories}`
                    : calculationResult.goalAdjustmentCalories ?? 0}{' '}
                  <span className="text-xs font-semibold text-indigo-700">kcal</span>
                </p>
                <p className="text-[10px] text-indigo-800 mt-0.5 capitalize">
                  {calculationResult.goal?.replace('_', ' ') || 'Moderate adaptation'}
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200">
                <p className="text-[11px] font-bold text-emerald-800 uppercase tracking-wide">4. Planned Daily Target</p>
                <p className="text-xl font-extrabold text-emerald-950 mt-1">{calculationResult.targetCalories} <span className="text-xs font-semibold text-emerald-700">kcal</span></p>
                <p className="text-[10px] text-emerald-800 mt-0.5">Recommended daily intake</p>
              </div>
            </div>

            {/* Target Macronutrients */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-3.5 rounded-2xl bg-emerald-50/60 border border-emerald-200">
                <p className="text-[10px] font-bold text-emerald-800 uppercase">Target Protein</p>
                <p className="text-lg font-extrabold text-emerald-950 mt-0.5">{calculationResult.targetProteinGrams} g</p>
                <p className="text-[10px] text-emerald-700">~25-30% daily calories</p>
              </div>

              <div className="p-3.5 rounded-2xl bg-amber-50/60 border border-amber-200">
                <p className="text-[10px] font-bold text-amber-800 uppercase">Target Carbohydrates</p>
                <p className="text-lg font-extrabold text-amber-950 mt-0.5">{calculationResult.targetCarbsGrams} g</p>
                <p className="text-[10px] text-amber-700">Whole grains & legumes</p>
              </div>

              <div className="p-3.5 rounded-2xl bg-blue-50/60 border border-blue-200">
                <p className="text-[10px] font-bold text-blue-800 uppercase">Target Healthy Fat</p>
                <p className="text-lg font-extrabold text-blue-950 mt-0.5">{calculationResult.targetFatGrams} g</p>
                <p className="text-[10px] text-blue-700">Unsaturated & seed oils</p>
              </div>

              <div className="p-3.5 rounded-2xl bg-teal-50/60 border border-teal-200">
                <p className="text-[10px] font-bold text-teal-800 uppercase">Target Dietary Fibre</p>
                <p className="text-lg font-extrabold text-teal-950 mt-0.5">{calculationResult.targetFibreGrams || 32} g</p>
                <p className="text-[10px] text-teal-700">ICMR 30-35g minimum</p>
              </div>
            </div>

            {/* Per-Meal Calorie Budgets */}
            {calculationResult.mealCalorieTargets && Object.keys(calculationResult.mealCalorieTargets).length > 0 && (
              <div className="p-4 rounded-2xl bg-gray-50 border border-gray-200 space-y-2">
                <p className="text-xs font-bold text-gray-700 uppercase tracking-wider flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5 text-emerald-600" />
                  Estimated Calorie Distribution ({calculationResult.mealsPerDay || 5} Meals/Day)
                </p>
                <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 pt-1">
                  {Object.entries(calculationResult.mealCalorieTargets).map(([mName, mCal]) => (
                    <div key={mName} className="p-2.5 bg-white rounded-xl border border-gray-200 text-center">
                      <span className="text-[10px] text-gray-500 font-bold block truncate">{mName}</span>
                      <span className="text-sm font-extrabold text-agro-950">{mCal} kcal</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Scientific Disclaimer */}
            <div className="p-4 rounded-2xl bg-gray-50 border border-gray-200 text-xs text-gray-600 flex items-start gap-2.5">
              <Info className="w-4 h-4 text-gray-500 shrink-0 mt-0.5" />
              <span>{calculationResult.disclaimer}</span>
            </div>

            {/* Generate 7-Day Plan CTA */}
            <div className="pt-2">
              <button
                type="button"
                onClick={handleGenerateFullPlan}
                disabled={generatingPlan}
                className="w-full flex items-center justify-center gap-2 py-4 px-6 rounded-2xl bg-agro-900 hover:bg-agro-800 text-white font-extrabold text-base shadow-lg transition-all"
              >
                {generatingPlan ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin text-green-400" />
                    Generating 7-Day Personalized Schedule with Ingredient Data...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 text-green-400" />
                    Generate Complete 7-Day Personalized Diet Plan
                    <ArrowRight className="w-5 h-5" />
                  </>
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
