import { apiClient } from './api';
import {
  NutritionProfileInput,
  NutritionCalculationResult,
  WeeklyDietPlanResponse,
} from '../types';

export const nutritionService = {
  async calculateMetrics(profile: NutritionProfileInput): Promise<NutritionCalculationResult> {
    try {
      const res = await apiClient.post<NutritionCalculationResult>('/nutrition/calculate', profile);
      return res.data;
    } catch (err: any) {
      if (err.response?.data?.detail) {
        throw new Error(err.response.data.detail);
      }
      throw new Error(err.message || 'Calculation failed');
    }
  },

  async generateWeeklyPlan(profile: NutritionProfileInput): Promise<WeeklyDietPlanResponse> {
    try {
      const res = await apiClient.post<WeeklyDietPlanResponse>('/nutrition/weekly-plan', profile);
      return res.data;
    } catch (err: any) {
      if (err.response?.data?.detail) {
        throw new Error(err.response.data.detail);
      }
      throw new Error(err.message || 'Plan generation failed');
    }
  },

  async generateNextWeekPlan(profile: NutritionProfileInput): Promise<WeeklyDietPlanResponse> {
    try {
      const res = await apiClient.post<WeeklyDietPlanResponse>('/nutrition/weekly-plan', {
        ...profile,
        generateNewWeek: true
      });
      return res.data;
    } catch (err: any) {
      if (err.response?.data?.detail) {
        throw new Error(err.response.data.detail);
      }
      throw new Error(err.message || 'Next week plan generation failed');
    }
  },

  async getLatestSavedPlan(): Promise<WeeklyDietPlanResponse | null> {
    try {
      const res = await apiClient.get<WeeklyDietPlanResponse>('/nutrition/weekly-plan');
      return res.data;
    } catch {
      return null;
    }
  },

  async getSavedWeeklyPlans(): Promise<any[]> {
    try {
      const res = await apiClient.get<any[]>('/nutrition/weekly-plans');
      return res.data;
    } catch {
      return [];
    }
  },

  async getWeeklyPlanById(id: string): Promise<WeeklyDietPlanResponse | null> {
    try {
      const res = await apiClient.get<WeeklyDietPlanResponse>(`/nutrition/weekly-plans/${id}`);
      return res.data;
    } catch (err: any) {
      if (err.response?.data?.detail) {
        throw new Error(err.response.data.detail);
      }
      return null;
    }
  },

  async deleteSavedPlan(id: string): Promise<boolean> {
    try {
      await apiClient.delete(`/nutrition/weekly-plans/${id}`);
      return true;
    } catch (err: any) {
      if (err.response?.data?.detail) {
        throw new Error(err.response.data.detail);
      }
      return false;
    }
  },

  async savePlan(plan: WeeklyDietPlanResponse): Promise<{ success: boolean; message: string }> {
    try {
      const res = await apiClient.post<{ message: string }>('/nutrition/save-plan', plan);
      return { success: true, message: res.data.message || 'Plan saved successfully' };
    } catch (err: any) {
      if (err.response?.data?.detail) throw new Error(err.response.data.detail);
      throw new Error(err.message || 'Could not save the plan to your account. Check your connection and sign-in status.');
    }
  },

  async getUserProfile(): Promise<any> {
    try {
      const res = await apiClient.get('/nutrition/profile');
      return res.data;
    } catch {
      return null;
    }
  },

  async updateUserProfile(updates: any): Promise<any> {
    try {
      const res = await apiClient.put('/nutrition/profile', updates);
      return res.data;
    } catch (err: any) {
      if (err.response?.data?.detail) {
        throw new Error(err.response.data.detail);
      }
      throw new Error(err.message || 'Failed to update profile');
    }
  },

  async searchFoods(query?: string, category?: string, cuisine?: string): Promise<any> {
    try {
      const params = new URLSearchParams();
      if (query) params.append('query', query);
      if (category) params.append('category', category);
      if (cuisine) params.append('cuisine', cuisine);
      const res = await apiClient.get(`/nutrition/foods?${params.toString()}`);
      return res.data;
    } catch (err: any) {
      return { count: 0, results: [] };
    }
  }
};
