import React, { useState, useEffect } from 'react';
import { PersistenceNotice } from '../components/PersistenceNotice';
import { Link } from 'react-router-dom';
import {
  HeartPulse,
  Flame,
  Dna,
  Save,
  ArrowLeft,
  CheckCircle2,
  Clock,
  Printer,
  Sparkles,
  Info,
  ChevronDown,
  ChevronUp,
  Utensils,
  ShieldAlert,
  Repeat,
  AlertTriangle,
  AlertCircle,
  RefreshCw,
  Calendar,
} from 'lucide-react';
import { WeeklyDietPlanResponse, NutritionProfileInput, SavedWeeklyPlanSummary } from '../types';
import { nutritionService } from '../services/nutritionService';

export const WeeklyDietPlan: React.FC = () => {
  const [plan, setPlan] = useState<WeeklyDietPlanResponse | null>(null);
  const [activeDay, setActiveDay] = useState<number>(1);
  const [activeTab, setActiveTab] = useState<'schedule' | 'guidance'>('schedule');
  const [expandedDishIndices, setExpandedDishIndices] = useState<Record<string, boolean>>({});
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);
  const [isRegenerating, setIsRegenerating] = useState(false);
  const [isGeneratingNextWeek, setIsGeneratingNextWeek] = useState(false);
  const [savedWeeks, setSavedWeeks] = useState<SavedWeeklyPlanSummary[]>([]);
  const [feedbackNotice, setFeedbackNotice] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRegeneratePlan = async () => {
    if (!plan) return;
    setIsRegenerating(true);
    setFeedbackNotice(null);
    try {
      const nextSeed = (plan.variationSeed || 0) + 1;
      const payload: NutritionProfileInput = {
        age: plan.profileSummary.age || 28,
        gender: plan.profileSummary.gender || 'male',
        heightCm: plan.profileSummary.heightCm || 172,
        weightKg: plan.profileSummary.weightKg || 68,
        goalWeightKg: plan.profileSummary.goalWeightKg,
        mealsPerDay: plan.profileSummary.mealsPerDay || 5,
        activityLevel: plan.profileSummary.activityLevel || 'moderate',
        goal: plan.profileSummary.goal || 'weight_loss',
        foodPreference: plan.profileSummary.foodPreference || 'vegetarian',
        allergies: plan.profileSummary.allergies || [],
        customAllergies: plan.profileSummary.customAllergies || '',
        intolerances: plan.profileSummary.intolerances || [],
        dislikedFoods: plan.profileSummary.dislikedFoods || '',
        dietaryRestrictions: plan.profileSummary.dietaryRestrictions || ['high_protein', 'balanced'],
        preferredCuisine: plan.profileSummary.preferredCuisine || 'indian',
        budgetTier: plan.profileSummary.budgetTier || 'moderate',
        cookingTimePref: plan.profileSummary.cookingTimePref || 'moderate',
        variationSeed: nextSeed,
      };

      const freshPlan = await nutritionService.generateWeeklyPlan(payload);
      setPlan(freshPlan);
      sessionStorage.setItem('agro_current_plan', JSON.stringify(freshPlan));
      setFeedbackNotice(`Refreshed Week ${freshPlan.weekNumber || 1} schedule with fresh recipe variety.`);
    } catch (err: any) {
      setFeedbackNotice(err.message || 'Failed to regenerate variation.');
    } finally {
      setIsRegenerating(false);
    }
  };

  const handleGenerateNextWeek = async () => {
    if (!plan) return;
    setIsGeneratingNextWeek(true);
    setFeedbackNotice(null);
    try {
      const payload: NutritionProfileInput = {
        age: plan.profileSummary.age || 28,
        gender: plan.profileSummary.gender || 'male',
        heightCm: plan.profileSummary.heightCm || 172,
        weightKg: plan.profileSummary.weightKg || 68,
        goalWeightKg: plan.profileSummary.goalWeightKg,
        mealsPerDay: plan.profileSummary.mealsPerDay || 5,
        activityLevel: plan.profileSummary.activityLevel || 'moderate',
        goal: plan.profileSummary.goal || 'weight_loss',
        foodPreference: plan.profileSummary.foodPreference || 'vegetarian',
        allergies: plan.profileSummary.allergies || [],
        customAllergies: plan.profileSummary.customAllergies || '',
        intolerances: plan.profileSummary.intolerances || [],
        dislikedFoods: plan.profileSummary.dislikedFoods || '',
        dietaryRestrictions: plan.profileSummary.dietaryRestrictions || ['high_protein', 'balanced'],
        preferredCuisine: plan.profileSummary.preferredCuisine || 'indian',
        budgetTier: plan.profileSummary.budgetTier || 'moderate',
        cookingTimePref: plan.profileSummary.cookingTimePref || 'moderate',
        generateNewWeek: true,
      };

      const nextWeekPlan = await nutritionService.generateNextWeekPlan(payload);
      setPlan(nextWeekPlan);
      sessionStorage.setItem('agro_current_plan', JSON.stringify(nextWeekPlan));
      setFeedbackNotice(`Successfully generated Week ${nextWeekPlan.weekNumber || 2} plan! Previously used dishes have been minimized to ensure fresh weekly variety.`);

      // Refresh saved weeks list
      const weeks = await nutritionService.getSavedWeeklyPlans();
      if (weeks && weeks.length > 0) {
        setSavedWeeks(weeks);
      }
    } catch (err: any) {
      setFeedbackNotice(err.message || 'Failed to generate next week plan.');
    } finally {
      setIsGeneratingNextWeek(false);
    }
  };

  const handleSelectWeek = async (weekId: string) => {
    if (!weekId) return;
    setLoading(true);
    try {
      const selectedPlan = await nutritionService.getWeeklyPlanById(weekId);
      if (selectedPlan) {
        setPlan(selectedPlan);
        sessionStorage.setItem('agro_current_plan', JSON.stringify(selectedPlan));
        setFeedbackNotice(`Loaded saved Week ${selectedPlan.weekNumber || 1} plan.`);
      }
    } catch (err: any) {
      setFeedbackNotice('Failed to load selected week plan.');
    } finally {
      setLoading(false);
    }
  };

  const fetchLatest = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch saved weeks history
      const weeks = await nutritionService.getSavedWeeklyPlans();
      if (weeks && weeks.length > 0) {
        setSavedWeeks(weeks);
      }

      // 2. Try to fetch from backend
      const data = await nutritionService.getLatestSavedPlan();
      if (data && data.days && data.days.length === 7) {
        setPlan(data);
        sessionStorage.setItem('agro_current_plan', JSON.stringify(data));
        return;
      }

      // 3. Generate standard balanced plan if none saved
      const defaultPlan = await nutritionService.generateWeeklyPlan({
        age: 28,
        gender: 'male',
        heightCm: 172,
        weightKg: 68,
        activityLevel: 'moderate',
        goal: 'weight_loss',
        foodPreference: 'vegetarian',
        mealsPerDay: 5,
        allergies: [],
        dietaryRestrictions: ['high_protein', 'balanced'],
        preferredCuisine: 'indian',
      });
      setPlan(defaultPlan);
      sessionStorage.setItem('agro_current_plan', JSON.stringify(defaultPlan));
    } catch (err: any) {
      console.error('Plan load error:', err);
      setError(err.message || 'Failed to assemble diet plan with verified food data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // 1. Load saved weeks list
    nutritionService.getSavedWeeklyPlans().then((weeks) => {
      if (weeks && weeks.length > 0) {
        setSavedWeeks(weeks);
      }
    });

    // 2. Try to load from session storage
    const cached = sessionStorage.getItem('agro_current_plan');
    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        if (parsed && parsed.days && parsed.days.length === 7) {
          setPlan(parsed);
          return;
        }
      } catch {
        // invalid cached JSON, fallback to fetchLatest
      }
    }

    fetchLatest();
  }, []);

  const handleSavePlan = async () => {
    if (!plan) return;
    setSaving(true);
    setSaveMessage(null);
    try {
      const res = await nutritionService.savePlan(plan);
      setSaveMessage(res.message);
    } catch {
      setSaveMessage('Could not save the plan to your account. The generated plan is still visible, but it has not been saved.');
    } finally {
      setSaving(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const toggleDishExpansion = (key: string) => {
    setExpandedDishIndices((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  // Loading State
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#fbfcf9] py-12 px-4">
        <div className="text-center space-y-4 max-w-md p-8 bg-white rounded-3xl border border-gray-200 shadow-card animate-in fade-in">
          <HeartPulse className="w-12 h-12 text-emerald-600 animate-pulse mx-auto" />
          <h2 className="text-lg font-bold text-agro-950">
            Assembling 7-Day Nutritional Schedule...
          </h2>
          <p className="text-xs text-gray-500 leading-relaxed">
            Calibrating ingredients with ICMR-NIN Indian Food Composition Tables (IFCT 2017) and verifying zero allergen leakage.
          </p>
        </div>
      </div>
    );
  }

  // Error State with Retry
  if (error || !plan) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#fbfcf9] py-12 px-4">
        <div className="text-center space-y-4 max-w-md p-8 bg-white rounded-3xl border border-red-200 shadow-card animate-in fade-in">
          <AlertCircle className="w-12 h-12 text-red-600 mx-auto" />
          <h2 className="text-lg font-extrabold text-agro-950">Diet Plan Generation Notice</h2>
          <p className="text-xs text-red-800 leading-relaxed bg-red-50 p-3.5 rounded-xl border border-red-200 text-left">
            {error || 'No active meal plan found in your current session. Please calculate your metabolic requirements and generate your personalized schedule.'}
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
            <button
              onClick={() => fetchLatest()}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-5 py-2.5 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold shadow-md transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Retry Generation
            </button>
            <Link
              to="/nutrition"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-5 py-2.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-800 text-xs font-bold transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" /> Recalculate Profile
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const currentDayData = plan.days.find((d) => d.dayNumber === activeDay) || plan.days[0];

  return (
    <div className="min-h-screen bg-[#fbfcf9] py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <PersistenceNotice savedToAccount={plan.savedToAccount} message={plan.persistenceMessage} />
        
        {/* Top Navigation & Actions */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-3">
            <Link
              to="/nutrition"
              className="inline-flex items-center gap-2 text-xs font-bold text-emerald-800 hover:text-emerald-950"
            >
              <ArrowLeft className="w-4 h-4" /> Back to Calorie Calculator
            </Link>

            {plan.weekNumber && (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-900 border border-emerald-300 text-xs font-extrabold shadow-2xs">
                <Calendar className="w-3.5 h-3.5 text-emerald-700" />
                Week {plan.weekNumber}
              </span>
            )}

            {savedWeeks.length > 1 && (
              <div className="flex items-center gap-1.5 text-xs">
                <span className="text-gray-500 font-medium">History:</span>
                <select
                  value={plan.id || ''}
                  onChange={(e) => handleSelectWeek(e.target.value)}
                  className="text-xs font-bold text-gray-700 bg-white border border-gray-300 rounded-xl px-2.5 py-1.5 focus:outline-hidden focus:ring-2 focus:ring-emerald-500"
                >
                  {savedWeeks.map((w) => (
                    <option key={w.id} value={w.id}>
                      Week {w.weekNumber} ({w.weekStartDate || 'Saved'})
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <button
              onClick={handleGenerateNextWeek}
              disabled={isGeneratingNextWeek}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-extrabold shadow-md transition-all disabled:opacity-50"
              title="Generate next week's 7-day plan with fresh recipes avoiding previous weeks' dishes"
            >
              <RefreshCw className={`w-3.5 h-3.5 text-emerald-200 ${isGeneratingNextWeek ? 'animate-spin' : ''}`} />
              {isGeneratingNextWeek ? 'Generating Next Week...' : `Generate Next Week (Week ${(plan.weekNumber || 1) + 1})`}
            </button>

            <button
              onClick={handleRegeneratePlan}
              disabled={isRegenerating}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-emerald-300 text-xs font-semibold text-emerald-800 hover:bg-emerald-50 shadow-2xs transition-colors disabled:opacity-50"
              title="Regenerate current week with a fresh variation"
            >
              <Sparkles className={`w-3.5 h-3.5 text-emerald-600 ${isRegenerating ? 'animate-spin' : ''}`} />
              {isRegenerating ? 'Regenerating...' : 'Regenerate Current Week'}
            </button>

            <button
              onClick={handlePrint}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-gray-200 text-xs font-semibold text-gray-700 hover:bg-gray-50 shadow-2xs transition-colors"
            >
              <Printer className="w-3.5 h-3.5 text-gray-500" />
              Print / PDF
            </button>

            <button
              onClick={handleSavePlan}
              disabled={saving}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-gray-900 hover:bg-black text-white text-xs font-bold shadow-md transition-colors disabled:opacity-50"
            >
              <Save className="w-3.5 h-3.5" />
              {saving ? 'Saving...' : 'Save Plan'}
            </button>
          </div>
        </div>

        {feedbackNotice && (
          <div className="flex items-center justify-between gap-2 p-3.5 bg-emerald-50 border border-emerald-300 rounded-xl text-emerald-950 text-xs animate-in fade-in shadow-sm">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-emerald-600 shrink-0" />
              <span className="font-semibold">{feedbackNotice}</span>
            </div>
            <button
              onClick={() => setFeedbackNotice(null)}
              className="text-emerald-700 hover:text-emerald-950 font-bold ml-2 text-sm"
            >
              ✕
            </button>
          </div>
        )}

        {saveMessage && (
          <div className="flex items-center gap-2 p-3.5 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 text-xs animate-in fade-in">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>{saveMessage}</span>
          </div>
        )}

        {/* Plan Header Summary Card */}
        <div className="bg-gradient-to-r from-emerald-950 via-agro-900 to-agro-800 rounded-3xl p-6 sm:p-8 text-white shadow-card">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-xs font-bold uppercase tracking-wider">
                <Sparkles className="w-3 h-3" />
                Evidence-Based 7-Day Schedule
              </span>
              <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
                Personalized Nutritional Plan
              </h1>
              <p className="text-xs sm:text-sm text-emerald-100/80">
                Targeting <strong className="text-white">{plan.profileSummary.targetCalories} kcal/day</strong> with{' '}
                <strong className="text-white">{plan.profileSummary.targetProtein}g protein</strong> for{' '}
                <span className="capitalize">{plan.profileSummary.goal.replace('_', ' ')}</span>.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-3 text-xs">
              <div className="bg-white/10 px-3 py-2 rounded-xl backdrop-blur-sm border border-white/10">
                <span className="text-gray-300 block text-[10px]">Preference</span>
                <span className="font-bold capitalize">{plan.profileSummary.foodPreference.replace('_', ' ')}</span>
              </div>
              <div className="bg-white/10 px-3 py-2 rounded-xl backdrop-blur-sm border border-white/10">
                <span className="text-gray-300 block text-[10px]">Excluded Allergens</span>
                <span className="font-bold">
                  {plan.profileSummary.allergies && plan.profileSummary.allergies.length > 0
                    ? plan.profileSummary.allergies.join(', ')
                    : 'None specified'}
                </span>
              </div>
              {plan.profileSummary.customAllergies && (
                <div className="bg-white/10 px-3 py-2 rounded-xl backdrop-blur-sm border border-white/10">
                  <span className="text-gray-300 block text-[10px]">Custom Exclusions</span>
                  <span className="font-bold">{plan.profileSummary.customAllergies}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* View Switcher: Meal Schedule vs Food Guidance */}
        <div className="flex items-center gap-3 border-b border-gray-200 pb-2">
          <button
            onClick={() => setActiveTab('schedule')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeTab === 'schedule'
                ? 'bg-emerald-700 text-white shadow-sm'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Clock className="w-4 h-4" /> 7-Day Meal Schedule
          </button>

          <button
            onClick={() => setActiveTab('guidance')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeTab === 'guidance'
                ? 'bg-emerald-700 text-white shadow-sm'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Utensils className="w-4 h-4" /> Foods to Eat, Avoid & Safe Substitutions
          </button>
        </div>

        {/* TAB 1: MEAL SCHEDULE */}
        {activeTab === 'schedule' && (
          <div className="space-y-6">
            {/* 7-Day Selector */}
            <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
              {plan.days.map((day) => (
                <button
                  key={day.dayNumber}
                  onClick={() => setActiveDay(day.dayNumber)}
                  className={`flex-1 min-w-[110px] p-3 rounded-2xl border text-center transition-all ${
                    activeDay === day.dayNumber
                      ? 'bg-emerald-700 text-white border-emerald-700 shadow-md scale-[1.02]'
                      : 'bg-white text-gray-700 border-gray-200 hover:border-emerald-300 hover:bg-emerald-50/50'
                  }`}
                >
                  <p className="text-[11px] uppercase font-bold opacity-80">Day {day.dayNumber}</p>
                  <p className="text-xs font-extrabold truncate">{day.dayName}</p>
                  <p className="text-[10px] mt-1 font-semibold opacity-90">{day.dailyTotalCalories} kcal</p>
                </button>
              ))}
            </div>

            {/* Active Day Overview Card */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-gray-100">
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full">
                    Day {currentDayData.dayNumber} of 7
                  </span>
                  <h2 className="text-2xl font-extrabold text-agro-950 mt-1">
                    {currentDayData.dayName}'s Meal Schedule
                  </h2>
                </div>

                {/* Daily Total Summary & Precision Metrics */}
                <div className="flex items-center gap-2.5 flex-wrap">
                  <div className="px-3 py-1.5 rounded-xl bg-gray-50 border border-gray-200 text-center">
                    <span className="text-[10px] font-bold uppercase text-gray-500 block">Goal Target</span>
                    <span className="text-sm font-extrabold text-gray-900">
                      {currentDayData.dailyTargetCalories || plan.profileSummary.targetCalories} <span className="text-[10px] font-normal">kcal</span>
                    </span>
                  </div>

                  <div className="px-3 py-1.5 rounded-xl bg-emerald-50 border border-emerald-200 text-center">
                    <span className="text-[10px] font-bold uppercase text-emerald-700 block">Planned Total</span>
                    <span className="text-sm font-extrabold text-emerald-950">
                      {currentDayData.dailyTotalCalories} <span className="text-[10px] font-normal">kcal</span>
                    </span>
                  </div>

                  <div className={`px-3 py-1.5 rounded-xl border text-center ${
                    Math.abs(currentDayData.calorieDifference || 0) <= 20
                      ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
                      : 'bg-amber-50 border-amber-200 text-amber-900'
                  }`}>
                    <span className="text-[10px] font-bold uppercase block">Target Diff</span>
                    <span className="text-sm font-extrabold">
                      {currentDayData.calorieDifference !== undefined && currentDayData.calorieDifference > 0 ? `+${currentDayData.calorieDifference}` : (currentDayData.calorieDifference ?? 0)} kcal
                      <span className="text-[10px] font-normal ml-1">({currentDayData.calorieDifferencePercent ?? 0}%)</span>
                    </span>
                  </div>

                  <div className="px-3 py-1.5 rounded-xl bg-amber-50 border border-amber-200 text-center">
                    <span className="text-[10px] font-bold uppercase text-amber-800 block">Protein</span>
                    <span className="text-sm font-extrabold text-amber-950">
                      {currentDayData.dailyTotalProtein} <span className="text-[10px] font-normal">g</span>
                    </span>
                  </div>

                  <div className="px-3 py-1.5 rounded-xl bg-blue-50 border border-blue-200 text-center">
                    <span className="text-[10px] font-bold uppercase text-blue-800 block">Carbs</span>
                    <span className="text-sm font-extrabold text-blue-950">
                      {currentDayData.dailyTotalCarbs} <span className="text-[10px] font-normal">g</span>
                    </span>
                  </div>

                  <div className="px-3 py-1.5 rounded-xl bg-purple-50 border border-purple-200 text-center">
                    <span className="text-[10px] font-bold uppercase text-purple-800 block">Fat</span>
                    <span className="text-sm font-extrabold text-purple-950">
                      {currentDayData.dailyTotalFat} <span className="text-[10px] font-normal">g</span>
                    </span>
                  </div>

                  <div className="px-3 py-1.5 rounded-xl bg-teal-50 border border-teal-200 text-center">
                    <span className="text-[10px] font-bold uppercase text-teal-800 block">Fibre</span>
                    <span className="text-sm font-extrabold text-teal-950">
                      {currentDayData.dailyTotalFibre || 32} <span className="text-[10px] font-normal">g</span>
                    </span>
                  </div>
                </div>
              </div>

              {/* Atwater Macro Energy Reconciliation & Tolerance Indicator */}
              <div className="p-3 bg-gray-50/80 rounded-2xl border border-gray-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                <div className="flex items-center gap-2">
                  <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-extrabold border ${
                    currentDayData.isWithinTolerance !== false
                      ? 'bg-emerald-100 text-emerald-800 border-emerald-200'
                      : 'bg-amber-100 text-amber-900 border-amber-300'
                  }`}>
                    {currentDayData.isWithinTolerance !== false ? '✓ Calorie Target Validated (±5% Tolerance)' : 'Target Deviation Reported'}
                  </span>
                  {currentDayData.macroReconciliation && (
                    <span className="text-gray-600 text-[11px]">
                      Atwater Energy: <code className="text-gray-800 font-mono font-bold bg-white px-1.5 py-0.5 rounded border border-gray-200">{currentDayData.macroReconciliation.formula} = {currentDayData.macroReconciliation.atwaterCalculatedKcal} kcal</code>
                    </span>
                  )}
                </div>
                {currentDayData.macroReconciliation?.note && (
                  <span className="text-[10px] text-gray-500 italic">
                    {currentDayData.macroReconciliation.note}
                  </span>
                )}
              </div>

              {/* Meals List */}
              <div className="space-y-4">
                {currentDayData.meals.map((meal, idx) => (
                  <div
                    key={idx}
                    className="p-5 rounded-2xl bg-gray-50 border border-gray-200 hover:border-emerald-300 transition-all space-y-4"
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-200 pb-2">
                      <div className="flex items-center gap-2">
                        <div className="w-7 h-7 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center text-xs font-bold">
                          {idx + 1}
                        </div>
                        <h3 className="text-sm font-extrabold text-agro-950">{meal.mealType}</h3>
                        <span className="text-xs text-gray-500 flex items-center gap-1">
                          <Clock className="w-3 h-3" /> {meal.timeSuggestion}
                        </span>
                      </div>

                      <div className="flex items-center gap-2 text-xs font-bold">
                        <span className="text-gray-700 flex items-center gap-1">
                          <Flame className="w-3.5 h-3.5 text-amber-600" />
                          {meal.totalCalories} kcal
                        </span>
                        <span className="text-emerald-700 flex items-center gap-1">
                          <Dna className="w-3.5 h-3.5 text-emerald-600" />
                          {meal.totalProtein}g protein
                        </span>
                      </div>
                    </div>

                    {/* Dish Items */}
                    <div className="space-y-3">
                      {meal.items.map((item, itemIdx) => {
                        const dishKey = `d${currentDayData.dayNumber}_m${idx}_i${itemIdx}`;
                        const isExpanded = !!expandedDishIndices[dishKey];

                        return (
                          <div
                            key={itemIdx}
                            className="p-4 bg-white rounded-xl border border-gray-200 space-y-2 text-xs"
                          >
                            <div className="flex items-start justify-between gap-3">
                              <div>
                                <div className="flex items-center gap-2">
                                  <h4 className="font-extrabold text-sm text-gray-900">{item.name}</h4>
                                  <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 text-[10px] font-bold capitalize">
                                    {item.cuisine || 'Indian'}
                                  </span>
                                </div>
                                <p className="text-gray-500 text-[11px] font-medium mt-0.5">
                                  Serving: <strong>{item.portion}</strong>
                                </p>
                              </div>
                              <div className="text-right shrink-0">
                                <span className="font-extrabold text-sm text-agro-950">{item.calories} kcal</span>
                                <span className="text-[10px] text-emerald-700 font-semibold block">{item.proteinGrams}g protein</span>
                              </div>
                            </div>

                            {/* Goal fit reason */}
                            {item.goalFitReason && (
                              <p className="text-[11px] text-emerald-800 bg-emerald-50/70 p-2.5 rounded-lg border border-emerald-100">
                                💡 <strong>Why this fits:</strong> {item.goalFitReason}
                              </p>
                            )}

                            {/* Preparation toggle */}
                            <button
                              type="button"
                              onClick={() => toggleDishExpansion(dishKey)}
                              className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 hover:text-emerald-900 pt-1"
                            >
                              {isExpanded ? (
                                <>
                                  <ChevronUp className="w-3.5 h-3.5" /> Hide Ingredient Breakdown & Preparation
                                </>
                              ) : (
                                <>
                                  <ChevronDown className="w-3.5 h-3.5" /> View {item.ingredients?.length || 0} Ingredients & Preparation Steps
                                </>
                              )}
                            </button>

                            {/* Expanded Ingredient Table & Recipe */}
                            {isExpanded && (
                              <div className="pt-3 space-y-3 border-t border-gray-100 animate-in fade-in">
                                {item.preparationInstructions && (
                                  <div className="p-3 bg-gray-50 rounded-lg text-gray-700 space-y-1">
                                    <p className="font-bold text-[11px] text-gray-800">👩‍🍳 Culinary Preparation:</p>
                                    <p className="text-[11px] leading-relaxed">{item.preparationInstructions}</p>
                                  </div>
                                )}

                                {item.ingredients && item.ingredients.length > 0 && (
                                  <div className="overflow-x-auto">
                                    <table className="w-full text-left text-[11px] border-collapse">
                                      <thead>
                                        <tr className="border-b border-gray-200 text-gray-500 font-bold">
                                          <th className="py-1 px-2">Ingredient</th>
                                          <th className="py-1 px-2">Quantity (Basis)</th>
                                          <th className="py-1 px-2 text-right">Calories</th>
                                          <th className="py-1 px-2 text-right">Protein</th>
                                          <th className="py-1 px-2 text-right">Carbs</th>
                                          <th className="py-1 px-2 text-right">Fat</th>
                                          <th className="py-1 px-2 text-right">Fibre</th>
                                        </tr>
                                      </thead>
                                      <tbody>
                                        {item.ingredients.map((ing, ingIdx) => (
                                          <tr key={ingIdx} className="border-b border-gray-100 text-gray-700 hover:bg-gray-50">
                                            <td className="py-1.5 px-2 font-medium">{ing.name}</td>
                                            <td className="py-1.5 px-2 text-gray-500">{ing.measure}</td>
                                            <td className="py-1.5 px-2 text-right font-bold text-gray-900">{ing.calories} kcal</td>
                                            <td className="py-1.5 px-2 text-right text-emerald-700">{ing.protein}g</td>
                                            <td className="py-1.5 px-2 text-right text-blue-700">{ing.carbs}g</td>
                                            <td className="py-1.5 px-2 text-right text-purple-700">{ing.fat}g</td>
                                            <td className="py-1.5 px-2 text-right text-amber-700">{ing.fibre ?? 0}g</td>
                                          </tr>
                                        ))}
                                      </tbody>
                                    </table>
                                  </div>
                                )}
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>

              {/* Daily Hydration Tip */}
              {currentDayData.hydrationTip && (
                <div className="p-4 rounded-2xl bg-blue-50 border border-blue-200 text-xs text-blue-900 flex items-center gap-2.5">
                  <span className="text-base">💧</span>
                  <p>
                    <strong>Hydration Goal:</strong> {currentDayData.hydrationTip}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 2: CLINICAL FOOD GUIDANCE (Eat / Avoid / Limit / Swaps) */}
        {activeTab === 'guidance' && plan.guidance && (
          <div className="space-y-6 animate-in fade-in">
            {/* Section 1: Foods to Eat */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-4">
              <h3 className="text-base font-extrabold text-agro-950 flex items-center gap-2 border-b pb-2">
                <Utensils className="w-5 h-5 text-emerald-600" />
                Foods to Eat: Whole Nutritional Focus
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {plan.guidance.foodsToEat.map((grp, idx) => (
                  <div key={idx} className="p-4 bg-emerald-50/40 rounded-2xl border border-emerald-100 space-y-2">
                    <h4 className="font-extrabold text-xs text-emerald-950 uppercase tracking-wide">
                      {grp.group}
                    </h4>
                    <div className="flex flex-wrap gap-1.5">
                      {grp.items.map((it, i) => (
                        <span key={i} className="px-2.5 py-1 bg-white rounded-lg text-xs font-semibold text-gray-800 border border-gray-200">
                          {it}
                        </span>
                      ))}
                    </div>
                    <p className="text-[11px] text-gray-600 leading-relaxed pt-1">
                      {grp.rationale}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Section 2: Foods to Avoid (Allergies & Strict Restrictions) */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-4">
              <h3 className="text-base font-extrabold text-agro-950 flex items-center gap-2 border-b pb-2">
                <ShieldAlert className="w-5 h-5 text-red-600" />
                Foods to Avoid: Excluded Allergens & Restrictions
              </h3>
              <div className="space-y-2.5">
                {plan.guidance.foodsToAvoid.map((item, idx) => (
                  <div key={idx} className="p-3.5 bg-red-50/60 rounded-xl border border-red-200 flex items-start justify-between gap-3 text-xs">
                    <div>
                      <p className="font-extrabold text-red-950">{item.item}</p>
                      <p className="text-[11px] text-red-800 mt-0.5">{item.reason}</p>
                    </div>
                    <span className="px-2 py-0.5 rounded-full bg-red-200/80 text-red-900 text-[10px] font-bold shrink-0">
                      {item.category}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Section 3: Safe Substitutions */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-4">
              <h3 className="text-base font-extrabold text-agro-950 flex items-center gap-2 border-b pb-2">
                <Repeat className="w-5 h-5 text-emerald-600" />
                Safe Culinary Substitutions
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {plan.guidance.safeSubstitutions.map((sub, idx) => (
                  <div key={idx} className="p-4 bg-gray-50 rounded-2xl border border-gray-200 space-y-2 text-xs">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-bold text-gray-500 line-through">{sub.original}</span>
                      <span className="font-extrabold text-emerald-700">➡️ {sub.substitute}</span>
                    </div>
                    <p className="text-[11px] text-gray-600 pt-1 leading-relaxed">
                      💡 {sub.benefit}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Section 4: Foods to Limit */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-4">
              <h3 className="text-base font-extrabold text-agro-950 flex items-center gap-2 border-b pb-2">
                <AlertTriangle className="w-5 h-5 text-amber-600" />
                Foods to Limit: Mindful Moderation
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {plan.guidance.foodsToLimit.map((lim, idx) => (
                  <div key={idx} className="p-4 bg-amber-50/50 rounded-2xl border border-amber-200 space-y-2 text-xs">
                    <p className="font-extrabold text-amber-950">{lim.group}</p>
                    <div className="flex flex-wrap gap-1">
                      {lim.items.map((it, i) => (
                        <span key={i} className="px-2 py-0.5 bg-white text-gray-700 rounded border border-gray-200 text-[10px]">
                          {it}
                        </span>
                      ))}
                    </div>
                    <p className="text-[11px] text-gray-600 leading-relaxed pt-1">
                      {lim.rationale}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Section 5: Practical Meal Timing & Habits */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-3 text-xs">
              <h3 className="text-base font-extrabold text-agro-950 flex items-center gap-2 border-b pb-2">
                <Clock className="w-5 h-5 text-emerald-600" />
                Practical Meal Timing & Digestion Protocols
              </h3>
              <ul className="space-y-2 text-gray-600 list-disc list-inside">
                {plan.guidance.timingAndPortionTips.map((tip, idx) => (
                  <li key={idx} className="leading-relaxed">
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* Nutritional Notes & Wellness Disclaimer */}
        <div className="bg-white rounded-3xl p-6 border border-gray-200 text-xs text-gray-600 space-y-2">
          <div className="flex items-center gap-1.5 font-bold text-gray-800">
            <Info className="w-4 h-4 text-emerald-600" />
            Nutritional Science & Clinical Disclaimer
          </div>
          <p className="leading-relaxed">
            {plan.disclaimer ||
              'This seven-day diet plan is generated from structured food nutrition data for general dietary wellness and lifestyle balance. It does not replace individualized medical advice or clinical dietetics.'}
          </p>
        </div>

      </div>
    </div>
  );
};
