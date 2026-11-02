import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Sprout,
  HeartPulse,
  BotMessageSquare,
  ArrowRight,
  Calendar,
  Sparkles,
  CheckCircle2,
  Clock,
  ChevronRight,
  Layers,
} from 'lucide-react';
import { User, ProductionHistoryItem } from '../types';
import { productionService } from '../services/productionService';

interface DashboardProps {
  user: User;
}

export const Dashboard: React.FC<DashboardProps> = ({ user }) => {
  const [history, setHistory] = useState<ProductionHistoryItem[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  useEffect(() => {
    const fetchHistory = async () => {
      setLoadingHistory(true);
      try {
        const data = await productionService.getHistory();
        setHistory(data);
      } catch {
        // Fallback
      } finally {
        setLoadingHistory(false);
      }
    };
    fetchHistory();
  }, []);

  const getRoleDisplay = () => {
    switch (user.role) {
      case 'farmer':
        return { label: 'Farmer Portal', badge: '🌱 Certified Farmer', color: 'bg-green-100 text-green-800' };
      case 'buyer':
        return { label: 'Produce Buyer Portal', badge: '🌾 Produce Trader', color: 'bg-amber-100 text-amber-800' };
      case 'admin':
        return { label: 'Administrator Portal', badge: '🛡️ System Administrator', color: 'bg-red-100 text-red-800' };
      default:
        return { label: 'Consumer & Health Portal', badge: '🥗 Wellness User', color: 'bg-emerald-100 text-emerald-800' };
    }
  };

  const roleInfo = getRoleDisplay();

  return (
    <div className="min-h-screen bg-[#fbfcf9] py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Welcome Header */}
        <div className="bg-gradient-to-r from-agro-950 via-agro-900 to-agro-800 rounded-3xl p-6 sm:p-10 text-white shadow-xl relative overflow-hidden">
          <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-green-500/10 rounded-full blur-3xl pointer-events-none"></div>
          
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-3">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/20 border border-green-400/30 text-green-300 text-xs font-bold tracking-wide">
                <Sparkles className="w-3.5 h-3.5" />
                {roleInfo.badge}
              </div>
              <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
                Welcome back, <span className="text-green-400">{user.fullName}</span>
              </h1>
              <p className="text-sm text-green-100/80 max-w-xl">
                Your AGRO AI command center is ready. Access crop & soil diagnostics, generate scientific 7-day personalized diet plans, or consult the agricultural assistant.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
              <div className="bg-white/10 backdrop-blur-md px-4 py-3 rounded-2xl border border-white/10 text-xs flex items-center gap-3">
                <Calendar className="w-4 h-4 text-green-300" />
                <div>
                  <p className="text-gray-300 text-[10px]">Today's Date</p>
                  <p className="font-bold text-white">{new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* SECTION: THREE PRIMARY PILLARS */}
        <div>
          <div className="flex items-center justify-between mb-5">
            <div>
              <h2 className="text-xl font-extrabold text-agro-950">Core Platform Modules</h2>
              <p className="text-xs text-gray-500">Access Better Production, Better Nutrition, or consult your AI Assistant</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Pillar 1: Better Production */}
            <div className="bg-white rounded-3xl p-7 border border-gray-200 shadow-card hover:shadow-xl transition-all duration-300 flex flex-col justify-between group hover:border-emerald-500">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="w-14 h-14 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center group-hover:scale-105 transition-transform">
                    <Sprout className="w-7 h-7 text-emerald-700" />
                  </div>
                  <span className="text-xs font-bold tracking-wide text-emerald-700 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200 flex items-center gap-1">
                    <Sparkles className="w-3 h-3 text-emerald-600" />
                    Diagnostics & CV
                  </span>
                </div>

                <h3 className="text-2xl font-bold text-agro-950 mb-2">Better Production</h3>
                <p className="text-xs text-gray-600 leading-relaxed mb-6">
                  Computer vision intelligence for plant health inspection, leaf & stem condition diagnosis, and pedological soil category assessment.
                </p>

                <div className="space-y-2.5 mb-6">
                  <Link
                    to="/plants"
                    className="flex items-center justify-between p-3.5 rounded-xl bg-gradient-to-r from-emerald-50 to-green-50 hover:from-emerald-100 hover:to-green-100 text-xs font-bold text-emerald-950 transition-colors border border-emerald-200"
                  >
                    <span className="flex items-center gap-2.5">
                      <Sparkles className="w-4 h-4 text-emerald-700" />
                      <div>
                        <div className="font-bold text-emerald-950">Plant Analysis</div>
                        <div className="text-[10px] text-gray-500 font-normal">Leaf, stem & flower condition & care tips</div>
                      </div>
                    </span>
                    <ChevronRight className="w-4 h-4 text-emerald-800" />
                  </Link>

                  <Link
                    to="/production/soil"
                    className="flex items-center justify-between p-3.5 rounded-xl bg-amber-50 hover:bg-amber-100 text-xs font-bold text-amber-950 transition-colors border border-amber-200"
                  >
                    <span className="flex items-center gap-2.5">
                      <Layers className="w-4 h-4 text-amber-700" />
                      <div>
                        <div className="font-bold text-amber-950">Soil Assessment</div>
                        <div className="text-[10px] text-gray-500 font-normal">Visual soil type & crop suitability</div>
                      </div>
                    </span>
                    <ChevronRight className="w-4 h-4 text-amber-600" />
                  </Link>
                </div>
              </div>

              <Link
                to="/production"
                className="w-full inline-flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs shadow-md transition-colors"
              >
                Open Production Hub
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            {/* Pillar 2: Better Nutrition */}
            <div className="bg-white rounded-3xl p-7 border border-gray-200 shadow-card hover:shadow-xl transition-all duration-300 flex flex-col justify-between group hover:border-emerald-500">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="w-14 h-14 rounded-2xl bg-green-100 text-green-800 flex items-center justify-center group-hover:scale-105 transition-transform">
                    <HeartPulse className="w-7 h-7 text-green-700" />
                  </div>
                  <span className="text-xs font-bold tracking-wide text-green-700 bg-green-50 px-3 py-1 rounded-full border border-green-200 flex items-center gap-1">
                    <Sparkles className="w-3 h-3 text-green-600" />
                    Wellness & Diet
                  </span>
                </div>

                <h3 className="text-2xl font-bold text-agro-950 mb-2">Better Nutrition</h3>
                <p className="text-xs text-gray-600 leading-relaxed mb-6">
                  Scientific BMR & TDEE calorie calculation and customized 7-day meal plans (5 meals/day) tailored to allergies and preferences.
                </p>

                <div className="bg-green-50/70 p-3.5 rounded-xl border border-green-100 mb-6 space-y-1.5 text-xs text-green-950 font-medium">
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-green-600 shrink-0" />
                    <span>Harris-Benedict / Mifflin-St Jeor Formulas</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-green-600 shrink-0" />
                    <span>Day 1 through Day 7 meal breakdown</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-green-600 shrink-0" />
                    <span>Strict allergen and cuisine filtering</span>
                  </div>
                </div>
              </div>

              <Link
                to="/nutrition"
                className="w-full inline-flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-green-700 hover:bg-green-800 text-white font-bold text-xs shadow-md transition-colors"
              >
                Plan 7-Day Nutrition
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            {/* Pillar 3: AGRO AI Assistant */}
            <div className="bg-white rounded-3xl p-7 border border-gray-200 shadow-card hover:shadow-xl transition-all duration-300 flex flex-col justify-between group hover:border-indigo-500">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="w-14 h-14 rounded-2xl bg-indigo-100 text-indigo-800 flex items-center justify-center group-hover:scale-105 transition-transform">
                    <BotMessageSquare className="w-7 h-7 text-indigo-700" />
                  </div>
                  <span className="text-xs font-bold tracking-wide text-indigo-700 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-200 flex items-center gap-1">
                    <Sparkles className="w-3 h-3 text-indigo-600" />
                    AI Assistant
                  </span>
                </div>

                <h3 className="text-2xl font-bold text-agro-950 mb-2">AGRO AI Assistant</h3>
                <p className="text-xs text-gray-600 leading-relaxed mb-6">
                  Intelligent conversational assistant for agronomy, organic fertilizers, soil amendments, disease remedies, and nutrition.
                </p>

                <div className="bg-indigo-50/70 p-3.5 rounded-xl border border-indigo-100 mb-6 space-y-1.5 text-xs text-indigo-950 font-medium">
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-indigo-600 shrink-0" />
                    <span>Zero external API keys or cloud tokens</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-indigo-600 shrink-0" />
                    <span>Domain knowledge base integration</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-indigo-600 shrink-0" />
                    <span>Instant response time & offline fallback</span>
                  </div>
                </div>
              </div>

              <Link
                to="/assistant"
                className="w-full inline-flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-indigo-700 hover:bg-indigo-800 text-white font-bold text-xs shadow-md transition-colors"
              >
                Start Chat Conversation
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>

        {/* Recent Analysis Activity */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Clock className="w-5 h-5 text-gray-500" />
              <h3 className="text-lg font-bold text-gray-900">Recent Production Analysis</h3>
            </div>
            <Link to="/production" className="text-xs font-bold text-green-700 hover:underline">
              Analyze New Image →
            </Link>
          </div>

          {loadingHistory ? (
            <p className="text-xs text-gray-400 py-4 text-center">Loading analysis history...</p>
          ) : history.length > 0 ? (
            <div className="divide-y divide-gray-100">
              {history.map((item) => (
                <div key={item.id} className="py-3 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-green-50 text-green-700 flex items-center justify-center text-xs font-bold">
                      {item.type === 'crop' ? '🌿' : '🪨'}
                    </div>
                    <div>
                      <p className="text-xs font-bold text-gray-800">{item.predictedClass}</p>
                      <p className="text-[11px] text-gray-400">{item.date}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-xs font-bold text-green-700">
                      {(item.confidence * 100).toFixed(1)}% Confidence
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-400 text-xs space-y-2">
              <p>No recent image scans recorded yet.</p>
              <Link
                to="/production/crop"
                className="inline-block px-4 py-2 bg-green-50 text-green-700 font-bold rounded-lg hover:bg-green-100 transition-colors"
              >
                Scan your first crop or soil photo
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
