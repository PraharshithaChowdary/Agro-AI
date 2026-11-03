import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Calendar,
  Flame,
  ArrowRight,
  Loader2,
  Trash2,
  AlertCircle,
  Plus,
  Dna,
  LogIn,
  CheckCircle2,
  Sparkles,
} from 'lucide-react';
import { SavedWeeklyPlanSummary } from '../types';
import { nutritionService } from '../services/nutritionService';

interface SavedPlansListProps {
  onSwitchToPlanner: () => void;
}

export const SavedPlansList: React.FC<SavedPlansListProps> = ({ onSwitchToPlanner }) => {
  const navigate = useNavigate();
  const [plans, setPlans] = useState<SavedWeeklyPlanSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [openingId, setOpeningId] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [feedback, setFeedback] = useState<string | null>(null);

  const isLoggedIn = !!localStorage.getItem('agro_token');

  const fetchPlans = async () => {
    if (!isLoggedIn) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await nutritionService.getSavedWeeklyPlans();
      setPlans(data || []);
    } catch (err: any) {
      setError(err.message || 'Failed to retrieve saved nutrition plans.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlans();
  }, [isLoggedIn]);

  const handleOpenPlan = async (planId: string) => {
    setOpeningId(planId);
    setError(null);
    try {
      const fullPlan = await nutritionService.getWeeklyPlanById(planId);
      if (fullPlan) {
        sessionStorage.setItem('agro_current_plan', JSON.stringify(fullPlan));
        navigate(`/nutrition/plan?id=${planId}`);
      } else {
        setError('Could not retrieve the complete plan details.');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to open the saved meal plan.');
    } finally {
      setOpeningId(null);
    }
  };

  const handleDeletePlan = async (planId: string, weekNumber: number) => {
    if (!window.confirm(`Are you sure you want to delete Week ${weekNumber} nutrition plan from your account?`)) {
      return;
    }
    setDeletingId(planId);
    setError(null);
    try {
      const ok = await nutritionService.deleteSavedPlan(planId);
      if (ok) {
        setPlans((prev) => prev.filter((p) => p.id !== planId));
        setFeedback(`Week ${weekNumber} plan successfully deleted.`);
        setTimeout(() => setFeedback(null), 4000);
      } else {
        setError('Failed to delete the nutrition plan.');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to delete plan.');
    } finally {
      setDeletingId(null);
    }
  };

  // 1. Unauthenticated State
  if (!isLoggedIn) {
    return (
      <div className="bg-white rounded-3xl p-8 sm:p-12 border border-gray-200 shadow-card text-center space-y-6 max-w-xl mx-auto animate-in fade-in">
        <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-700 flex items-center justify-center mx-auto shadow-sm">
          <Calendar className="w-8 h-8 text-emerald-600" />
        </div>
        <div className="space-y-2">
          <h2 className="text-2xl font-extrabold text-agro-950">Access Your Saved Nutrition Plans</h2>
          <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
            Sign in with your AGRO AI account to view your 7-day nutritional schedules, calorie targets, and ingredient breakdowns across web and mobile.
          </p>
        </div>
        <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
          <button
            onClick={() => navigate('/signin')}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-agro-900 hover:bg-agro-800 text-white font-bold text-xs shadow-md transition-all"
          >
            <LogIn className="w-4 h-4 text-green-400" /> Sign In to View Saved Plans
          </button>
          <button
            onClick={onSwitchToPlanner}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-5 py-3 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold text-xs transition-colors"
          >
            Use Free Planner Preview
          </button>
        </div>
      </div>
    );
  }

  // 2. Loading State
  if (loading) {
    return (
      <div className="bg-white rounded-3xl p-12 border border-gray-200 shadow-card text-center space-y-4 max-w-xl mx-auto">
        <Loader2 className="w-10 h-10 text-emerald-600 animate-spin mx-auto" />
        <h3 className="text-base font-bold text-agro-950">Loading Your Saved Nutrition Plans...</h3>
        <p className="text-xs text-gray-500">Querying your personalized schedules from the cloud database.</p>
      </div>
    );
  }

  // 3. Authenticated State with Plans or Empty
  return (
    <div className="space-y-6 animate-in fade-in">
      {/* Notifications */}
      {feedback && (
        <div className="flex items-center gap-2.5 p-3.5 bg-green-50 border border-green-200 rounded-2xl text-green-800 text-xs font-bold animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-green-600 shrink-0" />
          <span>{feedback}</span>
        </div>
      )}

      {error && (
        <div className="flex items-center gap-2.5 p-3.5 bg-red-50 border border-red-200 rounded-2xl text-red-700 text-xs animate-in fade-in">
          <AlertCircle className="w-4 h-4 text-red-600 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Header bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-2xl border border-gray-200 shadow-xs">
        <div>
          <h2 className="text-lg font-extrabold text-agro-950 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-emerald-600" />
            My Saved Nutrition Plans
            <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold">
              {plans.length}
            </span>
          </h2>
          <p className="text-xs text-gray-500 mt-0.5">
            Complete 7-day meal schedules, calorie calibrations, and macro distributions saved to your account.
          </p>
        </div>

        <button
          onClick={onSwitchToPlanner}
          className="inline-flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl bg-agro-900 hover:bg-agro-800 text-white font-bold text-xs shadow-sm transition-all shrink-0"
        >
          <Plus className="w-4 h-4 text-green-400" /> Generate New Week Plan
        </button>
      </div>

      {/* Empty State */}
      {plans.length === 0 ? (
        <div className="bg-white rounded-3xl p-10 border border-gray-200 shadow-card text-center space-y-5 max-w-lg mx-auto">
          <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto shadow-sm">
            <Sparkles className="w-8 h-8 text-emerald-600" />
          </div>
          <div className="space-y-1.5">
            <h3 className="text-lg font-extrabold text-agro-950">No Saved Meal Plans Found</h3>
            <p className="text-xs text-gray-500 leading-relaxed">
              You haven't generated or saved any 7-day nutrition plans yet. Use our personalized planner to calculate your metabolic needs and generate your first schedule!
            </p>
          </div>
          <button
            onClick={onSwitchToPlanner}
            className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs shadow-md transition-colors"
          >
            Create My First Meal Plan <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      ) : (
        /* Plans Grid */
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {plans.map((p) => {
            const formattedDate = p.weekStartDate || (p.createdAt ? p.createdAt.split('T')[0] : 'Active Plan');
            const isOpening = openingId === p.id;
            const isDeleting = deletingId === p.id;

            return (
              <div
                key={p.id}
                className="bg-white rounded-2xl p-5 border border-gray-200 hover:border-emerald-300 shadow-card hover:shadow-md transition-all flex flex-col justify-between space-y-4"
              >
                {/* Card Top */}
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-2">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-0.5 rounded-lg bg-emerald-100 text-emerald-800 font-extrabold text-xs">
                          Week {p.weekNumber}
                        </span>
                        {p.goal && (
                          <span className="px-2 py-0.5 rounded-lg bg-gray-100 text-gray-700 font-bold text-[10px] uppercase">
                            {p.goal.replace('_', ' ')}
                          </span>
                        )}
                        {p.foodPreference && (
                          <span className="px-2 py-0.5 rounded-lg bg-green-50 text-green-700 font-bold text-[10px] uppercase">
                            {p.foodPreference}
                          </span>
                        )}
                      </div>
                      <p className="text-[11px] text-gray-500 font-medium">
                        Start Date: <span className="font-semibold text-gray-700">{formattedDate}</span>
                      </p>
                    </div>

                    <button
                      type="button"
                      disabled={isDeleting || isOpening}
                      onClick={() => handleDeletePlan(p.id, p.weekNumber)}
                      title="Delete saved plan"
                      className="p-1.5 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors disabled:opacity-50"
                    >
                      {isDeleting ? <Loader2 className="w-4 h-4 animate-spin text-red-600" /> : <Trash2 className="w-4 h-4" />}
                    </button>
                  </div>

                  {/* Nutrients Row */}
                  <div className="grid grid-cols-3 gap-2 p-3 rounded-xl bg-gray-50 border border-gray-100 text-center">
                    <div className="space-y-0.5">
                      <span className="text-[10px] uppercase font-bold text-gray-400 flex items-center justify-center gap-1">
                        <Flame className="w-3 h-3 text-amber-500" /> Target
                      </span>
                      <p className="text-xs font-extrabold text-gray-900">
                        {p.targetCalories || 2000} <span className="text-[9px] font-normal text-gray-500">kcal</span>
                      </p>
                    </div>

                    <div className="space-y-0.5">
                      <span className="text-[10px] uppercase font-bold text-gray-400 flex items-center justify-center gap-1">
                        <Flame className="w-3 h-3 text-emerald-500" /> Avg Daily
                      </span>
                      <p className="text-xs font-extrabold text-gray-900">
                        {p.totalCaloriesAvg ? Math.round(p.totalCaloriesAvg) : (p.targetCalories || 2000)}{' '}
                        <span className="text-[9px] font-normal text-gray-500">kcal</span>
                      </p>
                    </div>

                    <div className="space-y-0.5">
                      <span className="text-[10px] uppercase font-bold text-gray-400 flex items-center justify-center gap-1">
                        <Dna className="w-3 h-3 text-blue-500" /> Protein
                      </span>
                      <p className="text-xs font-extrabold text-gray-900">
                        {p.totalProteinAvg ? Math.round(p.totalProteinAvg) : 75}{' '}
                        <span className="text-[9px] font-normal text-gray-500">g</span>
                      </p>
                    </div>
                  </div>
                </div>

                {/* Card Bottom / Action */}
                <div className="pt-2 border-t border-gray-100 flex items-center justify-between">
                  <span className="text-[10px] text-gray-400">
                    Saved: {p.createdAt ? new Date(p.createdAt).toLocaleDateString() : 'Cloud DB'}
                  </span>

                  <button
                    type="button"
                    disabled={isOpening}
                    onClick={() => handleOpenPlan(p.id)}
                    className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs shadow-sm transition-all disabled:opacity-50"
                  >
                    {isOpening ? (
                      <>
                        <Loader2 className="w-3.5 h-3.5 animate-spin" /> Loading Plan...
                      </>
                    ) : (
                      <>
                        Open 7-Day Plan <ArrowRight className="w-3.5 h-3.5" />
                      </>
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

