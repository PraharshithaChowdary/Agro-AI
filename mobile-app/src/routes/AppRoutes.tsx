import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { User } from '../types';
import { Welcome } from '../pages/Welcome';
import { SignIn } from '../pages/SignIn';
import { SignUp } from '../pages/SignUp';
import { ForgotPassword } from '../pages/ForgotPassword';
import { Dashboard } from '../pages/Dashboard';
import { BetterProduction } from '../pages/BetterProduction';
import { CropAnalysis } from '../pages/CropAnalysis';
import { SoilAnalysis } from '../pages/SoilAnalysis';
import { AnalyseMyPlant } from '../pages/AnalyseMyPlant';
import { IndianPlantExplorer } from '../pages/IndianPlantExplorer';
import { BetterNutrition } from '../pages/BetterNutrition';
import { WeeklyDietPlan } from '../pages/WeeklyDietPlan';
import { AIAssistant } from '../pages/AIAssistant';
import { Profile } from '../pages/Profile';

interface AppRoutesProps {
  user: User | null;
  onLoginSuccess: (user: User) => void;
  onLogout: () => void;
}

export const AppRoutes: React.FC<AppRoutesProps> = ({ user, onLoginSuccess, onLogout }) => {
  return (
    <Routes>
      {/* Public Authentication Pages */}
      <Route path="/" element={<Welcome />} />
      <Route
        path="/signin"
        element={user ? <Navigate to="/dashboard" replace /> : <SignIn onLoginSuccess={onLoginSuccess} />}
      />
      <Route
        path="/signup"
        element={user ? <Navigate to="/dashboard" replace /> : <SignUp onLoginSuccess={onLoginSuccess} />}
      />
      <Route path="/forgot-password" element={<ForgotPassword />} />

      {/* Protected User Dashboard: Redirects to /signin if not authenticated */}
      <Route
        path="/dashboard"
        element={user ? <Dashboard user={user} /> : <Navigate to="/signin" replace />}
      />

      {/* Feature Pages */}
      <Route path="/production" element={<BetterProduction />} />
      <Route path="/production/analyze-my-plant" element={<AnalyseMyPlant />} />
      <Route path="/production/plant" element={<AnalyseMyPlant />} />
      <Route path="/production/crop" element={<CropAnalysis />} />
      <Route path="/production/soil" element={<SoilAnalysis />} />
      <Route path="/production/plants" element={<IndianPlantExplorer />} />
      <Route path="/production/identify" element={<IndianPlantExplorer />} />
      <Route path="/plants" element={<IndianPlantExplorer />} />

      {/* Better Nutrition Feature */}
      <Route path="/nutrition" element={<BetterNutrition />} />
      <Route path="/nutrition/plan" element={<WeeklyDietPlan />} />

      {/* AGRO AI Assistant Feature */}
      <Route path="/assistant" element={<AIAssistant />} />

      {/* Protected Profile Page: Redirects to /signin if not authenticated */}
      <Route
        path="/profile"
        element={user ? <Profile user={user} onLogout={onLogout} /> : <Navigate to="/signin" replace />}
      />

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};
